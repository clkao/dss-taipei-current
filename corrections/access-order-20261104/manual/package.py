"""Finalize the DSS corrected local package after rendering and PDF review."""
import hashlib,json,zipfile,os,re,base64,gzip
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=ROOT/'builds/access-corrected';PUB=Path('/Users/clkao/git/dss-taipei-current')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,data):
 if p.is_symlink():p.unlink()
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
m=load(D/'model.json');page=load(D/'pdf-page-map.json');source=load(ROOT/'sources/minifigure/legacy-v10/model.json')
assert [{k:v for k,v in p.items() if k!='step'} for p in m['pieces']]==[{k:v for k,v in p.items() if k!='step'} for p in source['pieces']]
introductions=[i for o in m['build_operations'] for i in o['ids']];assert len(introductions)==len(set(introductions))==348
assert sha(D/'yangliu-shape.mpd')==sha(ROOT/'sources/minifigure/legacy-v10/source.mpd')
sheets=[r['page'] for r in page['page_records'] if r['kind'] in ['sticker-sheet','speech-bubble-print-sheet']];assert len(sheets)==2
scene=load(D/'render-scene.json');scene.setdefault('geometry_source_model_sha256',scene['model_sha256']);scene['model_sha256']=sha(D/'model.json');write(D/'render-scene.json',scene)
h=(D/'viewer.html').read_text().replace('pages 94–95',f'pages {sheets[0]}–{sheets[1]}').replace('Test-build edition. Physical grip, suspension and handling strength remain untested.','Access-order correction for review. Insertion clearance, physical grip, suspension and handling strength remain untested.')
h=re.sub(r'instructions\.pdf#page=\d+',f'instructions.pdf#page={sheets[0]}',h)
h=h.replace('Minifigure edition · local preview','Minifigure edition · Access-order correction')
match=re.search(r'atob\("([A-Za-z0-9+/=]+)"\)',h);assert match
payload=json.loads(gzip.decompress(base64.b64decode(match[1])));assert payload['placements']['instances']==scene['instances'];payload['placements']=scene
encoded=base64.b64encode(gzip.compress(json.dumps(payload,ensure_ascii=False).encode(),mtime=0)).decode();h=h[:match.start(1)]+encoded+h[match.end(1):]
(D/'viewer.html').write_text(h)
idx=D/'index.html'
if not idx.exists():idx.symlink_to('viewer.html')
write(D/'print-preflight.json',dict(pdf='instructions.pdf',pdf_sha256=sha(D/'instructions.pdf'),pages=page['pages'],print_sheets=[dict(page=n,contents=title) for n,title in zip(sheets,['Vehicle stickers','Two speech-bubble faces and jacket'])],scale='100% / actual size; check the 20 mm scale bar.',editable_sources='sticker-artwork.zip'))
# Keep every original editable artwork byte; replace only the obsolete page reference.
zpath=D/'sticker-artwork.zip';tmp=D/'sticker-artwork-new.zip'
old_artwork_sha256=sha(PUB/'sticker-artwork.zip')
with zipfile.ZipFile(PUB/'sticker-artwork.zip') as src,zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as dst:
 seen=set()
 for info in src.infolist():
  if info.filename in seen:continue
  seen.add(info.filename)
  data=src.read(info.filename)
  if info.filename=='PRINTING.txt':data=f'Print instructions.pdf pages {sheets[0]}–{sheets[1]} at 100% / actual size. Editable artwork bytes are unchanged from the retained release.\n'.encode()
  dst.writestr(info,data)
if zpath.is_symlink():zpath.unlink()
tmp.replace(zpath)
write(D/'full-instruction-check.json',dict(source_model_sha256=sha(ROOT/'sources/minifigure/legacy-v10/model.json'),candidate_model_sha256=sha(D/'model.json'),same_piece_records_except_introduction_step=True,unique_introductions=348,operations=len(m['build_operations']),main_steps=len(m['instruction_plan']['steps']),pdf_pages=page['pages'],model_mpd_unchanged=True,pdf_sha256=sha(D/'instructions.pdf'),limits='Identity and declared order only. Readability review is recorded separately. No physical or continuous insertion certification; no acceptance implied.'))
(D/'digital-fit-audit.md').write_text('''# Corrected instruction edition - evidence limits\n\nThe 348 rigid pieces and world poses are unchanged. The corrected sequence fits captive chassis pins before the second beam and ties, builds the complete nine-piece bumper before fitting the front dish, and builds each upper rail with every bracket before joining its carrier. Both side recipes are shown separately; prior shared-prefix/copy identity is retained in the source operations. The earlier bed-before-rear-trim order remains.\n\nRendered installed-state panels show explicit stock ownership and receiving context. They do not prove collision-free insertion, finger access, physical grip, stability or strength. Whole-carrier floor seating remains a separate unresolved dry-fit concern. The retained full199-operation/68-step audit distinguishes confirmed sequence conflicts from analogous suspected risks; none is converted into a physical pass here.\n\nThis local package awaits independent exact-package review and captain acceptance. Historical evidence and the unchanged publication remain separate.\n''')
(D/'README.txt').write_text('DSS Taipei Current / 洋流號 - Access-order correction. Open viewer.html offline; instructions.pdf contains the complete revised sequence. 348 unchanged rigid pieces, 67 main steps, 215 source-derived operations. Follow ordered panels. New-part highlights are installed states, not certified movements. Physical insertion, grip and strength remain unverified. See digital-fit-audit.md and full-instruction-check.json for scope. Rights and attribution remain in LICENSE.txt and credits.html.\n')
q=D/'sequence-audit.json'
if not q.exists():q.symlink_to(ROOT/'corrections/access-order-20261104/full-sequence-audit.json')
# Explicit publication file set. Generated diagnostic/render intermediates are not release assets.
names=['sequence-audit.json','model.json','instruction-plan.json','render-scene.json','catalog-meshes.json','index.html','viewer.html','instructions.pdf','pdf-page-map.json','full-instruction-check.json','print-preflight.json','digital-fit-audit.md','README.txt','sticker-artwork.zip','yangliu-shape.mpd','inventory.csv','wanted-list.xml','bricklink-inventory.csv','bricklink-mapping.json','LICENSE.txt','credits.html','physical-vehicle-attribution.json','contributor-count.json','soon-white.svg','soon-white-4096.png']
files={n:sha(D/n) for n in names if (D/n).is_file()}
write(D/'release-provenance.json',dict(edition=m['instruction_edition'],source_model_sha256=sha(ROOT/'sources/minifigure/legacy-v10/model.json'),candidate_model_sha256=sha(D/'model.json'),pieces=348,main_steps=67,operations=215,pdf_pages=page['pages'],retained_artwork_zip_sha256=old_artwork_sha256,generator='DSS-local adapter with retained house-demo renderer and PDF template',publication_changed=False,accepted=False,physical_tested=False,files=files))
files['release-provenance.json']=sha(D/'release-provenance.json')
with zipfile.ZipFile(D/'release.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in files:
  if n!='index.html':z.write(D/n,n)
 for name in ['licenses','tsai-banner','ldraw']:
  if not (D/name).exists():continue
  for parent,dirs,fnames in os.walk(D/name,followlinks=True):
   for f in fnames:
    p=Path(parent)/f;z.write(p,p.relative_to(D).as_posix())
files['release.zip']=sha(D/'release.zip')
write(D/'package-manifest.json',dict(edition='access-order-20261104',accepted=False,files=files,retained_unmodified=['technic/'],limits='Final review/acceptance is separate; package generation does not certify insertion or physical performance.'))
print(json.dumps(dict(package=str(D),pdf_pages=page['pages'],print_pages=sheets,files=len(files))))

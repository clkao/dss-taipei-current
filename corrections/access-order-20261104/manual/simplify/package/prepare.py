"""Static package integration. No PDF/render/browser; fail on existing output."""
from pathlib import Path
import hashlib,json,re,shutil,time,zipfile,copy
P=Path(__file__).resolve().parent;R=P.parents[4]
OLD=R/'builds/access-corrected-hybrid-prefix';PDF=R/'builds/simplification-i3-polish';B=R/'builds/simplification-package-retry1'
pins=json.loads((P/'inputs.json').read_text());start=time.monotonic()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def guard():
 assert time.monotonic()-start<60 and shutil.disk_usage(R).free>=512*1024**2
assert shutil.disk_usage(R).free>=576*1024**2
for n,h in pins.items():assert sha(R/n)==h,n
assert not B.exists() and not B.is_symlink()
base=json.loads((OLD/'package-manifest.json').read_text());page=json.loads((PDF/'pdf-page-map.json').read_text())
sheets=[x['page'] for x in page['page_records'] if x['kind'] in ['sticker-sheet','speech-bubble-print-sheet']]
assert page['pages']==69 and sheets==[61,62]
# All modified names become NEW regular files. Only immutable inputs are linked.
modified={'index.html','viewer.html','README.txt','full-instruction-check.json','print-preflight.json','sticker-artwork.zip','release-provenance.json','release.zip'}
B.mkdir()
for n,h in base['files'].items():
 assert sha(OLD/n)==h,n
 if n in modified:continue
 source=PDF/n if n in ['instructions.pdf','pdf-page-map.json'] else R/'builds/simplification-i2-assets/numbers-only.png' if n=='ordered-prefix.png' else OLD/n
 (B/n).symlink_to(source.resolve())
def write(n,data):
 p=B/n;assert not p.exists() and not p.is_symlink(),n
 p.write_bytes(data if isinstance(data,bytes) else data.encode())
def js(n,value):write(n,json.dumps(value,ensure_ascii=False,indent=2)+'\n')
for n in ['index.html','viewer.html']:
 old=(OLD/n).read_text();assert old.count('pages 128–129')==old.count('instructions.pdf#page=128')==old.count('Download instructions (PDF)')==1
 new=old.replace('pages 128–129','pages 61–62').replace('instructions.pdf#page=128','instructions.pdf#page=61').replace('Download instructions (PDF)','Build instructions (69-page PDF)')
 assert re.findall(r'<script\b.*?</script>',old,re.S)==re.findall(r'<script\b.*?</script>',new,re.S)
 write(n,new)
write('README.txt','DSS Taipei Current / 洋流號. Build with instructions.pdf (69 pages); print sheets61–62 at100% actual size. viewer.html is an alternate detailed inspection sequence: eight-piece lower base2x, then separate source-ordered rails. The preferred PDF repeats base8+rail4+rail3 each2x, with distinct C17/C18 order and separate carrier placements. These presentations share348 rigid pieces,215 operations and67 main identities; PDF pagination is not viewer navigation. The first three actions share the numbers-only diagram. Original source geometry, rights and artwork are unchanged. Physical/insertion AC2 and native UI AC4 remain unproven; no native adoption or acceptance is implied. See credits.html and LICENSE.txt.\n')
check=json.loads((OLD/'full-instruction-check.json').read_text());check.update(pdf_pages=69,pdf_sha256=sha(B/'instructions.pdf'),pdf_composition_review='eb1d9f6; exact PDF only',package_review='pending',viewer_scope='retained detailed sequence; not PDF pagination');js('full-instruction-check.json',check)
pre=json.loads((OLD/'print-preflight.json').read_text());pre.update(pages=69,pdf_sha256=sha(B/'instructions.pdf'))
for row,n in zip(pre['print_sheets'],sheets):row['page']=n
js('print-preflight.json',pre)
with zipfile.ZipFile(OLD/'sticker-artwork.zip') as src,zipfile.ZipFile(B/'sticker-artwork.zip','x') as dst:
 assert src.namelist().count('PRINTING.txt')==1
 for info in src.infolist():dst.writestr(info,b'Print instructions.pdf pages61-62 at100% / actual size. Check the20mm scale bar. Editable artwork unchanged.\n' if info.filename=='PRINTING.txt' else src.read(info.filename))
with zipfile.ZipFile(OLD/'sticker-artwork.zip') as a,zipfile.ZipFile(B/'sticker-artwork.zip') as b:
 assert a.namelist()==b.namelist()
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='PRINTING.txt')
guard()
files={n:sha(B/n) for n in base['files'] if n not in ['release.zip','release-provenance.json']}
prov=json.loads((OLD/'release-provenance.json').read_text());prov.update(pdf_pages=69,files=dict(files),accepted=False,publication_changed=False)
prov['hybrid_section'].update(diagram_sha256=sha(B/'ordered-prefix.png'),producer='Local DSS numbers-only derivative of retained experimental shared projection',section_acceptance='pending exact package review',native_studfleet_adopted=False)
prov['simplification']={'pdf_review':'eb1d9f6;69-page composition only','iterations':[71,71,69],'source':'manual/simplify/i3','viewer':'retained detailed alternate; only base8 deduplicated2x','pdf':'base8+rail4+rail3 each2x; C17/C18 distinct order','physical_AC2':False,'native_UI_AC4':False,'package_review':'pending'}
js('release-provenance.json',prov);files['release-provenance.json']=sha(B/'release-provenance.json')
# Stream unchanged archive members; never extract or duplicate a retained archive.
with zipfile.ZipFile(OLD/'release.zip') as src,zipfile.ZipFile(B/'release.zip','x') as dst:
 for info in src.infolist():
  guard()
  with dst.open(copy.copy(info),'w') as out:
   if info.filename in files:
    with (B/info.filename).open('rb') as inp:shutil.copyfileobj(inp,out,1024*1024)
   else:
    with src.open(info) as inp:shutil.copyfileobj(inp,out,1024*1024)
files['release.zip']=sha(B/'release.zip');manifest=dict(base);manifest.update(files=files,accepted=False);js('package-manifest.json',manifest)
with zipfile.ZipFile(B/'release.zip') as z,zipfile.ZipFile(OLD/'release.zip') as old:
 assert z.namelist()==old.namelist()
 for n in z.namelist():
  def zh(archive):
   h=hashlib.sha256()
   with archive.open(n) as f:
    for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
   return h.hexdigest()
  assert zh(z)==(files[n] if n in files else zh(old)),n
assert all(sha(B/n)==h for n,h in files.items())
assert sha(B/'instructions.pdf')==pins['builds/simplification-i3-polish/instructions.pdf']
for n in modified|{'package-manifest.json'}:assert (B/n).is_file() and not (B/n).is_symlink()
rows=[{'publication_path':n,'source':str(B/n),'sha256':sha(B/n),'previous_sha256':sha(OLD/n)} for n in list(files)+['package-manifest.json']]
js('publication-file-map.json',{'baseline':'24425a3cd5c0e925fe8922425fde7630b5177f7c','files':rows,'publication_changed':False,'preserve':['technic/','unrelated paths']})
newbytes=sum(p.stat().st_size for p in B.iterdir() if not p.is_symlink());assert newbytes<64*1024**2;guard()
js('package-check.json',{'scripts_byte_identical':True,'archive_member_hashes_verified':True,'artwork_except_PRINTING_unchanged':True,'pdf_pages':69,'print_pages':sheets,'new_regular_bytes':newbytes,'elapsed_seconds':time.monotonic()-start,'review':'pending','accepted':False})
print(B)

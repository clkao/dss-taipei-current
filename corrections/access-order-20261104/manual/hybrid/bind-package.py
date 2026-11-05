"""One bounded static package rebind; no renderer/PDF/browser invocation."""
from pathlib import Path
import hashlib,json,re,zipfile,time,shutil
P=Path(__file__).resolve().parent;R=P.parents[3];B=R/'builds/access-corrected-hybrid-prefix';OLD=R/'builds/access-corrected-r2'
start=time.monotonic();minimum=shutil.disk_usage(R).free
assert minimum>=576*1024**2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check_budget():
 global minimum
 minimum=min(minimum,shutil.disk_usage(R).free)
 assert minimum>=512*1024**2 and time.monotonic()-start<30
writable=['index.html','viewer.html','README.txt','full-instruction-check.json','print-preflight.json','sticker-artwork.zip','release-provenance.json','package-manifest.json','release.zip']
for n in writable:
 q=B/n;assert not q.is_symlink(), 'Refuse linked write: '+n
 assert q.exists()==(n in ['index.html','viewer.html']), 'Unexpected existing output: '+n
assert sha(OLD/'package-manifest.json')=='cbccba603b3a6a5076b677e704d6ba78f987f40c7945099e1b9c91635b8961f6'
assert sha(OLD/'release.zip')=='976b234297c15e57f162ce7524144d114e41c1099e91ed67cd242c2989dcfd20'
assert sha(B/'instructions.pdf')=='6d02aa7dbf0e9fc58cbc4f963bd9fbe805bba9a1cdd134a1ecc3d1b22e9ac062'
assert sha(B/'pdf-page-map.json')=='5aee7e6fd9b08d304a9335e424d1a61cde45395f041053f45fe4fb2c55e9dc78'
assert sha(B/'viewer.html')=='6f00c106ad2decca8f8bb6b868956ef8da0da1428dfa0fbbe972e5203e1d836f'
assert sha(B/'index.html')=='098bd2d1a7df43b3844b270bb9a7607d12901e24db538fec1fecb7bb5d35dc72'
base=json.loads((OLD/'package-manifest.json').read_text());before={n:sha(B/n) for n in base['files'] if (B/n).exists()};before['pdf-page-map.json']=sha(B/'pdf-page-map.json')
page=json.loads((B/'pdf-page-map.json').read_text());sheets=[x['page'] for x in page['page_records'] if x['kind'] in ['sticker-sheet','speech-bubble-print-sheet']];assert page['pages']==136 and sheets==[128,129]
retained=B/'before-package-bind';retained.mkdir()
def write(n,value):
 assert n in writable and not (B/n).is_symlink()
 (B/n).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
for n in ['index.html','viewer.html']:
 old=(B/n).read_text();assert old.count('pages 130–131')==old.count('instructions.pdf#page=130')==1
 new=old.replace('pages 130–131','pages 128–129').replace('instructions.pdf#page=130','instructions.pdf#page=128')
 assert re.findall(r'<script\b.*?</script>',old,re.S)==re.findall(r'<script\b.*?</script>',new,re.S)
 (B/n).rename(retained/n);(B/n).write_text(new)
(B/'README.txt').write_text((OLD/'README.txt').read_text()+'Hybrid section: the first three source actions share one diagram. The PDF has 136 pages; print sheets are pages 128–129. Diagram producer: experimental StudFleet task66 projection, integrated by the DSS legacy composer; native StudFleet adoption and physical insertion remain unverified.\n')
check=json.loads((OLD/'full-instruction-check.json').read_text());check.update(pdf_pages=136,pdf_sha256=sha(B/'instructions.pdf'));write('full-instruction-check.json',check)
preflight=json.loads((OLD/'print-preflight.json').read_text());preflight.update(pdf_sha256=sha(B/'instructions.pdf'),pages=136)
for row,n in zip(preflight['print_sheets'],sheets):row['page']=n
write('print-preflight.json',preflight)
# No extraction and no filesystem PRINTING.txt write. Rewrite just this ZIP member.
with zipfile.ZipFile(OLD/'sticker-artwork.zip') as src,zipfile.ZipFile(B/'sticker-artwork.zip','w') as dst:
 assert src.namelist().count('PRINTING.txt')==1
 for info in src.infolist():
  data=src.read(info.filename)
  if info.filename=='PRINTING.txt':data=b'Print instructions.pdf pages 128\xe2\x80\x93129 at 100% / actual size. Editable artwork bytes are unchanged from the retained release.\n'
  dst.writestr(info,data)
with zipfile.ZipFile(OLD/'sticker-artwork.zip') as a,zipfile.ZipFile(B/'sticker-artwork.zip') as b:
 assert a.namelist()==b.namelist()
 assert all(a.read(n)==b.read(n) for n in a.namelist() if n!='PRINTING.txt')
check_budget()
names=[n for n in base['files'] if n not in ['release.zip','release-provenance.json']]+['ordered-prefix.png']
files={n:sha(B/n) for n in names};prov=json.loads((OLD/'release-provenance.json').read_text());prov.update(pdf_pages=136,files=dict(files),accepted=False,publication_changed=False)
prov['hybrid_section']={'source_operations':['legacy-001a','legacy-012','legacy-001b'],'piece_ids':[172,216,231,178],'page':4,'diagram_sha256':sha(B/'ordered-prefix.png'),'producer':'StudFleet task66 experimental projection; DSS legacy PDF composer and viewer adapter','upstream_source':'a3972ea','asset_binding_sha256':'b5669accd2c7a101fd0c0172d32a6320ef9d6774ae104a015f11c79e642127fa','native_studfleet_adopted':False,'section_acceptance':'pending independent integrated artifact review','physical_tested':False}
write('release-provenance.json',prov);files['release-provenance.json']=sha(B/'release-provenance.json')
with zipfile.ZipFile(OLD/'release.zip') as src,zipfile.ZipFile(B/'release.zip','w') as dst:
 for info in src.infolist():dst.writestr(info,(B/info.filename).read_bytes() if info.filename in files else src.read(info.filename))
 assert 'ordered-prefix.png' not in src.namelist();dst.write(B/'ordered-prefix.png','ordered-prefix.png')
files['release.zip']=sha(B/'release.zip');manifest=dict(base);manifest['files']=files;write('package-manifest.json',manifest)
with zipfile.ZipFile(B/'release.zip') as z,zipfile.ZipFile(OLD/'release.zip') as oldz:
 for n in z.namelist():
  if n in files:assert hashlib.sha256(z.read(n)).hexdigest()==files[n]
  else:assert z.read(n)==oldz.read(n)
assert all(sha(B/n)==h for n,h in files.items())
assert all(sha(B/n)==h for n,h in before.items() if n not in writable)
assert sha(B/'credits.html')=='0d9e0d055958a4a256253f9715f9856bd452af67d677a99eb49d7ef025b6b367'
for n in ['index.html','viewer.html','README.txt']:
 text=re.sub(r'<script\b.*?</script>','',(B/n).read_text(),flags=re.S)
 assert not re.search(r'(?:pages?\s+130[–-]131|#page=130|138[- ]page)',text)
check_budget();outsize=sum((B/n).stat().st_size for n in writable)+sum(p.stat().st_size for p in retained.iterdir());assert outsize<=60*1024**2
allnames=names+['release-provenance.json','release.zip','package-manifest.json'];rows=[]
for n in allnames:rows.append({'source':str(B/n),'publication_path':n,'sha256':sha(B/n),'previous_sha256':sha(OLD/n) if (OLD/n).exists() else None,'action':'reuse unchanged' if (OLD/n).exists() and sha(OLD/n)==sha(B/n) else 'replace' if (OLD/n).exists() else 'add'})
(B/'hybrid-publication-file-map.json').write_text(json.dumps({'baseline_publication':'2105eb69bbc60228fe0eb5a49cd2242db0d0469a','files':rows,'preserve':['technic/','all unrelated publication paths'],'publication_changed':False},indent=2)+'\n')
result={'elapsed_seconds':time.monotonic()-start,'min_free_bytes':minimum,'conservative_output_bytes':outsize,'pdf_sha256':sha(B/'instructions.pdf'),'map_sha256':sha(B/'pdf-page-map.json'),'files':{n:sha(B/n) for n in allnames},'HTML_scripts_payload_handlers_unchanged':True,'artwork_members_unchanged_except_PRINTING':True,'all_manifest_archive_hashes_pass':True,'actual_print_pages':sheets,'native_studfleet_adopted':False,'accepted':False,'publication_changed':False}
(B/'hybrid-package-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

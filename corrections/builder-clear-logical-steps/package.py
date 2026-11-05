"""Bind one local candidate and its offline page viewer; never publish."""
from pathlib import Path
import json,hashlib,re,zipfile,shutil
from pypdf import PdfReader
R=Path(__file__).resolve().parents[2];B=R/'builds/clear-logical';O=B/'candidate';OLD=B/'simplification-package-retry1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert shutil.disk_usage(R).free>350*1024**2
mapping=json.loads((O/'pdf-page-map.json').read_text());n=mapping['pages'];pdf=PdfReader(O/'instructions.pdf');titles=[]
for rec,page in zip(mapping['page_records'],pdf.pages):
 text=page.extract_text().splitlines();titles.append(rec.get('title',text[2] if len(text)>2 else str(rec['page'])))
print_pages=[x['page'] for x in mapping['page_records'] if x['source_page'] in [61,62]]
immutable=['model.json','instruction-plan.json','yangliu-shape.mpd','inventory.csv','wanted-list.xml','bricklink-inventory.csv','bricklink-mapping.json','catalog-meshes.json','render-scene.json','LICENSE.txt','credits.html','digital-fit-audit.md','sequence-audit.json','ordered-prefix.png','soon-white-4096.png','soon-white.svg','physical-vehicle-attribution.json','contributor-count.json']
for name in immutable:
 dest=O/name
 if not dest.exists():dest.symlink_to((OLD/name).resolve())
oldviewer=(OLD/'viewer.html').read_text();viewer=oldviewer.replace('69-page PDF',f'{n}-page PDF').replace('pages 61–62',f'pages {print_pages[0]}–{print_pages[1]}').replace('instructions.pdf#page=61','instructions.pdf#page='+str(print_pages[0]))
assert re.findall(r'<script\b.*?</script>',oldviewer,re.S)==re.findall(r'<script\b.*?</script>',viewer,re.S)
(O/'model-viewer.html').write_text(viewer)
html=r'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>DSS Taipei Current — build guide</title><style>*{box-sizing:border-box}body{margin:0;background:#f7f4ee;color:#27333b;font:16px system-ui}header{padding:14px 20px;border-bottom:1px solid #d9d1c7;display:flex;gap:16px;align-items:center;flex-wrap:wrap}h1{font-size:20px;margin:0 auto 0 0}a{color:#a8422e}nav{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:14px 20px}button,select{font:inherit;padding:9px;max-width:100%}select{flex:1;min-width:160px}main{max-width:1400px;margin:auto}img{display:block;width:100%;height:auto}footer{padding:16px 20px;font-size:13px}button:disabled{opacity:.45}</style><header><h1>DSS Taipei Current / 洋流號</h1><a href="instructions.pdf">PDF</a><a id="enlarge" href="pages/page-01.jpg" target="_blank">Enlarge page</a><a href="model-viewer.html">3D inspection</a><a href="credits.html">Credits</a></header><nav aria-label="Instruction pages"><button id="prev">Previous</button><select id="pages" aria-label="Choose instruction page"></select><button id="next">Next</button><output id="position" aria-live="polite"></output></nav><main><img id="diagram" alt=""></main><footer>Local review candidate. Print the PDF at actual size. Physical fit and insertion clearance remain unverified.</footer><script>
const titles=TITLE_DATA;const select=document.querySelector('#pages'),img=document.querySelector('#diagram');let page=1;
titles.forEach((title,i)=>select.add(new Option((i+1)+' / '+title,String(i+1))));
function show(n){page=Math.max(1,Math.min(titles.length,n));select.value=String(page);img.src='pages/page-'+String(page).padStart(2,'0')+'.jpg';img.alt='Page '+page+': '+titles[page-1];document.querySelector('#enlarge').href=img.src;document.querySelector('#position').textContent=page+' / '+titles.length;document.querySelector('#prev').disabled=page===1;document.querySelector('#next').disabled=page===titles.length;history.replaceState(null,'','#page='+page)}
document.querySelector('#prev').onclick=()=>show(page-1);document.querySelector('#next').onclick=()=>show(page+1);select.onchange=()=>show(Number(select.value));addEventListener('keydown',e=>{if(e.target===select)return;if(e.key==='ArrowRight')show(page+1);if(e.key==='ArrowLeft')show(page-1)});show(Number(location.hash.match(/page=(\d+)/)?.[1]||1));window.inspectGuide=()=>({page,pages:titles.length,imageLoaded:img.complete&&img.naturalWidth>0,image:img.getAttribute('src'),title:titles[page-1]});
</script></html>'''.replace('TITLE_DATA',json.dumps(titles,ensure_ascii=False))
(O/'viewer.html').write_text(html);(O/'index.html').write_text(html)
(O/'README.txt').write_text(f'DSS Taipei Current local review candidate. Open viewer.html for the {n}-page build guide; model-viewer.html retains the alternate 3D inspection sequence. instructions.pdf is the print master. Print sticker sheets {print_pages[0]}-{print_pages[1]} at 100% and check the scale bar. Geometry, colors, poses, inventory and source operation plan are unchanged. Focused cutaways omit surrounding parts only for visibility; no removal is prescribed. No physical-fit, insertion or human-acceptance claim. Publication is not authorized by this package.\n')
with zipfile.ZipFile(OLD/'sticker-artwork.zip') as src,zipfile.ZipFile(O/'sticker-artwork.zip','w') as dst:
 for info in src.infolist():dst.writestr(info,f'Print instructions.pdf pages {print_pages[0]}-{print_pages[1]} at actual size; check scale bar.\n'.encode() if info.filename=='PRINTING.txt' else src.read(info))
for name in ['full-instruction-check.json','print-preflight.json']:
 data=json.loads((OLD/name).read_text());data.update(pdf_pages=n,pages=n,pdf_sha256=sha(O/'instructions.pdf'),accepted=False,review='pending independent exact-package review')
 if 'print_sheets' in data:
  for row,num in zip(data['print_sheets'],print_pages):row['page']=num
 (O/name).write_text(json.dumps(data,indent=2)+'\n')
provenance={'schema':'dss-local-instruction-candidate/1','predecessor_pdf_sha256':sha(OLD/'instructions.pdf'),'pdf_sha256':sha(O/'instructions.pdf'),'model_sha256':sha(O/'model.json'),'plan_sha256':sha(O/'instruction-plan.json'),'pages':n,'print_pages':print_pages,'accepted':False,'published':False,'native_studfleet_adopted':False,'physical_verified':False,'headless_review_only':True,'source':'corrections/builder-clear-logical-steps','known_limits':['Target locators are source-position markers, not connector certification.','Cord length, slack and knot type remain unspecified.','Cutaways preserve part poses but omit surrounding context explicitly.','3D inspection retains its predecessor operation navigation; the primary guide follows PDF pages.']}
(O/'release-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
files={str(p.relative_to(O)):sha(p) for p in O.rglob('*') if p.is_file() and p.name not in ['focused-pages.pdf','release.zip','package-manifest.json','package-check.json']}
(O/'package-manifest.json').write_text(json.dumps({'schema':'dss-local-package/1','files':files,'accepted':False},indent=2)+'\n')
with zipfile.ZipFile(O/'release.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for name in [*files,'package-manifest.json']:z.write(O/name,name)
with zipfile.ZipFile(O/'release.zip') as z:
 assert set(z.namelist())==set(files)|{'package-manifest.json'}
 for name,h in files.items():assert hashlib.sha256(z.read(name)).hexdigest()==h,name
assert all(sha(O/name)==sha(OLD/name) for name in immutable)
(O/'package-check.json').write_text(json.dumps({'immutable_files_verified':immutable,'archive_members_verified':len(files)+1,'zip_sha256':sha(O/'release.zip'),'pages':n,'print_pages':print_pages,'new_viewer_sha256':sha(O/'viewer.html'),'pdf_sha256':sha(O/'instructions.pdf'),'remaining_free_bytes':shutil.disk_usage(R).free,'independent_review':'pending'},indent=2)+'\n')
print(json.dumps(provenance,indent=2))

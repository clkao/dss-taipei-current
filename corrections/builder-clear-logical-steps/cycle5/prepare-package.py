"""Reuse unchanged package members; rasterize only corrected pages. Archive last."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys,zipfile,time
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';OLD=B/'cycle4/package';O=B/'cycle5/package';P=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changed=list(range(4,80))
assert sha(OLD/'instructions.pdf')=='89c7b5aee2ce4584e8bc9fc6bce6dfe92f997b8cca06cc6d1f2de28cdb1da28f'
assert sha(OLD/'viewer.html')=='4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865'
assert sha(OLD/'release.zip')=='06689b907c4780982ace5ac8acfdfa60b3ca3677bdbaab6a72017f658e21f1e1'
start=time.monotonic();minimum=shutil.disk_usage(R).free
assert minimum>=576*1024**2,'Admission requires 576 MiB free'
def guard():
 global minimum
 minimum=min(minimum,shutil.disk_usage(R).free)
 assert minimum>=512*1024**2,'Active disk floor'
 assert time.monotonic()-start<120,'Bounded local operation exceeded time budget'
oldmanifest=json.loads((OLD/'package-manifest.json').read_text())
if '--archive' not in sys.argv:
 modified={'index.html','model.json','instruction-plan.json','operation-crosswalk.json','model-viewer.html','viewer.html','pages/page-80.jpg','instructions.pdf','pdf-page-map.json','release-provenance.json','full-instruction-check.json','print-preflight.json','README.txt'}|{f'pages/page-{n:02d}.jpg' for n in changed}
 for name,h in oldmanifest['files'].items():
  assert sha(OLD/name)==h,name
  if name in modified:continue
  dest=O/name;dest.parent.mkdir(exist_ok=True,parents=True)
  if not dest.exists():dest.symlink_to((OLD/name).resolve())
 for n in ([int(v) for v in sys.argv[sys.argv.index('--raster-pages')+1].split(',') if v] if '--raster-pages' in sys.argv else changed):
  guard();path=O/'pages'/f'page-{n:02d}.jpg';assert not path.is_symlink()
  subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1200','-jpeg','-jpegopt','quality=80',str(O/'instructions.pdf'),str(path.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 for name in ['full-instruction-check.json','print-preflight.json']:
  data=json.loads((OLD/name).read_text());data.update(pdf_sha256=sha(O/'instructions.pdf'),pages=79,pdf_pages=79,review='captain follow-up: pending direct judgment',accepted=False)
  if name=='print-preflight.json':
   for sheet in data['print_sheets']:sheet['page']-=1
  else:data.update(candidate_model_sha256=sha(O/'model.json'),edition_plan_sha256=sha(O/'instruction-plan.json'),order_exception='Original44 before43;46 before45;72 before71; all other operation order exact',pdf_composition_review='Captain follow-up cycle5; author check, acceptance pending')
  (O/name).write_text(json.dumps(data,indent=2)+'\n')
 data=json.loads((OLD/'release-provenance.json').read_text());data.update(pdf_sha256=sha(O/'instructions.pdf'),correction_round='captain-follow-up',rejected_pdf_sha256=sha(OLD/'instructions.pdf'),affected_pages=changed,source='corrections/builder-clear-logical-steps/cycle5',pages=79,accepted=False,published=False)
 (O/'release-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
 (O/'README.txt').write_text('DSS Taipei Current / 洋流號. Use instructions.pdf or viewer.html. Print sheets71–72 at100% actual size. Geometry, stock, rights and artwork unchanged. Physical fit/insertion and native full-edition parity remain unverified.\n'+'Captain follow-up: 79 pages; shared named side-carrier methods with explicit rail-split variants; right loose short-rail operations71/72 swapped; coral step badges restored; rear-bed recipe pointer corrected. One authoritative derived plan drives PDF and3D inspection. Historical order exceptions43/44,45/46 remain. Exact package awaits direct captain judgment.\n')
 files={name:sha(O/name) for name in oldmanifest['files'] if name!='pages/page-80.jpg'};assert len(files)==108
 (O/'package-manifest.json').write_text(json.dumps({'schema':'dss-local-package/1','files':files,'accepted':False,'correction_round':'captain-follow-up'},indent=2)+'\n')
 (P/'prearchive-check.json').write_text(json.dumps({'pdf_sha256':sha(O/'instructions.pdf'),'viewer_sha256':sha(O/'viewer.html'),'affected_pages':changed,'unchanged_members':[n for n,h in files.items() if h==oldmanifest['files'][n]],'min_free_bytes':minimum,'elapsed_seconds':time.monotonic()-start,'archive_created':False},indent=2)+'\n')
 print('Affected-only package prepared; archive intentionally deferred until browser checks.')
else:
 assert not (O/'release.zip').exists(),'Do not replace bound successor archive'
 files=json.loads((O/'package-manifest.json').read_text())['files']
 with zipfile.ZipFile(O/'release.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for name in [*files,'package-manifest.json']:
   guard()
   with (O/name).open('rb') as src,z.open(name,'w') as dest:
    for chunk in iter(lambda:src.read(256*1024),b''):guard();dest.write(chunk)
 with zipfile.ZipFile(O/'release.zip') as z:
  assert set(z.namelist())==set(files)|{'package-manifest.json'}
  for name,h in files.items():assert sha(O/name)==h==hashlib.sha256(z.read(name)).hexdigest(),name
 guard();result={'pdf_sha256':sha(O/'instructions.pdf'),'viewer_sha256':sha(O/'viewer.html'),'zip_sha256':sha(O/'release.zip'),'package_manifest_sha256':sha(O/'package-manifest.json'),'archive_members_verified':len(files)+1,'min_free_bytes':minimum,'elapsed_seconds':time.monotonic()-start,'rejected_package_preserved':True,'accepted':False}
 (P/'package-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

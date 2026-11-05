"""Reuse unchanged package members; rasterize only corrected pages. Archive last."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys,zipfile,time
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';OLD=B/'cycle3/package';O=B/'cycle4/package';P=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();changed=[4,23,24,25,36]
assert sha(OLD/'instructions.pdf')=='c2cc842abc833241d8d543831d879c6273d9bfb9b12b05d4077afdd47de92ae0'
assert sha(OLD/'viewer.html')=='4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865'
assert sha(OLD/'release.zip')=='7427dbd7a7e642b61a852fc7840e8b4075c8494939b2220f22e48fe32e8bf533'
start=time.monotonic();minimum=shutil.disk_usage(R).free
assert minimum>=576*1024**2,'Admission requires 576 MiB free'
def guard():
 global minimum
 minimum=min(minimum,shutil.disk_usage(R).free)
 assert minimum>=512*1024**2,'Active disk floor'
 assert time.monotonic()-start<120,'Bounded local operation exceeded time budget'
oldmanifest=json.loads((OLD/'package-manifest.json').read_text())
if '--archive' not in sys.argv:
 modified={'instructions.pdf','pdf-page-map.json','release-provenance.json','full-instruction-check.json','print-preflight.json','README.txt'}|{f'pages/page-{n:02d}.jpg' for n in changed}
 for name,h in oldmanifest['files'].items():
  assert sha(OLD/name)==h,name
  if name in modified:continue
  dest=O/name;dest.parent.mkdir(exist_ok=True)
  if not dest.exists():dest.symlink_to((OLD/name).resolve())
 for n in changed:
  guard();path=O/'pages'/f'page-{n:02d}.jpg';assert not path.is_symlink()
  subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1200','-jpeg','-jpegopt','quality=80',str(O/'instructions.pdf'),str(path.with_suffix(''))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 for name in ['full-instruction-check.json','print-preflight.json']:
  data=json.loads((OLD/name).read_text());data.update(pdf_sha256=sha(O/'instructions.pdf'),review='correction captain follow-up: pending direct captain judgment',accepted=False)
  (O/name).write_text(json.dumps(data,indent=2)+'\n')
 data=json.loads((OLD/'release-provenance.json').read_text());data.update(pdf_sha256=sha(O/'instructions.pdf'),correction_round='captain-follow-up',rejected_pdf_sha256=sha(OLD/'instructions.pdf'),affected_pages=changed,source='corrections/builder-clear-logical-steps/cycle4',accepted=False,published=False)
 (O/'release-provenance.json').write_text(json.dumps(data,indent=2)+'\n')
 (O/'README.txt').write_text((OLD/'README.txt').read_text()+'Correction captain follow-up: orange continuous alignment paths, catalog stud endpoints and selected rear-bed camera. Exact package remains pending direct captain judgment.\n')
 files={name:sha(O/name) for name in oldmanifest['files']};assert set(files)==set(oldmanifest['files'])
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

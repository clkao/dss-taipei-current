"""One bounded local PDF experiment; adapted from retained hybrid/run-pdf.py."""
from pathlib import Path
import os,time,json,subprocess,hashlib,shutil,stat
R=Path.cwd();P=R/'corrections/access-order-20261104/manual/simplify/i2';D=R/'builds/simplification-i2';T=R/'tmp/simplification-i2';PY='/Users/clkao/git/house-demo/tmp/lego-standards-venv/bin/python'
start=time.monotonic();records=[];minimum=shutil.disk_usage(R).free;peak=0;peakrss=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not D.exists() and not T.exists() and minimum>=576*1024**2
pins=json.loads((P/'input-pins.json').read_text())
for name,value in pins.items():assert sha(R/name)==value,name
assert sha(Path(PY).resolve()).startswith('87d4df53')
T.mkdir(parents=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(T),TMP=str(T),TEMP=str(T))
def size():
 total=0
 for base in [D,T]:
  for root,dirs,files in os.walk(base,followlinks=False):
   for name in files:
    try:s=(Path(root)/name).stat(follow_symlinks=False)
    except FileNotFoundError:continue
    if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total

def run(argv,seconds,name):
 global minimum,peak,peakrss
 assert shutil.disk_usage(R).free>=576*1024**2
 began=time.monotonic();reason=None;identity=None
 with (T/(name+'.log')).open('w') as log:
  child=subprocess.Popen(argv,cwd=R,env=env,stdout=log,stderr=log)
  while child.poll() is None:
   rows=subprocess.check_output(['ps','-axo','pid=,ppid=,rss=,lstart=,command='],text=True).splitlines()
   row=next((r for r in rows if int(r.split()[0])==child.pid),None)
   if row:
    identity=identity or row;peakrss=max(peakrss,int(row.split()[2])*1024)
   minimum=min(minimum,shutil.disk_usage(R).free);peak=max(peak,size())
   if time.monotonic()-began>seconds-3 or time.monotonic()-start>157 or minimum<512*1024**2 or peak>160*1024**2 or peakrss>1024**3:
    reason='resource/deadline';child.terminate();break
   time.sleep(.1)
  try:code=child.wait(timeout=1)
  except subprocess.TimeoutExpired:child.kill();code=child.wait(timeout=1)
 census=subprocess.check_output(['ps','-axo','pid=,ppid=,command='],text=True).splitlines()
 survivors=[r for r in census if int(r.split()[0])==child.pid or int(r.split()[1])==child.pid]
 record=dict(argv=argv,exit=code,pid=child.pid,observed_identity=identity,explicit_parent_wait=True,survivors=survivors,elapsed_seconds=time.monotonic()-began,stop_reason=reason)
 records.append(record)
 (T/'run.json').write_text(json.dumps(dict(stages=records,elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak,observed_peak_direct_rss_bytes=peakrss),indent=2)+'\n')
 assert code==0 and not reason and not survivors,record
run([PY,str(P/'make_pdf.py')],90,'pdf')
run([PY,str(P/'check.py')],20,'check')
assert not (D/'a4-review').exists();(D/'a4-review').mkdir()
for n in [4,5,7,9,14,15,16,18,21,22,23,24,25,26,27,30,37,45,46,49,50,51,53,55,57,58,61]:
 run(['/opt/homebrew/bin/pdftoppm','-r','110','-png','-f',str(n),'-l',str(n),str(D/'instructions.pdf'),str(D/'a4-review/page')],min(8,max(3,157-(time.monotonic()-start))),'raster-'+str(n))
assert len(list((D/'a4-review').glob('*.png')))==27
minimum=min(minimum,shutil.disk_usage(R).free);peak=max(peak,size())
record=dict(stages=records,elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak,observed_peak_direct_rss_bytes=peakrss,pdf_sha256=sha(D/'instructions.pdf'),map_sha256=sha(D/'pdf-page-map.json'),rasters={f.name:sha(f) for f in sorted((D/'a4-review').glob('*.png'))},marker_repeated=False)
(D/'run.json').write_text(json.dumps(record,indent=2)+'\n');T.rename(D/'logs');print(json.dumps(record))

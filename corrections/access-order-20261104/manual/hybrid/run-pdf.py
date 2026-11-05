from pathlib import Path
import os,time,json,subprocess,hashlib,shutil,stat,sys
R=Path.cwd();D=R/'builds/access-corrected-hybrid-prefix';PYTHON='/Users/clkao/git/house-demo/tmp/lego-standards-venv/bin/python';start=time.monotonic();records=[];minimum=shutil.disk_usage(R).free;peak=0
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raster='--raster' in sys.argv
if raster:assert D.exists() and not (D/'a4-review').exists()
else:assert not D.exists()
TEMP=R/'tmp/hybrid-prefix-pdf-temp'
assert not TEMP.exists()
assert minimum>=576*1024**2
TEMP.mkdir(parents=True)
os.environ.update(TMPDIR=str(TEMP),TMP=str(TEMP),TEMP=str(TEMP),DSS_ORDERED_PREFIX='1',DSS_PDF_BUILD='builds/access-corrected-hybrid-prefix')
assert minimum>=576*1024**2
def size():
 total=0
 for x in list(D.rglob('*'))+list(TEMP.rglob('*')):
  try:s=x.stat(follow_symlinks=False)
  except FileNotFoundError:continue
  if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
base=size()
def run(argv,limit,budget,name):
 global minimum,peak
 assert shutil.disk_usage(R).free>=576*1024**2
 t=time.monotonic();stagebase=size();own=set();identities={};reason=None
 with (TEMP/(name+'.log')).open('w') as log:
  p=subprocess.Popen(argv,cwd=R,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log);own.add(p.pid)
  while p.poll() is None:
   rows=[list(map(int,l.split())) for l in subprocess.check_output(['ps','-axo','pid=,ppid='],text=True).splitlines()]
   for _ in range(4):own.update(pid for pid,ppid in rows if ppid in own)
   census={int(l.split(None,1)[0]):l.split(None,1)[1] for l in subprocess.check_output(['ps','-axo','pid=,lstart=,command='],text=True).splitlines()}
   for pid in own:
    if pid in census:identities.setdefault(pid,census[pid])
   minimum=min(minimum,shutil.disk_usage(R).free);sz=size();peak=max(peak,sz-base)
   if time.monotonic()-t>limit-3 or time.monotonic()-start>(27 if raster else 87) or minimum<512*1024**2 or sz-stagebase>budget*1024**2 or sz-base>(20 if raster else 100)*1024**2:
    reason='budget';p.terminate();break
   time.sleep(.1)
  exit=p.wait(timeout=2)
 remaining=[]
 for pid in own:
  try:os.kill(pid,0);remaining.append(pid)
  except ProcessLookupError:pass
 r=dict(argv=argv,exit=exit,pids=sorted(own),pid_identities=identities,remaining_pids=remaining,explicit_parent_wait=True,elapsed_seconds=time.monotonic()-t,stop_reason=reason);records.append(r)
 (TEMP/'run.json').write_text(json.dumps(dict(stages=records,elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak),indent=2))
 assert exit==0 and not remaining and not reason,r
P=R/'corrections/access-order-20261104/manual/hybrid'
if raster:
 (D/'a4-review').mkdir()
 for n in [3,4,5,128,129]:run(['/opt/homebrew/bin/pdftoppm','-r','110','-png','-f',str(n),'-l',str(n),str(D/'instructions.pdf'),str(D/'a4-review/page')],max(4,30-(time.monotonic()-start)),20,'raster-'+str(n))
 assert len(list((D/'a4-review').glob('*.png')))==5
else:
 run([PYTHON,str(P/'prepare.py')],10,20,'prepare')
 for name in ['hood-sticker-cut.png','hood-upper-sticker-guide.png','jacket-print.png']:
  assert not (D/name).exists() and not (D/name).is_symlink(), 'Generated guide must be absent before PDF: '+name
 run([PYTHON,str(P.parent/'make_pdf.py')],max(5,80-(time.monotonic()-start)),100,'pdf-create')
 run([PYTHON,str(P/'check-pdf.py')],max(4,90-(time.monotonic()-start)),100,'pdf-check')
record=dict(stages=records,elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak,pdf_sha256=sha(D/'instructions.pdf'),map_sha256=sha(D/'pdf-page-map.json'),marker_repeated=False)
if raster:record['rasters']={p.name:sha(p) for p in sorted((D/'a4-review').glob('*.png'))}
(D/('hybrid-raster-run.json' if raster else 'hybrid-generation-run.json')).write_text(json.dumps(record,indent=2))
# Retain owned logs; no deletion is used as process-closure proof.
TEMP.rename(D/('raster-logs' if raster else 'generation-logs'))
print(json.dumps(record))

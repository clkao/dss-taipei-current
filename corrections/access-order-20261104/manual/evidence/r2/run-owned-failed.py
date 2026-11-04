import os,time,json,subprocess,shutil,hashlib,signal,socket,sys
from pathlib import Path
cwd=Path.cwd();d=cwd/'builds/access-corrected-r2';profile=cwd/'tmp/yangliu-preview-chrome-c6da3312';start=time.monotonic();minimum=shutil.disk_usage(cwd).free;peak=0;own=set();reason=None
assert minimum>=576*1024**2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(d/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(d/'viewer.html')=='281f091079fd61c6820d28bff03e56208c074417ba5d25d899cd5151389ed3f5'
assert sha(cwd/'corrections/access-order-20261104/manual/review_r2.mjs')=='5b90524d5ba39ec193f58e5a2489de8dd479278ab029d59f43454dc3551751c3'
assert not profile.exists();sock=socket.socket();sock.bind(('127.0.0.1',19690));sock.close()
def size(p):return sum(x.stat().st_size for x in p.rglob('*') if x.is_file() and not x.is_symlink()) if p.exists() else 0
base=size(d)
argv=['/Users/clkao/.local/share/fnm/node-versions/v24.22.1/installation/bin/node',str(cwd/'corrections/access-order-20261104/manual/review_r2.mjs'),str(d)]
with (d/'r2-navigation-run.log').open('w') as log:
 p=subprocess.Popen(argv,cwd=cwd,stdout=log,stderr=log,start_new_session=True);own.add(p.pid)
 while True:
  rows=[list(map(int,l.split())) for l in subprocess.check_output(['ps','-axo','pid=,ppid='],text=True).splitlines()]
  for _ in range(6):own.update(pid for pid,ppid in rows if ppid in own)
  live=own&{pid for pid,ppid in rows};free=shutil.disk_usage(cwd).free;minimum=min(minimum,free);peak=max(peak,size(d)-base+size(profile))
  if time.monotonic()-start>80 or free<512*1024**2 or peak>150*1024**2:
   reason='budget';os.killpg(p.pid,signal.SIGTERM)
  if p.poll() is not None and not live:break
  if time.monotonic()-start>86:
   for pid in live:
    try:os.kill(pid,signal.SIGKILL)
    except ProcessLookupError:pass
   break
  time.sleep(.1)
 p.wait(timeout=2)
remaining=[]
for pid in own:
 try:os.kill(pid,0);remaining.append(pid)
 except ProcessLookupError:pass
if not remaining and profile.exists():shutil.rmtree(profile)
r=dict(argv=argv,cwd=str(cwd),exit=p.returncode,elapsed_seconds=time.monotonic()-start,started_unix=time.time()-(time.monotonic()-start),pids=sorted(own),remaining_pids=remaining,profile_removed=not profile.exists(),min_free_bytes=minimum,peak_increment_bytes=peak,stop_reason=reason)
(d/'r2-navigation-run.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));sys.exit(p.returncode)

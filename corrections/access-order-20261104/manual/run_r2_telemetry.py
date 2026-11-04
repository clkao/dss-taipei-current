"""One bounded diagnostic invocation; journal owned identities before waiting."""
import os,time,json,subprocess,shutil,hashlib,signal,socket
from pathlib import Path
R=Path(__file__).resolve().parents[3];D=R/'builds/access-corrected-r2';PROFILE=R/'tmp/yangliu-preview-chrome-c6da3312'
NODE='/Users/clkao/.local/share/fnm/node-versions/v24.22.1/installation/bin/node';HELPER=Path(__file__).with_name('review_r2_telemetry.mjs')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(D/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(D/'viewer.html')=='281f091079fd61c6820d28bff03e56208c074417ba5d25d899cd5151389ed3f5'
assert not PROFILE.exists();sock=socket.socket();sock.bind(('127.0.0.1',19690));sock.close()
assert shutil.disk_usage(R).free>=576*1024**2
start=time.monotonic();owned={};events=[];minimum=shutil.disk_usage(R).free;peak=0;stop=None;p=None
record={'argv':[NODE,str(HELPER),str(D)],'cwd':str(R),'helper_sha256':sha(HELPER),'started_unix':time.time(),'owned':owned,'events':events}
def scan():
 rows={}
 for line in subprocess.check_output(['ps','-axo','pid=,ppid=,lstart=,command='],text=True).splitlines():
  x=line.split(None,2)
  if len(x)==3:rows[int(x[0])]={'ppid':int(x[1]),'identity':x[2]}
 return rows
def size(path):return sum(x.stat().st_size for x in path.rglob('*') if x.is_file() and not x.is_symlink()) if path.exists() else 0
base=size(D)
def persist():
 record.update(elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak,stop_reason=stop,exit=p.poll() if p else None)
 (D/'r2-telemetry-run.json').write_text(json.dumps(record,indent=2))
def signal_owned(sig):
 rows=scan()
 for pid,identity in list(owned.items()):
  if rows.get(pid,{}).get('identity')!=identity:continue
  try:os.kill(pid,sig);events.append({'action':'signal','pid':pid,'signal':int(sig)})
  except (PermissionError,ProcessLookupError) as error:events.append({'action':'signal-error','pid':pid,'error':str(error)})
 persist()
try:
 with (D/'r2-telemetry-run.log').open('w') as log:
  p=subprocess.Popen(record['argv'],cwd=R,stdout=log,stderr=log,start_new_session=True)
  rows=scan();owned[p.pid]=rows.get(p.pid,{}).get('identity','missing-before-first-wait');persist()
  while True:
   rows=scan()
   for _ in range(6):
    for pid,item in rows.items():
     if item['ppid'] in owned and pid not in owned:owned[pid]=item['identity']
   live=[pid for pid,identity in owned.items() if rows.get(pid,{}).get('identity')==identity]
   minimum=min(minimum,shutil.disk_usage(R).free);peak=max(peak,size(D)-base+size(PROFILE));persist()
   if p.poll() is not None and not live:break
   if not stop and (time.monotonic()-start>75 or minimum<512*1024**2 or peak>150*1024**2):stop='time/disk/output budget';signal_owned(signal.SIGTERM)
   if stop and time.monotonic()-start>82:signal_owned(signal.SIGKILL)
   if time.monotonic()-start>86:break
   time.sleep(.1)
finally:
 rows=scan();remaining=[pid for pid,identity in owned.items() if rows.get(pid,{}).get('identity')==identity]
 record['remaining_owned_pids']=remaining;record['profile_bytes_before_cleanup']=size(PROFILE)
 if not remaining and PROFILE.exists():shutil.rmtree(PROFILE)
 record['profile_removed']=not PROFILE.exists();persist();print(json.dumps(record))
 if remaining or p is None or p.poll()!=0 or stop:raise SystemExit(1)

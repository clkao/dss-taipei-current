"""One bounded diagnostic invocation; journal owned identities before waiting."""
import os,time,json,subprocess,shutil,hashlib,signal,socket,stat,re
from pathlib import Path
R=Path(__file__).resolve().parents[5];D=R/'builds/simplification-i2-receivers';PROFILE=R/'tmp/yangliu-preview-chrome-f0c05ede'
NODE='/Users/clkao/.local/share/fnm/node-versions/v24.22.1/installation/bin/node';HELPER=Path(__file__).with_name('render-receivers.mjs')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not D.exists()
P=Path(__file__).parent
for name,value in json.loads((P/'receiver-pins.json').read_text()).items():assert sha(R/name)==value,name
assert not PROFILE.exists();sock=socket.socket();sock.bind(('127.0.0.1',19038));sock.close()
assert shutil.disk_usage(R).free>=576*1024**2
D.mkdir()
(D/'numbers-only.png').symlink_to(R/'builds/simplification-i2-assets/numbers-only.png')
(D/'temp').mkdir()
start=time.monotonic();owned={};events=[];minimum=shutil.disk_usage(R).free;peak=0;stop=None;p=None
record={'argv':[NODE,str(HELPER),str(D)],'cwd':str(R),'helper_sha256':sha(HELPER),'started_unix':time.time(),'owned':owned,'events':events}
def scan():
 rows={}
 for line in subprocess.check_output(['ps','-axo','pid=,ppid=,lstart=,command='],text=True).splitlines():
  x=line.split(None,2)
  if len(x)==3:rows[int(x[0])]={'ppid':int(x[1]),'identity':x[2]}
 return rows
def size(path):
 total=0
 for x in path.rglob('*'):
  try:entry=x.stat(follow_symlinks=False)
  except FileNotFoundError:continue
  if stat.S_ISREG(entry.st_mode):total+=entry.st_size
 return total
record['supervisor']={'pid':os.getpid(),'identity':scan()[os.getpid()]['identity'],'excluded_from_signal_targets':True}
base=size(D)
def persist():
 record.update(elapsed_seconds=time.monotonic()-start,min_free_bytes=minimum,peak_increment_bytes=peak,stop_reason=stop,exit=p.poll() if p else None)
 (D/'r2-telemetry-run.json').write_text(json.dumps(record,indent=2))
def signal_owned(sig):
 rows=scan()
 for pid,identity in list(owned.items()):
  if pid==record['supervisor']['pid'] or rows.get(pid,{}).get('identity')!=identity:continue
  try:os.kill(pid,sig);events.append({'action':'signal','pid':pid,'signal':int(sig)})
  except (PermissionError,ProcessLookupError) as error:events.append({'action':'signal-error','pid':pid,'error':str(error),'error_type':type(error).__name__})
 persist()
try:
 with (D/'r2-telemetry-run.log').open('w') as log:
  p=subprocess.Popen(record['argv'],cwd=R,stdout=log,stderr=log,start_new_session=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(D/'temp'),TMP=str(D/'temp'),TEMP=str(D/'temp')))
  rows=scan();owned[p.pid]=rows.get(p.pid,{}).get('identity','missing-before-first-wait');persist()
  while True:
   rows=scan()
   for _ in range(6):
    for pid,item in rows.items():
     if item['ppid'] in owned and pid not in owned:owned[pid]=item['identity']
   live=[pid for pid,identity in owned.items() if rows.get(pid,{}).get('identity')==identity]
   minimum=min(minimum,shutil.disk_usage(R).free);peak=max(peak,size(D)-base+size(PROFILE));persist()
   if p.poll() is not None and 'direct_node_reaped' not in record:record['direct_node_reaped']={'pid':p.pid,'exit':p.wait(),'explicit_wait':True};persist()
   if p.poll() is not None and not live:break
   if not stop and (time.monotonic()-start>75 or minimum<512*1024**2 or peak>150*1024**2):stop='time/disk/output budget';signal_owned(signal.SIGTERM)
   if stop and time.monotonic()-start>82:signal_owned(signal.SIGKILL)
   if time.monotonic()-start>86:break
   time.sleep(.1)
finally:
 rows=scan();remaining=[pid for pid,identity in owned.items() if rows.get(pid,{}).get('identity')==identity]
 record['remaining_owned_pids']=remaining;record['profile_bytes_before_cleanup']=size(PROFILE)
 if p is not None and p.poll() is not None and 'direct_node_reaped' not in record:record['direct_node_reaped']={'pid':p.pid,'exit':p.wait(),'explicit_wait':True}
 # Fresh independent closure census: exact private profile argument, no prefix match.
 rows=scan();pattern=re.compile(r'(?:^|\s)--user-data-dir='+re.escape(str(PROFILE))+r'(?:\s|$)')
 profile_users={pid:item for pid,item in rows.items() if pattern.search(item['identity'])}
 current_owned=[pid for pid,identity in owned.items() if rows.get(pid,{}).get('identity')==identity]
 unknown=[pid for pid,identity in owned.items() if identity=='missing-before-first-wait' or (pid in rows and rows[pid]['identity']!=identity)]
 port_free=False
 with socket.socket() as probe:
  try:probe.bind(('127.0.0.1',19038));port_free=True
  except OSError as error:record['closure_port_error']=str(error)
 eperm=any(e.get('error_type')=='PermissionError' for e in events)
 helper_record=D/'r2-telemetry.json'
 if helper_record.exists():
  helper_events=json.loads(helper_record.read_text()).get('events',[])
  eperm=eperm or any(e.get('phase')=='chrome-close-error' and 'EPERM' in e.get('error','') for e in helper_events)
 record['closure_census']={'profile_users':profile_users,'attributed_live_pids':current_owned,'unknown_identities':unknown,'port19038_free':port_free,'eperm_observed':eperm}
 cleanup_proven=not profile_users and not current_owned and not unknown and port_free and not eperm
 if cleanup_proven and PROFILE.exists():shutil.rmtree(PROFILE)
 else:record['profile_cleanup_withheld']=not cleanup_proven
 record['profile_removed']=not PROFILE.exists();persist();print(json.dumps(record))
 if remaining or not cleanup_proven or p is None or p.poll()!=0 or stop:raise SystemExit(1)

import os,sys,json,time,subprocess,hashlib,shutil,signal
from pathlib import Path
start=time.monotonic();root=Path(__file__).resolve().parent;repo=root.parent.parent
plan=json.loads((repo/'evidence/integration/supplied-dd6588c-artifact-review/prepared-retry.json').read_text())
args=plan['command_proposed'];out=Path(args[2]);assert not out.exists()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(args[1])==plan['script_sha256']
hp=repo/'evidence/integration/supplied-dd6588c-preparation/frozen-handoff.json';assert sha(hp)=='2b516efe26a1465369c112142db9abb2ae184826da37af04309a157131bdb14b'
h=json.loads(hp.read_text());assert sha(h['paths']['binary'])==h['binary_sha256']
for n,v in h['package_files_sha256'].items():assert sha(Path(h['paths']['package'])/n)==v,n
assert shutil.disk_usage(root).free>=512*1024**2
for n in ['tmp','cache']:(root/n).mkdir()
env=dict(os.environ,TMPDIR=str(root/'tmp'),XDG_CACHE_HOME=str(root/'cache'))
def size():
 total=0
 for base in [root,out]:
  for f in base.rglob('*'):
   try:
    if f.is_file() and not f.is_symlink():total+=f.stat().st_size
   except FileNotFoundError:pass
 return total
baseline=size();observed={};peak=0;minimum=shutil.disk_usage(root).free;halt=''
def rows():
 s=subprocess.run(['/bin/ps','-axo','pid=,ppid=,pgid=,command='],capture_output=True,text=True,timeout=2).stdout
 return [dict(zip(['pid','ppid','pgid','command'],c)) for line in s.splitlines() if len(c:=line.strip().split(None,3))==4]
def collect():
 allrows=rows();known={str(p.pid),*observed};changed=True
 while changed:
  changed=False
  for r in allrows:
   if r['ppid'] in known and r['pid'] not in known:known.add(r['pid']);changed=True
 for r in allrows:
  if (r['pid'] in known or str(root/'tmp') in r['command']) and not r['command'].startswith('/bin/ps '):observed[r['pid']]=r
 return [r for r in allrows if r['pid'] in observed and r['command']==observed[r['pid']]['command']]
with (root/'navigation.log').open('w') as log:
 p=subprocess.Popen(args,cwd=plan['cwd'],env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 while p.poll() is None:
  collect();peak=max(peak,size()-baseline);minimum=min(minimum,shutil.disk_usage(root).free)
  if time.monotonic()-start>78 or peak>40*1024**2 or minimum<512*1024**2:
   halt='lease bound';os.killpg(p.pid,signal.SIGTERM);break
  time.sleep(.2)
 try:code=p.wait(timeout=3)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait(timeout=2)
remaining=collect()
for r in remaining:
 try:os.kill(int(r['pid']),signal.SIGTERM)
 except ProcessLookupError:pass
if remaining:time.sleep(.4)
remaining=collect()
for r in remaining:
 try:os.kill(int(r['pid']),signal.SIGKILL)
 except ProcessLookupError:pass
if remaining:time.sleep(.2)
remaining=collect();peak=max(peak,size()-baseline);minimum=min(minimum,shutil.disk_usage(root).free)
record={'argv':args,'cwd':plan['cwd'],'pid':p.pid,'exit_code':code,'halt':halt,'script_sha256':sha(args[1]),'env_overrides':{k:env[k] for k in ['TMPDIR','XDG_CACHE_HOME']},'elapsed_seconds':time.monotonic()-start,'peak_additional_bytes':peak,'minimum_free_bytes':minimum,'observed':list(observed.values()),'remaining':remaining,'direct_child_waited':True}
if not remaining:
 for n in ['tmp','cache']:shutil.rmtree(root/n)
record['owned_temp_cache_removed']=not remaining;record['closure_elapsed_seconds']=time.monotonic()-start
(root/'execution.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='observed'}),flush=True)

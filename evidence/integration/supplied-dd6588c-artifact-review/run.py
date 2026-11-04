import json,hashlib,subprocess,time,shutil,os,signal
from pathlib import Path
root=Path(__file__).resolve().parent;repo=root.parent.parent;proposal=json.loads((repo/'evidence/integration/supplied-dd6588c-artifact-plan/proposal.json').read_text());hpath=repo/'evidence/integration/supplied-dd6588c-preparation/frozen-handoff.json';h=json.loads(hpath.read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(hpath)==proposal['frozen_handoff_sha256'];assert sha(h['paths']['binary'])==h['binary_sha256']
for n,v in h['package_files_sha256'].items():assert sha(Path(h['paths']['package'])/n)==v,n
(root/'tmp').mkdir();(root/'cache').mkdir();start=time.monotonic();records=[];observed={};env=dict(os.environ,**proposal['runtime_environment'])
def size():
 total=0
 for p in root.rglob('*'):
  try:
   if p.is_file() and not p.is_symlink():total+=p.stat().st_size
  except FileNotFoundError:pass
 return total
baseline=size()
for label,args in zip(['verify','navigation'],proposal['commands']):
 phase=time.monotonic();peak=0;minimum=shutil.disk_usage(root).free;halt='';assert minimum>512*1024**2
 with (root/(label+'.log')).open('w') as log:
  p=subprocess.Popen(args,cwd=proposal['cwd'],env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
  while p.poll() is None:
   used=size()-baseline;peak=max(peak,used);minimum=min(minimum,shutil.disk_usage(root).free)
   ps=subprocess.run(['ps','-axo','pid=,ppid=,pgid=,command='],capture_output=True,text=True).stdout
   for line in ps.splitlines():
    cols=line.strip().split(None,3)
    if len(cols)==4 and (cols[2]==str(p.pid) or str(root/'tmp') in cols[3]):observed[cols[0]]=dict(zip(['pid','ppid','pgid','command'],cols))
   if used>40*1024**2 or minimum<512*1024**2 or time.monotonic()-start>110:
    halt='lease bound';os.killpg(p.pid,signal.SIGTERM);break
   time.sleep(.2)
  try:code=p.wait(timeout=4)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);code=p.wait(timeout=2)
 record={'argv':args,'cwd':proposal['cwd'],'env_overrides':proposal['runtime_environment'],'pid':p.pid,'exit_code':code,'halt':halt,'elapsed_phase_seconds':time.monotonic()-phase,'elapsed_total_seconds':time.monotonic()-start,'peak_additional_bytes':peak,'minimum_free_bytes':minimum,'direct_child_waited':True};records.append(record);(root/(label+'-command.json')).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
 if code or halt:break
ps=subprocess.run(['ps','-axo','pid=,ppid=,pgid=,command='],capture_output=True,text=True).stdout
remaining=[]
for line in ps.splitlines():
 cols=line.strip().split(None,3)
 if len(cols)==4 and cols[0] in observed and cols[3]==observed[cols[0]]['command']:remaining.append(cols)
(root/'processes.json').write_text(json.dumps({'observed':list(observed.values()),'remaining':remaining},indent=2)+'\n');print('remaining owned processes',len(remaining),flush=True)
assert not remaining,'Owned processes remain: report before cleanup'
for n in ['tmp','cache']:shutil.rmtree(root/n)
(root/'closure.json').write_text(json.dumps({'all_observed_processes_closed':True,'owned_temp_cache_removed':True,'elapsed_total_seconds':time.monotonic()-start},indent=2)+'\n')

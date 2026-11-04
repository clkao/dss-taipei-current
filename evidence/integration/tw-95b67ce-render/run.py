import os,sys,json,time,subprocess,signal,shutil,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
work=Path('/Users/clkao/git/spacedock-research/studfleet/.worktrees/spacedock-ensign-show-installed-drafts-without-unverified-placement-hints')
label,*cmd=sys.argv[1:]
(root/'tmp').mkdir(exist_ok=True);(root/'cache').mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(root/'tmp'),XDG_CACHE_HOME=str(root/'cache'),PATH='/Users/clkao/.local/share/fnm/node-versions/v24.22.1/installation/bin:'+os.environ['PATH'])
def size():
 total=0
 for p in root.rglob('*'):
  try:
   if p.is_file() and not p.is_symlink():total+=p.stat().st_size
  except FileNotFoundError:pass
 return total
start=time.monotonic();minimum=shutil.disk_usage(root).free;peak=size();halt=''
assert minimum>512*1024**2
with (root/(label+'.log')).open('w') as log:
 proc=subprocess.Popen(cmd,cwd=work,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 while proc.poll() is None:
  used=size();free=shutil.disk_usage(root).free;peak=max(peak,used);minimum=min(minimum,free)
  if used>150*1024**2 or free<512*1024**2 or time.monotonic()-start>180:
   halt='owned-resource-or-command-time-limit';os.killpg(proc.pid,signal.SIGTERM);break
  time.sleep(.5)
 code=proc.wait(timeout=15)
report={'argv':cmd,'cwd':str(work),'environment_overrides':{k:env[k] for k in ['TMPDIR','XDG_CACHE_HOME','PATH']},'exit_code':code,'halt':halt,'peak_owned_bytes':peak,'minimum_free_bytes':minimum,'elapsed_seconds':time.monotonic()-start}
(root/(label+'-command.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));print((root/(label+'.log')).read_text()[-3000:]);sys.exit(code or bool(halt))

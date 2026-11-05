"""One local mobile-browser exercise with the established disk admission and active floor."""
from pathlib import Path
import json,subprocess,time,shutil,os,signal,hashlib,sys
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;O=R/'builds/clear-logical/cycle1/browser-review'
assert shutil.disk_usage(R).free>=576*1024**2,'Admission requires 576 MiB free; active floor remains 512 MiB'
assert not O.exists(),'Preserve any earlier run and its evidence'
O.mkdir();began=time.monotonic();minimum=shutil.disk_usage(R).free;peak=0;reason=None
node='/Users/clkao/.local/share/fnm/node-versions/v24.22.1/installation/bin/node';argv=[node,str(P/'review-mobile.mjs'),str(O)]
record={'argv':argv,'cwd':str(R),'active_floor_bytes':512*1024**2,'admission_free_bytes':minimum,'started_unix':time.time(),'memory_snapshot':subprocess.check_output(['vm_stat'],text=True)}
with (O/'run.log').open('w') as log:
 child=subprocess.Popen(argv,cwd=R,stdout=log,stderr=log,start_new_session=True)
 while child.poll() is None:
  minimum=min(minimum,shutil.disk_usage(R).free)
  if minimum<512*1024**2 or time.monotonic()-began>110:
   reason='active disk floor or time budget';os.killpg(child.pid,signal.SIGTERM);break
  time.sleep(.2)
 try:exit=child.wait(timeout=8)
 except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);exit=child.wait()
record.update(exit=exit,stop_reason=reason,min_free_bytes=minimum,elapsed_seconds=time.monotonic()-began)
(O/'run.json').write_text(json.dumps(record,indent=2)+'\n')
if exit or reason:raise SystemExit(1)
profile=R/'tmp'/('yangliu-preview-chrome-'+hashlib.sha256(str(O.resolve()).encode()).hexdigest()[:8]);tele=json.loads((O/'r2-telemetry.json').read_text());proc=subprocess.check_output(['ps','-axo','pid=,command='],text=True)
assert tele['chromeExit']['code']==0 and '--user-data-dir='+str(profile) not in proc
if profile.exists():shutil.rmtree(profile)
print('Finished; owned browser exited and private profile removed.')

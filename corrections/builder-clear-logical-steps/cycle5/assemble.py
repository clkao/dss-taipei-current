from pathlib import Path
import subprocess,time,json,shutil,os,signal
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;O=R/'builds/clear-logical/cycle5';minimum=shutil.disk_usage(R).free;assert minimum>=576*1024**2
start=time.monotonic();records=[]
for name in ['compose-pointer.py','compose-sides.py','headings.py','page-map-guide.py','prepare-package.py']:
 cmd=['/Users/clkao/git/house-demo/tmp/lego-standards-venv/bin/python',str(P/name)]
 if name=='headings.py':cmd += [str(O/'content.pdf'),str(O/'package/instructions.pdf')]
 if name=='prepare-package.py':cmd += ['--raster-pages','31,32,35']
 t=time.monotonic()
 with (O/('final-'+name+'.log')).open('w') as log:
  child=subprocess.Popen(cmd,cwd=R,stdout=log,stderr=log,start_new_session=True)
  while child.poll() is None:
   minimum=min(minimum,shutil.disk_usage(R).free)
   if minimum<512*1024**2 or time.monotonic()-start>180:os.killpg(child.pid,signal.SIGTERM);raise RuntimeError('Active disk/time guard')
   time.sleep(.2)
  records.append({'command':cmd,'exit':child.returncode,'elapsed_seconds':time.monotonic()-t});assert child.returncode==0,name
(P/'assembly-run.json').write_text(json.dumps({'commands':records,'minimum_free_bytes':minimum,'elapsed_seconds':time.monotonic()-start,'admission_MiB':576,'active_MiB':512},indent=2)+'\n');print('Final PDF composition and79-page raster pass completed.')

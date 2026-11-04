import json,hashlib,subprocess,time,os,signal,shutil
from pathlib import Path
root=Path(__file__).resolve().parent;repo=root.parent.parent
work=Path('/Users/clkao/git/spacedock-research/studfleet/.worktrees/spacedock-ensign-inspect-dss-minifigure-without-connector-backend-failure')
binary=work/'builds/dss-connector-implementation/studfleet-1267d4eb9ef1c9de'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
assert sha(binary)=='1267d4eb9ef1c9defc1fbf31453a201add36dabf0d0753ac8b9ce803dd4fa677'
tooling=json.loads((repo/'manifests/tooling.json').read_text())
for k,h in [('archive','sha256'),('python','executable_sha256')]:assert sha(tooling[k]['path'])==tooling[k][h]
start=time.monotonic();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(root/'tmp'));(root/'tmp').mkdir()
def size():
 n=0
 for p in root.rglob('*'):
  try:
   if p.is_file():n+=p.stat().st_size
  except FileNotFoundError:pass
 return n
def run(label,args):
 peak=size();minimum=shutil.disk_usage(root).free;halt='';assert minimum>512*1024**2
 with (root/(label+'.stdout')).open('w') as out,(root/(label+'.stderr')).open('w') as err:
  p=subprocess.Popen([str(binary),*map(str,args)],cwd=work,env=env,stdout=out,stderr=err,start_new_session=True)
  while p.poll() is None:
   peak=max(peak,size());minimum=min(minimum,shutil.disk_usage(root).free)
   if peak>80*1024**2 or minimum<512*1024**2 or time.monotonic()-start>350:
    halt='lease limit';os.killpg(p.pid,signal.SIGTERM);break
   time.sleep(.2)
  code=p.wait(timeout=10)
 record={'argv':[str(binary),*map(str,args)],'cwd':str(work),'env':{'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':env['TMPDIR']},'exit_code':code,'halt':halt,'elapsed_seconds':time.monotonic()-start,'peak_owned_bytes':peak,'minimum_free_bytes':minimum}
 (root/(label+'-command.json')).write_text(json.dumps(record,indent=2)+'\n');print(label,code,flush=True)
 if code or halt:raise RuntimeError((root/(label+'.stderr')).read_text())
source=repo/'evidence/bootstrap/intake/source.mpd';intake=root/'intake'
run('import',['import-mpd','--input',source,'--out',intake])
old=json.loads((repo/'evidence/bootstrap/intake/assembly.json').read_text());new=json.loads((intake/'assembly.json').read_text())
assert new==old;assert len(new['instances'])==348
oldp=json.loads((repo/'evidence/bootstrap/intake/import-report.json').read_text());newp=json.loads((intake/'import-report.json').read_text())
assert newp['origins']==oldp['origins'];assert newp['source_sha256']==oldp['source_sha256']==sha(source)
(root/'identity.json').write_text(json.dumps({'source_sha256':sha(source),'binary_sha256':sha(binary),'assembly_sha256':sha(intake/'assembly.json'),'all_348_instance_records_exact':True,'all_origin_chains_exact':True,'source_bytes_exact':(intake/'source.mpd').read_bytes()==source.read_bytes(),'resource_pins':{k:tooling[k] for k in ['python','archive','shadow']}},indent=2)+'\n')
run('inspect',['inspect','--assembly',intake/'assembly.json','--provenance',intake/'import-report.json','--report',root/'inspection.json','--connectivity','pyldraw3','--python',tooling['python']['path'],'--shadow',tooling['shadow']['path'],'--ldraw',tooling['archive']['path']])

import json,hashlib,shutil,subprocess,time,os,signal
from pathlib import Path
root=Path(__file__).resolve().parent
repo=root.parent.parent
work=Path('/Users/clkao/git/spacedock-research/studfleet/.worktrees/spacedock-ensign-show-reader-labels-without-internal-clutter')
binary=work/'builds/reader-label-implementation/studfleet'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(binary)=='ea886884d0aa35eba57f85dc193090813c1d7a8a1599c58c0d00ec2312ba00a7'
start=time.monotonic(); records=[]
def size():
 total=0
 for p in root.rglob('*'):
  try:
   if p.is_file():total+=p.stat().st_size
  except FileNotFoundError:pass
 return total
def run(name,args):
 assert shutil.disk_usage(root).free>512*1024**2
 out=root/(name+'.stdout');err=root/(name+'.stderr'); peak=size();minimum=shutil.disk_usage(root).free
 with out.open('w') as o,err.open('w') as e:
  p=subprocess.Popen([str(binary),*map(str,args)],cwd=work,stdout=o,stderr=e,start_new_session=True)
  while p.poll() is None:
   peak=max(peak,size());minimum=min(minimum,shutil.disk_usage(root).free)
   if peak>80*1024**2 or minimum<512*1024**2 or time.monotonic()-start>480:
    os.killpg(p.pid,signal.SIGTERM);p.wait();raise RuntimeError('lease bound reached')
   time.sleep(.1)
 result={'argv':[str(binary),*map(str,args)],'cwd':str(work),'exit_code':p.returncode,'peak_owned_bytes':peak,'minimum_free_bytes':minimum}
 (root/(name+'-command.json')).write_text(json.dumps(result,indent=2)+'\n');records.append(result)
 print(name,p.returncode,flush=True)
 if p.returncode:raise RuntimeError(err.read_text())
summary={'candidate_source':'3a6833baa4e78cc76f02c51a4e1133d9a3512591','binary_sha256':sha(binary),'specimens':{}}
for name,title,singular in [('speakers','DSS speakers','Speaker'),('rings','DSS life rings','Life ring')]:
 source=repo/'evidence/integration/scheduler-410a7a2'/f'{name}.mpd';old=repo/'builds/tw-95b67ce-check'/name;dest=root/name;dest.mkdir()
 run(name+'-import',['import-mpd','--input',source,'--out',dest/'intake'])
 assert (dest/'intake/assembly.json').read_bytes()==(old/'intake/assembly.json').read_bytes(), 'assembly bytes changed: stop for investigation'
 shutil.copy2(old/'plan.json',dest/'plan.json')
 plan=json.loads((dest/'plan.json').read_text());presentation=json.loads((old/'presentation.json').read_text())
 presentation['required_capabilities'].append('reader-labels-and-concise-text')
 presentation['reader_labels']={'title':title,'steps':{op['id']:f'Place {singular.lower()} {i+1}' for i,op in enumerate(plan['groups'][0]['operations'])},'units':{name:singular},'copies':{name+'-1':'First '+singular.lower(),name+'-2':'Second '+singular.lower()}}
 (dest/'presentation.json').write_text(json.dumps(presentation,indent=2)+'\n')
 assert sha(dest/'plan.json')==presentation['plan_sha256']
 run(name+'-check',['draft','--assembly',dest/'intake/assembly.json','--provenance',dest/'intake/import-report.json','--plan',dest/'plan.json','--presentation',dest/'presentation.json','--check-only'])
 summary['specimens'][name]={'source_sha256':sha(source),'assembly_sha256':sha(dest/'intake/assembly.json'),'assembly_byte_identical_to_TW':True,'plan_sha256':sha(dest/'plan.json'),'plan_byte_identical_to_TW':True,'presentation_sha256':sha(dest/'presentation.json'),'captions':'All previous authored captions retained; no guidance caption override','result':'fresh import and check-only exit0'}
summary['commands']=records;summary['elapsed_seconds']=time.monotonic()-start
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))

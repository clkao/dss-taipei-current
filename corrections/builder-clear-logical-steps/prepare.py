"""Prepare source-bound local presentation jobs; immutable source is never rewritten."""
import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];B=R/'builds/clear-logical';P=Path(__file__).parent
m=json.loads((B/'simplification-package-retry1/model.json').read_text());steps=m['instruction_plan']['steps'];parts={p['id']:p for p in m['pieces']}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(B/'simplification-package-retry1/model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(B/'simplification-package-retry1/instructions.pdf')=='5c347b0e5d639a5ed5f45be6e867a14772fa01ed92ec4c80b472f956bbcf7bbd'
jobs=[]
def add(name,n,ids,new,focus,view='top',targets=None,**extra):
 jobs.append(dict(name=name,step=n,ids=ids,newIds=new,focus=focus,view=view,targets=targets or [],bands=steps[n-1]['manual']['bands_installed'],**extra))
for n in [14,15]:
 s=steps[n-1];prev=[i for i in s['manual']['ids'] if i not in s['new_ids']]
 for layer,placement in enumerate(s['placements']):
  new=placement['ids']; focus=s['new_ids']; t=[dict(id=i,label=str(j+1)) for j,i in enumerate(new)]
  add(f's{n}-{layer+1}-before',n,prev,[],focus,targets=t)
  prev=prev+new
  add(f's{n}-{layer+1}-after',n,prev,new,focus,targets=t)
for n in [5,6,7,8]:
 s=steps[n-1];new=s['new_ids'];prev=[i for i in s['manual']['ids'] if i not in new]
 # Local insertion receiver selection preserves every already installed part.
 for state,ids in [('before',prev),('after',s['manual']['ids']),('unit',new)]:
  add(f's{n}-{state}',n,ids,new if state!='before' else [],new,'underside',targets=[dict(id=new[0],label='A')])
s=steps[40];prev=[i for i in s['manual']['ids'] if i not in s['new_ids']]
for j,placement in enumerate(s['placements']):
 new=placement['ids'];focus=[74,193,201,199,200,287]
 add(f'cabin-{j+1}-before',41,prev,[],focus,targets=[dict(id=i,label=str(k+1)) for k,i in enumerate(new)])
 prev=prev+new
 add(f'cabin-{j+1}-after',41,prev,new,focus,targets=[dict(id=i,label=str(k+1)) for k,i in enumerate(new)])
add('steering-detail',41,[199,200],[200],[199,200],'front')
for view in ['top','front','front-other']:
 add('cord-'+view,64,steps[63]['manual']['ids'],[],[25,70,142,78],view,targets=[dict(id=i,label=str(k+1)) for k,i in enumerate([25,70,142,78])],cord=True)
fig=[i for i,p in parts.items() if p['module']=='candidate']
for state in ['before','after']:
 ids=[i for i in steps[66]['manual']['ids'] if parts[i]['module'] not in ['tsai'] and (state=='after' or i not in fig)]
 add('helm-'+state,67,ids,fig if state=='after' else [],fig,'rear-other',targets=[dict(id=255,label='A')])
(P/'jobs.json').write_text(json.dumps(jobs,indent=2)+'\n')
print(len(jobs),'jobs')

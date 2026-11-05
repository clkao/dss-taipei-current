"""Prepare presentation-only jobs from immutable source and derived catalog features."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent
m=json.loads((B/'candidate/model.json').read_text());steps=m['instruction_plan']['steps'];parts={x['id']:x for x in m['pieces']};features=json.loads((P/'features.json').read_text());jobs=[]
def add(name,ids,focus,direction,targets=None,**kw):jobs.append(dict(name=name,ids=ids,focus=focus,direction=direction,view='front',targets=targets or [],bands=False,newIds=[],**kw))
for item in features['suspension']:
 n=item['step'];s=steps[n-1];new=s['new_ids'];left=n in [5,7];pairs=item['pairs'];focus=[i for pair in pairs for i in [pair['pin_id']]]
 before=[i for i in s['manual']['ids'] if i not in new]
 add(f's{n}-receiver',before,focus,[1,-.5,1.7 if left else -1.7],targets=[{'id':p['receiver_id'],'local':p['hole_mouth_local_ldu'],'label':p['label'],'label_at':[.20 if k==0 else .80,.12]} for k,p in enumerate(pairs)],margin=3,minHeight=3)
 add(f's{n}-unit',new,new,[1,-.4,-1.7 if left else 1.7],targets=[{'id':p['pin_id'],'local':p['pin_end_local_ldu'],'label':p['label'],'label_at':[.20 if k==0 else .80,.12]} for k,p in enumerate(pairs)],margin=1.7,minHeight=2)
for ring in features['rings']:
 i=ring['id'];order=ring['order'];left=i in [25,70];xside=-1 if i in [25,78] else 1
 # The camera faces the exposed aperture end. Opposite-side clips reverse local X.
 local_x=4*xside*(1 if left else -1)
 add(f'ring-{order}',steps[63]['manual']['ids'],[i],[xside,.35,1.25 if left else -1.25],targets=[{'id':i,'local':[local_x,2,-20],'label':str(order),'label_at':[.18,.14]}],cord=True,margin=1.4,minHeight=1.5)
for n,plate in [(14,99),(15,129)]:
 s=steps[n-1]
 corner={'id':plate,'local':[80,0,-60],'label':'C','label_at':[.82,.15]}
 add(f'plate{n}-locator',s['manual']['ids'],s['manual']['ids'],[1,.8,1.15],targets=[corner],margin=1.15,minHeight=4)
 jobs[-1]['newIds']=[plate];jobs[-1]['bands']=True
 for state,ids in [('receiver',[plate]),('complete',[plate]+s['new_ids'])]:
  add(f'plate{n}-{state}',ids,[plate]+s['new_ids'],[1,-1.2,1.15],targets=[dict(corner,local=[80,8,-60])],margin=1.35,minHeight=3)
  jobs[-1]['newIds']=s['new_ids'] if state=='complete' else []
helm=[i for i,p in parts.items() if p['module']=='helm'];fig=[i for i,p in parts.items() if p['module']=='candidate'];focus=[284,255]+helm
foot_targets=[{'id':255,'local':[sum(v[k] for v in f['sole_bounds_local_ldu'])/4 for k in range(3)],'label':f['label'],'label_at':[.20 if f['label']=='L' else .80,.12]} for f in features['feet']]
polygons=[{'id':255,'local':f['sole_bounds_local_ldu'],'label':f['label']} for f in features['feet']]
for state,ids in [('receiver',[i for i in steps[66]['manual']['ids'] if i not in fig and parts[i]['module']!='tsai']),('detail',[284,255]+helm)]:
 add('feet-'+state,ids,focus,[-.3,1.3,1.1],targets=foot_targets,polygons=polygons,margin=1.3,minHeight=3)
 jobs[-1]['bands']=state=='receiver'
(P/'jobs.json').write_text(json.dumps(jobs,indent=2)+'\n');print(len(jobs),'planned views')

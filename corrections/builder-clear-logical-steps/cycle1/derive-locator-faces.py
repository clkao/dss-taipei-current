"""Project installed plate faces through the recorded job camera; check its existing C mark."""
from pathlib import Path
import json,math,itertools
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent
cat=json.loads((B/'candidate/catalog-meshes.json').read_text());inst={x['id']:x for x in json.loads((B/'candidate/render-scene.json').read_text())['instances']};jobs=json.loads((P/'jobs.json').read_text());loc=json.loads((B/'cycle1/renders/receiver-locations.json').read_text());bounds={}
def world(i,v):
 m=inst[i]['matrix'];q=[sum(m[k][a]*v[a] for a in range(3))+m[k][3] for k in range(3)];return[q[0]*.05,-q[1]*.05,-q[2]*.05]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):l=math.sqrt(dot(a,a));return[x/l for x in a]
def cross(a,b):return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def corners(i):
 part=inst[i]['part']
 if part not in bounds:
  vs=[]
  for mesh in cat['parts'][part]['meshes']:
   a=mesh['geometry']['data']['attributes']['position']['array'];vs += [a[k:k+3] for k in range(0,len(a),3)]
  bounds[part]=list(itertools.product(*[(min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3)]))
 return [world(i,v) for v in bounds[part]]
out={}
for job in jobs:
 if not job['name'].endswith('-locator'):continue
 vs=[v for i in job['focus'] for v in corners(i)];lo=[min(v[k] for v in vs) for k in range(3)];hi=[max(v[k] for v in vs) for k in range(3)];center=[(a+b)/2 for a,b in zip(lo,hi)]
 direction=norm(job['direction']);right=norm(cross([0,1,0],direction));up=cross(direction,right)
 def uv(v):v=[x-y for x,y in zip(v,center)];return[dot(v,right),dot(v,up)]
 fc=[uv(v) for v in itertools.product(*zip(lo,hi))];xmin=min(x for x,y in fc);xmax=max(x for x,y in fc);ymin=min(y for x,y in fc);ymax=max(y for x,y in fc);height=max(job['minHeight'],ymax-ymin,(xmax-xmin)/1.4)*job['margin'];width=height*1.4;cx=(xmin+xmax)/2;cy=(ymin+ymax)/2
 def project(v):x,y=uv(v);return{'x':(x-cx)/width+.5,'y':.5-(y-cy)/height}
 target=job['targets'][0];q=project(world(target['id'],target['local']));old=loc[job['name']]['targets'][0];error=max(abs(q[k]-old[k]) for k in ['x','y']);assert error<1e-9,error
 face=[[-80,0,-60],[80,0,-60],[80,0,60],[-80,0,60]]
 out[job['name']]={'id':target['id'],'local_face_ldu':face,'points':[project(world(target['id'],v)) for v in face],'projection_crosscheck_error':error,'meaning':'Top face display highlight; source colors remain unchanged.'}
(P/'locator-faces.json').write_text(json.dumps(out,indent=2)+'\n');print('Two installed plate highlights matched recorded camera.')

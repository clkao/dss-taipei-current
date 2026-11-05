"""Derive local catalog features and bind them to frozen occurrence transforms."""
from pathlib import Path
import json,hashlib,zipfile,math
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((B/'candidate/model.json').read_text());scene=json.loads((B/'candidate/render-scene.json').read_text());cat=json.loads((B/'candidate/catalog-meshes.json').read_text());inst={x['id']:x for x in scene['instances']}
assert sha(B/'candidate/model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
archive=zipfile.ZipFile(B/'cycle1/catalog.zip');members={}
def source(name):
 raw=archive.read('ldraw/'+name);members[name]=hashlib.sha256(raw).hexdigest();return raw.decode().splitlines()
def world(i,local):
 a=inst[i]['matrix'];return [sum(a[k][j]*local[j] for j in range(3))+a[k][3] for k in range(3)]
def vertices(part):
 for mesh in cat['parts'][part]['meshes']:
  a=mesh['geometry']['data']['attributes']['position']['array']
  yield from (a[j:j+3] for j in range(0,len(a),3))
beam=source('parts/32018.dat');ring=source('parts/4081b.dat');source('parts/32556b.dat');source('parts/2780.dat')
holes=[]
for num,line in enumerate(beam,1):
 a=line.split()
 if a and a[0]=='1' and a[-1]=='peghole.dat':holes.append({'local':list(map(float,a[2:5])),'source_line':num})
assert len(holes)==26
susp=[]
for n,pins,beam_id,xs,side in [(5,[217,219],172,[-80,-100],-10),(6,[226,225],178,[-80,-100],10),(7,[220,228],172,[80,100],-10),(8,[234,233],178,[80,100],10)]:
 pairs=[]
 for label,pin,x in zip(['A','B'],pins,xs):
  part=inst[pin]['part'];vs=list(vertices(part));end=min(v[0] for v in vs) if label=='A' or n in [6,8] else max(v[0] for v in vs)
  tip=[end,0,0];mouth=[x,10,side];hole=next(h for h in holes if h['local']==mouth)
  a=world(pin,tip);b=world(beam_id,mouth);radial=math.hypot(a[0]-b[0],a[1]-b[1]);assert radial<.001
  pairs.append({'label':label,'pin_id':pin,'pin_part':part,'pin_end_local_ldu':tip,'receiver_id':beam_id,'hole_mouth_local_ldu':mouth,'receiver_source_line':hole['source_line'],'pin_end_world_ldu':a,'hole_mouth_world_ldu':b,'axis_radial_error_ldu':radial,'axial_depth_ldu':abs(a[2]-b[2]),'meaning':'Catalog end-face center and nearest outside beam-hole mouth. Axis correspondence only; no insertion proof.'})
 susp.append({'step':n,'operation':m['instruction_plan']['steps'][n-1]['operations'][-1],'pairs':pairs})
rings=[]
for ordinal,i in enumerate([25,70,142,78],1):
 faces=[[-4,2,-20],[4,2,-20]]
 for face in faces:assert any(line.startswith('1 16 '+' '.join(map(str,face))+' ') and 'stud2a.dat' in line for line in ring)
 rings.append({'order':ordinal,'id':i,'part':'4081b','aperture_faces_local_ldu':faces,'aperture_faces_world_ldu':[world(i,f) for f in faces],'inner_radius_ldu':4,'source':'4081b.dat stud2a / inner 4-4cyli primitives','route_unchanged':True})
vs=list(vertices('3815c01'));sole=max(v[1] for v in vs);feet=[]
for label,side in [('L',-1),('R',1)]:
 pts=[v for v in vs if abs(v[1]-sole)<1e-5 and v[0]*side>0];lo=[min(v[k] for v in pts) for k in range(3)];hi=[max(v[k] for v in pts) for k in range(3)]
 rect=[[lo[0],sole,lo[2]],[hi[0],sole,lo[2]],[hi[0],sole,hi[2]],[lo[0],sole,hi[2]]]
 feet.append({'label':label,'piece_id':255,'sole_bounds_local_ldu':rect,'world_ldu':[world(255,v) for v in rect],'meaning':'Projected sole bounding footprint, not certified stud/cavity centers.'})
result={'schema':'dss-visible-feature-correspondence/1','model_sha256':sha(B/'candidate/model.json'),'render_scene_sha256':sha(B/'candidate/render-scene.json'),'catalog_meshes_sha256':sha(B/'candidate/catalog-meshes.json'),'catalog_archive_member_hashes':members,'suspension':susp,'rings':rings,'feet':feet,'physical_verified':False}
(P/'features.json').write_text(json.dumps(result,indent=2)+'\n')
print('Derived 8 pin/hole pairs, 4 ring apertures, and 2 sole footprints.')

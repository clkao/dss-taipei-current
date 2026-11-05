from pathlib import Path
import json,hashlib,itertools,numpy as np
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;O=R/'builds/clear-logical/cycle4/package';m=json.loads((O/'model.json').read_text());ps={p['id']:p for p in m['pieces']};left=m['instruction_plan']['steps'][16]['new_ids'];right=m['instruction_plan']['steps'][17]['new_ids'];I=np.eye(3);Z=np.diag([-1,-1,1]);tol=1e-5
# Catalog plate half-turn symmetry is around LDraw Y (model-local Z).
cat=json.loads((O/'catalog-meshes.json').read_text());symmetry={}
for part in ['3666','3710']:
 v=np.concatenate([np.array(q['geometry']['data']['attributes']['position']['array']).reshape(-1,3) for q in cat['parts'][part]['meshes']]);v=np.unique(np.round(v,4),axis=0);w=v@np.diag([-1,1,-1]);a={tuple(x) for x in v};b={tuple(x) for x in w};assert a==b
 symmetry[part]={'ldraw_rotation':np.diag([-1,1,-1]).tolist(),'unique_vertex_set_equal':True,'vertices':len(v)}
def map_for(A,B,Q,t):
 pairs=[]
 for i in A:
  p=ps[i]
  for j in B:
   q=ps[j]
   if (p['part'],p['color'])!=(q['part'],q['color']):continue
   pe=float(np.linalg.norm(Q@p['transform']['origin']+t-q['transform']['origin']))
   oe=min(float(np.max(abs(Q@np.array(p['transform']['matrix'])@s-q['transform']['matrix']))) for s in ([I,Z] if p['part'] in symmetry else [I]))
   if pe<tol and oe<tol:pairs.append({'left':i,'right':j,'part':p['part'],'color':p['color'],'position_error_scene_units':pe,'orientation_error':oe})
 return pairs
# These axis-aligned source orientations permit all proper signed-axis rotations.
rot=[]
for perm in itertools.permutations(range(3)):
 for signs in itertools.product([-1,1],repeat=3):
  Q=np.zeros((3,3))
  for i,j in enumerate(perm):Q[i,j]=signs[i]
  if np.linalg.det(Q)>.99:rot.append(Q)
best=[]
for Q in rot:
 for i in left:
  for j in right:
   if (ps[i]['part'],ps[i]['color'])!=(ps[j]['part'],ps[j]['color']):continue
   t=np.array(ps[j]['transform']['origin'])-Q@ps[i]['transform']['origin'];pairs=map_for(left,right,Q,t)
   if not best or len(pairs)>best[0]['count']:best=[dict(count=len(pairs),rotation=Q.tolist(),translation=t.tolist(),pairs=pairs)]
assert best[0]['count']==13
Q=Z;t=np.array([21.99997932,8.00000056,.00000268]);pairs=map_for(left,right,Q,t);assert len(pairs)==13
units=[]
for name,A,B,tx in [('lower_carrier',[97,96,115,117,140,197,98,116],[158,156,166,185,205,176,157,167],21.99997932),('long_rail',[38,39,41,42],[81,87,83,89],17.99998015),('short_rail',[331,46,48],[333,82,93],27.99998015)]:
 tt=np.array([tx,8.00000056,.00000268]);pp=map_for(A,B,Q,tt);assert len(pp)==len(A);units.append(dict(name=name,count=len(A),rotation=Q.tolist(),translation=tt.tolist(),pairs=pp))
# The final joints distinguish congruent subunits from one congruent full carrier.
ops={o['step']:o for o in m['build_operations']};joint=[]
for n in [56,60,69,73,61,74]:joint.append({k:ops[n][k] for k in ['step','id','kind','assembly','child','placements'] if k in ops[n]}|{'source_mate_pairs':ops[n].get('source_mate_pairs',[])})
result={'source_sha256':hashlib.sha256((O/'model.json').read_bytes()).hexdigest(),'left_ids':left,'right_ids':right,'same_inventory':sorted((ps[i]['part'],ps[i]['color']) for i in left)==sorted((ps[i]['part'],ps[i]['color']) for i in right),'complete_rigid_congruence':False,'proper_rotations_examined':24,'position_orientation_tolerance':tol,'plate_symmetry_evidence':symmetry,'maximal_rigidly_aligned_subset':best[0],'subset_not_a_complete_connected_recipe':'13 includes three outer brackets supported only through the omitted upper plates; not a valid preassembled13-part unit.','complete_verified_common_units':units,'real_difference':'After aligning lower carriers with 180-degree proper rotation, source left long rail center x9 maps to right x13, but right long rail is at x9; source left short rail center x14 maps to right x8, but right short rail is at x14. The rail split reverses relative to the lower-carrier frame.','final_joints':joint,'minimal_order_proposal':{'left_unchanged':[57,58,59,60],'right_current':[70,71,72,73],'right_proposed':[70,72,71,73],'reason':'Under the complete short-rail rigid copy map, left first bracket46 corresponds to right93 (current op72), and left next bracket48 corresponds to right82 (current op71). Both stay loose and both precede join73. No final geometry/ownership change.','status':'PROPOSED ONLY; no semantic mutation'},'access_limits':'Source loose-rail bracket-before-join structure retained. No claim of certified physical insertion, grip or clearance; step19 witness and installed suspension bands must remain.','presentation_recommendation':'Do not label complete15-part carrier2x. Show common8-part lower recipe and common4/3-part loose rail recipes with readable names, then one explicit opposite rail-split comparison and two distinct full-carrier/chassis placements. No internal IDs or tiny detail locators.'}
(P/'side-equivalence-finding.json').write_text(json.dumps(result,indent=2)+'\n');print('Complete15 noncongruent; maximal aligned13 (not connected); verified common complete units8/4/3; right71/72 order swap proposed only.')

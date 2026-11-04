"""Small source-bound checks for the three post-publication presentation regressions."""
from pathlib import Path
import json,hashlib
from collections import Counter
R=Path(__file__).resolve().parents[3];D=R/'builds/access-corrected-r2';P=R/'builds/access-corrected'
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=load(D/'model.json');old=load(P/'model.json');source=load(R/'sources/minifigure/legacy-v10/model.json')
assert m['pieces']==old['pieces']
assert [{k:v for k,v in p.items() if k!='step'} for p in m['pieces']]==[{k:v for k,v in p.items() if k!='step'} for p in source['pieces']]
assert m['build_operations']==old['build_operations']
assert Counter(i for o in m['build_operations'] for i in o['ids'])==Counter(p['id'] for p in m['pieces'])
steps=m['instruction_plan']['steps'];previous=old['instruction_plan']['steps'];flex=[];overviews=[]
for s in steps:
 if not s['manual'].get('corrected'):continue
 for f in s['manual']['frames']:
  anchors=[b['anchor_ids'] for b in m['suspension_bands'] if set(b['anchor_ids'])<=set(f['shown_ids'])]
  expected=bool(s['manual'].get('bands_installed') and f['assembly']==m['assembly_roots']['truck'] and anchors)
  assert f['bands_installed']==expected
  if expected:flex.append({'step':s['number'],'panel':f['number'],'source_operation':f['source_operation'],'kind':f['kind'],'anchors':anchors})
 root=[f for f in s['manual']['frames'] if f['assembly']==s['assembly'] and f['kind']!='receiver-context'];selected=root[-1] if root else s['manual']['frames'][-1]
 assert s['manual']['ids']==selected['shown_ids']
 assert set(s['manual']['overview_new_ids'])<=set(s['manual']['ids'])
 overviews.append({'step':s['number'],'source_operation':selected['source_operation'],'assembly':selected['assembly'],'changed':s['manual']['ids']!=previous[s['number']-1]['manual']['ids']})
assert previous[10]['manual']['ids']==[190]
assert 169 in steps[10]['manual']['ids'] and 190 not in steps[10]['manual']['ids']
assert steps[10]['manual']['frames'][-1]['shown_ids']==[190]
assert steps[10]['manual']['overview_new_ids']==[169]
assert [x['step'] for x in overviews if x['changed']]==[11]
left,right=steps[16],steps[17];lp=left['manual'];rp=right['manual']
assert lp['repeat_prefix_frames']==rp['repeat_prefix_frames']==4 and lp['repeat_prefix_count']==rp['repeat_prefix_count']==2 and rp['repeat_prefix_from']==17
assert not previous[16]['manual'].get('repeat_prefix_count') and not previous[17]['manual'].get('repeat_prefix_from')
assert len(lp['common_prefix_copies'])==2 and all(len(x)==8 for x in lp['common_prefix_copies'])
assert not set(lp['common_prefix_copies'][0])&set(lp['common_prefix_copies'][1])
pieces={p['id']:p for p in m['pieces']};scene={p['id']:p for p in load(P/'render-scene.json')['instances']}
pairs=[(97,158),(96,166),(115,156),(117,185),(140,176),(197,205),(98,167),(116,157)]
rotation=[-1,1,-1];a=scene[97]['matrix'];b=scene[158]['matrix'];max_error=0;matrices=[]
for x,y in pairs:
 aa=scene[x]['matrix'];bb=scene[y]['matrix'];assert (pieces[x]['part'],pieces[x]['color'])==(pieces[y]['part'],pieces[y]['color'])
 error=max(abs(b[i][3]+rotation[i]*(aa[i][3]-a[i][3])-bb[i][3]) for i in range(3));assert error<.0001;max_error=max(max_error,error)
 symmetry=[-1,1,-1] if x==97 else [1,1,1]
 assert all(rotation[i]*aa[i][j]*symmetry[j]==bb[i][j] for i in range(3) for j in range(3))
 matrices.append({'left':x,'right':y,'left_exact_matrix':aa,'right_exact_matrix':bb,'origin_error_ldu':error,'plate_local_half_turn':x==97})
mesh=load(P/'catalog-meshes.json')['parts']['3666']['meshes'][0]['geometry']['data']['attributes']['position']['array'];vertices={tuple(round(v,4) for v in mesh[i:i+3]) for i in range(0,len(mesh),3)}
assert vertices=={(-x,y,-z) for x,y,z in vertices}
for lf,rf in zip(lp['frames'][:4],rp['frames'][:4]):
 assert lf['copy_new_ids']==[lf['ids'],rf['ids']]
 assert Counter((pieces[i]['part'],pieces[i]['color']) for i in lf['ids'])==Counter((pieces[i]['part'],pieces[i]['color']) for i in rf['ids'])
 assert lf['copy_source_operations']==[lf['source_operation'],rf['source_operation']]
html=(D/'viewer.html').read_text();assert 'jl=g.module==="tsai",Ql=!!M.bands_installed,Cn(),zn(M.view' in html
assert 'Qs=new Set(x?.manual.overview_new_ids||x?.new_ids||[])' in html
report={'same348_piece_records':True,'same215_operations_and_unique_stock':True,'fail_before':['legacy detailed handler unconditionally disables bands','group11 root overview is local seed190','both carrier groups discard source common-prefix metadata'],'eligible_band_frames':flex,'overview_sweep':overviews,'common_prefix':{'pieces_per_copy':8,'copies':2,'parts_per_panel_per_copy':[1,2,3,2],'matrix_correspondence':matrices,'max_origin_error_ldu':max_error,'origin_tolerance_ldu':.0001,'exact_pose_equality_claimed':False,'3666_local_half_turn_vertexset_precision':.0001,'new_geometry_or_normalization':False},'pins':{n:sha(D/n) for n in ['model.json','instruction-plan.json','viewer.html']},'published_snapshot_pins':{n:sha(P/n) for n in ['model.json','instructions.pdf','viewer.html','index.html','package-manifest.json']},'limits':'Static source/presentation evidence only. Actual flexible visibility, copy returns and PDF/UI readability await separately leased checks; no physical proof.'}
(D/'r2-static-check.json').write_text(json.dumps(report,indent=2));print(json.dumps({'eligible_band_frames':len(flex),'main_overview_changes':[11],'common_prefix_copies':2,'max_origin_error_ldu':max_error,'pins':report['pins']}))

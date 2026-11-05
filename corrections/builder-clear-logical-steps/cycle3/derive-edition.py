from pathlib import Path
import json,copy,hashlib
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;O=R/'builds/clear-logical/cycle3/package';O.mkdir(exist_ok=True)
old=json.loads((R/'builds/clear-logical/cycle2/package/model.json').read_text());m=copy.deepcopy(old);plan=copy.deepcopy(old['instruction_plan']);cross=[]
for new,op in enumerate(m['build_operations'],1):cross.append({'new_operation':new,'source_operation':new,'source_id':op['id']})
for a,b in [(43,44),(45,46)]:
 m['build_operations'][a-1],m['build_operations'][b-1]=m['build_operations'][b-1],m['build_operations'][a-1]
 for new,src in [(a,b),(b,a)]:m['build_operations'][new-1]['step']=new;cross[new-1]={'new_operation':new,'source_operation':src,'source_id':old['build_operations'][src-1]['id']}
for n,pg in [(14,24),(15,25)]:
 s=plan['steps'][n-1];ops=s['operations'];upper=m['build_operations'][ops[0]-1]['ids'];lower=m['build_operations'][ops[1]-1]['ids'];entry=[i for i in s['manual']['ids'] if i not in s['new_ids']]
 s['new_ids']=upper+lower;s['placements']=[dict(ids=upper,direction='top',contacts=[]),dict(ids=lower,direction='top',contacts=[])]
 frames=[]
 for k,ids in enumerate([upper,lower],1):
  frames.append(dict(number=k,title='Attach the upper course to the floor' if k==1 else 'Attach the lower course to the upper course',ids=ids,shown_ids=entry+upper+(lower if k==2 else []),operations=[ops[k-1]],source_operation=cross[ops[k-1]-1]['source_id'],view='underside',preassembled=False,bands_installed=True,image=f'pages/page-{pg}.jpg'))
 s['manual'].update(frames=frames,instance_frames=copy.deepcopy(frames),unit_name='installed floor spacers',note='Attach the upper course first, then the lower course. Keep the chassis assembled; insertion access remains unverified.')
plan['edition_order_correction']={'round':3,'source_pairs_reversed':[[43,44],[45,46]],'authority':'FO explicit narrow upper-before-lower disposition during captain correction round3','source_geometry_changed':False}
m['instruction_plan']=plan;m['instruction_edition']=str(old.get('instruction_edition',''))+' / correction round3 upper-before-lower spacers';m['instruction_order_crosswalk']=cross
assert m['pieces']==old['pieces']
for name,obj in [('instruction-plan.json',plan),('model.json',m)]: (O/name).write_text(json.dumps(obj,indent=2)+'\n')
(P/'operation-crosswalk.json').write_text(json.dumps({'source_model_sha256':hashlib.sha256((R/'builds/clear-logical/cycle2/package/model.json').read_bytes()).hexdigest(),'source_plan_sha256':hashlib.sha256((R/'builds/clear-logical/cycle2/package/instruction-plan.json').read_bytes()).hexdigest(),'operations':cross,'only_changed_sources':[43,44,45,46]},indent=2)+'\n')
# Patch only instruction semantics after the existing payload is decoded, before viewer initialization.
h=(R/'builds/clear-logical/cycle2/package/model-viewer.html').read_text();anchor='window.PROTOTYPE=JSON.parse(await new Response(stream).text());';assert h.count(anchor)==1
patch={k:m[k] for k in ['instruction_plan','build_operations','instruction_edition','instruction_order_crosswalk']}
h=h.replace(anchor,anchor+'Object.assign(window.PROTOTYPE.model,'+json.dumps(patch,separators=(',',':'))+');');h=h.replace('src="ordered-prefix.png"','src="pages/page-04.jpg"')
(O/'model-viewer.html').write_text(h)
print('Derived one edition plan; only original operation pairs43/44 and45/46 swapped. Historical input untouched.')

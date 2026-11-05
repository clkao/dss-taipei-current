from pathlib import Path
import json,copy,hashlib
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;OLD=R/'builds/clear-logical/cycle4/package';O=R/'builds/clear-logical/cycle5/package'
old=json.loads((OLD/'model.json').read_text());m=copy.deepcopy(old);plan=m['instruction_plan'];cross=copy.deepcopy(old['instruction_order_crosswalk'])
m['build_operations'][70],m['build_operations'][71]=m['build_operations'][71],m['build_operations'][70];cross[70],cross[71]=cross[71],cross[70]
for n in [71,72]:m['build_operations'][n-1]['step']=n;cross[n-1]['new_operation']=n
# Copy-local short-rail order now matches the proper rigid occurrence map.
s=plan['steps'][17]
for key in ['frames','instance_frames']:
 ff=s['manual'][key];f11,f12=ff[10],ff[11]
 f11.update(ids=[93],shown_ids=[333,93],operations=[71],source_operation='legacy-057b',title='Fit the first bracket to the loose short rail',note='Keep the rail loose until both brackets are fitted.')
 f12.update(ids=[82],shown_ids=[333,93,82],operations=[72],source_operation='legacy-055b',title='Fit the second bracket to the loose short rail',note='Both brackets are fitted before joining this rail to the lower carrier.')
s['new_ids']=[i for op in m['build_operations'][61:74] if op['kind']=='build' for i in op['ids']]
# Explicit shared recipe records refer to occurrences, never duplicate stock.
finding=json.loads((P/'side-equivalence-finding.json').read_text());units=[]
for name,steps,groups in [('lower carrier',[49,50,51,52],[62,63,64,65]),('long rail',[53,54,55],[66,67,68]),('short rail',[57,58,59],[70,71,72])]:
 units.append({'name':name,'copies':2,'operations_by_copy':[steps,groups],'ids_by_copy':[[i for n in ns for i in m['build_operations'][n-1]['ids']] for ns in [steps,groups]],'per_copy_parts':8 if name=='lower carrier' else 4 if name=='long rail' else 3})
for st in plan['steps'][16:18]:
 recipe=[op for op in m['build_operations'] if op['step'] in st['operations'] and op['kind']=='build']
 st['recipe_operations']=[op['step'] for op in recipe]
 st['recipe_frames']=[dict(end_operation=op['step'],operations=[op['step']],ids=op['ids']) for op in recipe]
plan['side_carrier_presentation']={'shared_method':units,'complete_carriers_congruent':False,'variant':'Long and short rail placement differs relative to the rotated lower carrier.','distinct_chassis_joins':[61,74],'loose_brackets_before_join':[[53,54,55,56],[57,58,59,60],[66,67,68,69],[70,71,72,73]],'source':'cycle5/side-equivalence-finding.json','physical_clearance_verified':False}
plan['edition_order_correction'].update(round='captain-follow-up-cycle5',source_pairs_reversed=[[43,44],[45,46],[71,72]],authority='FO authorized original spacer pairs and narrow right loose-short-rail71/72 swap; no other operation reorder')
m['instruction_order_crosswalk']=cross;m['instruction_edition']+=' / shared side method and right short-rail bracket order'
assert m['pieces']==old['pieces'];assert m['colors']==old['colors'];assert len({x['id'] for x in m['build_operations']})==215
for name,obj in [('model.json',m),('instruction-plan.json',plan),('operation-crosswalk.json',{'operations':cross,'only_changed_original_sources':[43,44,45,46,71,72]})]:
 target=O/name
 if target.is_symlink():target.unlink()
 target.write_text(json.dumps(obj,indent=2)+'\n')
(P/'operation-crosswalk.json').write_bytes((O/'operation-crosswalk.json').read_bytes())
# Start with immutable pre-edition viewer; inject the one current model instruction plan.
h=(R/'builds/clear-logical/cycle2/package/model-viewer.html').read_text();anchor='window.PROTOTYPE=JSON.parse(await new Response(stream).text());';assert h.count(anchor)==1
patch={k:m[k] for k in ['instruction_plan','build_operations','instruction_edition','instruction_order_crosswalk']};h=h.replace(anchor,anchor+'Object.assign(window.PROTOTYPE.model,'+json.dumps(patch,separators=(',',':'))+');').replace('src="ordered-prefix.png"','src="pages/page-04.jpg"')
# Primary PDF guide shows the common method; detailed3D inspection preserves per-copy joins.
assert h.count('</style>')==1
h=h.replace('</style>','#step-title{background:#d86c55;color:white;border-radius:8px;padding:10px 12px}</style>',1)
h=h.replace('80-page PDF','79-page PDF').replace('instructions.pdf#page=72','instructions.pdf#page=71').replace('Print sheets: pages 72–73','Print sheets: pages 71–72')
(O/'model-viewer.html').write_text(h)
print('Only new order swap71/72; current plan includes exact shared recipe occurrences and distinct joins.')

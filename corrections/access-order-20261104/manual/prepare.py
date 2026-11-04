"""DSS-only presentation adapter. One derived correction sequence; no geometry edits."""
import base64,copy,gzip,hashlib,json,re,os
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'builds/access-corrected'
OLD=Path('/Users/clkao/git/house-demo/output/yangliu-refined-v10')
PUB=Path('/Users/clkao/git/dss-taipei-current')
def read(p):return json.loads(p.read_text())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
c=read(ROOT/'corrections/access-order-20261104/candidate-authoring.json'); m=read(ROOT/'sources/minifigure/legacy-v10/model.json')
assert sha(ROOT/'sources/minifigure/legacy-v10/model.json')==c['source_sha256']
OUT.mkdir(parents=True,exist_ok=True);(OUT/'images').mkdir(exist_ok=True)
# Read-only shared assets. Changed images always use new filenames.
for p in (OLD/'images').iterdir():
 q=OUT/'images'/p.name
 if not q.exists():q.symlink_to(p)
for n in ['part-icons.json','front.png','rear.png','render-scene.json','catalog-meshes.json','prototype-summary.json','inventory.csv','preliminary-inventory.csv','wanted-list.xml','bricklink-inventory.csv','bricklink-mapping.json']:
 q=OUT/n
 if not q.exists():q.symlink_to(OLD/n)
for n in ['LICENSE.txt','licenses','credits.html','physical-vehicle-attribution.json','contributor-count.json','tsai-banner','sticker-artwork.zip','soon-white.svg','soon-white-4096.png','ldraw']:
 q=OUT/n
 if (PUB/n).exists() and not q.exists():q.symlink_to(PUB/n)
q=OUT/'yangliu-shape.mpd'
if not q.exists():q.symlink_to(ROOT/'sources/minifigure/legacy-v10/source.mpd')
oldsteps={s['number']:s for s in m['instruction_plan']['steps']}
ops=c['build_operations']; byid={o['id']:o for o in ops}; bylegacy=defaultdict(list)
for o in ops:bylegacy[o['legacy_operation']].append(o['step'])
numbermap={g['legacy_main_step']:g['number'] for g in c['reader_groups']};numbermap[5]=1
contents=defaultdict(set);states={};newstock={}
for o in ops:
 new=set(contents[o['child']]) if o.get('child') else set(o['ids'])
 contents[o['assembly']].update(new);states[o['id']]=sorted(contents[o['assembly']]);newstock[o['id']]=sorted(new)
steps=[];jobs=[];bindings=[]
def render(name,ids,new,view='rear',bands=False):
 jobs.append([name,dict(ids=ids,newIds=new,view=view,width=1600,height=1000,decorations=False,bands=bands)])
 return name+'.png'
for g in c['reader_groups']:
 s=copy.deepcopy(oldsteps[g['legacy_main_step']]);a=s['manual'];s['number']=g['number'];s['legacy_step']=g['legacy_main_step'];s['operations']=[byid[i]['step'] for i in g['operation_ids']];s['end_operation']=s['operations'][-1]
 for k in ['recipe_step']:
  if s.get(k):s[k]=numbermap[s[k]]
 for k in ['repeat_from','repeat_prefix_from']:
  if a.get(k):a[k]=numbermap[a[k]]
 for k in ['recipe_operations']:
  s[k]=[i for n in s.get(k,[]) for i in bylegacy[n]]
 for k in ['frames','instance_frames']:
  for f in a.get(k,[]):f['operations']=[i for n in f['operations'] for i in bylegacy[n]]
 for f in s.get('recipe_frames',[]):
  f['operations']=[i for n in f['operations'] for i in bylegacy[n]];f['end_operation']=f['operations'][-1]
 # Prefix changes affect only old2–4; pins have already been introduced.
 if g['legacy_main_step'] in [2,3,4]:
  a['ids']=sorted(set(a['ids'])|{216,231});a['image']=render(f'images/corrected-{s["number"]:03}-main',a['ids'],s['new_ids'],a['view'])
 if g['panels']:
  frames=[]
  for index,panel in enumerate(g['panels'],1):
   o=byid[panel['operation_id']];new=newstock[o['id']];shown=states[o['id']];view=panel['view'] or 'rear'
   if o['id'] in ['legacy-001a','legacy-001b']:view='underside'
   if o['id']=='legacy-033b':view='top'
   # Open rail undersides and bumper mounting surfaces need a low-angle view.
   if 'upper-rail' in o['assembly'] or 'upper-rail' in o.get('child',''):view='underside'
   frame=dict(number=index,title=panel['title'],note=panel['note'],view=view,ids=new,shown_ids=shown,operations=[o['step']],source_operation=o['id'],kind=o['kind'],child=o.get('child'),assembly=o['assembly'],preassembled=False)
   if o['id'] in ['legacy-035j','legacy-049j1','legacy-049j2','legacy-057j1','legacy-057j2','legacy-050','legacy-058']:
    receiver=sorted(set(shown)-set(new));before=copy.deepcopy(frame)
    before.update(number=len(frames)+1,title='Locate the receiving structure',note='Keep the completed '+o['child'].replace('-',' ')+' separate. Locate the mating surfaces shown here; the next panel shows the installed result. No insertion path is certified.',ids=[],shown_ids=receiver,kind='receiver-context',child=None,awaiting_child=o['child'])
    if o['id']=='legacy-035j':before['view']='underside'
    if o['id'] in ['legacy-049j1','legacy-049j2']:before['view']='front'
    if o['id'] in ['legacy-057j1','legacy-057j2']:before['view']='front-other'
    before['image']=render(f'images/receiver-{o["id"]}',receiver,[],before['view'],a.get('bands_installed',False));frames.append(before)
   frame['number']=len(frames)+1
   frame['image']=render(f'images/corrected-{s["number"]:03}-{index:02}',shown,new,view,a.get('bands_installed',False));frames.append(frame)
   bindings.append(dict(step=s['number'],frame=frame['number'],operation=o['id'],receiver_before=sorted(set(shown)-set(new)),new=new,after=shown,kind=o['kind'],child=o.get('child'),image=frame['image']))
  a['frames']=a['instance_frames']=frames;a['corrected']=True;a['title']=g['title'];a['note']='Follow every ordered panel. Completed units are built separately before their join. Insertion clearance and physical fit remain unverified.'
  for k in ['repeat_prefix_from','repeat_prefix_count','repeat_prefix_frames']:a.pop(k,None)
  s['copies']=1;s['repeat_count']=1
  a['ids']=frames[-1]['shown_ids'];a['image']=frames[-1]['image'];a['view']=frames[-1]['view'];a['approach_frames']=[]
  s['new_ids']=list(dict.fromkeys(i for oid in g['operation_ids'] for i in byid[oid]['ids']))
 steps.append(s)
m['pieces']=c['pieces'];m['build_operations']=ops;m['assembly_roots']=c['assembly_roots'];m['steps']=len(ops)
m['instruction_edition']='Access-order correction / local review';m['revision']='access-order-20261104';m.pop('physical_audit',None)
m['instruction_plan']=dict(schema='house-instructions/1',steps=steps,operation_to_step={str(n):s['number'] for s in steps for n in s['operations']},sections=[])
# The frozen geometry and source metadata are retained; old audit claims are historical only.
m['instruction_correction_source_sha256']=c['source_sha256'];m['instruction_correction_limits']='Static sequence and identity only; physical access is unverified.'
assert len(m['instruction_plan']['operation_to_step'])==len(ops)==215
assert len({i for o in ops for i in o['ids']})==348
save(OUT/'model.json',m);save(OUT/'instruction-plan.json',m['instruction_plan']);save(OUT/'correction-panels.json',bindings);save(OUT/'instruction-render-jobs.json',jobs);save(OUT/'specimen-jobs.json',jobs[:4])
# Reuse exact embedded geometry/library bytes; only replace the model and presentation data.
html=(OLD/'viewer.html').read_text();match=re.search(r'atob\("([A-Za-z0-9+/=]+)"\)',html);assert match
data=json.loads(gzip.decompress(base64.b64decode(match[1])));assert data['model']['pieces']==read(ROOT/'sources/minifigure/legacy-v10/model.json')['pieces']
data['model']=m
original_icons=copy.deepcopy(data.get('recipeIcons',{}))
data['recipeIcons']={str(numbermap[int(k)]):v for k,v in data.get('recipeIcons',{}).items() if int(k)!=5}
for step in steps:
 if step['manual'].get('corrected'):continue
 old=oldsteps[step['legacy_step']]
 if str(old['number']) in original_icons:
  assert data['recipeIcons'][str(step['number'])]==original_icons[str(old['number'])]
  assert step['module']==old['module'] and step['assembly']==old['assembly']
  assert step['manual']['instance_frames'][-1]['ids']==old['manual']['instance_frames'][-1]['ids']
for step in steps:
 for key in ['repeat_from','repeat_prefix_from']:
  if oldsteps[step['legacy_step']]['manual'].get(key) and not step['manual'].get('corrected'):
   assert step['manual'][key]==numbermap[oldsteps[step['legacy_step']]['manual'][key]]

for s in steps:
 if s['manual'].get('corrected'):
  image=OUT/s['manual']['image']
  if image.exists():data.setdefault('recipeIcons',{})[str(s['number'])]='data:image/png;base64,'+base64.b64encode(image.read_bytes()).decode()
payload=base64.b64encode(gzip.compress(json.dumps(data,ensure_ascii=False).encode(),mtime=0)).decode();html=html[:match.start(1)]+payload+html[match.end(1):]
html=html.replace('68 build steps','67 build steps').replace('Digital fit audit complete.','Corrected sequence; physical access remains unverified.')
html=html.replace('</html>', '<script>'+ (Path(__file__).parent/'viewer-notes.js').read_text()+'</script></html>')
(OUT/'viewer.html').write_text(html)
save(OUT/'preparation-evidence.json',dict(model_source_sha256=c['source_sha256'],candidate_sha256=sha(ROOT/'corrections/access-order-20261104/candidate-authoring.json'),legacy_viewer_sha256=sha(OLD/'viewer.html'),operations=215,steps=67,render_jobs=len(jobs),corrected_panels=len(bindings),limits='Source preparation only; render and package review pending.'))
print(json.dumps(dict(output=str(OUT),render_jobs=len(jobs),panels=len(bindings))))

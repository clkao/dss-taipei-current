from pathlib import Path
from collections import Counter
import json,hashlib,math,zipfile
from pypdf import PdfReader
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical';O=B/'cycle4/package';OLD=B/'cycle3/package'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(P/n).write_text(json.dumps(v,indent=2)+'\n')
fixed=['model.json','instruction-plan.json','model-viewer.html','viewer.html','operation-crosswalk.json']
assert all(sha(O/n)==sha(OLD/n) for n in fixed)
m=json.loads((O/'model.json').read_text());plan=json.loads((O/'instruction-plan.json').read_text());assert m['instruction_plan']==plan
ids=[p['id'] for p in m['pieces']];assert len(ids)==len(set(ids))==348;assert Counter(i for s in plan['steps'] for i in s['new_ids'])==Counter(ids);assert len(m['build_operations'])==215
assert sha(OLD/'instructions.pdf')=='c2cc842abc833241d8d543831d879c6273d9bfb9b12b05d4077afdd47de92ae0';assert sha(OLD/'release.zip')=='7427dbd7a7e642b61a852fc7840e8b4075c8494939b2220f22e48fe32e8bf533'
a=PdfReader(OLD/'instructions.pdf');b=PdfReader(O/'instructions.pdf');assert len(a.pages)==len(b.pages)==80;changed=[4,23,24,25,36];same=[]
for n,page in enumerate(b.pages,1):
 assert abs(float(page.mediabox.width)-841.89)<1 and abs(float(page.mediabox.height)-595.28)<1
 if n not in changed:
  assert page.get_contents().get_data()==a.pages[n-1].get_contents().get_data();assert sha(O/f'pages/page-{n:02d}.jpg')==sha(OLD/f'pages/page-{n:02d}.jpg');same.append(n)
manifest=json.loads((O/'package-manifest.json').read_text());assert all(sha(O/n)==h for n,h in manifest['files'].items())
browser=json.loads((B/'cycle4/browser-review-hidden/browser-check.json').read_text());assert not browser['errors'];assert [c['page'] for c in browser['checks']]==changed
prior=json.loads((P.parent/'cycle3/browser-check.json').read_text());assert not prior['errors'];edition=next(c for c in prior['checks'] if c.get('edition_plan_equal'));assert len(edition['spacer_frame_checks'])==4
loc=json.loads((B/'cycle4/requested-views/receiver-locations.json').read_text());assert all(x['source_unchanged'] for x in loc.values())
# Actual catalog subpart stud centers, not a bounding box or plate origin.
z=zipfile.ZipFile(B/'cycle1/catalog.zip');sources={}
for name in ['ldraw/parts/3460.dat','ldraw/parts/s/3460s01.dat','ldraw/parts/3666.dat','ldraw/parts/s/3666s01.dat','ldraw/p/stud.dat','ldraw/p/stug-1x8.dat','ldraw/p/stug-1x6.dat']:
 raw=z.read(name);sources[name]={'sha256':hashlib.sha256(raw).hexdigest(),'text':raw.decode()}
for name,x in [('ldraw/p/stug-1x8.dat',10),('ldraw/p/stug-1x6.dat',-10)]:
 rows=[l.split() for l in sources[name]['text'].splitlines() if l.startswith('1 ') and l.endswith('stud.dat')]
 assert any([float(a) for a in row[2:5]]==[x,0,0] for row in rows)
assert '1 16 0 -4 0' in sources['ldraw/p/stud.dat']['text']
checks=[]
for i in [0,2]:
 aa,bb=loc['floor-studs']['targets'][i:i+2];assert aa['local']==[10,8,-30] and bb['local']==[10,-4,0];error=max(abs(aa['world'][j]-bb['world'][j]) for j in [0,2]);assert error<1e-5
 checks.append({'floor_id':aa['id'],'receiver_id':bb['id'],'floor_cavity_local_ldu':aa['local'],'receiver_stud_top_local_ldu':bb['local'],'horizontal_axis_error_scene_units':error})
axes=[]
for name,count in [('core-thread',2),('spacer14-thread',4),('spacer15-thread',4)]:
 for i in range(count):
  ts=loc[name]['targets'][i*4:i*4+4];aa,bb=ts[0],ts[-1];dx=(bb['x']-aa['x'])*1400;dy=(bb['y']-aa['y'])*1000;l=math.hypot(dx,dy);error=max(abs(dx*(t['y']-aa['y'])*1000-dy*(t['x']-aa['x'])*1400)/l for t in ts);assert error<.01
  axes.append({'diagram':name,'axis':i,'maximum_projected_collinearity_error_pixels':error,'one_arrowhead':True})
save('feature-check.json',{'catalog_sources':sources,'p23_pairs':checks,'rejected_origin_x0_between_studs':True,'alignment_axes':axes,'p36_stud_targets':json.loads((B/'cycle4/selected-bed/receiver-locations.json').read_text())['bed-selected-B']['targets'],'physical_insertion_verified':False})
save('browser-check.json',browser)
save('validation.json',{'bindings':{n:sha(O/n) for n in fixed+['instructions.pdf']},'same_derived_sequence_geometry_stock_as_cycle3':True,'source_order_equal_to_original':False,'retained_authorized_original_order_delta':[[44,43],[46,45]],'unique_introductions':348,'operations':215,'pages_A4':80,'changed_pages':changed,'unchanged_page_content_streams_and_raster_bytes':same,'loose_members_verified':len(manifest['files']),'new_browser_image_paths':changed,'reused_four_frame_sequence_check':{'path':'../cycle3/browser-check.json','sha256':sha(P.parent/'cycle3/browser-check.json'),'reason':'Exact model, plan, guide and model-viewer bytes unchanged; cycle3 actual navigation, ownership, bands and downstream step16 result reused.'},'historical_cycle3_preserved':True,'independent_review':False,'captain_acceptance':False,'physical_verified':False})
print('75 unchanged page streams/rasters; 109 members; exact cycle3 plan/viewers; real stud and coherent-axis checks passed.')

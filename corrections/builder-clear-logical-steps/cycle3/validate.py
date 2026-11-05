from pathlib import Path
from collections import Counter
import json,hashlib,math
from pypdf import PdfReader
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical';O=B/'cycle3/package';OLD=B/'cycle2/package';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'model.json').read_text());old=json.loads((OLD/'model.json').read_text());plan=json.loads((O/'instruction-plan.json').read_text());cross=json.loads((P/'operation-crosswalk.json').read_text())['operations'];assert m['instruction_plan']==plan;assert m['pieces']==old['pieces'];assert m['colors']==old['colors'];assert m['suspension_bands']==old['suspension_bands']
assert sha(OLD/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(OLD/'instruction-plan.json')=='df9ef0bf23d3f1ab71ac98dbe8dc351073658f241b7f705bf84a991cc412d9ff'
assert sha(OLD/'instructions.pdf')=='19d5c4262279624e38635367f958fcb9ccd6ffa87ca3b9a8f0da91da87d1716c';assert sha(OLD/'release.zip')=='98fc465d0f6bb04d4eb4100efb2bb40984f9a80469b007e472befe88c5325c00'
expected=list(range(1,216));expected[42:46]=[44,43,46,45];assert [x['source_operation'] for x in cross]==expected
for new,src in enumerate(expected,1):
 a=dict(m['build_operations'][new-1]);a['step']=src;assert a==old['build_operations'][src-1]
assert Counter(i for o in m['build_operations'] if o['kind']=='build' for i in o['ids'])==Counter(i for o in old['build_operations'] if o['kind']=='build' for i in o['ids'])
ids=[p['id'] for p in m['pieces']];assert len(ids)==len(set(ids))==348;assert Counter(i for s in plan['steps'] for i in s['new_ids'])==Counter(ids)
for n in range(1,68):
 a=plan['steps'][n-1];b=old['instruction_plan']['steps'][n-1]
 if n not in [14,15]:assert a==b
 else:
  assert a['manual']['ids']==b['manual']['ids'];f=a['manual']['frames'];upper=m['build_operations'][a['operations'][0]-1]['ids'];lower=m['build_operations'][a['operations'][1]-1]['ids'];assert f[0]['ids']==upper and f[1]['ids']==lower;assert not set(lower)&set(f[0]['shown_ids']);assert set(f[1]['shown_ids'])==set(b['manual']['ids'])
# Source-bound connector grid control, distinct from insertion/physical verification.
ps={p['id']:p for p in m['pieces']};rows=[]
for n,plate in [(14,99),(15,129)]:
 upper=plan['steps'][n-1]['placements'][0]['ids'];po=ps[plate]['transform']['origin']
 for i in upper:
  v=ps[i]['transform']['origin'];x,z=(v[0]-po[0])*20,(v[1]-po[1])*20;err=max(min(abs(x-a) for a in range(-70,71,20)),min(abs(z-a) for a in range(-50,51,20)));plane=abs(v[2]-(po[2]-.4));assert err<.0001 and plane<.00001
  rows.append(dict(upper_id=i,floor_id=plate,cavity_local_ldu=[x,8,z],grid_error_ldu=err,plane_error_scene_units=plane))
shadow=Path(json.loads((R/'manifests/tooling.json').read_text())['shadow']['path']);sources={}
for name in ['parts/3036.dat','parts/6141.dat','p/stud.dat']:sources[name]={'sha256':sha(shadow/name),'text':(shadow/name).read_text()}
(P/'receiver-correspondence.json').write_text(json.dumps({'upper_to_floor':rows,'shadow_sources':sources,'catalog_alignment_demonstrated':True,'automated_connector_engine_rerun':False,'physical_fit_or_insertion_verified':False},indent=2)+'\n')
a=PdfReader(OLD/'instructions.pdf');b=PdfReader(O/'instructions.pdf');assert len(a.pages)==len(b.pages)==80;changed=[4,23,24,25,36];same=[]
for n,page in enumerate(b.pages,1):
 assert abs(float(page.mediabox.width)-841.89)<1 and abs(float(page.mediabox.height)-595.28)<1
 if n not in changed:assert page.get_contents().get_data()==a.pages[n-1].get_contents().get_data();assert sha(O/f'pages/page-{n:02d}.jpg')==sha(OLD/f'pages/page-{n:02d}.jpg');same.append(n)
for n in [24,25]:assert 'Upper layer first' in b.pages[n-1].extract_text() and 'Lower layer next' in b.pages[n-1].extract_text()
for folder in ['bed-specimen','core-floor','spacers','finalviews']:
 loc=json.loads((B/'cycle3'/folder/'receiver-locations.json').read_text());assert all(v['source_unchanged'] for v in loc.values())
manifest=json.loads((O/'package-manifest.json').read_text());assert all(sha(O/n)==h for n,h in manifest['files'].items());browser=json.loads((B/'cycle3/browser-review/browser-check.json').read_text());assert not browser['errors'];edition=next(c for c in browser['checks'] if c.get('edition_plan_equal'));assert len(edition['spacer_frame_checks'])==4
result={'model_sha256':sha(O/'model.json'),'plan_sha256':sha(O/'instruction-plan.json'),'model_viewer_sha256':sha(O/'model-viewer.html'),'pdf_sha256':sha(O/'instructions.pdf'),'viewer_sha256':sha(O/'viewer.html'),'source_piece_records_exact':True,'colors_bands_geometry_unchanged':True,'source_order_equal':False,'authorized_order_delta':[[44,43],[46,45]],'other_operations_exact':True,'pieces_unique_introductions':348,'operations':215,'pages_A4':80,'changed_pages':changed,'unchanged_page_content_streams_and_raster_bytes':same,'spacer_entry_exit_unchanged':True,'browser_plan_equal':True,'four_browser_frames_ownership_and_bands_pass':True,'downstream_step16_unchanged':True,'loose_members_verified':len(manifest['files']),'historical_cycle2_bytes_preserved':True,'independent_pass_claimed':False,'captain_acceptance':False,'physical_verified':False}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

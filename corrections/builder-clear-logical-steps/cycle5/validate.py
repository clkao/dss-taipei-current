from pathlib import Path
from collections import Counter
import json,hashlib,re
from pypdf import PdfReader
from PIL import Image,ImageChops,ImageDraw
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical';O=B/'cycle5/package';OLD=B/'cycle4/package';ORIG=B/'cycle2/package';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'model.json').read_text());old=json.loads((OLD/'model.json').read_text());orig=json.loads((ORIG/'model.json').read_text());plan=json.loads((O/'instruction-plan.json').read_text());assert m['instruction_plan']==plan
for k in ['pieces','colors','suspension_bands']:assert m[k]==old[k]==orig[k],k
expected=list(range(1,216));expected[42:46]=[44,43,46,45];expected[70:72]=[72,71]
for n,src in enumerate(expected,1):
 a=dict(m['build_operations'][n-1]);a['step']=src;assert a==orig['build_operations'][src-1],n
cross=json.loads((O/'operation-crosswalk.json').read_text())['operations'];assert [x['source_operation'] for x in cross]==expected
ids=[p['id'] for p in m['pieces']];assert len(ids)==len(set(ids))==348;assert Counter(i for s in plan['steps'] for i in s['new_ids'])==Counter(ids)
units=plan['side_carrier_presentation']['shared_method'];assert [u['per_copy_parts'] for u in units]==[8,4,3]
for copy,step in [(0,17),(1,18)]:
 assert Counter(i for u in units for i in u['ids_by_copy'][copy])==Counter(plan['steps'][step-1]['new_ids'])
 for u in units:assert len(u['ids_by_copy'][copy])==u['per_copy_parts']
assert m['build_operations'][70]['ids']==[93] and m['build_operations'][71]['ids']==[82];assert plan['steps'][17]['manual']['frames'][10]['shown_ids']==[333,93] and plan['steps'][17]['manual']['frames'][11]['shown_ids']==[333,93,82]
assert plan['steps'][18]==old['instruction_plan']['steps'][18],'Step19 witness changed'
r=PdfReader(O/'instructions.pdf');assert len(r.pages)==79
for page in r.pages:assert abs(float(page.mediabox.width)-841.89)<1 and abs(float(page.mediabox.height)-595.28)<1
for n in range(27,33):assert not re.search(r'\b[ABC](?:17|18)\b',r.pages[n-1].extract_text())
assert sha(O/'index.html')==sha(O/'viewer.html')
s=(O/'viewer.html').read_text();a=s.index('const titles=')+len('const titles=');b=s.index(';const select=',a);titles=json.loads(s[a:b]);assert len(titles)==79;assert not (O/'pages/page-80.jpg').exists()
h=(O/'model-viewer.html').read_text();assert 'instructions.pdf#page=71' in h and 'Print sheets: pages 71–72' in h and '79-page PDF' in h
pre=json.loads((O/'print-preflight.json').read_text());assert pre['pages']==pre['pdf_pages']==79 and [x['page'] for x in pre['print_sheets']]==[71,72]
manifest=json.loads((O/'package-manifest.json').read_text());assert len(manifest['files'])==108 and all(sha(O/n)==v for n,v in manifest['files'].items())
# Image-equivalence below exactly recorded heading/footer edits. No claim of whole-page byte equality.
by={x['page']:x for x in json.loads((P/'heading-changes.json').read_text())['pages']};same=[];limits=[]
for n in range(1,80):
 oldn=n if n<33 else n+1
 if n in [27,28,29,30,31,32,35]:continue
 a=Image.open(OLD/f'pages/page-{oldn:02d}.jpg').convert('RGB');b=Image.open(O/f'pages/page-{n:02d}.jpg').convert('RGB');assert a.size==b.size;d=ImageChops.difference(a,b);draw=ImageDraw.Draw(d);rects=[]
 for row in by.get(n,{}).get('changes',[]):
  for key in ['rect','new_rect']:
   if key not in row:continue
   x,y,w,hh=row[key];sx=a.width/841.8897638;sy=a.height/595.2755906;box=[int(x*sx)-16,int((595.2755906-y-hh)*sy)-16,int((x+w)*sx)+16,int((595.2755906-y)*sy)+16];draw.rectangle(box,fill=0);rects.append(box)
 if oldn in {7,17,34,37,38,41,42,43,45,46,47,52,53,54,56,61,63,65}:draw.rectangle((20,60,1180,135),fill=0);rects.append([20,60,1180,135])
 if n>=33:draw.rectangle((1100,790,1200,840),fill=0);rects.append([1100,790,1200,840])
 assert d.getbbox() is None,(n,d.getbbox());same.append(n);limits.append({'page':n,'source_page':oldn,'excluded_heading_footer_rectangles_pixels':rects})
assert len(same)==72
feature=[]
for folder in ['variants-inside','placements']:
 loc=json.loads((B/'cycle5'/folder/'receiver-locations.json').read_text())
 for name,v in loc.items():
  assert v['source_unchanged']
  for k in [0,2]:
   a,b=v['targets'][k:k+2];err=max(abs(a['world'][i]-b['world'][i]) for i in [0,2]);assert err<1e-5;feature.append({'diagram':name,'from':a,'to':b,'horizontal_error_scene_units':err})
browser=json.loads((B/'cycle5/browser-review/browser-check.json').read_text());assert not browser['errors'];check=next(x for x in browser['checks'] if x.get('edition_plan_equal'));assert len(check['carrier_frame_checks'])==5
assert sha(OLD/'instructions.pdf')=='89c7b5aee2ce4584e8bc9fc6bce6dfe92f997b8cca06cc6d1f2de28cdb1da28f';assert sha(OLD/'release.zip')=='06689b907c4780982ace5ac8acfdfa60b3ca3677bdbaab6a72017f658e21f1e1'
result={'model_sha256':sha(O/'model.json'),'plan_sha256':sha(O/'instruction-plan.json'),'pdf_sha256':sha(O/'instructions.pdf'),'model_viewer_sha256':sha(O/'model-viewer.html'),'guide_and_index_sha256':sha(O/'viewer.html'),'unique_pieces_and_introductions':348,'operations':215,'only_original_order_exceptions':[[44,43],[46,45],[72,71]],'piece_records_colors_bands_exact':True,'step19_witness_unchanged':True,'source_rigid_congruence_complete_carriers':False,'shared_unit_sizes':[8,4,3],'pages_A4':79,'source_page33_removed':True,'source36_to35_and37_to36':True,'unchanged_regions_pages':same,'pixel_comparison_exclusions':limits,'feature_correspondence':feature,'five_actual_carrier_frames_and_step19_checked':True,'loose_members_verified':108,'prior_cycle4_preserved':True,'physical_verified':False,'captain_acceptance':False,'independent_review':False}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(P/'browser-check.json').write_text(json.dumps(browser,indent=2)+'\n');print('79 A4;72 unchanged diagram/tray regions;348 exact pieces;215 unique ops;only3 authorized swaps;actual carrier frames passed.')

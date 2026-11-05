"""Check immutable source, operation/stock ownership, and exact PDF/ZIP bindings."""
from pathlib import Path
from collections import Counter
import hashlib,json,zipfile
from pypdf import PdfReader
R=Path(__file__).resolve().parents[2];B=R/'builds/clear-logical';O=B/'candidate';P=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((O/'model.json').read_text());steps=m['instruction_plan']['steps'];mapping=json.loads((O/'pdf-page-map.json').read_text())
assert sha(O/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(O/'instruction-plan.json')=='df9ef0bf23d3f1ab71ac98dbe8dc351073658f241b7f705bf84a991cc412d9ff'
ids=[p['id'] for p in m['pieces']];assert len(ids)==len(set(ids))==348
introduced=[i for s in steps for i in s['new_ids']];assert Counter(introduced)==Counter(ids)
ops=[i for s in steps for i in s['operations']];assert sorted(ops)==list(range(1,216))
focused=[p for p in mapping['page_records'] if 'focused_page' in p];changed={n for p in focused for n in p['steps']}
for n in changed:
 rows=[p for p in focused if p['steps']==[n]]
 assert Counter(i for p in rows for i in p['new_ids'])==Counter(steps[n-1]['new_ids']),('stock',n)
 assert Counter(i for p in rows for i in p['operations'])==Counter(steps[n-1]['operations']),('operations',n)
checks=[]
for folder in ['assets','assets-v2','assets-v3','detail-final','feet','cabin-detail']:
 loc=json.loads((B/folder/'receiver-locations.json').read_text());assert all(r['source_unchanged'] for r in loc.values());checks.append({'folder':folder,'rendered_views':len(loc),'source_records_unchanged':True})
r=PdfReader(O/'instructions.pdf');assert len(r.pages)==mapping['pages']==80
for page in r.pages:assert abs(float(page.mediabox.width)-841.89)<1 and abs(float(page.mediabox.height)-595.28)<1
for n in range(1,81):assert (O/'pages'/f'page-{n:02d}.jpg').is_file()
manifest=json.loads((O/'package-manifest.json').read_text())
with zipfile.ZipFile(O/'release.zip') as z:
 for name,h in manifest['files'].items():assert sha(O/name)==h==hashlib.sha256(z.read(name)).hexdigest(),name
result={'model_sha256':sha(O/'model.json'),'plan_sha256':sha(O/'instruction-plan.json'),'pdf_sha256':sha(O/'instructions.pdf'),'viewer_sha256':sha(O/'viewer.html'),'zip_sha256':sha(O/'release.zip'),'pieces':348,'unique_introductions':348,'source_operations':215,'changed_steps_stock_and_operation_coverage':sorted(changed),'source_render_checks':checks,'pages':80,'all_page_rasters_exist':True,'all_pages_A4_landscape':True,'zip_member_hashes_match':True,'independent_review':'pending','human_acceptance':False,'physical_verified':False}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

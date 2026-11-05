from pathlib import Path
from collections import Counter
import json,hashlib
from pypdf import PdfReader
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical';O=B/'cycle1/package';OLD=B/'candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
changed=[10,12,14,16,24,25,69,71]
prior=json.loads((P.parent/'validation.json').read_text())
for f,key in [('model.json','model_sha256'),('instruction-plan.json','plan_sha256')]:assert sha(O/f)==prior[key]
for f,key in [('instructions.pdf','pdf_sha256'),('viewer.html','viewer_sha256'),('release.zip','zip_sha256')]:assert sha(OLD/f)==prior[key]
m=json.loads((O/'model.json').read_text());s=m['instruction_plan']['steps'];ids=[p['id'] for p in m['pieces']]
assert len(ids)==len(set(ids))==348
assert Counter(i for a in s for i in a['new_ids'])==Counter(ids)
assert sorted(i for a in s for i in a['operations'])==list(range(1,216))
a=PdfReader(OLD/'instructions.pdf');b=PdfReader(O/'instructions.pdf');assert len(a.pages)==len(b.pages)==80
unchanged=[]
for n,p in enumerate(b.pages,1):
 assert abs(float(p.mediabox.width)-841.89)<1 and abs(float(p.mediabox.height)-595.28)<1
 if n not in changed:
  assert p.get_contents().get_data()==a.pages[n-1].get_contents().get_data(),n
  assert sha(O/f'pages/page-{n:02d}.jpg')==sha(OLD/f'pages/page-{n:02d}.jpg')
  unchanged.append(n)
 else:assert sha(O/f'pages/page-{n:02d}.jpg')!=sha(OLD/f'pages/page-{n:02d}.jpg')
for folder in ['renders','renders-feet-top']:
 loc=json.loads((B/'cycle1'/folder/'receiver-locations.json').read_text());assert all(v['source_unchanged'] for v in loc.values())
manifest=json.loads((O/'package-manifest.json').read_text());assert all(sha(O/n)==h for n,h in manifest['files'].items())
check=json.loads((B/'cycle1/browser-review/browser-check.json').read_text());assert not check['errors']
result={'model_sha256':sha(O/'model.json'),'plan_sha256':sha(O/'instruction-plan.json'),'pdf_sha256':sha(O/'instructions.pdf'),'viewer_sha256':sha(O/'viewer.html'),'pieces':348,'unique_introductions':348,'source_operations':215,'pages':80,'A4_landscape':True,'changed_pages':changed,'unchanged_pdf_content_streams_and_page_rasters':unchanged,'loose_manifest_members_verified':len(manifest['files']),'render_source_records_unchanged':True,'rejected_pdf_viewer_zip_unchanged':True,'browser_errors':[],'human_acceptance':False,'physical_verified':False,'independent_review':'pending'}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

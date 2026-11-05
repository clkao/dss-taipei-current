from pathlib import Path
from pypdf import PdfReader
import json,hashlib
ROOT=Path(__file__).resolve().parents[4];D=ROOT/'builds/access-corrected-hybrid-prefix';OLD=ROOT/'builds/access-corrected-r2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'model.json').read_text());page=json.loads((D/'pdf-page-map.json').read_text());prior=json.loads((OLD/'pdf-page-map.json').read_text());pdf=PdfReader(D/'instructions.pdf')
assert len(pdf.pages)==page['pages']==136
assert all(abs(float(p.mediabox.width)-841.89)<1 and abs(float(p.mediabox.height)-595.276)<1 for p in pdf.pages)
assert sha(D/'model.json')==sha(OLD/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert sha(D/'instruction-plan.json')==sha(OLD/'instruction-plan.json')
assert len(m['pieces'])==348 and len(m['build_operations'])==215
records=page['page_records'];diagram=[r for r in records if r['kind']=='ordered-construction-diagram'];assert len(diagram)==1
assert diagram[0]==dict(page=4,kind='ordered-construction-diagram',step=1,panels=[1,2,3],source_operations=['legacy-001a','legacy-012','legacy-001b'],image='ordered-prefix.png')
expected=[r for r in prior['page_records'] if r['page'] not in [4,5,6]];actual=[r for r in records if r['page']!=4]
assert [{k:v for k,v in r.items() if k!='page'} for r in expected]==[{k:v for k,v in r.items() if k!='page'} for r in actual]
for old,new in zip(expected,actual):assert new['page']==old['page']-(2 if old['page']>6 else 0)
for r in actual:
 if 'image' in r:assert sha(D/r['image'])==sha(OLD/r['image'])
texts=[p.extract_text() for p in pdf.pages]
assert 'BOTH exposed pins' in texts[3]
assert sum('2x / parts for one copy' in t for t in texts)==4
assert sum('Use the second base from step 17' in t for t in texts)==1
sheets=[r['page'] for r in records if r['kind'] in ['sticker-sheet','speech-bubble-print-sheet']];assert sheets==[128,129]
assert page['pdf_sha256']==sha(D/'instructions.pdf')
result=dict(actual_pages=136,diagram_page=4,source_operations=diagram[0]['source_operations'],actual_print_sheets=sheets,remaining_page_metadata_equal=True,model_plan_images_unchanged=True,pdf_sha256=sha(D/'instructions.pdf'),map_sha256=sha(D/'pdf-page-map.json'),visual_review='pending',physical_tested=False)
(D/'hybrid-pdf-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

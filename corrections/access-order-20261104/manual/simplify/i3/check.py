from pathlib import Path
import json,hashlib
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[5];D=ROOT/'builds/simplification-i3';BASE=ROOT/'builds/access-corrected-hybrid-prefix'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
model=json.loads((D/'model.json').read_text());mapping=json.loads((D/'pdf-page-map.json').read_text());pdf=PdfReader(D/'instructions.pdf')
assert sha(D/'model.json')==sha(BASE/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
assert len(model['pieces'])==348 and len(model['build_operations'])==215
ids=[i for s in model['instruction_plan']['steps'] for i in s['new_ids']];assert len(ids)==len(set(ids))==348
assert len(pdf.pages)==mapping['pages']==69
assert set(mapping['steps'])==set(map(str,range(1,68)))
assert mapping['pdf_sha256']==sha(D/'instructions.pdf')
assert all(abs(float(p.mediabox.width)-841.8898)<.01 and abs(float(p.mediabox.height)-595.2756)<.01 for p in pdf.pages)
assert not (D/'instructions.pdf').is_symlink() and not (D/'pdf-page-map.json').is_symlink()
assert sha(BASE/'instructions.pdf')=='6d02aa7dbf0e9fc58cbc4f963bd9fbe805bba9a1cdd134a1ecc3d1b22e9ac062'
measure=json.loads((D/'tray-measurements.json').read_text())
assert all(40+l['printed_width']+10<=t['cell_width']+.001 for t in measure for l in t['labels'])
record={'measured_tray_cells':len(measure),'pages':len(pdf.pages),'pdf_sha256':sha(D/'instructions.pdf'),'map_sha256':sha(D/'pdf-page-map.json'),'unchanged_model_sha256':sha(D/'model.json'),'source_steps':67,'source_operations':215,'unique_parts':348,'visual_review':'pending; this static check is not readability or physical proof','baseline_immutable':True}
(D/'static-check.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))

text='\n'.join(p.extract_text() or '' for p in pdf.pages)
assert '39:96' not in text and '46:115' not in text
assert 'Build 1 more shield / recipe 52' in text

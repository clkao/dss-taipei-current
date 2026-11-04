from pathlib import Path
from pypdf import PdfReader
import json,hashlib
D=Path(__file__).parent;m=json.loads((D/'model.json').read_text());page=json.loads((D/'pdf-page-map.json').read_text());pdf=PdfReader(D/'instructions.pdf')
assert len(pdf.pages)==page['pages']==138
assert all(abs(float(p.mediabox.width)-841.89)<1 and abs(float(p.mediabox.height)-595.276)<1 for p in pdf.pages)
records=page['page_records'];panels=[x for x in records if x['kind']=='corrected-ordered-panel'];assert len(panels)==48
assert [x['panel'] for x in panels if x['step']==17]==list(range(1,17))
assert [x['panel'] for x in panels if x['step']==18]==list(range(5,17))
texts=[p.extract_text() for p in pdf.pages];assert sum('2x / parts for one copy' in t for t in texts)==4
assert sum('Use the second base from step 17' in t for t in texts)==1
sheets=[x['page'] for x in records if x['kind'] in ['sticker-sheet','speech-bubble-print-sheet']];assert sheets==[130,131]
assert page['pdf_sha256']==hashlib.sha256((D/'instructions.pdf').read_bytes()).hexdigest()
assert len(m['pieces'])==348 and len(m['build_operations'])==215
result={'actual_pages':len(pdf.pages),'corrected_printed_panels':len(panels),'left_common_2x_pages':4,'right_prefix_omitted':True,'right_explicit_remaining_copy_note':True,'actual_print_pages':sheets,'pdf_sha256':page['pdf_sha256'],'page_map_sha256':hashlib.sha256((D/'pdf-page-map.json').read_bytes()).hexdigest(),'limits':'Artifact/text accounting only; actual A4 visual review remains separate.'}
(D/'r2-pdf-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

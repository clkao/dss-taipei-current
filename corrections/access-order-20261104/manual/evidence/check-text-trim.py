from pypdf import PdfReader
from pathlib import Path
import json,hashlib
p=Path(__file__).parent;r=PdfReader(p/'instructions.pdf');assert len(r.pages)==142
assert all(abs(float(x.mediabox.width)-841.89)<1 and abs(float(x.mediabox.height)-595.276)<1 for x in r.pages)
t='\n'.join(x.extract_text() for x in r.pages)
for s in ['Installed view - insertion clearance','ACCESS-ORDER CORRECTION / LOCAL REVIEW','unchanged final model','pieces already built. Do not collect']:assert s not in t,s
assert 'remain unverified' in t
old=json.loads((p/'before-text-trim/pdf-page-map.json').read_text());new=json.loads((p/'pdf-page-map.json').read_text())
assert old['pdf_sha256']==hashlib.sha256((p/'before-text-trim/instructions.pdf').read_bytes()).hexdigest()
assert new['pdf_sha256']==hashlib.sha256((p/'instructions.pdf').read_bytes()).hexdigest()
assert {k:v for k,v in old.items() if k!='pdf_sha256'}=={k:v for k,v in new.items() if k!='pdf_sha256'}
print('142 landscape A4 pages; exact page/source/image map except correctly rebound PDF hash; reduced prose and retained limits')

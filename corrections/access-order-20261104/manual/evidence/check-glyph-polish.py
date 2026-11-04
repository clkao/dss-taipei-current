from pathlib import Path
from pypdf import PdfReader
import hashlib,json
p=Path(__file__).parent;old=PdfReader(p/'before-glyph-polish/instructions.pdf');new=PdfReader(p/'instructions.pdf');affected={36,37,39,127};assert len(old.pages)==len(new.pages)==142
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for n,(a,b) in enumerate(zip(old.pages,new.pages),1):
 assert list(a.mediabox)==list(b.mediabox)
 before=a.get_contents().get_data();after=b.get_contents().get_data()
 if n not in affected:assert before==after,('unexpected page-content change',n)
 # Exact image bytes/placement operator streams are retained; text is the only authorized change.
 def images(page):
  return sorted(sha(im.data) for im in page.images)
 assert images(a)==images(b),('changed images',n)
 rows.append(dict(page=n,old_content_sha256=sha(before),new_content_sha256=sha(after),changed=before!=after))
text={n:new.pages[n-1].extract_text() for n in affected}
for n in [36,37,39]:assert 'Turn:' in text[n] and '↻' not in text[n]
assert '洋 above / 流 below / both faces.' in text[127]
a=json.loads((p/'before-glyph-polish/pdf-page-map.json').read_text());b=json.loads((p/'pdf-page-map.json').read_text())
assert a.pop('pdf_sha256')==sha((p/'before-glyph-polish/instructions.pdf').read_bytes())
assert b.pop('pdf_sha256')==sha((p/'instructions.pdf').read_bytes())
assert a==b
result=dict(pages=142,affected_pages=sorted(affected),unchanged_page_content_streams=138,all_page_images_identical=True,map_identical_except_bound_pdf_hash=True,pdf_sha256=sha((p/'instructions.pdf').read_bytes()),page_comparison=rows)
(p/'glyph-equivalence.json').write_text(json.dumps(result,indent=2));print('PASS: four-page text-only correction;138 unchanged content streams; all images unchanged')

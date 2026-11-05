from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import IndirectObject,StreamObject,DictionaryObject,ArrayObject
import hashlib,json
R=Path(__file__).resolve().parents[5];A=R/'builds/simplification-i3';B=R/'builds/simplification-i3-polish';affected={45,56,57}
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((A/'instructions.pdf').read_bytes())=='42948683c57d88986c5eb85029a848d6212c156b14ac566cb3c875afdef64ae3'
old=PdfReader(A/'instructions.pdf');new=PdfReader(B/'instructions.pdf');assert len(old.pages)==len(new.pages)==69
# Compare semantic resource objects, resolving indirect object numbers without dropping fields.
def canonical(x):
 if isinstance(x,IndirectObject):return canonical(x.get_object())
 if isinstance(x,StreamObject):return {'dictionary':{str(k):canonical(v) for k,v in x.items()},'decoded_stream':sha(x.get_data())}
 if isinstance(x,DictionaryObject):return {str(k):canonical(v) for k,v in x.items()}
 if isinstance(x,ArrayObject):return [canonical(v) for v in x]
 if isinstance(x,bytes):return {'bytes':x.hex()}
 return str(x)
rows=[]
for n,(a,b) in enumerate(zip(old.pages,new.pages),1):
 assert list(a.mediabox)==list(b.mediabox)
 sa=a.get_contents().get_data();sb=b.get_contents().get_data()
 if n not in affected:
  assert sa==sb,('page content',n)
  assert canonical(a['/Resources'])==canonical(b['/Resources']),('page resources',n)
  assert sorted(sha(im.data) for im in a.images)==sorted(sha(im.data) for im in b.images),('page images',n)
 rows.append({'page':n,'old_stream':sha(sa),'new_stream':sha(sb),'changed':sa!=sb})
assert 'After / outer face' in new.pages[44].extract_text()
a=json.loads((A/'pdf-page-map.json').read_text());b=json.loads((B/'pdf-page-map.json').read_text())
assert a.pop('pdf_sha256')==sha((A/'instructions.pdf').read_bytes());assert b.pop('pdf_sha256')==sha((B/'instructions.pdf').read_bytes());assert a==b
assert sha((A/'model.json').read_bytes())==sha((B/'model.json').read_bytes())=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
result={'pages':69,'affected':sorted(affected),'unchanged_content_resources_images_pages':66,'map_equal_except_bound_pdf_hash':True,'source_model_unchanged':True,'pdf_sha256':sha((B/'instructions.pdf').read_bytes()),'map_sha256':sha((B/'pdf-page-map.json').read_bytes()),'page_streams':rows}
(B/'polish-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='page_streams'}))

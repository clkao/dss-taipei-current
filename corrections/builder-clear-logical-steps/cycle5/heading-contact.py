from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical/cycle5';O=B/'heading-review';O.mkdir(exist_ok=True)
items=[]
for n in range(4,71):
 im=Image.open(B/f'package/pages/page-{n:02d}.jpg').convert('RGB');items.append((n,'top',im.crop((0,0,1200,205))))
 if n in [54,65]:items.append((n,'lower heading',im.crop((0,430,1200,550))))
records=[]
for k in range(0,len(items),8):
 chunk=items[k:k+8];out=Image.new('RGB',(1200,sum(im.height+22 for _,_,im in chunk)), 'white');draw=ImageDraw.Draw(out);y=0
 for n,label,im in chunk:draw.text((5,y+3),f'FINAL PAGE {n} / {label}',fill='black');out.paste(im,(0,y+22));y+=im.height+22
 file=O/f'headings-{k//8+1:02d}.png';out.save(file);records.append({'path':str(file.relative_to(R)),'pages':[(n,label) for n,label,_ in chunk],'sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
(P/'heading-review-sheets.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'heading sheets; all main-step pages, including lower panel badges.')

from pathlib import Path
import json,io,math,shutil,sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent;O=B/'cycle2/package';O.mkdir(exist_ok=True)
assert shutil.disk_usage(R).free>=576*1024**2
for name,font in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+font))
W,H=landscape(A4);BG='#f7f4ee';INK='#27333b';ACC='#bd5037'
only='--specimen' in sys.argv
c=canvas.Canvas(str(O/('specimen.pdf' if only else 'focused-pages.pdf')),pagesize=(W,H))
def txt(s,x,y,size=11,bold=False):c.setFillColor(HexColor(INK));c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,s)
def arrow(a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l
 # Leave both physical features visible. Arrow follows their common projection.
 a=(a[0]+ux*8,a[1]+uy*8);b=(b[0]-ux*7,b[1]-uy*7)
 c.setStrokeColor(HexColor(ACC));c.setFillColor(HexColor(ACC));c.setLineWidth(2);c.line(*a,*b)
 p=c.beginPath();p.moveTo(*b);p.lineTo(b[0]-ux*9-uy*3.5,b[1]-uy*9+ux*3.5);p.lineTo(b[0]-ux*9+uy*3.5,b[1]-uy*9-ux*3.5);p.close();c.drawPath(p,fill=1,stroke=0)
def photo(folder,name,x,y,w,h):
 loc=json.loads((B/'cycle2'/folder/'receiver-locations.json').read_text())[name]
 c.drawImage(str(B/'cycle2'/folder/(name+'.png')),x,y,w,h)
 def pt(t):return x+w*t['x'],y+h*(1-t['y'])
 return loc,pt
pages=[]
for n,pg in [(5,10),(6,12),(7,14),(8,16)]:
 if only and n!=5:continue
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 txt('DSS TAIPEI CURRENT',32,H-27,10,True);txt(f'{n}  Attach the completed suspension unit',32,H-64,21,True)
 loc,pt=photo('representative-fit' if n==5 else 'remaining','s'+str(n)+'-placement',125,65,588,420)
 for k in [0,2]:arrow(pt(loc['targets'][k]),pt(loc['targets'][k+1]))
 c.setStrokeColor(HexColor('#d9d1c7'));c.line(32,42,W-32,42)
 txt('348 pieces | Design by CL Kao | Powered by spacedock.md',32,27,8);txt(str(pg),W-42,27,8)
 c.showPage();pages.append(pg)
if not only:
 # Preserve the original recipe/tray on page36; replace only its placement panel and callout.
 loc,pt=photo('bed-overhead','bed-placement',395,100,420,300)
 c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.3)
 for poly in [p for p in loc['polygons'] if p['id']==81]:
  points=[pt(q) for q in poly['points']];path=c.beginPath();path.moveTo(*points[0])
  for q in points[1:]:path.lineTo(*q)
  path.close();c.drawPath(path,stroke=1,fill=0)
 target=pt(loc['targets'][4]);c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.3);c.line(380,242,target[0],target[1]);c.circle(*target,3,stroke=1,fill=0)
 for k in [3]:arrow(pt(loc['targets'][k]),pt(loc['targets'][k+1]))
 c.showPage();pages.append(36)
c.save()
if not only:
 old=PdfReader(B/'cycle1/package/instructions.pdf');focused=PdfReader(O/'focused-pages.pdf');writer=PdfWriter()
 for n,p in enumerate(old.pages,1):
  if n in pages and n!=36:p=focused.pages[pages.index(n)]
  elif n==36:
   buf=io.BytesIO();wipe=canvas.Canvas(buf,pagesize=(W,H));wipe.setFillColor(HexColor(BG));wipe.rect(378,44,W-400,400,fill=1,stroke=0);wipe.save();buf.seek(0);p.merge_page(PdfReader(buf).pages[0]);p.merge_page(focused.pages[-1])
  writer.add_page(p)
 with (O/'instructions.pdf').open('wb') as f:writer.write(f)
 mapping=json.loads((B/'cycle1/package/pdf-page-map.json').read_text());mapping['correction_round']=2;mapping['affected_pages']=pages;
 for row in mapping['page_records']:
  if row['page'] in pages:row.update(unchanged_content=False,correction_round=2)
 (O/'pdf-page-map.json').write_text(json.dumps(mapping,indent=2)+'\n')
 assert shutil.disk_usage(R).free>=512*1024**2
print(pages)

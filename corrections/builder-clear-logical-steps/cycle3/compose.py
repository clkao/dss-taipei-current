from pathlib import Path
from collections import Counter
import json,io,math,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent;O=B/'cycle3/package';assert shutil.disk_usage(R).free>=576*1024**2
m=json.loads((O/'model.json').read_text());plan=json.loads((O/'instruction-plan.json').read_text());assert m['instruction_plan']==plan
parts={p['id']:p for p in m['pieces']};base=B/'access-corrected-hybrid-prefix';icons=json.loads((base/'part-icons.json').read_text())
for name,font in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+font))
W,H=landscape(A4);BG='#f7f4ee';INK='#27333b';ACC='#bd5037';c=canvas.Canvas(str(O/'focused-pages.pdf'),pagesize=(W,H));pages=[]
def txt(s,x,y,size=11,bold=False,color=INK):c.setFillColor(HexColor(color));c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,s)
def begin(title,page):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0);txt('DSS TAIPEI CURRENT',32,H-27,10,True,ACC);txt(title,32,H-65,21,True)
 c.setStrokeColor(HexColor('#d9d1c7'));c.line(32,42,W-32,42);txt('348 pieces | Design by CL Kao | Powered by spacedock.md',32,27,8);txt(str(page),W-42,27,8)
def tray(ids,x=36,y=465):
 for k,((part,color),q) in enumerate(Counter((parts[i]['part'],parts[i]['color']) for i in ids).items()):
  c.drawImage(str(base/icons[part+'|'+color]),x,y-k*48,42,32,preserveAspectRatio=True);txt(f'{q} x {part}',x+46,y+10-k*48,10,True)
def badge(s,x,y):
 c.setFillColor(HexColor('#ffffff'));c.setStrokeColor(HexColor(ACC));c.circle(x,y,10,fill=1,stroke=1);txt(s,x-4,y-4,12,True,ACC)
def arrow(a,b):
 dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l;a=(a[0]+ux*5,a[1]+uy*5);b=(b[0]-ux*4,b[1]-uy*4)
 c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(3.4);c.line(*a,*b);c.setStrokeColor(HexColor('#20272b'));c.setFillColor(HexColor('#20272b'));c.setLineWidth(1.8);c.line(*a,*b);p=c.beginPath();p.moveTo(*b);p.lineTo(b[0]-ux*8-uy*3,b[1]-uy*8+ux*3);p.lineTo(b[0]-ux*8+uy*3,b[1]-uy*8-ux*3);p.close();c.drawPath(p,fill=1,stroke=0)
def photo(folder,name,x,y,w,h):
 loc=json.loads((B/'cycle3'/folder/'receiver-locations.json').read_text())[name];c.drawImage(str(B/'cycle3'/folder/(name+'.png')),x,y,w,h);return loc,lambda t:(x+w*t['x'],y+h*(1-t['y']))
def pairarrows(loc,pt,count):
 for k in range(0,count*2,2):arrow(pt(loc['targets'][k]),pt(loc['targets'][k+1]))
begin('1  Build the chassis core',4);tray([172,178,216,231],y=450)
loc,pt=photo('finalviews','core-pins',175,280,588,210);pairarrows(loc,pt,2);badge('1',180,455);badge('2',180,340)
loc,pt=photo('finalviews','core-close',175,65,588,210);pairarrows(loc,pt,2);badge('3',180,230)
c.showPage();pages.append(4)
begin('13  Install both floor plates',23);tray([99,129]);loc,pt=photo('core-floor','floor-plates',150,65,630,450);pairarrows(loc,pt,2);txt('Studs up. Support the chassis underneath.',36,62,10);c.showPage();pages.append(23)
for n,pg in [(14,24),(15,25)]:
 s=plan['steps'][n-1];begin(f'{n}  Four spacers — two layers',pg);tray(s['new_ids']);txt('4 stacks / 2 plates each',200,475,12,True)
 for k,x in [(1,32),(2,435)]:
  txt(f'{k}  '+('Upper layer first' if k==1 else 'Lower layer next'),x,441,13,True)
  loc,pt=photo('finalviews',f'spacer{n}-layer{k}',x,160,375,268);pairarrows(loc,pt,4);a=pt(loc['targets'][-1]);badge('C',a[0]+9,a[1]+13)
 # Exact earlier locator includes installed bands and canonical whole-chassis context.
 x,y,w,h=36,48,175,125;name=f'plate{n}-locator';c.drawImage(str(B/'cycle1/renders'/(name+'.png')),x,y,w,h)
 xy=lambda t:(x+w*t['x'],y+h*(1-t['y']))
 face=json.loads((P.parent/'cycle1/locator-faces.json').read_text())[name];points=[xy(q) for q in face['points']];path=c.beginPath();path.moveTo(*points[0])
 for q in points[1:]:path.lineTo(*q)
 path.close();c.saveState();c.setStrokeColor(HexColor('#1379b5'));c.setFillColor(HexColor('#1379b5'));c.setFillAlpha(.15);c.drawPath(path,stroke=1,fill=1);c.restoreState()
 t=json.loads((B/'cycle1/renders/receiver-locations.json').read_text())[name]['targets'][0];a=xy(t);badge('C',a[0]+20,a[1]+20);c.setStrokeColor(HexColor(ACC));c.line(a[0]+14,a[1]+12,*a)
 txt(('Rear' if n==14 else 'Front')+' floor plate · C marks the same front corner.',230,126,11,True)
 txt('Chassis omitted in closeups; keep it assembled.',230,99,10)
 txt('Install the upper layer first. Insertion access remains unverified.',230,77,10)
 c.showPage();pages.append(pg)
# p36 overlay replaces the right placement panel only.
loc,pt=photo('bed-specimen','bed-trial1',395,100,420,300)
c.setStrokeColor(HexColor(ACC));c.setLineWidth(1)
for poly in loc['polygons']:
 points=[pt(q) for q in poly['points']];p=c.beginPath();p.moveTo(*points[0])
 for q in points[1:]:p.lineTo(*q)
 p.close();c.drawPath(p,stroke=1,fill=0)
for k in [1,3]:arrow(pt(loc['targets'][k]),pt(loc['targets'][k+1]))
a=pt(loc['targets'][4]);c.setStrokeColor(HexColor(ACC));c.setLineWidth(1);c.line(380,242,*a);c.circle(*a,2,fill=0,stroke=1)
c.showPage();pages.append(36);c.save()
old=PdfReader(B/'cycle2/package/instructions.pdf');focused=PdfReader(O/'focused-pages.pdf');writer=PdfWriter()
for n,p in enumerate(old.pages,1):
 if n in pages and n!=36:p=focused.pages[pages.index(n)]
 elif n==36:
  buf=io.BytesIO();wipe=canvas.Canvas(buf,pagesize=(W,H));wipe.setFillColor(HexColor(BG));wipe.rect(378,44,W-400,400,fill=1,stroke=0);wipe.save();buf.seek(0);p.merge_page(PdfReader(buf).pages[0]);p.merge_page(focused.pages[-1])
 writer.add_page(p)
with (O/'instructions.pdf').open('wb') as f:writer.write(f)
mapping=json.loads((B/'cycle2/package/pdf-page-map.json').read_text());mapping.update(correction_round=3,affected_pages=pages,edition_plan_sha256=__import__('hashlib').sha256((O/'instruction-plan.json').read_bytes()).hexdigest())
for row in mapping['page_records']:
 if row['page'] in pages:row.update(unchanged_content=False,correction_round=3)
(O/'pdf-page-map.json').write_text(json.dumps(mapping,indent=2)+'\n');assert shutil.disk_usage(R).free>=512*1024**2;print(pages)

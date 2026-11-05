"""Compose focused A4 pages and reuse exact predecessor pages, preserving source plan."""
from pathlib import Path
import json,hashlib,io,copy,shutil
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[2];B=R/'builds/clear-logical';O=B/'candidate';O.mkdir(exist_ok=True)
assert shutil.disk_usage(R).free>512*1024**2
old=B/'simplification-package-retry1';base=B/'access-corrected-hybrid-prefix'
m=json.loads((old/'model.json').read_text());steps=m['instruction_plan']['steps'];parts={p['id']:p for p in m['pieces']};icons=json.loads((base/'part-icons.json').read_text())
for name,font in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+font))
W,H=landscape(A4);BG='#f7f4ee';INK='#27333b';ACC='#bd5037';maps=[];pagejobs={};current=None
c=canvas.Canvas(str(O/'focused-pages.pdf'),pagesize=(W,H));c.setTitle('DSS focused construction views')
def txt(t,x,y,size=11,bold=False,color=INK):c.setFillColor(HexColor(color));c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,t)
def image(p,x,y,w,h):
 from PIL import Image
 im=Image.open(p).convert('RGB');im.thumbnail((1400,1000));buf=io.BytesIO();im.save(buf,format='JPEG',quality=90)
 c.drawImage(ImageReader(buf),x,y,w,h,preserveAspectRatio=True,anchor='c')
def begin(title,n,op=None):
 global current
 current={'title':title,'steps':[n],'operations':op or steps[n-1]['operations'],'new_ids':[]}
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0)
 txt('DSS TAIPEI CURRENT',32,H-27,10,True,ACC);txt(title,32,H-65,21,True)
 c.setStrokeColor(HexColor('#d9d1c7'));c.line(32,42,W-32,42)
 txt('348 pieces | Design by CL Kao | Powered by spacedock.md',32,27,8);txt('Our contributions: CC BY-SA 4.0',W-210,27,8)
def finish():
 maps.append(current);c.showPage();return len(maps)-1
def tray(ids,y=H-105,caption=None):
 current['new_ids']=list(ids);counts=list(Counter((parts[i]['part'],parts[i]['color']) for i in ids).items());cols=min(6,len(counts)) or 1;cell=(W-72)/cols
 for j,((part,color),q) in enumerate(counts):
  x=36+(j%cols)*cell;yy=y-(j//cols)*50
  image(base/icons[part+'|'+color],x,yy-35,42,34);txt(f'{q} x {part}',x+46,yy-20,10,True)
 if caption:txt(caption,36,y-55,10)
def photo(folder,name,x,y,w,h,marks=True):
 image(B/folder/(name+'.png'),x,y,w,h)
 if marks:
  loc=json.loads((B/folder/'receiver-locations.json').read_text())[name]['targets'];scale=min(w/1400,h/1000);ix=x+(w-1400*scale)/2;iy=y+(h-1000*scale)/2
  for t in loc:
   px=ix+t['x']*1400*scale;py=iy+(1-t['y'])*1000*scale
   c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.3);c.circle(px,py,5,stroke=1,fill=0)
   txt(t['label'],px+8,py+7,10,True,ACC)
def standard(n,title=None):
 s=steps[n-1];begin(title or f'{n}  '+s['manual']['title'],n);tray(s['new_ids']);image(base/s['manual']['image'],70,65,W-140,360)
 if n==63:txt('White print on clear film.',36,65,10)
 return finish()
pagejobs[8]=[standard(4)]
for n,pg in [(5,9),(6,10),(7,11),(8,12)]:
 s=steps[n-1];begin(f'{n}  '+s['manual']['title'],n,s['operations'][:-1]);tray(s['new_ids'])
 for j,f in enumerate(s['manual']['frames']):
  image(base/f['image'],36+j*255,125,245,270);txt(str(j+1),42+j*255,405,14,True,ACC)
 txt('Complete this unit before attaching it to the frame.',36,90,11);recipe=finish()
 begin(f'{n}  Attach the completed suspension unit',n,[s['operations'][-1]])
 photo('detail-final',f's{n}-before',35,100,370,355);photo('detail-final',f's{n}-after',435,100,370,355)
 txt('Receiving frame',36,465,12,True);txt('Completed unit in place',435,465,12,True)
 photo('detail-final',f's{n}-unit',620,65,170,100)
 txt('Completed unit',620,58,9)
 txt('Match A and B on the unit to A and B on the frame.',36,72,10);pagejobs[pg]=[recipe,finish()]
for n,pg,other in [(14,19,13),(15,20,16)]:
 s=steps[n-1];begin(f'{n}  Four floor spacers - two plates per stack',n);tray(s['new_ids'])
 photo('detail-final',f's{n}-stack',36,210,175,195,False);txt('4x',65,410,18,True,ACC);txt('2 x 6141 per stack',36,188,11,True)
 photo('detail-final',f's{n}-before',225,115,280,300);photo('detail-final',f's{n}-after',530,115,280,300)
 txt('1  Find four locations',225,430,12,True);txt('2  Fit all four stacks',530,430,12,True)
 image(base/s['manual']['image'],36,55,145,120)
 txt('Underside detail: surrounding chassis is omitted from these two views; it remains assembled.',225,92,9)
 txt('Build each stack bottom plate first, then top plate. No extra parts.',225,73,10)
 target=finish();pagejobs[pg]=[standard(other),target] if n==14 else [target,standard(other)]
pagejobs[33]=[standard(25),standard(26,'26  Right side panels - use all six listed parts')]
pagejobs[41]=[standard(40)]
for k,title in [(1,'Dashboard and two grilles'),(2,'Steering stand and wheel'),(3,'Seat')]:
 s=steps[40];ids=s['placements'][k-1]['ids'];begin('41'+chr(96+k)+'  '+title,41,[s['operations'][k-1]]);tray(ids)
 photo('cabin-detail',f'cabin-{k}-before',35,120,370,335);photo('cabin-detail',f'cabin-{k}-after',435,120,370,335)
 txt('Receiving cabin',36,435,12,True);txt('After this action',435,435,12,True)
 if k==2:
  photo('assets','steering-detail',335,48,150,95,False);txt('Wheel angle',490,88,10)
  txt('Cutaway: surrounding body stays assembled.',36,65,9)
 else:txt('Cutaway: surrounding body is omitted; it stays assembled.',36,80,10)
 image(base/s['manual']['image'],675,52,135,100)
 pagejobs[41].append(finish())
pagejobs[58]=[standard(63)]
begin('64  Thread the four rings in order',64);txt('Craft cord: about 0.6 mm diameter. Cut length and slack are not specified.',36,H-105,11)
photo('assets','cord-top',36,130,520,340)
photo('assets','cord-front',560,275,245,195);photo('assets','cord-front-other',560,75,245,195)
txt('1 > 2 > 3 > 4',36,118,16,True,ACC);txt('Route outside the front bumper; leave slack and keep clear of the wheels.',36,91,10)
txt('Tie end knots after threading at 1 and 4. Knot type is not specified.',36,71,10)
pagejobs[58].append(finish())
begin('67  Place the completed figures',67)
photo('assets-v2','helm-before',36,170,370,300,False);photo('feet','helm-feet',435,170,235,300,False)
photo('assets','helm-after',680,205,125,180,False)
txt('Helm platform before placement',36,478,12,True);txt('Foot placement detail',435,478,12,True)
txt('Upper body omitted in detail; use the complete figure.',435,158,9)
txt('Use the completed candidate from 65. Place the other figure beside the vehicle.',36,130,11)
txt('The overhead view exposes the platform; it does not prescribe removing the enclosure.',36,105,10)
txt('Exact stud engagement and insertion clearance remain unverified.',36,80,10)
pagejobs[60]=[finish()]
c.save()
focused=PdfReader(O/'focused-pages.pdf');oldpdf=PdfReader(old/'instructions.pdf');writer=PdfWriter();mapping=[]
for i,page in enumerate(oldpdf.pages,1):
 if i in pagejobs:
  for index in pagejobs[i]:writer.add_page(focused.pages[index]);mapping.append(dict(source_page=i,focused_page=index+1,**maps[index]))
 else:
  writer.add_page(page);mapping.append({'source_page':i,'unchanged_content':True})
# Carriers retain source diagrams and receive an explicit shared-recipe reference.
for index,(page,rec) in enumerate(zip(writer.pages,mapping),1):
 buf=io.BytesIO();over=canvas.Canvas(buf,pagesize=(W,H));over.setFillColor(HexColor(BG));over.rect(W-56,19,30,17,fill=1,stroke=0);over.setFillColor(HexColor(INK));over.setFont('Body',8);over.drawRightString(W-32,27,str(index))
 if rec['source_page'] in [24,26]:
  over.setFillColor(HexColor(BG));over.rect(36,44,W-72,20,fill=1,stroke=0);over.setFillColor(HexColor(ACC));over.setFont('Bold',10);over.drawString(36,50,'Panels .10-.12 are the completed C rail recipe shown earlier. Use C17 / C18 here; no new parts.')
 over.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0]);rec['page']=index
writer.add_metadata({'/Title':'DSS Taipei Current - clear logical construction candidate','/Author':'CL Kao'})
with (O/'instructions.pdf').open('wb') as f:writer.write(f)
(O/'pdf-page-map.json').write_text(json.dumps({'pages':len(mapping),'page_records':mapping},indent=2)+'\n')
print('Composed',len(mapping),'pages')

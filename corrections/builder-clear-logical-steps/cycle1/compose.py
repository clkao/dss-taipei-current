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
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';O=B/'cycle1/package';assert shutil.disk_usage(R).free>=576*1024**2;assert not (O/'release.zip').exists();O.mkdir(exist_ok=True)
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
def photo(name,x,y,w,h,marks=True,polygons=True):
    folder=B/'cycle1'/('renders-feet-top' if name.startswith('feet-') else 'renders');image(folder/(name+'.png'),x,y,w,h)
    loc=json.loads((folder/'receiver-locations.json').read_text())[name];scale=min(w/1400,h/1000);ix=x+(w-1400*scale)/2;iy=y+(h-1000*scale)/2
    def xy(v):return ix+v['x']*1400*scale,iy+(1-v['y'])*1000*scale
    c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.3)
    if name.endswith('-locator'):
      face=json.loads((Path(__file__).parent/'locator-faces.json').read_text())[name];points=[xy(v) for v in face['points']]
      path=c.beginPath();path.moveTo(*points[0])
      for v in points[1:]:path.lineTo(*v)
      path.close();c.saveState();c.setStrokeColor(HexColor('#1379b5'));c.setFillColor(HexColor('#1379b5'));c.setFillAlpha(.15);c.setLineWidth(2);c.drawPath(path,stroke=1,fill=1);c.restoreState()
    if polygons:
      for poly in loc.get('polygons',[]):
       points=[xy(v) for v in poly['points']];path=c.beginPath();path.moveTo(*points[0])
       for v in points[1:]:path.lineTo(*v)
       path.close();c.setDash(3,2);c.drawPath(path);c.setDash()
    if marks:
      for t in loc['targets']:
       px,py=xy(t);lx=ix+t['label_at'][0]*1400*scale;ly=iy+(1-t['label_at'][1])*1000*scale
       c.circle(px,py,2.2,stroke=1,fill=0);c.line(lx,ly-8,px,py);c.setFillColor(HexColor('#ffffff'));c.circle(lx,ly+4,10,stroke=1,fill=1);txt(t['label'],lx-4,ly,14,True,ACC)

for n,pg in [(5,10),(6,12),(7,14),(8,16)]:
 s=steps[n-1];begin(f'{n}  Attach the completed suspension unit',n,[s['operations'][-1]])
 txt('Frame: outside face',36,465,12,True);txt('Unit: inside face',435,465,12,True)
 photo(f's{n}-receiver',36,170,365,280);photo(f's{n}-unit',435,170,365,280)
 txt('A and B: beam holes',36,155,10);txt('A and B: exposed pin ends',435,155,10)
 txt('Turn the completed unit to see its inside face.',36,120,11)
 txt('Match A to A and B to B. The lower view shows the result.',36,96,11)
 image(base/s['manual']['image'],640,48,160,115)
 pagejobs[pg]=finish()
for n,pg,plate_title in [(14,24,'Rear floor plate'),(15,25,'Front floor plate')]:
 s=steps[n-1];begin(f'{n}  Four floor spacers - two plates per stack',n);tray(s['new_ids'])
 image(B/'detail-final'/f's{n}-stack.png',36,240,145,140);txt('4x / 2 plates each',36,410,13,True,ACC)
 photo(f'plate{n}-receiver',210,160,285,285);photo(f'plate{n}-complete',520,160,285,285)
 txt('Receiving plate underside',210,440,12,True);txt('Four completed stacks',520,440,12,True)
 photo(f'plate{n}-locator',36,48,210,160);txt(plate_title,260,137,12,True)
 txt('Blue highlight: installed plate. C: the same front corner.',260,111,10)
 txt('Chassis omitted in underside details only. Keep it assembled.',260,86,10)
 pagejobs[pg]=finish()
begin('64  Thread the four rings in order',64)
# Every leader terminates on a catalog-defined visible aperture face.
for order,x,y in [(1,32,300),(2,595,300),(4,32,80),(3,595,80)]:
 photo(f'ring-{order}',x,y,215,210)
 txt('Ring '+str(order),x,y+205,11,True)
image(B/'assets/cord-top.png',255,150,330,310)

for box in json.loads((Path(__file__).parent/'ring-locator.json').read_text())['boxes']:
 left,top,right,bottom=box['bounds'];sc=330/1400;ix=255;iy=150+(310-1000*sc)/2
 x=ix+left*1400*sc;y=iy+(1-bottom)*1000*sc
 c.setStrokeColor(HexColor(ACC));c.setLineWidth(1);c.rect(x,y,(right-left)*1400*sc,(bottom-top)*1000*sc,stroke=1,fill=0)
 c.setFillColor(HexColor('#ffffff'));c.circle(x-6,y+10,8,stroke=1,fill=1);txt(box['label'],x-9,y+6,11,True,ACC)

txt('1 > 2 > 3 > 4',280,122,17,True,ACC)
txt('Cord stays outside the bumper. Leave slack and keep clear of wheels.',36,66,9)
txt('Tie ends after threading at 1 and 4. Knot type and cut length remain unspecified.',36,51,9)
pagejobs[69]=finish()
begin('67  Place the completed figures',67)
txt('Platform before placement',36,465,12,True);txt('Foot positions / same view',435,465,12,True)
photo('feet-receiver',36,165,365,290);photo('feet-detail',435,165,365,290)
txt('L / R show the two sole footprints. Match the helm wheel landmark.',36,143,10)
txt('Detail omits the enclosure and upper body. Keep both assembled.',36,118,10)
txt('Use the completed figure from 65. Stud engagement and access remain unverified.',36,93,10)
txt('Place the other figure beside the vehicle.',36,68,10)
image(B/'assets/helm-after.png',690,48,110,100)
pagejobs[71]=finish()
c.save()
focused=PdfReader(O/'focused-pages.pdf');rejected=PdfReader(B/'candidate/instructions.pdf');writer=PdfWriter()
oldmap=json.loads((B/'candidate/pdf-page-map.json').read_text());mapping=[]
for n,page in enumerate(rejected.pages,1):
 rec=copy.deepcopy(oldmap['page_records'][n-1])
 if n in pagejobs:
  index=pagejobs[n];new=focused.pages[index];buf=io.BytesIO();over=canvas.Canvas(buf,pagesize=(W,H));over.setFillColor(HexColor(INK));over.setFont('Body',8);over.drawRightString(W-32,27,str(n));over.save();buf.seek(0);new.merge_page(PdfReader(buf).pages[0]);writer.add_page(new)
  rec['correction_round']=1;rec['correction_focused_page']=index+1
 else:writer.add_page(page)
 mapping.append(rec)
with (O/'instructions.pdf').open('wb') as f:writer.write(f)
(O/'pdf-page-map.json').write_text(json.dumps({'pages':len(mapping),'page_records':mapping},indent=2)+'\n')
print('Revised affected pages:',sorted(pagejobs))

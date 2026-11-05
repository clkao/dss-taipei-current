from pathlib import Path
from collections import Counter
import json,math,io,sys
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
from headings import badge
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical';O=B/'cycle5/package';m=json.loads((O/'model.json').read_text());plan=m['instruction_plan'];ps={p['id']:p for p in m['pieces']};base=B/'access-corrected-hybrid-prefix';icons=json.loads((base/'part-icons.json').read_text());W,H=841.8897637795277,595.2755905511812
for n,f in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
ACC='#bd5037';BG='#f7f4ee';c=canvas.Canvas(str(B/'cycle5/side-pages.pdf'),pagesize=(W,H));pages=[]
def text(s,x,y,size=12,bold=False):c.setFillColor(HexColor('#27333b'));c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,s)
def start(title,page,number=17):
 c.setFillColor(HexColor(BG));c.rect(0,0,W,H,fill=1,stroke=0);text('DSS TAIPEI CURRENT',32,569,9,True);text('04 / BODY SIDES AND WHEEL ARCHES',32,550,9);badge(c,number,title,32,514);c.setStrokeColor(HexColor('#d9d1c7'));c.line(32,42,W-32,42);text('348 pieces | Design by CL Kao | Powered by spacedock.md',32,27,8);text(str(page),W-42,27,8)
def tray(ids,x,y,w):
 items=list(Counter((ps[i]['part'],ps[i]['color']) for i in ids).items());cell=w/len(items)
 for k,((part,col),count) in enumerate(items):c.drawImage(str(base/icons[part+'|'+col]),x+cell*k,y-30,38,30,preserveAspectRatio=True);text(f'{count} x {part}',x+cell*k+42,y-18,10,True)
def pic(path,x,y,w,h):c.drawImage(str(path),x,y,w,h,preserveAspectRatio=True,anchor='c')
def finish(n):c.showPage();pages.append(n)
def masked(name,folder,x,y,w,h):
 loc=json.loads((B/'cycle5'/folder/'receiver-locations.json').read_text())[name];pt=lambda t:(x+w*t['x'],y+h*(1-t['y']))
 for axis in loc['segments']:
  a,b=[pt(loc['targets'][axis[k]]) for k in ['from_target','to_target']];dx,dy=b[0]-a[0],b[1]-a[1];L=math.hypot(dx,dy);ux,uy=dx/L,dy/L
  for r in axis['runs']:
   lo=max(r['from'],4/L);hi=min(r['to'],1-3/L)
   if hi<=lo:continue
   c.saveState()
   if r['hidden']:c.setDash([3,2],lo*L%5)
   a1=(a[0]+dx*lo,a[1]+dy*lo);b1=(a[0]+dx*hi,a[1]+dy*hi);c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(3.2);c.line(*a1,*b1);c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.6);c.line(*a1,*b1);c.restoreState()
  end=(b[0]-3*ux,b[1]-3*uy);p=c.beginPath();p.moveTo(*end);p.lineTo(end[0]-7*ux-3*uy,end[1]-7*uy+3*ux);p.lineTo(end[0]-7*ux+3*uy,end[1]-7*uy-3*ux);p.close();c.setFillColor(HexColor(ACC));c.drawPath(p,fill=1,stroke=0)
 return loc,pt
if '--draft' not in sys.argv:
 for name,n,frames,total in [('lower carrier',27,[1,2,3,4],[97,96,115,117,140,197,98,116]),('long rail',28,[5,6,7],[38,39,41,42]),('short rail',29,[10,11,12],[331,46,48])]:
  start('Build the '+name+' · 2x',n);text('Parts for one copy',36,478,10,True);tray(total,180,488,620)
  if len(frames)==4:
   for k,f in enumerate(frames):
    x=36+(k%2)*392;y=65+(1-k//2)*190;text(str(k+1),x,y+175,12,True);pic(base/plan['steps'][16]['manual']['frames'][f-1]['image'],x+18,y,360,174)
  else:
   for k,f in enumerate(frames):
    x=36+k*258;text(str(k+1),x,430,12,True);pic(base/plan['steps'][16]['manual']['frames'][f-1]['image'],x,150,250,270)
   text('Fit every bracket while the rail is loose.',36,88,12)
  text('Use one copy on each side.',36,58,10);finish(n)
start('Join the rails',30)

for n,x,label in [(17,30,'Left side'),(18,426,'Right side')]:
 text(label,x+10,443,14,True);name=f'side{n}-variant';y=125;w=386;h=w/1.4;pic(B/'cycle5/variants-inside'/(name+'.png'),x,y,w,h)
 if (B/'cycle5/variant-masks/receiver-locations.json').exists():loc,pt=masked(name,'variant-masks',x,y,w,h)
 else:
  loc=json.loads((B/'cycle5/variants-inside/receiver-locations.json').read_text())[name];pt=lambda t:(x+w*t['x'],y+h*(1-t['y']))
 for target in loc['targets'][4:]:
  px,py=pt(target);tx=px-20;ty=413;text('Long · 1 x 6' if target['id'] in [38,81] else 'Short · 1 x 4',tx,ty,10,True);c.setStrokeColor(HexColor(ACC));c.setFillColor(HexColor(BG));c.circle(tx-13,ty+3,8,fill=1,stroke=1);text('1' if target['id'] in [38,81] else '2',tx-16,ty,10,True);c.setStrokeColor(HexColor(ACC));c.setLineWidth(.8);c.line(tx+20,ty-5,px,py);c.circle(px,py,2,fill=0,stroke=1)
text('Keep both lower carriers in the orientation shown.',36,82,11)
finish(30)
if '--draft' not in sys.argv:
 for n,pg in [(17,31),(18,32)]:
  start('Install the '+('left' if n==17 else 'right')+' side carrier',pg,n);text('1 completed side carrier · no new loose parts',36,478,12)
  name=f'side{n}-placement'
  from PIL import Image,ImageChops
  imagepath=B/'cycle5/placements'/(name+'.png');im=Image.open(imagepath).convert('RGB');bb=ImageChops.difference(im,Image.new('RGB',im.size,im.getpixel((0,0)))).getbbox();l,t,r,b=bb;l=max(0,l-25);t=max(0,t-25);r=min(im.width,r+25);b=min(im.height,b+25)
  x,y,w,h=60,55,720,400;scale=min(w/(r-l),h/(b-t));ix=x+(w-(r-l)*scale)/2-l*scale;iy=y+(h-(b-t)*scale)/2-(im.height-b)*scale
  c.saveState();clip=c.beginPath();clip.rect(x,y,w,h);c.clipPath(clip,stroke=0);c.drawImage(str(imagepath),ix,iy,im.width*scale,im.height*scale);masked(name,'placement-masks',ix,iy,im.width*scale,im.height*scale);c.restoreState();finish(pg)
c.save()
if '--draft' not in sys.argv:
 source=PdfReader(O/'instructions.pdf');new=PdfReader(B/'cycle5/side-pages.pdf');out=PdfWriter()
 for n,page in enumerate(source.pages,1):
  if n==33:continue
  if n in pages:page=new.pages[pages.index(n)]
  elif n>33:
   buf=io.BytesIO();cc=canvas.Canvas(buf,pagesize=(W,H));cc.setFillColor(HexColor(BG));cc.rect(W-58,20,30,20,fill=1,stroke=0);cc.setFillColor(HexColor('#27333b'));cc.setFont('Body',8);cc.drawRightString(W-32,27,str(n-1));cc.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0])
  out.add_page(page)
 with (B/'cycle5/content.pdf').open('wb') as f:out.write(f)
print(pages)

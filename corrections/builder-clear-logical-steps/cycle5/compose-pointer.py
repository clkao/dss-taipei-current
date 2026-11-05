from pathlib import Path
from collections import Counter
import json,io,math,shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';P=Path(__file__).parent;O=B/'cycle5/package';assert shutil.disk_usage(R).free>=576*1024**2
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
def arrow(a,b,head=True):
 dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy);ux,uy=dx/l,dy/l;a=(a[0]+ux*5,a[1]+uy*5);b=(b[0]-ux*4,b[1]-uy*4)
 c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(3.4);c.line(*a,*b);c.setStrokeColor(HexColor(ACC));c.setFillColor(HexColor(ACC));c.setLineWidth(1.8);c.line(*a,*b);p=c.beginPath();p.moveTo(*b);p.lineTo(b[0]-ux*8-uy*3,b[1]-uy*8+ux*3);p.lineTo(b[0]-ux*8+uy*3,b[1]-uy*8-ux*3);p.close();
 if head:c.drawPath(p,fill=1,stroke=0)
def photo(folder,name,x,y,w,h):
 loc=json.loads((B/'cycle4'/folder/'receiver-locations.json').read_text())[name];c.drawImage(str(B/'cycle4'/folder/(name+'.png')),x,y,w,h);return loc,lambda t:(x+w*t['x'],y+h*(1-t['y']))
hidden={}
for folder in ['hidden-specimen','hidden-remaining']:
 hidden.update(json.loads((B/'cycle4'/folder/'receiver-locations.json').read_text()))
def masked_arrows(name,pt):
 data=hidden[name]
 for axis in data['segments']:
  a,b=[pt(data['targets'][axis[k]]) for k in ['from_target','to_target']];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);ux,uy=dx/length,dy/length
  for run in axis['runs']:
   lo=max(run['from'],5/length);hi=min(run['to'],1-4/length)
   if hi<=lo:continue
   aa=(a[0]+dx*lo,a[1]+dy*lo);bb=(a[0]+dx*hi,a[1]+dy*hi)
   c.saveState()
   if run['hidden']:c.setDash([3,2],(lo*length)%5)
   c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(3.4);c.line(*aa,*bb);c.setStrokeColor(HexColor(ACC));c.setLineWidth(1.8);c.line(*aa,*bb);c.restoreState()
  # Receiver arrowhead stays solid; endpoint is the same source-bound feature.
  end=(b[0]-ux*4,b[1]-uy*4);c.setFillColor(HexColor(ACC));p=c.beginPath();p.moveTo(*end);p.lineTo(end[0]-ux*8-uy*3,end[1]-uy*8+ux*3);p.lineTo(end[0]-ux*8+uy*3,end[1]-uy*8-ux*3);p.close();c.drawPath(p,fill=1,stroke=0)
# Fit the entire visible diagram, including every body/rail end, with padding.
from PIL import Image,ImageChops
ip=B/'cycle4/selected-bed/bed-selected-B.png';im=Image.open(ip).convert('RGB');bb=ImageChops.difference(im,Image.new('RGB',im.size,im.getpixel((0,0)))).getbbox();left,top,right,bottom=bb;left=max(0,left-25);top=max(0,top-25);right=min(im.width,right+25);bottom=min(im.height,bottom+25)
x,y,w,h=395,55,420,405;scale=min(w/(right-left),h/(bottom-top));ix=x+(w-(right-left)*scale)/2-left*scale;iy=y+(h-(bottom-top)*scale)/2-(im.height-bottom)*scale
c.saveState();clip=c.beginPath();clip.rect(x,y,w,h);c.clipPath(clip,stroke=0);c.drawImage(str(ip),ix,iy,im.width*scale,im.height*scale);c.restoreState()
loc=json.loads((B/'cycle4/selected-bed/receiver-locations.json').read_text())['bed-selected-B'];pt=lambda t:(ix+t['x']*im.width*scale,iy+(1-t['y'])*im.height*scale)
(P/'bed-layout.json').write_text(json.dumps({'source_image':'selected-bed/bed-selected-B.png','all_visible_geometry_bbox':list(bb),'padded_display_window':[left,top,right,bottom],'no_visible_geometry_omitted':True},indent=2)+'\n')
c.setStrokeColor(HexColor(ACC));c.setLineWidth(1)
for poly in [min(loc['polygons'],key=lambda q:sum(t['x'] for t in q['points'])/len(q['points']))]:
 points=[pt(q) for q in poly['points']];p=c.beginPath();p.moveTo(*points[0])
 for q in points[1:]:p.lineTo(*q)
 p.close();c.drawPath(p,stroke=1,fill=0)
masked_arrows('bed-selected-B',pt)
# Recipe leader identifies the new crossbar. Recover this fixed orthographic
# projection from its camera basis and already-captured source-bound points.
import numpy as np
D=np.array([-2,2,1.1],dtype=float);D/=np.linalg.norm(D);rightv=np.cross([0,1,0],D);rightv/=np.linalg.norm(rightv);upv=np.cross(D,rightv)
world=np.array([t['world'] for t in loc['targets']]);xy=np.array([[t['x'],t['y']] for t in loc['targets']]);coefx=np.linalg.lstsq(np.column_stack((world@rightv,np.ones(len(world)))),xy[:,0],rcond=None)[0];coefy=np.linalg.lstsq(np.column_stack((world@upv,np.ones(len(world)))),xy[:,1],rcond=None)[0]
assert max(abs(np.column_stack((world@rightv,np.ones(len(world))))@coefx-xy[:,0]))<1e-8
assert max(abs(np.column_stack((world@upv,np.ones(len(world))))@coefy-xy[:,1]))<1e-8
origin=parts[33]['transform']['origin'];newworld=np.array([origin[0],origin[2],-origin[1]])+np.array([-2.5,13,0]);newtarget={'id':33,'world':newworld.tolist(),'x':float(np.dot([newworld@rightv,1],coefx)),'y':float(np.dot([newworld@upv,1],coefy))};a=pt(newtarget)
(P/'recipe-pointer.json').write_text(json.dumps({'target':newtarget,'meaning':'New floating rear-bed crossbar, not assembled receiver','fixed_camera_projection_residual_max':float(max(abs(np.column_stack((world@rightv,np.ones(len(world))))@coefx-xy[:,0]))),'removed_outline':'rightmost projected receiving polygon'},indent=2)+'\n')
c.setStrokeColor(HexColor(ACC));c.setLineWidth(1);c.line(380,242,*a);c.circle(*a,2,fill=0,stroke=1)
c.showPage();pages.append(36);c.save()
old=PdfReader(B/'cycle4/package/instructions.pdf');focused=PdfReader(O/'focused-pages.pdf');writer=PdfWriter()
for n,p in enumerate(old.pages,1):
 if n in pages and n!=36:p=focused.pages[pages.index(n)]
 elif n==36:
  buf=io.BytesIO();wipe=canvas.Canvas(buf,pagesize=(W,H));wipe.setFillColor(HexColor(BG));wipe.rect(378,44,W-400,400,fill=1,stroke=0);wipe.save();buf.seek(0);p.merge_page(PdfReader(buf).pages[0]);p.merge_page(focused.pages[-1])
 writer.add_page(p)
with (O/'instructions.pdf').open('wb') as f:writer.write(f)
mapping=json.loads((B/'cycle4/package/pdf-page-map.json').read_text());mapping.update(correction_round='captain-follow-up',affected_pages=pages)
for row in mapping['page_records']:
 if row['page'] in pages:row.update(unchanged_content=False,correction_round='captain-follow-up')
(O/'pdf-page-map.json').write_text(json.dumps(mapping,indent=2)+'\n');assert shutil.disk_usage(R).free>=512*1024**2;print(pages)

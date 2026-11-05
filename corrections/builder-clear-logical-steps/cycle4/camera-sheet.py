from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical/cycle4';O=B/'camera-study-retry';loc=json.loads((O/'receiver-locations.json').read_text());c=canvas.Canvas(str(B/'camera-comparison.pdf'),pagesize=(900,710))
c.setFont('Helvetica-Bold',18);c.drawString(20,683,'Page36 — four bounded camera candidates, same display separation')
for k,name in enumerate(['A','B','C','D']):
 x=20+(k%2)*445;y=355-(k//2)*330;w,h=420,300;c.drawImage(str(O/f'bed-{name}.png'),x,y,w,h);c.setFont('Helvetica-Bold',13);c.setFillColor(HexColor('#27333b'));c.drawString(x,y+307,name)
 t=loc['bed-'+name]['targets'];pt=lambda q:(x+w*q['x'],y+h*(1-q['y']))
 for a,b in [(1,2),(3,4)]:
  p,q=pt(t[a]),pt(t[b]);dx,dy=q[0]-p[0],q[1]-p[1];z=math.hypot(dx,dy);u,v=dx/z,dy/z;p=(p[0]+u*4,p[1]+v*4);q=(q[0]-u*3,q[1]-v*3)
  c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(3);c.line(*p,*q);c.setStrokeColor(HexColor('#bd5037'));c.setLineWidth(1.7);c.line(*p,*q);path=c.beginPath();path.moveTo(*q);path.lineTo(q[0]-u*7-v*3,q[1]-v*7+u*3);path.lineTo(q[0]-u*7+v*3,q[1]-v*7-u*3);path.close();c.setFillColor(HexColor('#bd5037'));c.drawPath(path,fill=1,stroke=0)
c.save()

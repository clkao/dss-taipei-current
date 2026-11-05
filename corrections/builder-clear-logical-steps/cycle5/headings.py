"""Restore retained coral number badges without changing scene or tray coordinates."""
from pathlib import Path
import io,json,re,hashlib
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader,PdfWriter
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;O=R/'builds/clear-logical/cycle5/package';W,H=841.8897637795277,595.2755905511812
for n,f in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/System/Library/Fonts/Supplemental/'+f))
CORAL=HexColor('#d86c55');BG=HexColor('#f7f4ee');INK=HexColor('#27333b')
paired={7,17,34,37,38,41,42,43,45,46,47,52,53,54,56,61,63,65}
special={55:[47,48],66:[60,61],67:[62],70:[65,66]}
known={5:1,6:1,18:10,19:11,20:12,21:12,22:12,35:20,36:20,44:33,57:51,58:51,59:52,60:52,62:55,64:57}
plan=json.loads((O/'instruction-plan.json').read_text());titles={s['number']:s['manual']['title'] for s in plan['steps']}
def rows_of(page):
 rows=[]
 def f(t,cm,tm,font,size):
  x=tm[4]*cm[0]+tm[5]*cm[2]+cm[4];y=tm[4]*cm[1]+tm[5]*cm[3]+cm[5]
  if t.strip():rows.append(dict(text=t.strip(),x=x,y=y,size=size))
 page.extract_text(visitor_text=f);return rows
def badge(c,num,title,x,y,width=770,large=True):
 size=21 if large else 12;bw=44 if large else 30;bh=34 if large else 30
 c.setFillColor(CORAL);c.roundRect(x-3,y-10,bw,bh,7,stroke=0,fill=1);c.setFillColor(white);c.setFont('Bold',size);c.drawCentredString(x-3+bw/2,y,str(num))
 if title:
  style=ParagraphStyle('heading',fontName='Bold',fontSize=size,leading=size+3,textColor=INK)
  pp=Paragraph(title,style);ww,hh=pp.wrap(width-bw-12,80);pp.drawOn(c,x+bw+8,y+size-hh)
def apply(src,dest):
 reader=PdfReader(src);writer=PdfWriter();record=[]
 for docn,page in enumerate(reader.pages,1):
  n=docn if docn<33 else docn+1
  if n<4 or n>71 or 27<=n<=33:writer.add_page(page);continue
  rows=rows_of(page);top=next((r for r in rows if r['size']>=20 and r['y']>500),None);buf=io.BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));changes=[]
  if n in paired:
   c.setFillColor(BG);c.rect(29,509,W-58,34,stroke=0,fill=1)
   for row in rows:
    match=re.match(r'^(\d{1,2})\s+(.+)',row['text'])
    if row['size']!=12 or not match or not 450<row['y']<490:continue
    num=int(match[1]);x=row['x'];y=row['y'];width=377 if x<400 else 380
    c.setFillColor(BG);c.rect(x-5,y-17,width+5,40,stroke=0,fill=1);badge(c,num,match[2],x,y,width,False);changes.append(dict(number=num,title=match[2],rect=[x-5,y-17,width+5,40]))
   # Any wrapped continuation belongs to the same previous paragraph and stays below it only if not already covered.
  elif n in special:
   for num in special[n]:
    row=next(r for r in rows if r['size']==12 and re.match(r'^'+str(num)+r'(?:\s|$)',r['text']));x,y=row['x'],row['y'];suffix=row['text'][len(str(num)):].strip();width=90 if n in [55,66,67] else 200
    c.setFillColor(BG);c.rect(x-5,y-12,width,36,stroke=0,fill=1);badge(c,num,suffix,x,y,width,False);changes.append(dict(number=num,title=suffix,rect=[x-5,y-12,width,36]))
  elif top:
   match=re.match(r'^(\d{1,2})([abc]?)\s*(.*)',top['text']);num=int(match[1]) if match else known[n];title=(match[3] if match and match[3] else top['text'] if not match else titles[num]);x,y=32,top['y']
   c.setFillColor(BG);c.rect(29,y-9,W-58,36,stroke=0,fill=1)
   for sub in rows:
    if 'one-copy parts' in sub['text'] and 495<sub['y']<510:
     c.setFillColor(BG);c.rect(30,sub['y']-5,500,16,stroke=0,fill=1);c.setFillColor(INK);c.setFont('Body',10);c.drawString(36,493,'Parts for one copy');changes.append(dict(subtitle_moved=True,rect=[30,sub['y']-5,500,16],new_rect=[36,489,125,15]))
   badge(c,num,title,x,y);changes.append(dict(number=num,title=title,rect=[29,y-9,W-58,36]))
   # Component installation caption must not repeat the main number.
   for row in rows:
    if n!=36 and row['size']==12 and re.match('^'+str(num)+r'\s*/',row['text']) and row['y']<450:
     c.setFillColor(BG);c.rect(row['x']-2,row['y']-4,100,21,stroke=0,fill=1);c.setFillColor(INK);c.setFont('Bold',12);c.drawString(row['x'],row['y'],'Install '+row['text'].split('/',1)[1].strip());changes.append(dict(remove_duplicate=row['text'],rect=[row['x']-2,row['y']-4,100,21]))
  c.save();buf.seek(0);page.merge_page(PdfReader(buf).pages[0]);writer.add_page(page);record.append(dict(page=docn,source_page=n,changes=changes))
 with open(dest,'wb') as f:writer.write(f)
 (P/'heading-changes.json').write_text(json.dumps({'baseline':'sources/legacy-recipes/make_full_instruction_pdf.py:start','baseline_sha256':hashlib.sha256((R/'sources/legacy-recipes/make_full_instruction_pdf.py').read_bytes()).hexdigest(),'coral':'#d86c55','treatment':'rounded coral number badge with white bold number; component/local numbering subordinate','pages':record},indent=2)+'\n')
if __name__=='__main__':
 import sys
 apply(Path(sys.argv[1]),Path(sys.argv[2]))

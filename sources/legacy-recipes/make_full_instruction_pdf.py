"""Illustrate the shared full-build plan; never make a parallel step sequence."""
import argparse,hashlib,html,json,math,shutil
from collections import Counter
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--dir',type=Path,default=ROOT/'output/yangliu-full-instructions-draft-v1')
ap.add_argument('--pdf',type=Path,default=ROOT/'output/pdf/yangliu-full-instructions-draft-v1.pdf')
ap.add_argument('--site-url',default='https://clkao.github.io/dss-taipei-current/')
args=ap.parse_args();D=args.dir;OUT=args.pdf;OUT.parent.mkdir(exist_ok=True)
credits_url=args.site_url.rstrip('/')+'/credits.html'
m=json.loads((D/'model.json').read_text());plan=m['instruction_plan'];parts={p['id']:p for p in m['pieces']}
COUNT=len(parts);STEPS=len(plan['steps']);LOTS=len(Counter((p['part'],p['color']) for p in parts.values()))
EDITION=m['instruction_edition'];AUDITED=bool(m.get('physical_audit'))
icons=json.loads((D/'part-icons.json').read_text())
pdfmetrics.registerFont(TTFont('Body','/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Bold','/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
W,HH=landscape(A4);INK=HexColor('#27333b');MUTED=HexColor('#637178');CORAL=HexColor('#d86c55');BG=HexColor('#f7f4ee');LINE=HexColor('#d9d1c7')
DISCLAIMER='An independent fan design for use with genuine LEGO® bricks. Not affiliated with, sponsored by, or endorsed by the LEGO Group.'
c=canvas.Canvas(str(OUT),pagesize=(W,HH));c.setTitle('DSS Taipei Current / 洋流號 - '+EDITION);c.setAuthor('CL Kao');c.setSubject('Illustrated test-build instructions. Design by CL Kao. Powered by spacedock.md.')
page=0;page_records=[];jpeg_cache={}
def para(text,x,y,width,size=11,color=INK,font='Body',leading=None):
    font='STSong-Light' if any(ord(ch)>0x3000 for ch in text) else font
    p=Paragraph(html.escape(text).replace('\n','<br/>'),ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.35,textColor=color))
    _,height=p.wrap(width,2000);p.drawOn(c,x,y-height);return y-height
def label(text,x,y,size=10,color=MUTED,bold=False):
    c.setFillColor(color);c.setFont('STSong-Light'if any(ord(ch)>0x3000 for ch in text)else'Bold'if bold else'Body',size);c.drawString(x,y,text)
def start(section,title,number=None):
    global page
    page+=1;c.setFillColor(BG);c.rect(0,0,W,HH,fill=1,stroke=0)
    label('DSS TAIPEI CURRENT  /  '+EDITION.upper(),32,HH-26,9,CORAL,True)
    label(section.upper(),32,HH-45,9)
    if number is not None:
        c.setFillColor(CORAL);c.roundRect(30,HH-99,45,43,8,fill=1,stroke=0)
        c.setFillColor(white);c.setFont('Bold',21);c.drawCentredString(52.5,HH-84,str(number));x=88
    else:x=32
    para(title,x,HH-60,W-x-36,21,font='Bold',leading=25)
    c.setStrokeColor(LINE);c.line(32,42,W-32,42)
    label(f'{COUNT} pieces  |  Design by CL Kao  |  Powered by spacedock.md',32,27,8)
    c.linkURL('https://spacedock.md/',(224,20,410,36),relative=0,thickness=0)
    label('Our contributions: CC BY-SA 4.0',W-210,27,8)
    c.linkURL(credits_url+'#license',(W-214,20,W-62,36),relative=0,thickness=0)
    c.setFont('Body',8);c.drawRightString(W-32,27,str(page))
def finish(kind,**meta):
    page_records.append(dict(page=page,kind=kind,**meta));c.showPage()
def picture(path,x,y,w,h,stretch=False):
    path=Path(path)
    if path.suffix=='.png' and not stretch:
        # Reuse compact JPEG encodings in the PDF, preserving the source PNGs.
        if path not in jpeg_cache:
            from io import BytesIO
            im=Image.open(path).convert('RGB');im.thumbnail((960,680));buf=BytesIO();im.save(buf,format='JPEG',quality=78,subsampling=2,optimize=True)
            jpeg_cache[path]=ImageReader(BytesIO(buf.getvalue()))
        image=jpeg_cache[path]
    else:image=ImageReader(str(path))
    c.drawImage(image,x,y,w,h,preserveAspectRatio=not stretch,anchor='c',mask='auto')
def part_box(ids,x=32,y=None,width=160):
    y=HH-124 if y is None else y
    counts=Counter((parts[i]['part'],parts[i]['color']) for i in ids)
    label('PARTS IN THIS STEP',x,y,9,INK,True);y-=14
    row=min(58,(y-112)/max(1,len(counts)))
    for (part,color),quantity in counts.items():
        picture(D/icons[part+'|'+color],x,y-row+3,65,row-6)
        label(str(quantity)+' x '+part,x+69,y-18,10,INK,True)
        para(m['colors'][color][2],x+69,y-27,width-69,9)
        y-=row
    return y

start('Minifigure edition','洋流號 / DSS Taipei Current')
picture(D/'front.png',235,100,560,365)
label('FULL BUILD',36,HH-143,30,INK,True)
label(f'{STEPS} numbered steps',36,HH-179,17,INK)
label(f'{COUNT} catalog pieces',36,HH-205,17,INK)
para(f'{COUNT} rigid pieces\n2 suspension bands + craft cord\nCustom stickers supplied separately',36,HH-238,190,11)
para('TEST-BUILD EDITION' if AUDITED else 'DRAFT FOR FIT REVIEW',36,154,190,12,CORAL,'Bold')
para('Complete illustrated sequence. Digital connection review is separate from physical fit, grip and suspension testing.',36,131,190,10)
para(DISCLAIMER,36,78,W-72,8.5,MUTED)
label('Full credits on the website',36,58,9,CORAL)
c.linkURL(credits_url,(32,50,230,72),relative=0,thickness=0)
finish('cover')

start('Before building','Read the pictures, then dry-fit')
guide_cards=[
 ('01  NEW PARTS',D/plan['steps'][1]['manual']['image'],'Blue outline = new.'),
 ('02  CALLOUTS',D/next(s['manual']['frames'][0]['image'] for s in plan['steps'] if s['manual'].get('frames')),'2× = two copies.'),
 ('03  DRY-FIT',D/next(s['manual']['image'] for s in plan['steps'] if 265 in s['new_ids']),'Check fit; do not force.')]
for index,(title,file,note) in enumerate(guide_cards):
    x=36+index*259
    picture(file,x,210,247,230)
    label(title,x,186,12,INK,True)
    para(note,x,169,235,11)
para('Print stickers at 100%; check the 20 mm ruler. Bands and cord are outside the rigid count. The cabin driver is omitted.',36,103,W-72,10)
para('Test-build edition: full insertion replay, physical grip, suspension travel and handling strength remain unverified.',36,77,W-72,10,CORAL)
finish('reading-guide')

start('Build map','Chapters and parts')
chapters=[]
for s in plan['steps']:
    if not chapters or chapters[-1]['title']!=s['section']:chapters.append(dict(title=s['section'],first=s['number'],last=s['number']))
    chapters[-1]['last']=s['number']
for index,chapter in enumerate(chapters):
    columns=5 if len(chapters)>12 else 4;cell=(W-72)/columns
    col=index%columns;row=index//columns;x=36+col*cell;y=HH-120-row*141
    sample=plan['steps'][chapter['last']-1]['manual']['image']
    picture(D/sample,x,y-94,cell-14,92)
    para(chapter['title'],x,y-97,cell-12,9,font='Bold')
    label(f"{chapter['first']} - {chapter['last']}",x,y-128,9)
finish('contents')

step_page={}
for s in plan['steps']:
    n=s['number'];a=s['manual'];new=s['new_ids']
    frames=a.get('frames',[])
    if a.get('repeat_prefix_from'):frames=frames[a['repeat_prefix_frames']:]
    if frames:
        # Local recipe pictures are those compiled by recipe_frames, not a
        # second PDF-only interpretation of the construction operations.
        for offset in range(0,len(frames),4):
            group=frames[offset:offset+4]
            start(s['section'],a['title'],n)
            if s['repeat_count']>1:label(f"{s['repeat_count']}×",36,HH-115,18,CORAL,True)
            elif a.get('repeat_prefix_from'):label(f"← {a['repeat_prefix_from']}",36,HH-115,14,CORAL,True)
            elif a.get('repeat_prefix_count'):label(f"{a['repeat_prefix_count']}×"if offset==0 else'1×',36,HH-115,18,CORAL,True)
            for k,frame in enumerate(group):
                x=36+(k%2)*389;y=HH-146-(k//2)*192
                letter=chr(96+frame['number']);label(f"{n}{letter}. {frame['title']}",x,y,11,INK,True)
                picture(D/frame['image'],x,y-157,230,145)
                if frame.get('preassembled'):
                    picture(D/frame['image'],x+236,y-90,72,80)
                    label('1×',x+315,y-30,11,INK,True)
                    label('Preassembled',x+292,y-51,9)
                    continue
                counts=Counter((parts[i]['part'],parts[i]['color']) for i in frame['ids'])
                for j,((p,co),q)in enumerate(counts.items()):
                    yy=y-18-j*43
                    picture(D/icons[p+'|'+co],x+236,yy-37,53,36)
                    label(f'{q} x {p}',x+292,yy-10,9,INK,True)
                    para(m['colors'][co][2],x+292,yy-20,86,8)
            finish('local-recipe',step=n)
    if a.get('approach_frames'):
        start(s['section'],'Slide inward → lower',n)
        for k,frame in enumerate(a['approach_frames']):
            x=36+k*390
            picture(D/frame['image'],x,145,376,300)
            para('1 plate above'if k==0 else'Slide in ↓',x,128,370,12,font='Bold')
        para('Rails go on afterward.',36,75,W-72,11)
        finish('installation-approach',step=n)
    step_page[str(n)]=page+1
    start(s['section'],a['title'],n)
    if a.get('turn_model'):label('↻ '+a['turn_model'],W-160,HH-102,12,CORAL,True)
    if a.get('repeat_from'):
        label(f"1×  ← {a['repeat_from']}",36,HH-115,14,CORAL,True)
    instance_frames=a.get('instance_frames')or a.get('frames')or[]
    if a.get('preassembled'):
        picture(D/a['image'],32,HH-282,162,129)
        label('1× preassembled',36,HH-300,12,INK,True)
    elif instance_frames:
        picture(D/instance_frames[-1]['image'],32,HH-282,162,129)
        label(str(s.get('copies',1))+'×',36,HH-300,18,INK,True)
    else:part_box(new,y=HH-137)
    picture(D/a['image'],208,105,W-240,HH-230)
    note=''
    if a.get('bands_installation'):note='2× x37 · one loop per side.'
    elif a.get('art')=='hood':note='Two films. Upper film spans all three level tiles.'
    elif a.get('art')=='banner':note='洋 above · 流 below · both faces.'
    elif a.get('art')=='sail':note='White print on clear film.'
    elif a.get('art')=='cord':note='Thread four rings; tie loosely. Keep clear of wheels.'
    elif a.get('preassembled'):note='Preassembled.'
    elif a.get('approach_frames'):note='Slide inward one plate high, then lower.'
    elif a.get('repeat_from'):note='Use the remaining copy.'
    if note:para(note,210,83,W-246,11)
    finish('build-step',step=n)

start('Print at actual size','Campaign sticker placement guide')
continuous_hood=any(s['name']=='hood-upper' for s in m.get('hood_sticker_sections',[]))
para('For printing, use the separate vector print-and-cut sheets. This page is a fitting guide. '+('The upper hood film spans three level tiles. Keep clips, studs and the step down to the curved hood clear.' if continuous_hood else 'Use one sticker per part; keep clips, studs and seams clear.'),36,HH-121,W-75,11)
mm=72/25.4
art=H/Path(m['hood_artwork']).parent;v6=H/Path(m['surface_artworks']['wedge-tile']).parent;front=H/'sources/artwork-75875'
# Crop to the exact UV region actually projected on the hood shell.
uv=m['hood_uv_bounds'];v=[v for s in m['decal_surfaces'] for v in s['uv']]
umin,umax=min(a[0] for a in v),max(a[0] for a in v);vmin,vmax=min(a[1] for a in v),max(a[1] for a in v)
hood=Image.open(art/'hood.png');cw,ch=hood.size
hood_crop=hood.crop((int(umin*cw),int((1-vmax)*ch),int(umax*cw),int((1-vmin)*ch)))
temp=D/'hood-sticker-cut.png';hood_crop.save(temp)
items=[('Hood - white strip / clear sides',temp,26.4,19.88),('Upper banner / face 1',H/m['surface_artworks']['banner-upper'],14.4,14.4),('Upper banner / face 2',H/m['surface_artworks']['banner-upper'],14.4,14.4),('Lower banner / face 1',H/m['surface_artworks']['banner-lower'],14.4,14.4),('Lower banner / face 2',H/m['surface_artworks']['banner-lower'],14.4,14.4),('Wedge flag - white / clear',v6/'wedge-tile.png',14.4,14.4)]
if m.get('hood_sticker_sections'):
    sections={s['name']:s for s in m['hood_sticker_sections']}
    hood_items=[]
    section_titles=([('H1 / whole upper character','hood-upper'),('H2 / curved hood + white strip','hood-front')] if continuous_hood else [('H1 / white tile','hood-white-tile'),('H2 / curved hood + white strip','hood-front'),('H3 / left overflow','hood-left-overflow'),('H4 / right overflow','hood-right-overflow')])
    for title,name in section_titles:
        s=sections[name];file=art/s['png']
        if name=='hood-upper':
            x,y,w,h=s['crop_viewbox'];file=D/'hood-upper-sticker-guide.png'
            hood.crop((round(x*cw/64),round(y*ch/48),round((x+w)*cw/64),round((y+h)*ch/48))).save(file)
        hood_items.append((title,file,s['width_mm'],s['height_mm']))
    items=hood_items+items[1:]
if m.get('banner_sticker_sections'):
    banner_items=[]
    for index,s in enumerate(m['banner_sticker_sections'],1):
        for face in range(1,s['copies']+1):
            banner_items.append((f'Banner {index} / face {face}',H/m['surface_artworks'][s['name']],s['width_mm'],s['height_mm']))
    items=[i for i in items if not i[0].startswith(('Upper banner','Lower banner'))]
    items[-1:-1]=banner_items
if not m.get('front_revision'):items += [('Left headlamp',front/'headlamp-left.png',14.56,15.04),('Right headlamp',front/'headlamp-right.png',14.56,15.04),('Plain grille',front/'grille.png',31.36,15.36)]
for index,(title,file,w,h) in enumerate(items):
    col=index%3;row=index//3;x=42+col*259;y=HH-179-row*111
    label(title,x,y,10,INK,True);picture(file,x,y-65,w*mm,h*mm,stretch=True)
    label(f'{w:.2f} x {h:.2f} mm',x+105,y-31,9)
c.setStrokeColor(INK);c.setLineWidth(.7);c.line(43,67,43+20*mm,67);c.line(43,63,43,71);c.line(43+20*mm,63,43+20*mm,71);label('20 mm',43+24*mm,64,9)
if continuous_hood:para('Hood: apply H1 as one clear film across the white centre tile and both level orange side tiles. Do not cut at their internal seams. H2 keeps the straight white strip on the curved hood; keep it separate from H1 at the height change. Square flags: printed Reddish Orange backgrounds on White parts, both faces. Wedge: white emblem on clear film.',36,HH-500,W-75,9)
elif m.get('hood_sticker_sections'):para('Hood: H1 goes on the white tile; H3/H4 go on the level orange side tiles. H2 keeps the straight white strip under the lower character. Align on paper first, then apply separate sections without bridging the raised tile seam. Wedge: white emblem on clear film.',36,HH-500,W-75,9)
elif m.get('hood_artwork_transparent'):para('Hood: use clear film with white ink, or place a cut white strip under a clear lettering decal. The lettering extends beyond the strip; leave those side areas transparent. Wedge flag: white emblem on clear film, with no printed background.',36,HH-425,W-75,10)
finish('sticker-sheet')

if 'bubble-rest' in m.get('surface_artworks',{}):
    start('Print at actual size','One banner / two speech-bubble faces')
    tsai=next(s for s in plan['steps']if s['module']=='tsai')
    picture(D/tsai['manual']['image'],40,120,430,330)
    for name,caption,x in [('bubble-rest','Face 1',510),('bubble-listen','Face 2',660)]:
        picture(H/m['surface_artworks'][name],x,330,15.36*mm,15.36*mm,stretch=True)
        label(caption,x,310,10,INK,True)
    shirt=Image.open(H/m['surface_artworks']['jacket']).convert('RGBA').resize((1480,1160))
    warped=Image.new('RGBA',shirt.size)
    for y in range(1160):
        width=round(1136+(1480-1136)*y/1159)
        warped.alpha_composite(shirt.crop((0,y,1480,y+1)).resize((width,1)),((1480-width)//2,y))
    jacket_print=D/'jacket-print.png';warped.save(jacket_print)
    picture(jacket_print,510,210,14.8*mm,11.6*mm,stretch=True)
    para('Jacket / clear film\n14.8 mm lower edge × 11.6 mm high',565,239,215,9)
    para('Print at 100%. Both banner faces are 15.36 × 15.36 mm. Apply to opposite sides of one White 2335 flag. Keep both clips clear.',510,295,265,10)
    c.setStrokeColor(INK);c.line(510,170,510+20*mm,170)
    c.line(510,166,510,174);c.line(510+20*mm,166,510+20*mm,174)
    label('20 mm scale check',510,150,10)
    para('Custom graphics by CL Kao. The figure is a likeness approximation; real hand/bar grip remains untested.',36,78,W-72,10)
    finish('speech-bubble-print-sheet')

lots=Counter((p['part'],p['color']) for p in parts.values());entries=sorted(lots.items())
for offset in range(0,len(entries),20):
    start('Rigid inventory',f'Parts list {offset//20+1} / {math.ceil(len(entries)/20)}')
    for index,((part,color),quantity) in enumerate(entries[offset:offset+20]):
        col=index%4;row=index//4;x=33+col*196;y=HH-125-row*79
        picture(D/icons[part+'|'+color],x,y-54,77,55)
        label(f'{quantity} x {part}',x+80,y-16,10,INK,True)
        para(m['colors'][color][2],x+80,y-25,110,9)
    finish('inventory')

start('Checks and remaining work','Checks and remaining physical tests')
checks=[
 ('DIGITAL COVERAGE',D/'front.png',f'{COUNT} rigid parts, introduced once. MPD poses and inventory match.'),
 ('MAST + PLATFORM',D/next(s['manual']['image']for s in plan['steps']if 265 in s['new_ids']),'Dry-fit clips and mount. Support the chassis; do not lift by equipment.'),
 ('SUSPENSION',D/next(s['manual']['image'] for s in plan['steps'] if s['manual'].get('bands_installation')),'Fit both bands. Check wheel clearance and suspension travel.'),
 ('CORD + STICKERS',D/next(s['manual']['image']for s in plan['steps']if s['manual'].get('art')=='cord'),'Check threading, knot slack and paper fit before final application.')]
for index,(title,file,note) in enumerate(checks):
    x=36+(index%2)*390;y=HH-126-(index//2)*202
    picture(file,x,y-133,220,130)
    para(title,x+228,y-12,145,11,font='Bold')
    para(note,x+228,y-51,145,10)
para('Targeted digital fit checks only. Full continuous assembly replay, physical grip, stiffness and handling strength remain unverified.',36,70,W-72,10,CORAL)
label('Full credits on the website →',36,98,11,CORAL,True)
c.linkURL(credits_url,(32,88,W-32,115),relative=0,thickness=0)
finish('validation')
c.save()
shutil.copyfile(OUT,D/'instructions.pdf')
(D/'pdf-page-map.json').write_text(json.dumps(dict(pages=page,steps=step_page,page_records=page_records,pdf_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest()),indent=2)+'\n')
print(json.dumps(dict(pdf=str(OUT),pages=page,steps=len(plan['steps']),bytes=OUT.stat().st_size),indent=2))

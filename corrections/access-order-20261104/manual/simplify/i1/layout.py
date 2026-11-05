# Executed inside the retained PDF template's namespace; no source mutation.
from collections import Counter

def compact_tray(ids,x,y,width):
    counts=list(Counter((parts[i]['part'],parts[i]['color']) for i in ids).items())
    columns=3 if width<350 else 4
    cell=width/columns
    for j,((part,color),quantity) in enumerate(counts):
        xx=x+(j%columns)*cell; yy=y-(j//columns)*38
        picture(D/icons[part+'|'+color],xx,yy-29,36,29)
        label(str(quantity)+' x '+part,xx+38,yy-17,8,INK,True)

def frame_card(s,f,x,y,w,h,tag=None):
    label(tag or str(s['number'])+'.'+str(f['number']),x,y-12,12,CORAL,True)
    if f.get('preassembled'):label('1x preassembled',x+62,y-12,9,INK,True)
    elif f.get('child'):label('1x / '+str(len(f['ids']))+' pieces',x+62,y-12,9,INK,True)
    elif f.get('kind')=='receiver-context':label('Receiving points',x+62,y-12,9,INK)
    picture(D/f['image'],x,y-h+48,w,h-70)
    if not f.get('preassembled') and not f.get('child') and f.get('kind')!='receiver-context':compact_tray(f['ids'],x,y-h+40,w)

def main_card(s,x,y,w,h):
    a=s['manual'];para(str(s['number'])+'  '+a['title'],x,y,w,12,font='Bold',leading=15)
    picture(D/a['image'],x,y-h+100,w,h-150)
    if a.get('repeat_from'):label('1x from '+str(a['repeat_from']),x,y-h+80,11,CORAL,True)
    elif a.get('preassembled'):label('1x preassembled',x,y-h+80,11,INK,True)
    else:compact_tray(s['new_ids'],x,y-h+85,w)
    notes={'hood':'Two films; keep the height change clear.','banner':'洋 above / 流 below / both faces.','sail':'White print on clear film.','cord':'Thread four rings; tie loosely. Keep clear of wheels.'}
    note=notes.get(a.get('art'),'')
    if a.get('bands_installation'):note='2x x37 / one loop per side'
    if note:para(note,x,65,w,10)

step_page={}
for item in composition_pages:
    ss=[plan['steps'][n-1] for n in item['steps']];s=ss[0];a=s['manual'];kind=item['kind']
    for n in item['steps']:step_page.setdefault(str(n),page+1)
    start(s['section'],item.get('title',' / '.join(str(n) for n in item['steps'])))
    if kind=='prefix':
        compact_tray([172,216,231,178],36,HH-120,180)
        picture(D/'ordered-prefix.png',200,80,W-232,HH-185)
    elif kind=='main':
        width=(W-86)/len(ss)
        for j,st in enumerate(ss):main_card(st,36+j*(width+14),HH-113,width,HH-170)
    elif kind=='frames':
        ff=[a['frames'][i-1] for i in item['frames']];cols=2;rows=(len(ff)+1)//2
        width=(W-90)/2;height=(HH-165)/rows
        for j,f in enumerate(ff):frame_card(s,f,36+(j%2)*(width+18),HH-113-(j//2)*height,width,height)
        if item.get('copies'):label('2x / quantities for one copy',W-235,HH-91,10,CORAL,True)
    elif kind=='rail2':
        # Geometry is repeated; source order is not. Preserve both first-bracket views.
        pairs=[(ss[0],10,'17 / 18: base'),(ss[0],11,'17: first bracket'),(ss[1],11,'18: first bracket'),(ss[0],12,'2x: completed rail')]
        width=(W-90)/2;height=(HH-165)/2
        for j,(st,i,tag) in enumerate(pairs):frame_card(st,st['manual']['frames'][i-1],36+(j%2)*(width+18),HH-113-(j//2)*height,width,height,tag)
        label('2x / quantities for one copy',W-235,HH-91,10,CORAL,True)
    elif kind=='callout':
        ff=[a['frames'][i-1] for i in item.get('frames',range(1,len(a['frames'])+1))]
        width=330;cols=2 if len(ff)>2 else 1;rows=(len(ff)+cols-1)//cols
        height=(HH-175)/rows
        c.setStrokeColor(LINE);c.roundRect(28,52,350,HH-160,8,stroke=1,fill=0)
        label(str(s.get('copies',1))+'x / one-copy quantities',36,HH-107,10,CORAL,True)
        for j,f in enumerate(ff):frame_card(s,f,36+(j%cols)*165,HH-124-(j//cols)*height,width/cols-8,height)
        label(str(s['number'])+' / installation',402,HH-120,12,INK,True)
        picture(D/a['image'],397,96,W-430,HH-240)
        # Link the assembly callout to its destination without inventing a motion path.
        c.setStrokeColor(CORAL);c.setLineWidth(1.2);c.line(380,HH/2,394,HH/2)
        label(str(s.get('copies',1))+'x',402,78,13,CORAL,True)
    elif kind=='approach':
        for j,f in enumerate(a['approach_frames']):
            picture(D/f['image'],36+j*390,110,375,HH-240)
            label('1 plate above' if j==0 else 'Slide inward, then lower',36+j*390,88,11,INK,True)
    else:raise ValueError(kind)
    finish('simplification-i1',composition=item,source_operations={str(st['number']):st['operations'] for st in ss})

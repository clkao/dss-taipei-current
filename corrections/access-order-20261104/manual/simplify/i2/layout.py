# Executed inside the retained PDF template's namespace; no source mutation.
from collections import Counter

tray_measurements=[]
locations=json.loads((D/'receiver-assets/receiver-locations.json').read_text())

def compact_tray(ids,x,y,width):
    counts=list(Counter((parts[i]['part'],parts[i]['color']) for i in ids).items())
    if not counts:return 0
    # Reserve the actual complete identifier, not a fixed number of columns.
    cell=max(94,max(40+pdfmetrics.stringWidth(str(q)+' x '+part,'Bold',9)+10 for (part,color),q in counts))
    columns=max(1,int(width//cell));cell=width/columns
    tray_measurements.append({'width':width,'columns':columns,'cell_width':cell,'labels':[{"text":str(q)+' x '+part,"printed_width":pdfmetrics.stringWidth(str(q)+' x '+part,'Bold',9)} for (part,color),q in counts]})
    for j,((part,color),quantity) in enumerate(counts):
        xx=x+(j%columns)*cell;yy=y-(j//columns)*43
        picture(D/icons[part+'|'+color],xx,yy-32,36,29)
        label(str(quantity)+' x '+part,xx+40,yy-20,9,INK,True)
    return math.ceil(len(counts)/columns)*43

def marked_picture(name,state,x,y,w,h):
    info=locations[name];targets=info['targets'];file=D/'receiver-assets'/str(name+'-'+state+'.png')
    # Larger source-bound detail plus small unmarked whole-assembly locator.
    xx=[t['x'] for t in targets];yy=[t['y'] for t in targets]
    cw=min(.88,max(.28,max(xx)-min(xx)+.28));ch=min(.88,max(.42,max(yy)-min(yy)+.38))
    cx=(min(xx)+max(xx))/2;cy=(min(yy)+max(yy))/2
    left=max(0,min(1-cw,cx-cw/2));top=max(0,min(1-ch,cy-ch/2))
    dw=w*.72;dh=h;scale=min(dw/(1600*cw),dh/(1000*ch));iw=1600*scale;ih=1000*scale
    ox=x+(dw-1600*cw*scale)/2-left*iw;oy=y+(dh-1000*ch*scale)/2-(1-top-ch)*ih
    c.saveState();path=c.beginPath();path.rect(x,y,dw,dh);c.clipPath(path,stroke=0,fill=0)
    picture(file,ox,oy,iw,ih)
    for t in targets:
        tx=ox+t['x']*iw;ty=oy+(1-t['y'])*ih
        c.setStrokeColor(CORAL);c.setLineWidth(1.6);c.circle(tx,ty,8,stroke=1,fill=0)
        label(t['label'],tx+9,ty+7,10,CORAL,True)
    c.restoreState()
    picture(file,x+w*.74,y+h*.52,w*.26,h*.4)
    label('Location',x+w*.74,y+h*.49,8,MUTED)
    mw=w*.26;mh=h*.4;ms=min(mw/1600,mh/1000);mx=x+w*.74+(mw-1600*ms)/2;my=y+h*.52+(mh-1000*ms)/2
    c.setStrokeColor(CORAL);c.setLineWidth(.7);c.rect(mx+left*1600*ms,my+(1-top-ch)*1000*ms,cw*1600*ms,ch*1000*ms,stroke=1,fill=0)
    label(' / '.join(str(t['moving'])+':'+str(t['receiver']) for t in targets),x,y-11,8,MUTED)

def frame_card(s,f,x,y,w,h,tag=None,tray=True):
    n=s['number'];num=f['number'];label(tag or str(n)+'.'+str(num),x,y-12,12,CORAL,True)
    if f.get('preassembled'):label('1x preassembled',x+62,y-12,9,INK,True)
    elif f.get('child'):
        component=('B' if num==9 else 'C' if num==14 else 'A+B+C')+str(n) if n in [17,18] else '1x unit'
        label(component,x+80,y-12,10,INK,True)
    elif f.get('kind')=='receiver-context' and n in [17,18]:
        label(('A' if num==8 else 'A+B' if num==13 else 'Truck')+str(n),x+80,y-12,10,INK,True)
    pair=next((k for k in locations if k==f's{n}-f{num}' or k==f's{n}-f{num+1}' and f.get('kind')=='receiver-context'),None)
    if pair:marked_picture(pair,'before' if f.get('kind')=='receiver-context' else 'after',x,y-h+45,w,h-72)
    else:picture(D/f['image'],x,y-h+(48 if tray else 12),w,h-(70 if tray else 34))
    if tray and not f.get('preassembled') and not f.get('child') and f.get('kind')!='receiver-context':compact_tray(f['ids'],x,y-h+40,w)

def main_card(s,x,y,w,h):
    a=s['manual'];para(str(s['number'])+'  '+a['title'],x,y,w,12,font='Bold',leading=15)
    picture(D/a['image'],x,y-h+100,w,h-150)
    if a.get('repeat_from'):
        label('1x / recipe '+str(a['repeat_from']),x,y-h+98,10,CORAL,True)
        compact_tray(s['new_ids'],x,y-h+85,w)
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
        ff=[a['frames'][i-1] for i in item['frames']];copies=item.get('copies')
        if copies:
            unit_ids=list(dict.fromkeys(i for f in ff for i in f['ids']));compact_tray(unit_ids,36,HH-111,W-72)
            badge='A' if item['frames'][0]==1 else 'B'
            label(badge+'17 + '+badge+'18 / 2x / one-copy parts',36,HH-91,10,CORAL,True)
            label(badge+'18 reserved for step 18',W-240,58,10,CORAL,True)
        cols=2;rows=(len(ff)+1)//2;width=(W-90)/2;height=(HH-(225 if copies else 165))/rows
        for j,f in enumerate(ff):frame_card(s,f,36+(j%2)*(width+18),HH-(171 if copies else 113)-(j//2)*height,width,height,tray=not copies)
    elif kind=='rail2':
        compact_tray([331,46,48],36,HH-111,W-72)
        label('C17 + C18 / 2x / one-copy parts',36,HH-91,10,CORAL,True)
        # Each lane is an exact source sequence; never read the two lanes serially.
        width=(W-130)/3;height=(HH-225)/2
        for row,st in enumerate(ss):
            top=HH-171-row*height
            c.setStrokeColor(LINE);c.roundRect(28,top-height+6,W-56,height-2,8,stroke=1,fill=0)
            for col,i in enumerate([10,11,12]):frame_card(st,st['manual']['frames'][i-1],45+col*(width+15),top,width,height-6,tag='C'+str(st['number'])+' / '+str(col+1),tray=False)
        label('C18 reserved for step 18',W-240,58,10,CORAL,True)
    elif kind=='callout':
        all_frames=a['frames'];unit_ids=list(dict.fromkeys(i for f in all_frames if not f.get('preassembled') for i in f['ids']))
        tray_height=compact_tray(unit_ids,36,HH-111,W-72)
        ff=[all_frames[i-1] for i in item.get('frames',range(1,len(all_frames)+1))]
        if s['number'] in [47,48,60]:ff=[ff[-1]]
        width=330;cols=2 if len(ff)>2 else 1;rows=(len(ff)+cols-1)//cols
        top=HH-125-tray_height;height=(top-68)/rows
        c.setStrokeColor(LINE);c.roundRect(28,52,350,top-44,8,stroke=1,fill=0)
        label(str(s.get('copies',1))+'x / one-copy parts',36,HH-91,10,CORAL,True)
        for j,f in enumerate(ff):frame_card(s,f,36+(j%cols)*165,top-(j//cols)*height,width/cols-8,height,tag=str(j+1),tray=False)
        label(str(s['number'])+' / '+str(s.get('copies',1))+'x',402,top-12,12,INK,True)
        picture(D/a['image'],397,80,W-430,top-115)
        c.setStrokeColor(CORAL);c.setLineWidth(1.2);c.line(380,(top+60)/2,394,(top+60)/2)
    elif kind=='approach':
        for j,f in enumerate(a['approach_frames']):
            picture(D/f['image'],36+j*390,110,375,HH-240)
            label('1 plate above' if j==0 else 'Slide inward, then lower',36+j*390,88,11,INK,True)
    else:raise ValueError(kind)
    finish('simplification-i2',composition=item,source_operations={str(st['number']):st['operations'] for st in ss})

(D/'tray-measurements.json').write_text(json.dumps(tray_measurements,indent=2)+'\n')

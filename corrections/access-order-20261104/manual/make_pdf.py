"""DSS-local layout overlay on the retained legacy PDF template."""
from pathlib import Path
import hashlib,sys,os
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/os.environ.get('DSS_PDF_BUILD','builds/access-corrected-r2')
TEMPLATE=ROOT/'sources/legacy-recipes/make_full_instruction_pdf.py'
code=TEMPLATE.read_text()
# Reader-facing text only: retain the model and every image/quantity/page layout.
code=code.replace("'DSS TAIPEI CURRENT  /  '+EDITION.upper()", "'DSS TAIPEI CURRENT'")
# Two exact legacy PDF literals have unsupported glyphs in their selected fonts.
old_turn="label('↻ '+a['turn_model'],W-160,HH-102,12,CORAL,True)"
assert code.count(old_turn)==1
code=code.replace(old_turn,"label('Turn: '+a['turn_model'],W-160,HH-102,12,CORAL,True)")
old_banner="note='洋 above · 流 below · both faces.'"
assert code.count(old_banner)==1
code=code.replace(old_banner,"note='洋 above / 流 below / both faces.'")
def caption(f):
    op=f['source_operation']
    if f['kind']=='receiver-context':
        return 'Locate the mounting points. Keep the completed unit separate.'
    exact={
      'legacy-012':'Fit one pin near each end. Leave both pin ends exposed toward the second beam.',
      'legacy-001b':'Align both holes. Seat both pins before adding tie plates.',
      'legacy-006':'Check both pins are seated and all tie plates are fitted.',
      'legacy-032b':'Build the bumper separately: brackets, cap, slopes, then trim.',
      'legacy-035j':'Fit the cap to the front ties. Support the chassis; leave the front dish off.',
      'legacy-031b':'Turn over. Fit the front dish after the complete bumper.',
      'legacy-050':'Align both floor supports before seating the completed carrier.',
      'legacy-058':'Align both floor supports before seating the completed carrier.',
    }
    if op in exact:return exact[op]
    if op in ['legacy-049j1','legacy-049j2','legacy-057j1','legacy-057j2']:
        return 'Align the mounting brackets. Keep the other rail separate until its brackets are complete.'
    note=f.get('note','')
    note=note.replace('Support the loose rail while fitting the bracket; do not attach the rail to the lower carrier yet.', 'Support the loose rail. Fit this bracket before attaching the rail.')
    return note

needle="    frames=a.get('frames',[])"
assert code.count(needle)==1
block='''    if a.get('corrected'):
        step_page[str(n)]=page+1
        display_frames=[f for f in a['frames'] if not (a.get('repeat_prefix_from') and f['number']<=a['repeat_prefix_frames'])]
        for f in display_frames:
            if os.environ.get('DSS_ORDERED_PREFIX')=='1' and n==1 and f['number']<=3:
                if f['number']!=1:continue
                start(s['section'],'Fit both pins before the second beam',n)
                part_box([172,216,231,178],x=36,y=HH-149,width=165)
                picture(D/'ordered-prefix.png',206,135,W-240,HH-260)
                para('3. Seat the second beam on BOTH exposed pins.',210,123,W-247,11)
                finish('ordered-construction-diagram',step=n,panels=[1,2,3],source_operations=['legacy-001a','legacy-012','legacy-001b'],image='ordered-prefix.png')
                continue
            start(s['section'],f['title'],n)
            label(f"Panel {f['number']} / {len(a['frames'])}",36,HH-117,11,CORAL,True)
            if f.get('copy_count')==2:label('2x / parts for one copy',210,HH-117,11,CORAL,True)
            if a.get('repeat_prefix_from') and f==display_frames[0]:label('Use the second base from step '+str(a['repeat_prefix_from']),210,HH-117,11,CORAL,True)
            if f.get('child'):
                para('1 x COMPLETED UNIT',36,HH-146,174,11,font='Bold')
                para(f['child'].replace('-',' '),36,HH-170,174,13,font='Bold')
                para(str(len(f['ids']))+' pieces / no new loose parts',36,HH-213,166,11)
            elif f.get('awaiting_child'):
                para('RECEIVING STRUCTURE',36,HH-146,174,11,font='Bold')
                para('No new parts. Set the completed unit aside.',36,HH-180,166,11)
            else:
                part_box(f['ids'],x=36,y=HH-149,width=165)
            picture(D/f['image'],206,135,W-240,HH-260)
            note=caption(f)
            para(note,210,123,W-247,11)
            finish('corrected-ordered-panel',step=n,panel=f['number'],source_operation=f['source_operation'],image=f['image'])
        continue
'''
code=code.replace(needle,block+needle)
code=code.replace("shutil.copyfile(OUT,D/'instructions.pdf')","# Output already lives in the package.")
# Exact original artwork paths resolve against the retained read-only library.
code=code.replace("H=Path(__file__).resolve().parent;ROOT=H.parents[1]","H=Path('/Users/clkao/git/house-demo/projects/yangliu-vehicle');ROOT=H.parents[1]")
sys.argv=[str(TEMPLATE),'--dir',str(OUT),'--pdf',str(OUT/'instructions.pdf')]
exec(compile(code,str(TEMPLATE),'exec'),{'__name__':'__main__','__file__':str(TEMPLATE),'caption':caption,'os':os})

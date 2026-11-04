"""DSS-local layout overlay on the retained legacy PDF template."""
from pathlib import Path
import hashlib,sys
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'builds/access-corrected'
TEMPLATE=ROOT/'sources/legacy-recipes/make_full_instruction_pdf.py'
code=TEMPLATE.read_text()
needle="    frames=a.get('frames',[])"
assert code.count(needle)==1
block='''    if a.get('corrected'):
        step_page[str(n)]=page+1
        for f in a['frames']:
            start(s['section'],f['title'],n)
            label(f"Panel {f['number']} / {len(a['frames'])}",36,HH-117,11,CORAL,True)
            if f.get('child'):
                para('USE ONE COMPLETED UNIT',36,HH-146,174,11,font='Bold')
                para(f['child'].replace('-',' '),36,HH-170,174,13,font='Bold')
                para(str(len(f['ids']))+' pieces already built. Do not collect these as loose parts again.',36,HH-213,166,11)
            else:
                part_box(f['ids'],x=36,y=HH-149,width=165)
            picture(D/f['image'],206,135,W-240,HH-260)
            note=f.get('note') or ('Join the completed unit to the receiving structure shown.' if f.get('child') else 'Add the highlighted parts in this panel before continuing.')
            para(note,210,123,W-247,11)
            label('Installed view - insertion clearance and physical fit remain unverified.',210,62,8.5,MUTED)
            finish('corrected-ordered-panel',step=n,panel=f['number'],source_operation=f['source_operation'],image=f['image'])
        continue
'''
code=code.replace(needle,block+needle)
code=code.replace("shutil.copyfile(OUT,D/'instructions.pdf')","# Output already lives in the package.")
# Exact original artwork paths resolve against the retained read-only library.
code=code.replace("H=Path(__file__).resolve().parent;ROOT=H.parents[1]","H=Path('/Users/clkao/git/house-demo/projects/yangliu-vehicle');ROOT=H.parents[1]")
sys.argv=[str(TEMPLATE),'--dir',str(OUT),'--pdf',str(OUT/'instructions.pdf')]
exec(compile(code,str(TEMPLATE),'exec'),{'__name__':'__main__','__file__':str(TEMPLATE)})

"""Compose one isolated iteration from frozen DSS images. No rendering or publication."""
from pathlib import Path
import hashlib, json, os, sys, runpy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BASE=ROOT/'builds/access-corrected-hybrid-prefix'
D=ROOT/'builds/simplification-i1-retry1'
assert not D.exists(), 'Preserve candidates; output must be absent'
expected={'model.json':'3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229','instructions.pdf':'6d02aa7dbf0e9fc58cbc4f963bd9fbe805bba9a1cdd134a1ecc3d1b22e9ac062'}
for name,sha in expected.items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha,name
D.mkdir()
for name in ['model.json','part-icons.json','front.png','images','ordered-prefix.png']:(D/name).symlink_to((BASE/name).resolve())
TEMPLATE=ROOT/'sources/legacy-recipes/make_full_instruction_pdf.py'
code=TEMPLATE.read_text()
assert hashlib.sha256(TEMPLATE.read_bytes()).hexdigest().startswith('150df952')
code=code.replace("'DSS TAIPEI CURRENT  /  '+EDITION.upper()", "'DSS TAIPEI CURRENT'")
finish_line="page_records.append(dict(page=page,kind=kind,**meta));c.showPage()"
assert code.count(finish_line)==1
code=code.replace(finish_line,finish_line+";jpeg_cache.clear()")
code=code.replace("H=Path(__file__).resolve().parent;ROOT=H.parents[1]", "H=Path('/Users/clkao/git/house-demo/projects/yangliu-vehicle');ROOT=H.parents[1]")
code=code.replace("note='洋 above · 流 below · both faces.'", "note='洋 above / 流 below / both faces.'")
begin=code.index('step_page={}');end=code.index("start('Print at actual size'",begin)
code=code[:begin]+(HERE/'layout.py').read_text()+'\n'+code[end:]
code=code.replace("shutil.copyfile(OUT,D/'instructions.pdf')",'# PDF already in own output')
composition=runpy.run_path(str(HERE/'plan.py'))['pages']()
(D/'composition-plan.json').write_text(json.dumps(composition,indent=2)+'\n')
sys.argv=[str(TEMPLATE),'--dir',str(D),'--pdf',str(D/'instructions.pdf')]
exec(compile(code,str(TEMPLATE),'exec'),{'__name__':'__main__','__file__':str(TEMPLATE),'composition_pages':composition})

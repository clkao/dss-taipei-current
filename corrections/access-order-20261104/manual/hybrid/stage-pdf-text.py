"""Retain exact first PDF/map/guides before the authorized text-only successor."""
from pathlib import Path
import hashlib
R=Path(__file__).resolve().parents[4];D=R/'builds/access-corrected-hybrid-prefix'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(D/'instructions.pdf')=='d8cb787b8f6572854370e650b4ceb2f59c35d78e3ae5bec7ebd43d16bbabc137'
assert sha(D/'pdf-page-map.json')=='e9df2efac6f2499a68d1d744848fc82cf522015bc5d1e40c216e107ea371f67c'
names=['instructions.pdf','pdf-page-map.json','hood-sticker-cut.png','hood-upper-sticker-guide.png','jacket-print.png']
for n in names:assert (D/n).is_file() and not (D/n).is_symlink(),n
keep=D/'before-diagram-text-trim';keep.mkdir()
for n in names:(D/n).rename(keep/n)
for n in names:assert not (D/n).exists() and not (D/n).is_symlink(),n

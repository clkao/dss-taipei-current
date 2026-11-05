"""One-time UI-only successor staging; execute only with its coordinated lease."""
from pathlib import Path
import hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];B=R/'builds/access-corrected-hybrid-prefix'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(B/'viewer.html')=='1d56a99417d2e6d64185398f9c85a76ccea31837803a46c8d737a126831b7a18'
assert sha(B/'instructions.pdf')=='d8cb787b8f6572854370e650b4ceb2f59c35d78e3ae5bec7ebd43d16bbabc137'
old=subprocess.check_output(['git','show','5562901:corrections/access-order-20261104/manual/hybrid/viewer.js'],cwd=R,text=True)
new=(P/'viewer.js').read_text();retained=B/'before-sidebar-fix';retained.mkdir()
for n in ['viewer.html','index.html']:
 h=(B/n).read_text();needle='<script>'+old+'</script>';assert h.count(needle)==1
 (B/n).rename(retained/n);(B/n).write_text(h.replace(needle,'<script>'+new+'</script>'))
for f in list(B.glob('r2-*.json'))+list(B.glob('r2-*.log'))+list(B.glob('r2-*.png')):f.rename(retained/f.name)
print(sha(B/'viewer.html'))

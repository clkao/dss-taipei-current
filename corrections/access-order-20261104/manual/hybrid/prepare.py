"""Opt-in candidate staging. Run only under the coordinated integration lease."""
import hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
OLD=ROOT/'builds/access-corrected-r2';NEW=ROOT/'builds/access-corrected-hybrid-prefix'
binding=json.loads((P/'binding.json').read_text())
assert binding['corrected_asset'] and binding['corrected_asset_sha256'], 'Await exact upstream paired-target asset handoff'
UP=Path(binding['corrected_asset'])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(UP)==binding['corrected_asset_sha256']
assert sha(OLD/'model.json')=='3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229'
m=json.loads((OLD/'model.json').read_text());frames=m['instruction_plan']['steps'][0]['manual']['frames']
assert [(f['source_operation'],f['ids']) for f in frames[:3]]==[('legacy-001a',[172]),('legacy-012',[216,231]),('legacy-001b',[178])]
NEW.mkdir() # Fail rather than reuse an existing candidate.
# Reuse unchanged assets; generated files are never links to historical outputs.
exclude={'index.html','viewer.html','credits.html','instructions.pdf','pdf-page-map.json','release.zip','package-manifest.json','release-provenance.json','print-preflight.json','full-instruction-check.json','sticker-artwork.zip','README.txt'}
for p in OLD.iterdir():
 if p.name in exclude or p.name.startswith(('before-','a4-','glyph-','r2-')):continue
 if p.is_file() or p.name=='images':(NEW/p.name).symlink_to(p.resolve())
(NEW/'ordered-prefix.png').symlink_to(UP)
script='<script>'+ (P/'viewer.js').read_text()+'</script>'
for n in ['viewer.html','index.html']:
 h=(OLD/n).read_text();assert h.count('</html>')==1;(NEW/n).write_text(h.replace('</html>',script+'</html>'))
(NEW/'credits.html').write_bytes((OLD/'credits.html').read_bytes())
print(NEW)

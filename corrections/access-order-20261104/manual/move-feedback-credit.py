"""One-time static site correction, preserving the reviewed R2 artifacts."""
import hashlib,json,re,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent; ROOT=P.parents[2]; B=ROOT/'builds/access-corrected-r2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
oldmap=json.loads((P/'evidence/r2/r2-publication-file-map.json').read_text())
before={r['publication_path']:sha(B/r['publication_path']) for r in oldmap['files']}
assert all(before[r['publication_path']]==r['sha256'] for r in oldmap['files'])
changed=['index.html','credits.html','release-provenance.json','release.zip','package-manifest.json']
retained=B/'before-credit-move';retained.mkdir()
for n in changed:
 p=B/n
 if p.is_symlink():
  (retained/n).write_bytes(p.read_bytes());p.unlink()
 else:p.rename(retained/n)
feedback=(P/'instruction-feedback.html').read_text()
link='<p id="instruction-feedback"><a href="credits.html#instruction-feedback">Instruction feedback / 組裝說明回饋</a></p>'
old=(retained/'index.html').read_text();assert old.count(feedback)==1
index=old.replace(feedback,link)
credits=(P/'retained-credits.html').read_text();assert credits==(retained/'credits.html').read_text()
anchor='<section id="physical-vehicle">';assert credits.count(anchor)==1
credits=credits.replace(anchor,feedback+'\n'+anchor)
(B/'index.html').write_text(index);(B/'credits.html').write_text(credits)
assert credits.count(feedback)==1 and feedback not in index
assert credits.index(feedback)<credits.index(anchor)
assert re.findall(r'<script\b.*?</script>',old,re.S)==re.findall(r'<script\b.*?</script>',index,re.S)
assert index.replace(link,feedback)==old
prov=json.loads((retained/'release-provenance.json').read_text())
for n in ['index.html','credits.html']:prov['files'][n]=sha(B/n)
write(B/'release-provenance.json',prov)
manifest=json.loads((retained/'package-manifest.json').read_text())
for n in ['index.html','credits.html','release-provenance.json']:manifest['files'][n]=sha(B/n)
with zipfile.ZipFile(retained/'release.zip') as src,zipfile.ZipFile(B/'release.zip','w') as dst:
 for info in src.infolist():
  data=(B/info.filename).read_bytes() if info.filename in ['index.html','credits.html','release-provenance.json'] else src.read(info.filename)
  dst.writestr(info,data)
manifest['files']['release.zip']=sha(B/'release.zip');write(B/'package-manifest.json',manifest)
assert all(sha(B/n)==s for n,s in before.items() if n not in changed)
with zipfile.ZipFile(B/'release.zip') as z,zipfile.ZipFile(retained/'release.zip') as oldz:
 assert z.namelist()==oldz.namelist()
 for n in z.namelist():
  if n not in ['index.html','credits.html','release-provenance.json']:assert z.read(n)==oldz.read(n)
  if n in manifest['files']:assert hashlib.sha256(z.read(n)).hexdigest()==manifest['files'][n]
assert all(sha(B/n)==s for n,s in manifest['files'].items())
rows=[dict(source=str(B/n),publication_path=n,sha256=sha(B/n),previous_sha256=before[n],action='replace' if n in changed else 'reuse unchanged') for n in before]
write(P/'evidence/r2/credit-move-publication-file-map.json',dict(baseline_publication='244eda13a5c64c46ad8a7081be7151e0b5e775be',files=rows,preserve=['technic/','all unrelated publication paths'],publication_changed=False))
write(P/'evidence/r2/credit-move-check.json',dict(changed=changed,pins={n:sha(B/n) for n in changed},pdf_sha256=sha(B/'instructions.pdf'),full_feedback_exactly_once_in_credits=True,homepage_anchor_link_only=True,index_scripts_and_embedded_data_unchanged=True,all_other_release_files_unchanged=True,zip_unchanged_members_byte_equal=True,manifest_hashes_pass=True,retained=str(retained)))
print(json.dumps({n:sha(B/n) for n in changed},indent=2))

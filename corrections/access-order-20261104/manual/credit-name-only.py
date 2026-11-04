"""Apply the captain's name-only credit edit to the existing static package."""
from pathlib import Path
import hashlib,json,re,zipfile
P=Path(__file__).resolve().parent;B=P.parents[2]/'builds/access-corrected-r2'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
prior=json.loads((P/'evidence/r2/credit-move-publication-file-map.json').read_text())
before={r['publication_path']:sha(B/r['publication_path']) for r in prior['files']}
assert all(before[r['publication_path']]==r['sha256'] for r in prior['files'])
changed=['credits.html','release-provenance.json','release.zip','package-manifest.json']
retained=B/'before-credit-name-only';retained.mkdir()
for n in changed:(B/n).rename(retained/n)
old=(retained/'credits.html').read_text();section=(P/'instruction-feedback.html').read_text().rstrip('\n')
pattern=r'<section id="instruction-feedback".*?</section>'
assert len(re.findall(pattern,old,re.S))==1
new=re.sub(pattern,lambda _:section,old,flags=re.S)
assert section.count('<p>')==1 and '<p>彭柏源</p>' in section
(B/'credits.html').write_text(new)
assert re.sub(pattern,'',old,flags=re.S)==re.sub(pattern,'',new,flags=re.S)
prov=json.loads((retained/'release-provenance.json').read_text());prov['files']['credits.html']=sha(B/'credits.html');write(B/'release-provenance.json',prov)
manifest=json.loads((retained/'package-manifest.json').read_text())
for n in ['credits.html','release-provenance.json']:manifest['files'][n]=sha(B/n)
with zipfile.ZipFile(retained/'release.zip') as src,zipfile.ZipFile(B/'release.zip','w') as dst:
 for info in src.infolist():dst.writestr(info,(B/info.filename).read_bytes() if info.filename in ['credits.html','release-provenance.json'] else src.read(info.filename))
manifest['files']['release.zip']=sha(B/'release.zip');write(B/'package-manifest.json',manifest)
assert all(sha(B/n)==v for n,v in before.items() if n not in changed)
with zipfile.ZipFile(B/'release.zip') as z,zipfile.ZipFile(retained/'release.zip') as oldz:
 assert z.namelist()==oldz.namelist()
 for n in z.namelist():
  if n not in ['credits.html','release-provenance.json']:assert z.read(n)==oldz.read(n)
  if n in manifest['files']:assert hashlib.sha256(z.read(n)).hexdigest()==manifest['files'][n]
assert all(sha(B/n)==v for n,v in manifest['files'].items())
rows=[dict(source=str(B/n),publication_path=n,sha256=sha(B/n),previous_sha256=before[n],action='replace' if n in changed else 'reuse unchanged') for n in before]
write(P/'evidence/r2/credit-name-publication-file-map.json',dict(baseline_publication='1ee039a',files=rows,preserve=['technic/','all unrelated publication paths'],publication_changed=False))
write(P/'evidence/r2/credit-name-check.json',dict(changed=changed,pins={n:sha(B/n) for n in changed},pdf_sha256=sha(B/'instructions.pdf'),credit_heading_preserved=True,credit_paragraph_name_only=True,homepage_link_unchanged=True,other_files_and_zip_members_unchanged=True,manifest_hashes_pass=True,retained=str(retained)))
print(json.dumps({n:sha(B/n) for n in changed},indent=2))

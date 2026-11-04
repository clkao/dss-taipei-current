"""Prepare relative Technic links and one public print PDF."""
import hashlib,json,posixpath,re,shutil,zipfile
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit

OLD_PRINT_PDFS=['stickers-a4.pdf','stickers-compact.pdf','stickers-cutlines.pdf','stickers-white-ink-mask.pdf','tsai-banner-print.pdf']

def stage_technic(source,site):
    source,site=Path(source),Path(site)
    target=site/'technic'
    shutil.copytree(source,target,dirs_exist_ok=True)
    for page in target.rglob('*.html'):
        def replace(match):
            url=urlsplit(match[2])
            if not url.path.startswith('/') or url.path.startswith('//'):return match[0]
            path=site/url.path.lstrip('/')
            if path.is_dir():path=path/'index.html'
            elif not path.suffix and path.with_suffix('.html').exists():path=path.with_suffix('.html')
            if not path.is_file():raise ValueError(f'Broken local link: {page}: {match[2]}')
            relative=posixpath.relpath(path.relative_to(site).as_posix(),page.parent.relative_to(site).as_posix())
            return match[1]+urlunsplit(('', '',relative,url.query,url.fragment))+match[3]
        text=re.sub(r'\bdonor\b','upstream',page.read_text(),flags=re.I)
        page.write_text(re.sub(r'((?:href|src|action)=["\'])(/[^"\']*)(["\'])',replace,text))
    manifest=target/'package-manifest.json'
    data=json.loads(manifest.read_text())
    data['hosting_adaptation']='Relative links and explicit HTML targets for a GitHub Pages project subdirectory; embedded model unchanged.'
    data['files']={p.relative_to(target).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in target.rglob('*') if p.is_file() and p!=manifest}
    manifest.write_text(json.dumps(data,indent=2)+'\n')

def single_print_pdf(site):
    site=Path(site)
    for name in OLD_PRINT_PDFS:(site/name).unlink(missing_ok=True)
    guide=dict(pdf='instructions.pdf',pages=102,print_sheets=[dict(page=94,contents='Vehicle stickers'),dict(page=95,contents='Two speech-bubble faces and jacket')],scale='100% / actual size; check the printed scale bar.',editable_sources='sticker-artwork.zip',scope='One public print PDF. Editable SVG files retain specialist cut and white-ink layouts.')
    old=site/'print-preflight.json'
    if old.exists():
        data=json.loads(old.read_text())
        if 'artwork' in data:
            evidence=site/'review-evidence';evidence.mkdir(exist_ok=True)
            (evidence/'artwork-source-preflight.json').write_text(json.dumps(data,indent=2)+'\n')
    old.write_text(json.dumps(guide,indent=2)+'\n')
    path=site/'sticker-artwork.zip';temp=site/'artwork-updated.zip'
    with zipfile.ZipFile(path) as src,zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as out:
        seen=set()
        for info in src.infolist():
            if info.filename.endswith('.pdf') or info.filename in seen or info.filename=='PRINTING.txt':continue
            seen.add(info.filename);out.writestr(info,src.read(info.filename))
        out.writestr('PRINTING.txt','Print instructions.pdf pages 94–95 at 100% / actual size. This ZIP contains editable artwork, not a second print PDF. Specialist white-ink and cut layouts remain editable SVG sources.\n')
    temp.replace(path)
    return guide

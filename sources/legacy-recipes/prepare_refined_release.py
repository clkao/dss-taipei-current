"""Package the shared v8 model/plan and compact offline viewer. Does not deploy."""
import argparse,hashlib,html,json,re,shutil,subprocess,sys,zipfile
from collections import defaultdict
from pathlib import Path
from static_release_assets import stage_technic,single_print_pdf
H=Path(__file__).resolve().parent;R=H.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--build',type=Path,default=R/'output/yangliu-refined-v8');ap.add_argument('--evidence',type=Path,default=H/'evidence/refined-v8-2026-11-03');ap.add_argument('--source',type=Path,default=H/'prototypes/refined-v8');ap.add_argument('--github-pages',action='store_true');a=ap.parse_args()
D=a.build;O=a.out;B=R/'output/yangliu-sharing-site-20261103-v3';E=a.evidence
if O.exists():raise SystemExit('Use a fresh staging directory')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
m=load(D/'model.json');cat=load(D/'catalog-meshes.json');check=load(D/'full-instruction-check.json');mapping=load(D/'bricklink-mapping.json')
count=len(m['pieces']);steps=len(m['instruction_plan']['steps']);edition=m['instruction_edition'];label=m['revision']+'-20261103';conn=load(E/'catalog-connections.json');prefix=load(E/'controls.json')
assert check['model_sha256']==mapping['model_sha256']==sha(D/'model.json')
shutil.copytree(B,O,ignore=shutil.ignore_patterns('netlify.toml','_headers','vercel.json','release.zip')if a.github_pages else None)
if a.github_pages:
    (O/'.nojekyll').write_text('')
    stage_technic(B/'technic',O)
    (O/'README.md').write_text('''# DSS Taipei Current / 洋流號

**Democratic Service Ship** — a civic ship theme for this minifigure model.

[Open the 3D viewer](https://clkao.github.io/dss-taipei-current/) · [Illustrated PDF](https://clkao.github.io/dss-taipei-current/instructions.pdf) · [Sources and credits](https://clkao.github.io/dss-taipei-current/credits.html)

348 rigid pieces · 68 main steps · 102 PDF pages. Both figures arrive assembled; 小英 holds one two-sided speech-bubble banner.

This repository contains the prebuilt static website on its single `gh-pages` branch. GitHub Pages serves the branch root; `.nojekyll` keeps the files unchanged. No build is required to view the site. Download `release.zip` and open `viewer.html` for offline viewing.

Original contributions and adaptations © 2026 CL Kao, licensed under **CC BY-SA 4.0**. Third-party creations retain their original terms and attribution; see [LICENSE.txt](LICENSE.txt) and the full source credits. The 40 named creator identities comprise 35 LDraw authors, four other upstream creators, and CL Kao. PTadmin and unnamed collective contributors are acknowledged separately.

Real-brick fit, grip, suspension response and handling strength remain untested. The digital review and its limits are included in `digital-fit-audit.md` and `review-evidence/`.

The real-world 洋流號 is credited collectively to the Shen Po-yang campaign team and contributors. Its individual vehicle designer and fabricator remain unverified; see [the physical-vehicle reference](credits.html#physical-vehicle). This attribution is separate from the upstream LEGO construction and graphic sources.
''')
for n in ['instructions.pdf','full-instruction-check.json','pdf-page-map.json','yangliu-shape.mpd','inventory.csv','wanted-list.xml','bricklink-inventory.csv','bricklink-mapping.json','model.json','instruction-plan.json','assembly-manifest.json','mpd-validation.json','prototype-summary.json','render-scene.json','catalog-meshes.json']:
    if (D/n).exists():shutil.copyfile(D/n,O/n)
shutil.copyfile(D/'inventory.csv',O/'preliminary-inventory.csv')
shutil.copyfile(D/'viewer.html',O/'viewer.html');shutil.copyfile(D/'viewer.html',O/'index.html')
for n,t in cat['licenses'].items():(O/'licenses'/Path(n).name).write_text(t)
shutil.copyfile(H/'LICENSE.txt',O/'LICENSE.txt')
shutil.copyfile(H/'licenses/CC-BY-SA-4.0.txt',O/'licenses/CC-BY-SA-4.0.txt')
notices='LDraw geometry: original notices, unmodified source files supplied in ldraw/.\nTransforms, palette and assembly are adaptations by CL Kao.\n\n'
notices+='\n\n'.join(f+'\n'+'\n'.join(lines)for f,lines in sorted(cat['attribution'].items()))
(O/'CATALOG-NOTICES.txt').write_text(notices+'\n')
with zipfile.ZipFile(H/'sources/ldraw-complete.zip')as z,zipfile.ZipFile(O/'ldraw-sources.zip','w',zipfile.ZIP_DEFLATED)as out:
    for f in cat['attribution']:
        raw=z.read('ldraw/'+f);p=O/'ldraw'/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);out.writestr(f,raw)
    out.write(O/'CATALOG-NOTICES.txt','CATALOG-NOTICES.txt')
esc=html.escape;authors=defaultdict(list);rows=[]
for f,lines in sorted(cat['attribution'].items()):
    author='; '.join(v.removeprefix('0 Author: ')for v in lines if v.startswith('0 Author: '))or'See source notices';authors[author].append(f)
ldraw_creators=sorted({v.removeprefix('0 Author: ').strip()for lines in cat['attribution'].values()for v in lines if v.startswith('0 Author: ')and v.removeprefix('0 Author: ').strip()not in ['[PTadmin]','']})
other_upstream=['KamalMYafi','Sylvain Sauvage','Roland Melkert','AYA／AYA全糖腐女中心'];project_creators=['CL Kao']
creator_count=len(ldraw_creators)+len(other_upstream)+len(project_creators)
contributor_count=dict(credited_creator_identities=creator_count,ldraw_named_or_pseudonymous_creators=len(ldraw_creators),ldraw_creators=ldraw_creators,other_upstream_creators=other_upstream,project_creators=project_creators,administrative_attributions=['[PTadmin]'],ldraw_attribution_entries=len(authors),ldraw_source_files=len(cat['attribution']),scope='Named credited creator identities across upstream sources and this project; excludes unnamed library contributors and collective credits such as the campaign, Three.js and pyldraw3. Not a count of direct collaborators.',catalog_sha256=sha(D/'catalog-meshes.json'))
physical_vehicle=load(H/'design/physical-vehicle-attribution.json')
shutil.copyfile(H/'design/physical-vehicle-attribution.json',O/'physical-vehicle-attribution.json')
(O/'contributor-count.json').write_text(json.dumps(contributor_count,ensure_ascii=False,indent=2)+'\n')
for part in sorted({p['part']for p in m['pieces']}):
    f='parts/'+part+'.dat';lines=cat['attribution'][f];owner='; '.join(v.removeprefix('0 Author: ')for v in lines if v.startswith('0 Author: '));license='; '.join(v.removeprefix('0 !LICENSE ')for v in lines if v.startswith('0 !LICENSE '));used=[p for p in m['pieces']if p['part']==part]
    rows.append(f'<tr><td><a href="ldraw/{esc(f)}">{esc(part)}.dat</a></td><td>{esc(owner)}</td><td>{len(used)} occurrences; {esc(", ".join(sorted({p["module"]for p in used})))}</td><td>{esc(license)}</td></tr>')
by_author=''.join(f'<details><summary>{esc(owner)} · {len(files)} source files</summary><ul>'+''.join(f'<li><a href="ldraw/{esc(f)}">{esc(f)}</a></li>'for f in files)+'</ul></details>'for owner,files in sorted(authors.items()))
credit=(B/'credits.html').read_text().replace('this 327-piece vehicle',f'this {count}-piece scene')
credit=re.sub(r'<tbody>.*?</tbody>','<tbody>'+''.join(rows)+'</tbody>',credit,flags=re.S)
credit=re.sub(r'(</h2><p>Resolved geometry.*?</p>).*?(<p>Catalog archive SHA-256:)',lambda r:r[1]+by_author+r[2],credit,flags=re.S)
credit=re.sub(r'Model SHA-256: <code>.*?</code>',f'Model SHA-256: <code>{sha(D/"model.json")}</code>',credit)
credit=credit.replace('href="https://yangliu-lego.netlify.app/ldraw/','href="ldraw/').replace('href="/"','href="index.html"')
credit=credit.replace('<h2>Attribution and permission status</h2>','<h2>New enclosure and speech-bubble scene</h2><p>CL Kao added the transparent enclosure, relocated the helm and outboard rails, and planned the revised installation. Philippe Hurbain supplied the 59349 clear panel and 62711 bob-hair meshes; Steve Bliss supplied the plain 973 torso and 30374 bar meshes. The 小英 figure uses an adapted catalog-parts pose, a custom jacket graphic and one real 2335 flag with two speech-bubble decals, 叫你休息 and 講不聽. These custom graphics were drawn for this project; no external portrait was incorporated. The table below maps every active part to its original author.</p><h2>Attribution and permission status</h2>')
credit=credit.replace('<h2>Attribution and permission status</h2>','<h2 id="meme">Meme inspiration: AYA</h2><p>The 小英拍背／叫你休息 meme is credited to <strong><a href="https://www.threads.com/@theaya1108">AYA／AYA全糖腐女中心 (@theaya1108)</a></strong>. <a href="https://lurl.cc/TGMpwc">Original-comic link reported by 放言</a> · <a href="https://www.fountmedia.io/article/438474">source and attribution</a> · <a href="https://www.ftvnews.com.tw/news/detail/2026B02W0139">report crediting AYA for the 叫你休息 comic</a>.</p><p>This project adapts the meme into one two-sided LEGO speech-bubble banner. CL Kao drew the new decal layout; the faces read「叫你休息」and「講不聽」.「講不聽」is our adaptation of the dialogue, not a claim to quote the original comic exactly. The original character illustration is not reproduced. The original social post could not be opened independently; the source link above is retained as reported.</p><h2>Attribution and permission status</h2>')
credit=credit.replace('<h2>Attribution and permission status</h2>','<h2 id="license">License for our contributions</h2><p>Original contributions and adaptations © 2026 CL Kao, licensed under <a rel="license" href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>. Credit the creator, link the license, indicate changes, and share adaptations under the same or a compatible license as its terms require. <a href="LICENSE.txt">Scope and third-party exclusions</a> · <a href="licenses/CC-BY-SA-4.0.txt">Full legal text</a>.</p><p>This grant covers our contributions only. Referenced and incorporated third-party creations retain their original terms and attribution; it does not grant missing permissions for the donor assembly, campaign material or original meme.</p><h2>Attribution and permission status</h2>')
credit=re.sub(r'\bdonor\b','upstream',credit,flags=re.I)
credit=credit.replace('<title>Yangliu minifigure edition - sources and contributors</title>','<title>DSS Taipei Current - sources and contributors</title>')
physical_credit='''<section id="physical-vehicle"><h2>Original physical vehicle: 洋流號</h2><p>The real campaign vehicle is credited collectively to the <strong>Shen Po-yang campaign team and contributors / 沈伯洋競選團隊及參與創作者</strong>. <a href="https://current.puma.taipei/">Official campaign project</a> · <a href="https://udn.com/vote2026/story/124652/9785376">September 30 launch report identifying the campaign team</a> · <a href="https://www.ftvnews.com.tw/news/detail/2026A25W0161">October 25 report showing the later transparent enclosure</a>.</p><p>Its ship-themed pickup, deck, helm, mast, flags, speakers and later enclosure informed this LEGO interpretation. CL Kao adapted those visual features using the separately credited upstream pickup assembly; LEGO construction, proportions, attachment details, instructions and the DSS name are project adaptations. The original physical vehicle design is not claimed as our creation.</p><p>The individual vehicle designer and fabricator have <strong>not been independently identified</strong>. The collective campaign credit does not establish those roles; poster and graphic-design credits are separate. The original physical design is excluded from our CC BY-SA grant. <a href="physical-vehicle-attribution.json">Reference record and verification status</a>.</p></section>'''
credit=credit.replace('<div class="flow">',physical_credit+'<div class="flow">',1)
credit=credit.replace('<h1>What came from where</h1>',f'<h1>What came from where</h1><section id="contributors"><h2>{creator_count} credited creators — minifigure edition</h2><p>{len(ldraw_creators)} LDraw authors · {len(other_upstream)} other upstream creators · {len(project_creators)} project creator. This counts named people or public creator identities across the sources, including CL Kao; it is not a count of direct collaborators.</p><p>One further LDraw attribution is to the administrative account <strong>PTadmin</strong>. Unnamed contributors behind the campaign and software libraries are credited collectively and are not included in the people count. <a href="contributor-count.json">Count and source list</a>.</p></section>')
credit=credit.replace('<h1>What came from where</h1>','<h1>What came from where</h1><p><a href="technic/credits.html">Technic edition sources and contributors</a></p>')
(O/'credits.html').write_text(credit)
art=O/'tsai-banner';art.mkdir(exist_ok=True)
for p in(H/'accessories/tsai-banner').iterdir():
    if p.is_file():shutil.copyfile(p,art/p.name)
shutil.copyfile(D/'jacket-print.png',art/'jacket-print.png')
with zipfile.ZipFile(O/'sticker-artwork.zip','a',zipfile.ZIP_DEFLATED)as z:
    for p in art.iterdir():z.write(p,'tsai-banner/'+p.name)
print_guide=single_print_pdf(O)
for n in ['viewer.html','index.html']:
    text=(O/n).read_text().replace('Minifigure edition · local preview','Minifigure edition · '+edition)
    (O/n).write_text(text)
evidence=O/'review-evidence';evidence.mkdir(exist_ok=True)
for n in ['catalog-connections.json','connected-prefixes.json','controls.json','repeat-recipes.json','six-direction-broadphase.json','sampled-carrier-approaches.json','surface-screen-controls.json','local-panel-check.json','viewer-performance.json','sweep-review.json','reflection-winding-check.json','artifact-review.json','cabin-render-check.json','cabin-orbit-comparison.jpg','cabin-fixed.png']:
    if(E/n).exists():shutil.copyfile(E/n,evidence/n)
shield=R/'output/yangliu-shield-prototype/retained-rails/engineering'
for n in ['panel-approaches.json','mount-stud-sections.json','wheel-side-gate-control.json']:shutil.copyfile(shield/n,evidence/('shield-'+n))
review=f'''# {edition} digital review

{count} rigid pieces, {steps} main steps, {len(m['build_operations'])} assembly operations. The plan introduces each rigid part once and preserves the accepted 338-piece vehicle/enclosure poses. The optional 小英 scene adds {count-338} pieces beside the vehicle.

Catalog geometry resolves all {count} occurrences. Connector metadata is complete for {conn['summary']['coverage']['complete']} and partial for {conn['summary']['coverage']['partial']}. Confirmed and potential contacts are distinguished in the report; {conn['summary']['pieces_without_reported_contact']} occurrences have no reported contact. Missing metadata is unresolved evidence, not proof of a floating part or measured physical grip.

All {prefix['nonempty_operations']} nonempty construction prefixes have {prefix['temporal_graph_findings']} future-connection order findings against the final catalog graph. Repeated recipes use exact mesh comparisons; full mirrored side carriers are not falsely labelled identical. The old isolated step-21 slope is retained as a negative control.

Six-direction swept-box screening covers every non-seed operation. Actual mesh sampling covers both side carriers and the rear bed from all six directions. The rear trim is installed after the bed to remove its earlier insertion obstruction. Near-seat surface witnesses remain; see sweep-review.json for limits. These finite samples do not certify continuous solid collision freedom.

Shield installation: mounting plates, complete helm including wheel, two side panels held one plate high and slid inward before lowering, front panel, outboard rails, then flags. Straight lowering beside the helm and installing the wheel afterward fail the negative controls. Compound-path samples and 14 stud sections support the illustrated sequence. Cab/front clearance is nominal, not a measured manufacturing allowance.

Figures arrive preassembled and are placed last. 小英 holds one two-sided flag and stands beside the vehicle without a display plate. Hand/bar alignment and flag clips have catalog evidence; hair, printed-paper fit and real grip still require a dry-fit.

No physical load, stiffness, suspension response, hand access, grip or handling strength has been tested. Support the chassis; do not lift by the enclosure, helm or mast. These LEGO panels represent the vehicle's shields visually; no protective capability is claimed.
'''
(O/'digital-fit-audit.md').write_text(review)
prov=load(B/'release-provenance.json');prov.update(revision=m['revision'],model_sha256=sha(D/'model.json'),accepted_source_sha256=m['instruction_source_sha256'],accepted_shield_source_sha256=m['accepted_refinement']['shield_source_sha256'],rigid_pieces=count,public_steps=steps,pdf_pages=check['pdf_pages'],procurement_units=mapping['purchase_units'],purchase_lots=mapping['purchase_lots'],manufactured_part_colors_verified=mapping['validation']['all_part_color_combinations_verified'],presentation_revision=label,catalog_notices='Readable credits, per-file notices and exact source copies included.',physical_tested=False)
prov.pop('audited_candidate_sha256',None)
prov.update(display_name='DSS Taipei Current',ship_prefix='DSS',ship_prefix_expansion='Democratic Service Ship',ship_prefix_scope='A project-created civic prefix for the fictional ship theme.')
if 'copyright_status'in prov:prov['copyright_status']=re.sub(r'\bdonor\b','upstream',prov['copyright_status'],flags=re.I)
prov['credited_creator_identities']=creator_count
prov['physical_vehicle_reference']=physical_vehicle
prov['print_download']=print_guide
prov['technic_preview']=dict(url='technic/',status='work in progress',link_location='footer gear easter egg')
prov['display_animation']=dict(default=True,tires='Four tire-and-rim pairs rotate together; helm stays still.',figures='Candidate waves; 小英 walks in place with a fixed heading.',flags='Rigid clip flags sway; no cloth deformation.',camera='Slow orbit, suspended after manual interaction.',instructions='Canonical static poses; motion pauses during building.',performance='30 fps presentation; no scene rebuilds or geometry allocations per animation frame; pauses offscreen and respects reduced motion.')
prov.update(contribution_license='CC-BY-SA-4.0',license_scope='Original contributions and adaptations only; third-party rights excluded. See LICENSE.txt and credits.html#license.',meme_attribution='AYA／AYA全糖腐女中心 (@theaya1108); custom banner layout adapted by CL Kao.')
prov['files']={n:sha(O/n)for n in prov['files']if(O/n).exists()}
for n in ['model.json','instruction-plan.json','LICENSE.txt','licenses/CC-BY-SA-4.0.txt','tsai-banner/meme-attribution.json','contributor-count.json','physical-vehicle-attribution.json']:
    if(O/n).exists():prov['files'][n]=sha(O/n)
(O/'release-provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
(O/'README.txt').write_text('DSS Taipei Current / '+edition+': open viewer.html in a current browser. DSS means Democratic Service Ship, a project-created civic prefix. The model, part-tray thumbnails and rendering code are embedded for offline viewing. Other local links open the PDF, inventory, source credits, print sheets and review evidence. BrickLink requires pasting/uploading the XML and verifying it. Physical tests remain open.\n')
(O/'README.txt').write_text((O/'README.txt').read_text()+'The real-world 洋流號 is credited collectively to the Shen Po-yang campaign team and contributors. Its individual designer and fabricator remain unverified; see credits.html#physical-vehicle and physical-vehicle-attribution.json.\n')
# Keep tool inputs and artwork with the readable package; no claim that the
# external Python/LDraw dependency environment is bundled.
with zipfile.ZipFile(O/'release.zip','w',zipfile.ZIP_DEFLATED)as z:
    for p in sorted(O.rglob('*')):
        rel=p.relative_to(O)
        if p.is_file()and rel.parts[0]not in ['release.zip','package-manifest.json','index.html']and not any(x.startswith('.')for x in rel.parts):z.write(p,rel.as_posix())
    for n in ['compile_full_instructions.py','make_full_instruction_pdf.py','prepare_refined_source.py','prepare_tsai_prototype.py','tsai_bubble_artwork.py','preview.js','preview_motion.js','build_preview.mjs','viewer_panel.html','viewer_panel.css','check_full_instructions.py','check_preview_motion.mjs','static_release_assets.py','review_connected_sequence.py','mesh_approach_screen.py']:
        z.write(H/n,'rebuild-reference/'+n)
    z.write(a.source/'model.json','rebuild-reference/source-model.json')
manifest=dict(revision=m['revision'],presentation_revision=label,index_bytes=(O/'index.html').stat().st_size,files={p.relative_to(O).as_posix():sha(p)for p in O.rglob('*')if p.is_file()and p!=O/'package-manifest.json'})
(O/'package-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if not a.github_pages:assert all(sha(p)==sha(O/'technic'/p.relative_to(B/'technic'))for p in(B/'technic').rglob('*')if p.is_file())
print(json.dumps(dict(out=str(O),pieces=count,steps=steps,pdf_pages=check['pdf_pages'],direct_parts=len(rows),credited_creators=creator_count,ldraw_author_entries=len(authors),source_files=len(cat['attribution']),offline_bytes=(O/'release.zip').stat().st_size),indent=2))

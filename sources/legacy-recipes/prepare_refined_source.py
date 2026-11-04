"""Combine the accepted shield configuration and the separate 小英 accessory.

Keeps the accepted 338 vehicle occurrences exact. The new figure stands beside
the vehicle; it does not require a larger or crowded second-person platform.
"""
import argparse,copy,hashlib,json,subprocess,sys
from collections import Counter
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;R=H.parents[1]
sys.path.insert(0,str(R/'scripts'))
from lego_ldraw import write_exports
from lego_instruction_plan import renumber
S=H/'accessories/shields/accepted-retained-rails-v1'
T=R/'output/yangliu-tsai-prototype'
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=H/'prototypes/refined-v8');ap.add_argument('--without-display-base',action='store_true');ap.add_argument('--catalog-library',type=Path);args=ap.parse_args()
D=args.out;D.mkdir(exist_ok=True)
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=load(S/'model.json');accept=load(S/'appearance-acceptance.json');assert accept['accepted']and accept['model_sha256']==sha(S/'model.json')
base=copy.deepcopy(m['pieces']);tsai=load(T/'model.json');shift=np.array([2.5,-5.,0])
for p in tsai['pieces']:
    if args.without_display_base and p['id']==410:continue
    p=copy.deepcopy(p);p['transform']['origin']=(np.array(p['transform']['origin'])+shift).tolist();p['module']='tsai';m['pieces'].append(p)
count=348 if args.without_display_base else 349
assert len(m['pieces'])==count and len({p['id']for p in m['pieces']})==count
for surface in tsai['extra_decal_surfaces']:
    surface=copy.deepcopy(surface);surface['vertices']=(np.array(surface['vertices'])+np.array([shift[0],shift[2],-shift[1]])).tolist();m['extra_decal_surfaces'].append(surface)
m['surface_artworks'].update(tsai['surface_artworks'])
m.update(revision='yangliu-refined-source-v9'if args.without_display_base else'yangliu-refined-source-v8',prototype=True,
    accepted_refinement=dict(shield_source_sha256=sha(S/'model.json'),appearance_acceptance=accept,
        tsai_source_sha256=sha(T/'model.json'),tsai_placement='Standing beside the vehicle without a display base.'if args.without_display_base else'Separate beside-vehicle display base; not a second figure inside the shield enclosure.',
        tsai_shift_studs=shift.tolist(),scope='Accepted shield appearance plus requested 小英 speech-bubble accessory; physical tests remain open.'),
    dimensions_note='Updated transparent enclosure with three matching panes; optional 小英 speech-bubble scene beside the vehicle.')
m['limits']+=tsai['limits']+['Instructions must install shield mounting plates before relocated rails and pane units before tall flags.']
m['assembly_roots']={mod:mod for mod in sorted({p['module']for p in m['pieces']})}
m['build_operations']=[dict(kind='build',module=mod,assembly=mod,ids=[p['id']for p in m['pieces']if p['module']==mod],direction='seed',section_name='Frozen source poses',placements=[])for mod in m['assembly_roots']]
renumber(m);raw=json.dumps(m,ensure_ascii=False,indent=2).encode();(D/'model.json').write_bytes(raw)
rt=write_exports(m,D,model_sha256=sha(D/'model.json'))
cat=load(H/'prototypes/final-fit-v6/catalog-meshes.json')
for path in[R/'output/yangliu-shield-prototype/retained-rails/addon/catalog-meshes.json',T/'catalog-meshes.json']:
    extra=load(path);assert extra['catalog_archive_sha256']==cat['catalog_archive_sha256']
    for key in['parts','attribution','licenses','colors']:cat[key].update(extra[key])
(D/'catalog-meshes.json').write_text(json.dumps(cat,separators=(',',':')))
if args.catalog_library:subprocess.run(['node',str(R/'scripts/build_lego_catalog.mjs'),str(D),str(args.catalog_library)],check=True)
(D/'prototype-summary.json').write_text(json.dumps(dict(revision=m['revision'],pieces=count,lots=len(Counter((p['part'],p['color'])for p in m['pieces'])),modules=dict(Counter(p['module']for p in m['pieces'])),mpd_roundtrip=rt),indent=2)+'\n')
(D/'source-provenance.json').write_text(json.dumps(dict(model_sha256=sha(D/'model.json'),accepted_shield_source_sha256=sha(S/'model.json'),
    tsai_source_sha256=sha(T/'model.json'),accepted_vehicle_occurrences_preserved=338,requested_extra_occurrences=count-338,
    source_artwork=tsai['surface_artworks'],mpd=rt,limits=m['limits']),ensure_ascii=False,indent=2)+'\n')
# The source graph is assembled from bound, unchanged-pose reports. Its gaps
# remain explicit; new figure/base interfaces are not invented as connections.
base_graph=load(H/'prototypes/final-fit-v6/catalog-connections.json')
local=load(R/'output/yangliu-shield-prototype/retained-rails/local-inspection/catalog-connections.json')if(R/'output/yangliu-shield-prototype/retained-rails/local-inspection/catalog-connections.json').exists()else None
sources=[base_graph]
for path in[R/'output/yangliu-shield-prototype/retained-rails/catalog-connections.json',T/'catalog-connections.json']:
    if path.exists():
        report=load(path)
        if report.get('contacts'):sources.append(report)
changed=set(load(S/'integration.json')['moved_helm_ids'])|set(load(S/'integration.json')['moved_rail_and_ring_ids'])
rows={tuple(sorted(c['piece_ids'])):c for c in base_graph['contacts']if not(changed&set(c['piece_ids']))}
for graph in sources[1:]:
    for c in graph['contacts']:rows[tuple(sorted(c['piece_ids']))]=c
(D/'catalog-connections.json').write_text(json.dumps(dict(schema='refined-source-connection-evidence/1',model_sha256=sha(D/'model.json'),
    contacts=list(rows.values()),scope='Merged catalog evidence only; moved interfaces use fresh shield report; explicit partial/missing metadata remains unresolved.',
    source_graphs=[str(p)for p in[H/'prototypes/final-fit-v6/catalog-connections.json',R/'output/yangliu-shield-prototype/retained-rails/catalog-connections.json',T/'catalog-connections.json']]),indent=2)+'\n')
print(json.dumps(dict(source=str(D),pieces=count,lots=len(Counter((p['part'],p['color'])for p in m['pieces'])),sha256=sha(D/'model.json')),indent=2))

from pathlib import Path
import json,hashlib,shutil,math
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[3];P=Path(__file__).parent;B=R/'builds/clear-logical/cycle2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for src,dst in [('browser-review/browser-check.json','browser-check.json'),('package/package-manifest.json','package-manifest.json')]:shutil.copyfile(B/src,P/dst)
runs={}
for folder in ['suspension-specimen','suspension-specimen2','representative','representative-fit','remaining','bed-final','bed-overhead','browser-review']:
 data=json.loads((B/folder/'run.json').read_text());runs[folder]={k:data[k] for k in ['exit','stop_reason','admission_free_bytes','min_free_bytes','elapsed_seconds']};assert data['exit']==0 and data['min_free_bytes']>=512*1024**2
(P/'runtime-evidence.json').write_text(json.dumps(runs,indent=2)+'\n')
checks=[]
for n,folder in [(5,'representative-fit'),(6,'remaining'),(7,'remaining'),(8,'remaining')]:
 t=json.loads((B/folder/'receiver-locations.json').read_text())[f's{n}-placement']['targets'];v=[[t[k+1]['x']-t[k]['x'],t[k+1]['y']-t[k]['y']] for k in [0,2]];cross=v[0][0]*v[1][1]-v[0][1]*v[1][0];assert abs(cross)<1e-7
 checks.append(dict(step=n,projected_direction_cross_product=cross,source_features='cycle1/features.json',offset_ldu=[0,0,-120 if n in [5,7] else 120],source_unchanged=True))
bed=json.loads((B/'bed-overhead/receiver-locations.json').read_text())['bed-placement'];errs=[]
for a,b in [(1,2),(3,4)]:
 x=bed['targets'][a]['world'];y=bed['targets'][b]['world'];e=math.dist([x[0],x[1]-6,x[2]],y);assert e<.00001;errs.append(e)
(P/'feature-check.json').write_text(json.dumps({'suspension':checks,'bed_operation':82,'bed_recipe_operations':[77,78,79,80,81],'bed_unit_ids':[14,33,34,54,58,59,100,109,118],'receiving_plates':[38,81],'visible_callout_plate':81,'rail_underside_to_plate_top_error_scene_units':errs,'bed_display_offset_ldu':[0,-120,0],'physical_insertion_verified':False},indent=2)+'\n')
# Same rendered page scale/compression. The left recipe and tray remain byte-identical pixels.
a=Image.open(B.parent/'cycle1/package/pages/page-36.jpg');b=Image.open(B/'package/pages/page-36.jpg');box=(0,0,520,849);d=ImageChops.difference(a.crop(box),b.crop(box));left_equal=d.getbbox() is None
(P/'author-visual-review.json').write_text(json.dumps({'category':'author visual review, independent review pending','A4_affected_pages_inspected':[10,12,14,16,36],'mobile_source_pixel_views_inspected':[10,36],'default_fit_detail_readability_claimed':False,'horizontal_scrolling_required':True,'human_device_testing':False,'page36_left_recipe_and_tray_pixels_equal':left_equal,'comparison_region_pixels':[0,0,520,849],'initial_530px_comparison':'JPEG differences only x527..529 y495..511 near changed callout boundary; excluded from exact recipe-content comparison','screenshots':{str(p.relative_to(B)):sha(p) for p in (B/'browser-review').glob('*.png')},'bounded_audit':{'30,32,33':'Existing carrier details have localized region boxes and recognizable receivers; unchanged.','34':'Wheel arches visibly emphasized in main state; no detached callout. Unchanged.','35':'Rear-bed recipe only; no placement callout. Unchanged.','37,38':'Direct construction panels with new-part emphasis, no detached callout. Unchanged.'}},indent=2)+'\n')
assert left_equal
versions={}
for label,folder in [('rejected-original','candidate'),('reviewed-cycle1','cycle1/package'),('successor-cycle2','cycle2/package')]:versions[label]={n:sha(B.parent/folder/n) for n in ['instructions.pdf','viewer.html','release.zip']}
(P/'version-bindings.json').write_text(json.dumps(versions,indent=2)+'\n')
html='<!doctype html><meta charset="utf-8"><title>DSS correction round 2</title><style>body{font:16px system-ui;background:#f7f4ee;margin:24px}section{display:grid;grid-template-columns:1fr 1fr;gap:16px}img{width:100%}h2{margin-top:40px}</style><h1>Correction round 2 — before / after</h1><p>Left: reviewed cycle1. Right: revised cycle2. Presentation changes only; independent review and captain acceptance pending.</p>'
for n in [10,12,14,16,36]:html+=f'<h2>Page {n}</h2><section><a href="../cycle1/package/pages/page-{n:02d}.jpg"><img src="../cycle1/package/pages/page-{n:02d}.jpg" alt="Before page {n}"></a><a href="package/pages/page-{n:02d}.jpg"><img src="package/pages/page-{n:02d}.jpg" alt="After page {n}"></a></section>'
(B/'before-after.html').write_text(html)
(P/'before-after.html').write_text(html.replace('../cycle1/package/', '../../../builds/clear-logical/cycle1/package/').replace('"package/', '"../../../builds/clear-logical/cycle2/package/'))
(P/'reference-check.json').write_text(json.dumps({'url':'https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6594968.pdf','pdf_sha256':sha(B/'lego-6594968.pdf'),'printed_page_inspected':14,'observation':'Local construction callout uses arrows into the receiving assembly area, with transparent context. Used as illustration of spatial correspondence; no layout or LEGO artwork copied into DSS package.'},indent=2)+'\n')
print('Recorded runs, feature correspondence, preserved versions, inspected views and exact left-recipe pixel equality.')

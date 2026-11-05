"""Compare retained page artwork at the same raster scale; discard each temporary raster."""
from pathlib import Path
import subprocess,json,time,shutil
from PIL import Image,ImageChops,ImageStat
R=Path(__file__).resolve().parents[2];B=R/'builds/clear-logical';O=B/'candidate';P=Path(__file__).parent
start=time.monotonic();rows=[];temp=B/'reuse-source';mapping=json.loads((O/'pdf-page-map.json').read_text())
for rec in mapping['page_records']:
 if not rec.get('unchanged_content') or rec['source_page'] in [24,26]:continue
 assert time.monotonic()-start<120 and shutil.disk_usage(R).free>300*1024**2
 n=rec['source_page'];subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-scale-to','1200','-jpeg','-jpegopt','quality=80',str(B/'simplification-package-retry1/instructions.pdf'),str(temp)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 with Image.open(str(temp)+'.jpg') as old,Image.open(O/'pages'/f"page-{rec['page']:02d}.jpg") as new:
  region=(0,0,old.width,old.height-65);diff=ImageChops.difference(old.crop(region),new.crop(region));stat=ImageStat.Stat(diff);rows.append({'old_page':n,'new_page':rec['page'],'exact_pixels_except_footer':diff.getbbox() is None,'mean_absolute_difference':stat.mean})
 Path(str(temp)+'.jpg').unlink()
result={'raster_long_edge':1200,'excluded_bottom_pixels':65,'reason':'Page numbers changed; carrier reference pages are reviewed separately.','pages':rows,'all_retained_artwork_pixel_identical':all(x['exact_pixels_except_footer'] for x in rows),'elapsed_seconds':time.monotonic()-start}
(P/'reuse-check.json').write_text(json.dumps(result,indent=2)+'\n');print(result['all_retained_artwork_pixel_identical'],len(rows))
assert result['all_retained_artwork_pixel_identical']

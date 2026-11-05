from pathlib import Path
import json
R=Path(__file__).resolve().parents[3];B=R/'builds/clear-logical';O=B/'cycle5/package';old=B/'cycle4/package'
s=(old/'viewer.html').read_text();a=s.index('const titles=')+len('const titles=');b=s.index(';const select=',a);titles=json.loads(s[a:b]);titles[26:33]=['17 Build lower carriers · 2x','17 Build long rails · 2x','17 Build short rails · 2x','17 Join the rails · left/right variants','17 Install the left side carrier','18 Install the right side carrier'];assert len(titles)==79
s=s[:a]+json.dumps(titles,ensure_ascii=False)+s[b:];(O/'viewer.html').write_text(s)
if (O/'index.html').is_symlink():(O/'index.html').unlink()
(O/'index.html').write_text(s)
mp=json.loads((old/'pdf-page-map.json').read_text());rows=[]
for oldn in range(1,81):
 if oldn==33:continue
 n=oldn if oldn<33 else oldn-1
 rows.append({'page':n,'source_page':oldn,'title':titles[n-1],'heading_restored':4<=oldn<=71,'changed_scene':oldn in [27,28,29,30,31,32,36],'unchanged_content':oldn<=3,'renumbered_footer':oldn>33})
mp.update(pages=79,page_records=rows,correction_round='captain-follow-up-cycle5',removed_source_pages=[33],reason='One shared method and two distinct placements replace redundant carrier join/placement composition.');(O/'pdf-page-map.json').write_text(json.dumps(mp,indent=2)+'\n')

"""Object-specific, complete 308-piece draft using the shared plan compiler.

75875 informs the frame/body staging only. Every piece is introduced here;
the reader is never sent to another manual for missing construction steps.
The upright house sequencer cannot certify these transformed Technic poses.
Explicit construction operations therefore retain that validation limit.
"""
import argparse,copy,hashlib,json,shutil,sys
from collections import Counter,defaultdict
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from lego_instruction_plan import renumber,compile_plan,recipe_frames
from lego_ldraw import write_exports
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--source',type=Path,default=H/'prototypes/base-75875/dark-orange')
ap.add_argument('--out',type=Path,default=ROOT/'output/yangliu-full-instructions-draft-v1')
ap.add_argument('--edition',default='Full build draft 1')
ap.add_argument('--connected-sides',action='store_true',help='Build supported side carriers off the chassis; reuse their matching running boards')
ap.add_argument('--compact-build',action='store_true',help='Use connected chassis/riser callouts and combine nearby authored construction operations')
ap.add_argument('--refine-build',action='store_true',help='Preassembled figures, repeated equipment batches and fewer small main steps')
ap.add_argument('--steady-views',action='store_true',help='Keep a stable main viewing direction through each working section')
args=ap.parse_args();SOURCE=args.source;OUT=args.out;OUT.mkdir(parents=True,exist_ok=True)
if args.refine_build:args.compact_build=True
if args.compact_build:args.connected_sides=True
source_raw=(SOURCE/'model.json').read_bytes();m=json.loads(source_raw)
m['instruction_source_sha256']=hashlib.sha256(source_raw).hexdigest()
m['instruction_edition']=args.edition
if args.connected_sides:m['revision']='yangliu-minifigure-test-build-v7'
if args.compact_build:m['revision']='yangliu-minifigure-test-build-v8'
if args.refine_build:m['revision']='yangliu-minifigure-test-build-v9'
if args.steady_views:m['revision']='yangliu-minifigure-test-build-v10'
if args.steady_views:
    m['render_depth_bias']={'2001':4,'2002':4}
    m['render_depth_bias_note']='Display-only tie break at the nominal plate/cab-pillar contact; no pose or physical clearance is changed.'
m['instruction_scope']=f"All {len(m['pieces'])} rigid parts, figures, equipment and sticker placement; no external construction steps."
pieces={p['id']:p for p in m['pieces']};ops=[];seen=set()
# Earlier preview prints had a module but no per-piece owner. Bind them before
# partial-step rendering so lamps and grille cannot float ahead of their parts.
for surface in m.get('extra_decal_surfaces',[]):
    ref={'headlamp-left':'148','headlamp-right':'161','grille':'147'}.get(surface['artwork'])
    if ref:
        target=next(p for p in pieces.values() if p.get('base_source',{}).get('lxf_ref')==ref)
        surface.update(piece_id=target['id'],module=target['module'])
report_path=SOURCE/'catalog-connections.json'
if not report_path.exists():report_path=H/'evidence/75875-connections.json'
report=json.loads(report_path.read_text())
evidence={tuple(sorted(c['piece_ids'])):c for c in report['contacts']}
adaptations=m.get('instruction_adaptations',{})
replacements={int(i):v for i,v in adaptations.get('replacement_parts',{}).items()}
repaired=bool(m.get('physical_audit')or m.get('accepted_refinement'))
shield=all(i in pieces for i in range(2001,2012))
band_description=m.get('suspension_band_description','two Red x37 medium round-section belts')
hood_wings=m.get('hood_alignment_revision',{}).get('orange_wings',[])
flag_color=m['colors'][pieces[302]['color']][2]
banner_color=m['colors'][pieces[266]['color']][2]
continuous_hood=any(s['name']=='hood-upper' for s in m.get('hood_sticker_sections',[]))
contents=defaultdict(set)
def build(ids,title,note='',*,module='truck',assembly=None,view='front',context=None,hold=None):
    # Revised trim pairs use the same mount step as the original smooth tile.
    # This is an instruction grouping rule; no geometry is changed here.
    fillers=m.get('hood_rope_revision',{}).get('trim_fillers',{})
    ids=[j for i in ids for j in ([i,int(fillers[str(i)])] if str(i) in fillers else [i])]
    ids=list(dict.fromkeys(j for i in ids for j in replacements.get(i,[i]) if j in pieces))
    if not ids:return
    assert ids and not(seen&set(ids)),('Duplicate introduction',ids,seen&set(ids))
    assert all(pieces[i]['module']==module for i in ids),(title,ids,module)
    seen.update(ids);assembly=assembly or module
    contacts=[dict(piece_ids=list(pair),confirmed=row['confirmed'],potential=row['potential']) for pair,row in evidence.items()
              if set(pair)&set(ids) and set(pair)<=(contents[assembly]|set(ids))]
    op=dict(kind='build',module=module,assembly=assembly,ids=ids,direction='top',section_name=chapter,
            placements=[dict(ids=ids,direction='top',contacts=[])],catalog_pairs=contacts,
            manual=dict(title=title,note=note,view=view,context=context,hold=hold))
    ops.append(op);contents[assembly].update(ids);return op
def unit(module,recipes,title,note='',*,name=None,view='front',context=None,hold=None,repeat=None,prefix_repeat=None,recipe_view=None):
    child=name or module+'-unit'
    for ids,label in recipes:
        build(ids,label,module=module,assembly=child,view=recipe_view or view)
    ids=sorted(contents[child])
    op=dict(kind='join',module=module,assembly=module,child=child,ids=[],direction='top',section_name=chapter,
       instruction_component=True,placements=[dict(ids=ids,direction='top',contacts=[])],
       manual=dict(title=title,note=note,view=view,context=context,hold=hold))
    if repeat:
        group,index,count=repeat;op.update(repeat_group=group,repeat_index=index,repeat_count=count)
    if prefix_repeat:
        group,index,count,frames=prefix_repeat;op.update(repeat_prefix_group=group,repeat_prefix_index=index,repeat_prefix_count=count,repeat_prefix_frames=frames)
    ops.append(op);contents[module].update(ids)

chapter='01 / Chassis frame'
if args.compact_build:
    unit('truck',[([172,178],'Lay both long beams flat'),([150,163],'Tie both beams with the square plates'),
                  ([153,168,177],'Add the centre and front ties'),([173,179],'Fit both small round plates'),([134,164],'Cap the centre and frame ends')],
         'Build the chassis core','Start with both beams on the table. The next plates tie them together.',name='chassis-core',view='top')
else:
    build([172,178],'Lay out the two long chassis beams','Keep both beams on the table, parallel and two studs apart. The next plates tie them together.',view='top')
    build([150,163],'Tie the frame with the two square plates','Press each plate onto both long beams.',view='top')
    build([153,168,177],'Add the centre and front ties',view='top')
if not args.connected_sides:build([152,162],'Fit the rear frame brackets',view='rear')
if not args.compact_build:
    build([173,179],'Add the two small round plates',view='top')
    build([134,164]if args.connected_sides else[134,113,164],'Cap the centre and frame ends',view='top')
build([107,128],'Add the two rear longitudinal plates')
if args.connected_sides:
    build([152,162],'Fit the rear frame brackets','Attach both brackets to the longitudinal plates before adding the centre cap.',view='underside')
    build([113],'Tie the rear frame brackets',view='top')
    build([161],'Fit the lower rear bumper face',view='rear')
build([145,165],'Extend the longitudinal plates toward the front')
build([216,231],'Fit the two central suspension pins','Insert the pins from the side before the body covers this area.',view='underside')
chapter='02 / Suspension and underside'
for name,inner,pivot,pin,carrier,axle,ball,view in [
 ('Rear left',218,217,219,224,223,227,'rear'),('Rear right',230,226,225,241,240,242,'rear-other'),
 ('Front left',232,220,228,238,237,239,'front'),('Front right',245,234,233,246,248,247,'front-other')]:
    unit('truck',[([inner,pivot],name+' inner arm and pivot'),([pin,carrier],name+' outer arm'),([axle,ball],name+' wheel pin and ball pin')],
       name+' suspension unit','Match the pin direction shown. Hold the frame while fitting the arm; do not force a joint.',name=name.lower().replace(' ','-')+'-suspension',view='underside',
       hold='Check band retention and wheel travel with real bricks. Fit '+band_description+' after all four suspension units.' if repaired else 'Suspension travel and elastic-band routing have not been test-built.')
if m.get('suspension_bands'):
    ops.append(dict(kind='build',module='truck',assembly='truck',ids=[],direction='top',section_name=chapter,placements=[],
        manual=dict(title='Fit the two suspension bands',note='Use '+band_description+'. Under the chassis, loop one around towballs #227 and #239; loop the other around #242 and #247. Keep each loop on its own side. Fit before the wheels.',
        view='underside',context=None,focus_ids=sorted(contents['truck']),hold='Routing follows the reference suspension. The colored curves are routing guides; band tension, retention and loaded travel need a real-brick check.',accessory=True,bands_installation=True,catalog_accessory=band_description)))
build([171,181],'Fit the two rear underside dishes','Turn the chassis over for underside work.',view='underside')
build([204,188,191],'Fit the remaining underside dishes',view='underside')
build([169,190],'Add the rear socket plate and front lower tie',view='underside')
build([183,184,182],'Build the front lower bracket course',view='underside')
build([187,189],'Fit the two lower front slopes',view='underside')
if not args.connected_sides:build([119,120,206,214],'Add the rear lower trim and bushes',view='rear')
if not args.connected_sides:
    build([117,197,140],'Fit the left running-board slopes',view='front')
    build([176,205,185],'Fit the right running-board slopes',view='front-other')
    build([97,98,116],'Cap the left running board')
    build([158,157,167],'Cap the right running board',view='front-other')
if not args.connected_sides:
    build([101,102],'Fit the rear bumper cross strips',view='rear')
    build([192,196,195,202],'Add the rear clip and plate layer',view='rear')
    build([194,203,1,2],'Finish the rear bumper corners',view='rear')
    build([198,161],'Add the rear plate tile and bumper face',view='rear')
build([215,229,170],'Finish the lower front bumper')
chapter='03 / Floor and lower body'
build([99,129],'Install both floor plates','Return the chassis to studs-up orientation. Support it underneath while pressing the plates.',view='top')
if args.connected_sides:
    build([106,110,155,159],'Add the lower rear spacer course',view='underside')
    build([103,104,139,146],'Add the rear round spacer plates',view='underside')
    build([154,160,180,186],'Add the lower front spacer course',view='underside')
    build([135,148,174,175],'Add the front round spacer plates',view='underside')
else:
    build([103,104,139,146],'Add the rear round spacer plates',view='top')
    build([106,110,155,159],'Add the lower rear spacer course',view='top')
    build([135,148,174,175],'Add the front round spacer plates',view='top')
    build([154,160,180,186],'Add the lower front spacer course',view='top')
build([75,90,94],'Build the rear bed and centre floor')
build([131,133],'Add the two front floor plates',view='top')
build([63,111,91,151],'Add the four narrow floor supports',view='top')
if not args.connected_sides:
    build([96,115],'Fit the left lower-body brackets')
    build([156,166],'Fit the right lower-body brackets',view='front-other')
if not args.connected_sides:
    build([100,109,118],'Fit the rear cross brackets',view='rear')
    build([59,33],'Build the rear bed plate courses',view='rear')
chapter='04 / Body sides and wheel arches'
if args.connected_sides:
    for index,label,trim,lower,slopes,caps,upper,rails,remaining,view in [
        (1,'left',97,[96,115],[117,197,140],[98,116],[39,46],[38,331],[42,41,48],'front'),
        (2,'right',158,[166,156],[185,205,176],[167,157],[82,87],[333,81],[93,89,83],'front-other')]:
        recipes=[([trim],'Start with the orange running-board plate'),(lower,'Fit the two lower brackets'),
                 (slopes,'Fit the three black side slopes'),(caps,'Fit the orange end caps'),
                 (upper,'Add the two upper mounting brackets'),(rails,'Tie the brackets with the two top rails'),
                 (remaining,'Complete the side carrier')]
        unit('truck',recipes,'Install the '+label+' side carrier',
             'Build this carrier separately, then lower it onto both floor supports. Align the two attachment points before pressing.',
             name=label+'-side-carrier',view=view,context=['truck'],prefix_repeat=('Running boards',index,2,4),
             hold='Support the chassis underneath. The complete side carrier must be attached before adding its outer body panels.')
else:
    build([34,42,39],'Fit the rear-left upright brackets',view='rear')
    build([41,46,48],'Fit the front-left upright brackets')
    build([54,83,87],'Fit the rear-right upright brackets',view='rear-other')
    build([89,82,93],'Fit the front-right upright brackets',view='front-other')
    build([38,81],'Tie both body sides with long plates',view='top')
build([24,77],'Fit the rear white wheel arches',view='rear')
build([69,141],'Fit the front white wheel arches')
if args.connected_sides:
    unit('truck',[([33],'Start with the rear bed plate'),([59],'Fit the plate under the bed'),
                  ([100,109,118],'Fit the three rear cross brackets'),([34,54],'Fit both rear corner brackets'),
                  ([14,58],'Tie the bed with both long rails')],
         'Install the rear bed','Lower both long rails onto the side carriers and rear wheel arches.',
         name='rear-bed',view='rear',context=['truck'],recipe_view='rear')
    build([206,214],'Fit the two round rear trims','Fit these after the rear bed. They obstruct the bed brackets if installed earlier.',view='rear')
    build([119,120],'Fit the rear lower bumper strips',view='rear')
    build([101,102],'Fit the rear bumper cross strips',view='rear')
    build([192,196,195,202],'Add the rear clip and plate layer',view='rear')
    build([194,203,1,2],'Finish the rear bumper corners',view='rear')
    build([198],'Fit the rear plate tile',view='rear')
build([36,44,51],'Add the left side-facing backing plates')
build([35,45,49],'Fit the left curved and sloped panels')
build([37,43,50],'Finish the left narrow side tiles')
build([40,47],'Fit the left door and front side tiles')
build([61,84,108],'Add the right side-facing backing plates',view='front-other')
build([60,86,105],'Fit the right curved and sloped panels',view='front-other')
build([68,85,112],'Finish the right narrow side tiles',view='front-other')
build([88,92],'Fit the right door and front side tiles',view='front-other')
build([27,80,26,79],'Build the rear arch cap layers',view='rear')
build([25,78],'Fit the rear rope rings and trim' if m.get('hood_rope_revision') else 'Tile the rear arch caps','Face the closed rings outward, with their holes running along the truck. Fill the remaining stud with the Dark Orange tile.' if m.get('hood_rope_revision') else '',view='rear')
build([72,144,71,143],'Build the front arch cap layers')
build([70,142],'Fit the front rope rings and trim' if m.get('hood_rope_revision') else 'Tile the front arch caps','Use the low, outward-facing rings and retain the smooth orange trim. Leave the holes accessible for threading.' if m.get('hood_rope_revision') else '')
build([15,57]if args.connected_sides else[14,58,15,57],'Cap the rear side rails'if args.connected_sides else'Tie the rear side rails into the bed',view='rear')
build([32,76],'Extend the upper side supports')
build([10,64],'Add the upper body-side strips')
if not args.connected_sides:build([16],'Tie the rear cab floor')
build([12,67,13,66],'Fit the door and front-corner slopes')
build([9,53],'Fit the narrow upper side plates')
chapter='05 / Tailgate and front body'
unit('truck',[([209,208,211],'Lay out the tailgate backing plates'),([210,213],'Fit the two handles'),([207,212],'Finish the two tailgate strips')],
 'Fit the rear tailgate','Bring the handles to the rear clips and check their movement.',name='tailgate',view='rear',hold='Tailgate hinge insertion and clearance remain a test-build check.')
build([114,73],'Build the front body core')
build([127,149,124,137],'Add the front corner supports and lights')
build([95,125,138],'Fit the front face brackets')
if not args.connected_sides:build([126,147],'Fit the two inverted front corner slopes')
build([121],'Install the front central body brick')
build([123,136],'Fit the two black front supports' if m.get('front_revision') else 'Fit the two headlamp slopes')
if args.connected_sides:build([126,147],'Fit the two inverted front corner slopes')
if m.get('front_revision'):
    build([122],'Fit the front grille backing plate')
    build([309,310,311,312],'Build the slatted front grille','Use four grille tiles; no grille sticker is required.')
    build([317,318,319,314],'Finish the left curved bumper and clear headlight','Mount the clear 1 x 1 tile directly on the support, flush with the lower black tile.')
    build([320,321,322,316],'Finish the right curved bumper and clear headlight','Mirror the rounded outer edge. Both clear lenses sit at the same height.',view='front-other')
else:build([122],'Fit the plain front grille tile','The custom grille print has no Ford wordmark.')
build([55,30,52],'Build the hood support layer')
build([28,31],'Tie the rear edge of the hood supports')
chapter='06 / Cabin and figures'
build([56,62,130,132],'Fit the interior slopes')
if args.connected_sides:build([16],'Tie the rear cab floor')
build([74,193,201],'Fit the dashboard support and grille tiles')
build([199,200],'Assemble the steering stand and wheel','Match the wheel angle shown; check free movement before closing the cab.')
build([287],'Fit the cabin seat',module='interior',context=['truck'],hold=('Seat-to-floor alignment is checked digitally. The optional driver is omitted; retain the seat and controls.' if m.get('driver_revision',{}).get('included') is False else 'Seat-to-floor alignment is checked digitally. Test the seated driver and hand clearance before closing the cabin.') if repaired else 'The seat position is not confirmed by the connector report. Review its floor-stud alignment before pressing it in; do not force it.')
if any(p['module']=='driver' for p in pieces.values()):
    unit('driver',[([272,273],'Driver legs and torso'),([274,275],'Fit both driver arms'),([276,277],'Fit both driver hands'),([278,279],'Driver head and hair')],
     'Seat the driver','Use the seat and check the steering-wheel and windscreen clearance.',view='figure',context=['truck','interior'],hold='The driver-to-seat location is a trial fit. Confirm seating and headroom before adding the windscreen.')
def candidate_recipe():
    if args.refine_build:
        build([i for i,p in pieces.items()if p['module']=='candidate'],'Candidate minifigure','Preassembled.',module='candidate',view='figure',context=[])
        ops[-1]['manual'].update(preassembled=True,unit_name='candidate minifigure')
        return
    unit('candidate',[([255,256],'Candidate legs and printed torso'),([257,258,259,260],'Fit both arms and hands'),([261,262],'Fit the glasses head' if 261 not in pieces else 'Scarf and glasses head'),([263],'Short black hair')],
     'Complete the candidate minifigure','Fit the Dark Blue arms, Yellow hands, glasses head and short black hair. Keep the spare limbs from the purchased torso.' if repaired else 'Hair 98385 is the user-approved shorter style.',view='figure',context=[])
if not args.connected_sides:candidate_recipe()
build([11,65],'Build the two rear cab pillars','Use two standard 1 x 2 bricks per pillar.' if replacements else '')
build([6,8,22,23],'Fit the four transparent cab side panels','Keep the cabin open above while fitting these panels.')
build([19,20,21],'Tie the rear cab frame')
build([18,17],'Cap the rear cab frame')
build([7],'Fit the dedicated vehicle windscreen','Keep the glazing clear of the dashboard while pressing it down.' if m.get('driver_revision',{}).get('included') is False else 'Check that the driver clears the glazing before pressing it down.')
build([4,3],'Complete the front roof support')
build([29],'Fit the '+m['colors'][pieces[29]['color']][2]+' hood shell',module='hood',context=['truck','interior','driver'])
if 334 in pieces:
    build([334]+hood_wings,'Fit the white centre tile and orange wings' if hood_wings else 'Fit the white tile beside the windscreen','Snap the white 2 x 2 tile onto the hood rear centre studs. Add a Dark Orange 1 x 2 tile on each side, at the same height. Keep the original curved hood shell.' if hood_wings else 'Snap the white 2 x 2 tile onto the hood rear centre studs. Keep the original curved hood shell.',module='hood',context=['truck','interior','driver'])
build([5],'Fit the removable white cab roof',module='cab-roof',context=['truck','hood','interior','driver'])
chapter='07 / Road wheels'
for index,(rim,tyre,label,view) in enumerate([(221,222,'rear-left','rear'),(243,244,'rear-right','rear-other'),(235,236,'front-left','front'),(249,250,'front-right','front-other')],1):
    unit('truck',[([rim],'Wheel rim'),([tyre],'Fit the tyre around the rim')],
      'Fit the '+label+' wheel','Build four matching rim-and-tyre units. Align each rim with its wheel pin; do not bend the suspension to force it on.',
      name=label+'-wheel',view=view,repeat=('Wheels',index,4),hold='Wheel-pin grip, tyre clearance and suspension motion remain physical checks.')
    if args.compact_build:
        ops[-1]['instruction_batch']='all-road-wheels'
        ops[-1]['manual'].update(title='Fit all four completed wheels',view='rear',unit_name='wheel')
chapter='08 / Rear platform and helm'
stage_additions=[a['piece_id'] for a in adaptations.get('additions',[]) if a.get('after') in [280,281,282,283]]
if args.compact_build and len(stage_additions)==4:
    for index,(base,cap)in enumerate(zip([280,281,282,283],stage_additions),1):
        unit('truck',[([base],'Start with one black 2 x 2 plate'),([cap],'Stack the second plate')],
             'Fit the four platform risers','Make four matching two-plate stacks. Fit them to the bed before adding the platform.',
             name=f'platform-riser-{index}',view='rear',repeat=('Platform risers',index,4))
        ops[-1]['instruction_batch']='all-platform-risers';ops[-1]['manual']['unit_name']='platform riser'
else:
    build([280,281,282,283],'Install the four platform risers','Fit the risers to the bed before adding the removable platform.',view='rear')
    if stage_additions:build(stage_additions,'Cap the four platform supports','Keep the support layers level; the extra height clears the bed structure.',view='rear')
build([284],'Fit the tan rear platform','Check engagement at all four risers.',module='deck',context=['truck'],view='rear')
if shield:build([2001,2002],'Fit the white enclosure mounting plates','Fit both plates before the outboard rails.',module='shield',context=['deck'],view='rear')
if not shield:build([285,286],'Fit the two white nautical rails',module='deck',context=['truck'],view='rear',hold='The shorter rails align with the deck studs and clear the cab. Test retention before handling the removable platform.' if repaired else 'Rail mounting is not confirmed. This draft records the target position; attachment supports still need review.')
helm_recipes=[([251],'Helm base plate'),([252],'Fit the helm pedestal')]
for extra in adaptations.get('additions',[]):
    if extra.get('module')=='helm' and extra.get('before')==253:helm_recipes.append(([extra['piece_id']],'Fit the helm bearing spacer'))
helm_recipes += [([253],'Fit the Technic bearing brick')]
helm_recipes.append(([254],'Fit the ship wheel'))
unit('helm',helm_recipes,
    'Fit the helm console','Check that the wheel turns without touching the cab.',view='rear',context=['deck'],hold='The spacer and bearing are digitally aligned. Test the ship-wheel fit and rotation before fitting the figure.' if repaired else 'The bearing-to-pedestal joint needs review. Do not force the bearing into the illustrated pose.')
if shield:
    def shield_unit(index,ids,title):
        unit('shield',[([ids[0]],'White lower strip'),([ids[1]],'Fit the clear panel'),([ids[2]],'Fit the white top cap')],
             title,'Make three matching units. Fit the two sides first; keep the third for the front.',
             name=f'shield-panel-{index}',view='rear',repeat=('Clear shield panels',index,3))
        ops[-1]['manual']['unit_name']='shield panel'
    for index,ids in[(1,[2003,2006,2009]),(2,[2004,2007,2010])]:
        shield_unit(index,ids,'Fit both side shield panels')
        ops[-1]['instruction_batch']='side-shield-panels'
    ops[-1]['manual'].update(note='Keep each side panel one plate high. Slide inward from outside, then lower onto the studs. Keep the third panel for the front.',
        approach_specs=[dict(title='Hold the sides outside, one plate high',offsets=[dict(ids=[2003,2006,2009],ldraw=[0,-8,-80]),dict(ids=[2004,2007,2010],ldraw=[0,-8,80])]),
                        dict(title='Slide inward, then lower onto the studs',offsets=[dict(ids=[2003,2006,2009],ldraw=[0,-8,0]),dict(ids=[2004,2007,2010],ldraw=[0,-8,0])])])
    shield_unit(3,[2005,2008,2011],'Fit the remaining front shield panel')
    ops[-1]['manual']['note']='Use the third panel made earlier. Fit it before adding the tall flags.'
    build([285,286],'Fit the two outboard nautical rails','Fit the rails after the panels, on the outer row of mounting studs.',module='deck',context=['truck','shield'],view='rear',hold='Support the platform while pressing the rails; check their grip with real parts.')
chapter='09 / Speakers'
for index,mod,ids in [(1,'speaker-left',[288,289,290,291,292,293]),(2,'speaker-right',[294,295,296,297,298,299])]:
    base,a,b,cone1,cone2,cap=ids
    unit(mod,[([base],'Speaker base plate'),([a,b],'Fit both side-stud bricks'),([cone1,cone2],'Fit both speaker cones'),([cap],'Fit the smooth top tile')],
       'Mount the '+('left' if index==1 else 'right')+' roof speaker','Build two matching speaker units, then fit them to the roof studs.',
       context=['cab-roof'],repeat=('Speakers',index,2),hold='The cones are aligned to the side studs. Their socket fit has geometry support but still needs a fitting check.' if repaired else 'The small cone-to-side-stud alignment is not confirmed. Check the cone seating before mounting the speaker.')
    if args.refine_build:
        ops[-1]['instruction_batch']='both-speakers'
        ops[-1]['manual'].update(title='Fit both roof speakers',unit_name='speaker',view='front',note='2×')
chapter='10 / Larger triangular flag'
build([300],'Fit the mast foot plate',module='sail',context=['cab-roof'])
build([307,308],'Stack the two round mast supports',module='sail',context=['cab-roof'],hold='The support seating offset is corrected. Check full engagement during the test build.' if repaired else 'The digital support stack has a small seating offset. Confirm full stud engagement during fitting.')
build([301],'Insert the constant-diameter mast bar','Use the bar stop at the support. This is the 4095 bar, not the tapered antenna.',module='sail',context=['cab-roof'],hold='Bar seating and clip grip have not been measured.')
unit('sail',[([302,303],'Lay out the two '+flag_color+' wedge plates'),([304],'Tie both wedges with the smooth 2 x 2 tile'),([305,306],'Fit both clips behind the wedges')],
    'Clip the flag to the mast','The pointed end faces the rear. Keep the flag clear of both speakers.',name='sail-panel',context=['cab-roof','speaker-left','speaker-right'],
    hold='The clip axes are vertical and aligned with the mast. Fit the horizontal-clip plates shown; grip and insertion still need a physical check.' if repaired else 'Clip/socket locations are matched geometrically; the full insertion and grip still need a physical fitting check.')
chapter='11 / Rear banner and life rings'
if m.get('banner_mast_revision'):
    mast_revision=m['banner_mast_revision']
    mast_mount=mast_revision.get('mount_build_order',[264,341])
    if 264 not in mast_mount:mast_mount=[264]+mast_mount
    build(mast_mount,'Fit the rear mast foot and open-stud collar',mast_revision.get('mount_note','Seat the white round collar on the deck stud shown. Keep its centre hole clear.'),module='banner',context=['deck'],view='rear')
    build([265],'Insert the black rigid-hose mast',f"Use the factory {mast_revision.get('factory_length_studs',11)}-stud rigid hose, with constant diameter along its length. Insert it into the open-stud collar; do not substitute the tapered antenna.",module='banner',context=['deck'],view='rear',hold='Confirm the bottom grip and mast stiffness with real parts.')
else:
    build([264,265],'Build the rear banner mast',module='banner',context=['deck'],view='rear')
build([267,266],'Clip both '+banner_color+' flags to the rear mast','Both flags trail toward the rear. Apply one character to each panel.',module='banner',context=['deck'],view='rear',hold='All four clip positions align with the constant-diameter mast. Test grip and handling with real parts.' if m.get('banner_mast_revision') else 'Flag clips on the tapered antenna are not confirmed by the connector report. Check the fit before handling the model.')
for index,(mod,ids,view) in enumerate([('ring-left',[268,269],'rear'),('ring-right',[270,271],'rear-other')],1):
    unit(mod,[([ids[0]],'Life-ring mount'),([ids[1]],'Fit the red life ring')],
      'Position the '+mod.replace('-',' '),'Clip the mount to the white rail, then hang the life ring.' if repaired else 'Match the outside of the bed rail shown.',view=view,context=['deck'],repeat=('Life rings',index,2)if args.connected_sides else None,hold='The mount-to-rail connection is digitally aligned. Test clip grip before moving the platform.' if repaired else 'The life-ring mount does not yet have a confirmed attachment to the truck. Keep it separate until its mount is resolved.')
    if args.refine_build:
        ops[-1]['instruction_batch']='both-life-rings'
        ops[-1]['manual'].update(title='Fit both life rings',unit_name='life ring',view='rear',note='2×')
chapter='12 / Stickers and launch configuration'
def accessory(title,note,focus,view='front',art=None,place_figures=False):
    op=dict(kind='build',module='truck',assembly='truck',ids=[],direction='top',section_name=chapter,placements=[],
      manual=dict(title=title,note=note,view=view,context=None,hold=None,accessory=True,focus_ids=[i for i in focus if i in seen],art=art,place_figures=place_figures))
    ops.append(op)
hood_note=('Use two clear films. H1 carries the whole upper character across the white centre tile and both level orange side tiles; do not cut at the internal tile seams. H2 carries the lower character and its straight white strip on the curved hood. Keep the two films separate at the change in surface height.' if continuous_hood else 'Use the four numbered clear sections. Put the upper lettering on the white tile and the two orange side tiles with the small overflow sections; put the lower lettering and straight white strip on the curved hood. Align the strokes and keep film clear of the raised tile seam; do not bridge the part seams.') if 334 in pieces else ('Use the straight white strip and dark vertical lettering. Leave the sides clear so the Dark Orange hood shows through; keep the sticker clear of the rear studs.' if m.get('hood_artwork_transparent') else 'Use the coral field, irregular white band and dark vertical lettering. Keep the sticker on the smooth face of the single hood shell, clear of the rear studs.')
accessory('Apply the hood sticker',hood_note,[29,334]+hood_wings if 334 in pieces else [29],art='hood')
if not m.get('front_revision'):accessory('Apply the two headlamp stickers and grille print','Use one sticker per sloped headlamp part and one on the single smooth grille tile. Do not bridge seams.',[121,122,123,136],art='front')
banner_note='Upper panel: 洋. Lower panel: 流. Apply separate stickers to both sides, clear of the clips. '
banner_note+=('The white flags carry printed Reddish Orange backgrounds, straight white strips and dark lettering.' if m.get('printed_color_backgrounds') else 'Print only the white strip and dark lettering; the clear sides use the flag part color.')
accessory('Apply the individual banner stickers',banner_note,[265,266,267],view='rear',art='banner')
accessory('Apply the triangular flag tile sticker','Use only the white SOON/順 emblem on clear film; the '+flag_color+' tile supplies the background. Place it on the single smooth 2 x 2 tile, clear of the wedge seam.',[301,302,303,304,305,306],art='sail')
accessory('Fit the dangling decorative cord','Thread about 0.6 mm cream craft cord through rings #25, #70, #142, then #78. Route the front outside the bumper. Tie the end knots after threading and leave slack between rings; cut extra for knots and trim after fitting. Keep clear of the wheels and lamps.' if m.get('hood_rope_revision') else 'Tie the craft cord to the chosen attachment points. Let it sag between them. Keep it clear of the wheels and front lamps.',list(pieces),view='front',art='cord')
if args.connected_sides:
    chapter='13 / Figures and final placement'
    candidate_recipe()
if 400 in pieces:
    recipes=[([410],'Start with the display base'),([400,401],'Fit legs and jacket torso'),([402,403],'Fit both arms'),
                 ([404,405],'Fit both hands'),([406,407],'Fit the glasses head and short bob'),([408],'Fit the hand-held bar'),([409],'Clip on the two-sided speech bubble')]
    if args.refine_build:recipes=[(list(range(400,408)),'Preassembled 小英'),([408,409],'Attach the two-sided speech bubble')]
    unit('tsai',recipes,
         'Complete 小英 with the speech bubble','One banner, two faces: 叫你休息 / 講不聽. Apply the jacket decal and both banner decals. Keep the figure beside the vehicle.',
         view='figure',context=[])
    ops[-1]['manual'].update(decorations=True,unit_name='小英 figure and banner')
    if args.refine_build:next(o for o in ops if o['assembly']=='tsai-unit'and o['ids']==list(range(400,408)))['manual'].update(preassembled=True,unit_name='小英 minifigure')
accessory('Place the figures in the final scene'if 400 in pieces else'Place the candidate at the helm',
          'Place the candidate at the helm. 小英 stands beside the vehicle.'if 400 in pieces else'Fit the completed candidate on the rear platform. Review the rail, helm and figure attachments before handling the model.',
          list(pieces),view='rear',place_figures=True)
assert seen==pieces.keys(),('Missing parts',sorted(pieces.keys()-seen))
if args.compact_build:
    # Presentation batches preserve the exact ordered construction operations.
    # They do not imply a simultaneous insertion or change part ownership.
    groups=[
      ('Build the rear bumper strip layers',['Fit the rear lower bumper strips','Fit the rear bumper cross strips']),
      ('Finish the rear bumper',['Add the rear clip and plate layer','Finish the rear bumper corners','Fit the rear plate tile']),
      ('Build the left side panels',['Add the left side-facing backing plates','Fit the left curved and sloped panels']),
      ('Finish the left side trim',['Finish the left narrow side tiles','Fit the left door and front side tiles']),
      ('Build the right side panels',['Add the right side-facing backing plates','Fit the right curved and sloped panels']),
      ('Finish the right side trim',['Finish the right narrow side tiles','Fit the right door and front side tiles']),
      ('Finish the rear wheel-arch caps',['Build the rear arch cap layers','Fit the rear rope rings and trim']),
      ('Finish the front wheel-arch caps',['Build the front arch cap layers','Fit the front rope rings and trim']),
      ('Tie the upper body sides',['Extend the upper side supports','Add the upper body-side strips']),
      ('Finish the upper body strips',['Fit the door and front-corner slopes','Fit the narrow upper side plates']),
      ('Build the front body core',['Build the front body core','Add the front corner supports and lights']),
      ('Build the front face supports',['Fit the front face brackets','Install the front central body brick']),
      ('Fit the lamp housings and lower slopes',['Fit the two black front supports','Fit the two inverted front corner slopes']),
      ('Build the front grille',['Fit the front grille backing plate','Build the slatted front grille']),
      ('Build the hood supports',['Build the hood support layer','Tie the rear edge of the hood supports']),
      ('Build the cabin floor',['Fit the interior slopes','Tie the rear cab floor']),
      ('Fit the dashboard, steering and seat',['Fit the dashboard support and grille tiles','Assemble the steering stand and wheel','Fit the cabin seat']),
      ('Build the rear cab pillars and glazing',['Build the two rear cab pillars','Fit the four transparent cab side panels']),
      ('Tie and cap the rear cab frame',['Tie the rear cab frame','Cap the rear cab frame']),
      ('Fit the windscreen and roof support',['Fit the dedicated vehicle windscreen','Complete the front roof support']),
      ('Fit the hood and upper tiles',['Fit the Dark Orange hood shell','Fit the white centre tile and orange wings']),
    ]
    adopted=[]
    if args.refine_build:
        groups += [
          ('Build the rear frame supports',['Add the two rear longitudinal plates','Fit the rear frame brackets','Tie the rear frame brackets']),
          ('Fit the underside dishes',['Fit the two rear underside dishes','Fit the remaining underside dishes']),
          ('Finish the front lower bumper',['Build the front lower bracket course','Fit the two lower front slopes','Finish the lower front bumper']),
          ('Build the rear floor spacers',['Add the lower rear spacer course','Add the rear round spacer plates']),
          ('Build the front floor spacers',['Add the lower front spacer course','Add the front round spacer plates']),
          ('Build the bed floor and supports',['Build the rear bed and centre floor','Add the four narrow floor supports']),
          ('Fit all four wheel arches',['Fit the rear white wheel arches','Fit the front white wheel arches']),
          ('Fit both curved bumpers and headlights',['Finish the left curved bumper and clear headlight','Finish the right curved bumper and clear headlight']),
          ('Fit the sail mast and supports',['Fit the mast foot plate','Stack the two round mast supports','Insert the constant-diameter mast bar']),
          ('Fit the rear mast and both flags',['Insert the black rigid-hose mast','Clip both '+banner_color+' flags to the rear mast']),
        ]
    for serial,(title,names)in enumerate(groups,1):
        selected=[op for op in ops if op['manual']['title']in names]
        # Earlier batches may have renamed a terminal operation. A second
        # grouping here is restricted to original, disjoint headings.
        assert len(selected)==len(names),(title,names)
        indices=[ops.index(o)for o in selected]
        assert indices==list(range(indices[0],indices[0]+len(indices))),(title,'Noncontiguous operations')
        assert all(op['kind']=='build'and not op['manual'].get('accessory')for op in selected)
        notes=[op['manual']['note']for op in selected if op['manual']['note']]
        for op in selected:op['instruction_batch']=f'authored-region-{serial}'
        selected[-1]['manual'].update(title=title,note=' '.join(dict.fromkeys(notes)))
        adopted.append(dict(title=title,source_headings=names,piece_ids=[i for op in selected for i in op['ids']]))
    if args.refine_build:m['preassembled_figures']=[dict(module=mod,ids=sorted(i for i,p in pieces.items()if p['module']==mod and i not in[408,409]))for mod in ['candidate','tsai']]
    m['instruction_optimization']=dict(kind='Authored connected components and presentation batches through the shared compiler',
        component_recipes=['Chassis core','Four two-plate platform risers'],presentation_batches=adopted,
        repeated_wheel_installations_batched=4,
        source_geometry_preserved=True,construction_operations_retained=True,
        limit='Full native automatic optimization/insertion replay remains unsupported; targeted graph and path evidence is separate.')
m['build_operations']=ops
renumber(m)
plan=compile_plan(m)
# Presentation metadata is attached to the compiled steps; it never creates a
# second instruction sequence. Every local picture comes from recipe_frames.
jobs=[];state=set();op_by={o['step']:o for o in ops};bands_installed=False;prefix_first={}
view_changes=[];previous_view=None
steady_views={
 'Build the chassis core':'rear','Build the rear frame supports':'rear','Extend the longitudinal plates toward the front':'rear',
 'Finish the front lower bumper':'underside','Build the bed floor and supports':'front','Fit all four wheel arches':'front-other',
 'Finish the front wheel-arch caps':'rear','Cap the rear side rails':'rear','Tie the upper body sides':'rear','Finish the upper body strips':'rear',
 'Fit all four completed wheels':'front','Apply the individual banner stickers':'front','Place the figures in the final scene':'front',
}
for entry in plan['steps']:
    last=op_by[entry['end_operation']];manual=copy.deepcopy(last['manual'])
    if args.steady_views:
        old_view=manual['view'];manual['view']=steady_views.get(manual['title'],old_view)
        if manual['view']!=old_view:view_changes.append(dict(step=entry['number'],title=manual['title'],before=old_view,after=manual['view']))
        if previous_view and(previous_view=='underside')!=(manual['view']=='underside'):manual['turn_model']='Underside'if manual['view']=='underside'else'Studs up'
    previous_view=manual['view']
    state.update(entry['new_ids'])
    if any(op_by[n]['manual'].get('bands_installation') for n in entry['operations']):bands_installed=True
    manual['bands_installed']=bands_installed
    focus=manual.get('focus_ids')
    if focus is not None:shown=set(focus)
    elif manual.get('context') is not None:
        shown={i for i in state if pieces[i]['module'] in manual['context']}|set(entry['new_ids'])
        # Root-local work still needs its preceding local pieces.
        shown.update(i for i in state if pieces[i]['module']==entry['module'])
    elif entry['module']=='truck':shown={i for i in state if pieces[i]['module']=='truck'}
    else:shown={i for i in state if pieces[i]['module']==entry['module']}
    # The figure is built at its eventual location, but first remains aside.
    if entry['module']=='candidate':shown=set(entry['new_ids'])
    if args.connected_sides:
        # Main steps retain every installed vehicle component. Local recipe
        # frames remain isolated; the completed figure stays aside until its
        # explicit final placement. A module change must not hide the roof.
        shown={i for i in state if pieces[i]['module']not in['candidate','tsai']or manual.get('place_figures')}
        if entry['module']in['candidate','tsai']:shown=set(entry['new_ids'])
    manual['ids']=sorted(shown);manual['title']=manual['title'].replace('left roof speaker','left roof speaker')
    name=f"images/step-{entry['number']:03}"
    manual['image']=name+'.png'
    jobs.append([name,dict(ids=manual['ids'],newIds=entry['new_ids'],view=manual['view'],width=1400,height=900,decorations=bool(manual.get('accessory')or manual.get('decorations')),bands=bands_installed)])
    frames=[];local=set()
    recipe_child=last.get('child')
    if entry.get('copies',1)>1 and last.get('child'):
        recipe_child=next(op_by[n]['child']for n in entry['operations']if op_by[n].get('child'))
    local_ops=[o for o in ops if o['assembly']==recipe_child]
    instance_recipe=recipe_frames(local_ops,pieces)if local_ops and all(o['kind']=='build'for o in local_ops)else []
    for index,frame in enumerate(instance_recipe,1):
        local.update(frame['ids']);frame_ops=[op_by[n] for n in frame['operations']]
        fn=f"images/step-{entry['number']:03}-local-{index}"
        frames.append(dict(number=index,title=frame_ops[-1]['manual']['title'],view=frame_ops[-1]['manual']['view'],ids=frame['ids'],shown_ids=sorted(local),operations=frame['operations'],image=fn+'.png',preassembled=bool(frame_ops[-1]['manual'].get('preassembled'))))
        jobs.append([fn,dict(ids=sorted(local),newIds=frame['ids'],view=frame_ops[-1]['manual']['view'],width=800,height=600,decorations=entry['module']=='tsai')])
    manual['instance_frames']=frames
    manual['frames']=frames if entry.get('recipe_operations') else []
    if last.get('child'):manual['unit_name']=manual.get('unit_name',last['child'].replace('-',' '))
    if last.get('repeat_prefix_group'):
        group=last['repeat_prefix_group'];manual.update(repeat_prefix_frames=last['repeat_prefix_frames'],repeat_prefix_count=last['repeat_prefix_count'])
        if group in prefix_first:manual['repeat_prefix_from']=prefix_first[group]
        else:prefix_first[group]=entry['number']
    if entry.get('recipe_step') and not entry.get('recipe_operations'):manual['repeat_from']=entry['recipe_step']
    manual['approach_frames']=[]
    for index,spec in enumerate(manual.pop('approach_specs',[]),1):
        fn=f"images/step-{entry['number']:03}-approach-{index}"
        manual['approach_frames'].append(dict(number=index,title=spec['title'],offsets=spec['offsets'],image=fn+'.png'))
        jobs.append([fn,dict(ids=manual['ids'],newIds=entry['new_ids'],view=manual['view'],width=1200,height=850,decorations=False,bands=bands_installed,offsets=spec['offsets'])])
    entry['manual']=manual
m['instruction_plan']=plan
if args.steady_views:m['instruction_camera_review']=dict(changes=view_changes,main_direction_changes=sum(a['manual']['view']!=b['manual']['view']for a,b in zip(plan['steps'],plan['steps'][1:])),scope='Presentation only; installed poses and raw construction operations are unchanged. Local recipes retain their own useful viewing angles.')
(OUT/'images').mkdir(exist_ok=True)
lots=Counter((p['part'],p['color']) for p in m['pieces'])
icons={}
for index,((part,color),quantity) in enumerate(sorted(lots.items()),1):
    p=next(p for p in m['pieces'] if (p['part'],p['color'])==(part,color))
    name=f'images/part-{index:03}';icons[part+'|'+color]=name+'.png'
    jobs.append([name,dict(ids=[p['id']],view='front',width=360,height=280,decorations=False)])
jobs += [['front',dict(width=1600,height=1100)],['rear',dict(view='rear',width=1600,height=1100)]]
raw=json.dumps(m,ensure_ascii=False,indent=2).encode();(OUT/'model.json').write_bytes(raw)
roundtrip=write_exports(m,OUT,model_sha256=hashlib.sha256(raw).hexdigest())
(OUT/'yangliu-shape.mpd').write_bytes((OUT/'clkao-house.mpd').read_bytes())
for f in ['catalog-meshes.json'] :shutil.copyfile(SOURCE/f,OUT/f)
summary=json.loads((SOURCE/'prototype-summary.json').read_text());summary['mpd_roundtrip']=roundtrip
(OUT/'prototype-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(OUT/'instruction-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(OUT/'instruction-render-jobs.json').write_text(json.dumps(jobs,separators=(',',':')))
(OUT/'part-icons.json').write_text(json.dumps(icons,indent=2)+'\n')
(OUT/'inventory.csv').write_text('ldraw_part,color,quantity\n'+''.join(f'{p},{c},{q}\n' for (p,c),q in sorted(lots.items())))
shutil.copyfile(OUT/'inventory.csv',OUT/'preliminary-inventory.csv')
coverage=dict(schema='yangliu-full-instruction-coverage/1',source_model_sha256=m['instruction_source_sha256'],
    model_sha256=hashlib.sha256(raw).hexdigest(),plan_sha256=hashlib.sha256((OUT/'instruction-plan.json').read_bytes()).hexdigest(),
    pieces=len(pieces),lots=len(lots),public_steps=len(plan['steps']),internal_operations=len(ops),rigid_introductions=len(seen),
    all_parts_once=True,all_operations_covered=len(plan['operation_to_step'])==len(ops),external_build_steps=0,mpd=roundtrip,
    construction_order='Object-specific draft staging compiled by lego_instruction_plan.compile_plan; insertion replay not certified for these transformed Technic poses.',
    unresolved_interfaces=[s['number'] for s in plan['steps'] if s['manual'].get('hold')],physical_capacity='not_evaluated')
(OUT/'instruction-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
print(json.dumps(dict(out=str(OUT),pieces=len(pieces),steps=len(plan['steps']),operations=len(ops),render_jobs=len(jobs)),indent=2))

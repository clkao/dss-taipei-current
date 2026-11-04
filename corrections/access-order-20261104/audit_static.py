#!/usr/bin/env python3
"""Full source sequence coverage, not a geometric or physical insertion sweep."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
source=ROOT/'sources/minifigure/legacy-v10/model.json'; raw=source.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='49b6a0d3eb138e4f456084714d7cbf0422da8b8209ed500d057447dd9a6021a0'
m=json.loads(raw);ops=m['build_operations'];pieces={p['id']:p for p in m['pieces']}
step_by_op={n:s['number'] for s in m['instruction_plan']['steps'] for n in s['operations']}
# Explicit source-bound review regions exhaust the sequence; an absence of a
# static concern is not a clearance claim.
regions=[(1,12,'chassis closure and pins'),(13,28,'four suspension recipes and joins'),
(29,35,'bands underside dishes and front bumper'),(36,42,'floor and spacer closure'),
(43,58,'both side carriers'),(59,66,'wheel arches and rear bed'),(67,89,'body trim and cap layers'),
(90,93,'tailgate'),(94,105,'front core grille headlights and hood supports'),
(106,119,'cabin glazing windscreen hood and roof'),(120,131,'wheels'),(132,145,'platform and shield mounts'),
(146,164,'helm shield and outboard rails'),(165,174,'speakers'),(175,190,'masts flags and rings'),
(191,199,'print cord and supplied figures')]
findings=[]
def finding(key,kind,ns,ids,observation,impact,next_proof,disposition):
 findings.append(dict(key=key,classification=kind,operations=ns,reader_steps=sorted({step_by_op[n] for n in ns}),piece_ids=ids,
 parts={str(i):pieces[i]['part'] for i in ids},observation=observation,impact=impact,cheapest_next_proof=next_proof,disposition=disposition))
finding('pins','source-confirmed ordering conflict; physical concern reported',[1,2,3,4,5,6,12],[172,178,216,231],
 'Both parallel beams are tied and joined before either double-ended pin is introduced. Each pin has source catalog contacts to both beams; the pin collar is centred at their common face.',
 'A late pin instruction can require reopening the already tied chassis. Redrawing the same order does not repair this.',
 'Dry-fit one beam with both pins, then mate the second beam before ties. Verify collar seating and force before accepting the revised order.',
 'Candidate reorders and updates core membership; unaccepted.')
finding('front-bumper','source-confirmed ordering/grouping conflict; physical concern reported',[30,31,32,33,34,35],[191,190,183,184,182,187,189,215,229,170],
 'Front dish191 precedes lower tie190; brackets183/184 and cap182 share raw33. Reader13 merges33–35 with zero detail frames. Source elevations form lower tie / bracket foot / upper cap layers.',
 'The front dish can obstruct access; the combined panel also conceals the bracket/cap order.',
 'Dry-fit lower tie then brackets then cap, slopes and trim without191; add191 from the underside last. Check the final dish still seats without disassembly.',
 'Candidate builds a nine-piece front lower bumper locally on the table, joins via cap182 to168/177, then adds191. New join clearance unverified; unaccepted.')
finding('suspension','suspected joint-access and ergonomic risk',list(range(13,29)),[217,218,219,224,223,227,230,226,225,241,240,242,232,220,228,238,237,239,245,234,233,246,248,247],
 'All four recipes pair inner arm/pivot, outer pin/carrier, then wheel pin/ball pin; complete units join later. Source confirmed contacts establish intended mates but not pin insertion or finger access.',
 'A same-panel pair can hide which side receives a pin first; joining a finished unit to the corrected chassis still needs approach evidence.',
 'Check one left and one right inner-arm/pivot and outer pin/carrier pair with actual parts, then all four joins. Preserve each asymmetric pose and do not infer symmetry certification.',
 'No reorder: retain source until pair and unit approach checks identify an actual blocker.')
finding('floor-closure','ergonomic/closure review pending',[29,32,36,37,38,39,40,41,42],[99,129,63,111,91,151],
 'Floor plates99/129 arrive at36 after suspension/bands but before both carriers. Narrow supports63/111/91/151 arrive at42. These become the fixed prefix for side-carrier joins.',
 'Once both floor plates and support layers are installed, later brackets may need approach space that final contacts do not describe.',
 'Use the exact step18/19 prefix to inspect underside-facing carrier brackets against floor edges; compare deferring only the obstructing closure if a real obstruction is established.',
 'Do not defer floors speculatively: they support subsequent layers and may create unsupported prefixes.')
finding('side-carrier-local','captain-confirmed local access issue; mirrored source pattern',[47,48,49,55,56,57],[39,46,38,331,42,41,48,82,87,333,81,93,89,83],
 'Two upper brackets precede top rails, then three remaining upper brackets attach to those rails. Right:82/87→333/81→93/89/83. Left:39/46→38/331→42/41/48. The last brackets are added after rail closure, but the local unit has no floor underneath yet.',
 'Captain identifies the three right-angle parts under plates already attached to two brackets as the reported issue. Moving the last three earlier alone can restore floating pieces; each rail must first carry its own brackets as a separate local unit.',
 'Dry-fit each newly authored complete rail/bracket unit before joining the lower carrier, separately from whole-carrier installation; verify seating without force and distinguish awkward gripping from necessary removal.',
 'Candidate builds two separate upper rail units per side with all brackets fitted before each rail joins the lower carrier. Four shared running-board frames remain unchanged. Physical seating remains unverified.')
finding('side-carrier-join','suspected obstruction; retained unresolved near-seat witnesses',[36,42,50,58],[96,115,156,166,99,129,42,48,83,93,63,91,111,151],
 'The full15-piece right carrier joins at58 after floor99/129 and supports111/151. Retained above-path evidence names156/99 and166/129 as unreported near-seat pairs;83/111 and93/151 are reported stud pairs. Left has96/99,115/129 and42/63,48/91. This differs from local recipe assembly.',
 'Simultaneous upper seating and lower bracket/floor-edge clearance is unresolved. Finished-pose images and connected-prefix checks cannot prove a top-down route.',
 'First dry-fit right carrier into exact installed prefix, observing156/99 and166/129 from underneath. Record whether separation or only finger access is needed; then test left. If blocked, compare deferred floor closure vs split carrier installation with fresh lifecycle checks.',
 'No geometry change or fabricated motion. Existing top labels remain inherited unverified intent; do not treat them as certified.')
finding('rear-bed','previously corrected dependency retained; near-seat limits remain',[59,60,61,62,63,64,65,66,67],[100,118,206,214,99,109],
 'Bed installation66 precedes rear trims206/214 at67. Prior evidence found100↔206 and118↔214 obstruction when those trims were already present. Near-seat bed/floor pairs100/99,109/99,118/99 remained unresolved.',
 'Moving trims earlier would regress an existing correction. Current order does not establish every bed seating contact.',
 'Keep66 before67 as a regression assertion; dry-fit remaining near-seat bed/floor pairs only if acceptance needs them.',
 'No new defect claimed; candidate preserves corrected order.')
finding('body-caps','suspected hidden layering and ergonomic access',list(range(68,90)),[119,120,101,102,192,196,195,202,194,203,1,2,198,27,80,26,79,25,335,78,337,72,144,71,143,70,336,142,338],
 'Rear strip/clip/corner courses and wheel-arch cap layers carry source contacts between consecutive raw operations but several reader groups show only the final combined state.',
 'Reader can reverse dependent layers or lose access to clips/rope rings even though raw ordering is retained.',
 'Review the actual affected pages and dry-fit clip and rope-ring layers before caps; split panels only where an insertion dependency or practical ambiguity is demonstrated.',
 'Presentation/access suspects; do not bulk reorder merely because groups are long.')
finding('front-lights','suspected mixed attachment axes and hidden layers',list(range(94,106)),[95,125,138,121,123,136,126,147,122,309,310,311,312,317,318,319,314,320,321,322,316,55,30,52,28,31],
 'Front core→brackets→grille backing→slats precedes left/right curved bumper and light groups102/103. Hood supports104/105 later close the region. Raw102/103 themselves each introduce four parts.',
 'One finished headlight/bumper panel can conceal inner-to-outer mating and hand access; combined source operations are not an insertion path.',
 'Check bracket/grille and each four-part lamp/curved bumper course before hood supports. Use exact part transforms to identify approach directions only after mate verification.',
 'No correction until local obstruction or ordering ambiguity is established.')
finding('cabin-roof','ergonomic access with correct coarse closure order',list(range(106,120)),[199,200,287,11,324,65,325,6,8,22,23,19,20,21,18,17,7,4,3,29,334,339,340,5],
 'Steering/dashboard/seat108–110 precede pillars/glazing111–114, windscreen115–116, hood117–118 and roof119. Several reader groups merge their raw layers; roof is explicitly removable.',
 'Coarse order avoids seating the interior through an installed roof, but same-op steering pair and glazing/cap access are not certified.',
 'Inspect steering pair199/200 and glazing/frame cap seating before roof; retain interior-before-roof constraints and use visible ordered panels if the page hides the mate.',
 'No confirmed new trapped part; no auto-reorder.')
finding('shield','compound approach retained; physical seating and presentation pending',list(range(145,165)),[2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,285,286],
 'Mounts145 precede helm and panels; all three panel units install before outboard rails164 and tall masts175 onward. Accepted shield evidence is a bounded compound-path record, not a generic top insertion.',
 'Collapsing it to one straight top arrow or adding rails/flags early can invalidate intended access.',
 'Review exact compound approach and stud-section evidence for current unchanged panel poses, then physically seat mounts/panels before rails and flags.',
 'Candidate preserves this order and does not fabricate vectors or claim new sweep coverage.')
finding('late-equipment','ergonomic/repeated-recipe review pending',list(range(165,200)),[288,289,290,291,292,293,294,295,296,297,298,299,300,307,308,301,302,303,304,305,306,342,343,341,265,267,266,268,269,270,271],
 'Speakers are capped after cones; sail clips follow wedge tie; banner collar precedes mast and flags; figures are supplied and placed last. These preserve plausible coarse access order, but connector fit and small-part gripping are untested.',
 'Repeated recipes can hide per-copy access; final figure placement is not evidence of physical stability.',
 'Dry-fit cone sockets and flag clips locally, then install under the actual prefix. Preserve supplied-figure semantics and exact copy identity.',
 'No new confirmed ordering correction; maintain existing physical limits.')
rows=[]
for o in ops:
 ns=o['step']; ids=o['ids']; related=[f['key'] for f in findings if ns in f['operations']]
 rows.append({'operation':ns,'reader_step':step_by_op[ns],'region':next(label for a,b,label in regions if a<=ns<=b),
 'kind':o['kind'],'assembly':o['assembly'],'child':o.get('child'),'introduced_ids':ids,
 'parts':{str(i):pieces[i]['part'] for i in ids},'source_contacts':o.get('catalog_pairs',[]),
 'findings':related,'static_disposition':'linked review finding' if related else 'no new issue identified from static source; insertion/ergonomics untested'})
assert len(rows)==199 and {r['reader_step'] for r in rows}==set(range(1,69))
result={'schema':'dss-static-full-sequence-audit/1','adopted':False,'source_sha256':hashlib.sha256(raw).hexdigest(),
 'coverage':{'raw_operations':199,'reader_steps':68,'all_operations_assigned_region':True,'physical_or_continuous_geometric_sweep':False},
 'scope':'Static source audit of identities, existing contact records, local assembly lifecycles, closure order, and reader grouping. No new collision/backend/render or physical check.',
 'findings':findings,'operations':rows}
(OUT/'full-sequence-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Static coverage:199 operations,68 reader steps;',len(findings),'source-bound review findings.')

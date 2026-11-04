#!/usr/bin/env python3
"""Derive an unaccepted, static-only access-order candidate from one frozen model.
No compiler, renderer, importer, connector backend or shared-tool mutation.
"""
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / 'sources/minifigure/legacy-v10/model.json'
EXPECTED = '49b6a0d3eb138e4f456084714d7cbf0422da8b8209ed500d057447dd9a6021a0'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def derive():
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED, 'Unexpected source: review a new source before deriving'
    source = json.loads(raw)
    original = {o['step']: o for o in source['build_operations']}
    public = source['instruction_plan']['steps']
    old_main = {n: s['number'] for s in public for n in s['operations']}
    lineage = []

    def part(n, suffix='', ids=None, title=None, note=None, assembly=None):
        o = copy.deepcopy(original[n])
        o.update(id=f'legacy-{n:03}{suffix}', legacy_operation=n, legacy_main_step=old_main[n])
        if ids is not None:
            assert set(ids) <= set(original[n]['ids'])
            o['ids'] = ids
        if assembly:
            o['assembly'] = assembly
        altered = n in {1, 6, 12, 31, 32, 33, 34, 35, 47, 48, 49, 55, 56, 57}
        if altered:
            # Old generic 'top' came from build(), not a proved motion path.
            o.pop('instruction_batch', None)
            o['direction'] = None
            o['placements'] = [{'ids': list(o['ids']), 'direction': None, 'contacts': []}]
            o['approach_status'] = 'unverified; show installed state, do not infer an insertion arrow'
            o['catalog_pairs_source_only'] = o.pop('catalog_pairs', [])
            if title:
                o['manual']['title'] = title
            if note is not None:
                o['manual']['note'] = note
        lineage.append(o)
        return o

    # Fresh chassis: a pin's collar lies at the common face of the two beams.
    # Fit into the still-open first beam, mate the second, then lock with ties.
    ops = [part(1, 'a', [172], 'Start with one long chassis beam',
                'Keep the second long beam separate until both pins are fitted.'),
           part(12, ids=[216, 231], assembly='chassis-core',
                title='Fit the two friction pins into the first beam',
                note='Use the two holes shown by the unchanged final model, one near each end. Leave the other halves exposed toward the second beam.'),
           part(1, 'b', [178], 'Mate the second beam with the exposed pins',
                'Align both holes before pressing the beams together. Add no tie plates until both pins are seated.')]
    ops.extend(part(n) for n in range(2, 12))
    core_join = next(o for o in ops if o['legacy_operation'] == 6)
    core_join['manual']['note'] = 'Both pins belong inside this completed core. Continue with rear supports only after the tie plates are fitted.'
    ops.extend(part(n) for n in range(13, 31))
    ops += [part(31, 'a', [204, 188], 'Fit the remaining rear and centre underside dishes',
                 'Leave the front underside dish off until the lower bumper is complete.'),
            part(32, 'a', [169], 'Fit the rear socket plate', 'Keep the front work area open.'),
            part(32, 'b', [190], 'Fit the front lower tie plate',
                 'The front transparent dish is still omitted. Keep access to the bracket mounting faces.'),
            part(33, 'a', [183, 184], 'Fit both front brackets',
                 'Fit the brackets to the lower tie before adding the upper cap plate.'),
            part(33, 'b', [182], 'Cap the front brackets with the upper plate',
                 'Do this after both brackets are in place.'),
            part(34, title='Fit the two lower front slopes', note='Add them to the bracket faces before the outer bumper trim.'),
            part(35, 'a', [215, 229], 'Fit the two outer bumper slopes',
                 'Keep the centre tile separate for the next panel.'),
            part(35, 'b', [170], 'Fit the centre bumper tile',
                 'Complete the lower bumper before adding the front underside dish.'),
            part(31, 'b', [191], 'Fit the front transparent underside dish last',
                 'Turn the chassis over and fit this last dish after the lower bumper is complete. Do not remove the completed brackets to follow the earlier dish step.')]
    ops.extend(part(n) for n in range(36, 200))
    # The deferred dish cannot be used as temporary support for lower tie190.
    # Assemble the nine-piece lower bumper on the table, then attach it via
    # cap182 to existing front ties168/177. This is a declared new local unit,
    # not an unsupported floating plate installed on the chassis.
    for o in ops:
        if o['id'] in {'legacy-032b','legacy-033a','legacy-033b','legacy-034','legacy-035a','legacy-035b'}:
            o['assembly'] = 'front-lower-bumper'
    lower = next(o for o in ops if o['id']=='legacy-032b')
    lower['manual'].update(title='Start the front lower bumper on the table',
        note='Keep this lower tie plate separate from the chassis. Add the brackets, cap, slopes and trim before installing the complete bumper.')
    join = copy.deepcopy(next(o for o in ops if o['id']=='legacy-035b'))
    join.update(id='legacy-035j',kind='join',assembly='truck',child='front-lower-bumper',
        ids=[],instruction_component=True,
        placements=[{'ids':[170,182,183,184,187,189,190,215,229],'direction':None,'contacts':[]}])
    join['manual'].update(title='Fit the complete front lower bumper',
        note='Attach the upper cap to the existing front ties. Keep the front underside dish off; support the chassis while seating this bumper.')
    ops.insert(next(i for i,o in enumerate(ops) if o['id']=='legacy-031b'),join)
    # Each loose rail receives every bracket before being attached to the
    # lower carrier. Two disconnected rails are two local units, never a fake
    # connected seven-piece assembly. Original four-frame shared prefix stays.
    rail_units = {}
    rail_unit_rails = {}
    for side, n_mount, n_rail, n_rest, definitions in [
        ('left',47,48,49,[(38,39,[42,41],96),(331,46,[48],115)]),
        ('right',55,56,57,[(81,87,[89,83],156),(333,82,[93],166)])]:
        replacement=[]
        for index,(rail,mount,rest,mate) in enumerate(definitions,1):
            suffix = 'a' if index==1 else 'b'
            unit=f'{side}-upper-rail-{index}'
            rail_units[unit]=sorted([rail,mount]+rest)
            rail_unit_rails[unit]=rail
            a=part(n_rail,suffix,[rail],
                'Hold the loose upper rail with its underside exposed',
                'Keep this rail separate from the lower carrier until all its brackets are fitted.',assembly=unit)
            b=part(n_mount,suffix,[mount],
                'Fit the mounting bracket to the loose rail',
                'Support the loose rail while fitting the bracket; do not attach the rail to the lower carrier yet.',assembly=unit)
            c=part(n_rest,suffix,rest,
                'Fit the remaining brackets while the underside is open',
                'All brackets for this rail must be in place before installation on the lower carrier.',assembly=unit)
            j=copy.deepcopy(c)
            j.update(id=f'legacy-{n_rest:03}j{index}',kind='join',assembly=f'{side}-side-carrier',child=unit,ids=[],
                instruction_component=True,placements=[{'ids':rail_units[unit],'direction':None,'contacts':[]}],
                source_mate_pairs=[[mount,mate]])
            j['manual'].update(title='Fit this completed upper rail unit to the lower carrier',
                note='Align its mounting bracket with the lower bracket. Keep the other loose rail separate until its own brackets are complete.')
            replacement.extend([a,b,c,j])
        first=next(i for i,o in enumerate(ops) if o['legacy_operation']==n_mount)
        assert [o['legacy_operation'] for o in ops[first:first+3]]==[n_mount,n_rail,n_rest]
        ops[first:first+3]=replacement
    # Compute membership from introductions and joins, not stale legacy trays.
    contents, joined, introduced = {}, set(), []
    join_checks = []
    for step, o in enumerate(ops, 1):
        o['step'] = step
        a = o['assembly']
        assert a not in joined, ('write after child joined', a)
        contents.setdefault(a, set())
        if o['kind'] == 'join':
            child = o['child']
            assert child in contents and child not in joined
            expected = sorted(contents[child])
            old_set = sorted(i for p in original[o['legacy_operation']]['placements'] for i in p['ids'])
            if child == 'chassis-core':
                assert set(expected) == set(old_set) | {216, 231}
                o['placements'] = [{'ids': expected, 'direction': None, 'contacts': []}]
            elif child in rail_units:
                assert expected == rail_units[child]
                assert o['placements'][0]['ids'] == expected
            elif child == 'front-lower-bumper':
                assert expected == [170,182,183,184,187,189,190,215,229]
                assert o['placements'][0]['ids'] == expected
            else:
                assert expected == old_set, ('unexpected unit change', child)
            assert not contents[a] & contents[child]
            contents[a].update(contents[child])
            joined.add(child)
            join_checks.append({'operation': o['id'], 'child': child, 'parent': a,
                                'occurrences': expected, 'membership_changed': expected != old_set})
        else:
            assert not set(introduced) & set(o['ids'])
            introduced.extend(o['ids'])
            contents[a].update(o['ids'])
    assert len(introduced) == len(set(introduced)) == 348
    assert set(introduced) == {p['id'] for p in source['pieces']}
    # All original operations survive in one or more partitions, without added pieces.
    for n, old in original.items():
        partitions = [o for o in ops if o['legacy_operation'] == n]
        assert len(partitions) >= 1
        assert sorted(i for o in partitions for i in o['ids']) == sorted(old['ids'])
    old_owner = {i:o['assembly'] for o in original.values() for i in o['ids']}
    new_owner = {i:o['assembly'] for o in ops for i in o['ids']}
    owner_delta = {str(i): {'from':old_owner[i], 'to':new_owner[i]} for i in old_owner if old_owner[i] != new_owner[i]}
    expected_delta={str(i): {'from':'truck', 'to':'chassis-core'} for i in [216,231]}
    expected_delta.update({str(i): {'from':'truck','to':'front-lower-bumper'} for i in [170,182,183,184,187,189,190,215,229]})
    for unit,ids in rail_units.items():
        expected_delta.update({str(i): {'from':unit.split('-')[0]+'-side-carrier','to':unit} for i in ids})
    assert owner_delta == expected_delta
    # Every unaffected operation stays byte-equivalent, apart from lineage and new ordinal.
    for o in ops:
        if o['legacy_operation'] not in {1,6,12,31,32,33,34,35,47,48,49,55,56,57}:
            stripped = {k:v for k,v in o.items() if k not in {'id','legacy_operation','legacy_main_step','step'}}
            assert stripped == {k:v for k,v in original[o['legacy_operation']].items() if k != 'step'}
    positions = {i:o['step'] for o in ops for i in o['ids']}
    old_pos = {i:o['step'] for o in original.values() for i in o['ids']}
    constraints = [([172],[216,231],'first beam before pins'),
                   ([216,231],[178],'pins before second beam'),
                   ([178],[150,163,153,168,177],'second beam before ties'),
                   ([190],[183,184],'lower tie before brackets'),
                   ([183,184],[182],'brackets before cap'),
                   ([182],[187,189],'cap before front slopes'),
                   ([187,189],[215,229],'front slopes before outer trim'),
                   ([215,229],[170],'outer trim before centre tile'),
                   ([170,190,183,184,182,187,189,215,229],[191],'front dish after entire bumper')]
    regression = [{'rule':label,'before_ids':before,'after_ids':after,
                   'baseline_pass':max(old_pos[i] for i in before)<min(old_pos[i] for i in after),
                   'candidate_pass':max(positions[i] for i in before)<min(positions[i] for i in after)}
                  for before,after,label in constraints]
    regression.append({'rule':'preserve corrected bed install before trims206/214','baseline_pass':66 < old_pos[206] and 66 < old_pos[214], 'candidate_pass':next(o['step'] for o in ops if o['legacy_operation']==66) < min(positions[i] for i in [206,214])})
    for unit,ids in rail_units.items():
        parent_join=next(o for o in ops if o.get('child')==unit)
        regression.append({'rule':unit+' all brackets fitted before rail attaches to lower carrier',
            'candidate_pass':max(positions[i] for i in ids)<parent_join['step'],
            'baseline_pass':max(old_pos[i] for i in ids if i != rail_unit_rails[unit]) < old_pos[rail_unit_rails[unit]], 'baseline_note':'Original rail attached to mounting brackets before remaining brackets; exact source order is retained in crosswalk.'})
    assert all(x['candidate_pass'] for x in regression)
    assert not next(x for x in regression if x['rule']=='pins before second beam')['baseline_pass']
    assert not next(x for x in regression if x['rule']=='front dish after entire bumper')['baseline_pass']
    # Geometry, color, IDs and modules stay exact; only introduction-step metadata changes.
    pieces = copy.deepcopy(source['pieces'])
    for p in pieces:p['step'] = positions[p['id']]
    without_step = lambda ps:[{k:v for k,v in p.items() if k!='step'} for p in ps]
    assert without_step(pieces) == without_step(source['pieces'])
    groups = []
    for s in public:
        n = s['number']
        if n == 5:continue # Old pins now belong to the first core recipe.
        selected = [o for o in ops if o['legacy_main_step']==n and o['id']!='legacy-031b']
        if n == 1:selected = [o for o in ops if o['legacy_operation'] in [1,2,3,4,5,6,12]]
        if n == 13:selected += [o for o in ops if o['id']=='legacy-031b']
        changed = n in {1,11,12,13,18,19}
        groups.append({'number':len(groups)+1, 'legacy_main_step':n,
                       'operation_ids':[o['id'] for o in selected],
                       'title':s['manual']['title'],
                       'presentation_policy':'ordered explicit panels required; no combined final-only panel' if changed else 'unchanged legacy intent; regenerate against new ordinals',
                       'panels':[{'operation_id':o['id'],'title':o['manual']['title'],
                                  'note':o['manual'].get('note',''),'view':o['manual'].get('view'),
                                  'new_piece_ids':o['ids'],'kind':o['kind']} for o in selected] if changed else [],
                       'legacy_copies':s.get('copies'), 'legacy_repeat_count':s.get('repeat_count'),
                       'insertion_arrows':'not authorized by this correction'})
    assert [i for g in groups for i in g['operation_ids']] == [o['id'] for o in ops]
    candidate = {'schema':'dss-access-order-candidate/1','adopted':False,
                 'source':str(SOURCE.relative_to(ROOT)), 'source_sha256':EXPECTED,
                 'physical_validation':'pending','compiler_compatibility':'authoring intermediate; not a StudFleet build input',
                 'pieces':pieces,'colors':source['colors'],'assembly_roots':source['assembly_roots'],
                 'preassembled_figures':source['preassembled_figures'],
                 'build_operations':ops,'reader_groups':groups,
                 'note':'One derived construction sequence. Original snapshots stay immutable. Changed prefixes invalidate old prefix/sweep certificates.'}
    mapping = {'schema':'dss-correction-crosswalk/1','adopted':False,'source_sha256':EXPECTED,
               'operations':[{'old_operation':n,'old_main_step':old_main[n],
                              'candidate_operations':[{'id':o['id'],'ordinal':o['step'],'piece_ids':o['ids'],'assembly':o['assembly']} for o in ops if o['legacy_operation']==n]} for n in original],
               'reader_steps':[{'old_main_step':n,'candidate_groups':[g['number'] for g in groups if g['legacy_main_step']==n or (n==5 and g['legacy_main_step']==1)]} for n in range(1,69)],
               'ownership_delta':owner_delta}
    # Complete source audit: batches with hidden inner dependencies are review risks,
    # not proven obstructions and not automatically fixed by this patch.
    batches = []
    for s in public:
        nums=s['operations']; earlier=set(); links=[]
        for n in nums:
            o=original[n]
            for contact in o.get('catalog_pairs',[]):
                pair=set(contact['piece_ids'])
                if pair & earlier and pair & set(o['ids']):links.append({'operation':n, **contact})
            earlier.update(o['ids'])
        if len(nums)>1 and not s.get('manual',{}).get('frames'):
            batches.append({'legacy_main_step':s['number'],'operations':nums,'title':s['manual']['title'],
                            'cross_operation_contacts':links,
                            'classification':'suspected presentation/access risk; not proof of removal',
                            'changed_here':s['number'] in {11,13}})
    result={'schema':'dss-correction-static-check/1','adopted':False,'source_sha256':EXPECTED,
            'candidate_canonical_sha256':digest(candidate),'operations':len(ops),'reader_groups':len(groups),
            'unique_introductions':len(introduced),'geometry_colors_modules_exact_except_step':True,
            'all_original_operation_piece_partitions_preserved':True,'all_unchanged_operations_preserved':True,
            'all_units_join_once_after_contents_complete':True,'ownership_delta':owner_delta,
            'join_membership_checks':join_checks,'sequence_regressions':regression,
            'existing_copy_metadata_unchanged':True,'new_upper_rail_units':rail_units,
            'side_carrier_completed_join_membership_exact':all(x['membership_changed']==False for x in join_checks if x['child'] in ['left-side-carrier','right-side-carrier']),
            'new_local_unit':{'name':'front-lower-bumper','piece_ids':[170,182,183,184,187,189,190,215,229],'why':'Do not leave lower tie190 floating after deferring its dish; assemble on table and join via upper cap182.'},
            'proof_limit':'Static identity, declared order and assembly lifecycle only. No physical insertion, collision, readability or full-edition acceptance.'}
    for name,value in [('candidate-authoring.json',candidate),('crosswalk.json',mapping),('checks.json',result),
                       ('grouping-audit.json',{'schema':'dss-grouping-audit/1','adopted':False,'source_sha256':EXPECTED,'groups':batches})]:
        (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['operations','reader_groups','unique_introductions','geometry_colors_modules_exact_except_step','ownership_delta']},indent=2))

if __name__=='__main__':derive()

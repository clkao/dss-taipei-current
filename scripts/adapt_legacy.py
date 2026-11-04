#!/usr/bin/env python3
"""One-way DSS legacy adoption. Outputs are evidence, not a certified build plan.

assembly.json keeps StudFleet's admitted exact geometry byte-for-byte.
plan/presentation are explicitly DSS intermediate schemas until shared tooling
can express every accepted operation, supplied figure and compound path.
"""
import argparse
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def adapt(root, out):
    source = root / 'sources/minifigure/legacy-v10'
    intake = root / 'evidence/bootstrap/intake'
    model = json.loads((source / 'model.json').read_text())
    legacy = json.loads((source / 'instruction-plan.json').read_text())
    imported = json.loads((intake / 'assembly.json').read_text())
    report = json.loads((intake / 'import-report.json').read_text())
    assert sha(source / 'source.mpd') == report['source_sha256']
    assert sha(intake / 'assembly.json') == report['assembly_sha256']
    assert (source / 'source.mpd').read_bytes() == (intake / 'source.mpd').read_bytes()
    lines = (source / 'source.mpd').read_text().splitlines()
    by_uuid = {p['instance_id']: p for p in model['pieces']}
    instances = {p['id']: p for p in imported['instances']}
    crosswalk = []
    for origin in report['origins']:
        leaf = origin['path'][-1]
        comment = lines[leaf['line'] - 2].split()
        assert comment[:3] == ['0', '//', 'INSTANCE'], leaf
        piece = by_uuid[comment[3]]
        instance = instances[origin['id']]
        assert instance['part'] == str(piece['part'])
        assert instance['color'] == model['colors'][piece['color']][0]
        crosswalk.append({'piece_id': piece['id'], 'instance_id': piece['instance_id'],
                          'occurrence_id': origin['id'], 'module': piece['module'],
                          'part': instance['part'], 'color': instance['color'], 'source_path': origin['path']})
    assert len(crosswalk) == len(instances) == len(by_uuid) == 348
    assert len({x['piece_id'] for x in crosswalk}) == 348
    by_id = {x['piece_id']: x['occurrence_id'] for x in crosswalk}
    operations = []
    for op in model['build_operations']:
        n = op['step']
        operations.append({'id': f'legacy-op-{n:03}', 'legacy_operation': n,
                           'legacy_main_step': legacy['operation_to_step'][str(n)],
                           'occurrences': [by_id[i] for i in op.get('ids', [])],
                           'legacy_operation_exact': op})
    assert len(operations) == 199
    introduced = [i for op in model['build_operations'] for i in op.get('ids', [])]
    assert len(introduced) == 348 and len(set(introduced)) == 348
    assert set(introduced) == set(by_id)
    units = {}
    for op in model['build_operations']:
        units.setdefault(op['assembly'], []).append(op['step'])
    groups = [{'number': s['number'], 'operations': [f'legacy-op-{n:03}' for n in s['operations']],
               'legacy_presentation_exact': s} for s in legacy['steps']]
    assert len(groups) == 68
    common = {'generated_by': 'scripts/adapt_legacy.py', 'hand_edit': False,
              'source_model_sha256': sha(source / 'model.json'),
              'source_plan_sha256': sha(source / 'instruction-plan.json'),
              'assembly_sha256': sha(intake / 'assembly.json')}
    out.mkdir(parents=True, exist_ok=True)
    def write(name, value):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    (out / 'assembly.json').write_bytes((intake / 'assembly.json').read_bytes())
    write('occurrence-crosswalk.json', {'schema': 'dss-occurrence-crosswalk/1', **common, 'occurrences': crosswalk})
    write('operation-crosswalk.json', {'schema': 'dss-operation-crosswalk/1', **common,
          'operations': [{k: v for k, v in op.items() if k != 'legacy_operation_exact'} for op in operations]})
    write('plan.json', {'schema': 'dss-legacy-plan-intake/1', **common,
          'shared_generator_compatible': False,
          'order_policy': 'Preserve authored order and nested unit membership; do not infer independence or simultaneous construction.',
          'operations': operations, 'assembly_operation_membership': units,
          'supplied_preassembled_units': model['preassembled_figures'],
          'external_evidence': ['evidence/legacy-v10/connected-prefixes.json', 'evidence/legacy-v10/sweep-review.json'],
          'limits': ['Not studfleet/plan-1. No fabricated dependencies, copy transforms, insertion distances or certification.',
                     'Legacy direction and multi-phase approach frames remain source evidence; no lossy direction+distance conversion.']})
    write('presentation.json', {'schema': 'dss-legacy-presentation-intake/1', **common,
          'shared_generator_compatible': False, 'steps': groups,
          'note': 'Exact existing grouping/views/text retained. This intermediate is not fed to the strict StudFleet presentation parser.'})
    specs = {56: ('speakers-2x', ['n0', '7d']), 61: ('life-rings-2x', ['n0', '7d']),
             1: ('compact-main-step', ['h1']), 66: ('supplied-candidate', ['90']),
             67: ('supplied-tsai', ['90']), 18: ('shared-prefix-left-carrier', ['h1']),
             19: ('shared-prefix-right-carrier', ['h1']), 53: ('shield-compound-approach', ['31'])}
    write('specimens.json', {'schema': 'dss-migration-specimens/1', **common,
          'specimens': [{'name': name, 'main_step': n, 'shared_tool_dependencies': deps,
                         'occurrence_ids': [by_id[i] for i in legacy['steps'][n-1]['new_ids']],
                         'source_step': legacy['steps'][n-1]} for n, (name, deps) in specs.items()],
          'later': ['guidance and print assets: cn', 'reader labels: w4', 'neutral placement views: tw'],
          'acceptance': 'Compare actual artifacts and readability with legacy edition; counts alone never establish parity.'})
    return {'occurrences': len(crosswalk), 'operations': len(operations), 'main_steps': len(groups),
            'unique_introductions': len(set(introduced)), 'exact_imported_assembly_bytes': True,
            'part_color_uuid_crosswalk_complete': True, 'generator_plan_compatible': False,
            'geometry_changed': False, 'instruction_exported': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('migration/minifigure-v10'))
    args = parser.parse_args()
    print(json.dumps(adapt(Path(__file__).resolve().parents[1], args.out), indent=2))

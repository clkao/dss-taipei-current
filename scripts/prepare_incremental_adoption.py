#!/usr/bin/env python3
"""Derive section boundaries from retained DSS source. Does not generate instructions."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'manifests/incremental-adoption.json'
PINS = {
    'sources/minifigure/legacy-v10/model.json': '49b6a0d3eb138e4f456084714d7cbf0422da8b8209ed500d057447dd9a6021a0',
    'sources/minifigure/legacy-v10/instruction-plan.json': '9d05fe11832876ad3ee4fb52412c7f9ebd1f41d5f1dfcc1a0c7cb34932fa8402',
    'sources/minifigure/legacy-v10/source.mpd': '963953af7cd31d23d4adbfa8314b8cde23505d1fb5485da17950872c2cd6d1e2',
}

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    for path, expected in PINS.items():
        if hashlib.sha256((ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Retained source changed: {path}')
    steps = read('sources/minifigure/legacy-v10/instruction-plan.json')['steps']
    crosswalk = read('migration/minifigure-v10/occurrence-crosswalk.json')['occurrences']
    occurrences = {x['piece_id']: x['occurrence_id'] for x in crosswalk}
    model = read('sources/minifigure/legacy-v10/model.json')
    assert len(occurrences) == len(model['pieces']) == 348
    selected = {
        2: ('chassis-step-2', ['h1', 'tw', 'w4'], 'source-compiler-evidence',
            'evidence/integration/h1-16b3094-check/README.md',
            ['Actual PDF and numbered detail navigation', 'Legacy entry/exit context and adjacent step references']),
        56: ('speakers', ['7d', 'tw', 'w4'], 'isolated-artifact-evidence',
             'evidence/integration/labels-3a6833b-render/README.md',
             ['Vehicle support context at both joins', 'Schedule after preceding main steps', 'Exact two-copy ownership at section boundaries']),
        61: ('life-rings', ['7d', 'tw', 'w4'], 'isolated-artifact-evidence',
             'evidence/integration/labels-3a6833b-render/README.md',
             ['Vehicle support context at both joins', 'Schedule after preceding main steps', 'Exact two-copy ownership at section boundaries']),
        66: ('candidate-figure', ['90', 'tw', 'w4'], 'awaiting-candidate', None,
             ['Supplied eight-member unit and provenance', 'No loose-limb tray or unwanted recipe', 'Full stock quantities and installation context']),
        67: ('tsai-figure-accessory', ['90', 'tw', 'w4'], 'awaiting-candidate', None,
             ['Distinguish supplied members from later accessory introductions', 'Do not reintroduce body parts for accessory attachment', 'Full ten-member section coverage and stock quantities']),
    }
    entries = []
    seen = set()
    for step in steps:
        before = sorted(seen)
        additions = step['new_ids']
        assert len(additions) == len(set(additions))
        assert not (seen & set(additions)), f'Duplicate introduction in step {step["number"]}'
        seen.update(additions)
        if step['number'] not in selected:
            continue
        slug, dependencies, status, evidence, missing = selected[step['number']]
        entries.append({
            'section': slug, 'legacy_step': step['number'], 'title': step['manual']['title'],
            'operations': step['operations'], 'context_after_operation': min(step['operations']) - 1,
            'entry_piece_ids': before, 'new_piece_ids': additions, 'exit_piece_ids': sorted(seen),
            'entry_occurrences': [occurrences[x] for x in before],
            'new_occurrences': [occurrences[x] for x in additions],
            'exit_occurrences': [occurrences[x] for x in sorted(seen)],
            'counts': {'entry': len(before), 'new': len(additions), 'exit': len(seen)},
            'dependencies': dependencies, 'evidence_level': status, 'evidence': evidence,
            'remaining_section_checks': missing, 'adopted': False,
            'copy_boundary_status': 'Requires explicit recipe/copy reconciliation; piece sets alone do not establish availability',
        })
    assert seen == set(occurrences), 'Whole-plan introduction coverage differs from retained model'
    data = {
        'schema': 'dss-incremental-adoption/1', 'generated_by': 'scripts/prepare_incremental_adoption.py',
        'purpose': 'Preparation only; not executable StudFleet plan or workflow gate state',
        'source_pins': PINS, 'workflow': 'docs/instructions', 'edition': 'studfleet-parity-edition',
        'source_of_order': 'Retained instruction-plan.json and model build_operations',
        'priority': ['chassis-step-2', 'candidate-figure', 'tsai-figure-accessory', 'speakers', 'life-rings'],
        'priority_note': 'H1 artifact lease first, then90. Recipe context work can proceed when its own dependencies and resources are ready.',
        'sections': entries, 'whole_plan': {'steps': len(steps), 'unique_introductions': len(seen)},
        'retained_legacy_scope': ['All sections until exact section acceptance', 'Shared prefixes18/19', 'Retained shield panels and compound paths53', 'Guidance, print assets, purchasing exports, animation and full viewer parity'],
        'publication': {'authorized_by_this_manifest': False, 'hybrid_page_splicing': False},
    }
    TARGET.write_text(json.dumps(data, indent=2) + '\n')
    print(json.dumps({'manifest': str(TARGET), 'sections': {e['section']: e['counts'] for e in entries}, 'coverage': data['whole_plan']}))

if __name__ == '__main__':
    main()

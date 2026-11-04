---
title: Reconcile retained Blender reference with variant baselines
status: brief
source: Authorized 2026-11-03 DSS bootstrap handoff
started:
completed:
verdict:
score: 0.5
worktree:
issue:
pr:
mod-block:
id: ew17emhyb5am1q2a68m1r35m
---

## Brief

Retain and reconcile the existing Blender source with the current minifigure and Technic baselines. This is reference-only work in the modeling workflow, not a third production workflow. No replacement model is requested.

## Kind and model/reference links

Kind: shared reference revision. Source: `sources/reference/donor-campaign-v10/yangliu-source-v10.blend`; identity and historical provenance in `manifests/reference.json`. Linked variant records: `model-minifigure-v10` and `model-technic-v2`.

## Applicable shared features

Map campaign/subject features and source artwork to both variants. Preserve exact source hashes and source authorship. Inspect the retained Blender source and generation recipes before asserting its acceptance or compatibility.

## Accepted deviations

The handoff explicitly states that the outputs have not been demonstrated to share one fully synchronized reference revision. Preserve variant-specific accepted features and any previously accepted departures without asking for unchanged features again.

## Pending changes and hold release

The hold is a declared deferred reconciliation, not a tool release dependency. Clear it when the next operator scopes the actual feature comparison from retained evidence and is ready to dispatch that design work. Do not silently clear it as part of bootstrap.

## Acceptance criteria

**AC-1 — The existing reference source and provenance survive.** Verified by: `manifests/reference.json` hashes and retained Blender bytes, not a fabricated new mesh.
**AC-2 — Each variant has an exact reference relation.** Verified by: a future feature-by-feature reconciliation identifying applicable features, accepted deviations, pending changes and hashes. Currently unresolved.

## Final and limits

Reference-only output contract: Blender source, view, provenance, feature change record and scoped review. No MPD is required. A newly accepted reference revision does not update or approve either LEGO assembly.

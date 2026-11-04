---
title: Adopt accepted 348-piece minifigure baseline
status: done
source: Authorized 2026-11-03 DSS bootstrap handoff
started:
completed:
verdict:
score: 0.5
worktree:
issue:
pr:
mod-block: 
id: 3qfact42v2fae127r5s0650g
---

## Brief

One-time retrospective adoption of the existing accepted 348-rigid-piece minifigure model. No design or review stage was run through Spacedock. The handoff explicitly authorizes adoption of the accepted baseline, with existing engineering limits. Unknown historical approval timestamps remain unknown; blank verdict is intentional.

## Kind and model/reference links

Kind: LEGO minifigure variant. Set: DSS Taipei Current / Democratic Service Ship / 洋流號. Immutable identities: `manifests/minifigure.json`, `manifests/reference.json`, and `manifests/adoption.json` on main.
Authored source SHA256: be5a93440d508627b6aeb1a1ccb7099d7d50f3efecf45d1d9bc6d3ee6f223464.
Compiled model SHA256: 49b6a0d3eb138e4f456084714d7cbf0422da8b8209ed500d057447dd9a6021a0.
Accepted published MPD SHA256: 963953af7cd31d23d4adbfa8314b8cde23505d1fb5485da17950872c2cd6d1e2.

## Applicable shared features

Campaign/reference semantics and source Blender survive separately from LEGO assembly geometry. The current accepted features include the preassembled figures placed last, no 小英 bottom plate, shield as one component, and readable two-sided banner with the specified bubble tails. Viewer animation is presentation evidence only.

## Accepted deviations

Existing accepted poses and colors are retained unchanged. Association with the donor-campaign-v10 Blender reference is retained as a source pointer, not asserted as demonstrated synchronization.

## Pending changes

Reference reconciliation belongs to `reference-reconciliation`. No geometry change is part of adoption. A changed model requires a new linked revision; do not reopen this historical acceptance.

## Tooling dependencies

StudFleet old modified binary import is import-only proof. Current intake and exact occurrence crosswalk are under `evidence/bootstrap/` and `migration/minifigure-v10/`. Shared tool upgrades must be separately identified and checked. Construction profile coverage is 7 of 87 types, distinct from catalog coverage.

## Review notes

The historical acceptance is transferred from the complete user handoff in `sources/provenance/` or the handoff provenance listed by `manifests/adoption.json`. No new independent model review or physical build trial was performed. Retained external shield/prefix/sweep evidence retains its original scope.

## Acceptance criteria

**AC-1 — Exact accepted geometry is retained.** Verified by: source/MPD hashes in `manifests/minifigure.json`, fresh import output and occurrence crosswalk; a changed pose or occurrence must fail equality.
**AC-2 — Adoption preserves the original claim limits.** Verified by: source handoff, retained original review records and `manifests/adoption.json`; no record of a new review is created.

## Final and limits

Terminal means historical adoption filed, not stages replayed. Local model acceptance grants neither instruction acceptance nor physical-strength certification. Legacy instruction edition: `docs/instructions` / `legacy-minifigure-v10`.

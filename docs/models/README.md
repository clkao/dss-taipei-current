---
commissioned-by: spacedock@0.28.0-pre0
state: .spacedock-state
entity-type: model_revision
entity-label: revision
entity-label-plural: revisions
id-style: sd-b32
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: brief
      initial: true
    - name: design
      worktree: true
    - name: model-review
      fresh: true
      gate: true
      feedback-to: design
    - name: done
      terminal: true
---

# Model revisions

Own the shared subject/reference design and the separate minifigure and Technic interpretations. A reference-only revision and a LEGO variant revision use this same lifecycle with different artifact contracts. The set remains one long-lived identity. Instruction generation is not required.

## File Naming

Each revision is a folder named by a lowercase hyphenated slug, with `index.md` as its tracker.
Mutable trackers and review records live in `.spacedock-state`; authored artifacts and immutable manifests live on main.
Use temporary per-revision branches/worktrees, never permanent model/instruction branches.

## Schema

| Field | Type and meaning |
| --- | --- |
| id | Stable 24-character SD-B32 identifier minted by `spacedock new`. |
| title | Human-readable revision or edition title. |
| status | A stage named in this README. |
| source | Origin of the request or historical adoption authority. |
| started, completed | Actual workflow timestamps; leave unknown historical dates blank. |
| verdict | PASSED or REJECTED after an actual review; blank on retrospective adoption without a Spacedock review. |
| score | Priority from 0.0 to 1.0. |
| worktree | Temporary worker checkout, retained across review until durable artifacts are preserved. |
| issue, pr | Optional external references. |
| mod-block | Dispatch hold; `dependency:` records unresolved prerequisites, cleared only with cited evidence. |

Subject kind, variant, reference revision, linked model/edition, artifact hashes, deviations and dependencies belong in the body and versioned manifests. They are not custom engine frontmatter.
Use `spacedock new --workflow-dir docs/models --folder SLUG` with a complete stdin stub to create revisions. Never mint IDs manually. Validate before trusting state.

## Stages

### `brief`

Record one reference or variant revision and its scope.

- **Inputs:** Set identity, retained source, previous decisions and requested changes.
- **Outputs:** A bounded reference-only or LEGO-variant brief; applicable shared features, protected unchanged features, acceptance criteria and linked tool prerequisites.
- **Good:** Preserves acceptance of unchanged features at the exact revision.
- **Bad:** Treating each image as a new task or silently requiring instructions.

### `design`

Create or revise source and collect scoped evidence.

- **Inputs:** Brief, exact shared reference pin or explicit unresolved association, catalog and tool pins.
- **Outputs:** Reference-only: retained Blender source, provenance, views and feature change record; no MPD required. LEGO variant: exact authored model, MPD/intake, occurrence inventory, views, scoped checks and deviations.
- **Good:** Independent reference and variant revisions survive worktree cleanup.
- **Bad:** Changing poses for importer convenience or equating mesh appearance with buildability.

### `model-review`

A fresh reviewer evaluates the exact revision; rejected findings return to design.

- **Inputs:** Candidate identities, brief, prior acceptance scopes and check reports.
- **Outputs:** Independent findings with reproduced applicable import/inspect/preview evidence and separate appearance, connection, collision, insertion, manufacturing and physical limits. Triage each finding before correction.
- **Good:** Missing backend coverage stays unresolved; unchanged evidence is reused only within its scope.
- **Bad:** A failed backend becomes a pass or reference acceptance silently approves both variants.
- **Gate content:** Show exact artifact and source hashes, working views/package access, independent findings, acceptance criteria, reused acceptance scope and unresolved evidence. The captain decides whether this exact revision is accepted or returns for correction. No automatic production approval.

### `done`

Retain the accepted model or explicitly scoped historical adoption.

- **Inputs:** Exact acceptance authority, revision artifacts and unresolved limits.
- **Outputs:** Immutable retained handoff manifest linking source, checks, reference relation and scoped acceptance.
- **Good:** A future instruction edition can pin the model without changing it.
- **Bad:** Claiming instructions or physical strength were certified by model acceptance.

## Workflow-specific rules

- **Human-in-the-loop quality bar.** The captain owns acceptance. Independent review makes a recommendation with concrete findings; silence is not approval. No cosmetic stage may introduce unreviewed substance.
- **Repo mutation layer.** Design/authoring uses isolated temporary worktrees. Retain accepted artifacts before cleanup. Reviews use a fresh worker against exact candidate bytes.
- **Local delivery.** No PR merge mod: this set uses local delivery and the no-mod terminal ceremony. Publication has separate authority and never runs as a workflow side effect.
- **Historical adoption.** Seed records may start terminal only as explicit administrative adoption of existing scoped authority. Blank verdict and dates do not imply stages ran. Never fabricate a gate or backdate a review.
- **Dependency holds.** Any nonempty `mod-block` prevents dispatch. The body names the owner, blocked outcome, minimum evidence and release condition. Existing StudFleet dev tasks are read-only dependencies; source branches under review are not usable releases.
- **Reference consistency.** Record shared reference revision and applicable features, accepted deviations, pending changes and source hashes for each variant. An unresolved legacy association is explicit; reference changes never propagate silently.
- **Checks.** On each material LEGO candidate and independently at review, use shared catalog import/inspect/preview. Request `--connectivity pyldraw3` with pinned archive, Shadow and Python. Diagnose unmatched/potential contacts and use local pair controls. Connectivity, collision, insertion, manufacturing and physical strength are distinct. A reference-only revision needs no LEGO checks.
- **Tool boundaries.** Shared fixes stay in StudFleet docs/dev. The old modified binary only proves the commands actually exercised. Eleven construction profiles covering seven of 87 part types do not imply the other 80 lack catalog render or connector metadata. Technic exceeds the connector backend's 500-occurrence cap.

## Workflow State

State uses the orphan branch `spacedock-state/models` in this repository, mounted at `docs/models/.spacedock-state`.
For a clone with the state branch available, run `spacedock state init --workflow-dir docs/models`.
Use `spacedock status --workflow-dir docs/models --validate` and `spacedock status --workflow-dir docs/models --next`.
Resume with `spacedock codex` and `engage docs/models`. Inspect dependency holds before dispatch.

## Revision Template

```yaml
---
title: Concrete revision title
status: brief
source: Request or exact historical authority
started:
completed:
verdict:
score: 0.5
worktree:
issue:
pr:
mod-block:
---
```

Body sections: Brief; Kind and model/reference links; Source and artifact identities; Applicable shared features; Accepted deviations; Pending changes; Tooling dependencies; Review notes; Acceptance criteria; Final and limits.
Each acceptance criterion states a finished property with `Verified by:` a concrete artifact or exercise that can fail, rather than its own prose.

## Commit Discipline

Commit entity creation and lifecycle mutations with `spacedock state commit SLUG --workflow-dir docs/models`.
Commit substantive worker reports on their owning state branch and source artifacts on main or the temporary worker branch.
Keep state commits separate from source commits and preserve historical evidence.

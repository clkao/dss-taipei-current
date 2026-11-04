---
commissioned-by: spacedock@0.28.0-pre0
state: .spacedock-state
entity-type: instruction_edition
entity-label: edition
entity-label-plural: editions
id-style: sd-b32
stages:
  defaults:
    worktree: false
    concurrency: 1
  states:
    - name: intake
      initial: true
    - name: authoring
      worktree: true
    - name: instruction-review
      fresh: true
      gate: true
      feedback-to: authoring
    - name: delivered
      terminal: true
---

# Instruction editions

Consume an immutable accepted variant model, author construction intent and reader presentation, and deliver an independently reviewed local package. Publication is separate. Several editions may share one model revision.

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
Use `spacedock new --workflow-dir docs/instructions --folder SLUG` with a complete stdin stub to create revisions. Never mint IDs manually. Validate before trusting state.

## Stages

### `intake`

Bind one instruction edition to an immutable accepted variant model.

- **Inputs:** Accepted model revision and acceptance scope, prior legacy plan and desired edition outcome.
- **Outputs:** Model hash pin, one authoritative construction-plan source, occurrence/operation crosswalk requirements and relevant dependency holds.
- **Good:** Multiple editions may consume the same model revision.
- **Bad:** Using an unaccepted prototype or a moving reference as the edition input.

### `authoring`

Author and optimize construction intent and reader presentation.

- **Inputs:** Frozen assembly, one-way imported plan, presentation intent and supported shared tools.
- **Outputs:** assembly.json with exact geometry; plan.json with operations, dependencies, units and copies; presentation.json with grouping, views and text; exact output package and parity evidence. Unsupported intermediate schemas are explicitly labeled and not fed as supported plans.
- **Good:** Repeated recipes use exact copy maps; supplied figures are represented as supplied units when supported.
- **Bad:** Fake simultaneous groups, a second hand-maintained sequence, invented approach vectors or captions hiding tray defects.

### `instruction-review`

A fresh reviewer checks the complete exact local package and routes corrections.

- **Inputs:** Frozen edition, immutable model, original manual and artifact/readability evidence.
- **Outputs:** Independent inventory/plan correspondence, every PDF page at A4, main/local viewer paths and every major join; findings classified before repair. Plan/view/text corrections return to authoring; model defects link a new model revision in docs/models and block this edition.
- **Good:** Visual/readability parity is demonstrated, beyond matching page or part counts.
- **Bad:** Publication before exact-package acceptance or silently changing accepted model geometry.
- **Gate content:** Show exact artifact and source hashes, working views/package access, independent findings, acceptance criteria, reused acceptance scope and unresolved evidence. The captain decides whether this exact revision is accepted or returns for correction. No automatic production approval.

### `delivered`

Retain the accepted local edition, or the explicitly historical legacy delivery.

- **Inputs:** Exact package hashes, authority, provenance and outstanding limits.
- **Outputs:** Durable local delivery record with model pin and reviewed package identity.
- **Good:** Publication is a separate action with applicable authority, using these exact bytes.
- **Bad:** Local delivery treated as permission to publish, purchase parts or claim physical performance.

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

State uses the orphan branch `spacedock-state/instructions` in this repository, mounted at `docs/instructions/.spacedock-state`.
For a clone with the state branch available, run `spacedock state init --workflow-dir docs/instructions`.
Use `spacedock status --workflow-dir docs/instructions --validate` and `spacedock status --workflow-dir docs/instructions --next`.
Resume with `spacedock codex` and `engage docs/instructions`. Inspect dependency holds before dispatch.

## Revision Template

```yaml
---
title: Concrete revision title
status: intake
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

Commit entity creation and lifecycle mutations with `spacedock state commit SLUG --workflow-dir docs/instructions`.
Commit substantive worker reports on their owning state branch and source artifacts on main or the temporary worker branch.
Keep state commits separate from source commits and preserve historical evidence.

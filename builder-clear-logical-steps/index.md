---
title: Show clear logical construction steps and hidden attachment details
status: instruction-review
source: Captain requested fresh experienced-builder review and next improvement round; no page-count shortcut or oversized steps
started: 2026-11-05T11:00:32Z
completed:
verdict:
score: 0.94
worktree: .worktrees/spacedock-ensign-builder-clear-logical-steps
issue:
pr:
mod-block:
id: czrrfahe7jyh39409x9jnf6r
review-round:
    id: round:czrrfahe7jyh39409x9jnf6r:instruction-review:2
    stage: instruction-review
    cycle: 2
    briefing:
        id: briefing:czrrfahe7jyh39409x9jnf6r:instruction-review:round-2
        digest: sha256:547a4206c1d46db3ddeea8172837815371810abf7ab7129795b962254dd5a77d
        room-ref: '@review/instruction-review/round-2'
gates:
    version: 1
    records:
        - id: gate:czrrfahe7jyh39409x9jnf6r:instruction-review
          stage: instruction-review
          attempts:
            - id: gate-attempt:czrrfahe7jyh39409x9jnf6r-instruction-review-1
              briefing:
                id: briefing:czrrfahe7jyh39409x9jnf6r:instruction-review:attempt-1:revision-1
                digest: sha256:fd9bea1525ca78db0fbbe5c6d8b7955336f3829961c71f10e70871d4d589c68a
                room-ref: '@review/instruction-review/briefing-1'
              resolution:
                type: Resolution
                id: resolution:spacedock:czrrfahe7jyh39409x9jnf6r:instruction-review:1
                briefing: briefing:czrrfahe7jyh39409x9jnf6r:instruction-review:attempt-1:revision-1
                by: person:captain
                at: "2026-11-05T16:00:58.418097Z"
                decision: revise
                reason: 'Captain accepts the clarity direction but requests revision: replace suspension crossed A/B matching with a clearer diagram-led placement explanation, informed by typical LEGO conventions; page36 callout must identify the actual assembly area rather than the whole model. Preserve source/stock/order and return the exact revision for review.'
---

## Brief

Produce the next locally authored DSS instruction edition so an experienced LEGO builder can identify parts, receiving points, orientation, order and quantity without reconstructing hidden construction from finished views. This is a new edition after delivered a3, not reopening its historical approval. Captain explicitly asked to file and dispatch this round. No publication authority for this new exact package is inferred.

A logical step has one clear, verifiable construction result. Neither fewer pages nor fewer numbered steps is a target. Do not pack two steps onto a page or hide unrelated tasks in a large step with many substeps to reduce totals. Combine only when the grouping makes construction easier; split when focus, receiving location, orientation or assembly phase changes. Preserve useful simple numbered diagrams and proven repeated recipes; do not mechanically split every operation.

## Kind and model/reference links

Instruction edition consuming the unchanged accepted minifigure model used by a3. Source/model/poses/colors/stock remain immutable. A genuine model defect must be reported and linked to docs/models, not repaired in this edition. Shared reference reconciliation remains unresolved. This is DSS local authoring; StudFleet metadata/native work is not a dependency and must not be dispatched or edited here.

## Source and artifact identities

Published predecessor gh-pages b0b679a1de34a4141ea4e326118cf4dcde22e731; main delivery merge c15aa9b96302058cdf4bcbbdf8b143de558b96de; release record evidence/releases/a3-simplified-69-live.json. Exact 69-page PDF SHA256 5c347b0e5d639a5ed5f45be6e867a14772fa01ed92ec4c80b472f956bbcf7bbd. Model SHA256 3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229; plan df9ef0bf23d3f1ab71ac98dbe8dc351073658f241b7f705bf84a991cc412d9ff. Viewer 4802fff8c4c9e29828dbf9cdee48a2e945c96934a4a0fc70475962c99dcdd068. Verify actual pins before use.

Read-only predecessor author worktree: /Users/clkao/git/spacedock-research/dss-taipei-current/.worktrees/spacedock-ensign-minifigure-access-correction. Existing final package builds/simplification-package-retry1. All-page rasters builds/simplification-i3/a4-review with FINAL replacements 45/56/57 under builds/simplification-i3-polish/a4-review. Do not duplicate release bundles, archives or prior evidence. Publication worktree .worktrees/publication-access-corrected is read-only for this stage.

## Fresh reader findings and authorized correction scope

Fresh independent reader Ptolemy reviewed all 69 actual pages of the exact published PDF, without prior review reports, live-viewer exercise or physical build. These are visual ambiguity findings, not physical impossibility claims. Preserve the following source-bound triggers and reconcile them against actual source before correction:

1. HIGH, PDF19-20 steps14/15: eight 6141 round plates per tray; underside perspective hides receiving locations and stack heights. Show all locations and count per stack with an underside/attachment closeup.
2. HIGH, PDF41 step41: dashboard, two grilles, steering base/wheel and seat are obscured by cabin walls. Separate logical actions as needed; use an overhead view and steering inset rather than one overloaded final view.
3. HIGH, PDF58 step64: cord caption does not identify four rings, routing or endpoints. Show numbered receiving points, visible contrasting route and end/knot detail only as supported by source; unknown length/slack stays unknown.
4. MEDIUM, PDF8 step4 and PDF33 step26: missing parts trays or explicit repeat/allocation references. Make stock and repeat ownership unambiguous.
5. MEDIUM, PDF9-12 steps5-8: suspension module receiving holes hidden by installed modules. Show mating correspondence with separated presentation views and matching targets, without invented physical insertion claims.
6. MEDIUM, PDF60 step67: helm figure foot studs hidden. Show platform attachment closeup; investigate whether removal is actually necessary, do not infer it from occlusion.
7. LOW, PDF24/26 carriers17/18: numbering jumps .9 to .13 with no explanation that .10-.12 belong to shared recipe. Use continuous reader numbers or explicit completed-recipe reference without changing source operations.

Preserve known good results: PDF45 inner/outer wheel and attachment detail with four risers; PDF21-23 one-copy trays/build quantities/reserved copies; PDF56-57 life-ring and banner context. Audit adjacent pages for the same hidden-context or oversized-step problem; record justified no-change decisions, do not expand into model redesign or arbitrary wholesale reformatting.

## Applicable shared features and dependencies

Use existing demonstrated local/manual/hybrid rendering and retained numbers-only diagram. No native StudFleet adoption claim, migration hold or upstream coordination required. Other project checkouts are read-only. No new standing harness, workflow or gate. Ordinary authorized work in own outputs uses fresh resource guards, not blanket inter-project slot permission. Coordinate only actual shared writable runtime conflicts or observed host pressure.

## Acceptance criteria

**AC-1** The seven findings have explicit source-bound dispositions and corrected readable views where applicable; parts, targets, orientation, order and counts can be identified without hidden-state guessing. Verified by: exact before/after A4 pages and fresh independent reader review, with actual affected viewer paths where changed.

**AC-2** Logical steps each present one clear construction result; unrelated cabin or routing actions are not buried in oversized substep groups; page sharing serves readability rather than a quota. Verified by: reader-step/operation mapping and actual final-page review, including grouping/splitting rationale at changed boundaries.

**AC-3** Immutable model geometry, colors, poses and occurrence identity, unique stock ownership, dependency order, repeat quantities and installed flexible visibility are preserved. Verified by: source/hash and plan/copy correspondence checks plus actual affected receiving/main/return images; physical claims remain explicitly bounded.

**AC-4** The exact new PDF/viewer/package are independently reviewed and version-bound; unchanged evidence is reused only with demonstrated equivalence. Verified by: all final PDF pages at A4, changed viewer navigation and returns, manifest/ZIP member checks and independent instruction-review report. Digital, headless, live and physical evidence remain distinct.

**AC-5** Local generalized instruction rules reflect one verifiable result per step, effective callouts, explicit shared-recipe references and no page/step-count quota. Verified by: application to the concrete before/after edition, not prose presence alone.

## Review notes and limits

Author in an isolated worktree and commit source/evidence locally. You are not alone: preserve peers' edits and all prior publication/evidence. Independent instruction-review and captain acceptance remain required before new delivery/publication. No automatic approval. Start with source reconciliation and the cheapest decisive views, then render only necessary new assets; reuse unchanged exact assets. Use bounded fresh disk/memory checks and preserve actual failures. Do not wait for or alter StudFleet metadata. Report three dispatch outcomes: source-bound correction decisions; clear rendered instruction candidate; exact validation/review handoff.


## Stage Report: authoring

- DONE: Reconcile and disposition all seven fresh reader findings against exact source, preserving model, stock, copies and dependency order.
  Source commit `709069e`; `corrections/builder-clear-logical-steps/REVIEW-HANDOFF.md` maps each trigger, source operation, correction and limit. Both reported missing trays already existed and received clearer allocations.
- DONE: Produce clear logical steps and decisive receiving/attachment diagrams, with no page-count target or oversized substep shortcuts.
  The 80-page candidate separates suspension recipes/attachments and cabin operations, adds four-stack receiver details, numbered cord routing, figure foot detail and explicit completed-carrier references. `author-visual-review.json` records author inspection, not independent acceptance.
- DONE: Deliver exact locally validated PDF/viewer package and source-bound before/after evidence for independent review, without publication or shared-tool changes.
  Package: `.worktrees/spacedock-ensign-builder-clear-logical-steps/builds/clear-logical/candidate`; handoff and exact manifest are committed with the source. PDF `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956`; viewer `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865`; ZIP `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459`.

### Evidence boundaries

- Input/compilation: immutable model and plan hashes match the predecessor. Legacy/manual presentation remains explicit. No native StudFleet adoption claim.
- Artifact verification: `validation.json` checks 348 unique introductions, all 215 operations, changed-step stock/operation correspondence, A4 dimensions, all 80 rasters and every ZIP member. Missing parts, duplicate ownership, changed operation assignments or changed package bytes fail these checks.
- Equivalence: `reuse-check.json` compares 56 retained pages above the renumbered footer. Any artwork pixel change fails the exact comparison. Known-good wheel/riser, carrier recipe, life-ring and banner pages remain equivalent.
- Visual/headless: all 24 changed pages received author image inspection. `final-browser-check.json` records 20 page selections, next/previous, 1400/390-pixel layouts and return from 3D inspection. Failed image loading, horizontal overflow, navigation errors or runtime exceptions fail the exercised checks.
- Human acceptance: pending fresh independent instruction review and captain decision. No reader acceptance or publication authority is inferred.
- Physical limits: source-position markers do not certify connectors or insertion. Figure stud engagement, wheel engagement, cord cut length/slack and knot type remain unverified or unspecified.
- Runtime: default Node had a missing llhttp library; the declared Node 24 runtime succeeded. PyMuPDF was absent; ReportLab/pypdf/Poppler supplied the final process. Only task-owned closed Chrome profiles were removed. Final free disk was about 296 MiB; further rendering needs a fresh guard.
- StudFleet gaps: unchanged. This round changes local instruction presentation and artifact evidence only. No shared tool was tested or modified; full-edition native parity remains open.

### Summary

All seven findings now have source-bound dispositions and an exact local review candidate. The package preserves accepted model bytes, source operations, stock ownership and known-good repeated construction. Independent all-page reader review and captain acceptance remain the next required decisions.

## Stage Report: instruction-review

- DONE: Independently review the exact 80-page candidate for all seven findings and logical-step clarity at A4, using existing rasters and verifying source-bound dispositions; no page-count quota or oversized-step shortcuts.
  Review commit `9d011e1`, `corrections/builder-clear-logical-steps/INDEPENDENT-REVIEW.md`: all 80 A4-layout rasters inspected individually; seven dispositions and grouping decisions recorded. R1–R4 remain; recommendation is return to authoring.
- DONE: Check exact model/plan/stock/copy/flexible-state correspondence and package identity; critically review cutaways and A/B targets for misleading attachment implications, and assess changed viewer paths at their actual evidence level.
  Fresh `independent-check.json` verifies five pinned hashes, 108 manifest members, 348 unique introductions, 215 operations, changed-page allocations and source/plan byte equality; any changed member, duplicate stock or changed allocation fails. Visual checks preserve bands/recipes; R1/R2 reject origin projections as sufficient mating/threading targets.
- DONE: Report every acceptance criterion and concrete findings with severity, source/page evidence and smallest correction; preserve candidate bytes, use existing green evidence without duplicate rendering, and leave physical/live limitations and captain acceptance explicit.
  AC-1 not met; AC-2 met at changed boundaries; AC-3 digitally met with physical limits; AC-4/5 partial. R1/R2 HIGH, R3/R4 MEDIUM, R5 LOW evidence limitation. No candidate mutation or rendering; source/headless screenshot review is not live browser testing.

### Findings for routing

- R1 HIGH: pages 10/12/14/16, operations 17/21/25/29: A/B use new-pin origins, with off-hole/overlapping marks. Use source-derived visible pin-end/hole-mouth targets and a larger unit view.
- R2 HIGH: page 69, operation 210: occluded ring-origin marks appear over speakers/platform. Show the actual four apertures with closeups/leaders and preserve the source route and unknown knot/slack details.
- R3 MEDIUM: pages 24/25, operations 43–46: identical isolated floor plates lack a link to their installed position/orientation. Highlight the corresponding plate/corner in each complete-state locator.
- R4 MEDIUM: page 71, operation 215: foot detail lacks matched receiving targets and omits more structure than its label states. Add paired positions, a landmark/turn cue and complete omission labeling; do not infer removal.
- R5 LOW: recorded mobile fit is not detail readability; recorded 3D return is direct URL navigation. Exercise enlargement and actual link/back paths at the claimed viewing size.

### Evidence boundaries

Exact PDF `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956`; viewer `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865`; ZIP `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459`. Package remains `builds/clear-logical/candidate` in the author worktree. Existing 56-page artwork equivalence and headless results are reused within their actual scope, not upgraded to full-page identity, physical clearance or live user review.

No demonstrated model defect; corrections route to instruction authoring. Historical scoped model acceptance remains separate from this package's pending captain acceptance. No publication authority or physical certification is inferred. StudFleet gaps are unchanged: no shared tool update/test occurred; native full-edition parity remains open.

### Summary

The exact candidate has independently verified digital correspondence and substantially clearer logical grouping. Return it to authoring for visible attachment targets and cutaway orientation fixes before asking the captain to accept the package; no geometry change or wholesale reformatting is needed by these findings.


## Correction round 1: static preparation and resource hold

FO authorized correction of R1-R5 without a captain rejection. Source commit `420c107` derives actual catalog pin ends, beam-hole mouths, four ring apertures and two sole footprints. `corrections/builder-clear-logical-steps/cycle1/RESOURCE-AND-FEATURE-LOG.md` records the proposed changes, source evidence and resource boundary. Prepared jobs and the affected-page composer are not yet executed.

The FO restored the established 512 MiB active disk floor during source investigation. No new render, PDF, ZIP or browser run occurred under the proposed lower floor. Commands only read source/catalog data, created directories and linked the existing catalog. Static derivation and syntax checks followed under the restored rule. Fresh free space remains about 310 MiB, below 576 MiB admission.

All task-owned closed browser profiles were already removed in the prior round. No peer cleanup occurred. Existing unique evidence and artifacts remain preserved. Fresh read-only SHA256 checks confirm that the rejected PDF `db13a653`, viewer `4d6b7902` and ZIP `5c34b1d1` remain unchanged. R1-R5 remain open until rendered corrections, exact successor-package checks and actual enlarged/link/back exercises run after resource recovery. No authoring completion or acceptance is claimed for this correction round.

## Stage Report: authoring (cycle 2)

FO-authorized correction round 1 completed at source commit `92cc98d`, following static source commit `420c107`. This is a response to independent findings, not a captain rejection or acceptance. The original review and rejected package remain intact.

### Completion checklist

- [x] Correct R1-R4 with source-bound actual visible attachment features and matched context/orientation, preserving rejected bytes and immutable model/stock/order.
  - R1: catalog pin-end and beam-hole-mouth leaders, enlarged unit panels, explicit turn; pp10/12/14/16.
  - R2: four actual aperture closeups plus region locator, original cord route; p69.
  - R3: installed-plate blue highlight and matched C corner; pp24/25.
  - R4: same overhead foot views, paired sole regions and helm landmark, accurate enclosure/upper-body omission caption; p71.
  - Verified source records, exact model/plan, all 348 introductions and 215 operations. Unchanged 72 PDF content streams and page rasters match the predecessor exactly.
- [x] Exercise existing enlarged mobile detail and actual link/back navigation for R5 with honest evidence categories and bounded own resources.
  - Actual Enlarge anchor/native image zoom for pp10/24/69/71; actual 3D anchor and browser-history Back to loaded p71. Errors empty. Source-pixel screenshots visually inspected; horizontal scrolling required. Headless 390×900 viewport only, no live human/device test or default-fit detail readability claim.
  - Original resource hold preserved. 576 MiB admission / 512 MiB active guards retained. One archive admission failed before writes; later recovery admitted successful archive creation. No render/package/browser run used the proposed lower floor.
- [x] Return exact revised package, affected visual review and unchanged-content evidence for the kept independent reviewer; no publication or shared-tool work.
  - Package: `/Users/clkao/git/spacedock-research/dss-taipei-current/.worktrees/spacedock-ensign-builder-clear-logical-steps/builds/clear-logical/cycle1/package`.
  - PDF SHA256 `59b66fb0bfb8766306b89475e5516cc0c1a5286605355c760ca578a723530f64`.
  - Viewer SHA256 `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865` (unchanged shell; corrected images separately bound).
  - ZIP SHA256 `635049be41e87e1446500e433d58bece6a77822ddd816677abca4d079a0ecf04`; 109 archive members verified.

### Correction evidence

All source evidence below is under the author worktree `corrections/builder-clear-logical-steps/cycle1/`:

- `REVIEW-HANDOFF.md`: concrete R1–R5 disposition, exact successor and predecessor identities, remaining limits.
- `features.json`, `derive-features.py`, `locator-faces.json`, `ring-locator.json`, `jobs-feet-top.json`: actual feature and orientation correspondence.
- `validation.json`, `package-check.json`, `package-manifest.json`: immutable input, unaffected-content and exact-package verification.
- `browser-check.json`, `mobile-run.json`, `author-visual-review.json`: actual exercises and inspected screenshot hashes. Screenshots remain in `builds/clear-logical/cycle1/browser-review/`.
- `RESOURCE-AND-FEATURE-LOG.md`, `render-run.json`, `feet-top-run.json`, `first-draft.json`: retained hold, failed draft disposition, successful bounded runs. Archive minimum free 794,468,352 bytes; elapsed 1.11 seconds.

Rejected PDF `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956`, viewer `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865`, ZIP `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459` remain unchanged at `builds/clear-logical/candidate`. Review commit `9d011e1` remains unchanged.

### Summary and limits

Eight affected pages now use visible features and matched context. Previously green grouping, cabin, carrier and tray work remains unchanged. The exact successor is ready for the kept independent reviewer. Independent recommendation and captain acceptance remain pending. No publication occurred. Digital feature correspondence does not certify insertion clearance, physical fit or strength. Sole marks identify regions rather than certified stud/cavity centers. Cord knot, cut length and slack remain unspecified. No shared StudFleet update/test ran; DSS tooling gaps and native full-edition parity remain unchanged.

## Stage Report: instruction-review (cycle 2)

- DONE: Re-review corrected R1–R5 against exact source92cc98d cycle1/REVIEW-HANDOFF.md and PDF59b66fb0/ZIP635049be, inspecting all eight affected pages plus actual enlarged/link/back screenshots; preserve your original rejection.
  Review commit `d2c94bb`, `corrections/builder-clear-logical-steps/cycle1/INDEPENDENT-REVIEW.md`: eight page rasters and five browser screenshots inspected; R1–R5 resolved at stated scope. Original rejection and rejected package preserved.
- DONE: Verify exact successor bindings and 72-page/source/stock equivalence at their claimed evidence level without duplicate rendering; distinguish visual features from certified connector/access geometry and headless from human evidence.
  Fresh `cycle1/independent-check.json`: 108 loose members / exact 109 ZIP members, four artifact pins, 72 decoded PDF content streams and raster bytes, immutable model/plan, 348 unique introductions, 215 operations and source feature transforms pass. A changed member, missing introduction or changed retained raster fails these checks.
- DONE: Return a durable independent verdict and all AC dispositions for the exact candidate, identifying remaining material defects or acceptance limits; no candidate mutation, publication or new standing tests.
  PASS for local digital instruction review; recommend captain acceptance review. AC-1–5 met within artifact/visual/headless scope. No remaining material instruction defect found; physical fit/access/strength, live device testing and captain acceptance remain unproved.

### Dispositions and limits

R1: pp10/12/14/16 now identify visible pin ends and beam-hole mouths with enlarged panels and explicit face turn. R2: p69 exposes the four apertures with region locators and source-correct route. R3: pp24/25 pair the installed floor highlight with the same C corner. R4: p71 pairs L/R sole regions in the same overhead view with a helm landmark and explicit omissions. These are source-bound visual correspondences, not certified connector or insertion geometry.

R5: actual Enlarge clicks/native source-pixel zoom, selected-region screenshots, scrolling, actual 3D anchor and browser-history Back supply the missing headless evidence. Screenshots require horizontal scrolling and do not show every detail at once. Three recorded initial-fit widths are 662 pixels; no consistent mobile default-fit or live-phone readability is claimed. Reviewer inspected recorded evidence rather than running a new browser exercise.

The page-map byte-equality assumption initially failed because eight records add correction metadata; independent comparison confirms all previous stock/operation fields remain equal. The 72-page comparison is decoded content-stream/raster equality, not complete PDF resource-object identity. Original all-page inspection supplies the unchanged pages' review scope; no duplicate rendering occurred.

### Exact review target

Package: `builds/clear-logical/cycle1/package` in the author worktree. PDF `59b66fb0bfb8766306b89475e5516cc0c1a5286605355c760ca578a723530f64`; viewer shell `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865`; ZIP `635049be41e87e1446500e433d58bece6a77822ddd816677abca4d079a0ecf04`; manifest `9bd0220666d3d1af4d3d38c495d5a6069d9c6dd8e53ca9998463d8e6250b1310`. The manifest binds corrected page images despite the unchanged viewer-shell hash.

### Summary

The exact successor resolves the original review's visual blockers while preserving source, stock, order and known-good pages. Present it for the captain's acceptance decision; no delivery/publication approval is inferred. StudFleet gap status and native full-edition parity are unchanged because no shared tool update/test occurred; shared-reference reconciliation and physical certification remain unresolved.

## Stage Report: authoring (cycle 3)

Captain revision round2 completed at source commit `9d30303`. Exact feedback is preserved in `corrections/builder-clear-logical-steps/cycle2/CORRECTION-LOG.md`: replace crossed A/B suspension matching with direct diagrams, and point p36's callout to its assembly area. This is the actual gate-attempt1 revise response, not acceptance.

### Completion checklist

- [x] Replace suspension crossed-letter matching with source-bound readable common-frame placement diagrams, preserving canonical poses and honest physical limits.
  - pp10/12/14/16 now show one common-camera placement view, an intact unit separated for display, and two parallel arrows between actual catalog pin ends and beam-hole mouths. A/B labels and matching/turn prose removed. Representative actual pixels inspected before remaining final pages; failed camera/framing/layout specimens retained.
  - `feature-check.json` records parallel projected directions and unchanged source records. Display offsets do not certify insertion motion.
- [x] Fix page36 callout to identify the actual receiving area and apply the generalized placement/callout rule locally with a bounded analogous audit.
  - Step20 operation82 installs rear-bed unit IDs14,33,34,54,58,59,100,109,118 after recipe operations77–81. Rails14/58 align above carrier plates38/81. Final high-angle view exposes plate81's orange top; callout ends inside its localized outline, with rail58 placement arrow. The earlier low-angle hidden-face outlines were rejected and retained as failed evidence.
  - Original recipe panels/tray preserved; x0–519 source-pixel comparison passes. Near changed callout boundary, the wider initial crop had minor JPEG differences; no full-page equality claim.
  - `docs/instructions/README.md` now states common-frame placement and actual-area callout rules. Bounded actual-pixel audit of pp30/32/33/34/35/37/38 found no additional required change; decisions recorded.
- [x] Deliver inspected affected pages and exact successor package/equivalence evidence for the same reviewer and captain gate, preserving all prior versions and no publication.
  - Five affected A4 page images inspected. 75 unaffected PDF content streams and page JPEG bytes match cycle1 exactly. Exact model/plan, all348 unique introductions and all215 source operations preserved.
  - Actual Enlarge/native image zoom for pp10/36 and actual 3D-link/browser-history Back to loaded p36 passed with errors empty. Screenshots inspected; headless390×900 only, horizontal scrolling required. No live-device or default-fit detail readability claim.

### Exact package and review access

Author worktree: `/Users/clkao/git/spacedock-research/dss-taipei-current/.worktrees/spacedock-ensign-builder-clear-logical-steps`.

- Package: `builds/clear-logical/cycle2/package`.
- Before/after: `builds/clear-logical/cycle2/before-after.html`.
- PDF SHA256 `19d5c4262279624e38635367f958fcb9ccd6ffa87ca3b9a8f0da91da87d1716c`.
- Viewer SHA256 `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865` (unchanged shell; each package binds its own image bytes).
- ZIP SHA256 `98fc465d0f6bb04d4eb4100efb2bb40984f9a80469b007e472befe88c5325c00`.
- Manifest SHA256 `a69c695f58b89ffbdd98b66cbe88a6a5ccf2678b4b4427a4421fb4ae637a2ec3`; all109 ZIP members verified.

Evidence root: `corrections/builder-clear-logical-steps/cycle2/`. `REVIEW-HANDOFF.md` is the review entry; `CORRECTION-LOG.md` records feedback/disposition/failures/audit; `feature-check.json`, `receiver-catalog.json`, `author-visual-review.json`, `browser-check.json`, `runtime-evidence.json`, `validation.json`, `package-check.json`, `version-bindings.json` bind actual checks and limits. The provided official LEGO PDF printed14 was inspected as a spatial illustration reference; no reference artwork was copied into delivery.

Reviewed cycle1 PDF `59b66fb0bfb8766306b89475e5516cc0c1a5286605355c760ca578a723530f64` and ZIP `635049be41e87e1446500e433d58bece6a77822ddd816677abca4d079a0ecf04` remain unchanged, as do original rejected PDF `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956` and ZIP `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459`.

### Summary and limits

Direct suspension arrows replace the matching puzzle; page36 points to a visible receiving surface. All previously successful ring/plate/foot/cabin/carrier/grouping fixes remain unchanged. Eight scoped browser/render runs exited0; established576MiB admission/512MiB active guards retained. Archive minimum free5,008,572,416 bytes, elapsed1.08 seconds. No cleanup of peers or shared caches occurred.

Ready for same-reviewer recommendation and captain gate. No publication or acceptance claimed. Physical insertion, grip, strength and manufacturing remain unverified; cord knot/length/slack limits remain. No shared StudFleet update/test ran; DSS tooling gaps and native full-edition parity remain unchanged.

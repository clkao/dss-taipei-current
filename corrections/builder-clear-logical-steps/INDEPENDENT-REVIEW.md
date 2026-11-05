# Independent instruction review

Recommendation: **return to authoring**. The candidate improves logical grouping, but three attachment explanations still require hidden-state guessing. These are presentation findings, not evidence of an impossible physical model. Captain acceptance remains open.

## Exact scope and identity

Reviewed all 80 existing 1200-pixel A4 landscape page rasters individually, including trays, text baked into diagrams, captions, major joins, inventory and print guides. This is screen inspection of A4 layouts, not a printed-sheet or physical build exercise. No candidate bytes were changed and no duplicate rendering ran. Before-page references below are bound to the predecessor PDF in `input-pins.json`; before/after construction correspondence was checked against the retained source and page map. No new predecessor raster pass is claimed.

| Artifact | SHA256 |
| --- | --- |
| Model | `3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229` |
| Plan | `df9ef0bf23d3f1ab71ac98dbe8dc351073658f241b7f705bf84a991cc412d9ff` |
| Predecessor PDF | `5c347b0e5d639a5ed5f45be6e867a14772fa01ed92ec4c80b472f956bbcf7bbd` |
| Candidate PDF | `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956` |
| Page viewer | `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865` |
| ZIP | `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459` |

Package access: `builds/clear-logical/candidate/instructions.pdf`, `viewer.html`, `model-viewer.html`, and `release.zip`. `independent-check.json` records a fresh read-only verification of those five hashes, all 108 manifest members against loose files and ZIP bytes, 348 unique introductions, all 215 operations, changed-page stock/operation coverage, source/plan byte equality and 80 A4 page dimensions. Changing one member, losing or duplicating a stock introduction, or changing a focused page's operation allocation fails these checks. This does not independently establish a raster-to-PDF rendering relation; the existing author rendering evidence supplies that relation.

## Findings and smallest corrections

| ID | Severity | Evidence and reader impact | Smallest correction |
| --- | --- | --- | --- |
| R1 | HIGH | Pages 10/12/14/16, operations 17/21/25/29: A/B circles are projected from origins of new pins, not identified receiving connectors. `render-detail-final.mjs` projects `Vector3(0,0,0)` through the new piece matrix for both before and after images. The jobs use 217/219, 226/225, 220/228, 234/233. On page 16 the A mark is above the beam holes; on page 10 A/B and their letters overlap in the small unit inset. “Match A and B ... to ... frame” implies precise attachment correspondence the diagram has not established. | Mark actual visible pin ends and corresponding beam hole mouths with source-derived leader endpoints; enlarge the separate unit view and separate the labels. Keep the source pose unchanged and do not add a claimed insertion path. If correspondence cannot be resolved from source/catalog, label the unresolved connection explicitly rather than using a false precision cue. |
| R2 | HIGH | Page 69, operation 210: route order 25→70→142→78 is source-correct, but the origin markers do not visibly identify all ring apertures. In the upper-right view 4 appears on/near the speaker; in the lower-right view 1 does likewise. The top-view 1/4 markers sit over white platform structure while the cord runs outside the body. An occluded origin projected through the vehicle is not a readable threading target. | Add closeups of the actual four 4081b ring apertures with leader lines and a complete-model locator. Mark the cord entering/exiting the visible rings. Retain unknown cut length, slack and knot type; no invented knot geometry is needed. |
| R3 | MEDIUM | Pages 24/25, operations 43–46: counts and two-layer stacks are clear, and omission is explicitly disclosed. However the isolated 3036 rectangles have no front/rear cue, and the small complete-state locator has no highlighted plate or connection to the detail. The two pages use opposite pairs of corners on otherwise identical plates. A reader must infer which installed floor plate and orientation is intended. | Highlight the relevant plate in each existing locator and add a matching corner/front cue in the detail. Keep the receiving plate visible in the full assembly; retain bands in the locator. |
| R4 | MEDIUM | Page 71, operation 215: the bare foot/deck cutaway omits the helm and enclosure as well as the upper body; only the upper-body omission is labeled. It is presented at a different orientation from the overhead receiving view, with no matching foot targets or orientation cue. The result locator shows the complete figure but does not identify exact foot positions. | Put matching foot-position marks on the overhead view and detail, retain a recognizable helm/platform landmark or a clear turn cue, and label all deliberately omitted installed structure. Preserve the stated uncertainty about stud engagement/access and do not instruct removal without evidence. |
| R5 | LOW | Existing headless browser evidence checks 390-pixel horizontal fit, not readable construction details. The inspected `guide-390.png` makes the tray labels and targets too small to read at default fit. `review.mjs` navigates directly to the 3D file and back to a constructed URL, rather than exercising the link and browser history. | Exercise “Enlarge page” and the actual 3D link/back path at mobile size after the drawing corrections. Report readability only for the enlarged state actually inspected. This is an evidence limitation, not a new claim that navigation is broken. |

All findings route to instruction authoring. No demonstrated geometry defect requires a model revision. R1/R2 cannot be closed by a disclaimer in the handoff; the actionable diagram needs a visible, correctly located receiving feature.

## Disposition of the seven original findings

| Original finding | Source / before → candidate | Independent disposition |
| --- | --- | --- |
| Eight floor spacers | Operations 43–46; 19–20 → 24–25 | Quantity/layers improved; R3 remains for installed-plate orientation. |
| Cabin overload | Operations 124–126; 41 → 49–51 | Corrected at visual level: separate dashboard/grilles, steering and seat results; trays match each operation. Floor/support landmarks remain in the labeled cutaway, and both grilles are visible. Wheel angle is shown; engagement remains unverified. |
| Cord route/endpoints | Operation 210; 58 → 69 | Route/order and source limitations improved; R2 remains for visible ring identification. |
| Missing trays | Operation 13 and 93–94; 8/33 → 8/40 | Source reconciliation confirms existing stock, now clearly allocated: two 3460 plates and six right-panel parts in five lots. No new or duplicate stock. |
| Hidden suspension receiving holes | Operations 14–29; 9–12 → 9–16 | Recipe versus placement split is useful, but R1 prevents closure of mating correspondence. |
| Helm figure feet | Operation 215; 60 → 71 | Foot view added; R4 remains for mapping its pose to the receiving platform. No removal or physical-access result is inferred. |
| Carrier numbering jump | Shared C17/C18 recipes; 24/26 → 30/32 | Corrected: explicit .10–.12 recipe reference explains the jump. Branch-specific recipe order and reserved copies remain intact on pages 27–29. |

## Acceptance criteria

| Criterion | Result | Evidence and boundary |
| --- | --- | --- |
| AC-1 | Not met | All seven have source-bound dispositions, but R1–R4 leave attachment targets/orientation ambiguous. |
| AC-2 | Met for changed boundaries | Suspension recipes and joins have distinct pages; cabin operations 124/125/126 have distinct results; cord routing has its own page. Four two-plate spacers form one understandable repeated result. No page-count quota was used. |
| AC-3 | Met for immutable digital source and stock; physical limits open | Fresh hash/Counter checks preserve exact source, poses, colors, introductions, operation membership and copy metadata. Visual inspection finds bands retained in complete chassis views/locators and explicit cutaway omissions. Exact connector engagement is not proved by the targets. |
| AC-4 | Partial | Exact package and all pages independently inspected; prior 56-page pixel-equivalence evidence reused, not rerendered. Changed viewer is assessed through source, recorded headless checks and desktop/mobile screenshots. No fresh live browser or physical exercise; R5 bounds the claimed navigation/readability evidence. |
| AC-5 | Partial | One-result grouping is demonstrated by cabin/suspension changes and the shared-recipe reference is effective. Callout/locator implementation still fails R1–R4. Existing workflow rules require the appropriate behavior; prose presence does not close these findings. |

## Complete-page and adjacent audit

Pages 1–8: orientation, inventory conventions, chassis core and allocated step-4 tray inspected. Pages 9–17: four recipes, their receiving views and installed bands inspected; R1. Pages 18–26: dishes, bumper sequence, floor and spacers inspected; R3. Pages 27–33: shared recipes, distinct C branches, reservations and later carrier joins inspected. Pages 34–48: arches, body layers, tailgate, front assembly and cabin floor inspected; no additional correction is required by this bounded review. The existing whole-model body views remain less explicit than the new cabin details, but no new source-bound defect is asserted merely from page sharing.

Pages 49–54: cabin split and subsequent glazing/roof closure inspected. Page 55 preserves wheel inner/outer faces and all four risers. Pages 56–65: platform, helm, shield approach, speakers and masts inspected; existing approach depiction is not new clearance proof. Pages 66–68 preserve life-ring/banner context and clear-film instruction. Pages 69–71 carry R2/R4. Pages 72–80: print guides, six inventory pages and physical-test limits inspected; no new clipping or missing inventory panel found. Existing 56-page artwork equivalence excludes the bottom 65 pixels, so it is not full-page byte equality.

The immutable source preserves repeated construction and dependency order; the checks do not certify that every suggested manual motion is physically possible. Historical appearance/geometry acceptance remains scoped to its earlier exact configurations. This review neither renews physical certification nor accepts this package on the captain's behalf. Publication remains unauthorized for this candidate.

StudFleet gap status is unchanged: no StudFleet update or shared tool test occurred. Local artifact correspondence is independently verified; local visual clarity remains open on R1–R4, live/enlarged-view evidence on R5, human acceptance pending, and full-edition native parity unresolved.

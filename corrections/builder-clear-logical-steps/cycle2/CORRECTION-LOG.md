# Captain revision — correction round 2

The captain closed gate attempt 1 with revise. Exact feedback:

1. “Attach the completed suspension unit - are there better way with just diagram, not crossing A & B? what does typical lego instruction do?”
2. “p36 callout -> should indicate the area it is assembled, not the whole model”

The FO authorized this bounded presentation correction in the existing worktree. No model defect, publication authority or acceptance was inferred.

## Disposition

- Suspension pp10/12/14/16: FIXED for re-review. One common-camera diagram shows the completed unit in its canonical orientation, separated only for display. Two parallel placement arrows connect the actual catalog pin ends to beam-hole mouths. A/B labels, opposing-face panels and matching/turn prose are gone. The image is a local crop of the receiving chassis. It does not certify an insertion path.
- Page36: FIXED for re-review. The existing two recipe panels and parts tray remain. A higher receiving view exposes the orange top surface of side-carrier plate81; the callout ends on that surface, inside its local outline. One downward arrow links rear-bed rail58 to that visible receiver. No target is drawn over the occluded near plate38. The surrounding vehicle provides context.
- Local workflow rule: `docs/instructions/README.md` now requires common-frame placement correspondence where useful and callout endpoints on actual assembly areas/features. No shared tooling/schema change.

## Source mapping

Suspension operations17/21/25/29 retain source unit membership and the catalog pin-end/hole-mouth derivation from `../cycle1/features.json`. Display offsets are ±120 LDU on source Z, applied through the existing renderer's presentation-only offsets. The two projected directions are parallel; `feature-check.json` records the measured cross products. Canonical piece JSON remains unchanged.

Step20 operations77–81 build IDs14,33,34,54,58,59,100,109,118; operation82 installs that rear-bed unit. Rails14/58 lie over side-carrier plates38/81 and the rear-arch region24/77. Carrier plates38/81 were installed in steps17/18, arches24/77 in step19. Rail underside `[40,8,0]` and plate top `[-20,0,0]` align within 0.00001 scene units after removing the display offset. The final visible callout uses plate81; its top rectangle comes from the 3666 plate footprint, not a whole-model bounding box. Display offset `[0,-120,0]` lifts the intact bed for illustration. It is not a tested physical trajectory.

The provided official LEGO PDF was inspected at printed14: a subassembly callout points into its assembly area. `reference-check.json` binds the URL and reference PDF hash. The reference informed the spatial explanation; no LEGO artwork or specific layout was copied into the package.

## Actual iteration and failures

All earlier views remain under `builds/clear-logical/cycle2/`:

- `suspension-specimen`: three initial angles; pin-end occlusion made them unsuitable.
- `suspension-specimen2`: side-biased angles exposed both pin ends. Used to choose the representative orientation.
- `representative`: local framing had excess blank space because `pieceBounds` already reflected the display offset. Removed the extra offset from the bounds calculation; canonical source was unaffected.
- `representative-fit`: final step5 render. First composed `package/specimen.png` overlapped the title; resized the image in the page layout. `package/specimen-final.png` shows the corrected representative inspected before final handoff. The initial specimen PDF was a regenerable draft; the failed raster is preserved.
- `remaining`: other three suspension joins and first rear-bed view. No green views were rerendered for status.
- `bed-final`: the low view placed projected receiver outlines over occluding bracket faces. Rejected as misleading; the raster and `package/page36-draft.png` remain.
- `bed-overhead`: exposes plate81's top. The final page uses only that visible receiving outline/arrow and omits the hidden near-face target. `package/page36-overhead.png` retains the final inspection raster.
- A shell command with an unmatched quote failed before executing; corrected invocation succeeded. No package mutation occurred from that failed command.
- The initial 530-pixel-wide page36 comparison found JPEG differences only at x527–529/y495–511, next to the changed callout boundary. Exact recipe/tray comparison uses x0–519, including all recipe images and tray content; it passes. This narrow comparison is not full-page identity.

`runtime-evidence.json` records actual admission, minimum free space, elapsed time and exit for each run. All eight guarded browser/render runs exited0. The established 576 MiB admission / 512 MiB active floor remained in force. No cache or peer cleanup occurred in this round. Package composition and archive checks also retained these floors.

## Bounded analogous audit

Actual existing pixels inspected: pp30/32 carrier details already have local region boxes; p33 vehicle attachment has enlarged receiving structure with supplementary boxed locator. No change. Page34 uses direct wheel-arch emphasis, p35 is recipe-only, and pp37/38 use direct construction panels without detached callout pointers. No further analogous defect was established in this local sweep. This is not a new whole-book visual audit.

## Verification and limits

All five affected A4 page images were inspected. Native browser image enlargement at 390×900 was exercised for pp10/36 and inspected at source pixels. Horizontal scrolling is required; the screenshots show selected regions. Actual 3D-link/history Back returned to loaded p36 with errors empty. This is headless evidence, not human/mobile-device testing or default-fit detail readability.

`validation.json` proves exact immutable model/plan, 348 unique introductions, 215 source operations, 80 A4 landscape pages, 75 unchanged PDF content streams and page-image bytes. `package-check.json` verifies all109 ZIP members. `version-bindings.json` binds the original rejected package, reviewed cycle1 and successor cycle2. Prior ring, plate, foot, carrier and cabin fixes remain unchanged. No source geometry, color, stock, order or copy metadata changed.

Independent review and captain acceptance remain pending. Physical insertion, strength, grip and manufacture are not certified. Existing cord knot/length/slack limits remain. No StudFleet update or test occurred; shared tooling gaps and native full-edition parity remain unchanged.

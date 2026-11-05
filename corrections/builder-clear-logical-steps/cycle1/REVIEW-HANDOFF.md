# Correction round 1 — ready for independent re-review

This is the FO-authorized correction of reviewer R1–R5, not a captain rejection or acceptance. Original review commit `9d011e1` and `../INDEPENDENT-REVIEW.md` remain unchanged. No publication occurred.

## Exact successor

Package: `/Users/clkao/git/spacedock-research/dss-taipei-current/.worktrees/spacedock-ensign-builder-clear-logical-steps/builds/clear-logical/cycle1/package`. Open `viewer.html` or `instructions.pdf`; `release.zip` is standalone.

- PDF SHA256: `59b66fb0bfb8766306b89475e5516cc0c1a5286605355c760ca578a723530f64`
- Viewer SHA256: `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865` (unchanged shell; corrected page images are bound by manifest)
- ZIP SHA256: `635049be41e87e1446500e433d58bece6a77822ddd816677abca4d079a0ecf04`
- Manifest SHA256: `9bd0220666d3d1af4d3d38c495d5a6069d9c6dd8e53ca9998463d8e6250b1310`

`package-check.json` verifies 109 archive members. `validation.json` verifies all 108 loose members, 80 A4 landscape pages, unchanged model/plan, 348 unique introductions and all 215 source operations. This is artifact verification, not human acceptance.

## Actual disposition and evidence

| Finding | Correction and author result | Evidence |
| --- | --- | --- |
| R1 HIGH | Replaced origins with catalog pin ends and beam-hole mouths. Enlarged paired unit/receiver views show A/B leaders on visible features; inside/outside face turn is explicit. Author visual check ready for review on pp10/12/14/16. | `derive-features.py`, `features.json`, `jobs.json`, package pp10/12/14/16; `builds/clear-logical/cycle1/renders/receiver-locations.json` |
| R2 HIGH | Four closeups point at actual 4081b apertures. Whole-model locator boxes identify clip regions, not claimed aperture points. Source cord route retained; knot and length unknown. White badges improve contrast. Author check ready on p69. | `features.json`, `ring-locator.json`, package p69, rendered ring1–4 closeups |
| R3 MEDIUM | Blue display overlay highlights installed rear/front plate; C marks match the same source front corner in locator and underside views. Installed bands remain. Author check ready on pp24/25. | `derive-locator-faces.py`, `locator-faces.json`, package pp24/25 |
| R4 MEDIUM | Same overhead camera for both foot panels, paired L/R sole footprint regions and retained helm wheel. Caption states enclosure and upper body omitted and kept assembled. First oblique draft improved before handoff. Author check ready on p71. | `jobs-feet-top.json`, `features.json`, `first-draft.json`, `builds/clear-logical/cycle1/renders-feet-top`, package p71 |
| R5 LOW | Actual Enlarge anchors clicked for pp10/24/69/71, native image clicked to 1200-pixel width, scrolling exercised. Actual 3D anchor clicked; browser history Back returned to loaded p71. Enlarged screenshots inspected and details readable. | `browser-check.json`, `mobile-run.json`, `review-mobile.mjs`, `author-visual-review.json`, `builds/clear-logical/cycle1/browser-review/*.png` |

R5 is headless Chrome at a 390×900 viewport using native browser image zoom. Horizontal scrolling is required. It is not a live phone/user test, and default-fit detail readability is not claimed. Captured screenshots show selected source-pixel viewport regions, not every detail at once.

## Preserved predecessor and unaffected content

Rejected package remains at `builds/clear-logical/candidate`:

- PDF `db13a65349791ea4af2644df5cff26afd1a1bc29a218ec9f1df95983fca02956`.
- Viewer `4d6b790223e3a666ba1c3d6dc7b3fe88dc5dc5d3803b59bdf03e1bf7c7b84865`.
- ZIP `5c34b1d1783d4d67b12b0989431a0277a008f6356b530f952c9d8753cc0ea459`.

Only pages 10,12,14,16,24,25,69,71 changed. The other 72 PDF content streams and raster bytes match the predecessor exactly. Existing grouping, cabin split pp49–51, carrier references pp30/32, trays and source order are preserved. The earlier 56-page artwork equivalence remains scoped prior evidence; no new full-edition parity is inferred.

Model SHA256 `3d23390fdec3df05c4f7ade4ec11c47ef15330c722579ab8e47aa5603a12d229`; plan SHA256 `df9ef0bf23d3f1ab71ac98dbe8dc351073658f241b7f705bf84a991cc412d9ff`.

## Remaining limits

Independent re-review and captain acceptance remain pending. Feature derivation does not prove insertion clearance or physical fit. Sole outlines are foot-position regions, not certified stud/cavity centers. Cord knot, cut length and slack are unspecified. No shared StudFleet changes/tests ran; DSS tooling gaps and native full-edition parity remain unchanged. `RESOURCE-AND-FEATURE-LOG.md` retains the original hold and actual run outcomes; no evidence under a lowered active floor is claimed.

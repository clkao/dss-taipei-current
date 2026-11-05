# Clear logical construction candidate

The local candidate has 80 A4 landscape pages. Page count was an outcome, not a target. Independent review and captain acceptance remain open.

The package is at `builds/clear-logical/candidate`. Open `viewer.html` for the page guide or `instructions.pdf` for print review. `model-viewer.html` retains the predecessor 3D inspection sequence. `release.zip` contains the complete offline package. The print sheets are pages 72 and 73.

`validation.json` binds the final PDF, viewer, ZIP, model and source plan. The package manifest binds every archive member. These outputs remain local. No publication or shared-tool change occurred.

## Seven finding dispositions

| Finding | Source and before pages | Candidate pages | Disposition |
| --- | --- | --- | --- |
| Floor spacers | Steps 14/15, operations 43-46. Before 19-20. | 24-25 | Each step owns eight 6141 plates. Four positions have two layers, separated by 0.4 studs. The new detail shows four two-plate stacks, paired positions and the receiving plate underside. The complete-state locator retains the installed bands. The cutaway explicitly omits the surrounding chassis. |
| Cabin | Step 41, operations 124, 125, 126. Before 41. | 49-51 | Separate results show dashboard/grilles, steering, then seat. Each page owns only its source-operation tray. Exact floor and support pieces remain in the cutaway. A complete-state locator establishes context. The wheel inset preserves its source angle. |
| Cord | Step 64, operation 210. Before 58. | 69 | The source specifies rings 25, 70, 142, 78, in that order. Three views label them 1-4. The existing route receives contrasting display color. End knots belong at 1 and 4 after threading. Knot type, cut length and slack remain unspecified. No unsupported knot geometry appears. |
| Trays | Step 4, operation 13. Step 26, operations 93-94. Before 8 and 33. | 8 and 40 | Both trays already existed in the exact predecessor PDF. Step 4 has two 3460 plates. Step 26 has six parts in five part/color lots. Larger dedicated pages make their allocations explicit. No duplicate stock or invented repeat appears. |
| Suspension attachments | Steps 5-8, operations 14-29. Before 9-12. | 9-16 | Each three-action unit recipe precedes a separate attachment page. Matching A/B source-position marks connect the unit and frame. Right-side views face the right-side receiver. Earlier modules remain present. Marks do not establish connector engagement or an insertion path. |
| Helm figure | Step 67, operation 215. Before 60. | 71 | An overhead view exposes the platform. A separate foot detail retains piece 255 and deck 284 at their exact poses. A complete figure locator shows the intended result. The detail does not instruct upper-body or enclosure removal. Stud engagement and physical access remain unknown. |
| Carrier references | Steps 17/18. Before 24/26. | 30/32 | An explicit caption connects panels .10-.12 to the completed C17/C18 shared recipe. The source operations, separate branches, copy maps and reserved-copy ownership remain unchanged. |

## Grouping and adjacent-page audit

Suspension recipes and their later attachments have different receiving contexts. Each now has its own page. The three cabin operations have different results and separate pages. The cord route has a dedicated page.

Adjacent steps 13, 16, 25, 40 and 63 retain their source images on separate pages. This prevents the corrected action from sharing space with an unrelated task. Step 63 retains its clear-film instruction.

The four-stack recipe remains one logical result. Its two source layers appear as one short repeated recipe. This preserves lower-before-upper dependencies for every stack. The operation and stock checks reject a missing layer, duplicate introduction or changed operation assignment.

The initial chassis diagram remains unchanged. Shared carrier recipes remain on pages 27-29. Their receiving and placement views remain separate. The wheel/riser page remains on 55. Life-ring and banner context remain on 66-67. These known-good pages are pixel-identical above the changed footer.

The remaining adjacent pages retain their established views. No source-bound reason required a new model pose, a different repeat recipe or broader reformatting. This is a bounded author decision. Independent review can identify further ambiguity.

## Evidence and limits

- `validation.json` checks 348 unique introductions, 215 source operations, unchanged source hashes, A4 dimensions, all page rasters and ZIP member hashes.
- `reuse-check.json` checks 56 retained pages against the predecessor at 1200-pixel width. Every pixel above the footer matches. The two carrier-reference pages receive separate visual review.
- `builds/clear-logical/candidate/pages` contains all 80 final page rasters. Final changed-page contact sheets are `builds/clear-logical/final-review-1.jpg` through `final-review-6.jpg`.
- `builds/clear-logical/browser-final/browser-check.json` records headless page selection, next/previous, desktop/mobile layout and return from 3D inspection. Screenshots are beside that record.
- The author inspected all 24 changed pages in the final contact sheets. Critical attachment, spacer, cabin, cord and figure pages also received individual image inspection.
- Earlier render specimens remain in `assets`, `assets-v2` and `assets-v3`. Full-body cabin views failed to expose both grilles. The final labeled cutaway corrects that author finding.
- All final rendering checks compare source piece records before and after capture. No geometry, color, pose or occurrence change occurred. The cord contrast is a diagram display treatment.

These checks establish artifact integrity and author-level visual evidence. They do not establish independent reader acceptance, physical fit, insertion clearance or native StudFleet parity. Target marks use source positions, not certified connector coordinates. The wheel inset retains the source separation and angle without a physical engagement claim.

## Reproduction inputs

The predecessor build directories are read-only dependencies named in the dispatch. `builds/clear-logical` links them without copying their bundles. Their exact source hashes are in `input-pins.json`.

The runtime paths are declared in that file. The Python environment supplies ReportLab, pypdf and Pillow. Node 24 runs the existing browser renderer through private headless Chrome profiles. System Node fails because its llhttp library is missing. PyMuPDF is absent. Neither tool is needed by the final process.

`jobs*.json` contain presentation selections, not a second construction plan. `compose.py` consumes the immutable model plan. `validate.py` compares every changed step against that plan.

The final render inputs are `assets` for cord and steering, `assets-v2` for the overhead platform, `detail-final`, `cabin-detail` and `feet`. Their corresponding render scripts and job files are in this directory. After rendering, run `compose.py`, Poppler at 1200-pixel width, `package.py`, `validate.py`, `check-reuse.py`, then `review.mjs`. Preserve exact candidate bytes during independent review.

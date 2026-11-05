# Captain-directed diagram text reduction

Captain: “i don't think we need the text. the diagram should be obvious”. This supersedes the unrun grouped prose proposal in7bcefe4, which remains in history. Original candidate1d56a994, PDFd8cb/map e9df, upstream image69021 and all first-run evidence remain untouched.

The static viewer successor removes the repeated sentence below the bitmap. Its embedded short numbered labels remain unchanged, alongside one2+2tray, navigation and optional Inspect. Primary diagram mode hides step-title, step-description and recipe-copy-note after the synchronous wrapper chain, scoped to visible diagram/step1/frame3. It preserves their original text. Leaving diagram mode restores visibility before calling the original action/main handlers, so those handlers retain control of original Inspect/Next4/overview captions. No new grouped visible prose is added.

The revised one-off checker reads actual settled visibility after image decode/two animation frames. Both diagram screenshots must have no visible sidebar title/description/note and no extra caption element. Inspect1/2/3 and Next4 require their exact source action title and restored title/note visibility; a separate settled overview check requires diagram hidden and its original title/note visible. Source-state/stock/paired-mark assertions remain unchanged. Actual screenshots still need visual review.

## PDF static assessment only

Frozen make_pdf.py currently adds two explanatory strings on page4: title “Fit both pins before the second beam” at line45 and caption “3. Seat the second beam on BOTH exposed pins.” at line48. These duplicate the diagram's numbered labels. Smallest proposed PDF correction: use a short structural heading “Chassis core” and remove only that page's caption call. Retain step badge, image, tray, source operations, page count/map and all other pages. No PDF source edit or regeneration has occurred in this refinement; the parent must disposition that exact change and coordinate any generation/review. Current PDFd8cb remains the unchanged generated candidate, not final text approval.

## Failed-only UI proposal

Same exact staging command and scope as SIDEBAR-FIX.md, but current pins are diagram-text-static-pins.json and planned-runtime.json. PinnedPython87d/PYTHONDONTWRITEBYTECODE1 stage-sidebar-fix.py preserves original HTML/six images/logs before replacing only the appended hybrid script (<=5s15MiB). Then pinnedPython run-ui.py invokes Node24/review.mjs once (<=90s150MiB incl ownprofile/temp/cache and closure). Combined100s165MiB,576MiBstart/512floor, same absent privateprofilece86b402/free19402 and prior safe PIDidentity/directwait/cleanup rules. No runtime, candidate mutation, raster, PDF change or publication is authorized by this proposal. All original failure and separate closure evidence remain.

## Final combined successor proposal (supersedes PDF assessment-only paragraph)

FO authorized the exact PDF edit: structural heading “Chassis core” and removal of the one repeated caption call. These two source changes are now authored; no generated PDF bytes have changed. Page4 image/tray/layout/map/operation binding and all other pages remain as before.

Exact serial commands, same author cwd and pinnedPython87d/PYTHONDONTWRITEBYTECODE1:

1. `python manual/hybrid/run-pdf.py --text-trim` (full source prefix corrections/access-order-20261104/), <=90s/100MiB including closure. stage-pdf-text.py verifies oldd8cb/e9df and regular nonlink PDF/map/three guides, moves those five into new before-diagram-text-trim, then requires root paths absent/nonlinks. Existing generator writes only fresh owned paths. Existing checker verifies136A4, all page boxes and all page image bytes equal, decoded page content streams exactly equal for all135 unaffected pages (footers remain unchanged because page count is unchanged), map equality except pdf_sha256, independently bound old/new PDF hashes, page4 concise title/no duplicate caption, source/stock and actual print128/129. No marker replay.
2. Only pass: existing stage-sidebar-fix.py <=5s/15MiB, then run-ui.py <=90s/150MiB with six actual settled screenshots and original exact behavior assertions. Same privateprofile/free19402/temp/identity/wait/closure rules. Preserves original HTML/six screenshots/logs; no source model changes.
3. Only assertion and visual pass: run-pdf.py --raster <=30s/20MiB, five pending pages3/4/5/128/129 at110dpi. Fresh raster output path required. No earlier PDF rerun or redundant intermediate caption iteration.

Proposed combined225s/285MiB including bookkeeping/ownedclosure; fresh576MiB eachstage/active512floor, firstfailure STOP/preserve/noretry. Current pins are final-text-static-pins.json. ActualA4 and independent affected review remain pending. Package references/manifest/ZIP/publication remain outside this lease proposal.

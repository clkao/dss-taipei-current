# Captain-directed diagram text reduction

Captain: “i don't think we need the text. the diagram should be obvious”. This supersedes the unrun grouped prose proposal in7bcefe4, which remains in history. Original candidate1d56a994, PDFd8cb/map e9df, upstream image69021 and all first-run evidence remain untouched.

The static viewer successor removes the repeated sentence below the bitmap. Its embedded short numbered labels remain unchanged, alongside one2+2tray, navigation and optional Inspect. Primary diagram mode hides step-title, step-description and recipe-copy-note after the synchronous wrapper chain, scoped to visible diagram/step1/frame3. It preserves their original text. Leaving diagram mode restores visibility before calling the original action/main handlers, so those handlers retain control of original Inspect/Next4/overview captions. No new grouped visible prose is added.

The revised one-off checker reads actual settled visibility after image decode/two animation frames. Both diagram screenshots must have no visible sidebar title/description/note and no extra caption element. Inspect1/2/3 and Next4 require their exact source action title and restored title/note visibility; a separate settled overview check requires diagram hidden and its original title/note visible. Source-state/stock/paired-mark assertions remain unchanged. Actual screenshots still need visual review.

## PDF static assessment only

Frozen make_pdf.py currently adds two explanatory strings on page4: title “Fit both pins before the second beam” at line45 and caption “3. Seat the second beam on BOTH exposed pins.” at line48. These duplicate the diagram's numbered labels. Smallest proposed PDF correction: use a short structural heading “Chassis core” and remove only that page's caption call. Retain step badge, image, tray, source operations, page count/map and all other pages. No PDF source edit or regeneration has occurred in this refinement; the parent must disposition that exact change and coordinate any generation/review. Current PDFd8cb remains the unchanged generated candidate, not final text approval.

## Failed-only UI proposal

Same exact staging command and scope as SIDEBAR-FIX.md, but current pins are diagram-text-static-pins.json and planned-runtime.json. PinnedPython87d/PYTHONDONTWRITEBYTECODE1 stage-sidebar-fix.py preserves original HTML/six images/logs before replacing only the appended hybrid script (<=5s15MiB). Then pinnedPython run-ui.py invokes Node24/review.mjs once (<=90s150MiB incl ownprofile/temp/cache and closure). Combined100s165MiB,576MiBstart/512floor, same absent privateprofilece86b402/free19402 and prior safe PIDidentity/directwait/cleanup rules. No runtime, candidate mutation, raster, PDF change or publication is authorized by this proposal. All original failure and separate closure evidence remain.

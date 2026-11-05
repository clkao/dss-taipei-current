# Iteration1 — actual rendered candidate / partial visual coverage

Review the actual71-page PDF in `builds/simplification-i1-retry1/instructions.pdf`, SHAe8739547da1352bed969b21b5984d8af49278247a9076a0ff9cf57804ca2f132. Page map39736335368a8f3a8b245b01615306841a88af5474b4fb523a5ffd0398d9c613. Source2a3070a; all67 steps/215 operations/348 introductions and exact model3d23390f remain unchanged. Published136-page PDF/live24425a3 are immutable. Viewer remains the published baseline, not a claimed simplified candidate.

This is the first real simplification candidate, not one of three completed reviews. PDF creation and static check exited0. Fourteen110dpi A4 rasters exist in `a4-review/`:4,5,7,9,14,15,16,18,21,22,23,24,25,26. The next13 selected pages were not rendered:27,30,37,45,46,49,50,51,53,55,57,58,61. Independent feedback can use these14 without waiting or regenerating the PDF. Author viewed all14 individually. This is not complete71-page visual coverage or package acceptance.

## Findings to assess before iteration2

| Finding / evidence | Proposed next change, not yet applied |
| --- | --- |
| Page4 beam part label is cut by the next icon; page9 callout labels overlap neighboring icons. compact_tray fixes3 columns even at157–180pt widths. | Choose columns from minimum readable cell width, wrap to another row with reserved height; keep font size and quantity/part identity. |
| Page23 common three-piece rail has two different first-bracket views, but four panels look sequential and individual trays can imply three brackets rather than two. | Explicit17/18 fork from shared base to common finished construction; one-copy total tray3710×1,99207×2. Preserve both source orders and exact occurrence mapping. |
| Page24/26 receiving and installed camera orientations differ and the finished assembly shrinks. Page18/25 show context but attachment points are small. | Consistent scale/orientation where existing images permit; matched target locators and magnified attachment inset. Do not fake a motion path or use more prose to hide unclear geometry. |
| Page4 still has three verbal labels baked into the retained diagram. | Locally owned derivative from exact editable source; remove only verbal labels, preserve numbers/arrows/paired targets. No upstream feature dependency. |

Positive observations: page5 paired chassis panels and page7 paired ordinary steps remain roomy/readable. Page21 shows all four lower-base frames on one page with2x; page22 shows the four-piece rail2x. Bands remain visible in contextual pages. Page15 separates root support from loose bumper seed. These are author observations for review, not independent approval.

## Resource and failure scope

Original run04c7aeb stopped at observed1,196,032,000B RSS, child-15; preserved in failure-1. Narrow page-scoped cache clear succeeded in creating71 pages in5.120s with overall observed direct peak703,807,488B. Checker0.334s. Every launched raster exited0 and was reaped. Last completed-stage record:8.988s, own output8,789,756B, minimum free585,330,688B. Next-stage≥576MiB preflight failed; supervisor1, no next child. Later df showed330,854,400B free; attribution unknown. Fresh ps showed no owned processes. Slot was explicitly RELEASED. No automatic retry, deletion or source mutation followed.

Full hashes/bytes and closure/resource scope are in rendered-evidence/binding.json and original run-partial.json. The cache result supports the decoded-lifetime hypothesis; it does not identify the first run's exact interrupted allocation or turn its failure into a pass. No physical insertion, independent nativeUI, native adoption, publication or final package claims.

## Review request

Same Epicurus: inspect these14 exact pages and prioritize iteration2 corrections. Distinguish application of existing rules from any new rule justified by the visible failures. We propose minimum tray-cell width based on measured label extent and explicit alternative-branch composition because actual pages4/9/23 fail those needs. Keep necessary receiving views while improving correspondence. Do not count a static plan or the resource retry as another design iteration. Two further actual candidates remain due.

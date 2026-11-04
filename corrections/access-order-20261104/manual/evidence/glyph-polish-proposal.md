# Four-page glyph polish

Independent review found missing-glyph boxes before “Studs up” on PDF36/39 and in the mixed Chinese/English caption on127. Source investigation also finds the same turn prefix on37. Parent approved including that exact occurrence.

The retained template emits U+21BB with Arial Bold and U+00B7 in a paragraph selected as STSong-Light. DSS overlay replaces only the exact turn-label literal with `Turn: ` and the exact banner caption with `洋 above / 流 below / both faces.`. No broad Unicode normalization, CJK replacement, retained-template edits or image/geometry/order/stock changes.

Source `make_pdf.py` SHA256498003788840acce442ebfb65f87c21f9871ea5faeec8345c10c8ac967b73189. Existing final PDFfb4, mapd601, viewer9cc, siteindex593, manifest and source are retained in `builds/access-corrected/before-glyph-polish`; prior142rasters remain `a4-review`.

Proposed verification compares every decoded page content stream for the138 unaffected pages, every page image, dimensions, and the whole page map except independently bound PDFhash. Then render only36/37/39/127 at110dpi and inspect actual output. Prior138 rasters may represent the new PDF only after exact equivalence passes. PDF creation, check and raster require the coordinated runtime grant; no marker replay or browser run.

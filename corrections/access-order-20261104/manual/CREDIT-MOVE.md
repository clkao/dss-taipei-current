# Feedback credit placement

User request: “Instruction feedback -> please put that in the credit page”. The exact existing section now appears once in credits.html, after the contributor introduction and before the physical-vehicle section. The homepage retains its old #instruction-feedback anchor as a short link to credits.html#instruction-feedback.

Only index.html, credits.html and their dependent provenance, manifest and release ZIP changed. The old reviewed files remain in builds/access-corrected-r2/before-credit-move. The historical credits source was read and copied; it was not modified. package.py now preserves this placement on future builds, using the retained credits baseline.

Static checks confirm exact feedback text, unchanged homepage scripts and embedded data, all other release files unchanged, equal unaffected ZIP member bytes, and matching manifest/member hashes. PDF remains b69ae67b7c7894a862bd6b7e71d17a694956231bc459424e1e30fc6f4462718a. Viewer, model, plan, stock, Technic, artwork and rights remain unchanged. No render, browser, PDF generation or publication push was performed.

Exact five-file change pins and checks: evidence/r2/credit-move-check.json. Complete 28-file transport map against published 244eda13a5c64c46ad8a7081be7151e0b5e775be: evidence/r2/credit-move-publication-file-map.json. Parent owns the authorized publication transport. Prior physical and independent native-UI limits remain unchanged.

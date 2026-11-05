# Package integration first run — STOP

Authorized sourceb1f2eed/script16648d85154bdbb4db71b0d1913cb527a327cd0c35bc4f8bc7dd1f0ecedf339e. Command: PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l /Users/clkao/git/house-demo/tmp/lego-standards-venv/bin/python corrections/access-order-20261104/manual/simplify/package/prepare.py, owned worktree cwd. Parent waited exit1;0.92s real,0.74user,0.05sys; maximum directRSS93044736B, peak footprint82248160B. No live handle returned. No browser/PDF/render started.

- Intended: stream unchanged archive members into a new owned release ZIP while replacing exact reviewed package members.
- Observed: line62 `src.open(info)` raises `zipfile.BadZipFile: Truncated file header`; package manifest/final verification were not reached. Partial builds/simplification-package retained.
- Boundary: owned static packaging helper, not a demonstrated defect in source geometry, PDF or prior published archive. The pinned old ZIP hash passed before staging.
- Trigger hypothesis: destination `dst.open(info,'w')` receives the same ZipInfo object that later supplies `src.open(info)`; write-side header_offset mutation may redirect the source read. Proposed minimum correction: copy the ZipInfo for destination writing, preserving the source member identity; use a fresh successor directory. No fix or retry executed.

Existing output, old package and all accepted PDF bytes preserved. Actual run had fresh576MiB start and512MiB stage guards; exact minimum free and partial output bytes were not recorded by this failed script. Do not invent successful resource/ZIP checks. Source-only diagnosis and separately dispositioned repair remain next. Final package and browser pins are unavailable because packaging stopped before completion. No acceptance, publication or gate advancement.

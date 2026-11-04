# Source-bound access-order correction

This candidate addresses the reported late chassis pins, front bumper/dish order and the captain-confirmed three-bracket access problem in step19. The same upper-rail construction pattern is corrected in mirrored step18. It preserves all original snapshots and remains `adopted:false`. [Builder correction sheet](CORRECTION-SHEET.md) gives the concrete candidate sequence.

`derive.py` reads exactly one immutable source: `sources/minifigure/legacy-v10/model.json`, SHA-256 `49b6a0d3eb138e4f456084714d7cbf0422da8b8209ed500d057447dd9a6021a0`. That file contains the exact legacy instruction plan. The script partitions/reorders source operations and generates the candidate, crosswalk and checks. Do not hand-edit generated JSON or keep a second manually maintained plan.

```sh
python3 corrections/access-order-20261104/derive.py
python3 corrections/access-order-20261104/audit_static.py
```

These are static Python source transformations, not a compiler, importer, renderer, mesh sweep, connector backend or physical test. `candidate-authoring.json` is a declared DSS intermediate. It is not claimed to be a supported StudFleet plan. Old images, displayed step numbers, recipe frames and prefix/sweep certificates cannot simply be rebound to the changed sequence. Regenerate presentation from the new operation mappings and independently review it before adoption. No published release changes here.

## Diagnosis and correction

| Observation | Builder effect | Classification | Disposition / next evidence |
| --- | --- | --- | --- |
| Raw12 introduces collared pins216/231 after beams172/178 are tied and core joined | Late insertion may require opening the frame | Source-confirmed ordering conflict; community physical concern | Preinstall pins in first beam, mate second, then ties. Test actual seating; do not call it physically proven. |
| Raw31 introduces dish191 before lower tie190; raw33 groups brackets and cap; reader13 compresses33–35 without inner frames | Dish can block work and the pictured result hides layer order | Source-confirmed sequence/grouping conflict; community concern | Build nine-piece lower bumper on table, attach via182↔168/177, dish last. Whole-unit approach remains unverified. |
| Rails are attached to two brackets before the other three brackets are inserted beneath them in raw49/57 | Local access trap identified by captain in step19 | Captain-confirmed local recipe issue, with mirrored source pattern | Two separate complete rail/bracket units per side, then join lower carrier. Preserve 15-piece final carriers and test actual seating. |
| Old connected carrier and finite above-path records exist | They could be mistaken for proof that this local step is accessible | Evidence scope gap, not demonstrated loss of the floating-piece correction | Connectivity correction remains; local frames5–7 were not certified by a whole-carrier join sweep. |

The new bumper unit is deliberate: deferring dish191 without changing the work context leaves no source-demonstrated earlier support for lower tie190. Absence of a graph edge is not proof of floating, so the candidate explicitly builds the unit on the table. This changes its construction ownership, not its geometry. The upper rails are two local units on each side because the two loose rails have no source-declared connection to each other before joining the lower carrier.

## Static checks and scope

[checks.json](checks.json) records 348 unique introductions; exact geometry, colors, modules and UUIDs except updated introduction ordinals; all original operation piece partitions retained; all unaffected operations retained; completed child joins exactly cover their current stock; original copies/shared-prefix metadata preserved; and both final carrier memberships unchanged. Ownership deltas are explicit: two pins into chassis-core, nine bumper parts into a new local unit, and seven upper-carrier parts per side into two rail units. Five new local-unit joins are introduced.

The candidate has 215 operations: eleven additional operation partitions plus five added joins relative to 199. There are 67 **parent groups** because old late-pin step5 redirects to group1. Changed groups have ordered inner panels. No guide/accessory operation disappears; all 68 original reader identities map in [crosswalk.json](crosswalk.json). These counts do not predict a rendered manual's steps or pages.

Baseline regressions fail for late pins, premature dish, bracket/cap compression and upper-rail capture order; the candidate passes the corresponding declared-order checks. The already-corrected bed installation66 before rear trims206/214 at67 is explicitly preserved. These checks prove source order and identity only, not collision-free paths or hand access.

[full-sequence-audit.json](full-sequence-audit.json) covers **all 199 original operations and 68 reader steps**, assigning every operation to a reviewed region and preserving exact part/contact context. It includes four suspension recipes, both side carriers, floor/cab/roof closures, bumper/lights, shield and later equipment. Suspected local access, geometric uncertainty and ergonomic concerns are distinguished from confirmed source order and reported problems. Group size alone is not treated as evidence of an obstruction. Remaining suspects are not auto-reordered.

[source-evidence.json](source-evidence.json) retains the exact relayed community text and captain clarification, relevant source part records, catalog-file hashes and old control/rebinding identities. The old sweep sampled18 paths and3733 pair poses; it was not a full sequence or continuous physical sweep. Near-seat right-carrier pairs156/99 and166/129 (left96/99 and115/129) remain unverified.

## Smallest remaining probes

1. Dry-fit beam172, pins216/231 and beam178 before any tie plate. Confirm both pin collars seat without force; then add all ties.
2. Build the nine-piece lower bumper locally; test its cap182 joining to168/177 with191 absent, then fit191. Record any required disassembly separately from finger-access difficulty.
3. With each loose rail's underside exposed, fit all its brackets and join it to the lower carrier. Test both sides because the source poses and continuation groups are separate.
4. Keep the finished carrier and the exact floor prefix separate until testing the original whole-unit joins. Observe right156/99 and166/129 first. If that join fails, compare a deferred floor closure or split integration only after recording the obstruction; neither is implemented here.
5. After usable shared tooling supports these nested units, derive a new plan, compile/import/render in the allocated heavy slot, verify exact inventories/geometry, inspect all changed panels and independently review the entire affected edition. Physical and human acceptance remain separate.

This work is held in the existing instruction correction scope. It creates no workflow, entity, gate or shared-tool implementation. The reusable H1 work, publication and other projects are untouched.

# StudFleet gaps: DSS impact and simplification

This record separates observed failures, missing features, and candidate work under review. It describes the DSS adoption conditions for each fix.
The [task snapshot](../evidence/bootstrap/studfleet-gap-task-snapshot.json) records full IDs, current statuses, source hashes, and the owning state commit.
The [tool manifest](../manifests/tooling.json) identifies the actual executable and resources used for our demonstration.

The accepted legacy publication remains usable. These gaps affect new generation, inspection, portability, or later revisions.
No task status alone establishes compatibility with DSS. No shared project changed as part of this record.

## Reproduced connector failure: a separate defect

The fresh import admitted all **348 occurrences**. The subsequent explicit `pyldraw3` inspection reported:

```text
failed: connector malformed position: o/3/3/snap_cyl@L11:I0
```

The affected occurrence is `o/3/3`, part `3818`, in the candidate figure.
The [occurrence crosswalk](../migration/minifigure-v10/occurrence-crosswalk.json) binds it to the original piece and source path.
The [exact command](../evidence/bootstrap/inspection-command.json) records arguments, working directory, and environment.
The [inspection report](../evidence/bootstrap/inspection.json) retains the result.

The executable hash is `bcbaf07e0b068297cd95f0487dc62e844f67f3318f5bf11146e30a005ae20490`.
It reports source revision `9dc7c81ffefd3afaae9b6a877365e260910533a1` and `vcs.modified=true`.
The report also has `required_failure: false`. This field does not establish successful connector analysis.
The command exit status was lost during interruption. The record does not infer that status from the report.

**Exact gap:** the pinned public inspection journey cannot return usable connector analysis for this accepted model.
The error identifies a malformed position. It does not establish whether the cause is source geometry, connector metadata, conversion, or validation.
No root cause or fix is proven. No pose repair is authorized.

**DSS impact:** we cannot use this run as current whole-model connector evidence. Import and exact occurrence identity remain valid.
The failure affects the minifigure baseline, despite its count being less than 500.
It is separate from the Technic scale gap owned by `k4`.

**Owner:** the shared StudFleet inspection/connector area. The twelve linked tasks do not explicitly own this exact failure.
This local record preserves the defect for routing. It does not claim that a dedicated upstream task exists.

**Fix acceptance:** repeat the exact command with a pinned corrected release and unchanged source bytes.
The result must expose coverage, contacts, unresolved findings, and any unsupported transforms explicitly.
An independent review must reconcile the affected occurrence with its source and connector metadata.
A narrow control must preserve the failure signal for malformed input. A backend error must not appear as usable analysis.

**Simplification afterward:** use one shared inspection result for the designer and independent reviewer.
Retire the manual backend-failure triage for this case after the full run passes its declared contract.
Keep historical reports and separate collision, insertion, manufacturing, and physical limits.

## Feature gaps and their effects

The statuses below are snapshot observations. Existing IDs identify the owning StudFleet dev records, not new DSS tasks.

| Owner / status | Exact gap and DSS impact | Evidence needed from a usable fix | DSS simplification afterward |
| --- | --- | --- | --- |
| `nk` — backlog | No delivered portable skill/workflow package proves fresh creation, adoption, correction, and resume. Our setup uses a modified binary and machine-specific resources. This does not block the retained local legacy release. | A fresh agent completes a small real journey with compatible tools, catalog, renderer, and connector resolution. Resume preserves decisions. Wrong workspace and stale inputs refuse. Reference-only and variant contracts remain distinct. | Replace manual workflow setup and absolute runtime paths with one versioned entry point. Keep set-owned source, decisions, hashes, and two workflows. |
| `k4` — backlog | The connector backend caps input at 500 occurrences. Technic has 1101. A larger import limit does not extend connector coverage. This gap does not explain the 348-piece failure. | A bounded run accounts for every occurrence and relevant cross-module interface. Omitted or unsupported interfaces remain explicit. | Use a shared whole-model report, or a coverage-accounted scoped report, instead of manual inspection partitions. Keep Technic prototype limits. |
| `31` — backlog | Shared checks do not reproduce the shield's actual-mesh compound installation evidence. A direction and distance cannot represent lift, slide, and lower. | Step 53 and retained shield controls reproduce the positive path and blocked alternatives with exact transforms. Sampling and mesh limitations remain explicit. | Replace active use of bespoke mesh/path scripts with authored paths and shared reports. Retain old witnesses. Retire each external check only after equivalent coverage exists. |
| `h1` — backlog | Composition accepts local-unit sources, not arbitrary ordered main operations. DSS needs 199 operations presented as 68 main steps. False independent groups change construction meaning. | A compact main-step specimen preserves operation order, intermediate states, trays, references, and PDF/viewer navigation. No hidden introductions or pose changes. | Express reader groups in supported presentation data. Remove custom main-step merging from the active instruction compiler. Keep one construction sequence. |
| `90` — backlog | No explicit supplied-unit contract prevents unwanted figure recipes and loose-limb trays. Step 66 places the candidate. Step 67 adds the flag to assembled 小英. | Completed figure cards preserve all member occurrences and purchasing inventory. Accessory attachment works without reintroducing body parts. Ordinary 2× recipes retain their construction pages. | Replace figure-specific tray/page suppression with supplied-unit declarations. Remove active figure exceptions from custom PDF generation. |
| `n0` — validation | Existing root-only joins cannot preserve genuine nested component construction. DSS adoption must inspect exact recipe hierarchy before declaring this dependency required. | A real nested DSS specimen preserves child-to-parent-to-source maps, once-only coverage, local navigation, and inventory. Simple speakers or rings alone do not prove nested behavior. | Use supported nested units and joins where needed. Remove manual flattening or nested recipe expansion for those units. Do not require nesting for simple flat recipes. |
| `7d` — validation | Local recipes otherwise appear in preparation, apart from their intended main-model use. Copy availability and retention need shared semantics. | Speakers at 56 and life rings at 61 appear at their intended positions. Each recipe appears once with exact copies and per-copy trays. Any retained copy appears correctly at later use. | Replace manual recipe/page ordering and copy-count text with an authored schedule and derived copy state. |
| `cn` — validation | Guidance needs pages without rigid introductions. Bands, stickers, cord, and placement notes cannot become fake parts or duplicate operations. | Real DSS guides appear at exact anchors in the PDF and viewer. Coverage and inventory stay unchanged. Asset hashes and attribution survive export. | Move supported guides into presentation assets. Remove corresponding manual guide-page insertion. This fix alone does not prove print-sheet dimensions or editable artwork packaging. |
| `w4` — ideation | Fixed templates expose internal IDs, hashes, repeated captions, and routine state text. Short captions alone cannot remove this clutter. | Actual DSS main and recipe pages use useful action/component labels. Part numbers, page references, necessary copy notes, and draft limits remain visible. | Keep authored labels in presentation data. Stop template-specific text cleanup and local reader-label overrides for supported output. |
| `tw` — ideation | Installed views can still show an unsupported placement arrow. A guessed direction gives the builder false instructions. | A DSS installed-only specimen omits the hint in both PDF and viewer. Existing checked insertion requirements remain intact. | Use explicit neutral-view intent. Remove renderer workarounds that hide arrows. Compound-path evidence still belongs to `31`. |
| `rx` — backlog | Finite hardcoded purchasing mappings do not cover arbitrary imported lots. LDraw and BrickLink IDs cannot be assumed equal. | Reviewed mappings reconcile every DSS lot and quantity with the retained wanted list. Missing or ambiguous mappings refuse explicitly. | Generate matching CSV/XML through one shared exporter. Stop active set-specific wanted-list conversion. Keep reviewed mappings and their provenance. |
| `mc` — backlog | No accepted arbitrary-model diff journey isolates moved, recolored, added, and removed occurrences. Later revisions require manual comparison. | Real DSS changes show affected occurrences and stale evidence. Input reordering creates no false changes. Ambiguous identity stays explicit. | Replace manual revision comparisons with shared visual diffs and scoped evidence reuse. Keep human acceptance and the reference-feature ledger. |

The finite construction profiles cover seven of the current 87 part types.
The other 80 types are not thereby missing from the render catalog or shared connector metadata.
Broader rendering, connector coverage, collision checks, insertion checks, manufacturing evidence, and physical strength remain separate properties.

## Confirmed specimen distinctions

The original bootstrap specimen file remains a historical snapshot.
[Specimen corrections](../migration/minifigure-v10/specimen-corrections.json) supplies the current selection and scope.

- **Main composition:** use step 2, operations 7–9, with the state after operation 6 as context. These are ordered root-assembly additions.
  Step 1 builds a local chassis unit and joins it. That specimen does not prove arbitrary main-operation composition for `h1`.
- **Repeated recipes:** step 56 contains two six-piece speakers. Step 61 contains two two-piece life rings.
  Both are useful scheduling specimens. Neither alone proves nested-join support.
- **Shared prefixes:** steps 18/19 share four recipe frames before their distinct carrier continuations.
  Two complete identical recipes cannot represent that requirement. Whole-recipe scheduling alone does not establish shared-prefix support.
- **Retained panels:** step 53 calls for three shield panels, installs two side panels, and retains the third for the front.
  Retained-copy behavior and compound-path evidence need separate proof. The later front-panel use must consume the correct remaining copy.

These distinctions refine the adoption evidence. They do not expand the accepted implementation scope of an upstream task.

## What we can simplify, and when

The target active path is:

```text
accepted model revision -> assembly.json
construction authoring   -> plan.json
reader authoring        -> presentation.json + artwork
                         -> pinned StudFleet package + evidence
                         -> independent instruction review
```

1. **First supported specimens:** adopt individual usable fixes with exact source and tool pins.
   Speakers, life rings, main-step composition, and supplied figures provide small real examples.
   No specimen result replaces the current manual.
2. **Complete migration candidate:** translate the frozen legacy intent into supported plan and presentation contracts through one adapter.
   The current DSS intermediate schemas remain explicitly non-executable until that conversion is complete.
   Prefix carriers, shield approaches, guidance, print assets, and purchasing exports retain their separate evidence requirements.
3. **Parity and acceptance:** compare the complete generated package with the legacy edition.
   Review every A4 page, recipe, tray, major join, and viewer path.
   Counts alone do not establish usability.
4. **Active-path simplification:** after acceptance, stop editing the legacy compiler, PDF generator, and derived intermediate sequence for new editions.
   Use supported plan and presentation inputs as the sole active authoring source.
   Keep the one-way adapter for historical import or make it archival after migration.
   Keep old recipes, crosswalks, accepted bytes, and review records as provenance.

The retirement candidates are `compile_full_instructions.py`, `make_full_instruction_pdf.py`, and the equivalent migrated portions of release preparation.
They are retained under `sources/legacy-recipes/` and are already historical snapshots in this repository.
Retirement means removal from the active generation path. It does not mean deletion of accepted evidence.

Portable packaging (`nk`) and revision diffs (`mc`) improve maintenance. They need not block a bounded local specimen with explicit pins.
Technic inspection (`k4`) does not block minifigure instruction authoring.
Purchasing export (`rx`) gates a replacement purchasing package, not a model-only review.
Each edition must state which capabilities its promised deliverables require.

## Work that remains ours

Reference reconciliation remains DSS design work. A tool cannot decide which shared features each variant implements or approve deviations.
Instruction choices, artwork, attribution, and acceptance also remain set-owned.
Physical trials remain separate from digital evidence.

The current tasks do not establish full parity for publication animation, print-sheet packaging, or every custom viewer interaction.
Those features need explicit parity evidence before their existing implementations can leave the active path.
A shared generator release does not authorize publication. Publication still requires the exact accepted package and applicable user authority.

## DSS priority and tested update (2026-11-03)

These are DSS adoption priorities, not upstream workflow status changes.

| Area | Priority | Gaps |
| --- | --- | --- |
| Modeling | First | Exact 348-piece connector inspection failure; independently validate the forthcoming fix. |
| Modeling | When Technic resumes | k4: inspection beyond 500 occurrences. |
| Modeling | Before repeated revisions | mc: occurrence-aware model diffs. |
| Instructions | Current integration | tw: neutral views; 7d: recipe scheduling and retained copies. |
| Instructions | Next | h1: ordered main-step composition, then 90: supplied figures. |
| Instructions | Complete-edition parity | cn: guidance; w4: reader labels; shared prefixes 18/19; retained panels. n0 only where actual nesting requires it. |
| Instructions | Purchasing deliverable | rx: reviewed wanted-list export. |
| Both | Before replacing shield path evidence | 31: compound installation paths. |
| Both | Before portable adoption | nk: reproducible tool/workflow package. |

[Bounded TW render evidence](../evidence/integration/tw-95b67ce-render/README.md) advances tw from input checks to PDF/headless evidence, and strengthens 7d copy/tray/navigation evidence. Both packages verify; speaker exporter exit remains unknown after a DSS monitor failure. Neither task is declared closed. Main-anchor relocation, prefixes, full edition parity and human acceptance remain outstanding.

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

### Reader-label increment

[Candidate 3a6833b input checks](../evidence/integration/labels-3a6833b-check/README.md) pass on freshly imported speakers and rings. `w4` advances to DSS parser/compiler compatibility: authored labels survive and frame/copy/source semantics remain unchanged. Visual clutter removal and saved-package verification remain pending; no render lease was used. Next: bounded label rendering when authorized, then h1 and 90. Modeling priorities are unchanged.

### Connector increment

[Independent exact348 check](../evidence/integration/connector-50dfc27-check/README.md) on provisional 50dfc27 replaces backend failure with usable inspection evidence. Fresh import/inspect exit0; all348 source instances/origins unchanged. Metadata coverage:342 complete,6 partial;562 confirmed and447 potential contact observations;29 unmatched. The affected arm retains explicit zero-confidence diagnostics and no contact claim. Upstream release remains pending. This does not change k4 or establish construction validity. Instructions remain w4 visual validation, h1, then90.

### TW local delivery update

StudFleet FO delivery notice e6fd0463-1b21-4c90-827e-7f5fe53db0f1 reports `tw` locally merged at e6c8661b64e5f4f6b69fb680402c24dfff3df965 and archived done. Validated candidate a319c35 retains production95b67ce/source-tests a62d2f2. This is an upstream delivery report, not a new DSS test run.

DSS status: upstream delivered locally; bounded source, PDF verification and headless navigation evidence already present for that production mechanism. Full-manual human parity remains open. No rebuild ran solely for the merge ID. Source inherited from 7d/cn does not clear their broader human holds.

Remaining priorities: w4 actual PDF/viewer validation awaits a render lease; h1 production and then90 supplied-unit adoption. Connector50dfc27 has independent DSS evidence at cebb011, but upstream validation/merge remain pending. No shared source, workflow gate or publication changed.

### Reader-label artifact increment

[W4 bounded artifacts](../evidence/integration/labels-3a6833b-render/README.md) now pass both exports/verification and corrected headless copy-return navigation. All10 actual PDF pages inspected: useful labels/captions, stock quantities and retained-copy references preserved; default internal IDs/hashes removed. Original title-only harness refusal is retained; required draft warning was correct and remains independently asserted. No product repair occurred. `w4` advances to bounded artifact evidence, not human/full-manual acceptance. Remaining priorities: h1, then90; broader7d/cn holds remain.

### H1 input and connector delivery update

[H1 candidate16b3094](../evidence/integration/h1-16b3094-check/README.md) passes independent source audit and same-binary check-only. All16 occurrences match; step2 operations7-9 compose into one5-part reader step retaining13/15/16 intermediate states. Starting context after6 is explicitly out of scope. `h1` advances to DSS compiler compatibility; next are actual PDF/viewer checks, then90. A source filename handoff mismatch was reported and resolved in the DSS audit only.

FO notice a6d2af2a-2e51-418a-a8cb-5986f4bafa41 reports the connector repair locally merged at a7558f660a26dcc5054dc1c6e61b090458d6eaf2 and archived done. Existing independent DSS evidence cebb011 applies to the same production mechanism. No merge-ID-only retest ran. Coverage/zero-confidence/physical limits remain unchanged.

### Coordination update: artifact queue

FO notice22890108-29ff-4dbe-838d-5b24eda303d5 reports90 design approved and implementation dispatched for18 exact supplied members. DSS has not tested that implementation. W4 independent validation is held on an unexplained headless-navigation timeout; this does not negate DSS bounded evidence or establish a product defect. H1 producer artifacts exist, but live-review AC4/5 holds remain.

[H1 artifact invocation](../evidence/integration/h1-16b3094-check/artifact-invocation-prepared.json) is prepared, not executed. Read-only producer file hashes match its manifest; this is not CLI verification or visual acceptance. Await an explicit artifact lease, then complete H1 PDF/viewer checks;90 remains next. TW and connector remain delivered locally. No green source/compiler suite was repeated.

### H1 artifact increment

[H1 artifact evidence](../evidence/integration/h1-16b3094-render/README.md) advances h1 to successful export/package verification and two-page A4 review. Exact inputs,13/15/16 states and5-part tray remain intact. Navigation stopped on an obsolete DSS assertion: composed #approach is Ordered details, not a movement control. FO authorized a helper-only correction, prepared but not rerun pending a new browser lease. No demonstrated product defect or completed navigation claim. Next: finish H1 navigation, then90. All sections remain adopted=false.

### H1 navigation completion and W4 delivery

The authorized H1 helper retry passed on the unchanged package:13/15/16 states, five-part tray, Ordered details action and exact Finished step returns. No HTTP requests or page errors occurred. H1 now has bounded PDF/headless evidence. No section acceptance or full-manual parity is claimed. Next priority is90.

FO notice742924a2-ba37-4434-a93c-7b8b8f6801c6 reports W4 locally merged at34064f05e60b973df6184098acea2aea8a4d0695 and archived done. Existing DSS evidence7c29bb4 applies to the same ea886884 binary. No merge-ID-only retest ran. TW, connector and W4 keep separate exact binary pins until a combined build arrives. Broader7d/cn holds remain.

### Supplied-unit early handoff and H1 verification hold

[90 preparation](../evidence/integration/supplied-dd6588c-preparation/README.md) is read-only. The early package manifest differs from its advertised hash while producer artifact work remains active. A frozen handoff is required before package identity claims. No DSS CLI probe ran. Membership intent is8+8 supplied with2 later accessories; original198 sequence/context still needs explicit reconciliation for full section adoption.

FO notice29bf6d4e-4bd7-43cf-8bbf-14ef7f2ac901 reports H1 verification accepted false overview-Approach metadata in an independent negative control. Upstream AC3 repair is pending. Positive DSS PDF/navigation evidence remains provisional and does not cover that refusal. Next: frozen90 probe, then exact H1 fix feedback when supplied.

### Frozen90 identity preparation

The new frozen90 handoff passes read-only hashes, all18 exact source occurrences and8+8 supplied/2 accessory membership checks. Producer diagnosis links the old hash to an intentional negative-control window. Old failure evidence remains intact. Fresh same-binary import/check-only commands are prepared but unexecuted pending lease. This resolves the preparation identity hold, not compiler or section acceptance. H1 verification repair remains pending.

### Frozen90 compiler increment

[Independent fresh import/check-only](../evidence/integration/supplied-dd6588c-check/README.md) passes with exact frozen assembly/source and a new same-binary sidecar. Supplied ownership is8+8; only the2 later accessories have construction provenance. No fake local recipes exist. All18 inventory quantities and release/use stock boundaries reconcile. `90` now has independent compiler/stock evidence. No DSS artifact/browser check ran for this increment. Next: leased90 artifact feedback;198/decorations/330context and all section acceptance remain open.

FO notice1b09f595-8dd2-4c79-aeab-08f36188454d reports H1 guard fix b0748c9/binaryb410 clears the metadata counterexample upstream. This is not a DSS retest or release claim. Current upstream live/human review remains held. W4 remains delivered locally.


### Frozen90 artifact increment and read-only diagnosis

[Artifact review](../evidence/integration/supplied-dd6588c-artifact-review/README.md) records package verification exit 0 and inspection of the three existing full A4 rasters. Supplied cards, two later accessories, final placement/decal caption and draft limits remain visible. Headless navigation stopped at the initial 12-second load timeout. No step actions ran. The producer uses a 30-second default with the same viewer bytes and recorded runtime versions. This difference supports a bounded hypothesis, not a proven cause. Original failure telemetry is incomplete. No product defect or contention cause is established.

The lease is released with all observed owned processes closed. A failed-only navigation proposal awaits separate authorization. No green compiler/export/verify check will repeat. Gap 90 advances to verified package and existing-raster evidence, but navigation/live/human acceptance remains open. Next priorities are navigation, operation 198/decorations/330 context, then contextual speakers/rings and H1 acceptance. All sections remain adopted=false.


### Frozen90 failed-only navigation increment

[The single authorized retry](../evidence/integration/supplied-dd6588c-navigation-retry/README.md) passed all original headless assertions on the unchanged package. It retained 8/16/18 states, supplied cards, two accessories, draft limits and exact previous/next frame/tray returns. No page errors, failed requests or HTTP requests occurred. Load took 12.1204 seconds, supporting this run's timing hypothesis without proving the original cause. Four GPU performance warnings remain Deferred risk / runtime timing evidence under FO disposition. No correction or retry follows from them.

Gap 90 now has bounded independent headless evidence alongside the retained compiler/stock, package verification and A4 raster evidence. The lease ended after 54.0097 seconds with all observed owned processes closed. Live/human acceptance and operation 198/artwork/330-context reconciliation remain open. Those boundaries precede section adoption and removal of equivalent custom generation. Contextual speakers/rings and H1 acceptance remain next priorities. All sections remain adopted=false.


### Continuation owner assigned; H1 merge held

FO notice `305d5f3f` assigns the continuation gap to StudFleet task `tz2fgk3x5t3j8ghwsrem380v`, `continue-instructions-with-prior-built-context`. The read-only task record is at ideation. FO reports dispatch to Bernoulli after backlog approval. This is ownership and design progress, not a delivered capability or CLI pass.

The first specimen is step 61: two prior rails from operation 164 plus four new ring parts from operations 185–190. The full boundary remains 326 to 330 pieces, with 324 earlier pieces explicitly omitted from the focused view. Ideation first examines a supported full-plan/section-export alternative. No new schema is preapproved. The task owns this boundary separately from 7d, cn and 90. Fake seeds or supplied-stock declarations cannot replace prior ownership.

H1 remains provisional and unmerged. FO reports that its six-AC review and labeled manual-equivalence bridge passed, but merge preflight found five conflicts against accepted main `84ab84b`. No merge occurred. Guard rework superseded terminal approval. The producer now reconciles accepted main and H1 for `validation/2`. Existing DSS evidence does not establish the reconciled candidate.

Next priority is the continuation task's supported-path decision and bounded design proof, followed by H1 reconciliation evidence when supplied. No heavy slot is available. Supplied-unit evidence `990e37b` remains green without a redundant test. Figure operation 198, artwork, vehicle context, live/human review and full-manual parity remain distinct. All sections remain `adopted=false`. This update changed only dependency and gap records; no tests or workflow actions ran.


### H1 delivered locally; continuation design next

[Read-only delivery audit](../evidence/integration/h1-local-delivery-audit/README.md) confirms actual merge `8c325eb9550fb1e675705829f7287370cc48e333`, its parents and tree. Audited H1 and connector file identities match the independent report. H1 advances from provisional/unmerged to delivered locally. DSS's viewer matches the bridge's original viewer, while its separately exported PDF remains a distinct artifact. The original labeled upstream manual drive, corrected artifact bridge and DSS headless/A4 evidence retain their respective scopes.

No new combined-main CLI or fresh live/human evidence accompanies this delivery. Retained H1 `b410216e` and connector `1267d4eb` binaries stay separate. No runtime test repeated. Section and full-manual acceptance remain open, with all sections adopted=false.

Next priority is continuation task `tz2fgk3x5t3j8ghwsrem380v`. FO reports its 16-case API prototype and full348/visible6 partition proof passed; design review is next. This is not implementation delivery or DSS CLI evidence. Figure operation 198, artwork and prior vehicle context remain distinct adoption requirements.

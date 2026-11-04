# Incremental instruction adoption

This preparation belongs to the existing `studfleet-parity-edition` in `docs/instructions`.
It creates no new workflow or approval.
The accepted legacy manual remains the builder-facing edition.
Small section packages remain separate review artifacts until their exact scope passes review.

## Source and section boundaries

The [generated manifest](../manifests/incremental-adoption.json) binds the retained model, MPD, and instruction plan.
It derives each entry state, new-piece set, exit state, and occurrence list from the retained plan.
These boundaries describe authored states, not physical certification or personal progress.

| Section | Entry pieces | New pieces | Exit pieces | Current evidence |
| --- | ---: | ---: | ---: | --- |
| Chassis step 2, operations 7–9 | 11 | 5 | 16 | Exact source and compiler checks |
| Speakers, step 56 | 299 | 12 | 311 | Isolated PDF and headless copy checks |
| Life rings, step 61 | 326 | 4 | 330 | Isolated PDF and headless copy checks |
| Candidate figure, step 66 | 330 | 8 | 338 | Supplied-unit candidate pending |
| 小英 and accessory, step 67 | 338 | 10 | 348 | Supplied-unit candidate pending |

A section entry state includes earlier pieces, but its tray includes only the section introductions.
A small context extraction can omit unrelated pieces from its view.
Its omission record must retain their identities and explain the scope.
An isolated recipe cannot prove attachment to the vehicle or placement timing within the complete manual.
Piece sets alone cannot prove completed-copy availability, retention, or consumption.

## Adoption order

1. Finish the H1 artifact checks under the next explicit render lease.
2. Review chassis step 2 as a section with eleven declared starting pieces.
3. Test the supplied-unit candidate for steps 66 and 67.
4. Add vehicle context and later-use scheduling checks to speakers and life rings.
5. Expand only after each section preserves its boundary and instruction meaning.

The H1 section does not replace construction of its starting chassis.
The supplied-unit contract must distinguish the assembled body from later accessories.
The eighteen new members across steps 66/67 do not automatically form one supplied unit.
The source and explicit supplied-unit provenance determine that split.

## Execution procedure

1. Read the section record and its dependency holds.
2. Pin the usable StudFleet binary, source revision, runtime, catalog, and input hashes.
3. If rendering needs a shared resource lease, obtain the lease before the heavy command.
4. Derive the section input from the retained source through the set adapter.
5. Preserve every matrix, part, color, occurrence, operation order, and source comment that the extraction retains.
6. Record the mapping between original occurrences and fresh imported occurrences.
7. Record the entry state and every omitted context occurrence.
8. Declare every recipe copy that enters, remains within, or leaves the section.
9. Run the supported input command with matching provenance.
10. Export a fresh section package with the same pinned inputs.
11. Run `studfleet verify --out PACKAGE` with the same binary.
12. Inspect every actual PDF page at A4 size.
13. Exercise the viewer overview, intermediate states, copy selection, and return actions.
14. Compare stock, captions, geometry, and step references with the retained manual.
15. Record failed commands before any correction.
16. Classify each finding as source, authoring, tool, runtime, or evidence-harness work.
17. Release the shared resource lease after all owned jobs end.
18. Report the changed gaps, remaining limits, and next priority to the user and StudFleet.

The existing [H1 invocation](../evidence/integration/h1-16b3094-check/artifact-invocation-prepared.json) is ready for the artifact lease.
Its commands remain unexecuted in this preparation.
No new section exporter or alternate construction sequence exists here.
Reusable input-contract changes belong to StudFleet.

## Section acceptance

Each section review retains these concrete results:

| Property | Required evidence |
| --- | --- |
| Source identity | Exact source hashes and occurrence crosswalk with all retained scalars |
| Boundary identity | Entry, introductions, and exit sets match the generated manifest |
| Ordered construction | Each intermediate state matches the original operation sequence |
| Copy ownership | No unavailable, duplicated, lost, or prematurely consumed copy |
| Stock | Complete inventory and per-step trays agree, including supplied members |
| Reader usability | Every PDF page and viewer path shows useful labels and required construction limits |
| Context | Vehicle attachment context is present, or its omission is explicit within the accepted scope |
| References | Recipe pages, later placements, and adjacent section references resolve correctly |
| Review scope | Headless, resident live, human acceptance, and full-edition parity remain separate |

A reviewer recommends acceptance for an exact package and scope.
The captain owns acceptance under the existing instruction workflow.
A successful specimen does not automatically accept a section or the whole edition.
A model defect returns to `docs/models` with the instruction source unchanged.

## Simplification after acceptance

| Accepted capability | Active logic that it can replace | Evidence that remains |
| --- | --- | --- |
| Connector inspection | Manual triage of the former backend failure | Old failure, source pins, partial coverage, physical limits |
| Neutral installed views | Local arrow-hiding workarounds | Unknown movement and insertion limits |
| Reader labels | Template-specific text cleanup | Label source and exact artifact review |
| H1 composition | Custom merging of supported main operations | Original order and intermediate states |
| Supplied figures | Figure-specific tray and recipe suppression | Supplied provenance and full purchasing stock |
| Recipe scheduling | Manual recipe order and copy-count prose | Copy maps and retention evidence |

Acceptance retires only equivalent logic for the accepted scope.
The archived legacy compiler and PDF generator remain intact.
Unmigrated sections retain their current path.
Shared prefixes, shield paths, guides, print sheets, and purchasing exports need their own evidence.

## Complete edition and fallback

Section adoption does not splice new pages into the published PDF.
A complete candidate needs one coherent navigation system, inventory, page map, and package identity.
That candidate needs full independent review before it can replace the legacy edition.
Publication remains a separate action for the exact accepted package.

If a new section fails, retain its failure evidence and use the legacy edition.
The source pins and section records make the affected scope explicit.
No accepted source or legacy output needs replacement during preparation.

## Refresh the preparation

Run `python3 scripts/prepare_incremental_adoption.py` from the repository root.
The script refuses changed baseline hashes or duplicate piece introductions.
It checks all 68 steps against all 348 retained occurrences.
Its output is a preparation manifest, not an executable StudFleet plan.

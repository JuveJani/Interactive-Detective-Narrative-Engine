# Changelog — IMPLEMENTATION_PLAN.md

Revision history for `IMPLEMENTATION_PLAN.md` only.

This is a separate file rather than an entry in the repository's `CHANGELOG.md`, because that file is the project release changelog for Alpha 0.1 through 0.2b and editing it would be a repository implementation change, which this task excludes.

---

## v2.1 — 2026-07-28

Corrective revision. Removes implementation blockers so that implementation can begin. No accepted decision changed, no architecture redesigned, no implementation work added or removed, and the phase order P0–P10 is unchanged.

### Issue 1 — Per-phase ratification gating

| # | Section | Modification | Reason |
|---|---|---|---|
| 1 | § 14, preamble | Removed "Each item must be resolved and recorded in commit C0 before P1 begins." Replaced with a statement that each item is required by a specific phase and an `OPEN` item blocks only that phase and later ones. | The global gate made all ten ratifications block P1, including six that no phase before P5 needs. This was the primary implementation blocker. |
| 2 | § 1, paragraph 3 | Removed "Status advances to `Approved` when § 14 is empty, and only then may P1 begin." Replaced with: the document is authoritative for implementation at `In Review`; status records the review state, not permission to execute; phase entry is governed solely by § 3.2. | The status field was a second, independent global gate. Decoupling it removes the blocker while honouring the earlier instruction that status stay `In Review` until ratifications resolve. |
| 3 | § 3.2 | **New section: Ratification gating.** States that only ratifications required by the phase being entered must be resolved; defines the three outcomes (`RESOLVED` or `DEFERRABLE` → enter, `OPEN` → stop and report); states that a later block does not unwind completed earlier phases; defines `DEFERRABLE`. | Issue 1 requires an explicit per-phase gate with a defined stop condition. Previously the plan had no gating mechanism at all, only a global precondition. |
| 4 | § 14, ratification map | **New table** with **Required by** and **Status** columns for all ten items, plus the line "Phases clear to enter: P0, P1, P2, P3, P4." | The gate in § 3.2 needs a machine-checkable input. Without the map, an implementer cannot tell which ratifications apply to the phase being entered. |
| 5 | § 3, phase table, P0 row | Work changed from "Resolve every ratification in § 14; decide duplicate-file policy" to "Publish the ratification map in § 14; record any resolutions reached; confirm the phases that are clear to enter." | P0's old exit criterion was ten maintainer decisions, so P0 itself could never be completed by an implementer. The new criterion is achievable and preserves P0's slot in the unchanged phase order. |
| 6 | § 14.6 Duplicate-root-file policy | Status changed to `DEFERRABLE`, **Required by** set to "none in this revision", with the reason stated: no commit in C1–C9 edits any of the eight root copies or their canonical twins, because this revision edits no engine file. | The item was P0's second blocking deliverable. Since no phase in this revision touches an affected file, it cannot block anything. This unblocks P0. |
| 7 | § 14.7 Multi-class clue diversity | **Required by** changed from C1 to C5, with the reason stated: it is a threshold rule, not a vocabulary rule. | § 11.3 of v2.0 assigned the counting rule to C1 while § 11.2 tied it to a ratification needed for threshold evaluation in C5. The item blocked C1 only because of that misassignment. This unblocks P1. |
| 8 | § 14.9 Umbrella conclusion identifiers | **Required by** confirmed as C5, with an added statement that it does not gate C3 because § 8.7 assigns both identifiers a mechanically derived status and `DEPRECATED` is not assignable in C3. | The item blocked validation of P3 via gate `V2`. The mechanical derivation rule removes the dependency. This unblocks P3. |
| 9 | § 14.10 Route A classification | Marked **RESOLVED**, with provenance recorded: the recovery-workflow mechanism was one of three answers the accepted-decision authority itself enumerated when it required Route A's exact operation to be defined. The residual question was terminology, now settled in § 5.1. | The item blocked C2. It asked whether an option the accepting authority had already sanctioned was acceptable, so it was redundant rather than open. This unblocks P1. Provenance is recorded so a maintainer can reopen it trivially. |
| 10 | § 5.1 Objective | Route wording changed to "Two independent routes reach primary-archive access: one acquires the passphrase, and one bypasses it at a cost." | Consequence of item 9. The imprecise phrase "two independent acquisition routes" was what raised § 14.10; stating the position exactly closes it without changing any content. |
| 11 | § 5.8 | Added to the fifth-chain bullet: the case-overview section is a non-authoritative summary under `V10`, so § 14.4 gates only C6 and does not affect the canonical facts written in C2. | Without this, § 14.4 could be read as gating C2, which would re-block P1. |

**Net effect of Issue 1:** P0, P1, P2, P3 and P4 have no `OPEN` blocking ratification. The first blocked phase is P5.

### Issue 2 — Gate `V2` had no owning commit

| # | Section | Modification | Reason |
|---|---|---|---|
| 12 | § 8.7 | **New section: Identifier status declaration.** Assigns status declaration to **C3**. Defines a mechanical derivation rule from the P2 occurrence manifest: referenced at least once → `ACTIVE`, declared but unreferenced → `DEFINITION_ONLY`. States that `RESERVED` and `DEPRECATED` are not assigned in C3. Names the four recording documents, all already in C3's scope. Defines staged family coverage. | `V2` required a status on every declared identifier, but no commit was assigned the work, so `V2` could not pass after C3 as § 8.8 of v2.0 required. This was the second implementation blocker. C3 is the appropriate existing commit because it is the commit that touches the identifier namespaces, and no new phase or file is created. |
| 13 | § 8.7, derivation rule | Rule made purely mechanical, with no per-identifier judgement. | C3 must remain behaviour-neutral and independently revertible per § 4 rule 4. A judged status would import semantics into the rename commit and would also reintroduce the § 14.9 dependency. |
| 14 | § 13, gate `V2` | Added scoping: "Every declared identifier **in a migrated family**", plus "Family coverage follows § 8.7: the four families migrated in C3 after C3, additional families as their owning documents are edited, and every family at P10." | Unscoped, `V2` demanded statuses for `EVT_*` and variable identifiers whose owning documents are not edited until C4, C5 and C7. It was unsatisfiable after C3 by construction. |
| 15 | § 3, phase table, P3 row | Work extended to "Mechanical identifier rename only; identifier status declaration". | Records the assignment in the phase table so the two statements agree. |
| 16 | § 3.1, C3 row | Content extended with "identifier status declaration per § 8.7"; revert impact changed to "Pure spelling and status revert". | Same, for the commit plan. |
| 17 | § 3, second load-bearing rule | P3's behaviour-neutrality statement extended: "changes identifier spelling **and assigns mechanically derived statuses**, and nothing else". | The rule previously said P3 changes spelling and nothing else, which the new work would have contradicted. |
| 18 | § 4, rule 4 | Added: "and why the statuses C3 assigns are mechanically derived rather than judged". | Ties the revertibility requirement to the reason the derivation must stay mechanical. |
| 19 | § 8.9 | Changed to "Gates `V1`, `V2` after C3, with `V2` scoped per § 8.7." | Points the gate at its scoping rule instead of the unsatisfiable unscoped form. |
| 20 | § 8.8 | New side effect: status derivation depends entirely on the P2 manifest, so the manifest is a hard prerequisite of C3, not a convenience. | The mechanical rule has a single point of failure. If the manifest is incomplete, statuses are wrong in a way that looks correct. |
| 21 | § 9.6 | Added `FACT_` statuses to the C4 description of `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md`. | Required by the staged coverage in § 8.7; `FACT_` is the one family whose owning document is edited in C4. |
| 22 | § 10.4 | Clue register column list changed from "acquisition status" to "status". | The register column is the `V2` status field. The v2.0 wording named a different, undefined concept. |

### Issue 3 — Other internal inconsistencies that would block a start

| # | Section | Modification | Reason |
|---|---|---|---|
| 23 | § 3.1, C0 row and trailing note | Added: "C0 is a plan-only commit and occurs twice, once in P0 and once in P2. It modifies no repository canon file." | § 3.1 assigned C0 to both P0 and P2 while § 4 rule 1 forbade any commit spanning two phases. A direct contradiction an implementer would hit at P0. |
| 24 | § 4, rule 1 | Changed to "The nine repository-canon commits C1–C9 … and none of them spans two phases. C0 is exempt because it touches no canon file." | Resolves the same contradiction from the rule's side, without adding a commit or a phase. |
| 25 | § 11.1 | Added: "**C1 declares the vocabulary only.** The class-diversity counting rule is a separate item and lands in C5; see § 11.2." | v2.0 § 11.3 put "vocabulary and counting rule" in C1 while § 11.2 made the rule contingent on a ratification needed for C5. C1's scope was ambiguous. |
| 26 | § 11.2 | **New section: The class-diversity counting rule lands in C5.** States that the rule is a threshold rule, is written in C5 alongside the threshold restatement, and that § 14.7 gates C5 and not C1. | Splits the two sub-items that were conflated in v2.0, which is what unblocks C1 per item 7. |
| 27 | § 11.3, § 11.4, § 11.5, § 11.6 | § 11.3 reduced to tagging work only. § 11.4 replaced with a per-commit affected-files table distinguishing C1 from C5 rows. § 11.5 and § 11.6 renumbered. | The old § 11.3 prose listed C1 and C5 work in one sentence with no commit column, so an implementer could not tell which edit belonged to which commit. |
| 28 | § 11.5 | New side effect: `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` is edited twice, § 2 in C1 and § 3 in C5, and the sections are disjoint so the edits do not conflict. | The file being touched by two commits was previously unstated and would look like a commit-boundary violation. |
| 29 | § 11.6 | Added: "C1 requires only `V10`, because no clue is tagged and no threshold is evaluated in C1." | v2.0 named only `V7` for Decision 7, which cannot pass after C1 since no clue is tagged in C1. C1 had no satisfiable gate. |
| 30 | § 8.2, third bullet | Removed the trailing clause "so the file is touched once". | The claim became false once § 11.1 confirmed C1 also edits that file. Kept the substantive part, that `CLU-0n` replacement happens in C5 and not in C3. |
| 31 | § 1.3 | Added: "The location is fixed by this section and requires no repository edit; the three fields are written once, in commit C9." | § 3.1 listed "schema-metadata location fixed" as C1 content while § 1.3 said the fields are written in C9. An implementer would have looked for a C1 edit that does not exist. |
| 32 | § 3.1, C1 row | Removed "schema-metadata location fixed" from C1's content list. | Same. C1 has no repository edit for it. |
| 33 | § 8.3 | Added that the two umbrella identifiers "receive a mechanically derived status under § 8.7 rather than a judged one", and that § 14.9 is "required by C5". Final sentence extended to "a ratification decision that C5 needs and C3 does not." | Makes explicit that C3 is not blocked, which is the substance of item 8. |
| 34 | § 9.4.4 | Removed the phrase "changes disposition from the previous revision of this plan" from the `A_REED_ROOM` note. | Referenced a superseded revision, which is meaningless to an implementer reading v2.1. The disposition and its justification are unchanged. |
| 35 | Frontmatter | `version` 2.0 → 2.1. | Records the revision. `status` remains `In Review`; see item 2. |

### Verification performed on v2.1

| Check | Result |
|---|---|
| Section numbering sequential | Pass. §§ 1–15 with subsections in order; § 3.1 precedes § 3.2. |
| Inbound cross-references to § 14.x resolve to the intended item | Pass, 11 references checked. Item numbering 14.1–14.10 is deliberately unchanged from v2.0 so that no cross-reference elsewhere required editing. |
| Inbound cross-references to § 3.1, § 3.2, § 5.1, § 8.7, § 11.2, § 12.4 resolve | Pass. |
| Every commit C1–C9 has at least one satisfiable gate | Pass. C1 → `V10`; C2 → covered by C6 gates per § 5.9; C3 → `V1`, `V2` scoped; C4 → `V2`, `V4`; C5 → `V4`, `V7`, `V9`; C6 → `V1`, `V7`, `V9`; C7 → `V3`, `V5`, `V11`; C8 → `V6`; C9 → P10. |
| Register arithmetic | Unchanged: 47 − 8 − 8 − 1 + 7 = 37 stored variables, 11 derived totals. |
| Baseline counts | Unchanged. No re-verification against the repository was performed, since this task excludes repository review. |

### Not changed

- All eight accepted decisions, verbatim in scope and intent.
- The phase order P0–P10 and every phase's assigned decisions.
- The nine repository-canon commits C1–C9 and their boundaries.
- The variable register in § 9.4, including every disposition.
- `GRANT_CLUE` semantics, derivation of totals, and idempotence in § 10.2.
- The rename scope in § 8.2 — still three families, no state-variable migration.
- Gates `V1`, `V3`–`V11` other than the `V2` scoping in item 14.
- The out-of-scope list in § 15.
- `engine_spec_version`, which remains `2.0` because no engine file is edited.

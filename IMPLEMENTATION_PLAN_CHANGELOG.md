# Changelog — IMPLEMENTATION_PLAN.md

Revision history for `IMPLEMENTATION_PLAN.md` only.

This is a separate file rather than an entry in the repository's `CHANGELOG.md`, because that file is the project release changelog for Alpha 0.1 through 0.2b and editing it would be a repository implementation change, which these tasks exclude.

---

## v2.2 — 2026-07-28

Specification update. Resolves the three ratifications that blocked P5, and folds the documentation inconsistencies recorded in `IMPLEMENTATION_REPORT_P0_P4.md` back into the plan. No completed implementation work was modified, no architecture redesigned, no earlier phase changed, and no implementation work added.

Repository canon was not touched. Only `IMPLEMENTATION_PLAN.md` changed.

### Ratifications resolved

#### § 14.5 Point values — RESOLVED

**Decision.** Every clue is worth exactly 1 point. No per-clue tuning in this revision.

**Rationale.** The multi-point awards already in the node graph are multi-clue grants, not single clues of higher value. `EVT_113_APARTMENT_SEARCH` awards `P_STAGED +1 or +2` and its own text reads "A successful careful search reveals **two of**" four listed findings; the same pattern holds at `EVT_123`, `EVT_210`, `EVT_211` and `EVT_242`. Under `GRANT_CLUE` those become several one-point grants, which reproduces the existing award ranges exactly. A uniform value also preserves every threshold already written, since `07_EVIDENCE_VALIDATION.md` § 2 and `12_CLUE_DEPENDENCY_GRAPH.md` state their gates as the small integers 2, 3 and 4, authored against a de-facto unit-value model. Any non-uniform assignment would silently move all of them.

| # | Section | Modification | Reason |
|---|---|---|---|
| 1 | § 14.5 | Replaced the open question with the decision, the rationale, and a computed-maxima table for all eleven derived totals | § 14.5 asked for point values; the maxima follow mechanically from § 10.3 once the value is fixed |
| 2 | § 14.5 | Recorded that group memberships sum to 66 across 65 distinct clues, and that `CLUE_PHOTO_WINDOW_MARKS` contributing one point to each of two groups is not a double award under § 10.2 | The one clue in two groups is the only case where the uniform rule needs interpretation |
| 3 | § 14.5 | Recorded that the computed maximum of 8 supersedes the declared range `0-5` on `P_ROOK`, and that reachability remains a `V9` question | Prevents the corrected maximum being read as a claim that the public-accusation threshold is reachable |
| 4 | § 10.5 | Replaced "Assigning a point value to 65 clues is a set of new design decisions" with a statement that values are uniform and C5 transcribes them | The side effect described work that the resolution has eliminated |
| 5 | § 9.4.2 | Added a pointer to § 14.5 for each total's computed maximum | Keeps one source of truth for the maxima rather than duplicating the table |

#### § 14.7 Multi-class clue diversity behaviour — RESOLVED

**Decision.** A clue contributes exactly one class to a diversity count. Multi-class tags record which classes a clue is eligible to fill; at evaluation each held clue is assigned to one of its tagged classes, and the assignment across the held set is chosen to maximise the number of distinct classes. N classes therefore require at least N distinct clues.

**Rationale.** Both class documents require classes to be *independent*: `07_EVIDENCE_VALIDATION.md` § 1 says "A major accusation requires multiple independent classes" and `05_CLUE_ARCHITECTURE.md` § 2 says "Critical conclusions require at least two independent classes". Independence holds between evidence items, so one item cannot supply two independent classes. Counting all tags would let two clues clear the three-class bar on `CON_ROOK_PUBLICLY_PROVABLE`, the strongest gate in the case and the one this ratification was raised to protect.

| # | Section | Modification | Reason |
|---|---|---|---|
| 6 | § 14.7 | Replaced the open question with the decision, the rationale, and the exact rule text C5 writes into `07` § 1 | C5 needs the wording, not a description of the wording |
| 7 | § 11.2 | Recorded the resolution, pointed to § 14.7 for the rule text, and clarified that a tag list records eligibility rather than simultaneous contribution | § 11.2 previously described the item as an open dependency of C5 |

#### § 14.9 Umbrella conclusion identifiers — RESOLVED

**Decision.** `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` are retired by marking them `DEPRECATED` in C5. They are not deleted and receive no thresholds. All gating uses the four tiered identifiers.

**Rationale.** Only the tiered forms carry thresholds: `12_CLUE_DEPENDENCY_GRAPH.md` § 7 defines a partial and a provable tier, § 8 defines an operational and a publicly provable tier, and neither umbrella has a threshold of its own. The C3 manifest measured both as unreferenced. Retaining them live would give one concept two names, which `V10` forbids. Marking rather than deleting follows the repository's own idiom: `docs/STYLE_GUIDE.md` § "Status values" defines Deprecated as "retained temporarily but should not be used in new material", `DEPRECATED` is already in the `V2` vocabulary where a deprecated identifier may be unreferenced, and deletion would make the C3 registry rows vanish one commit after they were added, obscuring the migration record.

| # | Section | Modification | Reason |
|---|---|---|---|
| 8 | § 14.9 | Replaced the open question with the decision and rationale | — |
| 9 | § 14.9 | Assigned the `CON_REED_PRESENT` regloss to the same commit, restating it as "Reed was present at the confrontation" | Report § 6.5 recorded a duplicate gloss deferred out of C3 by § 4 rule 5. C5 is the commit that restates the thresholds these two identifiers gate, so it is the right home |
| 10 | § 8.3 | Changed "deferred to ratification § 14.9, which is required by C5" to record the resolution | The sentence described an open item |
| 11 | § 8.7 | Changed the `DEPRECATED` note to state that § 14.9 marks both identifiers `DEPRECATED` in C5 | Same |
| 12 | § 10.4 | Added a C5 row for `00_ENTITY_KEY_TABLE.md` covering the two deprecations and the regloss | C5's affected-files table had no row for this work |

### Gate and map updates following the resolutions

| # | Section | Modification | Reason |
|---|---|---|---|
| 13 | § 14 map | § 14.5, § 14.7 and § 14.9 changed from `OPEN` to `RESOLVED` | — |
| 14 | § 14 map | "Phases clear to enter" changed from P0–P4 to **P0–P5**, with P6 named as the first blocked phase and the blockers for P6, P7 and P8 listed | The § 3.2 gate reads this line |
| 15 | § 16.2 | Added three rows recording the resolutions and their one-line rationale | § 16.2 is the C0 ratification record and must reflect the current state |
| 16 | § 16.3 | Reduced the open list from eight items to five | — |
| 17 | § 16.4 | Updated to P0–P5 clear, P6 first blocked | — |
| 18 | Frontmatter | `version` 2.1 → 2.2 | `status` remains `In Review`; five ratifications are still `OPEN`, so the § 1 condition for `Approved` is unmet |

### Documentation inconsistencies from IMPLEMENTATION_REPORT_P0_P4

Each of these was a plan-side documentation error. None required a repository change, and none was applied to repository canon.

| # | Report § | Section | Modification | Reason |
|---|---|---|---|---|
| 19 | 6.2 | § 2 | Distinct clue identifiers 64 → **65**, listings 65 → **66**, with the § 17.2 manifest cited as the measured source | § 8.5 makes the manifest authoritative. The baseline undercounted by one |
| 20 | 6.2 | § 8.2 | Rename table count 64 → 65 distinct | Same undercount |
| 21 | 6.2 | § 11.3 | "All 64 baseline clues" → 65; "Forty-three are untagged" → forty-four | Same undercount, propagated into the tagging workload |
| 22 | 6.2 | § 11.4 | "Tag 43 untagged clues" → "Tag 44 untagged clues; record 1 point per clue" | Same, and the row now also carries the point-value work resolved in § 14.5 |
| 23 | 6.2 | § 14.5 | "All 64 baseline clues" replaced by the resolution, which states 65 | Same |
| 24 | 6.1 | § 11.6 | Added that `V10` after C1 is scoped to the facts C1 declares an owner for, with the three ending rows enforced at C7 | § 11.6 required `V10` after C1 while § 6.3 assigns the ending reduction to C7. The gate was unsatisfiable as written |
| 25 | 6.1 | § 13, `V10` | Added staged coverage to the pass criterion, mirroring the `V2` treatment, with full coverage a P10 requirement | Same inconsistency, fixed on the gate side |
| 26 | 6.6 | § 3.1, C1 row | Replaced "ending-ownership rule declared" with the named files: vocabulary in `07` § 1, prefix registry and ownership rules in `00_ENTITY_KEY_TABLE.md` | No affected-files table named a document for the ownership rule, so C1's scope was ambiguous |
| 27 | 6.7 | § 9.6 | Added `LOGIC/07_EVIDENCE_VALIDATION.md` to C4's file list, for the `EVAL_*` declarations the register names | `V4` cannot pass without them, and § 8.4 designates `07` as an `EVAL_` owner, but § 9.6 omitted the file |
| 28 | 6.4 | § 8.8 | Added a side effect recording that C3 registers `NPC_ROOK_NETWORK` in the Characters table, with the same justification as the five `CON_*` rows | The registration was required by `V2` but unnamed in the plan. Now documented so the C3 diff is explicable |
| 29 | 6.3 | § 17.1 | Reworded the lead-in to say the manifest *superseded* two § 2 counts which *have since been corrected*, and that the table is retained as the record | § 2 now carries the corrected values, so the correction table read as if the conflict were still live |

Report § 6.5 is covered by item 9 and report § 6.8 by items 13 to 17.

### Precision corrections made while resolving

| # | Section | Modification | Reason |
|---|---|---|---|
| 30 | § 14.5 maxima table | Four rows changed from "structural, authored in C5" to name the structural gate that already exists in `12` §§ 4, 6, 10 and 11, with the numeric restatement in C5 | The first wording implied those gates did not exist. They do; what C5 adds is their numeric restatement in `07` § 2 |

### Verification performed on v2.2

| Check | Result |
|---|---|
| Ratification map matches the ten subsection headings | Pass. Three carry `— RESOLVED` in the heading and `RESOLVED` in the map; five remain `OPEN`; one `DEFERRABLE`; § 14.10 unchanged |
| § 14 map, § 16.2, § 16.3 and § 16.4 agree | Pass. Five open items in both lists, P0–P5 clear in both places |
| No section still describes § 14.5, § 14.7 or § 14.9 as an open dependency | Pass. Zero matches for the previous "is required by C5" phrasing |
| No stale clue count remains | Pass. Zero matches for "All 64", "64 distinct", "43 untagged", "Forty-three", "point value to 65" |
| Section numbering sequential, § 3.1 before § 3.2 | Pass |
| Inbound cross-references resolve | Pass. § 14.x references at lines 229, 258, 277, 303, 315, 363, 417, 666, 695, 709, 736 all resolve to the intended item; item numbering unchanged since v2.0 |

### Not changed

- Any completed implementation. No file under `adventures/`, `engine/`, `templates/`, `docs/`, `data_dictionary/` or `reviews/` was touched.
- The eight accepted decisions.
- The phase order P0–P10 and each phase's assigned decisions.
- The nine repository-canon commits C1–C9 and their boundaries.
- The variable register in § 9.4 and every disposition in it.
- `GRANT_CLUE` semantics, derived totals and idempotence in § 10.2.
- The rename scope in § 8.2, still three families.
- Gates `V1`–`V9` and `V11`, other than the `V10` scoping in item 25.
- The five ratifications required by P6, P7 and P8, which remain `OPEN`.

---

## v2.1 — 2026-07-28

Corrective revision. Removes implementation blockers so that implementation can begin. No accepted decision changed, no architecture redesigned, no implementation work added or removed, and the phase order P0–P10 is unchanged.

### Issue 1 — Per-phase ratification gating

| # | Section | Modification | Reason |
|---|---|---|---|
| 1 | § 14, preamble | Removed "Each item must be resolved and recorded in commit C0 before P1 begins." Replaced with a statement that each item is required by a specific phase and an `OPEN` item blocks only that phase and later ones. | The global gate made all ten ratifications block P1, including six that no phase before P5 needs. This was the primary implementation blocker. |
| 2 | § 1, paragraph 3 | Removed "Status advances to `Approved` when § 14 is empty, and only then may P1 begin." Replaced with: the document is authoritative for implementation at `In Review`; status records the review state, not permission to execute; phase entry is governed solely by § 3.2. | The status field was a second, independent global gate. |
| 3 | § 3.2 | **New section: Ratification gating.** | Issue 1 requires an explicit per-phase gate with a defined stop condition. |
| 4 | § 14, ratification map | **New table** with **Required by** and **Status** columns for all ten items. | The gate in § 3.2 needs a machine-checkable input. |
| 5 | § 3, phase table, P0 row | Work changed from resolving every ratification to publishing the map, recording resolutions, and confirming clear phases. | P0's old exit criterion was ten maintainer decisions, so P0 could never be completed by an implementer. |
| 6 | § 14.6 | Marked `DEFERRABLE`, required by no phase. | No commit in C1–C9 edits an affected file, because this revision edits no engine file. |
| 7 | § 14.7 | **Required by** changed from C1 to C5. | § 11.3 assigned the counting rule to C1 while § 11.2 tied it to threshold evaluation in C5. |
| 8 | § 14.9 | Recorded that it does not gate C3. | The mechanical status rule in § 8.7 removes the dependency. |
| 9 | § 14.10 | Marked **RESOLVED** with provenance. | The item asked whether an option the accepting authority had already sanctioned was acceptable. |
| 10 | § 5.1 | Route wording made precise: two independent routes to primary-archive access, one acquiring and one bypassing at a cost. | Consequence of item 9. |
| 11 | § 5.8 | Added that the case-overview section is a non-authoritative summary, so § 14.4 gates only C6. | Without this, § 14.4 could be read as gating C2. |

### Issue 2 — Gate `V2` had no owning commit

| # | Section | Modification | Reason |
|---|---|---|---|
| 12 | § 8.7 | **New section: Identifier status declaration.** Assigns the work to C3 with a mechanical derivation rule from the P2 manifest. | `V2` required a status on every declared identifier but no commit was assigned the work. |
| 13 | § 8.7 | Rule made purely mechanical. | C3 must stay behaviour-neutral and independently revertible. |
| 14 | § 13, `V2` | Scoped to migrated families, with staged coverage and full coverage at P10. | Unscoped, `V2` demanded statuses for families whose documents are not edited until C4, C5 and C7. |
| 15 | § 3, P3 row | Work extended to include status declaration. | Records the assignment in the phase table. |
| 16 | § 3.1, C3 row | Content and revert impact extended. | Same, for the commit plan. |
| 17 | § 3, second load-bearing rule | P3 behaviour-neutrality statement extended to cover the mechanical statuses. | The rule previously said P3 changes spelling and nothing else. |
| 18 | § 4, rule 4 | Added the reason the derivation must stay mechanical. | Ties revertibility to the rule. |
| 19 | § 8.9 | `V2` pointed at its scoping rule. | — |
| 20 | § 8.8 | New side effect: the P2 manifest is a hard prerequisite of C3. | The mechanical rule has a single point of failure. |
| 21 | § 9.6 | Added `FACT_` statuses to the C4 description. | Required by the staged coverage in § 8.7. |
| 22 | § 10.4 | Clue register column renamed from "acquisition status" to "status". | The v2.0 wording named an undefined concept. |

### Issue 3 — Other internal inconsistencies

| # | Section | Modification | Reason |
|---|---|---|---|
| 23 | § 3.1 | C0 declared a plan-only commit occurring twice. | § 3.1 assigned C0 to both P0 and P2 while § 4 rule 1 forbade a commit spanning two phases. |
| 24 | § 4, rule 1 | Scoped to the nine canon commits, exempting C0. | Same contradiction, from the rule's side. |
| 25 | § 11.1 | Added that C1 declares the vocabulary only. | C1's scope was ambiguous between vocabulary and counting rule. |
| 26 | § 11.2 | **New section** placing the counting rule in C5. | Splits the two sub-items conflated in v2.0. |
| 27 | §§ 11.3–11.6 | § 11.3 reduced to tagging; § 11.4 replaced with a per-commit table; later subsections renumbered. | The old prose listed C1 and C5 work in one sentence with no commit column. |
| 28 | § 11.5 | New side effect: `05_CLUE_ARCHITECTURE.md` is edited twice, in disjoint sections. | Previously unstated, and would look like a boundary violation. |
| 29 | § 11.6 | Added that C1 requires only `V10`. | v2.0 named only `V7`, which cannot pass after C1. |
| 30 | § 8.2 | Removed the clause "so the file is touched once". | Became false once § 11.1 confirmed C1 also edits that file. |
| 31 | § 1.3 | Added that the location requires no repository edit and the fields are written in C9. | § 3.1 listed the location as C1 content while § 1.3 put the fields in C9. |
| 32 | § 3.1, C1 row | Removed "schema-metadata location fixed". | Same. |
| 33 | § 8.3 | Recorded the mechanical status and the C5 requirement for the umbrella identifiers. | Makes explicit that C3 is not blocked. |
| 34 | § 9.4.4 | Removed a phrase referencing a superseded revision. | Meaningless to an implementer reading v2.1. |
| 35 | Frontmatter | `version` 2.0 → 2.1. | Records the revision. |

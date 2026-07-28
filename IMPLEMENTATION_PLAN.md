---
title: Implementation Plan — Next Repository Revision
version: 2.1
status: In Review
depends_on:
  - docs/STYLE_GUIDE.md
  - engine/03_ARCHITECTURE.md
  - engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md
  - data_dictionary/SCHEMA_VERSIONING.md
used_by:
  - adventures/The_Last_Witness/DO_NOT_READ/LOGIC/
  - CHANGELOG.md
last_review:
reviewer:
---

# Implementation Plan — Next Repository Revision

## 1. Purpose and authority

This document is the implementation specification for the next repository revision. It converts eight accepted decisions into per-file edit instructions, a phase order, a commit plan, a complete variable register, a rollback strategy, and a validation gate.

This document does not implement anything. It contains no repository edits.

**This document is authoritative for implementation at `status: In Review`.** Status records the review state of the specification, not permission to execute it. Phase entry is governed solely by the ratification gate in § 3.2. Status advances to `Approved` when § 14 contains no `OPEN` item; that advance is a bookkeeping act and is not a precondition for any phase.

Where this document conflicts with an existing repository document, it governs **only for the duration of the migration**. On completion, every rule stated here must exist in its owning source document and this plan becomes a historical record, per `engine/03_ARCHITECTURE.md` § "3.10 Review Layer".

### 1.1 Target release

**Prototype Alpha 0.2c**, not Alpha 0.3. `DO_NOT_READ/07_PROTOTYPE_BUILD_PLAN.md` § "Required before player-book compilation" reserves Alpha 0.3 for the narrative compiler pass. This revision performs no narrative compilation.

### 1.2 Schema version impact

| Field | Before | After | Reason |
|---|---|---|---|
| `engine_spec_version` | `2.0` | `2.0` | **No engine file is edited in this revision.** The prefix registry moves to the adventure layer and the clue-class requirement is not promoted to the engine. |
| `data_dictionary_version` | `0.3` | `0.3` | No schema records exist to change. |
| `adventure_schema_version` | `0.1` | `1.0` | Three identifier families are renamed. Existing adventure data does not survive. |

### 1.3 Schema-version metadata location

One location only: **frontmatter of `adventures/The_Last_Witness/README.md`**, which is the adventure root record required by `data_dictionary/SCHEMA_VERSIONING.md` § "2. Required Version Fields".

No other adventure file gains frontmatter in this revision. The location is fixed by this section and requires no repository edit; the three fields are written once, in commit C9.

### 1.4 Defect classification

Using `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § "9. Post-Playtest Review":

| Decision | Classification |
|---|---|
| 1 — Passphrase | `ADVENTURE_LOGIC_DEFECT` + `CONTENT_DEFECT` |
| 2 — `NODE_TYPE` | `ADVENTURE_LOGIC_DEFECT` |
| 3 — `Outgoing` | `ADVENTURE_LOGIC_DEFECT` |
| 4 — State variables | `ADVENTURE_LOGIC_DEFECT` |
| 5 — Graph mapping | `ADVENTURE_LOGIC_DEFECT` |
| 6 — Progress model | `ADVENTURE_LOGIC_DEFECT` |
| 7 — Clue classes | `ADVENTURE_LOGIC_DEFECT` |
| 8 — Namespaces | `ADVENTURE_LOGIC_DEFECT` |

Every engine rule involved is already correct. Only the adventure fails to implement it, so no decision is an `ENGINE_RULE_DEFECT` in this revision.

---

## 2. Baseline inventory

Counts verified at commit `0923366cd3f1302a849f072dedc5b9be1d4e19a1`. These are the denominators for § 13.

| Quantity | Count | Source |
|---|---:|---|
| Nodes in the investigation graph | 40 | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| Nodes declaring an `Outgoing` block | 3 | `EVT_110`, `EVT_111`, `EVT_120` |
| Nodes declaring successors as "unlocks" inside **State changes** | 1 | `EVT_100_SHARED_BRIEFING` |
| Nodes declaring `NODE_TYPE` | 0 | — |
| Backbone entries in the core graph | 19 | `LOGIC/05_CORE_EVENT_GRAPH.md` |
| Distinct clue identifiers | 64 | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` (65 listings; `C_PHOTO_WINDOW_MARKS` in §§ 4 and 11) |
| Clue groups carrying class tags | 3 of 10 | §§ 2, 3, 8 |
| Deduction identifiers (`D_*`) | 13 | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| Conclusion identifiers (`CON_*`) | 10 | `LOGIC/00_ENTITY_KEY_TABLE.md` § "Conclusions" |
| Declared state variables | 47 | `LOGIC/01_WORLD_STATE_VARIABLES.md` §§ 1–9 |
| Variables used but never declared | 2 | `P_LENA_PROTECTING`, `P_DECOY` |
| State machines with no declared variable | 4 | `LOGIC/11_LOCATION_STATE_MACHINE.md` §§ 4, 5, 7, 8 |
| Ending families | 8 | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 6 |
| Ending families with a node identity | 0 | — |

---

## 3. Global phase order

Phases are strictly ordered. No phase begins while its predecessor's required gates fail.

| Phase | Work | Decisions | Commit |
|---|---|---|---|
| **P0** | Publish the ratification map in § 14; record any resolutions reached; confirm the phases that are clear to enter | — | C0 (plan only) |
| **P1** | Canonical ownership rules; World Bible passphrase facts | 7, 8 (registry), 1 (facts) | C1, C2 |
| **P2** | Complete migration manifests; full variable, clue and node registers | 4, 6, 8 | C0 (plan only) |
| **P3** | Mechanical identifier rename only; identifier status declaration | 8 | C3 |
| **P4** | Non-progress state-variable cleanup and writer/reader wiring | 4 | C4 |
| **P5** | Clue classes and progress model atomically, including progress variables | 6, 7 | C5 |
| **P6** | Passphrase routes and failure transformation | 1 | C6 |
| **P7** | `NODE_TYPE`, terminal nodes, and all `Outgoing` edges atomically | 2, 3 | C7 |
| **P8** | Core-to-investigation graph mapping | 5 | C8 |
| **P9** | Version, changelog, README, release metadata | — | C9 |
| **P10** | Final validation | all | none |

Two ordering rules are load-bearing and must not be relaxed:

- **P3 is behaviour-neutral.** No variable is deleted, no conclusion is split, no threshold moves, no semantic replacement occurs. P3 changes identifier spelling and assigns mechanically derived statuses, and nothing else, so it is independently revertible.
- **P4 excludes progress variables.** Their readers are the conclusion evaluators, which do not exist until P5. Wiring them in P4 would fail gate `V4` by construction. Non-progress state is wired in P4; progress state is converted in P5.

### 3.1 Commit plan

| Commit | Phase | Content | Revert impact |
|---|---|---|---|
| **C0** | P0, P2 | Ratification map, resolutions reached, and migration manifests, recorded in this plan | None on repository canon |
| **C1** | P1 | Canonical ownership: clue-class vocabulary single-sourced; ending-ownership rule declared; prefix registry added to the entity key table | Reverts to two class lists; no logic depends on it yet |
| **C2** | P1 | World Bible passphrase facts, with the version change its § 1 Authority requires | Reverts the canonical fact; P6 becomes ungrounded |
| **C3** | P3 | Mechanical identifier migration: `C_*`→`CLUE_*`, `D_*`→`CON_*`, backbone `EVT_*`→`ARC_*`; identifier status declaration per § 8.7 | Pure spelling and status revert; no semantics attached |
| **C4** | P4 | Non-progress state-variable cleanup and writer/reader wiring | Restores removed variables and unwires writers |
| **C5** | P5 | Clue-class assignment, class-diversity counting rule, and progress-model conversion, atomically | Restores point-award syntax and untagged clues |
| **C6** | P6 | Passphrase routes, thresholds, failure transformation | Removes both routes; C2 facts remain |
| **C7** | P7 | Node metadata, eight terminal nodes, complete outgoing graph | Removes all edges; graph returns to edgeless |
| **C8** | P8 | Core-to-investigation mapping | Removes the mapping file |
| **C9** | P9 | Release metadata, changelog, README, schema-version fields | Reverts release identity only |

C0 is a plan-only commit and occurs twice, once in P0 and once in P2. It modifies no repository canon file.

### 3.2 Ratification gating

**Only the ratifications required by the phase being entered must be resolved. Ratifications required by a later phase do not block an earlier phase.**

Before entering a phase, the implementer checks the ratification map in § 14 for items whose **Required by** column names that phase.

- If every such item is `RESOLVED` or `DEFERRABLE`, the phase is entered.
- If any such item is `OPEN`, implementation stops at that phase, the blocking item is reported, and no work from that phase or any later phase is performed.
- Work already completed in earlier phases is not reverted by a later block. The chain halts forward, it does not unwind.

An item marked `DEFERRABLE` is required by no phase in this revision. It does not block entry to any phase and may be carried into a later revision provided the deferral is recorded in C0.

---

## 4. Rollback strategy

1. **One commit per implementation unit.** The nine repository-canon commits C1–C9 in § 3.1 are the only permitted granularity, and none of them spans two phases. C0 is exempt because it touches no canon file.
2. **Validation after every commit.** The gate subset named in each decision section must pass before the next commit is authored. A failing gate halts the phase; it is not deferred to P10.
3. **No phase proceeds while its required checks fail.** P10 is a final confirmation, not the first time gates are run.
4. **The mechanical rename must be independently reversible.** C3 must be revertible with a single `git revert` that restores the repository to its C2 state with no semantic residue. This is why variable deletion, conclusion splitting and alias replacement are all excluded from C3, and why the statuses C3 assigns are mechanically derived rather than judged.
5. **Semantic changes never share a commit with bulk renaming.** If a semantic problem is discovered during C3, it is recorded and deferred to C4 or later. C3 does not fix it in place.
6. **Reverting a commit reverts every commit after it.** The chain C1→C9 is linear and each commit assumes its predecessors. There is no partial-revert path.

---

## 5. Decision 1 — The ledger passphrase

### 5.1 Objective

The passphrase remains a mandatory authentication factor for the primary archive. Two independent routes reach primary-archive access: one acquires the passphrase, and one bypasses it at a cost. Every gate that governs the archive states the same requirement.

### 5.2 Route A — the exact operation

Route A does **not** hand the players the passphrase. It unlocks a recovery workflow.

`DO_NOT_READ/01_WORLD_BIBLE.md` § "4. The ledger" > "Access" already establishes three factors: hardware key, passphrase, six-digit recovery code. The C2 fact addition states that Elias configured a documented passphrase-recovery procedure and that Nadia holds the written instructions alongside the encrypted upload. With the hardware key present and the complete six-digit code entered, the workflow permits a passphrase **reset** in place of passphrase **entry**.

The reset is not free, and this is what keeps the passphrase mandatory rather than decorative:

- it consumes additional time at `EVT_430_COMPLETE_TRANSFER`;
- it is logged, which downgrades authentication.

`LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "3. Evidence outcome" already distinguishes "Full authenticated transfer", which requires "preserved authentication", from "Partial official evidence". Route A therefore yields access at partial-authentication quality. Route B yields access with authentication intact.

No new item identifier is created. The instructions are content of the existing encrypted upload and are delivered as a clue, not tracked as physical custody, because nothing in the accepted decisions turns on who physically holds them.

### 5.3 Route B — the exact operation

Elias states the passphrase as a fragment. `DO_NOT_READ/03_CHARACTER_DATABASE.md` § `NPC-01` > "Statements while conscious" already establishes a fragment mechanism from 21:15. Route B is post-discovery and closes when `ELIAS_STATE` reaches `CRITICAL_UNRESPONSIVE`, which `LOGIC/01_WORLD_STATE_VARIABLES.md` § "1. Global clock" places at 01:00.

Route B being post-discovery is not circular for this factor. The passphrase is only needed once the primary key is held, and `DO_NOT_READ/01_WORLD_BIBLE.md` § "14. Immutable facts" fixes the primary key inside Signal Room 4B. This reasoning is recorded in the clue register so a later audit does not misread Route B as circular.

### 5.4 Clue and conclusion additions

| Identifier | Status | Note |
|---|---|---|
| `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` | **Existing** — already declared in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § 11 as `C_UPLOAD_RECOVERY_INSTRUCTIONS` | Route A. Reused, not created. |
| `CLUE_ELIAS_FRAGMENT_PASSPHRASE` | **New** | Route B. One new clue. |
| `CON_PASSPHRASE_ACCESS` | **New** | One new conclusion, with two tiers of quality rather than two tiers of strength. |

Decision 1 therefore adds exactly one clue and one conclusion.

### 5.5 Rejected candidates

Recorded so the decision is not silently revisited.

| Candidate | Verdict | Basis |
|---|---|---|
| Signal Room 4B physical mnemonic | Reject as a counted route | Co-located with the primary key; adds no independence. |
| Lena | Reject | `03_CHARACTER_DATABASE.md` § `NPC-03`: "She does not understand the full ledger or upload process." |
| Marcus | Reject | `01_WORLD_BIBLE.md` § 11: "Marcus does not know the exact hiding room or the ledger passphrase." |
| Reed's laptop | Reject | `01_WORLD_BIBLE.md` § "4. The ledger" > "Copies" item 3 makes the decoy a separate archive. |

### 5.6 Failure transformation

Neither route obtained means no primary-archive access. This must not deadlock. It routes to `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "3. Evidence outcome" > "Evidence lost" or "Public leak" depending on whether an external copy exists, satisfying the "degraded but still solvable outcome" clause of `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § "5. Soft-Lock Prevention".

### 5.7 Affected files

| File | Section | Edit | Commit |
|---|---|---|---|
| `DO_NOT_READ/01_WORLD_BIBLE.md` | § "4. The ledger" > "Access" | Add "Passphrase custody and recovery": Elias set the passphrase; a documented reset workflow exists; Nadia holds the written instructions with the upload; the reset is logged and downgrades authentication | C2 |
| `DO_NOT_READ/01_WORLD_BIBLE.md` | § "14. Immutable facts" | One line: the passphrase or its logged reset is required for the primary archive, and neither is recoverable from the decoy | C2 |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | § `NPC-01` > "Knowledge" and "Statements while conscious" | Add the passphrase to Elias's knowledge; add one fragment; keep the ambiguity constraint | C2 |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | § `NPC-02` > "Knowledge" | Nadia holds the instructions, not the secret | C2 |
| `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | § "2. Nadia Soren" > "Disclosure stages" | Attach the instructions to an existing stage; create no new stage | C6 |
| `LOGIC/00_ENTITY_KEY_TABLE.md` | § "Conclusions" | Add `CON_PASSPHRASE_ACCESS`. No item row is added | C6 |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | new § "Passphrase access"; § "12. Critical-route audit" | Add the group with both clues classed and point-valued; audit row states 2 independent routes | C6 |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § "2. Conclusion thresholds"; § "6. Soft-lock audit" | Add the threshold and the two-route soft-lock subsection | C6 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_123`, `EVT_410`, `EVT_430` | `GRANT_CLUE(CLUE_UPLOAD_RECOVERY_INSTRUCTIONS)` at `EVT_123`; replace the unsourced "retrieve passphrase information" line in `EVT_410` with a reference to `CON_PASSPHRASE_ACCESS`; add the conclusion to `EVT_430` entry conditions with the two quality tiers | C6 |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § "3. Evidence outcome" | Full transfer requires Route B quality; Route A yields partial | C6 |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | § `ARC_420` | Add the passphrase to "Complete transfer requires" | C6 |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | § "END-03" | Confirm the wording covers passphrase failure; adjust only if it excludes it | C6 |
| `DO_NOT_READ/02_MASTER_TIMELINE.md` | § `### 01:45` | Verify only. Already names all three factors | C6 |

### 5.8 Side effects

- The best ending becomes strictly harder. `END_WITNESS_SPEAKS` now requires Route B specifically, because Route A caps authentication at partial. This is a difficulty change, not only a consistency fix.
- Route B closes at 01:00, so late runs are capped at partial-authentication transfer even on perfect play thereafter. That is intended, but it must be visible to the maintainer before C6 lands.
- `LOGIC/04_TIME_COST_MATRIX.md` § "2. Investigation action costs" has no entry for the reset workflow. C6 must add one, or `EVT_430` cannot cost it.
- `DO_NOT_READ/00_CASE_OVERVIEW.md` § "Fair solution" lists four chains and does not mention the passphrase. Ratification § 14.4 decides whether it gains a fifth. That section is a non-authoritative summary under `V10`, so the question gates only C6 and does not affect the canonical facts written in C2.

### 5.9 Validation

Gates `V1`, `V7`, `V9` after C6. Two routes sharing no granting node, no source actor and no location; at least one obtainable before 01:00; the failure path terminating in a declared ending node.

---

## 6. Decision 2 — `NODE_TYPE` and `TERMINAL_TYPE`

### 6.1 Objective

Every node declares `NODE_TYPE`. Every terminal node additionally declares `TERMINAL_TYPE` drawn from the list in `engine/03_ARCHITECTURE.md` § "3.18 Terminal architecture": `VICTORY`, `PARTIAL_SUCCESS`, `NARRATIVE_FAILURE`, `CHARACTER_DEATH`, `TIME_EXPIRED`, `CASE_UNRESOLVED`, `CAMPAIGN_CONTINUATION`.

`templates/EVENT_TEMPLATE.md` already carries `node_type` and `terminal_type`, so no template change is needed.

### 6.2 The eight ending families become nodes

The eight families in `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 6 have no node identity, so there is nothing to declare a type on. Eight terminal nodes are created in `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 14.

`EVT_900_RESOLVE_ENDING` is a dispatcher with successors and is `INTERMEDIATE`.

| Ending family | Proposed `TERMINAL_TYPE` | Confidence |
|---|---|---|
| `END_WITNESS_SPEAKS` | `VICTORY` | High |
| `END_EVIDENCE_WITHOUT_WITNESS` | `PARTIAL_SUCCESS` | Medium |
| `END_LIFE_SAVED_TRUTH_DELAYED` | `PARTIAL_SUCCESS` | High |
| `END_PROTECTIVE_CUSTODY` | `NARRATIVE_FAILURE` | High |
| `END_PUBLIC_LEAK` | `PARTIAL_SUCCESS` | High |
| `END_SILENT_TERMINAL` | `CHARACTER_DEATH` or `TIME_EXPIRED` | Low — ratification § 14.1 |
| `END_WRONG_ACCUSATION` | `CASE_UNRESOLVED` | High |
| `END_FRACTURED_TRUTH` | `PARTIAL_SUCCESS` | High |

### 6.3 Affected files

| File | Section | Edit | Commit |
|---|---|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "1. Graph conventions" | Add `NODE_TYPE` and `TERMINAL_TYPE` to the field list | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | all 40 nodes | Add `NODE_TYPE: INTERMEDIATE` | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "14. Ending dispatch" | Add eight terminal nodes with ratified types | C7 |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § 6 | Add node identifier and terminal type per family; triggers stay here | C7 |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | `END-01`…`END-08` | Reduce to narrative outcome text plus a marked non-authoritative pointer to the trigger owner | C7 |

### 6.4 Side effects

- Ending content lives in three files. Ownership is fixed in C1 and enforced by `V10`: triggers in `14`, node identity and edges in `10`, narrative outcome in `06`. Summaries and cross-references remain permitted provided they are marked non-authoritative.
- `END_FRACTURED_TRUTH` requires two players per `06_ENDING_FRAMEWORK.md` § "END-08". Once it is a node, reachability is mode-dependent, which is why `V5` is evaluated per declared play mode.
- Declaring 40 nodes `INTERMEDIATE` asserts every one has a successor. That is false until the edges land, which is why Decisions 2 and 3 share commit C7.
- Eight terminal nodes make overlapping ending triggers reachable simultaneously. Ratification § 14.8 and gate `V11` address precedence.

### 6.5 Validation

Gates `V3`, `V5`, `V11` after C7.

---

## 7. Decision 3 — `Outgoing` declarations

### 7.1 Objective

Every node declares `Outgoing`. Terminal nodes declare `Outgoing: None`. This closes the defect named in `engine/00_ENGINE_SPECIFICATION_2.0.md` § "3.8 Terminal nodes".

### 7.2 Scope of work

**All 40 existing nodes are reviewed and normalised, not only the 37 that lack an `Outgoing` block.** The three that already have one — `EVT_110`, `EVT_111`, `EVT_120` — are re-authored to the declared format and their targets validated against the final node set. Their current blocks predate the terminal nodes and the passphrase work and cannot be assumed correct.

`EVT_100_SHARED_BRIEFING` requires a correction rather than an addition: its two successors sit in **State changes** as "unlocks" lines. A successor is a graph edge, not a state mutation, and leaving it there corrupts the writer/reader analysis in § 9.

Total: 40 existing nodes normalised, 8 new terminal nodes authored.

### 7.3 Split-branch terminators

`engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § "5. No Free Asynchronous Drift" requires every split branch to terminate in `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT` or `TERMINAL_OUTCOME`. None appears in the adventure.

This is an inference from an existing engine MUST, not part of the literal accepted decision. Ratification § 14.2 decides whether it is in scope for C7.

### 7.4 Affected files

| File | Section | Edit | Commit |
|---|---|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "1. Graph conventions" | Promote outgoing routes to a mandatory field with a stated format | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_100` | Move the two "unlocks" lines into `Outgoing` | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_110`, `EVT_111`, `EVT_120` | Re-author existing blocks to format; validate targets | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | 36 remaining nodes | Author `Outgoing` | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | 8 terminal nodes | `Outgoing: None` | C7 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "15. Graph integrity rules" | Restate as checkable assertions over the explicit edge set | C7 |
| `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | §§ 2, 4, 7 | Declare node membership per split phase, if § 14.2 is ratified in scope | C7 |

### 7.5 Side effects

This is the highest-yield and highest-risk commit.

- **Authoring edges forces reachability decisions that are currently unmade.** Two known problems surface immediately. The room-identifier chain: three of five identifier clues in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § 4 come from Elias, Lena and Iris, all placed inside Signal Room 4B by `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` § 3, so those edges cannot precede room discovery. The Rook proof chain: three nodes award Rook points to a maximum of 3 against a public-accusation threshold of 4. Neither is created by this decision; both become undeniable once edges exist.
- Five clues in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § 8 have no granting node: `CLUE_ROOK_KRELL_CONTACT`, `CLUE_ROOK_LENA_BULLETIN_FALSE`, `CLUE_REED_NAMES_ROOK_LINK`, `CLUE_MINA_AUTHENTICATES_REPORT`, `CLUE_EVIDENCE_ROOM_PHOTO_PATH`. C7 exposes them as orphans requiring a node or a `DEFINITION_ONLY` status.
- The 21:45 Nadia ferry-infrastructure failsafe in `ARC_170` has no node. It surfaces here as a missing edge and in C8 as an unimplemented backbone element.
- Edges crossing a split boundary cannot be timing-validated while `LOGIC/04_TIME_COST_MATRIX.md` § 3 and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4 disagree about leftover time and no maximum window duration is declared. Gate `V8` is `DEFERRED` for this reason.

### 7.6 Validation

Gates `V3`, `V5` after C7. `V8` is recorded as `DEFERRED`.

---

## 8. Decision 8 — Identifier namespaces

Presented before Decision 4 because the rename in P3 precedes the variable work in P4.

### 8.1 Canonical scheme

Mnemonic uppercase, full-word prefix, underscore separators. Identifiers are frozen at creation and survive display-name changes. A key may become a historical misnomer if a character is renamed; that is accepted and needs no engine amendment.

### 8.2 Rename scope

**Only identifiers with a demonstrated collision, ambiguity, alias or inconsistent scheme are renamed.** Three families qualify.

| Family | From | To | Reason | Count |
|---|---|---|---|---:|
| Clues | `C_*` | `CLUE_*` | Inconsistent scheme against every other entity prefix; single-letter prefix is unsafe for anchored search | 64 distinct |
| Conclusions | `D_*` | `CON_*` | Two live namespaces for one concept, used in different documents | 13 |
| Backbone | `EVT_nnn` in `05` | `ARC_nnn` | Shared stem with playable nodes; eight stems carry different meanings in each file | 19 |

**Explicitly not renamed in this revision:**

- All state variables keep their current names. `P_*`, `T_*`, `A_*`, `CLOCK`, `*_STATE`, `P1_*`, `P2_*`, `SHARED_KNOWLEDGE_SET` and the ending variables have no demonstrated collision. `P_STAGED` and `P1_LOCATION` are distinguishable under anchored search. A blanket `VAR_*` migration was considered and rejected as churn without a defect behind it.
- `NPC-01`, `LOC-01`, `CON-01`, `END-01`, `RH-01` and `CLU-01` are display ordinals within numbered document sections, not declared identifiers, and are left alone. The `CLU-0n` references inside `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` § 3 are replaced by `CLUE_*` references in C5, when that section is reduced and its counting moves to the logic layer, not in C3.
- `DEC_` and `CHK_` are not reserved. No such records exist.
- No engine file is edited.

### 8.3 The `D_*` to `CON_*` merge is 1:1

Eight `D_*` identifiers have an exact `CON_*` twin and merge cleanly: `STAGED_DISAPPEARANCE`, `HARBOR_DESTINATION`, `SIGNAL_4B`, `LENA_PROTECTING`, `REED_PRESENT`, `MEDICAL_EMERGENCY`, `DECOY_KEY`, `WINDOW_CODE`.

Five have no twin and become `CON_*` identifiers that the entity key table did not previously register: `CON_REED_CAUSED_CONFRONTATION`, `CON_MARCUS_LEAK_PARTIAL`, `CON_MARCUS_LEAK_PROVABLE`, `CON_ROOK_OPERATIONALLY_COMPROMISED`, `CON_ROOK_PUBLICLY_PROVABLE`. Registering them is documentation completion, not conceptual splitting: they already exist in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` under the `D_` prefix with their thresholds intact. No threshold, tier or meaning changes in C3.

Two existing `CON_*` identifiers have no `D_*` twin and are umbrella terms superseded by the tiered pair: `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED`. **They survive C3 unchanged**, and receive a mechanically derived status under § 8.7 rather than a judged one. Retiring or redefining them is semantic and is deferred to ratification § 14.9, which is required by C5.

The conclusion namespace after C3 therefore holds 15 identifiers, two of which await a ratification decision that C5 needs and C3 does not.

### 8.4 Prefix registry

Added to `LOGIC/00_ENTITY_KEY_TABLE.md` § "Purpose" in C1. Adventure-local, so no engine edit and no reverse-dependency question.

| Prefix | Entity | Owner |
|---|---|---|
| `NPC_` | Character | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `LOC_` | Location | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `ITEM_` | Item or evidence object | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `CLUE_` | Clue | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| `CON_` | Conclusion | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `FACT_` | NPC-knowledge fact | `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` |
| `ARC_` | Backbone arc | `LOGIC/05_CORE_EVENT_GRAPH.md` |
| `EVT_` | Playable or off-screen event node | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| `END_` | Ending family | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |
| `CLK_` | Clock-threshold trigger | `LOGIC/01_WORLD_STATE_VARIABLES.md` § 1 |
| `TR_` | State-machine transition | `LOGIC/11_LOCATION_STATE_MACHINE.md` |
| `EVAL_` | Gate evaluator | `LOGIC/07_EVIDENCE_VALIDATION.md`, `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |

`CLK_`, `TR_` and `EVAL_` are not cosmetic additions. Gate `V4` requires every writer and reader to resolve to a declared node, transition, initialization source or evaluator, and clock thresholds, location transitions and conclusion gates are currently anonymous prose. They are declared in C1 and populated in C4 and C5.

### 8.5 File scope

C3 edits only files that contain an affected identifier. The occurrence manifest produced in P2 is authoritative. The expected set, to be confirmed by that manifest rather than assumed:

| Family | Expected files |
|---|---|
| `C_*` → `CLUE_*` | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| `D_*` → `CON_*` | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`, `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |
| Backbone `EVT_*` → `ARC_*` | `LOGIC/05_CORE_EVENT_GRAPH.md`, `LOGIC/00_ENTITY_KEY_TABLE.md` § "Event key ranges" |

If the manifest finds occurrences outside this set, the manifest wins and this table is corrected before C3.

### 8.6 Execution method

Longest-identifier-first, anchored on word boundaries, each replacement confirmed against the manifest rather than applied as free-text substitution. `C_` is the dangerous case: it is short and appears inside ordinary words.

The rename is executed once, in C3, and is revertible in isolation.

### 8.7 Identifier status declaration

Gate `V2` requires every declared identifier to carry exactly one status from `ACTIVE`, `DEFINITION_ONLY`, `RESERVED` and `DEPRECATED`. **C3 assigns these statuses.** The assignment is mechanical, so it introduces no judgement into a behaviour-neutral commit.

**Derivation rule.** Status is computed from the occurrence manifest produced in P2, which gains a reference-count column for this purpose. No other input is used.

| Manifest result | Status |
|---|---|
| Referenced at least once outside its own declaring row | `ACTIVE` |
| Declared but never referenced | `DEFINITION_ONLY` |

`RESERVED` is not assigned in C3, because no identifier is reserved in this revision. `DEPRECATED` is not assigned in C3, because deprecation is a semantic judgement; the only candidates are `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` and their disposition is ratification § 14.9, required by C5.

**Where statuses are recorded.** All four documents are already in C3's file scope, so C3 gains no new file.

| Family | Recorded in |
|---|---|
| `NPC_`, `LOC_`, `ITEM_`, `CON_` | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `CLUE_` | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| `ARC_` | `LOGIC/05_CORE_EVENT_GRAPH.md` |
| `END_` | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |

**Coverage.** Statuses are declared as each family's owning document is edited: the four families above in C3; `FACT_` in C4; variables and `CLK_`, `TR_`, `EVAL_` in C4 and C5; `EVT_` in C7. `V2` is therefore evaluated over the migrated families after each commit, and over every family at P10. Full-coverage `V2` is a P10 requirement, not a C3 one.

### 8.8 Side effects

- Identifiers in external drafts and in-flight notes go stale in one commit. This is the cost of the single-pass rule and is preferable to a half-migrated repository.
- `LOGIC/00_ENTITY_KEY_TABLE.md` § "Conclusions" gains five rows in C3 to register identifiers that already exist under `D_`.
- `LOGIC/00_ENTITY_KEY_TABLE.md` § "Event key ranges" describes one numeric space and must be restated for two namespaces.
- `LOGIC/05_CORE_EVENT_GRAPH.md` § `ARC_320` holds the only working cross-reference into `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md`. Verify it still resolves after the prefix change.
- The ambiguous inline basename reference to `06_ENDING_FRAMEWORK.md` in `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 14 reads as if it points inside `LOGIC/`, where a different file occupies that number. Disambiguate in C7, when that section is rewritten, not in C3.
- Status derivation depends entirely on the P2 manifest. If the manifest is incomplete, statuses are wrong in a way that looks correct. The manifest is therefore a hard prerequisite of C3, not a convenience.

### 8.9 Validation

Gates `V1`, `V2` after C3, with `V2` scoped per § 8.7. Additionally: a diff review confirming C3 changed no threshold, no variable, no edge and no prose meaning.

---

## 9. Decision 4 — State variable system

### 9.1 Objective

Every variable has at least one writer and at least one reader, or it is removed. Every state machine has exactly one declared variable.

### 9.2 Initialization is not a writer

**An initialization source does not satisfy the writer requirement.** A variable whose only mutation is its initial assignment is a constant, not state, and must be removed or reclassified.

Initialization is recorded in its own column as `INIT`. Gate `V4` requires at least one writer that is not `INIT`.

### 9.3 Phase split

Non-progress variables are cleaned up and wired in C4. Progress variables are handled in C5, because their only readers are the conclusion evaluators created by Decision 6. Wiring them in C4 would fail `V4` by construction.

### 9.4 Complete variable register

Every current and proposed variable appears below. Dispositions are `KEEP`, `REMOVE`, `REPLACE`, `SPLIT`, `CREATE`. Writers and readers are identifiers, never prose.

#### 9.4.1 Global clock

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `CLOCK` | minutes, 20:00 onward | `20:00` | `INIT` | all `EVT_*` time costs | all `CLK_*`, all node availability windows, `EVAL_ENDING` | Global clock | KEEP |

`CLK_*` triggers declared in C1 and populated in C4: `CLK_2035`, `CLK_2130`, `CLK_2200`, `CLK_2205`, `CLK_2215`, `CLK_2230`, `CLK_2245`, `CLK_2300`, `CLK_2320`, `CLK_2330`, `CLK_2340`, `CLK_0000`, `CLK_0020`, `CLK_0100`, `CLK_0115`, `CLK_0120`, `CLK_0145`, `CLK_0200`.

#### 9.4.2 Progress points — all become derived quantities in C5

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `P_STAGED` | derived | — | — | `GRANT_CLUE` over group STAGED | `EVAL_CON_STAGED_DISAPPEARANCE` | — | REPLACE → derived |
| `P_HARBOR` | derived | — | — | `GRANT_CLUE` over group HARBOR | `EVAL_CON_HARBOR_DESTINATION` | — | REPLACE → derived |
| `P_ROOM_4B` | derived | — | — | `GRANT_CLUE` over group ROOM | `EVAL_CON_SIGNAL_4B` | — | REPLACE → derived |
| `P_ROOK` | derived | — | — | `GRANT_CLUE` over group ROOK | `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED`, `EVAL_CON_ROOK_PUBLICLY_PROVABLE` | — | REPLACE → derived |
| `P_MARCUS` | derived | — | — | `GRANT_CLUE` over group MARCUS | `EVAL_CON_MARCUS_LEAK_PARTIAL`, `EVAL_CON_MARCUS_LEAK_PROVABLE` | — | REPLACE → derived |
| `P_REED` | derived | — | — | `GRANT_CLUE` over group REED | `EVAL_CON_REED_PRESENT`, `EVAL_CON_REED_CAUSED_CONFRONTATION` | — | REPLACE → derived |
| `P_MEDICAL` | derived | — | — | `GRANT_CLUE` over group MEDICAL | `EVAL_CON_MEDICAL_EMERGENCY` | — | REPLACE → derived |
| `P_CODE` | derived | — | — | `GRANT_CLUE` over group CODE | `EVAL_CON_WINDOW_CODE` | — | REPLACE → derived |
| `P_LENA_PROTECTING` | derived | — | — | `GRANT_CLUE` over group LENA | `EVAL_CON_LENA_PROTECTING` | — | REPLACE → derived (never declared) |
| `P_DECOY` | derived | — | — | `GRANT_CLUE` over group DECOY | `EVAL_CON_DECOY_KEY` | — | REPLACE → derived (never declared) |
| *(new)* passphrase total | derived | — | — | `GRANT_CLUE` over group PASSPHRASE | `EVAL_CON_PASSPHRASE_ACCESS` | — | derived, created in C6 |

Eleven derived totals replace eight declared variables and two undeclared pseudo-variables. **No new stored point variable is created**, because under § 10 a total is computed from the held clue set and is not independently mutable.

#### 9.4.3 Trust

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `T_NADIA` | −2…+2 | `0` | `INIT` | `EVT_121`, `EVT_211` | `EVAL_NADIA_DISCLOSURE`, `EVAL_ENDING` | Nadia trust | KEEP |
| `T_MINA` | −2…+2 | `0` | `INIT` | `EVT_111`, `EVT_220` | `EVT_112`, `EVT_220`, `EVAL_RESCUE_CONTROL` | Mina trust | KEEP |
| `T_MARCUS` | −2…+2 | `−1` | `INIT` | `EVT_240` | `EVAL_MARCUS_DISCLOSURE` | Marcus trust | KEEP |
| `T_LENA` | −2…+2 | `−1` | `INIT` | none | none | — | REMOVE |
| `T_IRIS` | −2…+2 | `−1` | `INIT` | none | none | — | REMOVE |
| `T_REED` | −2…+2 | `−2` | `INIT` | none | none | — | REMOVE |

The three removals are safe because `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` §§ 4, 5 and 7 already gate Lena, Iris and Reed on evidence and leverage. C4 rewrites the § 4 phrase "pressured without trust" in evidence terms in the same commit.

#### 9.4.4 Antagonist awareness

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `A_ROOK_PLAYERS` | 0–4 | `0` | `INIT` | `EVT_111`, `EVT_112`, `EVT_221`, `EVT_223` | `TR_ANNEX_A_TO_B`, `TR_ANNEX_B_TO_C`, `TR_APT_A_TO_B`, `TR_DEVICE_SEIZED` | Rook awareness of players | KEEP |
| `A_ROOK_TERMINAL` | 0–3 | `1` | `INIT` | `EVT_803` | `TR_TERMINAL_HOSTILE_ROOK` | Rook terminal confidence | KEEP |
| `A_PUBLIC` | 0–3 | `0` | `INIT` | `EVT_440` | `EVAL_ENDING`, `EVAL_RESCUE_CONTROL` | Public awareness | KEEP |
| `A_KRELL_TERMINAL` | 0–3 | `2` | `INIT` | none | none | — | REMOVE |
| `A_REED_ROOM` | 0–3 | `0` | `INIT` | none | none | — | REMOVE |

`A_REED_ROOM` has no writer, and authoring one means inventing a scene in which Reed learns the room — a design act outside the accepted decisions. The narrative fact it was standing in for is already fixed prose in `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 ("Reed searches wrong upper rooms first because he lacks exact room number") and survives the removal unchanged.

The four off-screen resolution outcomes in `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 receive identifiers in C4, using the unallocated `EVT_8xx` range: `EVT_801` Reed reaches terminal first, `EVT_802` Rook reaches terminal first, `EVT_803` Reed and Rook meet, `EVT_804` Marcus meets the intermediary. This is required because `A_ROOK_TERMINAL`'s only writer lives there and `V4` forbids prose writers. `engine/03_ARCHITECTURE.md` § "3.17 Off-screen event architecture" already requires these to be events.

#### 9.4.5 Elias medical state

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `ELIAS_STATE` | 7-value enum | `CRITICAL_RESPONSIVE` | `INIT` | `CLK_2340`, `CLK_0100`, `CLK_0115`, `EVT_330`, `EVT_400` | `EVT_331`, `EVT_400`, `EVAL_ENDING` | Elias medical | KEEP |
| `ELIAS_SURVIVAL` | — | — | — | none | `EVAL_ENDING` | — | REMOVE — derived from `ELIAS_STATE` |

C4 rewrites `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "2. Medical outcome" to read `ELIAS_STATE` instead of its three prose categories. The mapping from three categories to seven enum values must be exhaustive or endings shift.

#### 9.4.6 Location state machines

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `APT_STATE` | 4-value enum | `SEALED_ACCESSIBLE_WITH_MINA` | `INIT` | `TR_APT_A_TO_B`, `TR_APT_B_TO_C`, `TR_APT_C_TO_D` | `EVT_111`, `EVT_112`, `EVT_113` | Elias apartment | KEEP |
| `NEWS_STATE` | 4-value enum | `OPEN_SUPERVISED` | `INIT` | `CLK_2035`, `CLK_2320`, `CLK_0000` | `EVT_121`, `EVT_122`, `EVT_123`, `EVT_240`, `EVT_430` | Newsroom | KEEP |
| `REED_OFFICE_STATE` | 4-value enum | `EMPTY_INTACT` | `INIT` | `CLK_2130`, `CLK_2205`, `CLK_2300` | `EVT_242` | Reed office | KEEP |
| `ROOM_4B_STATE` | 6-value enum | `HIDDEN_STABLE` | `INIT` | `EVT_330`, `EVT_400`, `EVT_420` | `EVAL_ENDING` | Signal Room 4B | KEEP |
| `TERMINAL_STATE` | — | — | — | — | — | — | SPLIT into the three below |
| `TERMINAL_WEATHER` | `DRY`/`SURGE`/`DRAINAGE_CLOSED` | `DRY` | `INIT` | `CLK_2245`, `CLK_2330` | `EVT_312` | Terminal weather | CREATE |
| `TERMINAL_HOSTILE` | `NONE`/`REED`/`ROOK_TEAM`/`REED_AND_ROOK` | `NONE` | `INIT` | `CLK_0020`, `TR_TERMINAL_HOSTILE_ROOK` | `EVT_314`, `EVT_420` | Terminal hostile presence | CREATE |
| `TERMINAL_ROUTES_KNOWN` | subset of 5 route tokens | empty | `INIT` | `EVT_210`, `EVT_212`, `EVT_311`, `EVT_313` | `EVT_310`–`EVT_314` | Terminal known routes | CREATE |
| `CAFE_STATE` | 3-value enum | `OPEN_FULL_RECORDS` | `INIT` | `CLK_2200`, `CLK_2230` | `EVT_211` | Café Orpheus | CREATE |
| `ANNEX_STATE` | 4-value enum | `NORMAL_ACCESS` | `INIT` | `TR_ANNEX_A_TO_B`, `TR_ANNEX_B_TO_C`, `TR_ANNEX_TO_D` | `EVT_220`, `EVT_221`, `EVT_222`, `EVT_223` | Police annex | CREATE |
| `IRIS_WORK_STATE` | 3-value enum | `SHIFT_ACTIVE` | `INIT` | `CLK_2200`, `TR_IRISWORK_SEIZED` | `EVT_230` | Iris workplace | CREATE |
| `ARCHIVE_STATE` | 3-value enum | `OPEN_PUBLIC` | `INIT` | `CLK_2320`, `TR_ARCHIVE_EMERGENCY` | `EVT_210` | Harbor archive | CREATE |

`TERMINAL_STATE` is split because `LOGIC/01_WORLD_STATE_VARIABLES.md` § 7 describes it as combining three dimensions and `LOGIC/11_LOCATION_STATE_MACHINE.md` § 9 confirms three independent ones. Three machines require three variables.

`ARCHIVE_STATE` uses `CLK_2320` because `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § `EVT_210` is the only place a closing time appears ("before 23:20 normal access; later emergency access"). `LOGIC/11_LOCATION_STATE_MACHINE.md` § 8 declares no times and `DO_NOT_READ/04_LOCATION_DATABASE.md` § `LOC-09` has no time-changes section. C4 must record the trigger in the state-machine document, or the variable cannot be wired.

#### 9.4.7 Player synchronization

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `P1_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | `EVT_100`, `EVT_110`, every P1-eligible node with a Location | node entry conditions | Player 1 position | KEEP |
| `P2_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | `EVT_100`, `EVT_120`, every P2-eligible node with a Location | node entry conditions | Player 2 position | KEEP |
| `P1_AVAILABLE_AT` | time | `20:00` | `INIT` | every P1-eligible node with a time cost | `EVT_150`, `EVT_300` | Player 1 availability | KEEP |
| `P2_AVAILABLE_AT` | time | `20:00` | `INIT` | every P2-eligible node with a time cost | `EVT_150`, `EVT_300` | Player 2 availability | KEEP |
| `SHARED_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | `EVT_150`, `EVT_300`, joint-scene `GRANT_CLUE` | every `EVAL_CON_*` | Shared knowledge | KEEP |
| `P1_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | `GRANT_CLUE` at P1-eligible nodes | `EVT_150`, `EVT_300` | Player 1 private knowledge | KEEP |
| `P2_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | `GRANT_CLUE` at P2-eligible nodes | `EVT_150`, `EVT_300` | Player 2 private knowledge | KEEP |
| `REGROUP_REQUIRED` | boolean | `false` | `INIT` | none | none | — | REMOVE |

The three knowledge sets are wired in C5 alongside `GRANT_CLUE`, not C4, because their writers are the clue-grant operation.

#### 9.4.8 Ending variables

| Identifier | Domain | Initial | Init source | Writers | Readers | State machine | Disposition |
|---|---|---|---|---|---|---|---|
| `FULL_LEDGER_TRANSFERRED` | boolean | `false` | `INIT` | `EVT_430` | `EVAL_ENDING` | Transfer outcome | KEEP |
| `ROOK_EXPOSED_PRIVATE` | boolean | `false` | `INIT` | `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED` | `EVT_400`, `EVAL_ENDING` | Rook exposure | KEEP |
| `ROOK_EXPOSED_PUBLIC` | boolean | `false` | `INIT` | `EVT_440` | `EVAL_ENDING` | Rook exposure | KEEP |
| `KRELL_VALE_EXPOSED` | boolean | `false` | `INIT` | `EVT_430`, `EVT_440` | `EVAL_ENDING` | Conspiracy exposure | KEEP |
| `TRUSTED_RESCUE_CONTROL` | boolean | `false` | `INIT` | `EVT_400` | `EVAL_ENDING` | Rescue control | KEEP |
| `PUBLIC_ACCUSATION_TARGET` | `NPC_*` or none | none | `INIT` | `EVT_440` | `EVAL_ENDING` | Accusation | KEEP |
| `PUBLIC_ACCUSATION_SUPPORT` | 0…n | `0` | `INIT` | `EVT_440` | `EVAL_ENDING` | Accusation | KEEP |
| `MARCUS_CONFESSED` | boolean | `false` | `INIT` | `EVT_241` | `EVAL_ENDING` | Marcus outcome | KEEP |
| `REED_COOPERATED` | boolean | `false` | `INIT` | `EVT_243` | `EVAL_ENDING` | Reed outcome | KEEP |
| `LENA_STATUS` | enum | `concealed` | `INIT` | `EVT_331`, `EVT_420` | `EVAL_ENDING` | Lena outcome | KEEP |
| `IRIS_STATUS` | enum | `concealed` | `INIT` | `EVT_331`, `EVT_400` | `EVAL_ENDING` | Iris outcome | KEEP |
| `LEDGER_PRIMARY_STATUS` | — | — | — | none | `EVAL_ENDING` | — | REMOVE — duplicates the item state of `ITEM_LEDGER_PRIMARY` |

#### 9.4.9 Aliases outside the owning document

| Identifier | Location | Disposition | Replaced by |
|---|---|---|---|
| `NADIA_TRUST` | `DO_NOT_READ/03_CHARACTER_DATABASE.md` § `NPC-02` | REPLACE | `T_NADIA` |
| `ROOK_EXPOSED` | `DO_NOT_READ/06_ENDING_FRAMEWORK.md` § "Ending variables" | REPLACE | `ROOK_EXPOSED_PRIVATE` + `ROOK_EXPOSED_PUBLIC` |
| `RESCUE_CONTROLLED_BY_TRUSTED_PARTY` | same | REPLACE | `TRUSTED_RESCUE_CONTROL` |
| `PUBLIC_ACCUSATION_CORRECT` | same | REPLACE | `PUBLIC_ACCUSATION_TARGET` + `PUBLIC_ACCUSATION_SUPPORT` |

All four are semantic replacements, not spelling changes, because three of them map one name onto a pair. They land in C4, never in C3.

### 9.5 Register arithmetic

| Step | Count |
|---|---:|
| Declared variables at baseline | 47 |
| − `REMOVE` (`T_LENA`, `T_IRIS`, `T_REED`, `A_KRELL_TERMINAL`, `A_REED_ROOM`, `REGROUP_REQUIRED`, `ELIAS_SURVIVAL`, `LEDGER_PRIMARY_STATUS`) | −8 → 39 |
| − `REPLACE` to derived (eight `P_*`) | −8 → 31 |
| − `SPLIT` parent (`TERMINAL_STATE`) | −1 → 30 |
| + `CREATE` (3 terminal dimensions, 4 location machines) | +7 → **37** |

**37 stored variables, each with a non-`INIT` writer and at least one reader, plus 11 derived totals.**

### 9.6 Affected files

`LOGIC/01_WORLD_STATE_VARIABLES.md` (register, all sections), `LOGIC/11_LOCATION_STATE_MACHINE.md` (transitions given `TR_*` identifiers; four machines bound to variables; archive trigger recorded), `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (writes declared per node), `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` (`EVT_8xx` identifiers for four off-screen outcomes), `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` (trust removals rewritten as evidence gates; `FACT_` statuses), `LOGIC/14_ENDING_TRIGGER_MATRIX.md` (medical outcome reads `ELIAS_STATE`), `LOGIC/02_ITEM_STATE_MATRIX.md` (item state as the source replacing `LEDGER_PRIMARY_STATUS`), `DO_NOT_READ/03_CHARACTER_DATABASE.md` (alias replaced), `DO_NOT_READ/06_ENDING_FRAMEWORK.md` (alias list replaced by a marked non-authoritative pointer). All in C4.

### 9.7 Side effects

- Removing three trust variables converts Lena, Iris and Reed from graduated relationship tracking to binary evidence gates. That is what the knowledge matrix already specifies, but it is a design consequence.
- Rewriting the medical outcome to read an enum changes how endings are computed. The three-to-seven mapping must be exhaustive.
- `EVT_241` and `EVT_314` declare no time cost, so they cannot write the availability variables. C4 must author costs for both.
- Giving the four off-screen outcomes `EVT_8xx` identifiers makes them nodes for the first time. They are not player-reachable and must be excluded from `V5` reachability, or marked with an off-screen flag so the gate does not report them unreachable.

### 9.8 Validation

Gates `V2`, `V4` after C4.

---

## 10. Decision 6 — Progress model

### 10.1 Canonical progression

```text
Node outcome
     ↓
  Points
     ↓
  Clues
     ↓
Conclusions
```

### 10.2 The single atomic operation

**`GRANT_CLUE(clue_identifier)` is the only operation a node may perform on investigative progress.**

- A clue carries its own point value and class tags. There is no separate point award.
- **Point totals are derived from the held clue set and are not independently mutable state.** No document may store, increment or decrement a point total.
- **Clue acquisition is idempotent.** `GRANT_CLUE` on an already-held clue is a no-op with respect to points and classes. A clue reachable through several routes awards its value exactly once.
- `GRANT_CLUE` writes to the acting player's private knowledge set. A joint-scene node writes to `SHARED_KNOWLEDGE_SET`. Regroup nodes `EVT_150` and `EVT_300` move clues from private sets into the shared set.
- A conclusion evaluator reads the union of `SHARED_KNOWLEDGE_SET` and the evaluating player's private set.

This invariant does the work of four separate fixes: it eliminates the `P_ROOK +1 procedural` syntax that mixes an increment with an untracked class label; it makes every total auditable back to clue identifiers; it removes the need for a class-tracking variable, since diversity is read from the held set; and it makes duplicate awarding structurally impossible rather than a rule someone must remember.

### 10.3 Maxima are computed, not declared

The maximum of a derived total equals the sum of the point values of all clues in its group. It is recorded in the register as a computed figure. Any mismatch between a declared threshold and the computed maximum is a validation failure rather than a silent inconsistency.

This retires the hand-maintained ranges in `LOGIC/01_WORLD_STATE_VARIABLES.md` § 2, at least three of which the node graph already appears to exceed.

### 10.4 Affected files

| File | Section | Edit | Commit |
|---|---|---|---|
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | § 1 and all groups | Restate as the clue register: identifier, class tags, point value, granting nodes, conclusion group, status | C5 |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § "2. Conclusion thresholds" | Restate every threshold as point sum plus class diversity over the held clue set; supply the missing thresholds for room identification, code completion and Reed presence; declare `EVAL_*` identifiers | C5 |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | § 2 | Replace the eight stored point variables with eleven derived totals and their computed maxima | C5 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | every **State changes** block | Replace point awards with `GRANT_CLUE(...)` | C5 |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | § 3 | Reduce to conclusion-level narrative rationale; replace `CLU-0n` references with `CLUE_*`; move all counting to the logic layer | C5 |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | §§ 4, 5 | Confirm accusation gates read conclusions, never raw totals | C5 |

### 10.5 Side effects

- Computing maxima will change reachable ceilings and may invalidate thresholds in either direction. The Rook public threshold of 4 against three granting nodes is the known case.
- Assigning a point value to 65 clues is a set of new design decisions that directly control difficulty. Ratification § 14.5.
- `LOGIC/07_EVIDENCE_VALIDATION.md` § 2 currently mixes point gates and category gates. Unifying them changes at least the room-identification gate from a category rule to a numeric one, altering when it unlocks.
- The medical conclusion is the only gate consistent across both systems today. Verify it survives unchanged, so the conversion can be demonstrated behaviour-preserving in at least one case.
- Idempotence interacts with multi-route clues. `CLUE_PHOTO_WINDOW_MARKS` belongs to two conclusion groups; the register must make clear that it is one clue contributing to two groups, not two clues.

### 10.6 Validation

Gates `V4`, `V7`, `V9` after C5.

---

## 11. Decision 7 — Clue classes

### 11.1 Canonical vocabulary and its single owner

Six classes, owned by **`LOGIC/07_EVIDENCE_VALIDATION.md` § "1. Proof classes"**, which is already correct and complete:

`PHYSICAL`, `DIGITAL`, `TESTIMONIAL`, `PROCEDURAL`, `CONTEXTUAL`, `BEHAVIOURAL`

**No engine requirement is added and the engine version is not bumped.** Defining the vocabulary once in the adventure satisfies the accepted decision. Promoting it to the engine would edit `engine/00_ENGINE_SPECIFICATION_2.0.md`, force the duplicate-root-file question, and bump `engine_spec_version` — all churn the decision does not require.

`DO_NOT_READ/05_CLUE_ARCHITECTURE.md` § "2. Clue classes" currently declares five, omitting `DIGITAL` and folding "recording" into `PHYSICAL`. It is reduced to a marked non-authoritative pointer, and its `PHYSICAL` definition drops "recording". This lands in C1, as a canonical-ownership change.

**C1 declares the vocabulary only.** The class-diversity counting rule is a separate item and lands in C5; see § 11.2.

### 11.2 The class-diversity counting rule lands in C5

How a multi-class clue counts toward diversity determines whether a single clue can satisfy a three-class threshold alone. It is therefore a threshold rule, not a vocabulary rule, and it belongs to the commit that restates thresholds.

The rule is written into `LOGIC/07_EVIDENCE_VALIDATION.md` § 1 in **C5**, alongside the threshold restatement in § 2. Ratification § 14.7 is required by C5 and does not gate C1.

Multi-class clues are permitted, and the existing `procedural/digital` and `testimonial/procedural` tags are retained.

### 11.3 Tagging work

All 64 baseline clues plus the one new passphrase clue carry at least one class. Twenty-one are tagged today, across §§ 2, 3 and 8. Forty-three are untagged while §§ 5, 7 and 8 already state class-diversity thresholds that cannot be evaluated without them.

### 11.4 Affected files

| File | Section | Edit | Commit |
|---|---|---|---|
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § 1 | Declare the six-class vocabulary as canonical | C1 |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | § 2 | Reduce to a marked non-authoritative pointer; drop "recording" from `PHYSICAL` | C1 |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § 1 | Add the class-diversity counting rule, per § 14.7 | C5 |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | all groups | Tag 43 untagged clues | C5 |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | **State changes** blocks | Remove ad-hoc class labels with the point awards | C5 |

### 11.5 Side effects

- Class assignment is a design act. A careless pass can silently make a three-class threshold unsatisfiable.
- Restoring `DIGITAL` moves some clues currently reasoned about as physical, which may reduce diversity in groups that relied on the five-class reading.
- Tagging and progress conversion share commit C5 because a clue's class and its point value are recorded in the same register row. Splitting them would leave the register half-populated between commits.
- `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` is edited twice, § 2 in C1 and § 3 in C5. The sections are disjoint, so the two edits do not conflict.

### 11.6 Validation

Gate `V7` after C5. C1 requires only `V10`, because no clue is tagged and no threshold is evaluated in C1.

---

## 12. Decision 5 — Core-to-investigation graph mapping

### 12.1 Deliverable

A new file, `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/16_EVENT_GRAPH_MAPPING.md`, in commit C8.

The core graph is retained as a backbone layer, not retired. `LOGIC/05_CORE_EVENT_GRAPH.md` § "Graph conventions" already frames itself that way and it holds the only cross-reference into `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md`. Folding it into `10` would discard the backbone view and lose the record of which backbone elements were never implemented.

### 12.2 Draft mapping

Ratification § 14.3 covers every row below High confidence.

| Backbone | Investigation nodes | Relationship | Confidence |
|---|---|---|---|
| `ARC_100` Nadia's briefing | `EVT_100` | 1:1 | High |
| `ARC_110` First split decision | Absorbed into the **Decision** block of `EVT_100`; realised by `EVT_110`, `EVT_120` | Absorbed | Medium |
| `ARC_120` Apartment cluster | `EVT_110`, `EVT_111`, `EVT_112`, `EVT_113`, `EVT_114`, `EVT_115` | Expanded 1:6 | High |
| `ARC_130` Newsroom cluster | `EVT_120`, `EVT_121`, `EVT_122`, `EVT_123` | Expanded 1:4 | High |
| `ARC_140` Café cluster | `EVT_211` | Relocated, opening block to midgame | Low — § 12.4 |
| `ARC_170` First synchronization gate | `EVT_150` | 1:1, renumbered | High |
| `ARC_200` Rook pressure | `EVT_223` | Partial | Medium |
| `ARC_210` Reed office opportunity | `EVT_242` | 1:1 | High |
| `ARC_220` Iris trail | `EVT_230`, `EVT_231`, `EVT_232` | Expanded 1:3 | High |
| `ARC_230` Marcus disclosure ladder | `EVT_240`, `EVT_241` | Expanded 1:2 | High |
| `ARC_240` Mina evidence preservation | `EVT_220`, partly `EVT_400` | Partial, split | Medium |
| `ARC_270` Second synchronization gate | `EVT_300` | 1:1, renumbered | High |
| `ARC_300` Terminal route selection | `EVT_310`–`EVT_314` | Expanded 1:5 | High |
| `ARC_320` Off-screen hostile convergence | `EVT_420`, `EVT_801`–`EVT_804` | Split across documents | Medium |
| `ARC_340` Signal Room discovery | `EVT_330`, `EVT_331` | Expanded 1:2, renumbered | High |
| `ARC_400` Trusted rescue validation | `EVT_400` | 1:1 | High |
| `ARC_420` Evidence transfer | `EVT_410`, `EVT_430` | Expanded 1:2 | High |
| `ARC_440` Final accusation | `EVT_440` | 1:1 | High |
| `ARC_900` Ending resolution | `EVT_900` plus eight terminal nodes | Expanded 1:9 | High |

Additions with no backbone origin: `EVT_210`, `EVT_212`, `EVT_221`, `EVT_222`, `EVT_243`.

Unimplemented backbone elements, recorded with a reason: the fixed no-later-than-22:10 trigger of `ARC_200`; the 21:45 Nadia ferry-infrastructure failsafe inside `ARC_170`.

### 12.3 Affected files

New `LOGIC/16_EVENT_GRAPH_MAPPING.md`; `LOGIC/05_CORE_EVENT_GRAPH.md` (purpose statement; the prefix change itself lands in C3); `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (back-reference per node). All in C8.

### 12.4 Side effects

- The `ARC_140` row records a semantic change, not a clean expansion. `DO_NOT_READ/02_MASTER_TIMELINE.md` § `### 20:05` assigns Café Orpheus to Player 2 as a starting lead; the investigation graph moves it to the midgame harbor branch. The mapping must not paper over this. Either the timeline changes or the node moves back.
- Formalising "unimplemented" turns previously invisible gaps into tracked debt the next revision must implement or delete. That is the intent.

### 12.5 Validation

Gate `V6` after C8.

---

## 13. Validation gates

Run after every commit, not only at P10. Each decision section names the subset that must pass before the next commit is authored.

| Gate | Check | Pass criterion |
|---|---|---|
| `V1` | Identifier resolution | Every identifier matches the prefix registry and resolves to exactly one register entry. |
| `V2` | Declaration status | Every declared identifier in a migrated family carries exactly one status: `ACTIVE`, `DEFINITION_ONLY`, `RESERVED` or `DEPRECATED`. Every `ACTIVE` identifier is referenced at least once. `DEFINITION_ONLY`, `RESERVED` and `DEPRECATED` identifiers may be unreferenced. No identifier is referenced without being declared. Family coverage follows § 8.7: the four families migrated in C3 after C3, additional families as their owning documents are edited, and every family at P10. |
| `V3` | Node declaration | Every node has exactly one `NODE_TYPE`. Every `TERMINAL` node has exactly one `TERMINAL_TYPE` from the approved set. Every `TERMINAL` node declares `Outgoing: None`. No `INTERMEDIATE` node declares a `TERMINAL_TYPE`. Every `INTERMEDIATE` node declares at least one valid target. |
| `V4` | Writer and reader resolution | Every variable has at least one writer that is not `INIT` and at least one reader. Every writer and reader resolves to a declared node (`EVT_*`), transition (`TR_*`, `CLK_*`), initialization source (`INIT`), or evaluator (`EVAL_*`). |
| `V5` | Reachability | Every `Outgoing` target exists. Every terminal node is reachable from `EVT_100` in at least one declared play mode. No player-facing node is unreachable in every mode. Off-screen `EVT_8xx` nodes are excluded. |
| `V6` | Backbone mapping | Every `ARC_*` maps to at least one `EVT_*` or carries an explicit unimplemented status with a reason. Every `EVT_*` maps to an `ARC_*` or carries an addition status. No identifier appears in both namespaces. |
| `V7` | Clue integrity | Every clue has at least one class from the single canonical set, a point value, and at least one granting node or a `DEFINITION_ONLY` status. Clue acquisition is idempotent: a clue reachable by several routes contributes its value exactly once, and no document stores a mutable point total. |
| `V8` | Time integrity | **DEFERRED.** Its blockers — the leftover-time conflict between `LOGIC/04_TIME_COST_MATRIX.md` § 3 and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, and the absence of declared maximum split-window durations — are out of scope for this revision. Recorded as deferred, not passed. Promoting it to a required gate requires moving those blockers into scope. |
| `V9` | Solvability | Every conclusion threshold is satisfiable from clues reachable without circularity, **and remains satisfiable after class assignment**. Every mandatory factor has at least two independent routes or an authored degraded outcome. Independent routes share no mandatory predecessor node. The passphrase has two routes, one obtainable before 01:00. |
| `V10` | Single source | Every fact has exactly one authoritative owner. Summaries and cross-references are permitted and must be explicitly marked non-authoritative. Ending triggers are owned by `14`; node identity and edges by `10`; narrative outcome by `06`; clue classes by `07` § 1. |
| `V11` | Ending-trigger precedence | The trigger conditions of the eight ending families are either provably mutually exclusive, or a deterministic priority order is declared in `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 1 and every reachable combination resolves to exactly one ending. |

---

## 14. Ratifications

Each item is required by a specific phase. Per § 3.2, an `OPEN` item blocks only the phase named in its **Required by** column and every phase after it. It does not block an earlier phase.

**Ratification map.** Item numbering is unchanged from v2.0 so that every cross-reference elsewhere in this document remains valid.

| § | Item | Required by | Status |
|---|---|---|---|
| 14.1 | `END_SILENT_TERMINAL` terminal type | P7 (C7) | OPEN |
| 14.2 | Split-branch terminator vocabulary | P7 (C7) | OPEN |
| 14.3 | Low and Medium confidence mapping rows | P8 (C8) | OPEN |
| 14.4 | Passphrase as a fifth solution chain | P6 (C6) | OPEN |
| 14.5 | Point values | P5 (C5) | OPEN |
| 14.6 | Duplicate-root-file policy | none in this revision | DEFERRABLE |
| 14.7 | Multi-class clue diversity behaviour | P5 (C5) | OPEN |
| 14.8 | Ending-trigger precedence | P7 (C7) | OPEN |
| 14.9 | Umbrella conclusion identifiers | P5 (C5) | OPEN |
| 14.10 | Route A classification | — | RESOLVED |

**Phases clear to enter: P0, P1, P2, P3, P4.** The first phase with an `OPEN` requirement is P5.

### 14.1 `END_SILENT_TERMINAL` terminal type

`CHARACTER_DEATH` or `TIME_EXPIRED`. Turns on whether `CHARACTER_DEATH` covers a non-player character; Elias is an NPC in every configuration. `engine/03_ARCHITECTURE.md` § 3.18 calls the list "Recommended", so extension is permitted, but adding a type is an engine change and would reopen § 1.2.

### 14.2 Split-branch terminator vocabulary

Whether `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, `TERMINAL_OUTCOME` are in scope for C7. Inferred from an existing engine MUST, not from the literal accepted decision.

### 14.3 Low and Medium confidence mapping rows

`ARC_110`, `ARC_140`, `ARC_200`, `ARC_240`, `ARC_320`. The café relocation is the one with a content consequence.

### 14.4 Passphrase as a fifth solution chain

Whether `DO_NOT_READ/00_CASE_OVERVIEW.md` § "Fair solution" gains a chain or the passphrase remains a sub-step of Chain B. That section is a non-authoritative summary under `V10`, so this affects only C6 and not the canonical facts written in C2.

### 14.5 Point values

All 64 baseline clues and the one new passphrase clue. These are design decisions that set difficulty, not transcriptions.

### 14.6 Duplicate-root-file policy

Deduplicate, or mark the eight byte-identical root copies non-authoritative in place.

**Required by no phase in this revision.** No commit in C1–C9 edits any of the eight root copies or their canonical twins, because this revision edits no engine file. The decision is precautionary and may be carried forward, provided the deferral is recorded in C0.

### 14.7 Multi-class clue diversity behaviour

Whether a clue tagged `procedural/digital` contributes one class or two toward a diversity threshold. Determines whether a single clue can satisfy a three-class gate alone. Required by C5, where the counting rule is written and thresholds are restated. It does not gate C1, which declares the vocabulary only.

### 14.8 Ending-trigger precedence

Mutual exclusivity or a declared priority order. Required by `V11` after C7.

### 14.9 Umbrella conclusion identifiers

Whether `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` survive alongside their tiered pairs, are marked `DEPRECATED`, or are retired.

Required by C5, where thresholds are restated. It does not gate C3: under § 8.7 both receive a mechanically derived status from the occurrence manifest, and `DEPRECATED` is not assignable in C3 at all.

### 14.10 Route A classification — RESOLVED

**Question.** Decision 1 requires "two independent acquisition routes". Route A unlocks a recovery workflow rather than acquiring the passphrase.

**Resolution.** The recovery-workflow mechanism was authorised by the accepted-decision authority, which enumerated it as one of three permitted answers when it required Route A's exact operation to be defined: the instructions may "directly reconstruct it", "unlock a recovery workflow", or "point to another existing source". Route A implements the second option as authorised. The residual question was terminology only, and § 5.1 now states the position precisely: two independent routes reach primary-archive access, one acquiring the passphrase and one bypassing it at a cost, with the passphrase remaining mandatory for full authentication.

**Effect.** No content changes. Required by no phase.

---

## 15. Out of scope

Recorded so the next scope decision starts from a complete picture.

- **Solo mode.** Required by `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` §§ 1 and 8 and by `PROTOTYPE_BRIEF.md`, implemented nowhere. `V5` is evaluated per declared mode because of this.
- **Split-window durations and the parallel-action conflict.** The reason `V8` is deferred.
- **Complexity budget overruns.** Location, clue and ending counts exceed the targets in `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 4. Those are design targets, not MUST rules, and C5 makes the clue count precise for the first time.
- **Two-player delivery model.** `engine/03_ARCHITECTURE.md` § 3.15 requires a declared model; none is declared.
- **Scene-mode declarations.** `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3 requires every scene to declare Joint, Split or Solo.
- **Engine chapter plan divergence.** `engine/README.md` reserves chapters 4 and 5 for content that does not exist.
- **All engine edits.** This revision touches no file under `engine/`. The prefix registry and the clue-class vocabulary are both adventure-local.
- **Stale version statements beyond this revision.** C9 corrects only what this revision changes.

---

## 16. C0 — Ratification record (P0)

Recorded at P0 under § 3.2. This section is the C0 ratification record.

### 16.1 Map published

The ratification map in § 14 is published with a **Required by** and a **Status** column for all ten items. It is the authoritative input to the § 3.2 phase gate.

### 16.2 Resolutions reached

| § | Item | Status | Record |
|---|---|---|---|
| 14.10 | Route A classification | RESOLVED | The recovery-workflow mechanism was authorised by the accepted-decision authority, which enumerated it as one of three permitted answers when it required Route A's exact operation to be defined. § 5.1 states the position precisely. No content change follows. Required by no phase. |
| 14.6 | Duplicate-root-file policy | DEFERRABLE — **deferral recorded** | No commit in C1–C9 edits any of the eight byte-identical root copies or their canonical twins, because this revision edits no engine file. The item is required by no phase in this revision and is carried forward. This entry satisfies the recording requirement in § 3.2 and § 14.6. |

### 16.3 Items remaining OPEN

| § | Item | Required by |
|---|---|---|
| 14.1 | `END_SILENT_TERMINAL` terminal type | P7 (C7) |
| 14.2 | Split-branch terminator vocabulary | P7 (C7) |
| 14.3 | Low and Medium confidence mapping rows | P8 (C8) |
| 14.4 | Passphrase as a fifth solution chain | P6 (C6) |
| 14.5 | Point values | P5 (C5) |
| 14.7 | Multi-class clue diversity behaviour | P5 (C5) |
| 14.8 | Ending-trigger precedence | P7 (C7) |
| 14.9 | Umbrella conclusion identifiers | P5 (C5) |

No `OPEN` item names P0, P1, P2, P3 or P4.

### 16.4 Phases clear to enter

**P0, P1, P2, P3, P4.** The first phase with an `OPEN` requirement is **P5**, blocked by § 14.5, § 14.7 and § 14.9.

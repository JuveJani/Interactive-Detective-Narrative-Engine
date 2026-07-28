---
title: Implementation Plan — Next Repository Revision
version: 1.0
status: Approved
depends_on:
  - docs/STYLE_GUIDE.md
  - engine/00_ENGINE_SPECIFICATION_2.0.md
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

This document is the authoritative implementation specification for the next repository revision. It converts eight accepted decisions into per-file edit instructions, a single global migration order, a side-effect register, and a validation gate.

This document does not implement anything. It contains no repository edits. Every instruction below is a specification for a future revision.

Where this document conflicts with an existing repository document, this document governs **only for the duration of the migration**. On completion, every rule stated here must exist in its owning source document, and this plan becomes a historical record. This follows `engine/03_ARCHITECTURE.md` § "3.10 Review Layer": "Reviews MUST NOT become hidden authoritative specifications. Accepted corrections MUST be incorporated into the responsible source document."

### 1.1 Target release

The next revision is **Prototype Alpha 0.2c**, not Alpha 0.3.

`adventures/The_Last_Witness/DO_NOT_READ/07_PROTOTYPE_BUILD_PLAN.md` § "Required before player-book compilation" reserves Alpha 0.3 for the narrative compiler pass. This revision performs no narrative compilation; it consolidates the logic layer delivered in Alpha 0.2b. Claiming 0.3 would misrepresent the build plan.

### 1.2 Schema version impact

Per `data_dictionary/SCHEMA_VERSIONING.md` § "3. Semantic Version Meaning", `MAJOR` changes may break existing adventure data.

| Field | Before | After | Reason |
|---|---|---|---|
| `engine_spec_version` | `2.0` | `2.1` | Decision 8 adds a normative prefix registry to `engine/03_ARCHITECTURE.md` § 3.14. Additive clarification, not a break. |
| `data_dictionary_version` | `0.3` | `0.3` | No schema records exist yet to change. |
| `adventure_schema_version` | `0.1` | `1.0` | Decision 8 renames every identifier in the adventure. Existing adventure data does not survive. |

These three fields are currently declared nowhere. Decision 8 introduces them as required frontmatter on the logic layer.

### 1.3 Defect classification

Each decision is classified using the vocabulary in `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § "9. Post-Playtest Review".

| Decision | Classification |
|---|---|
| 1 — Passphrase | `ADVENTURE_LOGIC_DEFECT` + `CONTENT_DEFECT` |
| 2 — `NODE_TYPE` | `ADVENTURE_LOGIC_DEFECT` |
| 3 — `Outgoing` | `ADVENTURE_LOGIC_DEFECT` |
| 4 — State variables | `ADVENTURE_LOGIC_DEFECT` |
| 5 — Graph mapping | `ADVENTURE_LOGIC_DEFECT` |
| 6 — Progress model | `ADVENTURE_LOGIC_DEFECT` |
| 7 — Clue classes | `ADVENTURE_LOGIC_DEFECT` |
| 8 — Namespaces | `ENGINE_RULE_DEFECT` + `ADVENTURE_LOGIC_DEFECT` |

No decision is classified `ENGINE_RULE_DEFECT` except Decision 8, because in every other case the engine rule is already correct and only the adventure fails to implement it.

---

## 2. Baseline inventory

All counts below were verified against the repository at commit `0923366cd3f1302a849f072dedc5b9be1d4e19a1`. They are the denominators for the validation gate in § 12.

| Quantity | Count | Source |
|---|---:|---|
| Nodes in the investigation graph | 40 | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| Nodes declaring an `Outgoing` block | 3 | `EVT_110`, `EVT_111`, `EVT_120` |
| Nodes declaring successors as "unlocks" inside **State changes** | 1 | `EVT_100_SHARED_BRIEFING` |
| Nodes declaring `NODE_TYPE` | 0 | — |
| Backbone entries in the core graph | 19 | `LOGIC/05_CORE_EVENT_GRAPH.md` |
| Distinct clue identifiers | 64 | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` (65 listings; `C_PHOTO_WINDOW_MARKS` appears in §§ 4 and 11) |
| Clue groups carrying class tags | 3 of 10 | §§ 2, 3, 8 only |
| Deduction identifiers (`D_*`) | 13 | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| Conclusion identifiers (`CON_*`) | 10 | `LOGIC/00_ENTITY_KEY_TABLE.md` § "Conclusions" |
| Declared state variables | 47 | `LOGIC/01_WORLD_STATE_VARIABLES.md` §§ 1–9 |
| Variables used but never declared | 2 | `P_LENA_PROTECTING`, `P_DECOY` |
| State machines with no declared variable | 4 | `LOGIC/11_LOCATION_STATE_MACHINE.md` §§ 4, 5, 7, 8 |
| Ending families | 8 | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § 6 |
| Ending families with a node identity | 0 | — |

The 13-to-10 deduction/conclusion relationship is not a discrepancy in count. Three conclusions each carry two strength tiers: `CON_REED_PRESENT` covers `D_REED_PRESENT` and `D_REED_CAUSED_CONFRONTATION`; `CON_MARCUS_LEAK` covers `D_MARCUS_LEAK_PARTIAL` and `D_MARCUS_LEAK_PROVABLE`; `CON_ROOK_COMPROMISED` covers `D_ROOK_OPERATIONALLY_COMPROMISED` and `D_ROOK_PUBLICLY_PROVABLE`. Seven single-tier conclusions plus three double-tier conclusions equals thirteen.

---

## 3. Decision 1 — The ledger passphrase

### 3.1 Objective

The passphrase remains a mandatory authentication factor. It gains at least two independent acquisition routes, and every document that gates on ledger access states the same three-factor requirement.

### 3.2 Canonical rule to be established

`adventures/The_Last_Witness/DO_NOT_READ/01_WORLD_BIBLE.md` § "4. The ledger" > "Access" already requires three factors: the hardware key, Elias's passphrase, and the six-digit recovery code. That requirement is correct and does not change. What changes is that the passphrase acquires declared sources, and the two transfer gates that currently omit it are corrected.

### 3.3 Route design and rejected candidates

Routes were selected only from actors the repository already places in a position to hold the fact. Rejected candidates are recorded so the decision is not silently revisited.

| Candidate | Verdict | Basis |
|---|---|---|
| Nadia — recovery instructions held with the upload | **Accept as Route A** | `04_LOCATION_DATABASE.md` § `LOC-02` clue 7 already lists "Recovery-code instructions"; `01_WORLD_BIBLE.md` § "4. The ledger" > "Copies" item 2 places the encrypted upload in her newsroom account; `EVT_123_NEWSROOM_RECORDS` already grants a code point for recovering upload instructions. |
| Elias — spoken fragment | **Accept as Route B** | `03_CHARACTER_DATABASE.md` § `NPC-01` > "Statements while conscious" already establishes a fragment mechanism from 21:15. |
| Signal Room 4B — physical mnemonic | **Reject as a counted route** | Co-located with the primary key. It would add no independence, exactly the flaw identified for the room-identifier chain. May be authored as an in-room confirmation that grants no independent point. |
| Lena | **Reject** | `03_CHARACTER_DATABASE.md` § `NPC-03` > "Knowledge": "She does not understand the full ledger or upload process." |
| Marcus | **Reject** | `01_WORLD_BIBLE.md` § "11. The newspaper betrayal": "Marcus does not know the exact hiding room or the ledger passphrase." |
| Reed's laptop | **Reject** | `01_WORLD_BIBLE.md` § "4. The ledger" > "Copies" item 3 makes the decoy a separate archive. A failed decoy decryption cannot expose the primary passphrase. |

Route A is pre-discovery, Player 2, newsroom, digital or procedural class. Route B is post-discovery, testimonial class, and is time-limited because `01_WORLD_STATE_VARIABLES.md` § "1. Global clock" places Elias at unresponsive from 01:00.

Route B being post-discovery is acceptable for this factor specifically, and only for this factor. The passphrase is required only once the primary key is in hand, and `01_WORLD_BIBLE.md` § "14. Immutable facts" fixes the primary key inside Signal Room 4B. A route that unlocks at room discovery is therefore not circular with respect to the thing it gates. This reasoning must be recorded in the clue register so a later audit does not mistake Route B for a circular source.

Because Route B expires at 01:00, the two routes alone do not satisfy `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § "5. Soft-Lock Prevention" in the late-arrival case. A third element is mandatory: an authored failure transformation, not a third route.

### 3.4 Failure transformation

Failing to obtain the passphrase must not deadlock. It must route to an outcome that already exists: `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "3. Evidence outcome" > "Partial official evidence". This satisfies the "degraded but still solvable outcome" clause of `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § "5. Soft-Lock Prevention" and preserves the distinction the ending framework already draws between rescue and exposure.

### 3.5 Affected files and exact edits

| File | Section | Edit |
|---|---|---|
| `DO_NOT_READ/01_WORLD_BIBLE.md` | § "4. The ledger" > "Access" | Add a subsection "Passphrase custody" declaring that Elias set the passphrase, that Nadia holds written recovery instructions with the upload, and that no other named character knows it. This is a canonical-fact addition and requires the explicit version change demanded by § "1. Authority". |
| `DO_NOT_READ/01_WORLD_BIBLE.md` | § "14. Immutable facts" | Add one line: the passphrase is required for the primary archive and is not recoverable from the decoy. |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | § `NPC-01` > "Knowledge"; § `NPC-01` > "Statements while conscious" | Add the passphrase to Elias's knowledge list. Add one fragment to the potential-fragment list. Keep the existing constraint that fragments are ambiguous without supporting clues. |
| `DO_NOT_READ/03_CHARACTER_DATABASE.md` | § `NPC-02` > "Knowledge" | Add that Nadia holds recovery instructions. Do not add the passphrase itself to her knowledge; she holds the instructions, not the secret. |
| `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | § "2. Nadia Soren" > "Disclosure stages" | Attach the recovery instructions to an existing disclosure stage. Do not create a new stage. |
| `LOGIC/00_ENTITY_KEY_TABLE.md` | § "Items and evidence objects"; § "Conclusions" | Add one item key for the recovery instructions. Add one conclusion key for passphrase possession. |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | new § "Passphrase"; § "12. Critical-route audit" | Add the clue group with both routes classed and point-valued per Decisions 6 and 7. Add a row to the audit table with the honest independent-route count of 2. |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § "2. Conclusion thresholds"; § "6. Soft-lock audit" | Add the passphrase threshold. Add a soft-lock subsection stating the two routes and the degraded outcome. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § 4 `EVT_123_NEWSROOM_RECORDS`; § 13 `EVT_410_LEDGER_RECOVERY`, `EVT_430_COMPLETE_TRANSFER` | Add the Route A grant to `EVT_123`. Replace the unsourced task line "retrieve passphrase information" in `EVT_410` with a reference to the conclusion. Add the passphrase to the entry conditions of `EVT_430`. |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § "3. Evidence outcome" > "Full authenticated transfer" and "Partial official evidence" | Add the passphrase to the full-transfer requirement list. Add passphrase failure to the partial list. |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | § "END-03: A Life Saved, Truth Delayed" | Confirm the wording covers passphrase failure as one cause of transfer failure. Adjust only if it excludes it. |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | § `EVT_420: Evidence transfer` | Add the passphrase to the "Complete transfer requires" list. |
| `DO_NOT_READ/02_MASTER_TIMELINE.md` | § `### 01:45` | Verify only. This entry already names all three factors and is the model the other documents must match. |

### 3.6 Migration order position

Phase 1 for the World Bible fact. Phase 6 for all logic wiring. The split is mandatory: `engine/03_ARCHITECTURE.md` § "3.12 Dependency direction" requires the World Bible to settle before Adventure Logic consumes it.

### 3.7 Side effects

- Adding a mandatory factor makes the best ending strictly harder. `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "6. Ending families" > `END_WITNESS_SPEAKS` becomes gated on one more chain. Confirm this is intended before implementing; it is a difficulty change, not only a consistency fix.
- Route B interacts with the medical clock. If a group finds the room after 01:00, Route B is closed and only Route A remains, which makes Route A load-bearing for late runs. The failure transformation in § 3.4 is what prevents this from becoming a soft lock, so it is not optional.
- `LOGIC/04_TIME_COST_MATRIX.md` § "2. Investigation action costs" has no entry for the `EVT_410` sub-tasks. Adding a factor to a node with no declared cost compounds the missing-cost problem recorded in § 11.
- The World Bible version change cascades: `DO_NOT_READ/00_CASE_OVERVIEW.md` § "Fair solution" lists four chains and does not mention the passphrase. Decide whether the passphrase becomes a fifth chain or remains a sub-step of Chain B.

### 3.8 Validation

Gates `V1`, `V4`, `V6`, `V7`, `V9` in § 12. Specifically: the passphrase conclusion must be reachable by two routes that share no granting node, no source actor, and no location; at least one route must be obtainable before 01:00; and the failure path must terminate in a declared ending node rather than an absent edge.

---

## 4. Decision 2 — `NODE_TYPE` and `TERMINAL_TYPE`

### 4.1 Objective

Every node declares `NODE_TYPE`. Every terminal node additionally declares `TERMINAL_TYPE`. This implements a rule the engine already states twice and the adventure implements zero times.

### 4.2 Canonical rule

`engine/00_ENGINE_SPECIFICATION_2.0.md` § "3.8 Terminal nodes" and `engine/03_ARCHITECTURE.md` § "3.18 Terminal architecture" both require the declaration. `templates/EVENT_TEMPLATE.md` already carries `node_type` and `terminal_type` fields, so no template change is needed. The recommended type list in § 3.18 is `VICTORY`, `PARTIAL_SUCCESS`, `NARRATIVE_FAILURE`, `CHARACTER_DEATH`, `TIME_EXPIRED`, `CASE_UNRESOLVED`, `CAMPAIGN_CONTINUATION`.

### 4.3 The eight ending families must become nodes

This is the substantive part of Decision 2. The eight families in `LOGIC/14_ENDING_TRIGGER_MATRIX.md` § "6. Ending families" currently have no node identity, so there is nothing to declare a terminal type on. Eight terminal nodes must be created in `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 14.

`EVT_900_RESOLVE_ENDING` is a dispatcher with successors and is therefore `INTERMEDIATE`, not terminal.

Proposed mapping, to be ratified before implementation:

| Ending family | Proposed `TERMINAL_TYPE` | Confidence |
|---|---|---|
| `END_WITNESS_SPEAKS` | `VICTORY` | High |
| `END_EVIDENCE_WITHOUT_WITNESS` | `PARTIAL_SUCCESS` | Medium — Elias dies in this family |
| `END_LIFE_SAVED_TRUTH_DELAYED` | `PARTIAL_SUCCESS` | High |
| `END_PROTECTIVE_CUSTODY` | `NARRATIVE_FAILURE` | High |
| `END_PUBLIC_LEAK` | `PARTIAL_SUCCESS` | High |
| `END_SILENT_TERMINAL` | `CHARACTER_DEATH` or `TIME_EXPIRED` | **Low — requires ratification** |
| `END_WRONG_ACCUSATION` | `CASE_UNRESOLVED` | High |
| `END_FRACTURED_TRUTH` | `PARTIAL_SUCCESS` | High |

Two questions must be answered by the maintainer, not by the implementer:

1. `CHARACTER_DEATH` is undefined as to whether it covers a non-player character. Elias is an NPC in every configuration. If the type is player-character-only, `END_SILENT_TERMINAL` is `TIME_EXPIRED` and `END_EVIDENCE_WITHOUT_WITNESS` is `PARTIAL_SUCCESS` on evidence grounds alone.
2. § 3.18 calls the list "Recommended terminal types", so extension is permitted. If neither existing type fits, adding one is an engine change and must be made in `engine/03_ARCHITECTURE.md`, not improvised in the adventure.

### 4.4 Affected files

| File | Section | Edit |
|---|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "1. Graph conventions" | Add `NODE_TYPE` and `TERMINAL_TYPE` to the field list, which currently has ten fields and omits both. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | all 40 nodes | Add `NODE_TYPE: INTERMEDIATE`. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "14. Ending dispatch" | Add eight terminal nodes, each with `NODE_TYPE: TERMINAL` and a ratified `TERMINAL_TYPE`. |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § "6. Ending families" | Add the node identifier and terminal type to each family. Trigger conditions stay here; node identity moves to the graph. |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | `END-01` … `END-08` | Reduce to narrative outcome text plus a pointer. Remove any restatement of trigger conditions. |
| `engine/03_ARCHITECTURE.md` | § "3.18 Terminal architecture" | Edit only if question 1 or 2 above forces a type-list change. |

### 4.5 Migration order position

Phase 7, after the namespace migration so the eight new nodes are authored in final identifiers.

### 4.6 Side effects

- Ending logic will exist in three files at once: `06_ENDING_FRAMEWORK.md` (narrative), `14_ENDING_TRIGGER_MATRIX.md` (triggers), `10_INVESTIGATION_NODE_GRAPH.md` (node identity and edges). Without the ownership split stated in § 4.4, this creates a third source of truth and violates `engine/03_ARCHITECTURE.md` § "3.13 Single source of truth". The ownership split is mandatory, not stylistic.
- `END_FRACTURED_TRUTH` is defined in `06_ENDING_FRAMEWORK.md` § "END-08" as requiring two players. Once it is a node, reachability validation will report it unreachable in any single-player configuration. Solo mode is out of scope for this revision, so validation gate `V5` must be evaluated per play mode rather than globally.
- Declaring `NODE_TYPE: INTERMEDIATE` on all 40 existing nodes asserts every one has a successor. That assertion is untrue until Decision 3 completes, so Decisions 2 and 3 must ship in the same revision or the repository is left in a state that fails its own rule more visibly than before.

### 4.7 Validation

Gates `V3` and `V5`. Every node carries exactly one `NODE_TYPE`; every `TERMINAL` carries exactly one `TERMINAL_TYPE` drawn from the ratified list; no `INTERMEDIATE` node carries a `TERMINAL_TYPE`.

---

## 5. Decision 3 — `Outgoing` declarations

### 5.1 Objective

Every node declares `Outgoing`. Terminal nodes declare `Outgoing: None`. This closes the structural defect named in `engine/00_ENGINE_SPECIFICATION_2.0.md` § "3.8 Terminal nodes": "A non-terminal node without a valid outgoing route is a structural defect."

### 5.2 Scope of work

Of 40 nodes, 3 declare `Outgoing`, 1 declares successors in the wrong field, and 36 declare nothing. Total edits: 37 existing nodes plus 8 new terminal nodes.

`EVT_100_SHARED_BRIEFING` requires a specific correction rather than an addition. Its two successors are currently expressed as "unlocks" lines inside **State changes**. Move them into an `Outgoing` block. A successor is a graph edge, not a state mutation, and leaving it in **State changes** will corrupt the writer/reader analysis required by Decision 4.

### 5.3 Split-branch terminators

`engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § "5. No Free Asynchronous Drift" requires every split branch to terminate in one of `REJOIN`, `REMOTE_CONTACT`, `WAIT_UNTIL_SYNC`, `EMERGENCY_INTERRUPT`, `TERMINAL_OUTCOME`. None of these appears anywhere in the adventure.

Nodes inside a split phase must therefore declare their `Outgoing` using this vocabulary in addition to node targets. This is an inference from an existing engine MUST rather than part of the literal accepted decision, and it should be ratified explicitly. It is included because writing edges for split-phase nodes without it produces edges that cannot be validated against § 5.

### 5.4 Affected files

| File | Section | Edit |
|---|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "1. Graph conventions" | Promote "outgoing routes" from a listed convention to a mandatory field with a stated format. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_100_SHARED_BRIEFING` | Move the two "unlocks" lines from **State changes** to `Outgoing`. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | 36 nodes from `EVT_112_RESTRICTED_APARTMENT` onward | Author `Outgoing`. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | 8 new terminal nodes | `Outgoing: None`. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § "15. Graph integrity rules" | Restate as checkable assertions over the now-explicit edge set instead of prose claims. |
| `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | § "2. Split One", § "4. Split Two", § "7. Final-act split" | Declare which nodes belong to which split phase, so § 5.3 terminators can be assigned. |

### 5.5 Migration order position

Phase 7, immediately after Decision 2 and in the same revision.

### 5.6 Side effects

This is the highest-yield and highest-risk item in the plan.

- **Authoring edges forces reachability decisions that are currently unmade.** Two known problems will surface immediately and must be resolved during authoring rather than deferred. First, the room-identifier chain: three of five identifier clues in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § "4. Signal Room 4B" come from Elias, Lena and Iris, all of whom `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` § "3. Fixed schedules" places inside Signal Room 4B, so those edges cannot precede room discovery. Second, the Rook proof chain: the three nodes that award Rook points reach a maximum of 3, and `LOGIC/07_EVIDENCE_VALIDATION.md` § "2. Conclusion thresholds" requires 4 for public accusation, so either new granting nodes are authored or the threshold moves. Neither problem is created by this decision; both become undeniable once edges exist.
- Five clues in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § "8. Rook compromised" have no granting node at all: `C_ROOK_KRELL_CONTACT`, `C_ROOK_LENA_BULLETIN_FALSE`, `C_REED_NAMES_ROOK_LINK`, `C_MINA_AUTHENTICATES_REPORT`, `C_EVIDENCE_ROOM_PHOTO_PATH`. Edge authoring will expose them as orphans requiring either a node or deletion.
- The failsafe in `LOGIC/05_CORE_EVENT_GRAPH.md` § `EVT_170` — Nadia revealing the ferry infrastructure at 21:45 — has no node in the investigation graph. It will surface as an unmapped backbone element in Decision 5 and as a missing edge here.
- Edge authoring interacts with the parallel-action model. `LOGIC/04_TIME_COST_MATRIX.md` § "3. Parallel action model" and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § "4. Synchronization Windows" disagree about leftover time, and `LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` declares no maximum window durations. Edges crossing a split boundary cannot be validated for timing until that is settled. This is out of accepted scope; record it as a blocker on gate `V8` rather than fixing it silently.

### 5.7 Validation

Gates `V3`, `V5`, `V8`. Every `INTERMEDIATE` node has at least one `Outgoing` target; every target resolves to a declared node; every terminal node is reachable from `EVT_100_SHARED_BRIEFING` in at least one play mode; no node is unreachable in every mode.

---

## 6. Decision 4 — State variable system

### 6.1 Objective

Every declared state variable has at least one writer and at least one reader, or it is removed. Every state machine has exactly one declared state variable.

### 6.2 The Variable Register

`LOGIC/01_WORLD_STATE_VARIABLES.md` becomes the sole owner of every variable and gains a register with these columns:

`Variable | Domain | Initial | Writers | Readers | Owning state machine`

Writers and readers are identifier lists, not prose. A variable with an empty writer list or an empty reader list fails validation and must be removed in the same revision that reports it.

### 6.3 Disposition table

Every one of the 47 declared variables, 2 undeclared-but-used variables, 1 duplicate alias and 4 undeclared state machines receives an explicit disposition. Removals are listed with their justification because each one deletes an authored concept.

**Remove — no writer, no reader, and no prose dependency:**

| Variable | Justification |
|---|---|
| `A_KRELL_TERMINAL` | No writer and no reader. `03_CHARACTER_DATABASE.md` § `NPC-06` makes Krell's presence optional and remote; his terminal confidence never affects a resolvable event. |
| `REGROUP_REQUIRED` | No writer and no reader. Regroups are authored gates (`EVT_150`, `EVT_300`), not a state flag. |

**Remove — redundant with a better-owned representation:**

| Variable | Justification |
|---|---|
| `T_LENA`, `T_IRIS`, `T_REED` | No writer exists. `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` §§ 4, 5 and 7 already gate all three on evidence and leverage, not on a trust scalar. Removing them makes the documents agree instead of maintaining an unused parallel mechanism. The prose in § 4 that reads "pressured without trust" must be rewritten in evidence terms in the same edit. |
| `ELIAS_SURVIVAL` | Derivable from the medical state machine once that machine has writers. Keeping both invites drift. |
| `LEDGER_PRIMARY_STATUS` | Duplicates the item state of `ITEM_LEDGER_PRIMARY` owned by `LOGIC/02_ITEM_STATE_MATRIX.md`. Derive, do not store. |
| `NADIA_TRUST` in `DO_NOT_READ/03_CHARACTER_DATABASE.md` § `NPC-02` | An alias of `T_NADIA` with the same range. Replace with a reference to the canonical variable. |
| `ROOK_EXPOSED`, `RESCUE_CONTROLLED_BY_TRUSTED_PARTY`, `PUBLIC_ACCUSATION_CORRECT` in `DO_NOT_READ/06_ENDING_FRAMEWORK.md` § "Ending variables" | Divergent names for variables already owned by `LOGIC/01_WORLD_STATE_VARIABLES.md` § 9. Delete the list and reference the owner. |

**Keep and wire — reader exists, writer must be authored:**

| Variable | Writer to author | Reader that already exists |
|---|---|---|
| `A_PUBLIC` | `EVT_440_FINAL_PUBLIC_POSITION`, Nadia publication | `01_WORLD_STATE_VARIABLES.md` § 4 "Public awareness 2+"; `05_CORE_EVENT_GRAPH.md` § `EVT_400`; `14_ENDING_TRIGGER_MATRIX.md` § 3 |
| `A_REED_ROOM` | An off-screen event or `EVT_243` outcome | `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 "Reed searches wrong upper rooms first because he lacks exact room number" |
| `ELIAS_STATE` | Clock thresholds at 23:40, 01:00, 01:15; `EVT_330`; `EVT_400` | `14_ENDING_TRIGGER_MATRIX.md` § "2. Medical outcome" — which must be rewritten to read the variable instead of its current prose categories |
| `APT_STATE`, `NEWS_STATE`, `REED_OFFICE_STATE` | The transitions in `11_LOCATION_STATE_MACHINE.md` §§ 2, 3, 6, restated as writes | Node entry conditions |
| `P1_AVAILABLE_AT`, `P2_AVAILABLE_AT` | Every node's time cost | Synchronization gates |
| `P1_PRIVATE_KNOWLEDGE_SET`, `P2_PRIVATE_KNOWLEDGE_SET` | Every clue grant | `EVT_150`, `EVT_300`; `08_TWO_PLAYER_CORE_RULES.md` § 7 |
| `P_ROOM_4B`, `P_CODE`, `P_REED` | Already written | No reader exists. Decision 6 supplies thresholds in `07_EVIDENCE_VALIDATION.md`. |

**Declare — currently used without declaration:**

`P_LENA_PROTECTING` and `P_DECOY` are used in `EVT_231_PREPAID_PHONE_TRACE` and `EVT_242_REED_OFFICE_SEARCH` with hedging text. Under Decision 6 every conclusion is point-gated, so both become real declared variables. The hedging text is deleted.

**Split — one state machine, three dimensions:**

`TERMINAL_STATE` violates the one-variable-per-state-machine rule. `LOGIC/01_WORLD_STATE_VARIABLES.md` § 7 says it "combines" weather, hostile presence and access-discovery, and `LOGIC/11_LOCATION_STATE_MACHINE.md` § 9 confirms three independent dimensions. These are three state machines and require three variables: weather, hostile presence, known access routes.

**Create — state machines with no variable:**

`LOGIC/11_LOCATION_STATE_MACHINE.md` §§ 4, 5, 7 and 8 define state machines for Café Orpheus, the police annex, Iris's workplace and the harbor archive with named states and no variable. Four variables must be declared in `LOGIC/01_WORLD_STATE_VARIABLES.md` § 7.

Net arithmetic: 47 declared, minus 7 removed, plus 4 new location variables, plus 2 from the terminal split, plus 3 new point variables from Decisions 1 and 6, giving 49 canonical variables, each with a non-empty writer list and a non-empty reader list.

### 6.4 Affected files

`LOGIC/01_WORLD_STATE_VARIABLES.md` (register, all sections), `LOGIC/11_LOCATION_STATE_MACHINE.md` (transitions restated as writes; four new variables bound), `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (writes declared per node), `LOGIC/02_ITEM_STATE_MATRIX.md` (item states as the source for the removed ledger-status variable), `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md` (off-screen writes, including the existing `A_ROOK_TERMINAL +1`), `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` (trust removals rewritten as evidence gates), `LOGIC/14_ENDING_TRIGGER_MATRIX.md` (reads the medical variable), `DO_NOT_READ/03_CHARACTER_DATABASE.md` (alias removed), `DO_NOT_READ/06_ENDING_FRAMEWORK.md` (divergent list removed).

### 6.5 Migration order position

Analysis and disposition in Phase 2. Removals executed with the rename in Phase 3. Writer and reader wiring in Phase 4.

### 6.6 Side effects

- Removing three trust variables changes the feel of Lena, Iris and Reed from graduated relationship tracking to binary evidence gates. That is what the knowledge matrix already specifies, but it is a design consequence and should be confirmed, not assumed.
- Rewriting `14_ENDING_TRIGGER_MATRIX.md` § 2 to read a variable rather than prose categories changes how medical outcomes are computed. The three prose categories must map onto the seven-value medical state exactly, or endings shift.
- Wiring `P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` will expose the contradiction between `LOGIC/04_TIME_COST_MATRIX.md` § "3. Parallel action model", whose worked example grants a free extra action, and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, which forbids it. The variables cannot be given consistent semantics until that is resolved.
- Two nodes declare no time cost at all — `EVT_241_MARCUS_FULL_DISCLOSURE` and `EVT_314_MAIN_ENTRY_CONFRONTATION` — so they cannot write the availability variables. Costs must be authored as part of this work.

### 6.7 Validation

Gates `V2` and `V4`. Zero variables with an empty writer or reader list; zero state machines without exactly one variable; zero variables referenced outside the register.

---

## 7. Decision 5 — Core-to-investigation graph mapping

### 7.1 Objective

Publish an explicit mapping between `LOGIC/05_CORE_EVENT_GRAPH.md` and `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`, documenting expansion where it occurred.

### 7.2 Deliverable

A new file, `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/16_EVENT_GRAPH_MAPPING.md`, taking the next free number in the sequence.

The core graph is retained as a backbone layer rather than retired. `LOGIC/05_CORE_EVENT_GRAPH.md` § "Graph conventions" already frames itself that way, and it holds the only cross-reference into `LOGIC/06_NPC_SCHEDULE_AND_PRIORITY.md`.

### 7.3 Namespace separation

Backbone entries migrate from `EVT_` to `ARC_` under Decision 8. Both files currently use `EVT_` stems, and several stems carry different meanings in each file: `EVT_120` is the apartment cluster in the core graph and the newsroom entry in the investigation graph, and the same inversion affects `EVT_110`, `EVT_210`, `EVT_220`, `EVT_230`, `EVT_240`, `EVT_300` and `EVT_420`. These are distinct strings and not literal duplicate identifiers, so this is a traceability defect rather than a collision, but the shared stem makes the mapping unreadable and invites misreference. Separating the namespaces removes the ambiguity permanently.

The alternative — retire `05_CORE_EVENT_GRAPH.md` and fold its content into `10` — was considered and rejected. It would discard the backbone view, orphan the schedule cross-reference, and lose the record of which backbone elements were never implemented.

### 7.4 Draft mapping

To be ratified before implementation. Confidence is stated because several rows are judgement calls.

| Backbone | Investigation nodes | Relationship | Confidence |
|---|---|---|---|
| `ARC_100` Nadia's briefing | `EVT_100_SHARED_BRIEFING` | 1:1 | High |
| `ARC_110` First split decision | Absorbed into the **Decision** block of `EVT_100`, realised by `EVT_110` and `EVT_120` | Absorbed | Medium |
| `ARC_120` Apartment cluster | `EVT_110`, `EVT_111`, `EVT_112`, `EVT_113`, `EVT_114`, `EVT_115` | Expanded 1:6 | High |
| `ARC_130` Newsroom cluster | `EVT_120`, `EVT_121`, `EVT_122`, `EVT_123` | Expanded 1:4 | High |
| `ARC_140` Café cluster | `EVT_211_CAFE_ORPHEUS` | Relocated from opening block to midgame | **Low — see § 7.6** |
| `ARC_170` First synchronization gate | `EVT_150_REGROUP_ONE` | 1:1, renumbered | High |
| `ARC_200` Rook pressure | `EVT_223_ROOK_INTERVIEW` | Partial | Medium |
| `ARC_210` Reed office opportunity | `EVT_242_REED_OFFICE_SEARCH` | 1:1 | High |
| `ARC_220` Iris trail | `EVT_230`, `EVT_231`, `EVT_232` | Expanded 1:3 | High |
| `ARC_230` Marcus disclosure ladder | `EVT_240`, `EVT_241` | Expanded 1:2 | High |
| `ARC_240` Mina evidence preservation | `EVT_220_MINA_REPORT_COMPARISON`, partly `EVT_400` | Partial, split | Medium |
| `ARC_270` Second synchronization gate | `EVT_300_REGROUP_TWO` | 1:1, renumbered | High |
| `ARC_300` Terminal route selection | `EVT_310`–`EVT_314` | Expanded 1:5 | High |
| `ARC_320` Off-screen hostile convergence | `EVT_420_REED_OR_ROOK_CONFRONTATION` plus `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4 | Split across documents | Medium |
| `ARC_340` Signal Room discovery | `EVT_330`, `EVT_331` | Expanded 1:2, renumbered | High |
| `ARC_400` Trusted rescue validation | `EVT_400_RESCUE_CONTROL` | 1:1 | High |
| `ARC_420` Evidence transfer | `EVT_410`, `EVT_430` | Expanded 1:2 | High |
| `ARC_440` Final accusation | `EVT_440_FINAL_PUBLIC_POSITION` | 1:1 | High |
| `ARC_900` Ending resolution | `EVT_900` plus eight new terminal nodes | Expanded 1:9 | High |

Investigation nodes with no backbone origin, to be recorded as additions: `EVT_210_HARBOR_ARCHIVE_ENTRY`, `EVT_212_TERMINAL_RECON`, `EVT_221_CAMERA_REQUEST_AUDIT`, `EVT_222_PROTECTION_ORDER_AUDIT`, `EVT_243_REED_NEGOTIATION`.

Backbone elements with no implementation, to be recorded as unimplemented with a reason: the fixed no-later-than-22:10 trigger of `ARC_200`, and the 21:45 Nadia ferry-infrastructure failsafe inside `ARC_170`.

### 7.5 Affected files

New `LOGIC/16_EVENT_GRAPH_MAPPING.md`; `LOGIC/05_CORE_EVENT_GRAPH.md` (prefix migration, purpose statement); `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (back-reference per node); `LOGIC/00_ENTITY_KEY_TABLE.md` § "Event key ranges" (restate for two namespaces).

### 7.6 Side effects

- The `ARC_140` row records a real semantic change, not a clean expansion. `DO_NOT_READ/02_MASTER_TIMELINE.md` § `### 20:05` assigns Café Orpheus to Player 2 as a starting lead, and `LOGIC/05_CORE_EVENT_GRAPH.md` places the café cluster in the opening block per the ranges in `00_ENTITY_KEY_TABLE.md`. The investigation graph moves it to the midgame harbor branch. The mapping must not paper over this; either the timeline changes or the node moves back.
- Renaming the backbone prefix touches the only working cross-reference between logic documents. Verify `LOGIC/05_CORE_EVENT_GRAPH.md` § `ARC_320` still resolves to `06_NPC_SCHEDULE_AND_PRIORITY.md` after the edit.
- Once "unimplemented" is a formal status, it becomes a backlog the next revision must either implement or delete. That is the intent, but it makes previously invisible gaps into tracked debt.

### 7.7 Validation

Gate `V6`. Every `ARC_` maps to at least one `EVT_` or carries an explicit unimplemented status with a reason; every `EVT_` maps to an `ARC_` or carries an explicit addition status; no identifier appears in both namespaces.

---

## 8. Decision 6 — Progress model

### 8.1 Canonical progression

```text
Node outcome
     ↓
  Points
     ↓
  Clues
     ↓
Conclusions
```

Definitions, to be stated once in `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` § 1 and referenced elsewhere:

- **Points** are the scalar award declared on a node outcome. They are the raw signal of investigative progress and the only quantity a node may grant.
- **Clues** are named, classed evidence units. A clue declares its identifier, its class or classes, its point value, its granting node or nodes, and its conclusion group. A point is realised only by instantiating a clue.
- **Conclusions** are gates evaluated over the held clue set, using point sum and class diversity.

### 8.2 The governing invariant

**A point may only be awarded by instantiating a clue.**

This single rule does most of the work:

- It eliminates the free-floating `P_ROOK +1 procedural` syntax used in `EVT_220`, `EVT_221` and `EVT_222`, which currently mixes an increment on a bounded integer with an untracked class label.
- It makes every point total auditable back to a clue identifier, so the reachable maximum of any variable is computable rather than hand-maintained.
- It removes the need for a separate class-tracking variable, because class diversity is read from the held clue set. This is why Decision 7 requires no new state.

### 8.3 Replacing declared ranges with computed maxima

`LOGIC/01_WORLD_STATE_VARIABLES.md` § "2. Case progress variables" declares fixed ranges such as `0-3`. Those ranges are hand-maintained and at least three of them are already exceeded by the sum of the awards in the node graph: the staged, harbor and room-identification variables can each reach 4 against a declared maximum of 3, assuming their granting nodes are mutually reachable. Whether they are mutually reachable is currently unknowable because the graph has no edges, which is why this is stated as a potential overflow rather than a proven one.

Under the new model the declared maximum of a point variable equals the sum of the point values of all clues in its group. It is a computed figure recorded in the register, and any mismatch is a validation failure rather than a silent inconsistency.

### 8.4 Affected files

| File | Section | Edit |
|---|---|---|
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | § 1 and all clue groups | Restate as the clue register: one row per clue with identifier, class or classes, point value, granting nodes, conclusion group. |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § "2. Conclusion thresholds" | Restate every threshold as point sum plus class diversity over the clue set. Supply the missing thresholds for room identification, code completion and Reed presence. |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | § 2 | Replace hand-declared ranges with computed maxima; add the three new point variables. |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | every node with a **State changes** block | Replace bare point awards with clue grants that carry point values. |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | § 3 | Reduce to conclusion-level narrative rationale; move all counting to the logic layer. |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | §§ 4, 5 | Confirm accusation gates read conclusions, never raw points. |

### 8.5 Migration order position

Phase 5, after classes exist and after the variable register exists.

### 8.6 Side effects

- Recomputing maxima will change the reachable ceiling of several variables and may invalidate existing thresholds in either direction. The Rook public-accusation threshold of 4 against three declared granting nodes is the known case; there may be others that only appear once maxima are computed.
- Converting 65 clue listings into a register with point values means assigning a point value to every clue for the first time. Those values are new design decisions, not transcriptions, and they directly control difficulty.
- `LOGIC/07_EVIDENCE_VALIDATION.md` § 2 currently expresses some gates in points and others in clue categories. Unifying them will change at least the room-identification gate from a category rule to a numeric one, which alters when the conclusion unlocks.
- The medical conclusion is the only gate currently consistent across both systems. Verify it survives the rewrite unchanged so the rewrite can be shown to be behaviour-preserving in at least one case.

### 8.7 Validation

Gates `V4`, `V7`, `V9`. Every point award traces to a clue; every clue has a point value; every declared maximum equals the computed sum; every conclusion threshold is satisfiable from clues that are reachable without circularity.

---

## 9. Decision 7 — Clue classes

### 9.1 Canonical class set

Six classes, taken from `LOGIC/07_EVIDENCE_VALIDATION.md` § "1. Proof classes", which is already correct and complete:

`PHYSICAL`, `DIGITAL`, `TESTIMONIAL`, `PROCEDURAL`, `CONTEXTUAL`, `BEHAVIOURAL`

### 9.2 Single ownership

Two documents currently define the class list and disagree. `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` § "2. Clue classes" declares five and omits `DIGITAL`, while folding "recording" into `PHYSICAL`. `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` nevertheless tags clues as digital.

Ownership splits across two layers:

- The **engine** owns the requirement. `engine/00_ENGINE_SPECIFICATION_2.0.md` § "3.6 Clue redundancy" gains one sentence: an adventure MUST declare a closed clue-class set, and every clue MUST carry at least one class from it. The engine does not name the classes, because `engine/03_ARCHITECTURE.md` § "3.2 Engine Specification" forbids adventure content in the engine.
- The **adventure** owns the vocabulary, in `LOGIC/07_EVIDENCE_VALIDATION.md` § 1. `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` § 2 is reduced to a pointer, and its definition of `PHYSICAL` drops "recording".

### 9.3 Tagging work

All 64 distinct clues require at least one class. Currently only §§ 2, 3 and 8 of `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` carry tags, covering 21 clues. The remaining 43 are untagged while §§ 5, 7 and 8 already state class-diversity thresholds that cannot be evaluated without them.

Multi-class clues are permitted; the existing `procedural/digital` and `testimonial/procedural` tags are retained. Class diversity counts distinct classes across the held set, and a multi-class clue contributes all of its classes. That counting rule must be stated explicitly, because it materially changes whether a three-class threshold is reachable.

### 9.4 Affected files

`LOGIC/07_EVIDENCE_VALIDATION.md` § 1 (canonical set, counting rule), `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` § 2 (reduced to a pointer), `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` (43 clues tagged), `engine/00_ENGINE_SPECIFICATION_2.0.md` § 3.6 (requirement added), `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` (ad-hoc class labels removed from point awards).

### 9.5 Migration order position

Phase 1 for the vocabulary decision, Phase 5 for the tagging, because tags are recorded in the clue register that Decision 6 creates.

### 9.6 Side effects

- Editing `engine/00_ENGINE_SPECIFICATION_2.0.md` desynchronises the byte-identical root copy `00_ENGINE_SPECIFICATION_2.0.md`. See § 11.
- Assigning classes to 43 clues is a design act. Class assignment determines which conclusions are reachable, so a careless tagging pass can silently make a three-class threshold unsatisfiable.
- The `DIGITAL` restoration means some clues currently reasoned about as physical are digital, which may reduce class diversity in groups that relied on the five-class reading.

### 9.7 Validation

Gate `V7`. Exactly one class list exists in the repository; every clue carries at least one class from it; every class-diversity threshold is satisfiable by at least one reachable clue combination.

---

## 10. Decision 8 — Identifier namespaces

### 10.1 Canonical scheme

**Mnemonic uppercase with a full-word prefix and underscore separators**, for example `CLUE_APT_SERVICE_LATCH`.

Three schemes exist today: numeric-hyphen labels in the case documentation (`NPC-01`, `LOC-01`, `CLU-01`, `CON-01`, `RH-01`, `END-01`), mnemonic-underscore keys in the logic layer (`NPC_ELIAS`, `C_*`, `D_*`, `CON_*`, `END_*`), and numeric-underscore examples in the engine (`NPC_001`, `CLUE_008`, `DEC_103`, `CHK_022`, `END_005`).

Mnemonic wins on the criteria that apply to this repository. The entire Alpha 0.2b logic layer already uses it; the prototype is hand-authored, print-first and manually validated, with automated tooling explicitly deferred by `reviews/GEMINI_ARCHITECTURE_REVIEW_RESPONSE_0.3.md` § "CI/CD Graph Validation"; and migrating 64 clues plus every other identifier to opaque numbers before the first playtest is high-churn, high-error and low-value.

One honest objection must be recorded. `engine/03_ARCHITECTURE.md` § "3.14 Internal IDs and public references" requires IDs to "survive renaming", and mnemonic keys embed display names, so `NPC_ELIAS` does not survive renaming the character. `LOGIC/00_ENTITY_KEY_TABLE.md` § "Purpose" justifies its keys on exactly the grounds its keys violate. The resolution is to amend § 3.14 to require that keys survive **display-name changes** and are frozen at creation, which is the property actually needed, and to accept that a key may become a historical misnomer if a character is renamed.

Amending § 3.14 is not a reverse dependency. `engine/03_ARCHITECTURE.md` § "3.12 Dependency direction" prohibits engine rules from depending on adventure data; a generic prefix registry names no adventure content.

### 10.2 Prefix registry

To be added to `engine/03_ARCHITECTURE.md` § 3.14 as a closed, extensible-by-amendment list.

| Prefix | Entity | Owner document |
|---|---|---|
| `NPC_` | Character | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `LOC_` | Location | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `ITEM_` | Item or evidence object | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `CLUE_` | Clue | `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` |
| `CON_` | Conclusion | `LOGIC/00_ENTITY_KEY_TABLE.md` |
| `RH_` | Red herring | `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` |
| `FACT_` | NPC-knowledge fact | `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` |
| `ARC_` | Backbone arc | `LOGIC/05_CORE_EVENT_GRAPH.md` |
| `EVT_` | Playable node | `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` |
| `END_` | Ending family | `LOGIC/14_ENDING_TRIGGER_MATRIX.md` |
| `VAR_` | State variable | `LOGIC/01_WORLD_STATE_VARIABLES.md` |
| `DEC_`, `CHK_` | Decision, check | Reserved — no records exist yet |

### 10.3 Complete migration table

| Current form | Canonical form | Files | Count |
|---|---|---|---:|
| `C_*` | `CLUE_*` | `12`, `10`, `07` | 64 distinct |
| `CLU-01`…`CLU-04` | merge into `CLUE_APT_*` | `05_CLUE_ARCHITECTURE.md` § `CON-01` | 4 |
| `D_*` | `CON_*` | `12`, `14` | 13 |
| `CON-01`…`CON-10` | `CON_*` | `05_CLUE_ARCHITECTURE.md` § 3 | 10 |
| `CON_*` (10 existing) | `CON_*`, three split into tiers | `00_ENTITY_KEY_TABLE.md`, `05`, `10` | 10 → 13 |
| `RH-01`…`RH-04` | `RH_*` | `05_CLUE_ARCHITECTURE.md` § 4 | 4 |
| `NPC-01`…`NPC-10` | `NPC_*` | `03_CHARACTER_DATABASE.md` | 10 |
| `LOC-01`…`LOC-10` | `LOC_*` | `04_LOCATION_DATABASE.md` | 10 |
| `END-01`…`END-08` | `END_*` | `06_ENDING_FRAMEWORK.md` | 8 |
| `EVT_nnn` (backbone) | `ARC_nnn` | `05` | 19 |
| `EVT_nnn_NAME` | unchanged | `10` | 40 |
| `P_*` | `VAR_PTS_*` | `01`, `05`, `07`, `10` | 8, plus 3 new |
| `T_*` | `VAR_TRUST_*` | `01`, `10` | 6 → 3 after removals |
| `NADIA_TRUST` | `VAR_TRUST_NADIA` | `03_CHARACTER_DATABASE.md` | 1 alias removed |
| `A_*` | `VAR_AWARE_*` | `01`, `06`, `11` | 5 → 4 after removal |
| `CLOCK` | `VAR_CLOCK` | `01`, `04` | 1 |
| `*_STATE` | `VAR_STATE_*` | `01`, `10`, `11` | 5 → 11 after split and additions |
| `P1_*`, `P2_*`, `SHARED_KNOWLEDGE_SET` | `VAR_SYNC_*` | `01`, `10`, `13` | 8 |
| Ending variables | `VAR_END_*` | `01`, `06`, `14` | 13 → 11 after removals |

The `VAR_` prefix with a domain segment resolves four defects at once: the collision between `P_` for progress and `P1_`/`P2_` for players; the `NADIA_TRUST` versus `T_NADIA` alias; the ending-variable name drift between `01` § 9 and `06`; and the un-prefixed `APT_STATE`, `ELIAS_STATE` and `CLOCK`.

### 10.4 Execution method

A single mechanical pass, longest-identifier-first to prevent partial-token corruption. `C_` and `D_` are dangerous: they are short, and `D_` is a substring of nothing but `C_` appears inside ordinary words. Every replacement must be anchored on a word boundary and confirmed against the published table rather than applied as a free-text substitution.

Migration is executed once, in one revision. A partially migrated repository is worse than either endpoint because it looks consistent while being ambiguous.

### 10.5 Affected files

Every markdown file in `adventures/The_Last_Witness/`, plus `engine/03_ARCHITECTURE.md` § 3.14, plus `LOGIC/00_ENTITY_KEY_TABLE.md` throughout.

### 10.6 Migration order position

Phase 3, after the disposition tables from Decision 4 are agreed so that doomed identifiers are never renamed, and before Decisions 2, 3, 5 and 6 author new content, so all new content is written in final names.

### 10.7 Side effects

- Every identifier in every external draft, note or in-flight review becomes stale in one commit. This is unavoidable and is the reason for the single-pass rule.
- Splitting three conclusions into tiers changes the conclusion count from 10 to 13 and requires `LOGIC/00_ENTITY_KEY_TABLE.md` § "Conclusions" to gain three rows.
- `LOGIC/00_ENTITY_KEY_TABLE.md` § "Event key ranges" describes one numeric space for events; it must be restated for two namespaces.
- The ambiguous inline reference to `06_ENDING_FRAMEWORK.md` in `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` § 14 is a basename that reads as if it points inside `LOGIC/`, where a different file occupies that number. Disambiguate it during this pass.
- Twelve entity keys are referenced only in `LOGIC/00_ENTITY_KEY_TABLE.md`. Five of them are gameplay objects that the clue graph reasons about under other names, and those are worth reconciling during the rename: the archive photograph duplicate, the transit card, the carrier log, the payment record and the ambulance authorisation. The remaining unreferenced keys are secondary characters and abstract zones; leave them unless the register work shows they are needed.

### 10.8 Validation

Gates `V1` and `V2`. Every identifier matches the registry; no identifier from a superseded scheme survives; every identifier resolves to exactly one register entry; no register entry is unreferenced except where deliberately reserved.

---

## 11. Global migration order

Phases are strictly ordered. Each phase must pass its gates before the next begins.

| Phase | Work | Decisions | Rationale for position |
|---|---|---|---|
| **P0** | Baseline inventory; record the counts in § 2; decide the handling of the eight byte-identical root duplicates | — | Read-only. Establishes denominators. |
| **P1** | Upper-layer canon: engine prefix registry and § 3.14 amendment; clue-class requirement in engine § 3.6; World Bible passphrase fact with version change; clue-class vocabulary single-sourced | 7, 8, 1 (fact only) | `engine/03_ARCHITECTURE.md` § 3.12 requires upper layers to settle first. |
| **P2** | Author the Variable Disposition Table and the Identifier Migration Table as specifications; skeleton the clue and node registers | 4, 8 | Paper exercise. Prevents renaming identifiers that are about to be deleted. |
| **P3** | Execute the mechanical rename and the variable deletions in one pass | 8, 4 (removals) | Single-pass rule. All later authoring uses final names. |
| **P4** | Wire writers and readers; bind one variable per state machine; split the terminal-exterior variable; create the four missing location variables | 4 | Requires final names. Precedes the progress model because points are variables. |
| **P5** | Rebuild the progress model; tag all 64 clues; restate every threshold | 6, 7 | Requires classes and variables. |
| **P6** | Author the passphrase routes, clues, conclusion, thresholds and failure transformation | 1 | Requires the clue register to exist. |
| **P7** | Add `NODE_TYPE` to 40 nodes; author `Outgoing` for 37; create 8 terminal ending nodes | 2, 3 | Last authoring phase, because edges must point at a final node set including the passphrase nodes. |
| **P8** | Publish the backbone mapping | 5 | Requires the final node set. |
| **P9** | Consistency sweep and full validation gate | all | — |
| **P10** | Version bump, changelog entry, README status correction | — | Records the revision. |

Decisions 2 and 3 must ship in the same revision. Declaring every node `INTERMEDIATE` while 36 of them have no successor asserts something false more loudly than the current silence.

### 11.1 Cross-cutting side effect: the root duplicates

Eight root-level files are byte-identical to canonical files elsewhere: `README (1).md`, `README (2).md`, `README (3).md`, `DOCUMENT_TEMPLATE.md`, `EVENT_TEMPLATE.md`, `ISSUE_TEMPLATE.md`, `STYLE_GUIDE.md`, and `00_ENGINE_SPECIFICATION_2.0.md`. A ninth, `README (4).md`, is a stale non-identical fork.

Phase 1 edits `engine/00_ENGINE_SPECIFICATION_2.0.md` for the clue-class requirement. The moment that edit lands, the root copy silently diverges and the repository has two engine specifications with different content and no marked precedence.

Deduplication is not among the accepted decisions, so this plan does not mandate it. It does mandate a decision at P0: either deduplicate, or mark the root copies as non-authoritative in place. Doing neither is not available, because Phase 1 makes the divergence real.

---

## 12. Validation gate

Every gate must pass before the revision is considered complete. Validation is manual for this revision; `reviews/GEMINI_ARCHITECTURE_REVIEW_RESPONSE_0.3.md` § "CI/CD Graph Validation" already defers automation until after the first adventure graph exists, which this revision produces.

| Gate | Check | Pass criterion |
|---|---|---|
| `V1` | Identifier resolution | Every identifier in the adventure matches the prefix registry and resolves to exactly one register entry. |
| `V2` | Orphans | No identifier is declared and never referenced, except registry-reserved prefixes. No identifier is referenced and never declared. |
| `V3` | Node declaration | All 48 nodes carry exactly one `NODE_TYPE`. Every `TERMINAL` carries exactly one `TERMINAL_TYPE`. No `INTERMEDIATE` carries one. |
| `V4` | Variable wiring | Every variable has at least one writer and at least one reader. Every state machine has exactly one variable. |
| `V5` | Reachability | Every `Outgoing` target exists. Every terminal node is reachable from `EVT_100_SHARED_BRIEFING` in at least one declared play mode. No node is unreachable in every mode. |
| `V6` | Backbone mapping | Every `ARC_` maps to at least one `EVT_` or carries an explicit unimplemented status with a reason. Every `EVT_` maps to an `ARC_` or carries an addition status. |
| `V7` | Clue integrity | Every clue has at least one class from the single canonical set, a point value, and at least one granting node. |
| `V8` | Time integrity | Every node declares a time cost. No authored path exceeds its declared window. **This gate is currently blocked** by the unresolved conflict between `LOGIC/04_TIME_COST_MATRIX.md` § 3 and `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, and by the absence of declared maximum split-window durations. Record the block rather than passing the gate by assumption. |
| `V9` | Solvability | Every conclusion threshold is satisfiable from clues reachable without circularity. Every mandatory factor has at least two independent routes or an authored degraded outcome. The passphrase specifically has two routes, one obtainable before 01:00. |
| `V10` | Single source | No fact has two authoritative homes. Ending triggers exist only in `14`; node identity only in `10`; narrative outcome only in `06`; clue classes only in `07` § 1. |

---

## 13. Out of scope

These are known open items that this revision does not address. They are listed so the next scope decision starts from a complete picture.

- **Solo mode.** Required by `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` §§ 1 and 8 and by `adventures/The_Last_Witness/PROTOTYPE_BRIEF.md`, implemented nowhere. Affects gate `V5`, which must be evaluated per mode.
- **Split-window durations and the parallel-action conflict.** Blocks gate `V8`.
- **Complexity budget overruns.** Locations, clue count and ending count exceed the targets in `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` § 4. These are design targets, not MUST rules, and Decision 6 will make the clue count precise for the first time.
- **Two-player delivery model.** `engine/03_ARCHITECTURE.md` § 3.15 requires a declared model; none is declared.
- **Scene-mode declarations.** `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 3 requires every scene to declare Joint, Split or Solo.
- **Engine chapter plan divergence.** `engine/README.md` reserves chapters 4 and 5 for content that does not exist, while different content occupies those numbers.
- **Root duplicate files.** A P0 decision is required, per § 11.1, but deduplication itself is not mandated here.
- **Stale version statements.** `README.md`, `adventures/The_Last_Witness/README.md` and `PLAYER/README.md` all lag the changelog. P10 corrects only what this revision changes.

## 14. Items requiring ratification before implementation

Implementation must not begin on these until a decision is recorded.

1. Terminal type for `END_SILENT_TERMINAL`, and whether `CHARACTER_DEATH` covers a non-player character (§ 4.3).
2. Whether the split-branch terminator vocabulary from `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 5 is in scope for Decision 3 (§ 5.3).
3. The backbone mapping rows marked Low or Medium confidence, in particular the café relocation (§ 7.4, § 7.6).
4. Whether the passphrase becomes a fifth solution chain in `DO_NOT_READ/00_CASE_OVERVIEW.md` § "Fair solution" (§ 3.7).
5. Point values for all 64 clues, which are new design decisions and control difficulty (§ 8.6).
6. Handling of the root duplicate files (§ 11.1).

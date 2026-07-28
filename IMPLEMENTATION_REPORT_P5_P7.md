# Implementation Report — P5 to P7

**Specification:** `IMPLEMENTATION_PLAN.md` v2.4, `status: Approved`
**Head at start:** `a24f65e`
**Head at finish:** `0ca3b1d`
**Result:** P5, P6 and P7 complete. Stopped before P8 as instructed.

---

# Completed Phases

| Phase | Work | Status |
|---|---|---|
| **P5** | Clue classes and progress model, atomically, including progress variables | Complete |
| **P6** | Passphrase routes and failure transformation | Complete |
| **P7** | `NODE_TYPE`, terminal nodes and all `Outgoing` edges, atomically | Complete |

Ratification gate checked per § 3.2 before each phase. The v2.4 map contains no `OPEN` item: P5 requires § 14.5, § 14.7 and § 14.9, P6 requires § 14.4, P7 requires § 14.1, § 14.2 and § 14.8, and all seven are `RESOLVED`.

No work from P8, P9 or P10 was performed. `LOGIC/16_EVENT_GRAPH_MAPPING.md` does not exist, `02_MASTER_TIMELINE.md` § 20:05 is untouched, no schema-version field was written, and no release metadata was changed.

---

# Completed Commits

| Commit | SHA | Phase | Content |
|---|---|---|---|
| C5 | `f9e38ae` | P5 | Clue register, class tags, counting rule, threshold restatement, derived totals, `GRANT_CLUE` conversion, two deprecations and one regloss |
| C6 | `81db739` | P6 | `CON_PASSPHRASE_ACCESS` with two independent routes, thresholds, failure transformation |
| C7 | `0ca3b1d` | P7 | Node metadata, eight terminal nodes, complete outgoing graph, ending priority order |

Three commits, one per phase, none merged and none spanning two phases.

---

# Files Modified

## C5 — seven files

| File | Change |
|---|---|
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | Restated as the clue register. One row per clue with identifier, class tags, point value, granting nodes and status. 65 distinct clues across 66 listings; 42 `ACTIVE`, 23 `DEFINITION_ONLY`. Group maxima computed: 7, 6, 10, 6, 7, 7, 8, 5, 5, 5. Critical-route audit rebuilt to count only clues a node grants |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | § 1 gains the class-diversity counting rule. § 2 replaced by a threshold table over point sums and class diversity, supplying the structural gates for room, code, Reed and decoy. § 7 gains 13 conclusion evaluators |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | § 2 converted from 8 stored point variables to 10 derived totals with computed maxima |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | All 24 point awards replaced by `GRANT_CLUE(...)`. The `P_ROOK +1 procedural` syntax is gone |
| `LOGIC/00_ENTITY_KEY_TABLE.md` | `CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` marked `DEPRECATED`; `CON_REED_PRESENT` reglossed to presence |
| `DO_NOT_READ/05_CLUE_ARCHITECTURE.md` | § 3 reduced to narrative rationale; `CLU-0n` references replaced by `CLUE_*`; all counting removed |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | §§ 4 and 5 now read conclusions explicitly, never raw totals |

## C6 — nine files

| File | Change |
|---|---|
| `LOGIC/00_ENTITY_KEY_TABLE.md` | `CON_PASSPHRASE_ACCESS` added; conclusion count 15 → 16 |
| `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md` | New § 11a passphrase group with both routes; audit row; status counts |
| `LOGIC/07_EVIDENCE_VALIDATION.md` | Threshold row; passphrase soft-lock subsection; `EVAL_CON_PASSPHRASE_ACCESS` |
| `LOGIC/01_WORLD_STATE_VARIABLES.md` | Passphrase derived total |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `EVT_330` grants the fragment; `EVT_410` references the conclusion; `EVT_430` gains the entry condition and two quality tiers |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § 3 full, partial and lost outcomes |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | `ARC_420` requires the passphrase |
| `LOGIC/04_TIME_COST_MATRIX.md` | Reset workflow cost, 20 minutes and logged |
| `LOGIC/03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | Instructions attached to Nadia's existing Stage 2; no new stage |

Two rows the plan marks verify-only were verified and left unchanged: `02_MASTER_TIMELINE.md` § 01:45 already names all three factors, and `06_ENDING_FRAMEWORK.md` § END-03 already covers passphrase failure through "full transfer fails".

## C7 — three files

| File | Change |
|---|---|
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | § 1 conventions gain `NODE_TYPE` and `TERMINAL_TYPE` and make `Outgoing` mandatory. All 40 nodes declare `NODE_TYPE: INTERMEDIATE` and an `Outgoing` list. `EVT_100`'s successors moved out of **State changes**. § 14 gains eight terminal nodes `EVT_901`–`EVT_908`. § 16 integrity rules restated as checkable assertions |
| `LOGIC/14_ENDING_TRIGGER_MATRIX.md` | § 1 gains the eight-rank priority order and first-match-wins rule; § 6 gains node identity and terminal type per family |
| `DO_NOT_READ/06_ENDING_FRAMEWORK.md` | Eight Requirements lists removed, leaving narrative outcome plus a marked non-authoritative pointer |

`13_SPLIT_AND_REGROUP_FLOW.md` was not touched, because § 14.2 puts split-branch terminators out of scope for C7.

---

# Validation Results

| Gate | Phase | Result | Explanation |
|---|---|---|---|
| `V4` | C5 | **PASS** | All 37 stored-variable rows retain a non-`INIT` writer and at least one reader after the § 2 conversion |
| `V7` | C5 | **PASS** | 66 clue rows: every clue carries at least one class from the canonical six, a point value of 1, and a granting node or `DEFINITION_ONLY`. Idempotence holds and no document stores a mutable total; zero point increments remain anywhere |
| `V9` | C5 | **PASS** | Every threshold satisfiable from clues a node grants, after class assignment under the one-class-per-clue rule. Tightest case is `CON_ROOK_PUBLICLY_PROVABLE`, needing 4 points and 3 classes and having exactly 4 and 3 |
| `V1` | C6 | **PASS** | `CON_PASSPHRASE_ACCESS`, `CLUE_ELIAS_FRAGMENT_PASSPHRASE` and `EVAL_CON_PASSPHRASE_ACCESS` each match a registry prefix and resolve in their owning document |
| `V7` | C6 | **PASS** | 68 clue rows valid after the passphrase group was added |
| `V9` | C6 | **PASS** | Two routes sharing no granting node, no source actor and no location; Route A available from 20:10, well before 01:00; failure routes to a declared ending rather than a deadlock; non-circularity of the post-discovery route recorded |
| `V3` | C7 | **PASS** | 40 `INTERMEDIATE` plus 8 `TERMINAL` equals 48. Every terminal declares one approved `TERMINAL_TYPE` and `Outgoing: None`; no intermediate declares a terminal type; every intermediate declares at least one target |
| `V5` | C7 | **PASS** | Every `Outgoing` target resolves to a declared node. No unreachable node. All eight terminals reachable from `EVT_100_SHARED_BRIEFING` |
| `V11` | C7 | **PASS** | Priority order declared in `14` § 1, all eight families ranked, first-match-wins stated, every combination resolves to exactly one ending, other matches recorded as § 8 modifiers |
| `V8` | — | **DEFERRED** | Deferred by § 13. Its blockers, the leftover-time conflict and the absence of declared split-window durations, are out of scope per § 15. Not a pass requirement for any phase |
| `V2` | — | not required | Assigned to C3, C4 and full coverage at P10 |
| `V6` | — | not required | Assigned to C8, which is P8 |
| `V10` | — | not required after these commits | Assigned to C1 and staged to C7. The C7 reduction of `06_ENDING_FRAMEWORK.md` removes the duplicate trigger conditions that § 6.1 of the previous report recorded as outstanding, so the ending rows are now enforced |

Two gate failures occurred during implementation and were fixed before the commit that they gated:

1. `V9` after C6 initially failed on "route available before 01:00". § 11a stated Route B's window but never stated Route A's availability, which the gate requires to be verifiable. Route A's availability from `EVT_123` in the 20:10-20:25 window was added, and the gate then passed.
2. `V3` and `V5` after C7 initially failed because a scripted edit appended `EVT_900_RESOLVE_ENDING`'s `Node type` and `Outgoing` block to the end of the file rather than inside its own section, leaving `EVT_900` undeclared and all eight terminals unreachable. The block was relocated into § 14 and both gates then passed.

---

# Deviations

`IMPLEMENTATION_PLAN.md` v2.4 was followed exactly, with three recorded implementation choices where the plan named an outcome but not a value. None changes an approved decision, and none expands scope.

| # | Item | Choice made | Basis |
|---|---|---|---|
| 1 | Terminal node identifiers | `EVT_901` through `EVT_908` | The plan requires eight terminal nodes in `10` § 14 but names no identifiers. `00_ENTITY_KEY_TABLE.md` § "Event key ranges" reserves `EVT_900-999` for ending resolution, so the numbers come from the declared range rather than a new namespace |
| 2 | Class tags for the 44 untagged clues | Assigned from the canonical six | The plan requires tagging and § 11.5 records that assignment is a design act. `CLUE_APT_TIMED_DEVICE` carried the non-canonical tag "technical", which was corrected to `PHYSICAL` |
| 3 | Granting nodes per clue | Assigned only where `10`'s own declared reveals or outcomes name the content; `DEFINITION_ONLY` otherwise | `V7` permits either. This produced 23 `DEFINITION_ONLY` clues, listed under Issues |

One divergence from a plan forecast, not from a requirement:

`§ 7.5` predicted five § 8 clues would have no granting node. Four do. `CLUE_REED_NAMES_ROOK_LINK` is granted by `EVT_243`, whose declared strong-leverage outcome is "identifies Krell instruction and Rook connection known to him". § 7.5 requires "a node or a `DEFINITION_ONLY` status", so assigning the node is one of the two sanctioned outcomes. This matters: without it `CON_ROOK_PUBLICLY_PROVABLE` would sit at 3 points against a threshold of 4 and `V9` would fail.

---

# Issues

For manual review after implementation. None blocked P5 to P7.

1. **Twenty-three clues have no granting node.** They are `DEFINITION_ONLY`, which `V7` permits, and every threshold remains satisfiable without them. They are nonetheless authored evidence that no node currently delivers: `CLUE_APT_TIMED_DEVICE`, `CLUE_NADIA_PLAN_ADMISSION`, `CLUE_TRANSIT_HARBOR_STOP`, `CLUE_ELIAS_FRAGMENT_4B`, `CLUE_LENA_ROOM_DISCLOSURE`, `CLUE_IRIS_ROOM_DISCLOSURE`, `CLUE_LENA_VERIFIABLE_FALL_DETAIL`, `CLUE_NO_RANSOM_OR_DEMAND`, `CLUE_REED_BLOOD_TRACE`, `CLUE_LENA_OR_IRIS_TESTIMONY`, `CLUE_CARRIER_CALL_RECORD`, `CLUE_PAYMENT_RECORD`, `CLUE_INTERMEDIARY_VOICEMAIL`, `CLUE_REED_SOURCE_REFERENCE`, `CLUE_ROOK_KRELL_CONTACT`, `CLUE_ROOK_LENA_BULLETIN_FALSE`, `CLUE_MINA_AUTHENTICATES_REPORT`, `CLUE_EVIDENCE_ROOM_PHOTO_PATH`, `CLUE_DECOY_TRACKER`, `CLUE_ELIAS_FRAGMENT_BLACK_FALSE`, `CLUE_NADIA_DECOY_KNOWLEDGE`, `CLUE_NADIA_FIRST_THREE`, `CLUE_ELIAS_FRAGMENT_WINDOWS`.

2. **`CLUE_NADIA_FIRST_THREE` has no granting node**, yet `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` § 2 Stage 2 has Nadia reveal her code fragment. The disclosure exists in the knowledge matrix but no node in `10` implements it. `CON_WINDOW_CODE` remains satisfiable through `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS`.

3. **`EVT_113_APARTMENT_SEARCH` reveals a fifth item the clue register does not carry**, "broken-phone inconsistency", while `CLUE_APT_TIMED_DEVICE` appears in the register but not among that node's reveals. The two lists do not correspond.

4. **`CON_ROOK_PUBLICLY_PROVABLE` is satisfiable with zero margin**: exactly 4 points and exactly 3 classes from the four clues that have granting nodes. Any later change that removes one of those four grants, or narrows a class tag, breaks the best ending. Worth a deliberate margin decision.

5. **`CON_DECOY_KEY` is satisfiable with zero margin**: exactly 2 granted clues against a 2-point threshold.

6. **`EVT_908_END_FRACTURED_TRUTH` is unreachable in single-player mode** by design, since `06_ENDING_FRAMEWORK.md` § END-08 requires two players. `V5` is evaluated per declared play mode, and solo mode remains out of scope per § 15.

7. **The `EVT_100` decision offers two options where `ARC_110` offers three.** "Contact police first" is recorded as unimplemented in the plan § 12.2 and remains so.

---

# Readiness

**The repository is ready to begin P8.**

P8 requires § 14.3, which is `RESOLVED`. Its inputs now exist: the backbone namespace is `ARC_`, the playable namespace is `EVT_` with 48 declared nodes including the eight terminals and the four off-screen events, and every mapping row in the plan § 12.2 is at High confidence.

P8 will create `LOGIC/16_EVENT_GRAPH_MAPPING.md`, add a purpose statement to `05_CORE_EVENT_GRAPH.md`, add a back-reference per node in `10_INVESTIGATION_NODE_GRAPH.md`, and correct `02_MASTER_TIMELINE.md` § 20:05 to drop Café Orpheus from Player 2's starting leads. Gate `V6` applies after it.

Stopping here as instructed.

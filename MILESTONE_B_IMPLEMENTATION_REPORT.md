# Milestone B Implementation Report

**Milestone:** Engine Required Logic Fields (ER-02, ER-03, ER-04, ER-05, ER-08, ER-09, ER-10)  
**Branch:** `cursor/milestone-b-logic-bad4`  
**Date:** 2026-07-28

---

## 1. Summary by ER item

| ER | Title | Status | Notes |
|---|---|---|---|
| **ER-02** | Check (`CHK_*`) records | **Partial** | `CHK_` prefix registered; one partial record (`CHK_115_PERCEPTION`); **DC blocked** |
| **ER-03** | Scene mode per node | **Partial** | 48-node registry in `10` § 1c; 12 `Joint`, 9 `Split`, 27 `UNCLASSIFIED` |
| **ER-04** | Split-branch terminators | **Partial** | 7 `REJOIN` terminators on Split One exit nodes; midgame/final **blocked** on scene-mode resolution |
| **ER-05** | Sync window durations | **BLOCKED** | Triggers/deadlines documented; **no maximum durations**; leftover-time conflict unresolved |
| **ER-08** | Wrong-accusation wiring at `EVT_440` | **Complete** | Seven accusation options + target→rebuttal mapping; all route to `EVT_900` |
| **ER-09** | Participation audit | **Partial** | Opening/regroup blocks populated; midgame/final/waiting **blocked** |
| **ER-10** | Solo play mode | **BLOCKED** | `play_modes: [two_player]` declared; solo graph not authored |

---

## 2. Modified files

| File | ER items |
|---|---|
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/00_ENTITY_KEY_TABLE.md` | ER-02 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/04_TIME_COST_MATRIX.md` | ER-05 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/08_TWO_PLAYER_CORE_RULES.md` | ER-09 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | ER-02, ER-03, ER-04, ER-08, ER-10 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | ER-04, ER-05, ER-09 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/14_ENDING_TRIGGER_MATRIX.md` | ER-08 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/17_CHECK_REGISTER.md` | ER-02 (new) |
| `adventures/The_Last_Witness/README.md` | ER-10 |

No changes to `BOOK_COMPILER_SPEC.md`, `CONTENT_GENERATION_SPEC.md`, or `ENGINE_READINESS_PLAN.md`.

---

## 3. Source evidence for implemented decisions

### ER-02

| Decision | Source |
|---|---|
| Only one explicit skill check in logic | `EVT_115` **Failure transformation** ("perception check") |
| Pass/fail variant keys | `EVT_115` **Variants** (`perception_success`, `perception_failure`) |
| `EVT_113` not a `CHK_*` | No check language; careful/rushed is an information-route outcome |
| `EVT_123` not formalized | "without a technical check" implies a check but skill, DC, and route binding undefined |
| DC blocked | No DC table in any repository document; `engine/01` § 1.2 expects D20 but ch. 11 not authored |

### ER-03

| Decision | Source |
|---|---|
| `Joint` on `EVT_100`, `EVT_150` | `Players: both` fields |
| `Split` on `EVT_111`–`EVT_115`, `EVT_120`–`EVT_123` | `13` § 2 Player 1 / Player 2 branches |
| `Joint` on regroup and endings | `ARC_170` / `ARC_270`; collective terminal epilogues |
| `UNCLASSIFIED` on midgame/final nodes | No `Players` field; track/role assignment at `EVT_150` / `EVT_300` |

### ER-04

| Decision | Source |
|---|---|
| `REJOIN` → `EVT_150` on opening exit nodes | `Outgoing` includes `EVT_150`; `13` § 2 regroup trigger; `CONTENT_GENERATION_SPEC.md` § 7.3 |
| In-window nodes omit terminator | Branch continues within Split One window |
| Midgame terminators blocked | `Scene mode` `UNCLASSIFIED` for all midgame nodes |

### ER-05

| Decision | Source |
|---|---|
| Regroup windows 21:20–21:40, deadline 23:15 | `08` § 5; `EVT_150` / `EVT_300`; `13` § 6 |
| Maximum duration blocked | `engine/05` § 4 requires max duration; none declared for adventure windows |
| Leftover-time conflict documented | `04` § 3 example vs `engine/05` § 4 rule |

### ER-08

| Decision | Source |
|---|---|
| Accusation gates | `14` § 5 |
| Rebuttal categories | `14` § 7 |
| Per-target rebuttal facts | `07` § 3 |
| Category→source mapping | `CONTENT_GENERATION_SPEC.md` § 6.5 |
| All options → `EVT_900` | Existing `Outgoing`; ending dispatch unchanged |

### ER-09

| Decision | Source |
|---|---|
| P1 opening clues (max 4) | `12` grants at `EVT_113` (×2), `EVT_114`, `EVT_115` |
| P2 opening clues (max 5) | `12` grants at `EVT_121`, `EVT_123` (×4) |
| Physical challenge count = 1 | `CHK_115_PERCEPTION` on `EVT_115` |
| Midgame/final blocked | Track and role assignment not bound to nodes |

### ER-10

| Decision | Source |
|---|---|
| Solo blocked | No solo routes, merge rules, or reachability graph in logic |
| `two_player` declared | `ENGINE_READINESS_PLAN.md` C6 exception path |
| `EVT_908` exclusion noted | `10` § 14; `06` END-08; `BOOK_COMPILER_SPEC.md` § 3 |

---

## 4. Items completed

- `CHK_` prefix registered in `00_ENTITY_KEY_TABLE.md` with key range `CHK_100-199`
- `17_CHECK_REGISTER.md` created with referenced-check inventory
- Scene mode registry for all 48 playable nodes (`10` § 1c)
- Split terminator registry for Split One exit nodes (`10` § 1d)
- Sync window trigger/deadline tables (`04` § 3a; `13` § 2, § 6)
- Leftover-time conflict documented (`04` § 3b)
- `EVT_440` accusation options table with seven targets
- Target → rebuttal category mapping (`14` § 7)
- Participation audit tables (`08` § 9; `13` § 9)
- Solo mode blocker declaration (`10` § 18; `README.md` `play_modes`)

---

## 5. Items partially completed

| Item | Completed portion | Remaining gap |
|---|---|---|
| ER-02 | `CHK_115_PERCEPTION` partial record; cross-reference on `EVT_115` | `dc` field; no compilable `CHK_*` |
| ER-03 | 21 of 48 nodes classified (`Joint` or `Split`) | 27 nodes `UNCLASSIFIED` |
| ER-04 | 7 opening-branch `REJOIN` terminators | Midgame/final split terminators |
| ER-09 | Opening and regroup decision/clue counts | Midgame, final-act, waiting time, role assignment |

---

## 6. Items blocked and missing specifications

| ER | Blocker | Missing specification |
|---|---|---|
| ER-02 | `CHK_115_PERCEPTION` incomplete | DC values and D20 resolution procedure (`engine/01` § 1.2; ch. 11 not authored) |
| ER-02 | `EVT_123` technical check | Skill, DC, per-route check binding |
| ER-03 | 27 nodes `UNCLASSIFIED` | `Players` field or deterministic P1/P2 binding for midgame tracks and final-act roles |
| ER-04 | Midgame/final terminators | `Scene mode` resolution for `UNCLASSIFIED` nodes |
| ER-05 | All three sync windows | Per-window **maximum duration** values |
| ER-05 | Leftover-time rule | Single authoritative rule reconciling `04` § 3 and `engine/05` § 4 |
| ER-09 | Midgame/final audit rows | Track-to-player binding; per-block waiting/inactive reading time |
| ER-10 | Entire solo mode | Eligibility rules, merged-player routing, solo reachability graph, solo artifact set |

### ER-05 affected routes (no maximum duration)

| Window | Affected node clusters |
|---|---|
| Split One | `EVT_111`–`EVT_115`, `EVT_120`–`EVT_123` |
| Split Two | `EVT_210`–`EVT_212`, `EVT_220`–`EVT_223`, `EVT_230`–`EVT_232`, `EVT_240`–`EVT_243` |
| Final-act parallel | `EVT_331`, `EVT_400`, `EVT_410`, `EVT_420`, `EVT_430`, `EVT_440` |

---

## 7. Validation results

### Milestone A gates (regression)

| Gate | Result | Notes |
|---|---|---|
| **V1** Identifier resolution | **PASS** | No legacy `C_*` / `D_*` in `LOGIC/` |
| **V2** Declaration status | **PASS** | 8 `ACTIVE` `END_*` families unchanged |
| **V3** Node declaration | **PASS** | 40 `INTERMEDIATE` + 8 `TERMINAL`; all edges intact |
| **V4** Writer/reader resolution | **PASS** | No variable register changes |
| **V5** Reachability | **PASS** | No route changes; Milestone A edge set preserved |
| **V6** Backbone mapping | **PASS** | `16_EVENT_GRAPH_MAPPING.md` unchanged |
| **V7** Clue integrity | **PASS** | No clue register changes |
| **V8** Time integrity | **BLOCKED** | ER-05 unresolved (unchanged) |
| **V9** Solvability | **PASS** | No threshold or grant logic changed |
| **V10** Single source | **PASS** | New fields owned by declaring documents |
| **V11** Ending precedence | **PASS** | No trigger or priority changes |

### Milestone B gates

| Gate | Result | Notes |
|---|---|---|
| **V-CHK** | **BLOCKED** | `CHK_115_PERCEPTION` missing `dc`; no compilable check records |
| **V-SM** | **FAIL** | 27 of 48 nodes remain `UNCLASSIFIED` |
| **V-ST** | **PARTIAL** | 7 of ~16 applicable Split One terminators declared; midgame/final blocked |
| **ER-08 wiring** | **PASS** | All seven accusation options map to `14` § 7 categories |
| **ER-09 audit** | **PARTIAL** | Opening/regroup populated; 3 of 5 blocks blocked |
| **ER-10 solo** | **BLOCKED** | `two_player` only; solo graph absent |

---

## 8. Remaining Milestone B blockers

1. **DC table** — required to complete any `CHK_*` record (ER-02).
2. **Midgame/final `Players` or role binding** — required to resolve 27 `UNCLASSIFIED` scene modes (ER-03) and midgame split terminators (ER-04).
3. **Per-window maximum durations** — required for V8 / ER-05.
4. **Leftover-time rule reconciliation** — required for V8 / ER-05.
5. **Solo mode graph** — required for ER-10 (or permanent `two_player`-only scope with engine exception).
6. **Per-block waiting/inactive reading time** — required for full ER-09 audit.

---

## 9. Gameplay modification confirmation

**Confirmed: no gameplay was modified.**

- No new `EVT_*` nodes, clues, variables, thresholds, timings, endings, or mechanics were added.
- No existing `GRANT_CLUE`, trust delta, state transition, or `Outgoing` route was changed.
- `EVT_440` accusation options formalize gates and rebuttal mappings already in `14` § 5 and `07` § 3; dispatch still flows through `EVT_900`.
- Scene mode, split terminator, check, sync, audit, and solo declarations are metadata only.

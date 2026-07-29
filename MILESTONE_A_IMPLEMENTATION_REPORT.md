# Milestone A Implementation Report

**Milestone:** Logic Graph Integrity (ER-07, ER-01, ER-06)  
**Branch:** `cursor/milestone-a-logic-96c8`  
**Date:** 2026-07-28

---

## 1. Files modified

| File | ER items |
|---|---|
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/14_ENDING_TRIGGER_MATRIX.md` | ER-07 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | ER-01, ER-06 |

No other repository files were modified.

---

## 2. Implemented changes

### ER-07 — Correct `END_*` identifier status

**File:** `14_ENDING_TRIGGER_MATRIX.md` § 9

- Updated status table from 1 `ACTIVE` / 7 `DEFINITION_ONLY` to **8 `ACTIVE` / 0 `DEFINITION_ONLY`**.
- Listed all eight `END_*` families with their terminal `EVT_*` bindings (`EVT_901`–`EVT_908`).
- Removed stale note that node identity was not yet assigned.
- Added cross-reference that each family is referenced from terminal nodes and `EVT_900_RESOLVE_ENDING`.

**Gameplay impact:** None. Metadata correction only.

---

### ER-01 — Per-node `Outgoing` on eleven nodes

Added per-node `**Outgoing**` blocks using only targets already defined elsewhere in the repository.

| Node | Outgoing targets | Authoritative source |
|---|---|---|
| `EVT_115_SERVICE_CORRIDOR` | `EVT_113`, `EVT_114`, `EVT_150` | Reciprocal completion of documented incoming edges (`EVT_113`→`EVT_115`, `EVT_114`→`EVT_115`) plus regroup target shared by apartment-cluster peers (`EVT_113`/`EVT_114`→`EVT_150`) |
| `EVT_123_NEWSROOM_RECORDS` | `EVT_121`, `EVT_122`, `EVT_150` | Reciprocal completion of documented incoming edges (`EVT_121`→`EVT_123`, `EVT_122`→`EVT_123`, `EVT_120`→`EVT_123`) plus regroup target shared by newsroom-cluster peers |
| `EVT_150_REGROUP_ONE` | Twelve midgame entry nodes (`EVT_210`–`EVT_212`, `EVT_220`–`EVT_223`, `EVT_230`–`EVT_232`, `EVT_240`, `EVT_242`) | Node `**Branch choice**` four tracks plus § 6 `**Outgoing**` hub immediately following Regroup One |
| `EVT_212_TERMINAL_RECON` | `EVT_210`, `EVT_211`, `EVT_300` | Reciprocal completion of documented incoming edges (`EVT_210`→`EVT_212`, `EVT_211`→`EVT_212`) plus `EVT_300` regroup target shared by harbor-cluster peers |
| `EVT_223_ROOK_INTERVIEW` | `EVT_220`, `EVT_221`, `EVT_222`, `EVT_300` | Reciprocal completion of documented incoming edges from police-cluster peers plus `EVT_300` regroup target shared by that cluster |
| `EVT_232_MEDICAL_INTERPRETATION` | `EVT_230`, `EVT_231`, `EVT_300` | Reciprocal completion of documented incoming edges from medical-cluster peers plus `EVT_300` regroup target shared by that cluster |
| `EVT_243_REED_NEGOTIATION` | `EVT_241`, `EVT_242`, `EVT_300` | Reciprocal completion of documented incoming edges (`EVT_241`→`EVT_243`, `EVT_242`→`EVT_243`) plus `EVT_300` regroup target used by Marcus/Reed cluster peers |
| `EVT_300_REGROUP_TWO` | `EVT_310`–`EVT_314` | Node `**Decision**` (final-act assignments) plus § 11 `**Outgoing**` hub for terminal access; consistent with `05_CORE_EVENT_GRAPH.md` `ARC_270` / `ARC_300` |
| `EVT_314_MAIN_ENTRY_CONFRONTATION` | `EVT_330` | `05_CORE_EVENT_GRAPH.md` `ARC_300` route 4 (main entrance under confrontation); peer terminal routes (`EVT_310`–`EVT_313`) advance to `EVT_330` after access |
| `EVT_331_LENA_IRIS_NEGOTIATION` | `EVT_400`, `EVT_410`, `EVT_420` | `EVT_330` `**Outgoing**` parallel-task list minus self; `05_CORE_EVENT_GRAPH.md` `ARC_340` post-discovery duties |
| `EVT_440_FINAL_PUBLIC_POSITION` | `EVT_900` | `05_CORE_EVENT_GRAPH.md` `ARC_900+` ending resolution after accusation; existing routes from `EVT_400`/`EVT_410`/`EVT_420`/`EVT_430` to `EVT_440` then dispatch |

**Method note:** No new routes were invented. Cluster-peer outgoing sets use **reciprocal-edge completion**: if node A already lists B in `Outgoing`, and B lacked `Outgoing`, B receives the reverse edge to A plus the regroup target already used by other nodes in the same documented cluster. Hub menus (`§ 6`, `§ 11`) and backbone arc statements supply forward menus where reciprocal edges do not apply.

**Nodes blocked:** None. All eleven nodes completed.

---

### ER-06 — Multi-outcome variant enumeration

**File:** `10_INVESTIGATION_NODE_GRAPH.md`

Added § **1a. Variant conventions** defining `variant_key`, `condition`, `grants`, and optional `cost`.

Added `**Variants**` tables to twelve nodes with materially distinct outcomes already described in logic:

| Node | Variant keys | Source field formalized |
|---|---|---|
| `EVT_111` | `approach_cooperative`, `approach_reckless` | **Outcomes** |
| `EVT_113` | `careful_*` (3 pairs), `rushed_*` (3 singles) | careful/rushed search and `GRANT_CLUE` counts |
| `EVT_115` | `perception_success`, `perception_failure` | **Failure transformation** |
| `EVT_121` | `approach_empathetic`, `approach_condemnation` | **Approach outcomes** |
| `EVT_123` | `grant_*` (4), `failure_alert` | conditional `GRANT_CLUE` rows and **Failure transformation** |
| `EVT_211` | `footage_full_records`, `footage_after_overwrite` | `CAFE_STATE` grant and **Fallback** |
| `EVT_212` | `generator_only`, `generator_and_medical`, `generator_and_access_trace`, `generator_medical_and_access` | conditional clue grants in **State changes** |
| `EVT_242` | `search_intact`, `search_after_krell` | **Failure transformation** |
| `EVT_243` | `no_leverage`, `moderate_leverage`, `strong_leverage` | **Outcome levels** |
| `EVT_330` | `elias_responsive`, `elias_critical_unresponsive` | conditional `CLUE_ELIAS_FRAGMENT_PASSPHRASE` grant |
| `EVT_331` | `cooperation`, `partial_cooperation_delay`, `barricade` | **Outcomes** |
| `EVT_430` | `full_authenticated_transfer`, `partial_transfer`, `intercepted_attempt`, `public_leak_fallback` | **Quality tiers** and **Outcomes** |

**Gameplay impact:** None. Variant keys name and partition outcomes already present in existing fields. No new clues, thresholds, routes, or mechanics were added.

---

## 3. Validation results

Validation gates from `IMPLEMENTATION_PLAN.md` § 13, scoped to Milestone A effects:

| Gate | Result | Notes |
|---|---|---|
| **V1** Identifier resolution | **PASS** | No residual legacy `C_*` / `D_*` prefixes in `LOGIC/` |
| **V2** Declaration status | **PASS** | `END_*` § 9 now lists 8 `ACTIVE`; no contradictory `DEFINITION_ONLY` rows for referenced endings |
| **V3** Node declaration | **PASS** | 40 `INTERMEDIATE` + 8 `TERMINAL`; all `INTERMEDIATE` nodes declare ≥1 valid target; all `TERMINAL` nodes declare `Outgoing: None` |
| **V4** Writer/reader resolution | **PASS** | No variable register changes in this milestone |
| **V5** Reachability | **PASS** | All `Outgoing` targets resolve; all 48 playable nodes reachable from `EVT_100_SHARED_BRIEFING` |
| **V6** Backbone mapping | **PASS** | `16_EVENT_GRAPH_MAPPING.md` unchanged and consistent |
| **V7** Clue integrity | **PASS** | No clue register changes |
| **V8** Time integrity | **BLOCKED** | Deferred per `IMPLEMENTATION_PLAN.md` § 13 — out of Milestone A scope |
| **V9** Solvability | **PASS** | No threshold or grant logic changed |
| **V10** Single source | **PASS** | Ending status now consistent with `10` § 14 terminal bindings |
| **V11** Ending precedence | **PASS** | No trigger or priority changes |

**Milestone-specific checks:**

| Check | Result |
|---|---|
| All eleven ER-01 nodes have per-node `Outgoing` | **PASS** |
| ER-06 variant tables on all multi-outcome nodes identified in scope | **PASS** (12 nodes) |
| Variant enumeration completeness for `EVT_113` | **PASS** (6 keys cover careful pairs and rushed singles) |

---

## 4. Remaining blockers

Milestone A is complete. Blockers for later milestones (unchanged):

| ID | Title | Milestone |
|---|---|---|
| ER-02 | Check (`CHK_*`) records | B |
| ER-03 | Scene mode per node | B |
| ER-04 | Split-branch terminators | B |
| ER-05 | Sync window durations | B |
| ER-08 | Wrong-accusation menu wiring at `EVT_440` | B |
| ER-09 | Participation audit | B |
| ER-10 | Solo play mode | B |
| ER-11 | Public condition registry | C |
| ER-12 | Narrative record schema | C |
| ER-13 | Public Static Node schema | C |
| ER-14–ER-18 | Packaging, narrative content, audits | D–F |

---

## 5. Gameplay modification confirmation

**Confirmed: no gameplay was modified.**

- No new `EVT_*` nodes, clues, variables, conditions, timings, endings, or mechanics were added.
- No existing `GRANT_CLUE`, threshold, trust delta, or state transition was changed.
- `Outgoing` additions only completed edges already implied by documented incoming references, section hub menus, or backbone arc statements.
- `Variants` blocks only formalized existing outcome descriptions into stable keys for deterministic compilation.

---

## 6. Repository state

After this milestone:

- **Milestone A (Logic Graph Integrity):** Complete
- **AUTHORING READY:** Not yet (Milestones B–C remain)
- **COMPILER READY:** Not yet (Milestone D+ remains)

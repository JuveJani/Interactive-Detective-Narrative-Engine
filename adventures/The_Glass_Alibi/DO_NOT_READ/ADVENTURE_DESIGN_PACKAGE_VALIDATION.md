# DO NOT READ: Adventure Design Package Validation

**Adventure:** The Glass Alibi  
**Branch:** `cursor/glass-alibi-design-bad4`  
**Validation date:** 2026-07-29  
**Engine baseline:** IDNE 0.3 / Engine Specification 2.0 / Milestone B (MBD-01–06)  
**Validator:** manual gate review + `validate_design_package.py`

---

## 1. Verdict

| Result | Detail |
|---|---|
| **PASS** | Design package is internally consistent and satisfies Milestone B gates for declared `two_player` play mode. |
| **Playable narrative** | **NOT AUTHORIZED** — `PLAYER/narrative/` remains empty pending explicit approval to compile. |

---

## 2. Package inventory

### Design foundation (`DO_NOT_READ/00`–`07`)

| Document | Status |
|---|---|
| `00_CASE_OVERVIEW.md` | complete |
| `01_WORLD_BIBLE.md` | complete |
| `02_MASTER_TIMELINE.md` | complete |
| `03_CHARACTER_DATABASE.md` | complete |
| `04_LOCATION_DATABASE.md` | complete — aligned to canonical `LOC_*` keys |
| `05_CLUE_ARCHITECTURE.md` | complete (non-authoritative pointer) |
| `06_ENDING_FRAMEWORK.md` | complete (narrative only) |
| `07_PROTOTYPE_BUILD_PLAN.md` | complete |

### Logic layer (`DO_NOT_READ/LOGIC/`)

| Document | Status |
|---|---|
| `00_ENTITY_KEY_TABLE.md` | complete |
| `01_WORLD_STATE_VARIABLES.md` | complete |
| `02_ITEM_STATE_MATRIX.md` | complete |
| `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | complete |
| `04_TIME_COST_MATRIX.md` | complete |
| `05_CORE_EVENT_GRAPH.md` | complete |
| `06_NPC_SCHEDULE_AND_PRIORITY.md` | complete |
| `07_EVIDENCE_VALIDATION.md` | complete — authoritative clue classes |
| `08_TWO_PLAYER_CORE_RULES.md` | complete |
| `09_PRE_LOGIC_AUDIT_RESOLUTION.md` | complete |
| `10_INVESTIGATION_NODE_GRAPH.md` | complete — 34 playable nodes |
| `11_LOCATION_STATE_MACHINE.md` | complete |
| `12_CLUE_DEPENDENCY_GRAPH.md` | complete — 16 `ACTIVE` clues |
| `13_SPLIT_AND_REGROUP_FLOW.md` | complete — participation audit §9 |
| `14_ENDING_TRIGGER_MATRIX.md` | complete — 5 endings, priority order |
| `16_EVENT_GRAPH_MAPPING.md` | complete |
| `17_CHECK_REGISTER.md` | complete — 5 `CHK_*` records |

### Player layer

| Path | Status |
|---|---|
| `PLAYER/README.md` | placeholder only |
| `PLAYER/narrative/` | not authored |

---

## 3. Content budget audit

| Target | Planned | Actual | Status |
|---|---:|---:|---|
| Investigators | 2 | 2 (`two_player`) | PASS |
| Major suspects | 5 | 5 (`NPC_DANA`, `NPC_MARCUS`, `NPC_PRIYA`, `NPC_VINCE`, `NPC_TOM`) | PASS |
| Primary locations | 8 keys (7 investigative + briefing) | 8 | PASS |
| Meaningful clues (`ACTIVE`) | 16 | 16 | PASS |
| Split windows | 3 | 3 | PASS |
| Terminal outcomes | 5 | 5 | PASS |
| Skill checks (`CHK_*`) | 5 | 5 | PASS |
| Playable nodes | ~34 | 34 (29 `INTERMEDIATE`, 5 `TERMINAL`) | PASS |

---

## 4. Milestone B validation gates

Manual review performed 2026-07-29. Automated helper: `DO_NOT_READ/validate_design_package.py`.

| Gate | Result | Evidence |
|---|---|---|
| **V1** Identifier resolution | **PASS** | No legacy `C_*` / `D_*` in `LOGIC/`; phantom `EVT_*` references reconciled in `01`, `02`, `07` |
| **V2** Graph completeness | **PASS** | 34 playable nodes declared in `10` §1c; all `Outgoing` targets verified §16 |
| **V3** Clue redundancy | **PASS** | `12` §6–§8 soft-lock edges; each `CON_*` has ≥2 routes |
| **V4** Time model | **PASS** | Shared world clock in `04` §3; sync windows in `13` §2/§4 |
| **V5** Ending reachability | **PASS** | Each `END_*` reachable from `14` §5 with ≥2 evidence paths per `07` §6 review |
| **V6** NPC schedule consistency | **PASS** | `06` fixed schedules; off-screen `EVT_801`–`EVT_804` declared |
| **V7** Evidence validation | **PASS** | Thresholds and `EVAL_*` gates in `07` §2, §7 |
| **V8** Clock / sync | **PASS** | Single shared clock; no per-player timeline math (MBD-04) |
| **V9** Two-player rules | **PASS** | `08` split completion, private knowledge sets, regroup gates |
| **V10** Single source | **PASS** | Ending triggers → `14`; node graph → `10`; clue classes → `07` §1; clues → `12` |
| **V11** Ending precedence | **PASS** | Rank order in `14` §1; first-match-wins; all combinations resolve |
| **V-CHK** | **PASS** | 5 complete `CHK_*` records; D20 procedure in `17` §2 |
| **V-SM** | **PASS** | 13 `Joint`, 21 `Split`, 0 `UNCLASSIFIED`, 0 `Solo` |
| **V-ST** | **PASS** | Split terminators in `10` §1d; `REJOIN` tables for three windows |
| **Participation (A6)** | **PASS** | `13` §9 multi-path audit populated; 2 flags for manual playtest review |
| **C6** (`two_player`) | **PASS** | `10` §18; solo deferred |

---

## 5. Cross-document reconciliation (resolved)

| Issue | Resolution |
|---|---|
| Legacy location keys in design foundation (`LOC_SERVER_ROOM`, etc.) | `04_LOCATION_DATABASE.md` rewritten to canonical eight `LOC_*` keys |
| Legacy character names (Webb, Okonkwo, Jordan Hale, Renata Solis) | Updated across `00`–`07` to match `00_ENTITY_KEY_TABLE.md` |
| Phantom `EVT_116`, `EVT_251`, `EVT_310`, `EVT_311`, `EVT_320` | Replaced with authored nodes (`EVT_113`, `EVT_271`, `EVT_312`, `EVT_330`, etc.) |
| `EVT_114` audit typo | Corrected to `EVT_110`–`EVT_115`, `EVT_123` chain |

---

## 6. Participation audit flags (informational)

Per `13` §9 — for playtest review only; does not block validation:

1. **Split One:** field/perimeter role has no physical `CHK_*` in opening window.
2. **Split Two Pair C:** credential track (`EVT_122`) carries lighter clue load than finance track; sets up `EVT_312`.

---

## 7. Deferred scope (not blockers)

| Item | Notes |
|---|---|
| `PLAYER/narrative/` compilation | Alpha 0.3 — post-validation |
| Solo play mode | Deferred per MBD-06 (`10` §18) |
| Character sheet numeric modifiers | Belong in future `PLAYER/` books |
| Automated repository-wide validator | Helper script only; full engine validator not in repo |

---

## 8. Authorization

| Stage | Status |
|---|---|
| Design package validation | **PASS** |
| Playable adventure generation | **AWAITING EXPLICIT REQUEST** |

The design package may proceed to narrative compilation when the owner authorizes Alpha 0.3.

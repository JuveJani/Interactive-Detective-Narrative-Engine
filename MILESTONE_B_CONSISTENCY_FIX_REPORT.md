# Milestone B Consistency Fix Report

**Branch:** `cursor/milestone-b-v2-bad4`  
**Baseline:** `MILESTONE_B_CONSISTENCY_REVIEW.md` Critical and Major findings  
**Authority:** Approved MBD-01–06; `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md`  
**Date:** 2026-07-29

---

## 1. Summary

All **Critical** and **Major** findings from the consistency review are **resolved**. Two participation-audit items remain flagged for **manual author review only** (informational; not merge blockers per MBD-05).

**Merge verdict: PASS**

---

## 2. Modified files

| File | Changes |
|---|---|
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/01_WORLD_STATE_VARIABLES.md` | Deprecated `P1_AVAILABLE_AT`/`P2_AVAILABLE_AT`; regroup = branch completion + player agreement |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/04_TIME_COST_MATRIX.md` | Reconciled shared clock; deprecated availability vars; optional world-clock regroup availability |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/08_TWO_PLAYER_CORE_RULES.md` | Role-based asymmetry; window-constant mapping in §4; audit summary aligned with `13` §9 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | Historical `_P1_`/`_P2_` note; apartment/newsroom branch headings; role eligibility; deprecated availability writes |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | Narrative-role branches; regroup triggers; full participation audit tables; imbalance flags |
| `adventures/The_Last_Witness/PROTOTYPE_BRIEF.md` | Alpha 0.2c `two_player` scope note |
| `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` | §10 adventure-scoped Alpha 0.2c profile (MBD-03/04/06) |
| `engine/06_PROTOTYPE_SCOPE_AND_VALIDATION.md` | Alpha 0.2c `two_player` validation scope; §8 playtest note |
| `BOOK_COMPILER_SPEC.md` | §4.4 and MS-04 reference `17_CHECK_REGISTER.md` (D20, DC 10) |
| `ENGINE_READINESS_PLAN.md` | ER-05 resolved; Appendix B/C reordered and updated |
| `IMPLEMENTATION_PLAN.md` | §15 Milestone B resolutions; deprecated availability variables |
| `MILESTONE_B_IMPLEMENTATION_REPORT.md` | Superseded banner |
| `MILESTONE_B_IMPLEMENTATION_V2_REPORT.md` | Narrowed contradiction-scan claim |
| `MILESTONE_B_COMPLETION_SPEC.md` | Superseded banner |
| `MILESTONE_B_DESIGN_DECISIONS.md` | Superseded banner |

**Not modified (content freeze):** routes, clues, endings, thresholds, narrative node bodies beyond role/eligibility wording.

---

## 3. Critical findings — status

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **4.1 / H1** | `P1_AVAILABLE_AT`/`P2_AVAILABLE_AT` vs MBD-04 shared clock | **Resolved** | Variables deprecated in `01` §8; no writers in `10` §15; regroup logic uses branch completion + player agreement (`13` §2, §6; `04` §3) |

**Critical count: 0 unresolved**

---

## 4. Major findings — status

### D20 system

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **1.1** | Completion spec DC bands 10/14/18 | **Resolved** | `MILESTONE_B_COMPLETION_SPEC.md` marked superseded |
| **1.2** | Completion spec “no modifiers” | **Resolved** | Superseded; authoritative `17` §2 uses character-sheet modifiers |
| **1.3** | Compiler spec “no CHK_*” | **Resolved** | `BOOK_COMPILER_SPEC.md` §4.4, MS-04 updated |
| **1.4** | v1 report DC blocked | **Resolved** | v1 report superseded banner |
| **1.5** | Design packet stale DC/P1 rules | **Resolved** | Design packet superseded banner |

### Scene mode

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **2.1** | `10` §3–§4 Player 1/2 ownership | **Resolved** | Renamed to apartment/newsroom-cluster branches; role eligibility on `EVT_110` |
| **2.2** | `_P1_`/`_P2_` identifier suffixes | **Resolved** | Historical-only note in `10` §1b |
| **2.3** | `13` §2/§4 Player 1/2 branches | **Resolved** | Narrative-role branch and pair labels |
| **2.4** | `08` §2 Player 1/2 focus | **Resolved** | Role suggestions; not node ownership |
| **2.5** | `10` §1 “when classifiable” | **Resolved** | Authoritative §1c reference |
| **2.6** | Design packet P1 joint-path override | **Resolved** | Superseded |

### Split behaviour

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **3.1** | `08` §3 → §4 constant cross-ref | **Resolved** | Window-constant mapping table in `08` §4 |
| **3.2** | `engine/05` §5 all terminators node-level | **Resolved** | `engine/05` §10 adventure profile; `10` §1d unchanged |
| **3.3** | World-clock trigger vs MBD-03 | **Resolved** | Regroup **available** not forced (`13` §2, `04` §3a) |

### Time model

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **4.2** | `engine/05` §4 sync math | **Resolved** | `engine/05` §10 — not simulated for Alpha 0.2c |
| **4.3** | Readiness plan ER-05 body stale | **Resolved** | §1–§6 ER-05 updated; Appendix C |
| **4.4** | `IMPLEMENTATION_PLAN` §15 defers resolved items | **Resolved** | §15 notes Milestone B resolutions |

### Participation audit

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **5.1** | Midgame/final audit tables incomplete | **Resolved** | `13` §9 full metrics per path |
| **5.2** | Imbalance not flagged | **Resolved** | Manual-review flags in `13` §9 imbalance summary |
| **5.3** | Completion spec Pair A canonical | **Resolved** | Superseded |
| **5.4** | v1 audit blocked | **Resolved** | Superseded |

### Solo scope

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **6.1** | Engine/brief require solo | **Resolved** | `engine/06` Alpha 0.2c note; `PROTOTYPE_BRIEF` scoped |
| **6.2** | Playtest §8 requires solo | **Resolved** | `engine/06` §8 qualified for Alpha 0.2c |
| **6.3** | v1 ER-10 blocked | **Resolved** | Superseded |

### Hidden contradictions

| ID | Finding | Status | Resolution |
|---|---|---|---|
| **H2** | Adventure vs `engine/05` | **Resolved** | `engine/05` §10 |
| **H3** | Metadata vs graph P1/P2 | **Resolved** | `10`/`13`/`08` role language |
| **H4** | v2 overclaims consistency | **Resolved** | v2 report contradiction-scan wording |
| **H5** | Audit complete vs incomplete | **Resolved** | Full `13` §9 tables + review flags |

**Major count: 0 unresolved**

---

## 5. Remaining issues (non-blocking)

| Item | Severity | Notes |
|---|---|---|
| Opening audit: apartment role has `CHK_*`, newsroom has zero | **Manual review** | Flagged in `13` §9; informational per MBD-05 |
| Midgame Pair C: recon role lower decision count | **Manual review** | Flagged in `13` §9; informational per MBD-05 |
| `P1_LOCATION`/`P2_LOCATION` session variables | **Minor** | Track physical seats; not node ownership. Out of consistency-review scope. |
| Character-sheet modifier numeric values | **Minor** | Deferred to future `PLAYER/` artifacts per v2 report |
| ER-01, ER-06, ER-16+ | **Out of scope** | Pre-existing Milestone A / narrative gaps |

---

## 6. Validation results

Manual validation 2026-07-29:

| Gate | Result | Evidence |
|---|---|---|
| **V-CHK** | **PASS** | `CHK_115_PERCEPTION` DC 10; D20 procedure in `17` §2 |
| **V-SM** | **PASS** | 48 nodes classified Joint/Split (`10` §1c summary) |
| **V-ST** | **PASS** | Node-level `REJOIN`/`TERMINAL_OUTCOME` only (`10` §1d); window constants in `08`/`13` |
| **V8** | **PASS** | Shared `CLOCK`; deprecated availability vars; no sync math in adventure logic |
| **A6 participation** | **PASS** | All paths in `13` §9 with full metric columns |
| **C6 solo** | **PASS** | `two_player` only; engine/brief qualified |
| **P1/P2 availability writes** | **PASS** | No active writers; deprecated in `01` |
| **Player-bound node language** | **PASS** | No “Player 1 branch/owns” in adventure `LOGIC/` |
| **Superseded docs** | **PASS** | v1 report, completion spec, design packet bannered |
| **Content freeze** | **PASS** | No route/clue/ending/threshold edits |

---

## 7. Merge verdict

**PASS**

- **0 Critical** findings unresolved  
- **0 Major** findings unresolved  
- Adventure logic, engine adventure profile, compiler spec, readiness plan, and prototype brief are aligned with MBD-01–06  
- Two participation-audit manual-review flags are intentional per MBD-05 and do not block merge

---

## 8. Repository change summary

The consistency fix pass closed the gap between Milestone B v2 implementation and the rest of the repository. Authoritative rules now live in adventure logic (`01`, `04`, `08`, `10`, `13`, `17`) with cross-layer reconciliation in `engine/05` §10, `engine/06`, `BOOK_COMPILER_SPEC.md`, and `ENGINE_READINESS_PLAN.md` Appendix C. Historical documents are preserved with superseded banners rather than rewritten.

# Milestone B Implementation V2 Report

**Branch:** `cursor/milestone-b-logic-bad4`  
**Baseline:** Approved design decisions MBD-01 through MBD-06 (Alpha 0.2c)  
**Date:** 2026-07-28

---

## 1. Summary

This revision implements the owner-approved Milestone B design decisions across adventure logic and readiness documentation. All six decision groups are applied consistently. No new routes, clues, endings, thresholds, or story content were introduced.

| Decision | Status |
|---|---|
| MBD-01 Check Resolution | **Implemented** |
| MBD-02 Scene Mode | **Implemented** |
| MBD-03 Split Behaviour | **Implemented** |
| MBD-04 Time Model | **Implemented** |
| MBD-05 Participation Audit | **Implemented** |
| MBD-06 Solo Mode | **Implemented** |

---

## 2. Modified files

| File | Changes |
|---|---|
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/17_CHECK_REGISTER.md` | D20 resolution procedure; DC bands (Easy 5 / Medium 10 / Hard 15); skill taxonomy; `CHK_115_PERCEPTION` complete at DC 10 |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | §1b–§1d rewritten per MBD-02/03; all 48 nodes classified (13 Joint, 35 Split); §18 play modes; `EVT_115` check reference updated |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/04_TIME_COST_MATRIX.md` | §3 shared world clock model; §3a sync windows; removed per-player timeline math and §3b conflict |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/08_TWO_PLAYER_CORE_RULES.md` | §3 split completion (MBD-03); §9 participation audit rewritten (MBD-05) |
| `adventures/The_Last_Witness/DO_NOT_READ/LOGIC/13_SPLIT_AND_REGROUP_FLOW.md` | Split completion and sync windows; §9 multi-path participation audit |
| `adventures/The_Last_Witness/README.md` | Play modes wording aligned to MBD-06 |
| `ENGINE_READINESS_PLAN.md` | Appendix C — Milestone B decision mapping and gate status |

**Unchanged (no contradiction):** `00_ENTITY_KEY_TABLE.md`, `14_ENDING_TRIGGER_MATRIX.md`, `BOOK_COMPILER_SPEC.md`, `CONTENT_GENERATION_SPEC.md`, story routes and clue graph.

---

## 3. Resolved blockers

| Blocker | Resolution |
|---|---|
| ER-02 / V-CHK | `CHK_115_PERCEPTION` complete: Perception, DC 10, pass/fail variants, fallback route |
| ER-03 / V-SM | 48/48 nodes declare `Joint` or `Split`; 0 `UNCLASSIFIED` |
| ER-04 / V-ST | Split terminators declared: Split One `REJOIN` table; Split Two and final-act rules in §1d |
| ER-05 / V8 | Single shared world clock; no leftover-time conflict; sync windows declared |
| ER-09 / A6 | Participation audit populated for all valid paths; developer-only |
| ER-10 / C6 | `two_player` only; solo deferred with documented engine exception (§18) |
| DC undefined | Medium band DC 10 assigned per MBD-01 |
| Scene mode P1/P2 binding | Replaced with narrative-role metadata (MBD-02) |
| Pair A audit bias | Removed; all path pairs evaluated (MBD-05) |
| Per-player clock math | Removed from `04` §3 (MBD-04) |
| `WAIT_UNTIL_SYNC` / `REMOTE_CONTACT` / `EMERGENCY_INTERRUPT` as node metadata | Clarified as window-level only (MBD-03) |

---

## 4. Remaining blockers

None within Milestone B scope for declared `two_player` play mode.

| Item | Notes |
|---|---|
| ER-01 | Eleven `INTERMEDIATE` nodes still lack complete `Outgoing` — Milestone A scope |
| ER-06 | Variant enumeration gaps — Milestone A scope |
| ER-16+ | Narrative layer not authored — post–Milestone B |
| Solo mode graph | Intentionally deferred per MBD-06; not a Milestone B blocker |
| Character sheet modifiers | Referenced by MBD-01; numeric values belong on future `PLAYER/` character sheets, not logic |

---

## 5. Validation results

Manual validation performed 2026-07-28 (no automated validator in repository).

| Gate | Result | Evidence |
|---|---|---|
| **V-CHK** | **PASS** | One `ACTIVE` `CHK_*` record with `dc: 10`; resolution procedure declared |
| **V-SM** | **PASS** | 48 nodes: 13 `Joint`, 35 `Split`, 0 `UNCLASSIFIED`, 0 `Solo` |
| **V-ST** | **PASS** | Split One `REJOIN` table; Split Two and final-act rules in `10` §1d |
| **V8** | **PASS** | Shared clock model in `04` §3; no BLOCKED sync conflicts |
| **Participation gate (A6)** | **PASS** | `08` §9 and `13` §9 populated for all valid paths |
| **C6 (solo scope)** | **PASS** | `play_modes: [two_player]`; exception in `10` §18 |
| **Contradiction scan** | **PASS** | No `BLOCKED` status in adventure logic except zero-count statements |
| **Content freeze** | **PASS** | No route, clue, ending, or threshold edits |

---

## 6. Decision implementation detail

### MBD-01 — Check Resolution

- Roll: `d20 + character_modifier`; success when `roll >= dc`
- Modifiers on player character sheet
- Multi-player: all eligible roll; highest successful result wins
- DC bands: Easy 5, Medium 10, Hard 15
- `CHK_115_PERCEPTION`: Medium (DC 10)
- Engine skill taxonomy: Perception, Investigation, Persuasion, Intimidation, Stealth, Technology, Medicine, Athletics

### MBD-02 — Scene Mode

- Scene mode = narrative role metadata, not player identity
- Either player may occupy a role when story permits
- All 48 playable nodes classified

### MBD-03 — Split Behaviour

- Players continue until no legal actions; finished player waits
- No forced movement, auto-jump, timer pressure
- `WAIT_UNTIL_SYNC`, `REMOTE_CONTACT`, `EMERGENCY_INTERRUPT` = window-level only

### MBD-04 — Time Model

- One shared world clock for world state, NPC schedules, events, deadlines
- No independent timelines during split; no sync mathematics

### MBD-05 — Participation Audit

- Developer validation tool only
- All valid paths evaluated (opening roles, Pairs A/B/C, three final-act patterns)
- Informational only; 2× imbalance rule for flagging

### MBD-06 — Solo Mode

- Alpha 0.2c: `two_player` only
- Solo deferred; validation scoped to declared play modes

---

## 7. Repository change summary

Milestone B v1 left six ER items partial or blocked. V2 closes all six for the `two_player` scope by applying owner-approved design decisions rather than inventing new mechanics. The logic layer now provides:

1. A compilable D20 check register with one active record.
2. Complete scene-mode metadata decoupled from player identity.
3. Split behaviour and terminators aligned with wait-until-done semantics.
4. A single shared-clock time model without per-player timeline math.
5. A multi-path participation audit for developer balance review.
6. Explicit two-player-only scope with solo deferred.

No additional design decisions were introduced beyond MBD-01 through MBD-06.

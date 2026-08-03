# Simulator Final Fix Report

**Branch:** `cursor/simulator-trust-loop-fix-bad4`  
**Date:** 2026-08-03  
**Against:** `SIMULATOR_ADAPTER_INDEPENDENT_REVIEW.md` residuals (trust-gate hole, R-212b loop, I-02 cost drift, `needs_followup` budget coupling)

---

## Summary

Four targeted repairs close the independent-review residuals. Quantitative trust now requires structural adapter invariants, not only an empty `ambiguities[]` list.

| Issue | Status |
|-------|--------|
| Trust-gate regression hole | **Fixed** |
| R-212b depth loop | **Fixed** |
| I-02 cost mismatch (10 vs 12) | **Resolved** (PLAYER authoritative) |
| `needs_followup` phone budget coupling | **Fixed** |

**Tests:** 111 OK (`python3 -m unittest discover -s tests -v`)  
**Diagnostic:** `./run_full_diagnostic.sh 1000 42` → `simulator_trustworthy: true`

---

## 1. Trust-gate regression hole

### Root cause

`simulator_trustworthy()` only checked empty `ambiguities`, legacy keyword arrays, partial/unsupported lists, and I-02 `blocked_return` without `blocked_minutes`. Reverting P-112 or removing I-02 blocked fields while keeping `ambiguities: []` left trust **true**.

### Correction

New `simulator/trust_gate.py` with `validate_trust_invariants()` called from `simulator_trustworthy()`. Validates:

| Invariant | Rule |
|-----------|------|
| Required schema fields | `schema_version`, `follow_up_actions`, `ambiguities` key, etc. must exist |
| P-112 key | No unconditional `ACCESS_MANAGER_KEY`; `partner_conditional_flags` with records partner rule |
| I-02 J-410 | `blocked_return`, `blocked_minutes`, `minutes` present; `minutes == blocked_minutes`; `minutes_cost_resolution` documented |
| Follow-ups | Non-empty `follow_up_actions` including `FU_GYM_ALIBI`, `FU_VENDOR_LOG`; no keyword `follow_ups` |
| R-212b | `next_options` [R-212, R-214]; skim `once_per_role_path` |
| Reachability | No unreachable nodes |

### Tests added

`tests/test_final_fixes.py::TestTrustGateInvariants` — adversarial mutations for each required field (P-112, I-02, follow-ups, keywords, ambiguities key, R-212b loop, cost resolution).

### Authoritative sources

- `SIMULATOR_ADAPTER_INDEPENDENT_REVIEW.md` claim 7 failure
- `sim_adapter.json` description: PLAYER cross-checked, authoritative for simulation

---

## 2. R-212b loop

### Root cause

Adapter used `"next": "R-212"` on R-212b (auto-return), omitting PLAYER’s explicit **Continue to R-212 or R-214**. Adversarial skim selection looped R-212 → R-212b until `max_path_steps` (≈1250 min).

### Correction

| Layer | Change |
|-------|--------|
| Adapter | R-212b `next_options: ["R-212", "R-214"]` per `PLAYER/BOOKLET_RECORDS.md` §R-212b |
| Adapter | R-212 skim choice `once_per_role_path: true` (“Skim and move on”) |
| Engine | Filter `once_per_role_path` choices in `run_role_path`; track `role_choices_used` on `GameState` |

### Tests added

- `TestR212bLoopTermination::test_adversarial_skim_terminates_without_depth_burn` — ≤1 skim visit, &lt;200 min, reaches R-214
- Trust regression `test_regression_r212b_auto_next_loop`

### Authoritative sources

- `PLAYER/BOOKLET_RECORDS.md` §R-212b: *Advance +5 min. Continue to R-212 or R-214.*
- `HARBORVIEW_v0.4.1_QA_REPORT.md` D1: R-212b continue fixed in v0.4.1

---

## 3. I-02 cost mismatch

### Root cause

`PLAYER/JOINT_SCENES.md` §J-410: **+10 min**; `DO_NOT_READ/LOGIC/00_ENTITY_KEY_TABLE.md`: **12 min**. No documented resolution.

### Correction

Repository precedence:

1. `sim_adapter.json` description — authoritative for simulation; PLAYER cross-checked  
2. `PLAYER/JOINT_SCENES.md` — player-facing timing  
3. `DO_NOT_READ` entity table — internal estimate drift  

Added `minutes_cost_resolution` on J-410 documenting authoritative **10** minutes, conflicting entity-table 12, and resolution rationale. Trust gate requires this field and rejects `unresolved: true` or minutes ≠ 10.

### Tests added

- `TestI02CostResolution::test_player_authoritative_ten_minutes`
- `test_regression_i02_cost_resolution_removed`
- `test_regression_i02_entity_conflict_unresolved`

### Remaining ambiguity

None for J-410 cost. Entity table 12 is documented drift, not simulated.

---

## 4. Follow-up phone budget

### Root cause

`run_role_path` incremented `follow_ups_used` when visiting a `needs_followup` scene node (e.g. P-214 after `CHK_JAMES_PRESS` fail), coupling forced scene routing to hub phone-slot budget.

### Correction

Removed `follow_ups_used += 1` on `pending_followup` visit. Budget increments **only** in `apply_follow_up()` when an explicit `follow_up_actions` entry executes.

States now separated:

| State | Behavior |
|-------|----------|
| Availability | `eligible_follow_up_options()` — no budget change |
| Selection | Hub lists FU options — no budget change |
| Execution | `apply_follow_up()` — grants + increments budget |
| `needs_followup` route | Scene visit only — **no** budget consumption |

### Tests added

`TestFollowUpBudgetSeparation` — four tests covering availability, selection, execution, and `needs_followup` non-consumption.

### Authoritative sources

- `PLAYER/JOINT_SCENES.md` follow-up table vs booklet scene routing (`CHK_JAMES_PRESS` fail → P-214)
- V2 review residual R2-01

---

## Adversarial trust mutations (manual)

| Mutation | `simulator_trustworthy` |
|----------|-------------------------|
| Baseline | **true** |
| Remove P-112 eligibility / restore unconditional key | **false** (2 blockers) |
| Remove I-02 `blocked_return` + `blocked_minutes` | **false** (2 blockers) |
| Empty `follow_up_actions` | **false** (1 blocker) |
| Restore R-212b auto-`next` loop | **false** (3 blockers) |

---

## Files changed

| File | Change |
|------|--------|
| `simulator/trust_gate.py` | New structural trust invariants |
| `simulator/self_check.py` | Delegate to `validate_trust_invariants` |
| `simulator/engine.py` | R-212b choice filter; remove `needs_followup` budget burn |
| `simulator/state.py` | `role_choices_used` tracking |
| `adventures/.../sim_adapter.json` | J-410 cost resolution; R-212b/R-212 navigation |
| `tests/test_final_fixes.py` | 20 new regression tests |

---

## Remaining ambiguities

| Item | Impact |
|------|--------|
| Entity table J-410 = 12 min | Documented drift only; PLAYER 10 used |
| Random strategy E-904 ≈86% at 1000×42 | Play/strategy observation; not adapter defect |
| `needs_followup` vs `follow_up_actions` naming | Semantically separated; no budget coupling |

---

## Final readiness

| Capability | Ready |
|------------|-------|
| Offline diagnosis | **YES** |
| Offline repair planning | **YES** |
| Quantitative tuning | **YES** (structural trust gate + canonical adapter) |
| Termux use | **YES** (`run_full_diagnostic.sh`, explain/export scripts) |

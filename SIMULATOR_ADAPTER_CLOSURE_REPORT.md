# Simulator Adapter Closure Report

**Adventure:** Harborview (`CASE_BENCHMARK_v0.4`)  
**Branch:** `cursor/simulator-adapter-closure-bad4`  
**Date:** 2026-08-03

## Summary

All four V2 adapter blockers are resolved. Quantitative simulator output is now **trustworthy** (`simulator_trustworthy: true`, `trust_blockers: []`).

---

## Blocker 1 — P-112 manager key granted unconditionally

| Item | Detail |
|------|--------|
| **Authoritative source** | `PLAYER/BOOKLET_PEOPLE.md` §P-112: *"Mark ACCESS_MANAGER_KEY if Records partner lacks it."*; `DO_NOT_READ/LOGIC/01_WORLD_STATE_VARIABLES.md`: key from P-112 **or** R-111b |
| **Problem** | `sim_adapter.json` listed `ACCESS_MANAGER_KEY` in P-112 `flags`, granting it on every People visit |
| **Correction** | Removed unconditional flag. Added `partner_conditional_flags` on P-112. Engine applies at split merge via `_apply_partner_conditional_flags()` only when Records path lacks the flag |
| **Tests** | `test_adapter_closure.TestP112ManagerKey` (eligible / ineligible / no unconditional flag) |
| **Remaining ambiguity** | None |

---

## Blocker 2 — Four material adapter ambiguities

| ID | Topic | Authoritative source | Resolution |
|----|-------|-------------------|------------|
| AMB-J121 | J-121 return routing | `sim_adapter.json` `J-121.next_options` | Explicit player choice `[J-120, J-130]` — already modeled |
| AMB-P112 | Manager key eligibility | `PLAYER/BOOKLET_PEOPLE.md` §P-112 | `partner_conditional_flags` at merge (see Blocker 1) |
| AMB-P111 | Closed bakery phone follow-up | `PLAYER/BOOKLET_PEOPLE.md` §P-111 | Gate `branch_choices`: `skip_closed` (0 min) vs `phone_followup` (+15 min, partial C-07) |
| AMB-R212B | R-212b skim loop | `sim_adapter.json` `R-212b.fake_choice` | Marked `fake_choice`; no simulation loop |

All four moved to `resolved_ambiguities[]`. `ambiguities[]` is empty.

| Item | Detail |
|------|--------|
| **Tests** | `test_adapter_closure.TestResolvedAmbiguities`, `TestP111ClosedBakeryGate`, `TestTrustGate.test_unresolved_ambiguity_downgrades_trust` |
| **Remaining ambiguity** | None material |

---

## Blocker 3 — Legacy keyword `follow_ups` partially active

| Item | Detail |
|------|--------|
| **Authoritative source** | Prior `simulator_unsupported` note; `follow_up_actions` as replacement |
| **Problem** | `follow_ups` keyword array remained in adapter and triggered `SIM-LEGACY-FOLLOWUPS` / trust blockers |
| **Correction** | Removed `follow_ups` array entirely. Retained `legacy_follow_ups_documentation` string for human reference only. Trust gate rejects only active keyword arrays (`legacy_keyword_follow_ups()` returns `[]`) |
| **Tests** | `test_adapter_closure.TestLegacyFollowUps`, `TestExplicitFollowUps` |
| **Remaining ambiguity** | None |

---

## Blocker 4 — I-02 retry costs 0 minutes

| Item | Detail |
|------|--------|
| **Authoritative source** | `PLAYER/JOINT_SCENES.md` §J-410: *"Advance +10 min"* at infer scene; blocked path returns to investigation without advancing to J-500 |
| **Problem** | Incomplete I-02 redirected to J-300 with zero minute charge, enabling free retry loops |
| **Correction** | Added `blocked_minutes: 10` and `blocked_return: J-300` on J-410. Engine charges `blocked_minutes` exactly once per blocked visit before returning |
| **Tests** | `test_adapter_closure.TestI02RetryCost`, `test_regressions.TestI02Block` |
| **Remaining ambiguity** | None (`blocked_cost_source` documented in adapter) |

---

## Trust gate

| Prerequisite | Status |
|--------------|--------|
| Material adapter ambiguities resolved | ✅ `ambiguities: []` |
| P-112 behavior canonical | ✅ `partner_conditional_flags` |
| I-02 retry timing canonical | ✅ `blocked_minutes: 10` |
| No unsupported follow-up on paths | ✅ keyword array removed |
| Deterministic reachability | ✅ no unreachable nodes |
| **Quantitative outputs trustworthy** | **✅ YES** |

Verified by:
- `python3 -m unittest discover -s tests -v` — **91 tests OK**
- `./run_full_diagnostic.sh 1000 42` — `simulator_trustworthy: true`

---

## Files changed

| File | Change |
|------|--------|
| `adventures/CASE_BENCHMARK_v0.4/sim_adapter.json` | P-112 conditional key, P-111 gate choices, J-410 blocked cost, resolved ambiguities, removed `follow_ups` |
| `simulator/engine.py` | Partner conditional flags, gate branch choices, I-02 blocked minutes |
| `simulator/self_check.py` | Expanded trust gate (ambiguities, legacy follow-ups, reachability, infer retry) |
| `simulator/loader.py` | Removed auto-injected `simulator_partial` for P-112 |
| `simulator/ai_context.py` | Expose `resolved_ambiguities` in trust context |
| `tests/test_adapter_closure.py` | New regression suite (18 tests) |
| `tests/test_explainer.py`, `tests/test_explainer_fixes.py`, `tests/test_regressions.py` | Updated for trusted adapter |

---

## Quantitative tuning verdict

**YES — quantitative Monte Carlo metrics may now be used for Harborview tuning**, subject to normal playtest validation. The simulator trust gate passes with zero blockers.

# IDNE Simulator — Independent Review V2

**Reviewer posture:** adversarial; do not trust `SIMULATOR_FIX_REPORT.md`, the 39 passing tests, or PASS claims.  
**Subject:** repaired simulator on PR #21 (`cursor/idne-simulator-fix-bad4`, commits `97ef007` + `5650d6b`)  
**Review date:** 2026-08-02  
**Method:** full source re-read, independent probes, required CLI re-runs  
**No simulator code was modified for this review.**

---

## Executive verdict

The PR **does fix the six mandatory ISS defects** that previously made E-901 unreachable and corrupted clock math. Independent probes confirm ISS-01, ISS-02, ISS-03, ISS-04/05 (hard leaks), ISS-06, and the core of ISS-09.

However, **new and residual defects still invalidate Monte Carlo quantitative outputs** for engine and adventure decisions:

1. Overdue hubs restore all choices and continue play past 23:00 without forcing ending dispatch.
2. Incomplete I-02 can loop through Hub 2 and inflate fiction time to thousands of minutes.
3. Hub-2 stairwell revisit navigates to Hub 1 (`J-110 → J-120`), not back to Hub 2.
4. Case-file follow-up slots remain unimplemented.
5. Soft strategy / adapter biases remain; trust gate is present but incomplete.

**Do not treat post-fix ending frequencies or fiction-minute averages as authoritative.**

---

## Re-execution evidence (this review)

| Command | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | **39 OK** |
| validate | `simulation_output/20260802_074949_035872_validate_0` |
| simulate 1000×42 | `…_074949_081659_simulate_0` — E-901: **3**, E-904: 880, fiction avg **811.3**, `simulator_trustworthy: false`, `simulator_engine_e901_ok: true` |
| trace 42 | `…_074951_021050_trace_0` — E-904, fiction **243** |
| compare 100×8 | `…_074952_144730_compare_0` — E-901: **3**/800, fiction avg **1084**, trustworthy **false** |

Oracle+clue-seeking probe (100 runs, force correct accuse): **E-901 = 16%**, E-904 = 66% — win is reachable but still rare under time/loop pressure.

---

## Verification of mandatory ISS fixes

### ISS-01 — Ending / I-03 order — **FIXED**

| Field | Evidence |
|---|---|
| Probe | J-510 step with full proof + accuse culprit → `I-03` marked; `evaluate_ending` → **E-901** |
| `_engine_e901_reachable` | **True** |
| Monte Carlo | E-901 count > 0 (3/1000 simulate) |

Previously impossible win is now engine-reachable. Synthetic ending-family tests match dispatcher order for E-901…E-905.

### ISS-02 — Double time charging — **FIXED**

| Field | Evidence |
|---|---|
| Probe | Stairwell: hub +15, destination +0, total +15 |
| Mechanism | `entry_cost_prepaid` + `skip_entry_minutes` under `hub_authoritative` |

### ISS-03 — Split window-local maxima — **FIXED**

| Field | Evidence |
|---|---|
| Probe | split1 people=25/records=20/wall=30; split2 people=32/records=32/wall=37 |
| Check | `wall == max(local_A, local_B) + 5`; split2 people **not** cumulative of split1 |

### ISS-04 / ISS-05 — Hard hidden-information leakage — **FIXED (hard leaks)**

| Field | Evidence |
|---|---|
| `public_options` | Keys: id, label, minutes, once_per_hub, risky, target — **no** `grants_clues` |
| Strategies | No Tomás / C-15 hardcode |
| Residual soft issues | See V2-07, V2-08 below (not the original hard leaks) |

### ISS-06 — Failure extra minutes — **FIXED**

| Field | Evidence |
|---|---|
| Probe | `CHK_INVOICE` fail → **15** (not 30) |

### ISS-09 — Finding ownership gate — **PARTIALLY FIXED**

| Field | Evidence |
|---|---|
| Good | `SIM-TRUST-DOWNGRADE` → UNDETERMINED; bottlenecks → UNDETERMINED when untrusted; no ADVENTURE `SIM-NO-WIN` while engine/trust fail |
| Incomplete | `SIM-FAKE-*` still labeled **ADVENTURE** while `simulator_trustworthy: false` (V2-06) |
| Gate weakness | Trust false solely because `ambiguities[]` is non-empty; `follow_ups` unimplemented is **not** listed in `simulator_unsupported` |

---

## Adapter ambiguities — documentation vs material

| # | Ambiguity text | Classification | Material? |
|---|---|---|---|
| 1 | J-121 → J-120 or J-130 | Harmless packaging if players choose; simulator offers both via `next_options` | **Low** — does not alone invalidate metrics |
| 2 | P-112 grants `ACCESS_MANAGER_KEY` always | **Material** — PLAYER says “if Records partner lacks it”; simulator always grants → T3 basement path easier | **Yes** — opportunity/access rates |
| 3 | Bakery-closed phone partial C-07 | Partially modeled via gate skip; joint follow-up slots for recovery **not** modeled | **Yes** — interacts with follow-ups gap |
| 4 | R-212b `fake_choice` | Labeled correctly | **Low** |
| 5 | “once_per_hub not tracked” | **Stale / wrong** — `once_per_hub` **is** implemented now | Documentation defect; misleads trust rationale |

**Conclusion:** Ambiguities 2 and 3 (plus unimplemented follow-ups) **materially change** simulation results. Ambiguity 5 is obsolete text. Trust downgrade is directionally correct but cites the wrong primary cause list.

---

## Remaining / new issue register

### V2-01 — Deadline does not halt hubs (choices restored)

| Field | Value |
|---|---|
| **Severity** | **critical** |
| **File/function** | `simulator/engine.py` `hub_options` |
| **Evidence** | At clock 1380 on J-300, filtered options empty then restored to all hub choices; step advances to J-330 at clock 1405 |
| **Consequence** | Play continues long past deadline; fiction minutes → 800–3000+; E-904 understates how often clock *should* have forced terminal dispatch earlier |
| **Required correction** | When `clock >= deadline`, force transition to J-600/E-904 (or offer only terminal actions); never restore filtered-empty hub menus |
| **Invalidates quantitative outputs?** | **YES** — time and ending distributions |

### V2-02 — Incomplete I-02 Hub-2 time bomb

| Field | Value |
|---|---|
| **Severity** | **critical** |
| **File/function** | `simulator/engine.py` `step` infer I-02 branch |
| **Evidence** | 41/50 random runs contain `blocked-I-02`; fiction minutes extremes in samples **146–3374** |
| **Consequence** | Loop Hub 2 ↔ I-02 without acquiring required facts; interacts with V2-01 after deadline |
| **Required correction** | Charge time on failed infer attempt; cap retries; or require new evidence before re-entry; force accusation/timeout path |
| **Invalidates quantitative outputs?** | **YES** |

### V2-03 — Hub-2 stairwell revisit exits to Hub 1

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `sim_adapter.json` `J-110.next` + `engine.step`; PLAYER also sends revisit to J-110→J-120 |
| **Evidence** | J-300 `stairwell_revisit` → J-110 → **J-120** (Hub 1), abandoning Hub 2 flow |
| **Consequence** | Structural navigation mismatch with intended Act-2 hub; strategies can strand in Act-1 graph |
| **Required correction** | Adapter/engine: revisit destination should return to calling hub (or separate revisit node). Adventure PLAYER change is out of scope for this PR — mark **UNDETERMINED**/adapter unsupported until resolved |
| **Invalidates quantitative outputs?** | **YES** for path/ending rates involving revisit |

### V2-04 — `hub_targets` last-write collision for shared destinations

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `_build_hub_targets` |
| **Evidence** | `J-110` maps only to hub_id **2** / `stairwell_revisit` / `once_per_hub: True`, overwriting Hub 1 stairwell metadata |
| **Consequence** | Prepaid-cost / once metadata for shared destinations incorrect depending on dict order |
| **Required correction** | Key by `(hub_id, target)` or store list; set prepaid from the **selected choice**, not a global target map |
| **Invalidates quantitative outputs?** | **Partial** — cost currently still 15 once for stairwell, but policy is fragile |

### V2-05 — Follow-up slots unimplemented

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | Adapter `follow_ups` / `follow_up_max`; absent from `engine.py` |
| **Evidence** | `follow_up_max` / `follow_ups` never referenced in engine; hub joint follow-ups for C-13/C-14 recovery missing |
| **Consequence** | Opportunity/motive recovery underrepresented; fair-path Monte Carlo biased |
| **Required correction** | Implement hub follow-up resolution with max uses, **or** add explicit `simulator_unsupported` entry and exclude opportunity metrics |
| **Invalidates quantitative outputs?** | **YES** for clue/ending fairness claims |

### V2-06 — ISS-09 incomplete: `SIM-FAKE-*` still ADVENTURE while untrusted

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/diagnostics.py` `analyze_simulation` |
| **Evidence** | Post-fix findings: `SIM-FAKE-J-122` / `SIM-FAKE-R-212b` layer=**ADVENTURE** alongside `SIM-TRUST-DOWNGRADE` |
| **Consequence** | Authors may still treat fake-choice findings as adventure-proven while simulator trust is false |
| **Required correction** | When `not trustworthy` or prechecks fail, force non-topology findings to SIMULATOR/UNDETERMINED |
| **Invalidates quantitative outputs?** | Finding interpretation **yes**; raw graph CSV no |

### V2-07 — Soft strategy leakage / bias

| Field | Value |
|---|---|
| **Severity** | **minor–major** |
| **File/function** | `simulator/strategies.py` `PoorDecisionsStrategy`, `ACTION_PRIORITY` |
| **Evidence** | Poor-decisions `suspects[:-1]` permanently excludes last suspect (**Tomás Reyes**, the culprit). `ACTION_PRIORITY` hardcodes Harborview action ids |
| **Consequence** | Compare-mode strategy mixes are not adventure-neutral; poor-decisions never “accidentally” correct-accuses last-listed culprit |
| **Required correction** | Shuffle/exclude randomly; keep priority tables in adapter strategy profiles, not code |
| **Invalidates quantitative outputs?** | **YES** for strategy-compare accusation stats |

### V2-08 — James fail → P-214 not forced

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `apply_node_effects` / `run_role_path` |
| **Evidence** | Fail sets `pending_followup=P-214`, but `next_options` are chosen first; pending only used if no options. Path membership check uses bare `P-214` vs `people:P-214` |
| **Consequence** | Fail path often skips forced gym follow-up; C-13 rates wrong |
| **Required correction** | On fail with `needs_followup`, override next node to follow-up before free `next_options` |
| **Invalidates quantitative outputs?** | **YES** for opportunity (C-13) metrics |

### V2-09 — Memory / max_states guards still unenforced

| Field | Value |
|---|---|
| **Severity** | **major** (safety claim) |
| **File/function** | `simulator/config.py` vs `runner.py` / `engine.py` |
| **Evidence** | `memory_guard_mb`, `max_states` never referenced in runner/engine |
| **Consequence** | Termux OOM risk under long I-02 loops (V2-02) |
| **Required correction** | Enforce caps or remove claims from docs |
| **Invalidates quantitative outputs?** | No (correctness); **yes** for Termux readiness claims |

### V2-10 — Unique output folders — **FIXED**

| Field | Evidence |
|---|---|
| Probe | Distinct microsecond+counter folder names under rapid successive runs |
| CLI | validate/simulate/trace/compare each got unique dirs |

### V2-11 — Split launch cost still ambiguous

| Field | Value |
|---|---|
| **Severity** | **minor** (parser ambiguity) |
| **Evidence** | Hub charges split1 **20** then adds `max(role)+5` for private paths |
| **Material?** | **Yes** if PLAYER “20 min” was meant as inclusive split estimate |
| **Invalidates?** | Time metrics until clarified |

---

## Test suite assessment

39 tests pass and cover the **fixed ISS regressions**. They **do not** catch:

- deadline hub restore (V2-01)
- I-02 retry unbounded time (V2-02)
- hub2 revisit → hub1 (V2-03)
- follow-up slot behavior (V2-05)
- forced P-214 on James fail (V2-08)
- memory guard enforcement (V2-09)
- PoorDecisions culprit exclusion (V2-07)

Passing tests ≠ trustworthy Monte Carlo.

---

## Scores and gates

| Score | Value | Rationale |
|---|---:|---|
| **Correctness** | **6 / 10** | Core ISS clock/ending/leak/check bugs fixed; deadline bypass + I-02 loops + navigation still wrong |
| **Diagnostic usefulness** | **5 / 10** | Trust downgrade helps; fake-choice still mis-owned; quantitative rates still unsafe |
| **Termux readiness** | **CONDITIONAL PASS** | Runs offline with timeout/progress/unique dirs; memory/state guards unimplemented; long loops possible |

| Decision gate | Answer |
|---|---|
| **Safe for engine decisions** | **NO** |
| **Safe for adventure tuning** | **NO** |

---

## Exact remaining blockers

1. **V2-01** Force terminal ending when `WORLD_CLOCK >= deadline` (no hub menu restore).  
2. **V2-02** Bound/cost incomplete I-02 retries.  
3. **V2-03 / V2-04** Fix revisit navigation + hub_targets prepaid keying.  
4. **V2-05** Implement follow-up slots **or** hard-unsupported gate.  
5. **V2-06** Extend ISS-09 so no ADVENTURE blame while untrusted.  
6. **V2-08** Force James fail follow-up node.  
7. **V2-09** Enforce or drop memory/state limits.  
8. Resolve material adapter ambiguities (P-112 key grant; split launch inclusivity; stale once_per_hub note).

---

## Minimum next implementation scope

1. Deadline terminalization at every hub/infer entry.  
2. I-02 failed-attempt cost + retry cap + metrics flag.  
3. Follow-up slot engine **or** `simulator_unsupported` + metric exclusion.  
4. Prepaid cost from selected choice object (delete global target map collision).  
5. Revisit return-to-caller-hub behavior in adapter simulation contract.  
6. Ownership gate: all non-topology findings → SIMULATOR/UNDETERMINED when trust false.  
7. Regression tests for V2-01, V2-02, V2-03, V2-05, V2-08.

Until those land, use the simulator only for: graph topology CSV, broken-link scans, and engine self-check that E-901 is *mechanically* reachable under synthetic states.

---

## Disposition of pre-fix vs post-fix outputs

| Generation | Quantitative use |
|---|---|
| Pre-ISS-fix outputs | **Discard** (E-901 impossible, double charge, cumulative splits) |
| Post-fix outputs from PR #21 | **Not safe** for engine/adventure decisions (V2-01/02 dominate E-904 and fiction averages) |
| Synthetic unit/regression probes | **OK** for verifying ISS-01–06 presence |

---

## Bottom line

PR #21 successfully repaired the **named critical ISS defects**. The simulator is materially better and E-901 is no longer impossible. It is **not** yet a trustworthy instrument for engine or adventure decisions because overdue play continues, I-02 can thrash Hub 2, follow-ups are missing, and several findings still over-claim adventure ownership.

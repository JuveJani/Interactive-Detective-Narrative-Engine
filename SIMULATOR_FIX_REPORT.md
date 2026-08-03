# IDNE Simulator Fix Report

**Branch:** `cursor/idne-simulator-fix-bad4`  
**Date:** 2026-08-02  
**Authority:** `SIMULATOR_INDEPENDENT_REVIEW.md` (ISS-01 through ISS-09, output folders, blocker handling)

---

## Summary

Targeted simulator repair addressing all defects that **invalidated simulation results**. Harborview adventure logic, PLAYER content, engine rules, and `sim_adapter.json` game semantics were **not modified**.

**Post-fix:** E-901 is engine-reachable; hub double-charging removed; split windows use local maxima; strategies are blind; check fail timing corrected; diagnostic gates prevent adventure-blame when simulator suspect; output folders are unique.

**Monte Carlo is still flagged `simulator_trustworthy: false`** due to documented adapter ambiguities and unimplemented follow-up slots — by design until those are resolved.

---

## ISS fixes

### ISS-01 — Ending / I-03 order

| Field | Detail |
|---|---|
| **Root cause** | `engine.step` evaluated `can_complete_infer("I-03")` before `state.accused` was set |
| **Correction** | J-510 now sets accused via strategy first, then marks I-03 when proof tags satisfied |
| **Files** | `simulator/engine.py` (`_complete_infer`, infer branch) |
| **Tests** | `tests/test_regressions.py::TestEngineE901`, `TestEndingsReachable` (all 5 endings) |
| **Invalidates old outputs?** | **YES** — all prior ending-frequency metrics |

### ISS-02 — Double time charging

| Field | Detail |
|---|---|
| **Root cause** | Hub choice minutes and destination `minutes` both applied on consecutive steps |
| **Correction** | `cost_policy: hub_authoritative` (default): hub pays choice cost; `entry_cost_prepaid` suppresses destination entry minutes unless `additive_cost: true` |
| **Files** | `simulator/engine.py` (`hub_targets`, hub step, `apply_node_effects`) |
| **Tests** | `tests/test_regressions.py::TestHubCostOnce` |
| **Invalidates old outputs?** | **YES** — all time/threshold/ending timing metrics |

### ISS-03 — Split window calculation

| Field | Detail |
|---|---|
| **Root cause** | `run_role_path` accumulated into cloned cumulative `role_minutes`; `resolve_split` used totals as window-local |
| **Correction** | `run_role_path` returns `(state, window_minutes)` with local counter; split merge uses window totals only |
| **Files** | `simulator/engine.py` (`run_role_path`, `resolve_split`) |
| **Tests** | `tests/test_regressions.py::TestSplitWindowLocal`, `tests/test_clock_splits.py` |
| **Invalidates old outputs?** | **YES** |

### ISS-04 / ISS-05 — Hidden-information leakage

| Field | Detail |
|---|---|
| **Root cause** | `enrich_options` exposed `grants_clues`; `pick_accused` hardcoded Tomás via C-15 |
| **Correction** | `public_options()` exposes only id, target, minutes, label, risk flags; strategies use public proof tags + suspect list only |
| **Files** | `simulator/engine.py`, `simulator/strategies.py` |
| **Tests** | `tests/test_regressions.py::TestHiddenInformation` |
| **Invalidates old outputs?** | **YES** for strategy compare / accusation analytics |

### ISS-06 — Failure cost doubling

| Field | Detail |
|---|---|
| **Root cause** | `apply_check_outcome` added `fail.extra_minutes` twice |
| **Correction** | Apply branch `extra_minutes` once |
| **Files** | `simulator/checks.py` |
| **Tests** | `tests/test_regressions.py::TestCheckFailTiming`, `tests/test_checks.py` |
| **Invalidates old outputs?** | **YES** for check-fail path timing |

### ISS-09 — Finding ownership / confidence gate

| Field | Detail |
|---|---|
| **Root cause** | `SIM-NO-WIN` emitted as ADVENTURE without engine self-check |
| **Correction** | `SimulatorSelfCheck`, `_engine_e901_reachable`, `simulator_trustworthy()` gate; adventure blame only when prechecks pass; else SIMULATOR or UNDETERMINED |
| **Files** | `simulator/self_check.py`, `simulator/diagnostics.py` |
| **Tests** | `tests/test_regressions.py::TestDiagnosticsGates` |
| **Invalidates old outputs?** | **YES** for finding interpretation (not raw CSV topology) |

### Output folders (ISS-14)

| Field | Detail |
|---|---|
| **Root cause** | Second-resolution timestamps collided |
| **Correction** | `make_output_dir(mode=...)` uses microseconds + monotonic counter |
| **Files** | `simulator/output.py`, `simulator/runner.py` |
| **Tests** | `tests/test_regressions.py::TestOutputFolders` |

---

## Additional blocker handling

| Mechanic | Status |
|---|---|
| **`once_per_hub`** | **Implemented** — `hub_visits` filters used choices in `hub_options` |
| **I-02 failure loop** | **Implemented** — incomplete I-02 redirects to J-300 instead of advancing to J-500 |
| **James check fail → P-214** | **Partial** — `pending_followup` set on fail; role path follows when needed |
| **Follow-up slot limits** | **Not implemented** — adapter `follow_ups` / `follow_up_max` documented only; triggers `simulator_trustworthy: false` via ambiguities |
| **CHK focus by role** | **Unchanged** — still flat +2 (minor; not invalidating) |

---

## Test results

```
python3 -m unittest discover -s tests -v
→ 39 tests OK (was 21)
```

New module: `tests/test_regressions.py` (18 tests covering mandatory regressions).

---

## Post-fix simulation runs

| Command | Output folder | Key result |
|---|---|---|
| validate | `simulation_output/20260802_073539_596371_validate_0` | 0 static critical findings |
| simulate 1000×42 | `simulation_output/20260802_073539_640751_simulate_0` | **E-901: 3**; E-904: 880; fiction avg **811** min |
| trace 42 | `simulation_output/20260802_073541_572658_trace_0` | E-904; fiction **243** min; engine E-901 precheck **true** |
| compare 100×8 | `simulation_output/20260802_073542_687670_compare_0` | **E-901: 3** / 800; trustworthy **false** |

---

## Old vs new output validity

| Output type | Pre-fix valid? | Post-fix valid? |
|---|---|---|
| `graph.csv` topology | Mostly yes | Yes |
| Spoiler static scans | Yes | Yes |
| Ending frequencies | **No** | **Conditional** — engine fixed; trust gate still false |
| Time / split balance | **No** | **Conditional** — metrics renamed (`fiction_minutes_avg`); follow-ups unimplemented |
| `SIM-NO-WIN` as adventure defect | **No** | Gated |

**All pre-fix `simulation_output/` folders should be discarded for quantitative decisions.**

---

## Safe for decisions?

| Use | Safe? |
|---|---|
| Engine rule changes based on Monte Carlo | **NO** — `simulator_trustworthy: false` |
| Adventure tuning from ending rates | **NO** — high E-904 still driven by strategy loops + unimplemented follow-ups |
| Delivery Adapter static graph review | **YES** (with manual review) |
| Regression testing simulator itself | **YES** |

---

## Remaining blockers

1. **Follow-up slots** not simulated — Monte Carlo trust downgrade active  
2. **Adapter ambiguities** (5 documented) — trust downgrade active  
3. **High E-904 rate** under random/poor strategies — mix of strategy bias and I-02 hub loops (needs human playtest to separate from adventure deadline)  
4. **`memory_guard_mb` / `max_states`** still declared but not enforced  
5. **Real wall-clock playtime** (IDNE §5.4) not estimated — only fiction minutes reported  

---

## Readiness verdict

| Criterion | Status |
|---|---|
| Critical simulator defects fixed | **YES** |
| Regression tests added | **YES** |
| Trustworthy for engine decisions | **NO** (conditional — ambiguities + follow-ups) |
| Trustworthy for adventure tuning | **NO** (same) |
| Safe for structural/diagnostic hygiene | **CONDITIONAL YES** |

Do **not** declare the simulator fully trustworthy because tests pass. Treat Monte Carlo as **exploratory** until follow-ups are implemented and adapter ambiguities are resolved or waived with human approval.

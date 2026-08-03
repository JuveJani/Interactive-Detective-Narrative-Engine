# Offline Explainer — Independent Review V2

**Reviewer posture:** adversarial. Do not trust `OFFLINE_EXPLAINER_FIX_REPORT.md` or the 71 passing tests without re-execution.  
**Subject:** PR #25 / `cursor/offline-explainer-fix-bad4` (commits `78989b1`, `4dc1f80`)  
**Review date:** 2026-08-03  
**Method:** full re-read of follow-up / diagnostics / repair-plan / AI-context code; independent probes (not the unit tests); Harborview CLI re-run  
**No product code was modified for this review.**

---

## Executive verdict

The eight claimed repairs **hold under independent verification**.

Deterministic `follow_up_actions` activate and respect per-action and global limits. Legacy keyword `follow_ups` are **not** silently simulated and are reported. Zero / rare success endings emit correctly qualified findings. While untrusted, Harborview findings do **not** use layer `ADVENTURE`. Finding-specific `repair-plan` preserves the global backlog; repeated calls are idempotent. Local-AI context separates facts, observations, ambiguity, and hypotheses. Quantitative tuning remains gated off while adapter ambiguities exist.

Residual risks remain (P-112 always grants manager key; I-02 free retry; forced check follow-up path still increments `follow_ups_used`; `FU_` id prefix coupling). None of those invalidate the eight verification claims.

| Gate | Answer |
|---|---|
| **Safe for offline diagnosis** | **YES** |
| **Safe for offline repair planning** | **YES** |
| **Safe for quantitative tuning** | **NO** |

---

## Re-execution evidence

| Command / probe | Result |
|---|---|
| Adversarial probe script (`/tmp/verify_v2.py`) | **All 8 claim blocks PASS** |
| `python3 -m unittest discover -s tests -v` | **71 OK** (informational only; not trusted as proof) |
| `./run_full_diagnostic.sh 200 42` | `simulation_output/20260803_042020_899609_simulate_0` |
| Harborview 200×42 | E-901:**2**, E-904:162, E-902:21, E-905:15; `simulator_trustworthy: false` |
| Findings | `SIM-TRUST-DOWNGRADE`, `SIM-WIN-UNTRUSTED`, `SIM-LEGACY-FOLLOWUPS`, bottlenecks, fakes — **0 ADVENTURE** |
| `repair-plan --finding SIM-FAKE-J-122` | Backlog options stayed **12**; `repair_plan_SIM-FAKE-J-122.md` created |
| AI trust context | All required sections present; 4 ambiguities; no culprit string |

---

## Claim-by-claim verification

### 1. Deterministic follow-ups activate and respect limits — **PASS**

| Check | Evidence |
|---|---|
| Actions present | Adapter `follow_up_actions`: `FU_GYM_ALIBI`, `FU_VENDOR_LOG`, `FU_GENERAL_PHONE` |
| Eligible when conditions met | With `CHECK_FAIL_CHK_JAMES_PRESS` at `J-300`, gym action appears |
| Wrong hub | At `J-120`, eligible list **empty** |
| Per-action max | Second `apply_follow_up(FU_GYM_ALIBI)` returns **0**; clue granted once |
| Global `follow_up_max` | When `follow_ups_used == follow_up_max`, hub options empty |
| Hub integration | `engine.step` selecting gym: clock **+10**, `C-13` granted, stays on hub |
| Hidden info | Public follow-up options contain **no** grant fields |

**Residual (does not fail claim):** Forced check path `needs_followup → P-214` still increments `follow_ups_used` inside `run_role_path` when the pending node is visited (probe seed 1 → `follow_ups_used=1`). That couples scene-forced follow-ups to the phone-slot budget. Deterministic hub `follow_up_actions` still work correctly.

### 2. Free-text keyword follow-ups no longer silently simulated — **PASS**

| Check | Evidence |
|---|---|
| Engine stub | `_resolve_follow_up` always returns **0** |
| Auto-grant scan | **0** clue grants across all nodes via keyword path |
| Reporting | Finding `SIM-LEGACY-FOLLOWUPS` (layer `SIMULATOR`) |
| Trust gate | `simulator_unsupported` includes legacy keyword notice; listed in trust blockers |

Legacy `follow_ups[]` keyword entries remain in the adapter as documentation only.

### 3. Zero-success endings always produce a correctly qualified finding — **PASS**

| Scenario | Finding | Layer / qualification |
|---|---|---|
| Untrusted, 0× E-901 | `SIM-NO-WIN-UNTRUSTED` | `UNDETERMINED`, confidence `low`; evidence states observation-only, not adventure proof |
| Trusted (ambiguities cleared), 0× E-901 | `SIM-NO-WIN` | `UNDETERMINED` (not `ADVENTURE`) |
| Untrusted, rare E-901 | `SIM-WIN-UNTRUSTED` | `UNDETERMINED`; no zero-win finding |
| Harborview 200×42 (2 wins) | `SIM-WIN-UNTRUSTED` present | Matches rare-but-reachable case |

When engine cannot reach E-901, `SIM-ENGINE-E901` (SIMULATOR) covers proven unreachability; zero-win branch does not invent an adventure blame finding.

### 4. Untrusted simulations never blame adventure without deterministic proof — **PASS** (Harborview)

| Check | Evidence |
|---|---|
| 30-run probe | **0** findings with `layer=ADVENTURE` |
| Fake / bottleneck | `UNDETERMINED`, confidence `low` when trust affects conclusion |
| Zero-win untrusted | Explicitly not adventure-proven |

**Residual:** `validate_static` can still emit `ADVENTURE` for unreachable/dead-end topology. Harborview currently emits none. Those would be **deterministic graph facts**, not Monte Carlo blame — acceptable under the claim’s “without deterministic proof” wording, but worth watching if validator starts firing.

### 5. Finding-specific repair plans preserve full backlog — **PASS**

| Check | Evidence |
|---|---|
| Before / after `repair-plan --finding SIM-FAKE-J-122` | `repair_options.json` length **12 → 12**; backlog SHA unchanged |
| Second fake finding plan | Backlog hash still unchanged |
| Artifacts | `repair_plan_<ID>.md` + `.json` created alongside global backlog |

### 6. Interrupted / repeated repair-plan cannot corrupt outputs — **PASS** (within tested scope)

| Check | Evidence |
|---|---|
| Idempotent re-run | Identical `repair_plan_SIM-FAKE-J-122.json` content |
| Atomic write | `atomic_write_text` uses temp + replace; leftover `.tmp` does not replace live backlog |
| Plan survival after `explain` | Finding plan file still present; backlog content stable |

**Residual:** There is no simulated hard kill mid-`replace()`. Atomic rename is the intended protection; crash *during* the final replace is OS-dependent and untested. Practical risk on Termux is low.

### 7. Local-AI context separates facts / observations / ambiguity / hypotheses — **PASS**

Trust context for `SIM-TRUST-DOWNGRADE` contains:

- `PROVEN_FACTS` (includes “rates are NOT facts about the adventure”)
- `SIMULATION_OBSERVATIONS`
- `AMBIGUITIES` (4 entries + related node excerpts in `node_excerpt`)
- `HYPOTHESES`
- `FORBIDDEN_CONCLUSIONS` (forbids Monte Carlo → adventure balance)
- `SAFE_REPAIR_OPTIONS`
- `REQUIRED_HUMAN_DECISIONS`

No culprit / `truth` strings in the trust package.

### 8. Quantitative tuning remains disabled while ambiguities exist — **PASS**

| Check | Evidence |
|---|---|
| `simulator_trustworthy` | **false** |
| Blockers | 4 ambiguities; legacy follow_ups unsupported; P-112 partial |
| `summary.md` | `QUANTITATIVE RESULTS UNTRUSTED` banner + blockers |
| `executive_diagnostic.md` | “Quantitative results trusted: **no**” + exact blockers |

---

## Harborview diagnostic snapshot (this review)

```
runs: 200, seed: 42
simulator_trustworthy: false
ending_distribution: E-901=2, E-902=21, E-904=162, E-905=15
ADVENTURE findings: none
repair_options after finding-specific plan: 12 (unchanged)
```

---

## Residuals (not claim failures)

| ID | Severity | Issue |
|---|---|---|
| R2-01 | minor | `needs_followup` visit increments `follow_ups_used` (phone budget coupled to forced scene) |
| R2-02 | minor | Hub follow-up detection also matches `id.startswith("FU_")` — naming convention, not schema |
| R2-03 | major (tuning) | P-112 still always grants `ACCESS_MANAGER_KEY` (documented partial) |
| R2-04 | major (tuning) | Incomplete I-02 still returns with 0 minute charge |
| R2-05 | info | `FU_GENERAL_PHONE` is always eligible under slot limit — strategies may burn slots |
| R2-06 | info | `validate_static` can still label topology issues `ADVENTURE` even when Monte Carlo is untrusted |

---

## Scores

| Score | /10 | Rationale |
|---|---:|---|
| **Simulator correctness** | **7.5** | Follow-ups now real; deadline/revisit/trust ownership hold; P-112 + I-02 free retry remain |
| **Explanation quality** | **7.5** | Proven vs suspected split works; untrusted rates labeled; templates still generic for bottlenecks |
| **Repair usefulness** | **7.5** | Backlog preservation fixed; per-finding plans usable; options still high-level |
| **Local-AI handoff quality** | **8** | Required sections present with ambiguities and forbidden conclusions; enough for offline discussion |

---

## Exact remaining blockers (quantitative tuning)

1. Adapter `ambiguities[]` still non-empty (4 entries, including material P-112 wording).  
2. `simulator_partial`: P-112 manager key granted without Records partner state check.  
3. Legacy keyword `follow_ups` still listed under `simulator_unsupported` (documented, not simulated).  
4. Incomplete I-02 retry still free of time cost (bias on ending mix).  

Until those are cleared or explicitly accepted as out-of-scope with metrics excluded, **do not use ending rates or fiction averages to tune Harborview**.

---

## Final gates

| Gate | Answer |
|---|---|
| Simulator correctness | **7.5 / 10** |
| Explanation quality | **7.5 / 10** |
| Repair usefulness | **7.5 / 10** |
| Local-AI handoff quality | **8 / 10** |
| Safe for offline diagnosis | **YES** |
| Safe for offline repair planning | **YES** |
| Safe for quantitative tuning | **NO** |
| Exact remaining blockers | P-112 key grant; 4 ambiguities; legacy follow_ups unsupported entry; free I-02 retry |

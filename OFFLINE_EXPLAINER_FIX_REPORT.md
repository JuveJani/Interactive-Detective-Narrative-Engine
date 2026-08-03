# Offline Explainer Fix Report

**Branch:** `cursor/offline-explainer-fix-bad4`  
**Addresses:** `OFFLINE_EXPLAINER_INDEPENDENT_REVIEW.md` (OE-01 through OE-11)

## Summary

Targeted fixes to simulator follow-ups, zero-win diagnostics, repair-plan backlog preservation, AI context structure, and quantitative trust messaging. Engine and Harborview PLAYER content unchanged.

---

## Issues fixed

| Review ID | Root cause | Correction |
|---|---|---|
| OE-01 | `SIM-NO-WIN` only emitted when `simulator_trustworthy=true` | Added `SIM-NO-WIN-UNTRUSTED` (observed zero, untrusted), `SIM-WIN-UNTRUSTED` (rare win while untrusted), trusted `SIM-NO-WIN` stays `UNDETERMINED` |
| OE-02 | All `UNDETERMINED` findings marked trust-affected | `_is_proven_fact()` keeps trust gate, simulator, and zero-win observation as proven |
| OE-03 | Keyword `_resolve_follow_up` never matched node IDs | Replaced with `follow_up_actions` in adapter; legacy `follow_ups` reported via `SIM-LEGACY-FOLLOWUPS` + `simulator_unsupported` |
| OE-04 | Stale ambiguity #5 (`once_per_hub not tracked`) | Removed from `ambiguities[]` (was false; tracking works) |
| OE-05 | High confidence on trust-affected findings | Confidence capped to `low` when trust affects conclusion |
| OE-06 | `repair-plan --finding` rewrote global backlog | Writes `repair_plan_<ID>.md/json` only; `ensure_global_backlog()` never shrinks existing backlog |
| OE-09 | Summary showed rates without untrusted banner | Added `QUANTITATIVE RESULTS UNTRUSTED` block and trust blockers |
| OE-11 | Trust AI context missing ambiguities / excerpts | Structured context: `PROVEN_FACTS`, `SIMULATION_OBSERVATIONS`, `AMBIGUITIES`, `HYPOTHESES`, `FORBIDDEN_CONCLUSIONS`, etc. |

## Follow-up simulation

New `simulator/follow_ups.py` + `follow_up_actions` in `sim_adapter.json`:

| Action ID | Source hubs | Eligibility | Effect |
|---|---|---|---|
| `FU_GYM_ALIBI` | J-300, J-500 | Missing C-13 + James press check failed | +10 min, grants C-13 |
| `FU_VENDOR_LOG` | J-300, J-500 | Missing C-14 | +10 min, grants C-14 |
| `FU_GENERAL_PHONE` | J-300, J-500 | Always (within slot limit) | +5 min |

- `follow_up_max` enforced globally
- Per-action `max_uses` enforced
- Legacy keyword `follow_ups` array **not simulated** — reported only
- Check failures set `CHECK_FAIL_<id>` flags for eligibility

## Tests added

`tests/test_explainer_fixes.py` (13 tests):

- Follow-up: eligible, ineligible, max count, cost/effect once, no hidden grants, hub step
- Zero-win: untrusted zero, rare win untrusted, trusted zero layer
- Repair plan: backlog preservation, idempotent re-run
- AI context: ambiguities present, no culprit leak
- Summary untrusted banner

Updated `tests/test_explainer.py` for new context key names.

**Total suite:** 71 tests, all passing.

## Example outputs (200 runs, seed 42)

```
simulator_trustworthy: false
findings: SIM-TRUST-DOWNGRADE, SIM-WIN-UNTRUSTED, SIM-LEGACY-FOLLOWUPS, ...
repair_options.json: 12 entries (preserved after repair-plan --finding)
executive_diagnostic.md: Quantitative trust status section at top
summary.md: QUANTITATIVE RESULTS UNTRUSTED banner
local_ai_context/finding_context_SIM-TRUST-DOWNGRADE.md: PROVEN FACTS / FORBIDDEN CONCLUSIONS sections
repair_plan_SIM-FAKE-J-122.md: finding-specific plan (backlog unchanged)
```

## Remaining blockers

| Blocker | Status |
|---|---|
| P-112 manager key always granted | Still partial (`simulator_partial`) |
| Quantitative adventure tuning | **Disabled** while ambiguities remain |
| Placeholder `.patch` files | Still placeholders (by design) |
| I-02 incomplete retry charges 0 minutes | Not in scope for this fix |

## Readiness

| Gate | Verdict |
|---|---|
| Offline diagnosis | **YES** — qualitative + proven trust facts; rates labeled untrusted |
| Offline repair planning | **YES** — backlog preserved; per-finding plans; no auto-edits |
| Quantitative tuning | **NO** — trust gate still down (4 ambiguities + P-112 partial + legacy follow_ups documented) |

## Commands verified

```bash
python3 -m unittest discover -s tests -v
./run_full_diagnostic.sh 200 42
./explain_latest.sh SIM-TRUST-DOWNGRADE
./export_latest_for_ai.sh SIM-TRUST-DOWNGRADE
python3 idne_sim.py repair-plan simulation_output/<latest> --finding SIM-FAKE-J-122
```

Shell scripts now use `#!/usr/bin/env bash` (works on Termux and Linux).

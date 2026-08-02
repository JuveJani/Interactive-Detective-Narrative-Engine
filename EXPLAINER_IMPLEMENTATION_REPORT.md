# Explainer Implementation Report

## Scope

Extended the offline IDNE simulator with finding explanations, repair advisor, offline AI handoff, and V2 simulator correctness fixes. Engine and Harborview adventure content were not modified.

## Simulator correctness (V2 blockers)

| Issue | Fix |
|-------|-----|
| Deadline restores all hub choices | At deadline, hubs offer decline only or force `J-600` |
| Fiction time past 23:00 | `advance_minutes` caps clock at `deadline_clock` |
| Hub 2 stairwell revisit leaves hub | `return_hub` returns to originating hub after `J-110` |
| `hub_targets` collision on `J-110` | Keyed by `(hub_id, target)` tuple |
| Follow-up slots | `follow_ups_used` / `follow_up_max`; pending follow-up routing |
| James fail → P-214 | Path-node check; forced routing in `run_role_path` |
| SIM-FAKE layer while untrusted | Downgraded to `UNDETERMINED` |
| PoorDecisionsStrategy / ACTION_PRIORITY | Generic priority from adapter; poor picks lowest priority |
| `memory_guard_mb` / `max_states` | Enforced in runner and engine |

## New modules

- `simulator/explainer.py` — structured human explanations
- `simulator/repair_advisor.py` — repair options (no auto-edits)
- `simulator/ai_context.py` — per-finding AI handoff packages
- `simulator/advisory_output.py` — executive and layer-split reports
- `simulator/commands.py` — `explain`, `repair-plan`, `export-ai-context`

## CLI

```
python3 idne_sim.py explain <output_folder> [--finding ID]
python3 idne_sim.py repair-plan <output_folder> [--finding ID]
python3 idne_sim.py export-ai-context <output_folder> [--finding ID]
```

## Scripts

- `run_full_diagnostic.sh`
- `explain_latest.sh`
- `export_latest_for_ai.sh`

## Tests

58 tests pass (`python3 -m unittest discover -s tests`).

New coverage: deadline, hub revisit, follow-ups, trust downgrade, explainer, repair advisor, AI export, no repo modification, deterministic output, interrupted recovery.

## Remaining unsupported / partial

- Adapter ambiguities (5 entries) keep `simulator_trustworthy: false`
- P-112 manager key without Records partner state check (partial)
- Phone follow-ups use keyword heuristics, not full player text
- `proposed_fix_*.patch` files are placeholders until human selects an approach

## Readiness

**Ready for offline Termux diagnostic use.** Human-readable reports work without AI. Quantitative adventure conclusions remain gated until adapter ambiguities are resolved.

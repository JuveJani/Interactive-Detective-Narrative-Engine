# IDNE Simulator — Implementation Report

**Date:** 2026-08-02  
**Branch:** `cursor/idne-simulator-bad4`  
**Target:** Termux / Google Pixel 10 Pro, offline, Python 3 stdlib

## Delivered

| Artifact | Status |
|---|---|
| `idne_sim.py` | CLI: validate, simulate, trace, compare |
| `simulator/` package | 12 modules |
| `adventures/CASE_BENCHMARK_v0.4/sim_adapter.json` | Harborview v0.4.1 graph |
| `tests/` | 6 test modules |
| `requirements.txt` | stdlib-only (empty deps) |
| `install_termux.sh`, `run_harborview.sh` | Termux helpers |
| Documentation | README, ARCHITECTURE, this report |

## Design decisions

1. **Machine-readable adapter** — PLAYER markdown lacks deterministic edge costs and check branching; `sim_adapter.json` is authoritative for simulation. PLAYER files used for static cross-checks (spoiler, steering, broken refs).

2. **Blind strategies** — `truth.culprit` read only in `endings.py`. Strategies infer accusation from collected proof tags and clue patterns.

3. **Parallel wall-clock** — `resolve_split()` applies `max(people_minutes, records_minutes) + regroup_overhead`, never the sum.

4. **Loop prevention** — Strategies filter options that grant no new clues; hub revisits without progress deprioritized.

## Harborview smoke results (seed 42, clue-seeking trace)

- Ending: E-902 (partial proof accusation)
- Game clock advance: ~201 minutes (19:00 → ~22:21)
- Clues: 9/15 major path
- Steps: 14

## Known limitations

| ID | Layer | Issue |
|---|---|---|
| BLK-01 | SIMULATOR | Hub `once_per_hub` revisit not modeled |
| BLK-02 | SIMULATOR | Follow-up slots (max 2) at hubs not auto-simulated |
| BLK-03 | ADVENTURE | I-02 failure loop back to J-300 not enforced — infer proceeds |
| BLK-04 | DELIVERY_ADAPTER | Logic docs (node graph v0.4.0) differ from v0.4.1 PLAYER — adapter follows PLAYER |
| BLK-05 | HUMAN_PLAYTEST | Wall-clock playtime vs in-fiction minutes unvalidated |

## Test coverage

- Graph parsing and reachability
- State / proof tags / infer gates
- D20 checks pass/fail grants
- Parallel clock ≠ sum of branches
- Deterministic seeds
- Ending dispatch E-901/E-904
- Partial output on interrupt path
- Static validate (no J-600 spoiler in v0.4.1)

## Example commands

```bash
python3 idne_sim.py validate adventures/CASE_BENCHMARK_v0.4
python3 idne_sim.py simulate adventures/CASE_BENCHMARK_v0.4 --runs 10000 --seed 42
python3 idne_sim.py trace adventures/CASE_BENCHMARK_v0.4 --seed 42
python3 idne_sim.py compare adventures/CASE_BENCHMARK_v0.4 --runs-per-strategy 1000
```

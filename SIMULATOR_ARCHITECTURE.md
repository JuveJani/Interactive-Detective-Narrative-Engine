# IDNE Simulator Architecture

## Overview

```text
idne_sim.py (CLI)
    └── simulator/runner.py
            ├── loader.py          # adventure + sim_adapter.json
            ├── validate.py        # static Tier-A style checks
            ├── engine.py          # two-player run loop
            ├── strategies.py      # blind play policies
            ├── diagnostics.py     # metrics + findings
            └── output.py          # timestamped artifacts
```

## Simulation model

### Shared world clock

- Single `WORLD_CLOCK` in minutes-from-midnight (Harborview starts 1140 = 19:00).
- Joint scenes advance clock directly.
- Split branches accumulate per-role minutes; regroup applies `max(people, records) + overhead`.

### Parallel splits

```text
J-130 launch
  ├─ People path (private minutes)
  └─ Records path (private minutes)
J-200 regroup → clock += max(people, records) + 5
```

Completed role waits implicitly (no extra clock until partner finishes).

### Endings

`simulator/endings.py` evaluates J-600 dispatch using adapter `truth` (simulator-only). Strategies never see culprit key.

## Adapter vs PLAYER package

| Source | Role |
|---|---|
| `sim_adapter.json` | Authoritative graph, costs, checks, proof rules |
| `PLAYER/*.md` | Cross-validation, spoiler/steering scans |
| `DO_NOT_READ/LOGIC/` | Optional logic cross-check (not loaded by strategies) |

### Harborview ambiguities (documented in adapter)

1. J-121 return choice (J-120 vs J-130) — simulator returns to hub.
2. P-112 conditional key grant — granted when People path visits P-112.
3. Bakery-closed phone partial C-07 — modeled as skip_to P-113 with partial grant.
4. Hub stairwell `once_per_hub` — not tracked in v1 adapter.
5. R-212b skim retry — marked `fake_choice`.

## Finding schema

Every finding includes:

- `id`, `severity`, `confidence`, `evidence`
- `file`, `identifier`, `expected_rule`
- `layer`, `auto_fix_possible`, `human_approval_required`

## Termux constraints

- Stdlib only (`requirements.txt` empty).
- Iterative simulation (no unbounded recursion).
- `SimConfig.max_states`, `timeout_seconds`, progress to stderr.
- SIGINT → partial write via `RunInterrupted`.

## Metrics

| Metric | Source |
|---|---|
| Graph nodes/edges | `graph.py` |
| Unreachable / dead ends | reachability BFS |
| Fake choices | `fake_choice` flag + hub duplicate targets |
| Impactful decision % | choices leading to clues/checks/infer |
| Path diversity | unique paths across runs |
| Clue bottlenecks | single-source grants |
| Split balance | per-run `split_segments` |
| Ending frequency | Monte Carlo / compare |
| Solo-solve check | role clue sets vs proof rules |

## Extension

New adventures: add `sim_adapter.json` following Harborview schema. Do not modify engine for adventure-specific rules.

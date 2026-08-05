# IDNE Offline Simulator

Python 3 simulator for IDNE v0.4 adventures. Runs fully offline on Termux (Google Pixel 10 Pro tested defaults). No AI, cloud APIs, GUI, or external databases.

## Quick start

```bash
chmod +x install_termux.sh run_harborview.sh idne_sim.py
./install_termux.sh          # Termux only
python3 idne_sim.py validate adventures/CASE_BENCHMARK_v0.4
./run_harborview.sh trace
```

## CLI

```bash
python3 idne_sim.py validate adventures/CASE_BENCHMARK_v0.4
python3 idne_sim.py simulate adventures/CASE_BENCHMARK_v0.4 --runs 10000 --seed 42
python3 idne_sim.py trace adventures/CASE_BENCHMARK_v0.4 --seed 42
python3 idne_sim.py compare adventures/CASE_BENCHMARK_v0.4 --runs-per-strategy 1000
```

### Safety flags (Pixel / Termux defaults)

| Flag | Default | Purpose |
|---|---|---|
| `--timeout` | 600 | Wall-clock cap per command |
| `--max-runs` | 50000 | Monte Carlo upper bound |

Press **Ctrl+C** to stop; partial results are written to the latest `simulation_output/<timestamp>/` folder.

## Output folder

Each run creates `simulation_output/YYYYMMDD_HHMMSS/` with:

- `summary.md`, `findings.md`, `findings.json`, `metrics.json`
- `graph.csv`, `paths.csv`, `endings.csv`, `clues.csv`
- `split_balance.csv`, `time_analysis.csv`, `state_register.csv`
- `simulator_log.txt`, `parse_errors.md`
- `trace_<seed>.json` (trace mode)

## Adventure adapter

Markdown PLAYER files are ambiguous for deterministic simulation. Each adventure ships a `sim_adapter.json` beside `PLAYER/`. Harborview mapping is documented in `adventures/CASE_BENCHMARK_v0.4/sim_adapter.json` under `ambiguities`.

Milestone 11 exports unified `.idne` ZIP packages (`ADVENTURE_GENERATOR_V2_SPEC.md`) for future Simulator v2 import; the current simulator still reads adventure directories directly.

## Simulator v2 (Part 1)

Canonical package-driven simulation foundation lives in `simulator_v2/`:

```python
from simulator_v2 import SimulatorService
svc = SimulatorService()
svc.load_package("path/to/adventure.idne")  # or unpacked canonical directory
svc.validate_readiness()
run_id = svc.start_run()
```

- Loads `.idne` archives or unpacked Generator v2 packages **without** `sim_adapter.json`
- Derives internal simulation model from canonical packages with source traceability
- Legacy simulator (`simulator/`) remains available for Harborview-class adventures with `sim_adapter.json`

See `SIMULATOR_V2_PART1_IMPLEMENTATION.md`.

## Strategies

| Name | Behaviour |
|---|---|
| `random` | Uniform legal choices |
| `clue-seeking` | Prefer uncollected clues |
| `broad-exploration` | Prefer unseen action IDs |
| `time-efficient` | Minimize minutes; rush accusation late |
| `cautious` | Avoid risky checks until proof complete |
| `risky` | Prefer d20 branches |
| `cooperation-focused` | Role-appropriate paths |
| `poor-decisions` | Baseline bad play |

Strategies **do not** read `DO_NOT_READ/` or `truth` in the adapter.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Layer attribution

Findings include `layer`: `ENGINE`, `ADVENTURE`, `DELIVERY_ADAPTER`, `PLAYER_PACKAGE`, `VALIDATOR`, `SIMULATOR`, or `HUMAN_PLAYTEST`.

See `SIMULATOR_ARCHITECTURE.md` for design detail.

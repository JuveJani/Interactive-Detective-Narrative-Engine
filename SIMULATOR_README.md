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

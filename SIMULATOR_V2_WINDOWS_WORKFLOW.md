# IDNE Simulator v2 — Windows 11 Offline Workflow

Target hardware: Acer Swift Go 14 (Core Ultra 5 228V, 32 GB RAM, no discrete GPU).

## Requirements

- Windows 11
- Python 3.11+ (user install — no administrator rights)
- No internet required after setup

## Installation

```powershell
cd C:\path\to\Interactive-Detective-Narrative-Engine
powershell -ExecutionPolicy Bypass -File scripts\windows\install.ps1
.\scripts\windows\setup-venv.ps1
```

## Validate a package

```powershell
python -m idne.sim_v2 validate tests\fixtures\sim_v2_solo
# or
powershell -ExecutionPolicy Bypass -File scripts\windows\validate-package.ps1 -Package tests\fixtures\sim_v2_solo.idne
```

## Complete diagnostic run

```powershell
python -m idne.sim_v2 diagnose tests\fixtures\sim_v2_solo --seed 42 --runs 1000
# or
powershell -ExecutionPolicy Bypass -File scripts\windows\run-diagnostic.ps1 -Package tests\fixtures\sim_v2_solo
```

Reports appear under `simulation_output_v2\<timestamp>_diagnose_*`.

## Open latest report

```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows\open-latest-report.ps1
```

## Export finding for local AI

```powershell
python -m idne.sim_v2 export-ai-context simulation_output_v2\<run_folder> --finding SIM-TRUST-...
```

## Interruption and resume

- Press **Ctrl+C** to interrupt; partial results are saved when possible.
- Re-run with `--resume` or `scripts\windows\resume-diagnostic.ps1`.
- Create `.cancel` in the output folder to signal cancellation during exhaustive mode.

## CLI commands

| Command | Example |
|---------|---------|
| validate | `python -m idne.sim_v2 validate adventure.idne` |
| trace | `python -m idne.sim_v2 trace adventure.idne --seed 42` |
| simulate | `python -m idne.sim_v2 simulate adventure.idne --runs 1000 --seed 42` |
| exhaustive | `python -m idne.sim_v2 exhaustive adventure.idne --max-states 200000` |
| compare | `python -m idne.sim_v2 compare adventure.idne --runs-per-strategy 100` |
| export-ai-context | `python -m idne.sim_v2 export-ai-context OUTPUT --finding FINDING_ID` |

## Deprecated entry point

`idne_sim.py` remains for legacy `sim_adapter.json` adventures only. Canonical packages must use `python -m idne.sim_v2`.

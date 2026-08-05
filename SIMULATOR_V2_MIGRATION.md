# Simulator v2 Migration Guide

## From legacy `idne_sim.py`

| Legacy | Simulator v2 |
|--------|----------------|
| `idne_sim.py validate adventure/` | `python -m idne.sim_v2 validate adventure.idne` |
| `idne_sim.py simulate ...` | `python -m idne.sim_v2 simulate ...` |
| `idne_sim.py trace ...` | `python -m idne.sim_v2 trace ...` |
| `idne_sim.py compare ...` | `python -m idne.sim_v2 compare ...` |
| `simulation_output/` | `simulation_output_v2/` |
| `sim_adapter.json` adventures | Still use deprecated `idne_sim.py` |

## Package requirements

Adventures must be Generator v2 canonical packages with all simulation layers and integrated validation PASS.

Harborview and Glass Alibi remain on legacy adapter until separately migrated.

## Report file mapping

| Legacy | v2 |
|--------|-----|
| summary.md | executive_diagnostic.md |
| findings.json | findings.json (expanded schema) |
| repair backlog | repair_backlog.md |
| AI context | ai_context/<finding_id>/ |

## API migration

```python
# Part 1–2
from simulator_v2 import load_simulator_package, SimulationEngine

# Part 3
from simulator_v2 import cmd_diagnose, RunnerConfig
from simulator_v2.ai_context import export_ai_context
```

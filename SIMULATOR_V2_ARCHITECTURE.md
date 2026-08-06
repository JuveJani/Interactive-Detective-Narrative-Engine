# Simulator v2 Architecture

## Layers

```
idne/sim_v2/cli.py          CLI entry (python -m idne.sim_v2)
simulator_v2/runner.py      Command orchestration
simulator_v2/diagnostics.py Integrated validators + simulation
simulator_v2/reports.py     Artifact writer
simulator_v2/modes.py       Simulation modes
simulator_v2/engine.py      Step execution
simulator_v2/package_loader.py  Load + integrated validation gate
simulator_v2/derivation.py  Canonical model
simulator_v2/trust_gate.py  Quantitative trust
simulator_v2/explainer.py   Human explanations
simulator_v2/repair_advisor.py  Repair suggestions
simulator_v2/ai_context.py  Offline AI export
simulator_v2/human_delivery/  Static gamebook human-delivery simulation
```

## Human-delivery layer

Parallel to canonical simulation (`simulator_v2/engine.py`), `simulator_v2/human_delivery/` walks the exported static gamebook using only player-visible section numbers and choices. It validates delivery separately from canonical graph simulation; a canonical PASS does not imply human-delivery PASS.

```
simulator_v2/human_delivery/loader.py    Unpacked workspace resolution (rejects .idne)
simulator_v2/human_delivery/parse.py     Deterministic GAMEBOOK.md parsing
simulator_v2/human_delivery/player_view.py  Restricted strategy boundary
simulator_v2/human_delivery/validate.py  Delivery findings + gamebook cross-check
simulator_v2/human_delivery/engine.py    Trace + Monte Carlo
simulator_v2/human_delivery/trust.py     Human-delivery trust gate
simulator_v2/human_delivery/runner.py    CLI handlers
```

## Data flow

1. **Load** — checksum, version, layers, `validate_adventure()`
2. **Derive** — immutable `CanonicalSimulationModel` + traceability
3. **Validate** — per-validator findings → unified `DiagnosticFinding`
4. **Simulate** — trace, Monte Carlo, compare, bounded exhaustive
5. **Trust** — gate quantitative conclusions
6. **Report** — atomic writes to unique timestamped folder

## Legacy boundary

- `simulator/` + `idne_sim.py` — legacy adapter adventures only (deprecated)
- `simulator_v2/` — canonical packages only

## Performance defaults

- Memory guard: 4096 MB
- Max Monte Carlo runs: 10,000
- Max exhaustive states: 200,000
- Exhaustive timeout: 300 s
- Workers: 1 (deterministic default)
- Atomic writes, unique output folders, checkpoint resume

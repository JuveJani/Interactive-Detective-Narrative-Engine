# Simulator v2 — Part 1 Implementation

**Branch:** `cursor/simulator-v2-bad4`  
**Status:** Part 1 complete (package, derivation, state core)

## Modules

| Module | Purpose |
|---|---|
| `simulator_v2/package_loader.py` | Load `.idne` or canonical directory; validate layers, checksum, version, integrated validation |
| `simulator_v2/derivation.py` | Deterministic canonical → simulation model derivation with traceability |
| `simulator_v2/state.py` | Copyable simulation state (never mutates fixed truth) |
| `simulator_v2/service.py` | UI-independent application service boundary |
| `simulator_v2/legacy.py` | Legacy simulator compatibility markers |

## Tests

`tests/test_simulator_v2_part1.py` — 15 focused tests  
Fixtures: `scripts/build_sim_v2_fixtures.py`

## Legacy boundary

`simulator/` is marked `LEGACY_MODE = True` and requires `sim_adapter.json`. Generator v2 packages use `simulator_v2/` only.

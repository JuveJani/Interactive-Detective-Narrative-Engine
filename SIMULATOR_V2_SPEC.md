# Simulator v2 Specification

**Version:** 2.0.0  
**Status:** Complete (Parts 1–3)

## Purpose

Offline production diagnostic tool for canonical IDNE `.idne` adventure packages. Runs on modest Windows laptops without GPU or internet during use.

## Scope

- Load and validate canonical multi-layer packages
- Deterministic simulation (single investigator and two-player)
- Integrated validators: Investigation, Story, Playtime Calibration, DM Feeling
- Quantitative simulation with trust gate
- Human-readable and machine-readable reports
- Offline local-AI context export per finding

## Out of scope

- Adventure generation
- Windows/Android GUI
- Legacy `sim_adapter.json` execution (use deprecated `idne_sim.py`)
- Future mechanics: inventory handlers, retry policies, false-check handlers, puzzle handlers (extension points documented only)

## Commands

```
python -m idne.sim_v2 validate <package>
python -m idne.sim_v2 trace <package> [--seed N] [--strategy NAME]
python -m idne.sim_v2 simulate <package> [--runs N] [--seed N]
python -m idne.sim_v2 exhaustive <package> [--max-states N]
python -m idne.sim_v2 compare <package> [--runs-per-strategy N]
python -m idne.sim_v2 diagnose <package>
python -m idne.sim_v2 export-ai-context <output> --finding ID
```

## Trust policy

Quantitative adventure findings are trusted only when package integrity passes, required mechanics are supported, traversal coverage is declared, no fallback replaced missing fields, and strategies pass hidden-information checks. Otherwise ownership remains SIMULATOR, PACKAGE, GENERATOR, or UNDETERMINED.

## Extension points (not implemented)

| Future mechanic | Extension hook |
|-----------------|----------------|
| Inventory | `executor._collect_item_from_object`, `state.items` |
| Retry checks | `eligibility.one_attempt_available`, `state.check_attempts` |
| False-check routes | `executor._apply_check` failure branch |
| Puzzles | `action_enumerator` + new `ActionKind` |

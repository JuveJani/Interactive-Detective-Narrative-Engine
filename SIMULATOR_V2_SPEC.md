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
python -m idne.sim_v2 delivery-validate <unpacked-adventure-dir>
python -m idne.sim_v2 human-trace <unpacked-adventure-dir> [--seed N] [--strategy NAME]
python -m idne.sim_v2 human-simulate <unpacked-adventure-dir> [--runs N] [--seed N] [--strategy NAME]
```

## Simulation layers

| Layer | Input | Navigation | Purpose |
|-------|-------|------------|---------|
| **Canonical** | `.idne` archive or `adventure/` directory | Internal unit IDs and canonical state transitions | Validates underlying adventure logic |
| **Human-delivery** | Unpacked adventure workspace only (manifest + `adventure/`) | Public section numbers, visible choices, d20/check branches | Validates static gamebook delivery |

A canonical simulation **PASS** does **not** imply human-delivery **PASS**. The layers are independent.

### Human-delivery player-view boundary

During action selection, strategies receive a restricted `HumanDeliveryPlayerView` containing only:

- Declared starting filename and public section
- Current rendered GAMEBOOK section
- Visible choice text and destination section numbers
- Visible d20/check instructions and simulated roll results
- Player-visible state, knowledge, time, inventory, and visited sections

Strategies must **not** access hidden truth, author-only files, internal destination IDs before selecting a public destination, future sections, proof requirements, or canonical graph adjacency not visible in the current section. Deliberate hidden-information access raises `HiddenInformationAccessError`.

Internal unit IDs are resolved only **after** a visible destination is selected, for validation and route-equivalence comparison.

### Human-delivery trust

Human-delivery Monte Carlo statistics are **trusted** only when all hold:

- Delivery validation PASS
- Public-number mapping and GAMEBOOK coverage PASS
- Start declaration PASS
- Visible navigation parses completely
- Public and canonical transitions are equivalent for traced routes
- No hidden-information boundary violation
- Canonical package validation is PASS or CONDITIONAL_PASS

Otherwise traces may be generated for debugging, but quantitative results are marked **untrusted** (ownership SIMULATOR).

### Unpacked directory behavior

Human-delivery commands require an unpacked adventure workspace (`player_mapping_manifest.json` plus `adventure/`). Passing a `.idne` archive is rejected; the simulator does not silently read a stale packaged copy when an unpacked directory is provided.

### Known limitation

Structural human-delivery simulation proves that navigation, section mapping, and route equivalence are consistent. It does **not** prove semantic human comprehension of synthesis worksheets or free-form player reasoning.

## Trust policy

Quantitative adventure findings are trusted only when package integrity passes, required mechanics are supported, traversal coverage is declared, no fallback replaced missing fields, and strategies pass hidden-information checks. Otherwise ownership remains SIMULATOR, PACKAGE, GENERATOR, or UNDETERMINED.

## Extension points (not implemented)

| Future mechanic | Extension hook |
|-----------------|----------------|
| Inventory | `executor._collect_item_from_object`, `state.items` |
| Retry checks | `eligibility.one_attempt_available`, `state.check_attempts` |
| False-check routes | `executor._apply_check` failure branch |
| Puzzles | `action_enumerator` + new `ActionKind` |

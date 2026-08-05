# Known Limitations

Honest gaps as of `main` @ `38f2921`. Update when status changes.

## Generation and local models

- **Local-model quality not yet validated** on real brief → full `.idne` → integrated PASS workflows.
- **No proven one-shot local generation** of a complete adventure; Generator v2 requires staged pipeline by design.
- Model role assignments in `MODEL_ROLES.md` are provisional pending benchmarks.

## Tooling and environment

- **Phone control is not configured** for remote testing or device automation.
- **Cursor native Agent** cannot be assumed to use localhost LM Studio without explicit Cline/local configuration.
- LM Studio endpoint URLs, model IDs, and context windows are **not yet recorded** in `LOCAL_SETUP.md`.

## Simulator and mechanics

- **Legacy simulator** (`simulator/`, `idne_sim.py`) remains for `sim_adapter.json` adventures only.
- **Future mechanics not implemented:** inventory handlers, paid retries, false-check handlers, puzzle modules (extension points documented in `SIMULATOR_V2_SPEC.md` only).
- Two-player simulation supports split/regroup but may not match full legacy parallel-path metrics.

## Adventures and playtest

- **Harborview** and **Glass Alibi** use legacy adapter paths — not canonical `.idne` on main.
- **No real generated adventure** has yet passed human playtest end-to-end.
- Fixture packages (`tests/fixtures/sim_v2_*`) validate tooling — they are not shipping adventures.

## Validation

- Investigation validator may **SKIP** on fixtures without `investigation_validator_manifest.json`.
- **CONDITIONAL_PASS** integrated validation policy should be reviewed before treating packages as production-ready.

## Infrastructure (explicitly out of scope for OFFLINE_AI setup)

- No RAG, embeddings, vector DB, or new MCP servers added by this workspace setup.
- No Android or Windows GUI for player-facing play.

## Reporting uncertainty

When any item above affects a task, state it as a **limitation** or **assumption** in the completion report — do not hide it.

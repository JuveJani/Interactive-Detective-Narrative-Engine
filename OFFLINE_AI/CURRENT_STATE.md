# Current State

**Last updated:** 2026-08-05  
**Base branch:** `main` @ `38f2921` (merge PR #46 — Simulator v2 integration fixes)

## Completed milestones

| Milestone | Scope | Key reference |
|-----------|--------|---------------|
| 1 | World First | `WORLD_FIRST_GENERATION_SPEC.md` |
| 2 | Environment | `ENVIRONMENT_SYSTEM_SPEC.md` |
| 3 | Object interaction | `OBJECT_INTERACTION_SYSTEM_SPEC.md` |
| 4 | Investigation core | `INVESTIGATION_CORE_SPEC.md` |
| 5A–C | Investigation validator, NPC, flow | Validator specs M7–M9 area |
| 6 | Capability checks | `CAPABILITY_CHECK_SYSTEM_SPEC.md` |
| 7–10 | Story, playtime, DM feeling validators | `*_VALIDATOR_SPEC.md`, `*_CALIBRATION_SPEC.md` |
| 11 | Adventure Generator v2 | `ADVENTURE_GENERATOR_V2_SPEC.md`, `idne/generate/` |

## Major subsystems (complete on main)

### Adventure Generator v2

- Staged offline pipeline from approved brief to `.idne` package.
- CLI: `python -m idne.generate`
- Integrated validation gate before export.

### Simulator v2

- Canonical package loader, derivation, execution, strategies, modes, diagnostics, CLI.
- CLI: `python -m idne.sim_v2`
- Windows offline workflow: `SIMULATOR_V2_WINDOWS_WORKFLOW.md`, `scripts/windows/`
- Legacy `idne_sim.py` deprecated for canonical packages.

## Test status

- **433 tests OK** — `python -m unittest discover -s tests`
- Includes Simulator v2 Parts 1–3 and integration-fix regression tests.

## Not yet proven

- Real **local LM Studio** end-to-end adventure generation (brief → all layers → PASS validation → human playtest).
- Local model quality benchmarks for assigned roles (`MODEL_ROLES.md`).
- Phone control / remote device workflow.

## Next goal

1. **Local LM Studio integration** — configure adapter, document measured settings in `LOCAL_SETUP.md`.
2. **One-stage generation test** — run Generator v2 against a real brief with a local model; record PASS/FAIL/BLOCKED honestly.
3. Update `SESSION_HANDOFF.md` and this file after each milestone.

## Do not assume

- Cursor native Agent uses localhost LM Studio (not configured by default).
- Any generated adventure is playtest-ready without human review.
- Future mechanics (inventory, retry, false-check, puzzle modules) exist — they do not.

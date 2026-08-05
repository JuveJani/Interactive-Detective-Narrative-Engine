# IDNE — Agent Instructions

**Interactive Detective Narrative Engine (IDNE)** is a staged, world-first system for authoring, validating, simulating, and repairing detective adventures. Canonical packages preserve fixed world truth; player-facing content is derived from it.

## Current completed state

- **Milestones 1–11** implemented (World First through Adventure Generator v2).
- **Simulator v2** complete (Parts 1–3 + integration fixes on `main`).
- **433 tests** passing on `main` as of merge `38f2921`.
- Real end-to-end adventure generation with local LM Studio is **not yet proven**.

Read `OFFLINE_AI/CURRENT_STATE.md` before substantial work.

## Authoritative document priority

When documents conflict, prefer in this order:

1. Normative specs (`IDNE_ENGINE_v0.4.md`, layer specs, validator specs, `ADVENTURE_GENERATOR_V2_SPEC.md`, `SIMULATOR_V2_SPEC.md`)
2. `IDNE_DEVELOPMENT_WORKFLOW.md` and `IDNE_ADVENTURE_QA_SPEC.md`
3. Implementation reports and architecture docs
4. `OFFLINE_AI/` memory files (orientation only — not a second source of truth)
5. Chat history (never authoritative)

## Fixed-world-truth principle

World truth is immutable once approved. Generators, simulators, and validators must not silently rewrite fixed truth. Player-visible state derives from canonical packages; hidden truth stays out of player-visible simulation state.

## Generator v2 workflow

- One **human-approved brief** drives generation.
- Generate **one canonical layer at a time**; validate and repair before continuing.
- Never generate a full adventure in one model response.
- Export `.idne` packages for Simulator v2 and downstream tools.

See `ADVENTURE_GENERATOR_V2_SPEC.md` and `idne/generate/`.

## Validation and Simulator v2

- Integrated validation: `python -m idne.validate_adventure <adventure_root>`
- Simulator v2 CLI: `python -m idne.sim_v2 validate|trace|simulate|compare|exhaustive|diagnose <package>`
- Quantitative simulator findings are trusted only when package integrity, mechanics support, coverage, and trust gate pass.
- Never weaken validators to obtain PASS.

## Branch, test, and review discipline

- Branch from `main` for new work; use descriptive branch names.
- Run focused tests for the area changed, then `python -m unittest discover -s tests`.
- Commit with clear messages; do not claim tests passed unless they were run.
- Stop on unresolved FAIL or BLOCKED validation/simulation results.

## Prohibited shortcuts

- Guessing canonical IDs, schemas, or validator rules instead of reading specs.
- Editing adventures (Harborview, Glass Alibi) or legacy simulator paths unless explicitly requested.
- Adding hidden fallbacks that mask missing package data.
- Treating Monte Carlo rates as adventure facts when trust gate is false.
- Implementing future mechanics (inventory, retry, false-check, puzzle handlers) without an approved spec.

## Evidence discipline

Label outputs explicitly as **fact**, **observation**, **assumption**, or **proposal**. Do not present assumptions or simulator observations as proven adventure defects when trust is false.

## Session continuity

After significant work, update `OFFLINE_AI/SESSION_HANDOFF.md` with branch, commits, tests run, decisions, blockers, and next safe action.

## Where to look next

| Topic | File |
|-------|------|
| Project state | `OFFLINE_AI/CURRENT_STATE.md` |
| Architecture map | `OFFLINE_AI/ARCHITECTURE_MAP.md` |
| Operating rules | `OFFLINE_AI/OPERATING_RULES.md` |
| Task format | `OFFLINE_AI/TASK_TEMPLATE.md` |
| Local setup (LM Studio) | `OFFLINE_AI/LOCAL_SETUP.md` |

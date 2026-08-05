# IDNE core rules (Cline)

Before substantial work, read:

1. `AGENTS.md`
2. `OFFLINE_AI/CURRENT_STATE.md`

## Operating rules

- Use repository Markdown as persistent memory; do not rely on chat history for project continuity.
- Follow authoritative specs (`IDNE_ENGINE_v0.4.md`, layer specs, `ADVENTURE_GENERATOR_V2_SPEC.md`, `SIMULATOR_V2_SPEC.md`) over informal notes.
- Preserve fixed world truth. Never weaken validators to obtain PASS.
- Generator v2: one approved brief, one canonical layer at a time, validate before next stage.
- Simulator v2: use `python -m idne.sim_v2`; respect trust gate and integrated validation status.
- Inspect before editing; plan before large changes.
- Run focused tests, then the full suite: `python -m unittest discover -s tests`.
- Never claim commands were run unless they were actually run.
- Stop on unresolved FAIL or BLOCKED.
- Do not generate a full adventure in one model response.
- Distinguish **facts**, **observations**, **assumptions**, and **proposals**.
- Update `OFFLINE_AI/SESSION_HANDOFF.md` after significant work.

## Further reading

- `OFFLINE_AI/OPERATING_RULES.md`
- `OFFLINE_AI/ARCHITECTURE_MAP.md`
- `OFFLINE_AI/KNOWN_LIMITATIONS.md`
- `OFFLINE_AI/TASK_TEMPLATE.md`
- `OFFLINE_AI/LOCAL_SETUP.md`

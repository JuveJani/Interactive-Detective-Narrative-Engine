# OFFLINE_AI — Persistent Project Memory

This directory is the **shared, version-controlled memory** for IDNE offline AI work. It is used by Cursor, Cline, LM Studio agents, CLI agents, and human developers.

## Purpose

- Provide project continuity **without chat history**.
- Point agents to authoritative specs instead of duplicating them.
- Record current state, limitations, and session handoff.

## Files

| File | Purpose |
|------|---------|
| `CURRENT_STATE.md` | What is done, test count, next goal |
| `ARCHITECTURE_MAP.md` | World First → Generator → Validators → Simulator → Repair |
| `OPERATING_RULES.md` | Discipline for edits, validation, and reporting |
| `MODEL_ROLES.md` | Suggested local-model task roles (benchmark before trusting) |
| `KNOWN_LIMITATIONS.md` | Honest gaps and unproven areas |
| `SESSION_HANDOFF.md` | Latest branch, commits, tests, blockers, next action |
| `TASK_TEMPLATE.md` | Scoped task brief for agents |
| `LOCAL_SETUP.md` | LM Studio, Cline, model IDs (fill as measured) |
| `SYSTEM_PROMPT.md` | Reusable bootstrap prompt for local agents |

## Root entry points

- `AGENTS.md` — concise rules for all agents
- `.cursor/rules/00-idne-core.mdc` — Cursor persistent rule
- `.clinerules/00-idne-core.md` — Cline persistent rule

## Not a second source of truth

Specs in the repository root (`IDNE_ENGINE_v0.4.md`, validator specs, generator/simulator specs) remain authoritative. Update `OFFLINE_AI` when project state changes; do not copy entire specifications here.

# Current State

**Last updated:** 2026-08-06  
**Base branch:** `main`

## Completed milestones

| Milestone | Scope |
|-----------|--------|
| 1–11 | World First through Adventure Generator v2 |
| Simulator v2 | Canonical package loader, human delivery, diagnostics |
| Epistemic progression | State-gated scene progression engine + Cold Storage migration |
| Investigation graph fix | Deterministic BFS deduplication for IV state graph |
| Checksum test fix | Cross-platform file selection in package tests |
| **Local AI Step 1** | Deterministic orchestrator core (`idne/local_ai/`) |

## Local AI Orchestrator (Step 1)

- CLI: `python -m idne.local_ai`
- Supported task type: `adventure_brief` (prepare only)
- Run workspace: `.local_ai_runs/` (gitignored)
- Status reached: `READY_FOR_MODEL`
- **No model adapter yet** — no LM Studio calls

See `OFFLINE_AI/LOCAL_AI_ARCHITECTURE.md` and `OFFLINE_AI/QUICKSTART.md`.

## Test status

Run: `python -m unittest discover -s tests`

## Next goal

1. Local model adapter (OpenAI-compatible endpoint) for `READY_FOR_MODEL` tasks
2. Response validation and brief JSON application through existing Generator v2 paths
3. Measure one real brief generation with LM Studio; record settings in `LOCAL_SETUP.md`

## Do not assume

- Cline is required or used
- Any prepared prompt has been sent to a model
- Chat history is authoritative

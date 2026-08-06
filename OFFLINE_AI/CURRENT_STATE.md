# Current State

**Last updated:** 2026-08-06  
**Base branch:** `main`

## Local AI Orchestrator

| Step | Status |
|------|--------|
| Step 1 | Deterministic task preparation → `READY_FOR_MODEL` |
| Step 2 | LM Studio OpenAI-compatible transport → `RESPONSE_RECEIVED` |
| Step 3 | Semantic validation + apply (not started) |

- CLI: `python -m idne.local_ai`
- Config: `OFFLINE_AI/local_ai.example.toml` → `local_ai.toml`
- Mock adapter for CI and Termux: `--mock`
- **No semantic validation or repository apply yet**

## Test status

Run: `python -m unittest discover -s tests` (552+ tests)

## Next goal

Step 3: validate model JSON against brief schema; apply through Generator v2 paths.

## Cline

Not used for Local AI workflow.

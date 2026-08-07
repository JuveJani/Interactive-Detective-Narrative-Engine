# Current State

**Last updated:** 2026-08-06  
**Base branch:** `main`  
**PR:** #54 (`cursor/offline-local-ai-core`)

## Local AI Orchestrator

| Step | Status |
|------|--------|
| Step 1 | Deterministic task preparation → `READY_FOR_MODEL` |
| Step 2 | LM Studio OpenAI-compatible transport → `RESPONSE_RECEIVED` |
| Step 3 | Response parse/validate, proposal build, explicit apply → `APPLIED` |

- CLI: `python -m idne.local_ai`
- Config: `OFFLINE_AI/local_ai.example.toml` → `local_ai.toml`
- Mock adapter for CI and Termux: `--mock`
- Semantic response schema: `idne/schemas/local_ai_adventure_brief_response.schema.json`
- Draft output root: `adventures/_local_ai_drafts/` (gitignored)
- **AI-powered semantic repair is not implemented**

## End-to-end mock workflow (no network)

```bash
python -m idne.local_ai prepare --task-type adventure_brief \
  --input OFFLINE_AI/examples/adventure_brief_input.md \
  --output adventures/_local_ai_drafts/example_offline_brief/adventure_brief.json
python -m idne.local_ai run .local_ai_runs/<task-id> --mock
python -m idne.local_ai process .local_ai_runs/<task-id>
python -m idne.local_ai review .local_ai_runs/<task-id>
python -m idne.local_ai apply .local_ai_runs/<task-id>
```

## Test status

Run: `python -m unittest discover -s tests` (590+ tests)

## Cline

Not used for Local AI workflow.

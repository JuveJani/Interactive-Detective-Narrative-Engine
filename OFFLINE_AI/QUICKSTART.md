# Local AI Quickstart (Step 1)

Deterministic task preparation only — **no model calls**.

## Prerequisites

- Python 3.10+
- Repository clone with normative specs present
- No network access required

## Windows

```powershell
cd D:\Repositories\IDNE\Interactive-Detective-Narrative-Engine
python -m idne.local_ai doctor
python -m idne.local_ai prepare --task-type adventure_brief --input OFFLINE_AI/examples/adventure_brief_input.md
```

Inspect the prepared prompt:

```powershell
python -m idne.local_ai show-prompt .local_ai_runs\<task-id>
python -m idne.local_ai inspect-context .local_ai_runs\<task-id>
python -m idne.local_ai status .local_ai_runs\<task-id>
```

## Termux / Linux

```bash
cd ~/Interactive-Detective-Narrative-Engine
python -m idne.local_ai doctor
python -m idne.local_ai prepare --task-type adventure_brief --input OFFLINE_AI/examples/adventure_brief_input.md
python -m idne.local_ai show-prompt .local_ai_runs/<task-id>
```

## What you should see

- Doctor status `READY` or `DEGRADED` (if Git unavailable)
- Prepare prints task directory, included files, context size, and duration
- Final task status `READY_FOR_MODEL`
- `prompt.txt` requests structured JSON only

## Next step (not in Step 1)

Configure a local OpenAI-compatible endpoint and add a model adapter that reads `prompt.txt`, never the whole repository.

## Cline

Do not use Cline for this workflow.

# Local AI Orchestrator — Architecture (Step 1)

**Status:** Deterministic core only — no model adapter yet.

## Purpose

Prepare exact, validated Local AI task packages so a future local model receives
only semantic work. Python performs all deterministic repository operations.

## What Python does now

- Detect platform runtime (`platform_runtime.py`)
- Resolve safe repository-relative paths (`paths.py`)
- Build versioned `LocalAITask` records (`task_model.py`)
- Read explicit allowlisted files only (`context_builder.py`)
- Enforce context budgets without silent truncation
- Build deterministic prompts (`prompt_builder.py`)
- Write run artifacts under `.local_ai_runs/<task-id>/`
- Report doctor readiness (`doctor.py`)

## What will later delegate to AI

- Semantic field authoring for briefs and canonical layers
- Story/player prose generation per Generator v2 stage
- Repair wording proposals after validator findings

## What AI must never do

- Explore the repository or choose context files
- Assign IDs, paths, manifests, or hashes
- Write directly into the repository
- Manage stage state or pick validators

## Authority order

1. Specification files (`*_SPEC.md`, `AGENTS.md`)
2. Workflow documentation (`*_WORKFLOW.md`)
3. Implementation reports
4. `OFFLINE_AI/` memory (orientation only)
5. Chat history (never included automatically)

## Task directory contents

| File | Purpose |
|------|---------|
| `task.json` | Versioned machine-readable task |
| `context_manifest.json` | Sources, sizes, budget result |
| `context.txt` | Concatenated authoritative context |
| `prompt.txt` | Deterministic model-ready prompt |
| `status.json` | Status + preparation metrics |
| `diagnostics.json` | Blockers and file lists |

## Reuse

This layer orchestrates existing Generator v2 stage definitions (`idne/generate/stages.py`), brief field requirements (`idne/generate/brief.py`), and normative specs. It does **not** replace Adventure Generator v2.

## Cline

Cline is **not** part of this workflow. Use `python -m idne.local_ai` only.

## Current limitation

No LM Studio or other model adapter is configured in Step 1. Preparation stops at `READY_FOR_MODEL`.

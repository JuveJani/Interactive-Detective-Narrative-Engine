# Local AI Orchestrator — Architecture

**Status:** Step 3 — response validation, proposal, explicit apply

## Purpose

End-to-end offline Local AI workflow for `adventure_brief`:

`prepare` → `run` → `process` → `review` → `apply`

Python owns IDs, paths, manifests, validators, and atomic writes. The model
provides semantic brief content only.

## Pipeline stages

| Stage | Command | Output |
|-------|---------|--------|
| Prepare | `prepare` | `READY_FOR_MODEL` |
| Transport | `run` | `RESPONSE_RECEIVED` |
| Parse | `parse` | `parsed_response.json`, `processing_stage=PARSED` |
| Response validate | `validate-response` | `response_validation_report.json` |
| Proposal build | `build-proposal` | `proposal/` directory |
| Proposal validate | `validate-proposal` | `VALIDATED` |
| Apply | `apply` | draft brief file, `APPLIED` |

Convenience: `process` runs parse → validate-response → build-proposal → validate-proposal (stops on first failure).

## Semantic response schema

Model-facing schema: `idne/schemas/local_ai_adventure_brief_response.schema.json`

Fields include premise, opening_situation, initial_observable_facts, and canonical brief parameters. Python maps this into Adventure Generator v2 `adventure_brief.json` via `proposal_builder.map_semantic_to_canonical()`:

- Direct copy: universe, genre, realism_level, player_mode, investigator_character, target_playtime_minutes, in_world_duration, tone, difficulty, location_scale, content_boundaries, theme arrays
- Composed into `author_notes`: working_title, premise, setting, opening_situation, initial_observable_facts, author_notes

## Safe structural repairs (`structural_repair.py`)

Allowed only:

- UTF-8 BOM strip
- Whitespace trim
- Line ending normalization
- Single Markdown JSON fence removal
- Extraction of one unambiguous JSON object from short commentary

Not repaired: missing commas, wrong types, missing fields, duplicate keys, multiple objects.

## Protected values

Model output must not include task_id, adventure_id, paths, hashes, manifests, or internal IDs. Checked in `response_validate.validate_protected_values()`.

## Output destinations

Draft root: `adventures/_local_ai_drafts/` (gitignored)

Prepare with explicit `--output`. Paths must:

- Be repository-relative
- End with `/adventure_brief.json`
- Not touch existing adventures, specs, tests, Cold Storage, or A_Hutoriasztas

## Proposal directory

`proposal/adventure_brief.json`, `proposal_manifest.json`, `provenance.json`, `validation_report.json`, `human_review.md`

## Attempt preservation

`run --force` archives prior attempt under `attempts/001/`, `attempts/002/`, etc.

## Status model

- `task.status`: major milestones (`RESPONSE_RECEIVED`, `VALIDATED`, `APPLIED`)
- `status.json.processing_stage`: substates (`PARSED`, `RESPONSE_VALIDATED`, `PROPOSAL_READY`, `VALIDATED`, `APPLIED`)

## Network policy

Network requests occur only through the configured adapter endpoint. Mock mode (`--mock`) opens no sockets.

## Not yet implemented

- AI semantic repair loop
- Full adventure generation
- Automatic git commit

## Cline

Not used. CLI: `python -m idne.local_ai`

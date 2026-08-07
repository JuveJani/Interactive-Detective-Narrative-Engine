# Adventure Brief Structured Mapping — Design Spec

**Status:** Source of truth for Local AI semantic → canonical brief mapping  
**Branch:** `cursor/offline-local-ai-core`  
**PR:** #54

## Problem

The Local AI semantic response schema defines structured narrative fields (`working_title`, `premise`, `setting`, `opening_situation`, `initial_observable_facts`, `author_notes`). `map_semantic_to_canonical()` previously serialized most of these into a single `author_notes` prose blob, destroying machine-readable structure.

## Decision: Option A — extend canonical brief schema

Add **optional** structured narrative fields to the canonical Adventure Generator v2 `adventure_brief.json` schema. These concepts belong in the brief: they are author-facing setup consumed by downstream generation stages (via the full brief dict in stage context).

**Not chosen:** Option B (semantic sidecar only) would preserve structure outside the approved brief artifact, splitting narrative data across files and leaving the generator context without structured access.

## Canonical representation

| Field | Type | Required | Source |
|-------|------|----------|--------|
| `working_title` | string | optional | semantic |
| `premise` | string | optional* | semantic (required in Local AI response) |
| `setting` | string | optional | semantic |
| `opening_situation` | string | optional* | semantic (required in Local AI response) |
| `initial_observable_facts` | string[] | optional | semantic |
| `author_notes` | string | optional | semantic `author_notes` only |

\* Required in Local AI semantic responses; optional in canonical brief for backwards compatibility with legacy briefs (e.g. Cold Storage) that store narrative prose only in `author_notes`.

Existing required canonical fields unchanged.

## Mapping rules

1. Copy shared parameter fields directly (unchanged).
2. Copy `premise`, `opening_situation` as top-level strings.
3. Copy `working_title`, `setting` when present and non-blank.
4. Copy `initial_observable_facts` as a string array (trimmed, empty items dropped).
5. Set `author_notes` **only** from semantic `author_notes` when present and non-blank.
6. **Never** embed `Premise:`, `Setting:`, etc. labels in `author_notes`.
7. **Never** duplicate structured fields into both top-level keys and `author_notes`.

## Backwards compatibility

- Legacy briefs without structured narrative fields continue to pass `validate_brief()`.
- Optional-field type checks apply only when fields are present.
- No changes to adventures, translations, or existing brief files.
- Local AI task/run identity and reasoning/content separation unchanged.

## Validation

- `validate_brief()` validates optional narrative field types when present.
- Local AI semantic validation unchanged (pre-map).
- Proposal validation uses `validate_brief()` on mapped output.

## Tests

Regression tests in `tests/test_local_ai_brief_mapping.py` (or extended step3 tests) covering structured preservation, author_notes isolation, no data loss, proposal validation, legacy brief compatibility, and deterministic mock mapping.

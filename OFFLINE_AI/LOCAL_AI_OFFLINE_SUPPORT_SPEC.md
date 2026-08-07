# Local AI Offline Support — Implementation Spec

**Status:** Source of truth for offline user/support documentation and `support-bundle`  
**Branch:** `cursor/offline-local-ai-core`  
**PR:** #54

## Purpose

Make the Local AI Orchestrator **usable and repairable offline** without requiring the user or a small local model to rediscover repository architecture. Deliver:

1. `OFFLINE_AI/USER_GUIDE.md` — short, non-developer workflow guide
2. `OFFLINE_AI/LOCAL_AI_SUPPORT.md` — repair/diagnostic context for offline AI assistants
3. `python -m idne.local_ai support-bundle [TASK_RUN]` — deterministic diagnostic bundle

## Non-goals

- Do not merge PR automatically
- Do not modify adventures or translations
- Do not overwrite user `local_ai.toml`
- Do not expose secrets in bundles
- Do not modify task run directories when generating bundles

## User guide requirements

Target audience: non-developer author on Windows/Pixel with LM Studio.

Must document exact commands and expected status transitions:

```
prepare → READY_FOR_MODEL
run     → RESPONSE_RECEIVED
process → VALIDATED (via parse/validate/build/validate substages)
review  → human checkpoint
apply   → APPLIED
```

Troubleshooting (compact):

| Symptom | First checks |
|---------|----------------|
| LM Studio unreachable | doctor, server tab, loopback URL |
| Model not configured | `models`, set `model` in local_ai.toml |
| Multiple models | configure explicit `model` |
| Reasoning without final content | increase `doctor_probe_max_tokens` / task `max_output_tokens` |
| INVALID_STATUS on run | `review`, stale response vs status, `--force` rules |
| Parse failure | `response_parse_report.json`, model JSON discipline |
| Validation failure | `response_validation_report.json`, `proposal/validation_report.json` |
| Proposal not applyable | `review`, must be VALIDATED, warnings flag |

Configuration policy:

- `local_ai.toml` is **user-owned** — never overwritten by tooling
- `OFFLINE_AI/local_ai.example.toml` may gain keys after updates
- Users compare example vs local file and merge new keys manually

## Support guide requirements

For offline AI repair assistants. Document **implemented behavior only**:

- Module map (`idne/local_ai/*`)
- Source content identity vs run definition identity
- Run directory layout and processing stages
- LM Studio transport, `content` vs `reasoning_content`
- Parse → validate → proposal → apply pipeline
- Attempt preservation, path/symlink rules, config precedence
- Cross-platform (pathlib, no string prefix security)
- Diagnostic decision tree with artifact paths per failure class
- Invariants that must not be weakened
- Required tests after code changes

**Invariant:** `reasoning_content` is diagnostic metadata only — never task output.

## Support bundle command

```
python -m idne.local_ai support-bundle [TASK_DIRECTORY] [--config PATH]
```

### Output location

```
.local_ai_support/<bundle_id>/
  REPORT.md
  bundle_manifest.json
  environment.json
  artifact_summary.json
  artifacts/          # copied JSON/text when present
```

`<bundle_id>` deterministic: `{task_id_or_environment}_{git_head_8}`.

### REPORT.md sections (ordered)

1. Summary (task status, processing stage, apply allowed)
2. Environment (platform, Python, git commit, dirty)
3. Effective config (redacted)
4. Adapter/model/endpoint
5. Doctor-style checks (non-network where possible)
6. Task identity (source vs run definition)
7. Transport/reasoning metadata
8. Attempts
9. Last error
10. Artifact existence table
11. Useful repo-relative paths

### Security

- Redact API tokens, env secret values, Authorization headers
- Never write secrets to bundle
- Read-only access to task directory

### Determinism

- Sorted artifact names and JSON keys
- Stable bundle id for same task + git head
- POSIX repo-relative paths in serialized output

### Tests

`tests/test_local_ai_support_bundle.py`:

- bundle creation with mock task
- secret redaction
- missing optional artifacts
- deterministic ordering / bundle id
- pathlib safe paths
- task directory unmodified (mtime/hash check on task.json)

## Files to create/modify

| File | Action |
|------|--------|
| `OFFLINE_AI/LOCAL_AI_OFFLINE_SUPPORT_SPEC.md` | create (this file) |
| `OFFLINE_AI/USER_GUIDE.md` | create |
| `OFFLINE_AI/LOCAL_AI_SUPPORT.md` | create |
| `idne/local_ai/support_bundle.py` | create |
| `idne/local_ai/cli.py` | add command |
| `tests/test_local_ai_support_bundle.py` | create |
| `.gitignore` | add `.local_ai_support/` |

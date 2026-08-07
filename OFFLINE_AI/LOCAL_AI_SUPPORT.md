# Local AI Support Guide

Context for a **small offline AI** helping diagnose Local AI Orchestrator failures. Document reflects **implemented behavior only** (branch `cursor/offline-local-ai-core`, PR #54).

## Critical invariant

**`reasoning_content` is diagnostic metadata only.** It may appear in `transport_report.json` and support bundles. It is **never** written to `response.txt`, parsed JSON, proposals, or applied output. Task output always comes from final `content`.

## Module architecture

| Module | Responsibility |
|--------|----------------|
| `cli.py` | Command-line entry (`doctor`, `prepare`, `run`, `process`, `apply`, `support-bundle`, …) |
| `config.py` | Load `local_ai.toml`, endpoint policy, secret env resolution |
| `doctor.py` | Environment/runtime/adapter readiness checks |
| `task_builder.py` | `prepare_task()` — context, prompt, run directory |
| `task_model.py` | Task schema, statuses, identities, transitions |
| `context_builder.py` | Authoritative file context package |
| `prompt_builder.py` | Prompt assembly from context |
| `transport.py` | `run_task()` — model call, status transition to `RESPONSE_RECEIVED` |
| `model_adapter.py` | Adapter factory, retries, model selection |
| `lm_studio_client.py` | HTTP transport, `content` vs `reasoning_content` parsing |
| `response_capture.py` | Persist `request.json`, `response.txt`, `transport_report.json` |
| `response_parser.py` | Parse model text → `parsed_response.json` |
| `structural_repair.py` | Safe pre-parse repairs (BOM, fences, etc.) |
| `response_validate.py` | Schema and semantic validation |
| `proposal_builder.py` | Canonical brief proposal under `proposal/` |
| `proposal_validate.py` | Proposal package validation |
| `apply.py` | Write draft output after human review gate |
| `process.py` | Unified parse → validate → build → validate pipeline |
| `attempts.py` | Archive prior model attempts on re-run |
| `run_state.py` | `task.json`, `status.json` load/write |
| `paths.py` | Repo-relative path normalization and allowlist security |
| `output_paths.py` | Draft output path policy (`adventures/_local_ai_drafts/`) |
| `content_identity.py` | Brief/proposal content hashing |
| `platform_runtime.py` | Cross-platform runs root, temp paths |
| `support_bundle.py` | Offline diagnostic bundle generation |
| `mock_adapter.py` | Deterministic adapter for tests/offline doctor |

## Identity: source content vs run definition

- **Source content identity** (`source_content_identity` in `task.json`): SHA256 of author input path(s) and file hash(es). Changes when input file content changes.
- **Run definition identity** (`compute_run_definition_identity()`): hash of task type + inputs + **output paths**. Drives `task_id` and run directory name.
- **Rule:** Same input with **different `--output`** → different `task_id` and run directory. Reusing a run dir after changing output causes stale artifacts and `INVALID_STATUS`.

## Run directory layout

Under `.local_ai_runs/<safe-task-id>/`:

| Artifact | Purpose |
|----------|---------|
| `task.json` | Task definition, status, allowed paths |
| `status.json` | Processing stage, prompt hash, timestamps |
| `prompt.txt` | Model prompt |
| `context_manifest.json` | Context sections and sizes |
| `request.json` | Outbound API request (may contain redacted fields in bundles) |
| `response.txt` | Final model **content** only |
| `raw_response.json` | Full API payload (optional, config `retain_raw_response`) |
| `transport_report.json` | Adapter, model, usage, reasoning metadata |
| `parsed_response.json` | Parsed JSON from response |
| `response_parse_report.json` | Parse method, repairs, errors |
| `response_validation_report.json` | Response validation findings |
| `proposal/` | Built proposal, validation, human review |
| `attempts/` | Archived prior attempts |
| `diagnostics.json` | Transport failures, last error hints |
| `apply_report.json` | Apply outcome (after apply) |

Draft outputs go only to paths under `adventures/_local_ai_drafts/` via explicit `apply`.

## Status and processing stages

**Task status (`task.json`):**

```
READY_FOR_MODEL → RESPONSE_RECEIVED → VALIDATED → APPLIED
```

(Failure paths: `FAILED`, `BLOCKED`; early: `CREATED`, `PREPARED`.)

**Processing stage (`status.json`):**

```
NONE → PARSED → RESPONSE_VALIDATED → PROPOSAL_READY → VALIDATED → APPLIED
```

`process` stops at first failure and leaves stage at last successful step.

## LM Studio transport

- OpenAI-compatible chat completions at configured `base_url` (default `http://127.0.0.1:1234/v1`).
- Loopback required unless `allow_remote_endpoint = true`.
- API token from env var named in config (`api_token_env`, default `LM_STUDIO_API_TOKEN`).
- Retries per `[transport] retry_count`.
- `parse_completion_response()` separates:
  - **`content`** → `response.txt`, parsing, proposals
  - **`reasoning_content`** → metadata in `transport_report.json` only
- `ReasoningWithoutContentTransportError` when reasoning present but final content empty.

## Parse / validate / proposal / apply pipeline

1. **parse** — `response.txt` → structural repair → JSON extract → `parsed_response.json`
2. **validate-response** — schema, protected values, semantic boundaries
3. **build-proposal** — map to canonical brief under `proposal/`
4. **validate-proposal** — proposal package checks
5. **apply** — gated: task `VALIDATED`, stage `VALIDATED`, optional warning acknowledgement

`verify_run_definition()` before parse ensures `task.json` matches current run parameters.

## Attempt preservation

On `run --force` or re-run when allowed, `attempts.py` archives current response artifacts to `attempts/<n>/` before replacing. Inspect `attempts/` when comparing model outputs.

## Path, symlink, and security rules

- All user paths normalized to **POSIX repo-relative** strings.
- Traversal (`../`), absolute paths, and paths outside repo rejected.
- Allowlists deduplicated and sorted deterministically.
- Security checks use `Path.resolve()` + `relative_to()` — **not** string prefix checks.
- Symlinks: resolved paths must stay under repo root.
- Directories cannot be used as input files.

## Config precedence

1. CLI `--config`
2. Environment `IDNE_LOCAL_AI_CONFIG`
3. `local_ai.toml` at repo root
4. Built-in defaults

**Never overwrite user `local_ai.toml` automatically.**

## Cross-platform requirements

- Use `pathlib.Path` throughout; serialize paths with forward slashes.
- Runs root: `.local_ai_runs/` via `platform_runtime.local_ai_runs_root()`.
- Support bundles: `.local_ai_support/`.
- UTF-8 for all text artifacts.

## Diagnostic decision tree

```
Failure at doctor
  → environment.json checks, LM Studio reachability, config model
Failure at prepare
  → input path allowlist, authoritative files missing, output path policy
Failure at run (INVALID_STATUS / transport)
  → task.json status, stale response vs output change, transport_report.json, diagnostics.json
Failure at process (parse)
  → response.txt, response_parse_report.json (model JSON discipline)
Failure at process (validate-response)
  → response_validation_report.json, parsed_response.json
Failure at process (validate-proposal)
  → proposal/validation_report.json, proposal/adventure_brief.json
Failure at apply
  → review output, VALIDATED status, warnings, output path writable
Reasoning-only response
  → transport_report.json reasoning_* fields; increase max_output_tokens; never treat reasoning as output
```

## Files to inspect by failure class

| Failure | Inspect first |
|---------|----------------|
| LM Studio unreachable | `doctor` output, `local_ai.toml` `[adapter]`, `diagnostics.json` |
| Model selection | `models` command, config `model`, `transport_report.json` |
| INVALID_STATUS | `task.json`, `status.json`, `review`, compare `allowed_output_files` to prepare |
| Parse | `response.txt`, `response_parse_report.json` |
| Response validation | `response_validation_report.json`, `parsed_response.json` |
| Proposal validation | `proposal/validation_report.json` |
| Apply blocked | `review`, `task.status`, `status.processing_stage`, warning flags |
| Reasoning without content | `transport_report.json` (`reasoning_present`, `finish_reason`) |

## Support bundle command

```bash
python -m idne.local_ai support-bundle [TASK_DIRECTORY] [--config PATH] [--mock]
```

- Writes read-only bundle to `.local_ai_support/<task_id_or_environment>_<git_short>/`
- Redacts secrets; does not modify task directory
- Use `--mock` for doctor when LM Studio is offline

## Invariants — do not weaken during repairs

1. `reasoning_content` never becomes task output.
2. Draft apply only under `adventures/_local_ai_drafts/` via explicit `apply`.
3. User `local_ai.toml` never auto-overwritten.
4. Run identity includes output paths — no silent run dir reuse across outputs.
5. Path security via resolved containment, not string prefixes.
6. Deterministic ordering for allowlists, JSON keys, bundle output.
7. Adventures and translations are not modified by orchestrator except explicit apply to draft paths.

## Required tests after code changes

**Focused Local AI:**

```bash
python3 -m unittest tests.test_local_ai_support_bundle -v
python3 -m unittest tests.test_local_ai tests.test_local_ai_step3 tests.test_local_ai_transport tests.test_local_ai_prepare_reuse tests.test_local_ai_reasoning -v
```

**Full repository suite:**

```bash
python3 -m unittest discover -s tests
```

Add or update tests when changing: transport parsing, identities, path rules, bundle redaction, or status transitions.

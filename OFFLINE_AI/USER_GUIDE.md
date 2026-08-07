# Local AI User Guide

Short guide for running the offline Local AI workflow on Windows or Linux. You do not need to know Python internals — run these commands from the repository root.

## Before you start

1. **LM Studio** — download/load a model and start the **Local Server** (OpenAI-compatible API).
2. **Configuration (optional)** — copy `OFFLINE_AI/local_ai.example.toml` to `local_ai.toml` in the repository root and adjust if needed.
3. **Python** — use the project’s Python environment from this repository.

## Normal workflow

### 1. Start LM Studio

- Open LM Studio.
- Load a model on the **Models** tab.
- Start the **Local Server** (default URL: `http://127.0.0.1:1234`).
- Note the model id if you have more than one model loaded.

### 2. Doctor

Checks that the repository, run directory, and (optionally) LM Studio are ready.

```powershell
python -m idne.local_ai doctor
python -m idne.local_ai doctor --test-completion
```

Without LM Studio (mock):

```powershell
python -m idne.local_ai doctor --mock --test-completion
```

**Expected:** status `OK` or `DEGRADED` (git unavailable is OK). `BLOCKED` means fix the reported issue before continuing.

### 3. Prepare

Creates a task run directory and prompt **without** calling the model.

```powershell
python -m idne.local_ai prepare --task-type adventure_brief `
  --input OFFLINE_AI/examples/adventure_brief_input.md `
  --output adventures/_local_ai_drafts/my_brief/adventure_brief.json
```

**Expected status:** `READY_FOR_MODEL`  
**Note the run directory** printed as `Dir:` (under `.local_ai_runs/`).

### 4. Run

Sends the prompt to your configured model.

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id>
```

Mock (no server):

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id> --mock
```

**Expected status:** `RESPONSE_RECEIVED`

### 5. Process

Parses the model response, validates it, builds a proposal, and validates the proposal.

```powershell
python -m idne.local_ai process .local_ai_runs\<task-id>
```

**Expected status:** `VALIDATED` (processing stage reaches `VALIDATED`)

### 6. Review

Human checkpoint before writing any draft file.

```powershell
python -m idne.local_ai review .local_ai_runs\<task-id>
```

Check validation results and that **Apply allowed: yes**.

### 7. Apply

Writes the validated proposal to your draft output path (never overwrites canonical adventures automatically).

```powershell
python -m idne.local_ai apply .local_ai_runs\<task-id>
```

Use `--overwrite` only to replace a draft file previously written by the **same** task.  
Use `--acknowledge-warnings` if response validation recorded warnings you accept.

**Expected status:** `APPLIED`

## Status transitions

| Step    | `task.status`       | `processing_stage` (after step)      |
|---------|---------------------|--------------------------------------|
| prepare | `READY_FOR_MODEL`   | `NONE`                               |
| run     | `RESPONSE_RECEIVED` | `NONE`                               |
| process | `VALIDATED`         | `VALIDATED`                          |
| apply   | `APPLIED`           | `APPLIED`                            |

Inside **process**, stages advance: `NONE` → `PARSED` → `RESPONSE_VALIDATED` → `PROPOSAL_READY` → `VALIDATED`.

## Configuration (`local_ai.toml`)

- **`local_ai.toml` is user-owned.** Tooling never overwrites it automatically.
- **`OFFLINE_AI/local_ai.example.toml`** may gain new options after updates.
- To sync safely after an update:
  1. Open both files side by side.
  2. Copy **new keys only** from the example into your `local_ai.toml`.
  3. Do not replace your whole file unless you intend to reset settings.

Common settings:

| Key | Purpose |
|-----|---------|
| `[adapter] model` | Required when multiple models are loaded |
| `[adapter] base_url` | LM Studio server URL (default loopback) |
| `[transport] max_output_tokens` | Max tokens for task completions |
| `[transport] doctor_probe_max_tokens` | Tokens for doctor completion probe |

Config lookup order: `--config` → `IDNE_LOCAL_AI_CONFIG` → `local_ai.toml` → defaults.

## Troubleshooting

| Problem | What to do |
|---------|------------|
| **LM Studio unreachable** | Confirm server is running; run `doctor`; check `base_url` in `local_ai.toml` points to loopback (`127.0.0.1`). |
| **Model not configured** | Run `python -m idne.local_ai models`; set `model = "..."` in `local_ai.toml`. |
| **Multiple models available** | Set an explicit `model` in `local_ai.toml` — auto-select fails when ambiguous. |
| **Reasoning without final content** | Some models return thinking in `reasoning_content` but empty `content`. Increase `doctor_probe_max_tokens` and `max_output_tokens` in config; retry `run --force` if needed. |
| **INVALID_STATUS on run** | Run `review`. Often a stale response from a previous run — check output path matches prepare, or use `run --force` only when appropriate. |
| **Parse failure** | Inspect `response_parse_report.json` in the run directory; model must return parseable JSON. |
| **Validation failure** | Inspect `response_validation_report.json` and `proposal/validation_report.json`. |
| **Proposal not applyable** | Run `review` — status must be `VALIDATED` with stage `VALIDATED`; use `--acknowledge-warnings` if warnings block apply. |

## Offline diagnostic bundle

When you need help diagnosing a failure (for yourself or an offline assistant):

```powershell
python -m idne.local_ai support-bundle .local_ai_runs\<task-id> --mock
```

Output is written under `.local_ai_support/` (gitignored). The bundle does **not** modify your task run.

See `OFFLINE_AI/LOCAL_AI_SUPPORT.md` for repair context aimed at offline AI assistants.

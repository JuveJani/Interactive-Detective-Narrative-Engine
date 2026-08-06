# Local AI Quickstart

## 1. Configure (optional)

Copy `OFFLINE_AI/local_ai.example.toml` to `local_ai.toml` in the repository root.

Default endpoint: `http://127.0.0.1:1234/v1`

Optional API token: set environment variable named in config (default `LM_STUDIO_API_TOKEN`).

## 2. Start LM Studio (Windows)

1. Open LM Studio.
2. Download/load a local model.
3. Start the **Local Server** (OpenAI-compatible).
4. Note the model id from the Models tab.

## 3. Doctor

```powershell
python -m idne.local_ai doctor
python -m idne.local_ai doctor --test-completion
```

Mock (no server):

```powershell
python -m idne.local_ai doctor --mock --test-completion
```

## 4. Prepare task

```powershell
python -m idne.local_ai prepare --task-type adventure_brief `
  --input OFFLINE_AI/examples/adventure_brief_input.md `
  --output adventures/_local_ai_drafts/example_offline_brief/adventure_brief.json
```

## 5. Run task

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id>
```

Mock:

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id> --mock
```

## 6. Process response

```powershell
python -m idne.local_ai process .local_ai_runs\<task-id>
python -m idne.local_ai review .local_ai_runs\<task-id>
```

Or step-by-step:

```powershell
python -m idne.local_ai parse .local_ai_runs\<task-id>
python -m idne.local_ai validate-response .local_ai_runs\<task-id>
python -m idne.local_ai build-proposal .local_ai_runs\<task-id>
python -m idne.local_ai validate-proposal .local_ai_runs\<task-id>
```

## 7. Apply (explicit)

```powershell
python -m idne.local_ai apply .local_ai_runs\<task-id>
```

Use `--overwrite` only to rewrite a draft file previously written by the same task.
Use `--acknowledge-warnings` if response validation recorded human-review warnings.

## 8. Inspect

```powershell
python -m idne.local_ai show-response .local_ai_runs\<task-id>
python -m idne.local_ai transport-report .local_ai_runs\<task-id>
python -m idne.local_ai attempts .local_ai_runs\<task-id>
python -m idne.local_ai models
```

## Termux

Mock end-to-end on Pixel:

```bash
python -m idne.local_ai doctor --mock
python -m idne.local_ai prepare --task-type adventure_brief \
  --input OFFLINE_AI/examples/adventure_brief_input.md \
  --output adventures/_local_ai_drafts/example_offline_brief/adventure_brief.json
python -m idne.local_ai run .local_ai_runs/<task-id> --mock
python -m idne.local_ai process .local_ai_runs/<task-id>
python -m idne.local_ai apply .local_ai_runs/<task-id>
```

LAN to laptop: edit `local_ai.toml` with laptop IP and `allow_remote_endpoint = true`.

## Limitations

- No AI semantic repair loop yet — invalid model JSON must be fixed by re-running with `--force` or editing offline.
- Apply writes only to approved draft paths under `adventures/_local_ai_drafts/`.
- Does not generate a full adventure or modify existing adventures.

## Cline

Not part of this workflow.

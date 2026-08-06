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
python -m idne.local_ai prepare --task-type adventure_brief --input OFFLINE_AI/examples/adventure_brief_input.md
```

## 5. Run task

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id>
```

Mock:

```powershell
python -m idne.local_ai run .local_ai_runs\<task-id> --mock
```

## 6. Inspect

```powershell
python -m idne.local_ai show-response .local_ai_runs\<task-id>
python -m idne.local_ai transport-report .local_ai_runs\<task-id>
python -m idne.local_ai models
```

## Termux

Mock workflow on Pixel:

```bash
python -m idne.local_ai doctor --mock
python -m idne.local_ai prepare --task-type adventure_brief --input OFFLINE_AI/examples/adventure_brief_input.md
python -m idne.local_ai run .local_ai_runs/<task-id> --mock
```

LAN to laptop: edit `local_ai.toml` with laptop IP and `allow_remote_endpoint = true`.

## Limitation

Step 2 does **not** validate or apply model JSON to the repository. See `OFFLINE_AI/OFFLINE_CHECKLIST.md`.

## Cline

Not part of this workflow.

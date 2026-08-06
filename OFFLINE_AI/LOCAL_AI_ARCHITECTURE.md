# Local AI Orchestrator — Architecture

**Status:** Step 2 — LM Studio transport adapter (no semantic validation yet)

## Purpose

Prepare exact, validated Local AI task packages and send `prompt.txt` to a local
OpenAI-compatible model (LM Studio). Python performs all deterministic work.

## What Python does

- Deterministic task preparation (Step 1)
- Configuration loading and endpoint safety (`config.py`)
- Model listing and chat completion transport (`lm_studio_client.py`, `model_adapter.py`)
- Response capture inside task directories only (`response_capture.py`, `transport.py`)
- Mock adapter for tests and Termux offline workflow (`mock_adapter.py`)
- Doctor diagnostics (`doctor.py`)

## What the model adapter does (transport only)

- `GET /v1/models` — list and select model
- `POST /v1/chat/completions` — send prepared prompt
- Save raw response, extracted content, transport metrics
- Transition task `READY_FOR_MODEL` → `RESPONSE_RECEIVED`

## What the adapter must NOT do

- Explore the repository or modify `prompt.txt`
- Add chat history
- Write outside `.local_ai_runs/<task-id>/`
- Assign IDs, repair schemas, or apply output

## Network policy

Network requests occur **only** through the configured adapter endpoint.
Default: loopback (`127.0.0.1`, `localhost`, `::1`) only.
Set `allow_remote_endpoint = true` for trusted LAN (e.g. Termux → laptop).

## Task directory (after transport)

| File | Purpose |
|------|---------|
| `task.json` | Versioned task record |
| `prompt.txt` | Prepared prompt (unchanged by adapter) |
| `request.json` | Outbound request metadata |
| `raw_response.json` | Full model HTTP JSON |
| `response.txt` | Extracted assistant content |
| `transport_report.json` | Timing, usage, classification |
| `status.json` | Updated status + attempt count |

## Configuration

See `OFFLINE_AI/local_ai.example.toml`. User file: `local_ai.toml` (gitignored).

Precedence: `--config` → `IDNE_LOCAL_AI_CONFIG` → `local_ai.toml` → defaults.

## Termux modes

1. **Mock only** — prepare/run with `--mock` on device
2. **LAN adapter** — point `base_url` at laptop LM Studio with `allow_remote_endpoint = true`

LM Studio does not run on Android.

## Step 3 (not yet)

- Semantic JSON validation
- Repair and repository application

## Cline

Not used. CLI: `python -m idne.local_ai`

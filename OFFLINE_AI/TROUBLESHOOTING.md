# Local AI Troubleshooting

## Doctor reports BLOCKED — model server not reachable

1. Start LM Studio.
2. Open **Local Server** tab and click **Start Server**.
3. Load a model in LM Studio before running tasks.
4. Verify endpoint: `http://127.0.0.1:1234/v1`
5. Run: `python -m idne.local_ai doctor`

Use mock mode when LM Studio is unavailable:

```bash
python -m idne.local_ai doctor --mock
```

## Multiple models available

Configure an explicit model id in `local_ai.toml`:

```toml
[adapter]
model = "your-exact-model-id"
```

List ids: `python -m idne.local_ai models`

## Endpoint rejected (non-loopback)

Default policy allows loopback only. For Termux → laptop on LAN:

```toml
[adapter]
base_url = "http://192.168.x.x:1234/v1"
allow_remote_endpoint = true
```

## Task already has a response

Use `--force` to overwrite transport artifacts:

```bash
python -m idne.local_ai run .local_ai_runs/<task-id> --force
```

## Connection refused / timeout

- Confirm LM Studio server is running.
- Increase timeouts in `local_ai.toml` `[transport]` section.
- Check firewall rules for LAN access.

## Malformed or empty completion

Transport succeeded but response shape was invalid. Inspect:

- `raw_response.json`
- `transport_report.json`

Run `python -m idne.local_ai parse <task-dir>` for structured parse errors.

## Parse or validation failure

Inspect:

- `response_parse_report.json`
- `response_validation_report.json`
- `proposal/validation_report.json`

Re-run model with `--force` (archives prior attempt). Do not apply until `review` shows apply allowed.

## Apply blocked

- Task must be `VALIDATED`
- Warnings require `--acknowledge-warnings`
- Existing output requires `--overwrite` (same task only)
- Output must be under `adventures/_local_ai_drafts/`

## Cline

Do not use Cline for Local AI orchestration. Use `python -m idne.local_ai` only.

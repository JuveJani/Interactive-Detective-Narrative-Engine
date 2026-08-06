# Offline Verification Checklist

Use this checklist after configuring LM Studio on Windows.

## Before disabling internet

- [ ] LM Studio installed and model downloaded
- [ ] Local server started at `http://127.0.0.1:1234/v1`
- [ ] `local_ai.toml` copied from `OFFLINE_AI/local_ai.example.toml` (optional)
- [ ] `python -m idne.local_ai doctor` → READY
- [ ] `python -m idne.local_ai doctor --test-completion` → completion OK
- [ ] Prepare example task
- [ ] Run prepared task → `RESPONSE_RECEIVED`
- [ ] Inspect `response.txt` and `transport_report.json`

## Disable connectivity

- [ ] Turn off Wi-Fi
- [ ] Disconnect Ethernet / other internet paths
- [ ] Confirm browser cannot reach external sites
- [ ] LM Studio local server still running

## Offline rerun

- [ ] `python -m idne.local_ai doctor --test-completion` → still OK
- [ ] Prepare a fresh example task
- [ ] Run task → `RESPONSE_RECEIVED`
- [ ] Record duration and token usage from `transport_report.json`

## Termux (Pixel)

Mock mode (no laptop):

```bash
python -m idne.local_ai doctor --mock --test-completion
python -m idne.local_ai prepare --task-type adventure_brief --input OFFLINE_AI/examples/adventure_brief_input.md
python -m idne.local_ai run .local_ai_runs/<task-id> --mock
```

Optional LAN mode to Windows laptop: set `allow_remote_endpoint = true` and laptop IP in `local_ai.toml`.

## Not in scope yet (Step 3+)

- [ ] Semantic JSON validation against brief schema
- [ ] Writing brief into repository
- [ ] Full adventure generation

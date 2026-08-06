# Offline Verification Checklist

Use this checklist after configuring LM Studio on Windows.

## Before disabling internet

- [ ] LM Studio installed and model downloaded
- [ ] Local server started at `http://127.0.0.1:1234/v1`
- [ ] `local_ai.toml` copied from `OFFLINE_AI/local_ai.example.toml` (optional)
- [ ] `python -m idne.local_ai doctor` → READY
- [ ] `python -m idne.local_ai doctor --test-completion` → completion OK
- [ ] Prepare example task with explicit draft output
- [ ] Run prepared task → `RESPONSE_RECEIVED`
- [ ] `python -m idne.local_ai process <task-dir>` → `VALIDATED` or clear validation failure
- [ ] `python -m idne.local_ai review <task-dir>`
- [ ] If validation passes: `python -m idne.local_ai apply <task-dir>` → `APPLIED`
- [ ] Confirm only draft brief under `adventures/_local_ai_drafts/` was written

## Disable connectivity

- [ ] Turn off Wi-Fi
- [ ] Disconnect Ethernet / other internet paths
- [ ] Confirm browser cannot reach external sites
- [ ] LM Studio local server still running

## Offline rerun

- [ ] `python -m idne.local_ai doctor --test-completion` → still OK
- [ ] Prepare a fresh example task
- [ ] Run task → `RESPONSE_RECEIVED`
- [ ] Process → validate or record local validation failure (transport vs semantic)
- [ ] Record duration, token usage, parse repairs from reports

## Termux (Pixel)

Mock end-to-end (no laptop):

```bash
python -m idne.local_ai doctor --mock --test-completion
python -m idne.local_ai prepare --task-type adventure_brief \
  --input OFFLINE_AI/examples/adventure_brief_input.md \
  --output adventures/_local_ai_drafts/example_offline_brief/adventure_brief.json
python -m idne.local_ai run .local_ai_runs/<task-id> --mock
python -m idne.local_ai process .local_ai_runs/<task-id>
python -m idne.local_ai apply .local_ai_runs/<task-id>
```

Optional LAN mode to Windows laptop: set `allow_remote_endpoint = true` and laptop IP in `local_ai.toml`.

## Not in scope

- [ ] AI semantic repair loop
- [ ] Full adventure generation
- [ ] Modifying existing adventures

## Cline

Not used.

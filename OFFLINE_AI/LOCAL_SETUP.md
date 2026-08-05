# Local Setup

Reserve sections for measured local AI configuration. **Do not invent values** until benchmarked on your machine.

Target reference hardware: Acer Swift Go 14 (Core Ultra 5, 32 GB RAM, Windows 11, no discrete GPU).

---

## Python environment

```powershell
# Windows — see also scripts/windows/install.ps1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # if present
python -m unittest discover -s tests
```

| Field | Value |
|-------|-------|
| Python version | _TBD_ |
| venv path | `.venv` |

---

## LM Studio

| Field | Value |
|-------|-------|
| LM Studio version | _TBD_ |
| Local server URL | _TBD_ (e.g. `http://localhost:1234/v1`) |
| API compatibility | OpenAI-compatible chat completions |

### Loaded models

| Model name | File / ID | Context length | Notes |
|------------|-----------|----------------|-------|
| Qwen3.5 9B | _TBD_ | _TBD_ | |
| Qwen2.5 Coder 7B | _TBD_ | _TBD_ | |
| Qwen2.5 Coder 14B | _TBD_ | _TBD_ | |
| Qwen3.6 35B-A3B | _TBD_ | _TBD_ | |

### Context settings (measured)

| Task type | Context tokens | Temperature | Notes |
|-----------|----------------|-------------|-------|
| Generator stage | _TBD_ | _TBD_ | |
| Code edit | _TBD_ | _TBD_ | |
| Report explanation | _TBD_ | _TBD_ | |

---

## Cline (inside Cursor)

| Field | Value |
|-------|-------|
| Cline version | _TBD_ |
| API provider | _TBD_ |
| Base URL | _TBD_ |
| Model ID string | _TBD_ |
| Rules file | `.clinerules/00-idne-core.md` |

---

## Generator v2 local backend

| Field | Value |
|-------|-------|
| Adapter config path | _TBD_ (`idne/model_adapter/`) |
| Backend name | _TBD_ |
| Verified stage | _TBD_ |

---

## Performance results (measured)

| Task | Model | Wall time | Outcome |
|------|-------|-----------|---------|
| _TBD_ | | | |

---

## Phone access

| Field | Value |
|-------|-------|
| Status | Not configured |
| Method | _TBD_ |
| Use case | _TBD_ |

---

## Simulator v2 offline workflow

See `SIMULATOR_V2_WINDOWS_WORKFLOW.md` and `scripts/windows/`.

```powershell
python -m idne.sim_v2 validate tests\fixtures\sim_v2_solo.idne
python -m idne.sim_v2 diagnose tests\fixtures\sim_v2_solo.idne
```

---

## Update policy

When you measure a value, update this file and note the date in `SESSION_HANDOFF.md`. Remove `_TBD_` only with evidence from an actual run.

# IDNE Offline Setup — Windows 11

**Target platform:** Acer Swift Go 14, Core Ultra 5 228V, 32 GB RAM, 1 TB SSD, Windows 11  
**Milestone:** 11 — Adventure Generator v2

---

## 1. Prerequisites

1. Install **Python 3.10 or newer** from [python.org](https://www.python.org/downloads/). Enable “Add Python to PATH”.
2. Install **Git** for Windows.
3. Clone the IDNE repository.

Verify:

```powershell
python --version
python -m idne.generate --help
```

(Use `python3` on systems where that is the Python 3 command.)

---

## 2. Core generator (no network)

The generator runs offline with the deterministic mock backend (tests and dry-runs):

```powershell
python -m idne.generate tests\fixtures\gen_v2_brief_solo.json --workspace generated\test_solo --auto-approve
```

No pip packages are required for core validation and mock generation.

---

## 3. Local LLM (30–32B quantized)

For production generation with a local model:

### Option A — LM Studio / OpenAI-compatible server

1. Install LM Studio (or similar) and load a 30–32B quantized model.
2. Start the local server (default often `http://127.0.0.1:1234`).
3. Create `model_config.json`:

```json
{
  "backend": "openai_compatible",
  "local_mode": true,
  "endpoint_url": "http://127.0.0.1:1234",
  "model_name": "your-model-id",
  "context_size": 8192,
  "temperature": 0.1,
  "max_output_tokens": 2048
}
```

4. Run:

```powershell
python -m idne.generate brief.json --workspace generated\my_case --config model_config.json
```

### Option B — CLI runner

Wrap your local inference script to read JSON from stdin and print JSON to stdout. Configure:

```json
{
  "backend": "cli_runner",
  "local_mode": true,
  "cli_command": "python C:\\path\\to\\local_llm_bridge.py"
}
```

---

## 4. Validation

```powershell
python -m idne.validate_adventure generated\my_case\adventure
```

---

## 5. Offline assurance

- Set `local_mode: true` in model config.
- Mock backend never uses the network.
- After models and specs are installed locally, generation does not require internet access.

---

## 6. Notes

- Local 32B model quality for full staged generation is **not** proven in Milestone 11; validate output with integrated validation and human review.
- Do not generate reference adventures until brief and approvals are complete.

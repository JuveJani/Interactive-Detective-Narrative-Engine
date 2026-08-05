# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `capability_checks` — capability check definitions drafted; PLAYER content not started.

| Item | Path |
|------|------|
| Capability check approval (spoiler-free) | `CAPABILITY_CHECK_APPROVAL_PLAYER_TEST.md` |
| Capability check approval (author-only) | `DO_NOT_READ/CAPABILITY_CHECK_APPROVAL_REPORT.md` |
| Capability check package | `adventure/DO_NOT_READ/capability_check_package.json` |
| Investigation flow package | `adventure/DO_NOT_READ/investigation_flow_package.json` |

Resume after human approval of capability checks:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `investigation_flow` — flow and ending graph drafted; capability checks not started.

| Item | Path |
|------|------|
| Investigation flow approval (spoiler-free) | `INVESTIGATION_FLOW_APPROVAL_PLAYER_TEST.md` |
| Investigation flow approval (author-only) | `DO_NOT_READ/INVESTIGATION_FLOW_APPROVAL_REPORT.md` |
| Investigation flow package | `adventure/DO_NOT_READ/investigation_flow_package.json` |
| Investigation core package | `adventure/DO_NOT_READ/investigation_core_package.json` |

Resume after human approval of investigation flow:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| Human approval report (brief) | `HUMAN_APPROVAL_REPORT.md` |
| Fixed truth approval report | `DO_NOT_READ/FIXED_TRUTH_APPROVAL_REPORT.md` (**AUTHOR-ONLY**) |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `investigation_core` — investigation core drafted; investigation flow not started.

| Item | Path |
|------|------|
| NPC approval (spoiler-free) | `NPC_APPROVAL_REPORT_PLAYER_TEST.md` |
| Environment/object approval (spoiler-free) | `ENVIRONMENT_OBJECT_APPROVAL_PLAYER_TEST.md` |
| Investigation core approval (spoiler-free) | `INVESTIGATION_CORE_APPROVAL_PLAYER_TEST.md` |
| Investigation core approval (author-only) | `DO_NOT_READ/INVESTIGATION_CORE_APPROVAL_REPORT.md` |
| Investigation core package | `adventure/DO_NOT_READ/investigation_core_package.json` |
| Environment package | `adventure/DO_NOT_READ/environment_package.json` |
| Object interaction package | `adventure/DO_NOT_READ/object_interaction_package.json` |
| NPC investigation package | `adventure/DO_NOT_READ/npc_investigation_package.json` |

Resume after human approval of investigation core:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

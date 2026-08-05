# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| Human approval report (brief) | `HUMAN_APPROVAL_REPORT.md` |
| Fixed truth approval report | `DO_NOT_READ/FIXED_TRUTH_APPROVAL_REPORT.md` (**AUTHOR-ONLY**) |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `fixed_truth` — causal and world-state timelines drafted; NPC stage not started.

Resume after human approval of fixed truth:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

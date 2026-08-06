# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `playtime` + `dm_feeling` — packages generated; Tier B review and Tier C playtest pending.

| Item | Path |
|------|------|
| Playtime + DM Feeling approval (spoiler-free) | `PLAYTIME_DM_FEELING_APPROVAL_PLAYER_TEST.md` |
| Playtime + DM Feeling approval (author-only) | `DO_NOT_READ/PLAYTIME_DM_FEELING_APPROVAL_REPORT.md` |
| Playtime package | `adventure/DO_NOT_READ/playtime_calibration_package.json` |
| Tier C playtest template | `adventure/DO_NOT_READ/dm_feeling_reports/tier_c_playtest_questionnaire.md` |

Resume after human approval:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

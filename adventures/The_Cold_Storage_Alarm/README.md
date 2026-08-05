# The Cold Storage Alarm

First real IDNE adventure prepared for Adventure Generator v2.

| Item | Path |
|------|------|
| Canonical brief | `adventure_brief.json` / `brief/adventure_brief.json` |
| World truth package | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generation state | `.generation/generation_state.json` |

**Status:** `AWAITING_APPROVAL` at `story_player` — PLAYER prose drafted; playtime not started.

| Item | Path |
|------|------|
| PLAYER approval (spoiler-free) | `STORY_PLAYER_APPROVAL_PLAYER_TEST.md` |
| PLAYER approval (author-only) | `DO_NOT_READ/STORY_PLAYER_APPROVAL_REPORT.md` |
| PLAYER content | `adventure/PLAYER/` |
| PLAYER mapping manifest | `player_mapping_manifest.json` |

Resume after human approval of story_player:

```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```

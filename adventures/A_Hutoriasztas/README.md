# A hűtőház riasztás

Az első igazi IDNE kaland az Adventure Generator v2-hez készült.

| Tétel | Útvonal |
|------|------|
| Kanonikus rövid | `adventure_brief.json` / `brief/adventure_brief.json` |
| Világigazság csomag | `adventure/DO_NOT_READ/world_truth_package.json` |
| Generációs állapot | `.generation/generation_state.json` |

**Állapot:** `AWAITING_APPROVAL` a `playtime' + `dm_feeling` – csomagok generálva; Tier B felülvizsgálat és Tier C játékteszt függőben.

| Tétel | Útvonal |
|------|------|
| Lejátszási idő + DM Jóváhagyás (spoilermentes) | `PLAYTIME_DM_FEELING_APPROVAL_PLAYER_TEST.md` |
| Lejátszási idő + DM Jóváhagyás (csak szerző) | `DO_NOT_READ/PLAYTIME_DM_FEELING_APPROVAL_REPORT.md` |
| Játékidő csomag | `adventure/DO_NOT_READ/playtime_calibration_package.json` |
| C szintű játékteszt sablon | `adventure/DO_NOT_READ/dm_feeling_reports/tier_c_playtest_questionnaire.md` |

Folytatás emberi jóváhagyás után:```bash
python3 -m idne.generate adventure_brief.json --workspace . --resume
```
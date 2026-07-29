# Compilation Report

**Adventure:** The Glass Alibi  
**Package:** `PLAYER/`  
**Compilation date:** 2026-07-29  
**Validation:** PASS

---

## Files created

| Path | Purpose |
|---|---|
| `README.md` | Package overview and quick start |
| `SETUP.md` | Preparation and role assignment |
| `HOW_TO_PLAY.md` | Rules, time, checks, communication |
| `NAVIGATION_INDEX.md` | Scene code index |
| `JOINT_SCENES.md` | Shared joint scenes (8 codes) |
| `BOOKLET_SYSTEMS.md` | Private systems-track scenes (11 codes) |
| `BOOKLET_FIELD.md` | Private field-track scenes (10 codes) |
| `ENDINGS.md` | Terminal outcome pages (5 codes) |
| `SHARED/CASE_FILE.md` | Clock, clue log, worksheets |
| `CHARACTERS/CHARACTER_SHEET_SYSTEMS.md` | Systems investigator sheet |
| `CHARACTERS/CHARACTER_SHEET_FIELD.md` | Field investigator sheet |
| `validate_player_package.py` | Structural validation helper |

---

## Validation

| Check | Result |
|---|---|
| Required file inventory | PASS |
| Scene code coverage (29 playable scene codes + 5 endings) | PASS |
| Clue record slots (16) | PASS |
| Skill check references (5) | PASS |
| Spoiler isolation (`DO_NOT_READ` not required for play) | PASS |

Run locally: `python3 validate_player_package.py` from this folder.

---

## Play parameters

| Field | Value |
|---|---|
| Players | 2 |
| Estimated playtime | 90–150 minutes |
| Play mode | Cooperative split / regroup |
| Starting clock | Saturday 19:00 |
| Report deadline | Sunday 00:30 |

---

## Setup instructions

1. Print or open **separate** systems and field booklets for each player.
2. Share one joint scene file and one case file.
3. Keep endings closed until scene **J-900**.
4. Assign roles per `SETUP.md`.
5. Begin at **J-100** in `JOINT_SCENES.md`.

---

## Printing and device requirements

| Material | Copies | Notes |
|---|---:|---|
| `JOINT_SCENES.md` | 1 shared | Both players |
| `BOOKLET_SYSTEMS.md` | 1 | Systems player only — do not share until splits |
| `BOOKLET_FIELD.md` | 1 | Field player only |
| `SHARED/CASE_FILE.md` | 1 shared | Write on printed copy or shared doc |
| Character sheets | 1 each | Match assigned role |
| `ENDINGS.md` | 1 shared | Seal until directed |
| d20 die | 1 | Shared roll acceptable |

Digital play: three isolated views (shared / systems / field) plus a hidden endings tab.

---

## Internal design

Compiled from approved design package in `DO_NOT_READ/`. Internal logic files were not modified for this compilation.

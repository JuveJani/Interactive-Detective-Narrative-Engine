# Package Export Report — A hűtőriasztás

**Stage:** `package_export`  
**Date:** 2026-08-06  
**Package status:** `PRE_PLAYTEST`

---

## Exported artifact

| Field | Value |
|-------|-------|
| **File** | `adventures/The_Cold_Storage_Alarm/The_Cold_Storage_Alarm.idne` |
| **Adventure ID** | `The_Cold_Storage_Alarm` |
| **Package schema version** | `1.0` |
| **Archive entries** | 51 bevételezési jegyzék-tracked files (52 ZIP members incl. bevételezési jegyzék + checksum) |
| **SHA-256** | `61868211e1685c3c0565df8b040a8df3bcb9a6e07255a9ead53f92b28618da49` |
| **Size** | ~89 KB |

---

## Package integrity validation

| Check | Result |
|-------|--------|
| `package_bevételezési jegyzék.json` present | PASS |
| `package_checksum.sha256` present | PASS |
| Per-entry SHA-256 vs bevételezési jegyzék | PASS |
| Checksum file vs extracted files | PASS |
| `read_idne_package` status | PASS |
| `verify_extracted_package` | PASS |

---

## Required layers included

### Adventure root (`adventure/`)

- `generation_bevételezési jegyzék.json`
- `play_bevételezési jegyzék.json`
- `PLAYER/` — full játékosnak szóló prose (96 mapped units)
- Logic packages under `DO_NOT_READ/`:
  - world_truth
  - environment
  - object_interaction
  - investigation_core
  - npc_investigation
  - investigation_flow
  - capability_check
  - story_validator
  - playtime_calibration
  - dm_feeling_validator
  - investigation_validator (IV harness)
- bevételezési jegyzéks for each layer

### Extra roots

| Prefix | Source | Purpose |
|--------|--------|---------|
| `generation/` | `.generation/` | Generation state and reports |
| `brief/` | `brief/` | Canonical adventure brief |

---

## Build command (reproducible)

```bash
python3 -c "
from pathlib import Path
from idne.idne_package import build_idne_package

workspace = Path('adventures/The_Cold_Storage_Alarm')
build_idne_package(
    workspace / 'adventure',
    workspace / 'The_Cold_Storage_Alarm.idne',
    'The_Cold_Storage_Alarm',
    extra_roots={
        'generation': workspace / '.generation',
        'brief': workspace / 'brief',
    },
)
"
```---

## Simulator v2 terhelés ellenőrzése

| Mező | Érték |
|-------|--------|
| Betöltési állapot | KÉSZ |
| Lejátszási mód | egyetlen_nyomozó |
| Csomag verzió | 1.0 |
| Integrált érvényesítés | CONDITIONAL_PASS |
| Hiányzó szimulációs rétegek | egyik sem |

---

## Exportszabályzat alkalmazva

- Az exportálás **nem** leminősítve a C szintre függőben.
- Az exportálás **nem** leminősítve a 120 perces cél feletti játékidő miatt.
- A CONDITIONAL_PASS megőrizve a lejátszási idő és a dm_feeling validátorokon.
- A csomag állapota **PRE_PLAYTEST**, nem ADVENTURE_READY.
- Nincs PLAYER vagy upstream logikai módosítás az idő csökkentése érdekében.

---

## Export utáni követelmények

1. Emberi játékteszt spoilermentes útmutató és játékidő rögzítési lap segítségével.
2. Jegyezze fel a falióra tényleges idejét (a szünetek nélkül).
3. Az ülés után töltse ki a C szintű kérdőívet.
4. A játékteszt utáni javítások után futtassa újra az integrált érvényesítést.
5. Ne jelölje kalandra késznek, amíg nincs C szintű bizonyíték, és az integrált állapot PASS.
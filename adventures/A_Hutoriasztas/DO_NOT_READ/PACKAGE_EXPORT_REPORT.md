# Csomagexportálási jelentés — A hűtőriasztás

**Stádium:** "csomagexport".  
**Dátum:** 2026-08-06  
**Csomag állapota:** `PRE_PLAYTEST`

---

## Exportált műtermék

| Mező | Érték |
|-------|--------|
| **Fájl** | `adventures/The_Cold_Storage_Alarm/The_Cold_Storage_Alarm.idne` |
| **Kalandazonosító** | `The_Cold_Storage_Alarm` |
| **Csomagséma verzió** | "1,0" |
| **Archív bejegyzések** | 51 jegyzékben nyomon követett fájl (52 ZIP-tag jegyzékkel + ellenőrző összeggel) |
| **SHA-256** | "61868211e1685c3c0565df8b040a8df3bcb9a6e07255a9ead53f92b28618da49" |
| **Méret** | ~89 KB |

---

## A csomag integritásának ellenőrzése

| Ellenőrizze | Eredmény |
|-------|---------|
| `package_bevételezési jegyzék.json` jelen | PASS |
| `package_checksum.sha256` jelen | PASS |
| Bejegyzésenkénti SHA-256 vs jegyzék | PASS |
| Ellenőrzőösszeg fájl vs kibontott fájl | PASS |
| `read_idne_package` állapot | PASS |
| `ellenőrizze_kivont_csomagot` | PASS |

---

## A szükséges rétegeket tartalmazza

### Kaland gyökér (`kaland/`)

- "generation_bevételezési jegyzék.json".
- "play_bevételezési jegyzék.json".
- `PLAYER/` — teljes, játékosra néző próza (96 feltérképezett egység)
- Logikai csomagok a `DO_NOT_READ/` alatt:
  - világ_igazság
  - környezet
  - objektum_interakció
  - vizsgálati_mag
  - npc_investigation
  - vizsgálati_folyamat
  - képesség_ellenőrzés
  - story_validator
  - playtime_calibration
  - dm_feeling_validator
  - vizsgálati_ellenőrző (IV kábelköteg)
- Megnyilvánulások minden réteghez

### Extra gyökerek

| Előtag | Forrás | Cél |
|--------|---------|---------|
| "generáció/" | `.generáció/` | Generációs állapot és jelentések |
| `rövid/` | `rövid/` | Kanonikus kalandfilm |

---

## Építési parancs (reprodukálható)```bash
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
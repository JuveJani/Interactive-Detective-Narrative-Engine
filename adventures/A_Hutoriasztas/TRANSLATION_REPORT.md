# Fordítási jelentés — A hűtőriasztás

**Forrás:** `adventures/The_Cold_Storage_Alarm/`  
**Cél:** `adventures/A_Hutoriasztas/`  
**Magyar cím:** A hűtőriasztás  
**Fordítás dátuma:** 2026-08-06

---

## Összefoglaló

| Metrika | Érték |
|---------|------:|
| Fordított fájlok (md + json) | 76 |
| Fordított JSON | 35 |
| Fordított Markdown | 41 |
| Változatlanul másolt | 0 |
| Kihagyott (bináris) | 1 (`The_Cold_Storage_Alarm.idne`) |
| Forrás szószám (md + json) | 46 349 |
| Cél szószám (md + json) | 46 947 |
| DO_NOT_READ fájlok (forrás / cél) | 22 / 22 |

---

## Angol forrás érintetlensége

**PASS** — Az angol `adventures/The_Cold_Storage_Alarm/` fa byte-szinten változatlan.

- Aggregált forrás hash (összes fájl): `d8b343a35a362c1c37df1279c40b8e823eeb1b96b8abde60a9404d43fdcdf708`
- `.idne` hash változatlan: `61868211e1685c3c0565df8b040a8df3bcb9a6e07255a9ead53f92b28618da49`
- Nem készült új `.idne` csomag a magyar fából.

---

## DO_NOT_READ lefedettség

**PASS** — Minden szerzői `DO_NOT_READ` anyag lefordítva, azonos relatív útvonalakon:

- `DO_NOT_READ/` (gyökér jóváhagyási jelentések)
- `adventure/DO_NOT_READ/` (logika csomagok)
- `adventure/DO_NOT_READ/dm_feeling_reports/`

---

## Strukturális és parse ellenőrzés

| Ellenőrzés | Eredmény |
|------------|----------|
| Relatív mappa-struktúra megőrizve | PASS |
| Minden forrásfájlnak van megfelelője (`.idne` kivétel) | PASS |
| Minden JSON parse-olható | PASS (35/35) |
| Azonosítók (pl. EVT-*, LOC-*, NPC-*) megőrizve | PASS (mintavétel: world_truth) |
| `adventure_id` mezők változatlanok | PASS |
| Hash / checksum / schema_version mezők | PASS — változatlan |

---

## Fordítási módszer

1. `scripts/translate_cold_storage_hu.py` — struktúra másolás, JSON biztonságos mezőfordítás.
2. Google Translate (deep-translator) alapfordítás + token-védelem (ID-k, időbélyegek).
3. `TRANSLATION_GLOSSARY.md` utólagos terminológiai igazítás.
4. Cím és nyelvi finomítás utófeldolgozás (`A hűtőriasztás`, `a CZ-1`).

---

## Terminológiai döntések

| Angol | Magyar | Indoklás |
|-------|--------|----------|
| cold storage | hűtőtár | Raktárhely; csarnok: hűtőtár csarnok |
| cold-chain | hideglánc | Iparági szabványos magyar kifejezés |
| loading dock | rakodópart | Természetes raktári kontextus |
| badge | belépőkártya | Hozzáférési kontextus |
| compliance deadline | megfelelőségi határidő | Jogi/üzemeltetési nyomás |
| staging control | staging szabályozás | Műszaki pontosság |
| BMS | BMS | Rövidítés változatlan |
| conditional pass | feltételes megfelelés | Validátor státusz |

Teljes glosszárium: `TRANSLATION_GLOSSARY.md`

---

## Nem szó szerinti fordítási példák

| Angol | Magyar | Megjegyzés |
|-------|--------|------------|
| "Your job tonight is to find why staging control failed" | "Ma este az a dolga, hogy kiderítse, miért nem sikerült a szakaszolási vezérlés" | Természetes magyar szórend |
| "answers are not delivered automatically" | "a válaszok kézbesítése nem történik meg automatikusan" | Játékmechanika értelme megmaradt |
| "fair-play mystery" | "fair-play rejtély" / "tisztességes rejtély" | Kontextustól függően |

---

## Futásidő-biztonság miatt változatlan mezők

- Összes belső azonosító (LOC-*, OBJ-*, NPC-*, KNOW-*, EVT-*, END-*, CHK-*, stb.)
- JSON kulcsok, enum értékek (`PASS`, `FAIL`, `CONDITIONAL_PASS`, `single_investigator`, stb.)
- `adventure_id`: `The_Cold_Storage_Alarm`
- Időbélyegek, számok, hash-ek, checksum-ok, sémaverziók
- Fájlútvonalak (`PLAYER/CHARACTERS/CHARACTER_SHEET.md`, stb.)
- Proper nevek (Elena Morales, Marcus, Lori, Pat, Dev Santos)
- Műszaki kódok (CZ-1, CMD-CZ1-MUTE-STAGE, BADGE-DEV-TEMP, stb.)
- `a.m.` / `p.m.` időformátumok (forrás szerint)

---

## Kihagyott / nem fordított

| Fájl | Ok |
|------|-----|
| `The_Cold_Storage_Alarm.idne` | Bináris kanonikus csomag — nem fordítandó, nem másolva |

---

## Fordított fájlok (teljes lista)

### Gyökér és jóváhagyások
- `README.md`, `ACTUAL_PLAYTIME_RECORDING_SHEET.md`, `PRE_PLAYTEST_PLAYER_GUIDE.md`
- `HUMAN_APPROVAL_REPORT.md`, `STORY_PLAYER_APPROVAL_PLAYER_TEST.md`
- `CAPABILITY_CHECK_APPROVAL_PLAYER_TEST.md`, `INVESTIGATION_CORE_APPROVAL_PLAYER_TEST.md`
- `INVESTIGATION_FLOW_APPROVAL_PLAYER_TEST.md`, `NPC_APPROVAL_REPORT_PLAYER_TEST.md`
- `ENVIRONMENT_OBJECT_APPROVAL_PLAYER_TEST.md`, `PLAYTIME_DM_FEELING_APPROVAL_PLAYER_TEST.md`
- `DO_NOT_READ/*.md` (10 jóváhagyási / validációs jelentés)

### PLAYER
- `adventure/PLAYER/*.md` (13 fájl)

### Logika csomagok és manifestek
- `adventure/DO_NOT_READ/*.json` (11 csomag)
- `adventure/DO_NOT_READ/dm_feeling_reports/*`
- `adventure/*_manifest.json`, `play_manifest.json`
- `brief/adventure_brief.json`, `adventure_brief.json`
- `player_mapping_manifest.json`, `PROVISIONAL_PLAYTIME_ESTIMATE.json`
- `.generation/generation_state.json`, `.generation/reports/*`

---

## Bizonytalanságok / ismert korlátok

- Gépfordítás alapja: természetes magyar cél, de emberi lektorálás ajánlott a PLAYER nagy térfogamú szövegeinél.
- A `mode` üres string mezők a tier_b_export.json-ban változatlanok maradtak.
- A magyar fa nem futtató kanonikus csomag; validátor/export nem futott a fordított fán.

---

## Megerősítések

- [x] Angol forrás byte-szinten érintetlen
- [x] Minden DO_NOT_READ anyag lefordítva
- [x] Relatív struktúra megőrizve
- [x] JSON parse: PASS
- [x] Azonosítók és numerikus hivatkozások megőrizve

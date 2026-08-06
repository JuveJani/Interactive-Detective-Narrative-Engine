# Fordítási jelentés — A hűtőriasztás

**Forrás:** `adventures/The_Cold_Storage_Alarm/`  
**Cél:** `adventures/A_Hutoriasztas/`  
**Dátum:** 2026-08-06

## Összefoglaló

| Metrika | Érték |
|---------|-------|
| Fordított fájlok (tükör) | 77 |
| Fordított Markdown | 42 |
| Fordított JSON (manifest + runtime) | 34 |
| Forrás szószám (md+json) | 59 058 |
| Cél szószám (md+json) | 58 503 |
| Nyilvános szakaszok | 96 |
| Kezdő szakasz | 636 |
| Kezdő fájl | `PLAYER/GAMEBOOK.md` |

## Angol forrás érintetlensége

Az angol `The_Cold_Storage_Alarm` fa **byte-szinten változatlan**. Nem készült `.idne` csomag.

## DO_NOT_READ

Minden `DO_NOT_READ` **Markdown** és jelentés lefordítva, azonos relatív útvonalakon.

A `DO_NOT_READ/*.json` csomagfájlok **gépi gráf- és validátor-kompatibilitás** miatt az angol forrásból másolt strukturális mezőket tartalmaznak; az emberi olvasható mezők egy része le lett fordítva, a gépi jelentésű kulcsok, ID-k és címkék változatlanok. A magyar `story_validator_package.json` kiegészült védett fájlnév-akronímákkal (`GAMEBOOK`, `PLAYER`, stb.).

## Kizárt fájlok

| Fájl | Ok |
|------|-----|
| `The_Cold_Storage_Alarm.idne` | Bináris csomag — nem tükrözendő |
| `TRANSLATION_*.md` | Fordítási meta-jelentések (csak cél) |

## Védett fájlnév- és útvonal-ellenőrzés

**PASS** — Programozott ellenőrzés: nincs lefordított fájlnév a játékos PLAYER fájlokban (`JÁTÉKKÖNYV`, `HELYSZÍNEK`, stb.). A `PLAYER/GAMEBOOK.md` hivatkozások változatlanok.

## Informális megszólítás

**PASS** — Tegezés a játékosnak szóló utasításokban (`nyisd meg`, `kezdd`, `válassz`, `menj`). Formális `Ön` / `nyissa meg` minták javítva.

## Szakaszszám-megőrzés

**PASS** — Mind a 96 angol szakasz megvan a magyar `GAMEBOOK.md`-ben; az útvonal-gráf azonos.

## Útvonal-egyenérték

**PASS** — Angol és magyar nyilvános útvonal-gráf megegyezik (programozott összehasonlítás).

## Human-delivery validáció (magyar)

```
delivery-validate: PASS (0 finding)
human-trace --seed 42: COMPLETED, route equivalence PASS
human-simulate --runs 25 --seed 42: trusted True, canonical equivalence PASS
```

- Kezdő fájl: `PLAYER/GAMEBOOK.md`
- Kezdő szakasz: **636**
- Rejtett fájl-hozzáférés: nincs

## Review körök

| Kör | Javítások |
|-----|-----------|
| 1. kör (pontosság) | 25 automatikus tegezés + kézi PLAYER dokumentumok + 47 unit-marker + 6 angol választás-sor |
| 2. kör (természetesség) | 5 szóhasználati/clarity javítás |

Részletek: `TRANSLATION_REVIEW_PASS_1.md`, `TRANSLATION_REVIEW_PASS_2.md`.

## Strukturális megjegyzések

- A `GAMEBOOK.md` lapozási utasításai (`turn to section **N**`, `**What do you do?**`, csekk-sorok) **angolul maradtak**, mert a human-delivery parser ezeket a strukturális jelölőket várja — a magyar próza nem torzult.
- A referencia PLAYER fájlok (`LOCATIONS.md`, `OBJECTS.md`, stb.) **választás-sorai angolul maradtak** a navigációs gráf-validátor kompatibilitásához; a törzs és címek magyarul vannak.
- A `<!-- unit:... -->` jelölők angol slugokkal lettek visszaállítva.

## Terminológiai bizonytalanságok

- *staging szabályozás* ↔ *refrigeration staging* — következetesen „staging szabályozás”
- *write-off* — „selejtezés” / „termék-selejtezés”
- *inference worksheet* — „következtetési munkalap”

## Állapot

A kaland státusza **PRE_PLAYTEST** maradt. A történeti logika, útvonalak, csekkek és szakaszszámok változatlanok.

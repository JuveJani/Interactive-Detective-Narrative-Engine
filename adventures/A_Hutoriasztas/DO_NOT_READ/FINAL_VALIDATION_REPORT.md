# Végső integrált érvényesítési jelentés – A hűtőriasztás

**Stádium:** `végső_érvényesítés`  
**Dátum:** 2026-08-06  
**Csomag állapota:** `PRE_PLAYTEST`  
**Kaland készen áll:** **Tiltott**

---

## Vezetői összefoglaló

Az integrált érvényesítés az összes kötelező logikai rétegben befejeződött. Nincsenek kötelező érvényesítési hibák. Az általános állapot **CONDITIONAL_PASS**, mivel a játékidő és a DM-feeling csomagok megtartják a Tier B függőben lévő tételeket, és a Tier C játékteszt bizonyítékai hiányoznak. Ezt a szabályzat megőrzi – az exportálás nincs blokkolva.

Az emberi játékteszt engedélyezett. Az Adventure Ready **nem** engedélyezett.

---

## Integrált ellenőrzési eredmény

| Mező | Érték |
|-------|--------|
| **Általános állapot** | **CONDITIONAL_PASS** |
| **Kötelező hibák** | Nincs |
| **B. szint függőben** | 7 tétel |
| **C szint teljesítve** | hamis |

### Ellenőrzőnkénti állapot

| Validator | Állapot |
|-----------|--------|
| egyetlen_nyomozó | PASS |
| világelső | PASS |
| környezet | PASS |
| objektum_interakció | PASS |
| vizsgálati_mag | PASS |
| npc_investigation | PASS |
| vizsgálati_folyamat | PASS |
| capability_check | PASS |
| vizsgálat | PASS |
| történet | PASS |
| játékidő | CONDITIONAL_PASS |
| dm_feeling | CONDITIONAL_PASS |

### B szint függőben (megőrzött)

- PT-B-PATH-MEDIAN
- PT-B-SCARCITY
- DF-B-AGENCY-NAV
- DF-B-következtetés-QUALITY
- DF-B-NPC-NEUTRALITY
- DF-B-ENDING-OPACITY
- DF-B-TIME-PRESSURE

---

## Becsült játékidő (ellenőrizetlen előrejelzés)

A lejátszási idő kalibrációs csomag útvonalérzékeny becsléseket rögzít. Ezek **csak modellelőrejelzések** – nem mért játékidő.

| Útvonal | Előrejelzett percek |
|------|------------------:|
| Legrövidebb valószínű | ~81 |
| Várható vizsgálat (PATH-MEDIAN) | ~163 |
| Széles körű feltárás | ~211 |
| Tökéletlen befejező útvonal | ~132 |
| Tökéletes befejező útvonal | ~193 |
| Határidő/időtúllépési útvonal | ~141 |

**Cél:** 120 perc  
**Várható vizsgálati útvonal:** a cél felett (a cél kb. 136%-a) – PT-TARGET-WARNING megőrizve CONDITIONAL_PASS megállapításként.

**Kalibrálási szabályzat:** A falióra tényleges játékideje **mérni kell** emberi játékteszt során, mielőtt bármilyen szabályt vagy JÁTÉKOS újrakalibrálást végezne. Nincs PLAYER vágás engedélyezett lejátszás előtti teszt. A korábbi kalandok lényegesen rövidebbek voltak, mint a modell becslései; a túlbecslést elismerik.

---

## Emberi jóváhagyások rögzítették ezt az exportálást

| Kapu | Jóváhagyva | Megjegyzés |
|------|----------|------|
| játékidő | Igen | Jóváhagyva a Playteszt előtti exportáláshoz a CONDITIONAL_PASS | ellenére
| dm_feeling | Igen | Jóváhagyva a Playteszt előtti exportáláshoz a CONDITIONAL_PASS | ellenére

Az összes upstream kaput (adventure_brief a story_playeren keresztül) korábban jóváhagyták.

---

## Repository tesztcsomag

| Hatály | Eredmény |
|-------|---------|
| Teljes lakosztály | 408 sikeres, 25 sikertelen |
| Nem szimulátor-v2 részhalmaz | 358 sikeres, 0 sikertelen |

A 25 hiba a Simulator v2 **fixture** tesztjeire korlátozódik (a `tesztek/fixtures/sim_v2_*` archívumok nem jelennek meg a munkaterületen). Adventure validation, generator v2, and layer validators pass. A A hűtőriasztás csomagellenőrzések sikeresen lefutottak az élő `.idne` betöltésen keresztül.

---

## Simulator v2 készenlét

| Ellenőrizze | Eredmény |
|-------|---------|
| Csomag rakomány | KÉSZ |
| Csomag verzió | 1.0 |
| Ellenőrző összeg | érvényes |
| Minden szimulációs réteg | jelen |
| Lejátszási mód | egyetlen_nyomozó |
| Integrált érvényesítés terheléskor | CONDITIONAL_PASS (engedélyezett) |
| A parancs megbízható kapujának érvényesítése | BLOKKOLVA (elvárható – a mennyiségi megbízhatóság integrált PASS-t igényel) |
| Determinisztikus nyom (mag=42) | TELJESÍTETT — 18 lépés, vége: END-NARRATIVE-CONTINUE |
| Monte Carlo füst (25 futás, vetőmag=42) | BEFEJEZETT — befejezések: 22 folytatás, 3 időtúllépés |

A teljes bejárást **nem** futtatták (csak korlátozott füst; az állapot robbanásveszélye elismert).

---

## Fennmaradó blokkolók az Adventure Ready előtt

1. **C szintű emberi játékteszt** – nincs koholt bizonyíték; csak kérdőív sablon.
2. **B szintű szemantikai áttekintés** — 7 függőben lévő kivonatalapú vélemény.
3. **Tényleges játékidő mérés** — szükséges a játékidőszabály újrakalibrálása előtt.
4. **Integrált PASS** – az Adventure Ready és a Simulator mennyiségi megbízhatóságához szükséges.

---

## Csomagexport

Lásd: „PACKAGE_EXPORT_REPORT.md”. Kanonikus csomag: `The_Cold_Storage_Alarm.idne`.

**Készenléti állapot:** `PRE_PLAYTEST`  
**Kalandra kész:** Tilos a Tier C bizonyítványig és az integrált PASS-ig.
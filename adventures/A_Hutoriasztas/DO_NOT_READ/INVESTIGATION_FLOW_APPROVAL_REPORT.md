# Vizsgálati folyamat és befejezések jóváhagyási jelentés – CSAK SZERZŐ / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Stage gate:** `investigation_flow`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Ne ossza szét a játékosok között.**

---

## Flow architektúra

| Alkatrész | Gróf |
|-----------|------:|
| Nyomozó órák | 5 (érkezés → archív szinkronizálás → dokkoló korlátozás → biztonsági szünet → határidő) |
| Jelenetláncok | 4 időkorlátos lánc |
| Világállami változatok | 3 (biztonsági archívum, dokk hozzáférés, ellenőrzési kíséret) |
| A hely ismételt látogatásának szabályai | 8 5 helyen |
| Következtetési áramlási kapuk | 6 (igazítva az nyomozási mag következtetésekhez) |
| Helyreállítási útvonalak | 9 diegetikus cselekvés |
| Áramlási állapotok | 3 (ACTIVE, VÁD, HATÁROZAT) |

Az órák EVT-018 és EVT-022 között vannak leképezve; `no_earlier_time_travel: true`.

---

## Befejező grafikon (szerzői térkép)

| Befejezés | Típus | Trigger összefoglaló |
|--------|------|------------------|
| END-PERFECT | tökéletes | Teljes vád (Lori + CMD-CZ1-MUTE-STAGE) + KNOW-PERFECT-RECONSTRUCTION + teljes bizonyítási tudáskészlet |
| END-PARTIAL-TECH-ONLY | részleges | A staging következtetés megoldva; csak műszaki ismeretek; helytelen vád megengedett |
| END-PARTIAL-MOTIVE-GAP | részleges | bevételezési jegyzék ismert; az újracímkézési következtetés hiányos |
| END-PARTIAL-WRONG-CULPRIT | részleges | NPC-DEV-t jelvényidőzítési ismeretekkel vádolja |
| END-PARTIAL-INCOMPLETE | részleges | Min 3 tudás; helytelen vád; sapkás felfedés |
| END-HIDDEN-RECORDS | rejtett | Csak az IT-rekordokat tartalmazó archívum szinkronizálási útvonala befejeződött |
| END-NARRATIVE-CONTINUE | narratív_kudarc | Dekoratív — a nyomozás vád nélkül folytatódik |
| END-TIMEOUT | határidő | T_DEADLINE lejárt; nincs teljes igazság |

A tökéletes befejezéshez `következtetés_perfect_resolved` szükséges – nincs automatikus feloldás pusztán a vádból.

---

## Vádkérdőív

Négy összetevő: Q-WHO, Q-HOW, Q-WHAT, Q-MOTIVE a CONC-WHO/HOW/WHAT/MOTIVE-hoz leképezve.

Helyes tökéletes válaszok: NPC-LORI (ki/indítvány), CMD-CZ1-MUTE-STAGE (hogyan/mi).

---

## Hibavédelem

- Hibák ellenőrzése a `check_label_failed` / `check_trend_failed` alternatív objektumműveletekkel az újralátogatás szabályaiban
- A következtetési hibák megőrzik a vizsgálatot a helyreállítási útvonalakon keresztül; a tökéletlen befejezések elérhetőek maradnak
- END-NARRATIVE-CONTINUE lehetővé teszi a vádemelés határidő előtti elhalasztását

---

## Helyőrző felbontás

A folyamatcsomag az NPC-csomag módosítása nélkül újraexportálja a vizsgálati mag `placeholder_resolution`-ját az NPC beszélgetési kapu kiértékeléséhez a folyamat futási idején.

---

## Érvényesítés állapota

- Vizsgálati folyamat (beleértve az érvényesítés befejezését is) - **PASS**
- Vizsgálat Ellenőrző – **PASS**
- Vizsgálati mag – **PASS**
- Világelső – **PASS**
- NPC - **PASS**
- Környezetvédelem — **PASS**
- Objektum interakció – **PASS**

Nincs képesség-ellenőrzés, JÁTÉKOS, játékidő, DM-feeling vagy csomagexport.

**Ne folytassa a képességellenőrzést, amíg a vizsgálati_folyamat-kapu nincs jóváhagyva.**
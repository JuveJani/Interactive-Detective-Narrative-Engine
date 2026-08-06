# Playtime + DM Feeling Approval Report – JÁTÉKOS TEST TULAJDONOS (Spoilermentes)

**Kaland:** A hűtőház riasztója  
**Színpadkapuk:** `játékidő`, `dm_feeling`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`

---

## Spoilermentes játékidő felmérés

Az útvonalérzékeny becslések egyetlen nyomozó szekvenciális időzítési szabályokat használnak. Az egymást kizáró utak nincsenek összeadva. Teljes PLAYER korpusz: ~7694 szó (változatlan ebben a szakaszban).

| Útvonal típusa | Becsült falióra | Elsődleges időcsoportok (perc) |
|-----------|---------------------:|---------------------------------|
| Legrövidebb valószínű | ~81 | olvasás ~50; interakció ~20; következtetés ~5 |
| Várható vizsgálat | ~163 | olvasás ~81; interakció ~44; következtetés ~23; újralátogatás ~6 |
| Széles körű feltárás (határidő előtt) | ~211 | olvasás ~103; interakció ~60; következtetés ~28; újra ~9 |
| Tökéletlen befejező útvonal | ~132 | olvasás ~65; interakció ~37; következtetés ~19 |
| Tökéletes befejező útvonal | ~193 | olvasás ~90; interakció ~58; következtetés ~28 |
| Határidő/időtúllépési útvonal | ~141 | olvasás ~74; interakció ~39; következtetés ~14 |

**A ~120 perces célhoz képest**

| Értékelés | Eredmény |
|------------|--------|
| Legrövidebb út | Cél alatt (sürgősségi/részleges útvonalakon várható) |
| Várható vizsgálati út | **Cél felett** (~136% a 120 percből) – fő figyelmeztető sáv |
| Széles körű feltárás | Jóval a cél felett |
| Becsületes túlhossz észlelve | Igen – nem takarja el az egységszám |
| Próza párnázott ezen a színpadon | Nem |

**Időnyomás:** a kimerítő feltárás meghaladja a kényelmes határidőt; A szűkösségi modell a nyomást szándékosként jelöli meg.

---

## Spoilermentes DM-feeling értékelés

| Méret | Tier A szerkezeti | Megjegyzések |
|-----------|-------------------|--------|
| Játékos ügynökség | PASS | Diegetikus navigációs/objektumcímkék; nem észleltek csupasz kódot |
| Felfedezés vs szállítás | PASS | Tárgyakkal és párbeszéddel szerzett információ |
| Kutatási mélység | PASS | Réteges helyek/objektumok; kitartó újralátogatások |
| Következtetés minősége | PASS (Tier B felülvizsgálat függőben) | Többtényezős munkalapok; nincs jelölőnégyzet színház zászlók |
| Világviszonylatban való reagálás | PASS | Az óra/állapot jelenetek változása PLAYER próza |
| Időnyomás | PASS (játékidőre delegál) | Határidő releváns; a kimerítő útvonal meghaladja az ablakot |
| Hibaminőség | PASS | Külön ellenőrizze a hibákat; helyreállítási útvonalak léteznek |
| Beszélgetési iroda | PASS (Tier B felülvizsgálat függőben) | Megbízhatósággal védett NPC-útvonalak bejelentettek |
| Az ok-okozati összefüggés vége | PASS (Tier B felülvizsgálat függőben) | Ok-okozati nyom szükséges; tökéletlen végződések átlátszatlan |
| Egynyomozós mód | PASS | Nincs partner/megosztott maradvány |

**Korlátozott statikus-DM érzés:** Strukturális csomaggal + PLAYER audit scannel értékelve. A szemantikai minőséget a Tier B kivonatokra halasztották.

---

## Tier B és Tier C állapot

| Tier | Állapot |
|------|--------|
| **B szint** | **Függőben** — 2 játékidős értékelés + 5 DM érzésértékelés PLAYER kivonat hivatkozásokkal |
| **C szint** | **Csak sablon** — kérdőív: `adventure/DO_NOT_READ/dm_feeling_reports/tier_c_playtest_questionnaire.md`; nem rögzítettek játékteszt-megfigyeléseket |
| **Kalandra kész** | **Nem elérhető** – valódi emberi játékteszt szükséges a végső készenlét előtt |

---

## Fennmaradó strukturális aggályok

1. A várt vizsgálati útvonal (~163 perc) meghaladja a 120 perces célt – erősítse meg az elfogadható útvonalakat vagy kalibrálja az emberi játékteszt után.
2. B szintű szemantikai áttekintések kiemelkedőek (ügynökség, következtetések egyértelműsége, NPC-semlegesség, befejező átlátszatlanság, időnyomás-próza).
3. C szintű emberi játéktesztet még nem hajtottak végre – ne jelölje meg, hogy Kaland kész.
4. A csomagexportálás (`.idne`) szándékosan nem jött létre.
5. A lejátszási idő érvényesítője a CONDITIONAL_PASS értéket adja vissza, amíg a Tier B elemeket meg nem oldják vagy elfogadják.

---

## Érvényesítési eredmények

| Validator | Állapot |
|-----------|--------|
| Playtime Calibration | **CONDITIONAL_PASS** |
| DM Feeling Validator | **CONDITIONAL_PASS** |
| Story Validator | **PASS** |
| Vizsgálat Validátor | **PASS** |
| Egyetlen nyomozó | **PASS** |
| Integrált érvényesítés | **CONDITIONAL_PASS** |

---

## Pontos jóváhagyás szükséges

| Választás | Akció |
|--------|---------|
| **A játékidő és a dm_feeling** jóváhagyása | Tovább a `végső_érvényesítési' szakaszhoz |
| **Felülvizsgálat kérése** | Adja meg az elérési útvonalakat, a B szintű felülvizsgálati tételeket vagy a bizonyítékok szerkezetét |
| **Elutasítás** | Csővezeték leállítása |

**Jelenlegi kapuk:** `playtime` + `dm_feeling` — **AWAITING_APPROVAL**

Nem jött létre ".idne" export. A generálás leállt: **AWAITING_APPROVAL**.
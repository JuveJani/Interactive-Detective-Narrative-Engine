# Környezeti és objektumkölcsönhatás jóváhagyási jelentés – CSAK SZERZŐKNEK / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Színpadkapuk:** `környezet`, `tárgyak`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Ne ossza szét a játékosok között.**

---

## Környezeti réteg összefoglalója

| Metrikus | Érték |
|--------|--------|
| Elsődleges vizsgálati helyszínek | 5 – dokk, hűtőház, vezérlőterem, biztonsági iroda, vezetői iroda |
| Hub helye | 1 – személyzeti pihenőhelyiség |
| Kezdési hely | LOC-DOCK (EVT-018 nyomozó érkezése) |
| Navigációs útvonalak | 20 kétirányú pár diegetikus címkékkel |
| Idő/állapot változatok | Dokkkorlátozás (EVT-020), archív szinkronizálás (EVT-019), biztonsági személyzet nélkül (EVT-021), hideg vészhelyzet (EVT-022), kíséret ellenőrzése (player_action) |
| Jellemzők | 12 – minden elsődleges hely interaktív szolgáltatáshivatkozással rendelkezik |

### Hozzáférés és útválasztás tervezése

- **Ellenőrző szoba:** Felügyelői kíséret szükséges `ACT-REQUEST-CONTROL-ESCORT`-ig a dokk eligazításánál; A törölt állapot hidegoldali és biztonsági oldali mérnöki útvonalakat tesz lehetővé. - **Biztonsági archívum:** Részleges rekordok EVT-019 előtt; teljes archívum a szinkronizálás után – értelmes visszatekintési kapu a jelvénylekérdezésekhez. - **Opcionális elágazás:** A pihenőhelyiség öltözőjének útvonala (fejlesztői jelvény) és a kikötőbe néző ablak; nem kötelező következtetés tények. - **Több útvonal:** Dokk ↔ hideg/biztonság/menedzser/szünet; break hub parancsikonok; hideg ↔ ellenőrzés kíséret után. ### Világelső igazodás

Minden hely ok-okozati idővonal-eseményekhez vagy kifejezett kalandbővítményhez vezet (LOC-FACILITY tároló). Az állapotátmenetek hivatkozása EVT-019/020/021/022 és a FACT-007 hozzáférési mintához kötött játékoskísérő akció. ---

## Objektum interakciós réteg összefoglalása

| Metrikus | Érték |
|--------|--------|
| Objektumok | 14 (4 beágyazott) |
| Akciók | 24 |
| Eredmény mértékegységei | 34 |
| Képességellenőrzések | 4 (észlelés ×3, technikai ×1) – egy-egy kísérlet |
| Játékos tudás helyőrzők megadva | Mind a 6 KNOW-* helyőrző az NPC csomagból |
| Kötelező következtetési információk | 12 információs azonosító interakciós útvonalakkal |

### Bizonyítékok útválasztása (a szerző térképe)

| Információk | Forrásobjektum/művelet | Kánoni bizonyíték | Tények |
|-------------|------------------------|--------------------|--------|
| INFO-belépőkártya-COLD-ENTRY | OBJ-belépőkártya-ARCHIVE / ACT-QUERY-COLD-ENTRY | EVD-belépőkártya-LOG | FACT-005 |
| INFO-CONTROL-ENTRY | OBJ-belépőkártya-ARCHIVE / ACT-QUERY-CONTROL-ENTRY | EVD-CONTROL-ENTRY | FACT-007 |
| INFO-EXIT-SCAN | OBJ-belépőkártya-ARCHIVE / ACT-QUERY-EXIT-SCAN | EVD-EXIT-SCAN | FACT-002 |
| INFO-BMS-COMMAND | OBJ-CTRL-TERM-02 / ACT-REVIEW-BMS-COMMAND-LOG | EVD-BMS-COMMAND | FACT-008 |
| INFO-STAGING-SUSPEND | Terminálnapló + állomásozó panel | EVD-BMS-COMMAND | FACT-009 |
| INFO-MAINT-SESSION | OBJ-CTRL-TERM-02 / ACT-REVIEW-MAINT-TICKET | EVD-MAINT-CLO1847 | FACT-018 |
| INFO-TEMP-TREND | OBJ-CTRL-TERM-02 / ACT-EXPORT-TEMP-TREND (CHK-TECH) | EVD-TEMP-TREND | FACT-010, FACT-017 |
| INFO-DOOR-AJAR | OBJ-ALARM-PANEL / ACT-REVIEW-ALARM-HISTORY | EVD-DOOR-ALARM | FACT-020 |
| INFO-LABEL-RESIDUE | OBJ-COLD-AISLE-C / ACT-SEARCH-LABEL-RESIDUE (CHK-PERCEPTION) | EVD-LABEL-RESIDUE | FACT-006 |
| INFO-LABEL-TIMESTAMP | OBJ-LABEL-RESIDUE / ACT-EXAMINE-RESIDUE-DETAIL | EVD-LABEL-RESIDUE | FACT-021 |
| INFO-bevételezési jegyzék-GAP | OBJ-bevételezési jegyzék-WORKSTATION / ACT-REVIEW-MNF-4471 | EVD-bevételezési jegyzék-POD | FACT-019, FACT-022 |
| INFO-belépőkártya-LOCKER (nem kötelező) | OBJ-LOCKER-BANK / ACT-INSPECT-LOCKER-14 | — | FACT-003 |

Egyetlen objektum sem oldja meg az esetet. A Lori-implikáció megköveteli a korrelációs jelvénynaplót (félrevezető hitelesítő adat), a vezérlőterem-bejegyzést, a jegyzék hiányát, a címke maradékát és a BMS parancsszekvenciát. ### Rejtett részletvédelem

- A sikertelen észlelési ellenőrzések (címke, retesz, szekrény) üres hibaegységeket használnak a "hints_misd_content: false" értékkel. - A maradék gyermekobjektum címkézése rejtve marad a sikeres keresésig. - A jelvényarchívum-lekérdezések blokkolva a helyrekordok=teljes_archívum időpontig (02:30 után). ### Tekintse meg újra a tervezést

- A biztonsági iroda visszatérése az archívum szinkronizálása után jelvénylekérdezések esetén. - Hideg folyosó visszatérése a jegyzék áttekintése után a maradék részleteinek értelmezéséhez. - Az objektum és a hely állapota a revisit_rules szerint megmarad. ---

## Vizsgálati útvonal vázlat

1. **Records-first:** Biztonsági riasztási előzmények → várakozás/újralátogatás archívum → jelvény + vezérlőbejegyzések → összefüggés a bevételezési jegyzék irodával. 2. **Fizikailag először:** Hideg ajtó + folyosó keresés → menedzser jegyzék → biztonsági jelvény keresztellenőrzése. 3. **Először műszaki:** Kísérő a vezérléshez → BMS parancs + hőmérsékleti trend + állomásozó panel → riasztási idővonal megerősítése. 4. **Választható parancsikon-kontextus:** A Break Room szekrény elmagyarázza a fejlesztői jelvény elérhetőségét a tettes megnevezése nélkül. ---

## Jóváhagyást igénylő feltételezések

1. Vezérlőtermi kíséret a dokk eligazítása során (a felügyelő jelen van a NPC-ELENA ütemterv szerint) – NPC-beszélgetés nem szükséges a hozzáférés engedélyezéséhez. 2. A képességellenőrző DC-k helyőrzők a capability_checks szakaszig. 3. Az információazonosítók egy későbbi szakaszban leképeződnek az nyomozási mag-hoz; PLAYER próza szerzője nem itt. 4. A „INFO-LATCH-DISTURBANCE” csak a tanúvallomások ellentmondását támogatja – a következtetés nem kötelező. **Ne folytassa a vizsgálati_magot mindaddig, amíg a környezeti és objektumkapukat jóváhagyták.**

---

## Érvényesítés állapota

- "python3 -m idne.environment_validate" - **PASS**
- `python3 -m idne.object_interaction_validate` — **PASS**
- `python3 -m idne.world_first_validate` — **PASS**
- `python3 -m idne.npc_investigation_validate` — **PASS**

Nincs vizsgálati mag, áramlás, PLAYER, lejátszási idő, DM-feeling vagy csomagexport.
# Fixed Truth Approval Report – CSAK SZERZŐKNEK / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Stage gate:** `fix_truth` (+ oksági és világállapot idővonalak)  
**Állapot:** `AWAITING_APPROVAL` (2. változat)  
**Ne ossza szét a játékosok között.**

---

## Az igazság tömör összefoglalása

**Lori Okonkwo (NPC-LORI)** logisztikai koordinátor valódi szállítói rövid szállítást fedezett fel **MNF-IN-4471** (48 beérkezett esetből 8). Nem hozott létre hiányzó készletet. Átcímkézte a raklapokat, hogy a WMS-vizsgálatok egy teljes **L-4471** tételt mutassanak, majd **Dev Santos** elfelejtett jelvényét használta fel a hűtőkamrába való belépéshez és a **felügyelet nélküli BMS-karbantartási munkamenetét** **CTRL-TERM-02**-án, hogy kiadja a **CMD-CZ1-MUTE-STAGE**-t, hogy elnémítsa az ajtót. A parancs felfüggesztette a CZ-1 kompresszor fokozatos működését, és fokozatos felmelegedést okozott. Erőszakmentes szállítmányozási csalás véletlen hűtési hibával. ---

## 1. Szállítás-csalási mechanizmus (pontos)

| Elem | Részlet |
|---------|---------|
| **SKU** | SKU-FBC-12KG (fagyasztott csont nélküli csirke 12 kg-os dobozok) |
| **Köteg** | BATCH-2026-0310-A ​​|
| **Bejövő jegyzék** | MNF-IN-4471 / L-4471 tétel / raklap PLT-4471-A |
| **A hordozó rekord** | POD-4471 felsorolja a 48 kézbesített esetet |
| **Fizikai igazság** | Csak **8 eset** érkezett PLT-4471-A-án (40-es fuvarozási eset – már meglévő eltérés) |
| **Karantén raklap** | PLT-Q118-B 48 sérült tokot tárol, Q-118 tétel, tervezett megsemmisítés |
| **Címkék eltávolítva** | LBL-4471-A (soros NL-20260312-4471A) 8 tokos részlegesről; LBL-Q118-B karantén raklapról |
| **Címkék alkalmazva** | LBL-4471-A → PLT-Q118-B (48 eset); LBL-Q118-B → 8-tokos részleges köteg |
| **Hamis WMS-megjelenés** | Szkennelés a C folyosón, a 3. rekeszben a teljes L-4471 felirat olvasható a 48-es karantén raklapon |
| **Az ellenőrzés megtévesztése** | A negyedéves ellenőrzés véletlenszerű paletta-címke vizsgálatot + jegyzékegyeztetést használ; rosszul felcímkézett 48-es raklap kezdetben átmenne |
| **Későbbi láthatóság** | Eltérés felületek címke sorozatnyomtatási előzményei alapján (NL-20260312-4471A átvételkor 8 esethez kötve), POD vs fogadási szám, esetsúly mintavétel vagy Q-118 megsemmisítési papírmunka eltérése |
| **Tényi bizonyíték** | Öntapadó hátlap NL-20260312-4471A a C folyosón; nem egyező címke-újrafelhasználási időbélyeg; MNF-IN-4471 vs POD-4471 dokumentumok |

**Fontos:** Címkecsere **újra hozzárendeli az identitást**; nem gyárt 40 hiányzó tokot. ---

## 2. Lori BMS hozzáférése (pontos)

| Elem | Részlet |
|---------|---------|
| **Terminál** | CTRL-TERM-02 (mérnöki munkaállomás, hűtési karbantartó rész) |
| **Szekció** | SVC-REFRG-MAINT (A Fejlesztő karbantartási munkamenete, zárolva maradt CLO-1847 bezáráskor) |
| **Lori igazolványa** | belépőkártya-LORI – logisztikai koordinátor; **nincs REFRG_TECH jogosultság** |
| **Hozzáférés típusa** | **Opportunista** felügyelet nélküli vállalkozói munkamenet alkalmazása; nem engedélyezett mérnöki hozzáférés |
| **Ajtónapló** | belépőkártya-LORI rögzítve a vezérlőterem ajtajánál 23:20:41 (jelenlétet bizonyít, nem szerzői jogot) |
| **Parancsnapló** | Rögzíti terminál CTRL-TERM-02 + munkamenet SVC-REFRG-MAINT + CMD-CZ1-MUTE-STAGE; **nem rögzíti Lori személyi kitűzőjét** |
| **Miért nem elegendő a naplózás önmagában** | A vezérlőteremben lévő bármely személy használhatja a feloldott munkamenetet; Fejlesztői munkamenet várható a karbantartási időszakokban; A Lorit összekapcsolni kell a jelvény belépési időzítésével + a hűtőkamrás jelvényével való visszaélésen + a nyilvánvaló indítékkal + a tárgyi bizonyíték átcímkézésével |

---

## 3. Riasztási és vezérlési sorrend (explicit lánc)

| lépés | Részlet |
|------|--------|
| **1. Első riasztás** | ALM-COLD-DOOR-AJAR, 23:18:45 |
| **2. Ok** | A hűtőház ajtaja nyitva >90 s átcímkézés közben (kocsi ék) |
| **3. Miért cselekedett Lori** | Nyitott ajtó jelzi a biztonsági pultot; dokumentálná a kiterjesztett jelenlétet csalás során |
| **4. Kiválasztott cselekvés** | CMD-CZ1-MUTE-STAGE bekapcsolva CTRL-TERM-02 (zóna teszt némítás + fokozatos tartás) |
| **5. Tervezett hatás** | Nyitott ajtó riasztó elnémítása 15 perces "teszt" ablakhoz |
| **6. Tényleges szabályozási hatás** | Ajtóriasztó elnémítva **és** CZ-1 igény-beállítás felfüggesztve |
| **7. Színpadi zavar** | A kompresszor forgása le van tiltva; A vezető egység fix fokozaton működik, amíg a szívónyomás meg nem emelkedik |
| **8. Fokozatos felmelegedés** | A glikolhurok és a raklap termikus tömegének késleltetése a befúvott levegő inflexiója ~23:27-ig |
| **9. Lori félreértése** | A vélt némaság csak a kijelentést érintette; kilépés a terminálból az átmeneti tartás törlése nélkül |
| **10. Eredményállapotok** | ALM-COLD-DOOR-AJAR elhallgatva 23:22; ALM-CZ1-STAGE-SUSP 23:24; ALM-COLD-HIGH 23:30 -14C küszöbön |

---

## 4. A függetlenség bizonyításának összefoglalása

| kérdés | A bizonyíték típusa | Főbb tények | NEM egyedül bizonyítja |
|----------|---------------|-----------|-----------------------|
| **Mi történt** | Riasztás + trend | FACT-020, FACT-010, FACT-011 | Identitás |
| **Hogyan (hűtés)** | BMS + karbantartás | FACT-008, FACT-009, FACT-018 | Ki nyomta meg a | gombot
| **Hogyan (csalás)** | Fizikai + manifeszt | FACT-006, FACT-019, FACT-021 | Ki címkézte át |
| **Ki (hozzáférés)** | Jelvénynaplók | FACT-005, FACT-002, FACT-007 | Lori, mint jelvény felhasználó (fejlesztői hitelesítő adat) |
| **Ki (szerző)** | Összefüggés | FACT-007 + FACT-005 + FACT-006 + FACT-019 + időzítés | Bármelyik napló |
| **Motívum** | Munkafolyamat | FACT-019, FACT-022, FACT-012 | Hűtéshiba |

**Tökéletes következtetés (Q-WHO):** FACT-005 + FACT-007 + FACT-006 + FACT-019 – jelvényekkel való visszaélés, jelenlét a vezérlőteremben, fizikai átcímkézés, nyilvánvaló rövidzárlat. A BMS napló (FACT-008) támogatja a (Q-HOW) metódust az FACT-018 + FACT-009 karakterláncokkal, de nem nevezi meg Lorit. ---

## Felelős színész / akciólánc

| színész | Szerep |
|-------|------|
| **NPC-LORI** | Csalás újracímkézése + opportunista BMS némító parancs |
| **NPC-DEV** | Innocent – ​​elfelejtett jelvény; karbantartási munkamenet feloldva maradt |
| **NPC-MARCUS** | Ártatlan – a reteszellenőrzés és a jelvényolvasó ellentmondása |
| **NPC-PAT** | Ártatlan tanú |
| **NPC-ELENA** | Ártatlan operatív válasz |
| **Szállító** | A valódi 40 esetből álló short-ship forrása (képernyőn kívül) |

---

## Oksági idővonal összefoglalója

22 esemény (EVT-001–EVT-022). A nyomozás időtartama változatlan **01:00–05:00**. Kulcs átdolgozása: EVT-009 ajtó-nyitott riasztó; EVT-011 CMD-CZ1-MUTE-STAGE felügyelet nélküli munkameneten; EVT-013 fokozatos hőmérséklet inflexió 23:27. ---

## Határidő mechanikája (változatlan)

- **02:30** jelvényarchívum szinkronizálása  
- **03:15** dokkkorlátozás  
- **04:30** Marcus nem elérhető  
- **05:00** leírási küszöb (FACT-015)  
- A fokozatos felfüggesztéssel kompatibilis hőmérséklet-görbe felülvizsgálva a fokozatos emelkedés érdekében

---

## A megbízhatósági vizsgálat eredményei

| Ellenőrizze | Megállapítás |
|-------|----------|
| Csalási mechanizmus | Rövid hajó már létezik; az újracímkézés csak az identitást hibásan rendeli hozzá |
| BMS hozzáférés | Opportunista munkamenet-használat; nincsenek valószínűtlen mérnöki jogosultságok |
| Vezérlőlánc | Explicit némítási reteszelés; fokozatos termikus tömegmelegedés |
| Függetlenség bizonyítása | A BMS-napló nem nevezi meg Lorit; több forrású Q-WHO |
| Validator | Világelső bérlet (G-WF1–G-WF7) |
| Fennmaradó gond | Előfordulhat, hogy a teljes WMS/POD mezőneveket később környezeti szinten igazítani kell |

---

## Emberi jóváhagyást igénylő feltételezések

1. Carrier short-ship (40 eset), mint már létező fizikai tény. 2. CMD-CZ1-MUTE-STAGE viselkedés a FACT-009 dokumentumban leírtak szerint. 3. Felügyelet nélküli SVC-REFRG-MAINT munkamenet szabályzat a CTRL-TERM-02-n. 4. Újracímkézési mechanizmus, amely elegendő az ellenőrzés megtévesztésére a mintavételig. 5. Lori, mint egyedüli szándékos szereplő (változatlanul). ---

## Pontos jóváhagyások szükségesek

| Kapu | Akció |
|------|--------|
| **`fix_igazság`** | Jóváhagyja a felülvizsgált megváltoztathatatlan igazságot, idővonalakat és bizonyítási szerkezetet |
| **`npcs`** | A fix_igazság jóváhagyásáig letiltva |

**Ne lépjen tovább az "npcs"-re, amíg ezt a változatot az ember nem hagyta jóvá.**
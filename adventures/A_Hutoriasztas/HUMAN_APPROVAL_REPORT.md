# Emberi jóváhagyási jelentés – A hűtőházi riasztás

**Stádium:** `kaland_brief`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Generátor:** Kalandgenerátor v2  
**Kanonikus rövid:** `adventure_brief.json`

---

## Három koncepciós jelölt

### A koncepció – A hűtőház riasztója (ajánlott)

Egy regionális hideglánc-raktár órák után hív egy létesítmény-automatizálási technikust, amikor a hűtés meghibásodik, és tüzet jelez, de semmi nyilvánvaló nem hiányzik. A nyomozás a jelvénynaplókon, az épületfelügyeleti exportokon, a hűtési ellenőrzéseken és a tanúk kihallgatásán keresztül fut, miközben a tárolási hőmérséklet a megfelelőségi határidő felé emelkedik. | Kritérium | Értékelés |
|-----------|------------|
| Vizsgálati mélység | Magas – a naplók, érzékelők, felülírások és a tanúvallomások keresztellenőrzése természetesen |
| Objektum-kölcsönhatási potenciál | Magas – ajtók, hűtők, BMS panelek, jelvényolvasók, karbantartási címkék |
| NPC komplexitás | Mérsékelt – öt helyszíni szerep plusz rekordalapú hatodik színész |
| Idő-nyomás potenciál | Magas – az emelkedő hőmérséklet bezárja a lehetőségeket a világon |
| Kétórás méretkockázat | Alacsony–közepes – az egyépületes lépték határos |
| Motor kompatibilitás | Erős – helyek, objektumok, NPC ismeretek, képességellenőrzések, időköltségek |

### B koncepció – A Campus Lab Containment

A közösségi főiskola létesítményeinek technikusa egy hétvégén válaszol, amikor a kémiai előkészítő laborban a HVAC leválasztása aktiválódik, és megkérdőjelezik a korlátozott tárhelyhez való hozzáférést. Az útvonalak tartalmazzák a füstelszívó érzékelőket, a vegyszerleltárt, a jelvénynaplókat és a személyzet menetrendjét a hétfői ellenőrzés előtt. | Kritérium | Értékelés |
|-----------|------------|
| Vizsgálati mélység | Mérsékelt – erős rekordok, kevesebb ipari objektum |
| Objektum-kölcsönhatási potenciál | Mérsékelt – burkolatok, tárolózárak, környezeti érzékelők |
| NPC komplexitás | Közepes – öt akadémiai és intézményi szerepkör |
| Idő-nyomás potenciál | Mérsékelt – hétfői újranyitási határidő |
| Kétórás méretkockázat | Alacsony – kompakt campus lábnyom |
| Motor kompatibilitás | Erős – kisebbnek érezhető, mint a célmélység |

### C koncepció – A kompterminál áramszünet

Egy kikötői automatizálási technikus egy önkormányzati kompterminált vizsgál, ahol az áramellátás és a jegyrendszerek meghibásodtak az ingázási csúcsidőszakban, és a tartalék generálás nem kapcsolódott be. A bizonyítékok kiterjednek a generátor karbantartására, a tehertároló relékre, a CCTV-re és a személyzeti naplókra a következő hajózás előtt. | Kritérium | Értékelés |
|-----------|------------|
| Vizsgálati mélység | Magas – mechanikus és digitális nyomok |
| Objektum-kölcsönhatási potenciál | Magas – generátorok, relék, jegyrendszerek |
| NPC komplexitás | Közepes–magas – hat tengerészeti és műveleti szerep |
| Idő-nyomás potenciál | Magas – másnap reggeli hajózás |
| Kétórás méretkockázat | Mérsékelt – a móló és a mechanikai hatókör bővülhet |
| Motor kompatibilitás | Jó – valamivel szélesebb terület, mint a karbantartó-tech gyep |

---

## Ajánlott koncepció

**A koncepció – A hűtőház riasztás**

A legjobb egyensúly a nyomozás mélysége, az objektumokkal való interakció, a technikus szerepkör illeszkedése, a korlátozott egyépületi lépték és a sürgős időkényszer között anélkül, hogy a gyilkosság vagy a nem támogatott mechanika hibája lenne. A raktári beállítás természetes hozzáférést biztosít az automatizálási szakértelemhez, a tárgyi bizonyítékokhoz és az intézményi NPC-khez, miközben kétórás statikus kalandozáson belül marad. **Ez az ajánlás nem jóváhagyás.** Emberi kijelentkezés szükséges a Rögzített Igazság létrehozása előtt. ---

## Rövid paraméterek (csak jóváhagyott séma mezőkben)

| Mező | Érték |
|-------|--------|
| A falióra tervezett időtartama | ~120 perc (`cél_játékidő_percek`: 120) |
| Világon belüli tervezett időtartam | Egy éjszakai műszak (~4 világóra) |
| Beállítás | Regionális hideglánc-elosztó raktár és kapcsolódó irodák, munkaidőn túl |
| Központi esemény | Kritikus hűtőházi hiba, valamint illetéktelen hozzáférési riasztások nyilvánvaló lopás vagy erőszak nélkül |
| Nyomozói szerep | Létesítmények automatizálási és hűtési karbantartó technikus |
| Helyek száma | 5 elsődleges + 1 másodlagos hub (lásd alább a szerkezetet) |
| NPC-szám | 5 elsődleges helyszíni + 1 csak rekord hozzáférésű rendszergazda |
| Játékos mód | `egyetlen_nyomozó` |

### A tervezett helystruktúra

1. Rakodási dokkoló  
2. Hűtőcsarnok  
3. Automatizálási vezérlőterem  
4. Biztonsági iroda  
5. Raktárvezetői iroda  
6. Személyzeti pihenőszoba (másodlagos központ)

### Tervezett vizsgálati struktúra

- A technikus intézményi nyomásra érkezik, hogy diagnosztizálja az automatizálási hibát. - Több vásári útvonal: jelvény/hozzáférési naplók, BMS trend export, hűtési alapértékek, tanúk kihallgatása, ajtók/érzékelők/ellenőrző panelek fizikai ellenőrzése. - A tanúvallomást össze kell hasonlítani a tárgyi és naplózott bizonyítékokkal. - Legalább egy fontos ellentmondás a tanúk beszámolója és a jelvény vagy az érzékelő nyilvántartása között. - Több út a részleges vagy teljes következtetésekhez; a tökéletlen befejezések megőrzik a vizsgálatot; egy teljes mértékben támogatott tökéletes befejezés. ### A tervezett időnyomás

Az emelkedő tárolási hőmérséklet és a közeledő leírási vagy megfelelési határidő fokozatosan lezárja az interjúkat és a mélyreható ellenőrzéseket. A kihagyott ablakok az önkényes kizárások helyett megváltoztatják a rendelkezésre álló lehetőségeket és a világállapotot. ### Tervezett aha szerkezettípus (megoldás nem derült ki)

**Késleltetett szignifikancia korreláció:** a rutin karbantartási időbélyeg, amely először adminisztratív szempontból jóindulatúnak tűnik, csak akkor válik értelmessé, ha kereszthivatkozásra hivatkozik egy felülírási szekvenciával és a hozzáférési időzítéssel. A játékosok rekonstruálják a jelentőséget; a motor nem adja le közvetlenül a következtetést. ### Főbb tartalmi határok

- Nincs grafikus erőszak; nincs természetfeletti felbontás. - Felnőtt munkahelyi témák: hanyagság, csalás, intézményi nyomás. - Nincs nem támogatott készlet, újrapróbálkozás, hamis ellenőrzés vagy rejtvényrendszer mechanika. - Nincs nyom-számlálás vagy narrátor megoldás szállítása. ---

## Emberi jóváhagyást igénylő feltételezések

1. **Incidens típusa** — Az ipari/hozzáférési/megfelelőségi titok az emberölés helyett elfogadható az első igazi kalandhoz. 2. **A hely és az NPC-k száma** — Öt elsődleges helyszín és öt helyszíni NPC (plusz csak a hatodik rekord) megfelel a kétórás célnak. 3. **Világon belüli időtartam** — Négy világórán belüli óra ~120 faliórapercre leképezve elfogadható ingerlés. 4. **Hang** — Módszeres, sürgető munkahelyi realizmus szenzációs erőszak nélkül. 5. **Befejezési irányelv** — Egy tökéletes befejezés plusz több tökéletlen befejezés, amelyek megőrzik a vizsgálatot, összhangban van az IDNE tervezési filozófiájával. 6. **Technikus főszereplő** — Egyetlen nyomozó automatizálási/karbantartási képességekkel (nincs külön játékos szerepkör). 7. **author_notes tervezési szándék** — A rövid JSON-ban szereplő strukturális megjegyzések csak a szerzőre vonatkoznak, és nem hagyják jóvá a történet felbontását. ---

## Pontos emberi jóváhagyások szükségesek

| Kapu | Intézkedés szükséges |
|------|------------------|
| `kaland_brief` | Tekintse át ezt a jelentést, és `adventure_brief.json`; a koncepció és a paraméterek jóváhagyása a rögzített igazság generálása előtt |
| Jövő: `fix_igazság` | Jóváhagyja a megváltoztathatatlan világigazságot, idővonalat és történetkritikus tényeket |
| Jövő: `npcs` | Jóváhagyja a főbb NPC-motivációkat, kapcsolatokat és ismereteket |
| Jövő: `investigation_flow` | A befejező szerkezet és az útvonal logika jóváhagyása |
| Jövő: "csomagexport" | Playteszt előtti csomagexportálás jóváhagyása |

**A rövid szakasz jóváhagyásához:** rögzítse a jóváhagyást generálási állapotban (`human_approvals.adventure_brief`), vagy futtassa újra a generátort dokumentált kijelentkezéssel az `ADVENTURE_GENERATOR_V2_WORKFLOW.md` szerint. ---

## Generációs állapot

A csővezeték inicializálása a rövid jóváhagyási kapunál történt. **Nem futottak későbbi szakaszok.**

- Rögzített igazság: nem jött létre  
- Idővonal rétegek: nincs létrehozva  
- NPC-csomag: nincs létrehozva  
- Környezet / objektumok / vizsgálati rétegek: nincs létrehozva  
- PLAYER tartalom: nincs létrehozva  
- `.idne` csomag: nincs létrehozva  

**Jelenlegi állapot:** `VÁRAKOZÓ_JÓVÁHAGYÁS` az `adventure_brief` szakaszban.
# A hűtőriasztás — Static Gamebook

Read the opening below, then **begin at the starting section**. Follow only the section numbers given in each choice. Do not look up internal codes or browse ahead.

## Opening

# A hűtőriasztás — Nyitó

Március 13-án, pénteken **1:00 a.m.**-kor érkezel a Northline hideglánc raktár **loading dock** rakodópartjára.

**Elena Morales** felügyelő behívott téged **on-call refrigeration technician** / ügyeletes hűtőtechnikusként. **high-temperature alarm on cold zone CZ-1**: a CZ-1 hideg zónában magas hőmérséklet-riasztás szólt **11:30 p.m.**-kor. A hűtőtár csarnok befúvott levegőjének hőmérséklete még mindig emelkedik. Ha a CZ-1 **5:00 a.m.**-ig a megfelelőségi küszöb felett marad, a létesítménynek termék-selejtezést kell kezdenie, és értesítenie kell az egészségügyi hatóságokat.

Ma éjjel a feladatod: kideríteni, miért hibásodott meg a staging szabályozás, kinek volt hozzáférése, és magyaráznak-e valamit a bevételezési nyilvántartások az eltérésekre — mielőtt a megfelelőségi határidő lezárja a műszakot.

**Kezdd a `PLAYER/GAMEBOOK.md` fájlban a 636. szakasznál.**

**Starting section: 636** — turn to section [**636**](#section-636) to begin your investigation.

---

<a id="section-105"></a>
## Section 105

### Hidden records

You used the records-only archive policy route instead of pressing further into the operational alarm. IT's sync schedule goes into the audit trail exactly as documented — a routine 2:30 a.m. batch upload, nothing more. It is a clean footnote to file, but it does not answer why CZ-1 kept climbing after the alarm sounded.

---

<a id="section-111"></a>
## Section 111

### Narrative continue

You defer final accountability while the clock still runs. Whatever you have learned so far stays open for revision from wherever you are standing in the facility. The night is not over, and neither is the investigation.

---

<a id="section-112"></a>
## Section 112

### Partial incomplete

Compliance documents operational response gaps — the riasztástörténet, supervisor actions, and temperature readings are on file, but several record threads never made it into your statement. Without a completed synthesis, the selejtezés review proceeds on the operational facts alone, and the question of exactly who caused tonight's failure stays open past your shift.

---

<a id="section-121"></a>
## Section 121

### Partial motive gap

Receiving discrepancy records are noted in your statement, and the bevételezési jegyzék exception on MNF-IN-4471 goes into the audit file as-is. The label residue and the relabeling it points to never quite connect into a finished synthesis. Someone will have to reopen the paperwork later to finish what your shift left half-drawn.

---

<a id="section-154"></a>
## Section 154

### Partial tech only

Your statement explains staging suspension and command timing in enough detail that engineering signs off on the mechanism. Compliance notes the unattended maintenance session as the technical root cause, with no name attached to who actually used it. The receiving floor's part in tonight's story never makes it into the record.

---

<a id="section-158"></a>
## Section 158

### Partial wrong culprit

Your statement centers on the contractor exit record, and Elena forwards it up the chain as filed. Dev's contract review gets flagged over a belépőkártya discrepancy he cannot fully explain away, even though the timeline you built does not quite hold together under scrutiny. Whatever actually reached into that unattended session on CTRL-TERM-02 goes unexamined tonight.

---

<a id="section-181"></a>
## Section 181

### Perfect

Your accountability statement matches independent belépőkártya, bevételezési jegyzék, physical, and BMS records. Compliance accepts a full reconstruction timeline: Lori Okonkwo borrowed Dev's forgotten belépőkártya to enter hűtőtár, swapped raklap labels to hide the short-ship, and used his unattended maintenance session to issue the mute command that suspended CZ-1 staging. Northline closes the shift with the selejtezés avoided and a documented case for both personnel review and the carrier dispute.

---

<a id="section-186"></a>
## Section 186

### Timeout

5:00 a.m. arrives before you finish. Compliance selejtezés procedures begin, and the health notification goes out on schedule regardless of what you found. Your investigation window closes under emergency protocol, whatever case you were building left unfinished.

---

<a id="section-195"></a>
## Section 195

### A jelvény helytelenül van feltüntetve

**Kérdés:** A hűtőházi jelvény bejegyzése a kilépési idők összehasonlítása után is érinti a vállalkozót?

**A konzultálandó rekordtípusok:**
- Hűtőszekrény bejövő jelvény bejegyzés (biztonsági iroda archívum)
- Vállalkozó kimenő dokkoló szkennelése (biztonsági iroda archívuma)
- A vállalkozó saját beszámolója a hátrahagyott jelvényről (szüneti szekrény vagy interjú)

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).
- Follow recovery route REC-SECURITY-ARCHIVE after incomplete synthesis. Turn to section [**304**](#section-304).
- Follow recovery route REC-BREAK-LOCKER after incomplete synthesis. Turn to section [**258**](#section-258).

---

<a id="section-214"></a>
## Section 214

### Ellenőrzési hozzáférési eltérés

**Kérdés:** Ki adhatná ki a BMS némítási parancsot hűtésmérnöki jogosultság nélkül?

**A konzultálandó rekordtípusok:**
- Control room door badge entry (security office archive)
- BMS command log and session identifier (control room workstation)

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).
- Follow recovery route REC-SECURITY-ARCHIVE after incomplete synthesis. Turn to section [**304**](#section-304).
- Follow recovery route REC-CONTROL-TERM after incomplete synthesis. Turn to section [**291**](#section-291).

---

<a id="section-218"></a>
## Section 218

### Bűnös támogatott

**Kérdés:** Melyik szerepkört támogatják a független hozzáférés, a csalás és a vezérlőterem nyilvántartása?

**A konzultálandó rekordtípusok:**
- Everything you have gathered on badge access, control room entry, and manifest fraud
- Cross-referenced timestamps from the security office

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).
- Follow recovery route REC-MANAGER-INTERVIEW after incomplete synthesis. Turn to section [**292**](#section-292).
- Follow recovery route REC-SECURITY-CROSSREF after incomplete synthesis. Turn to section [**305**](#section-305).

---

<a id="section-224"></a>
## Section 224

### Tökéletes rekonstrukció

**Kérdés:** Összekapcsolhatja a csalás eltitkolását, a jogosulatlan hozzáférést és a felfüggesztést egy támogatott idővonalon?

**A konzultálandó rekordtípusok:**
- Every record thread listed in the worksheets above
- The maintenance ticket and door-ajar alarm history (control room and security office)

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).

---

<a id="section-231"></a>
## Section 231

### Újracímkézési csalás

**Kérdés:** Használták a raklap átcímkézését a bejövő mennyiség elrejtésére?

**A konzultálandó rekordtípusok:**
- Label adhesive residue and timestamp comparison (aisle C)
- Manifest MNF-IN-4471 versus carrier POD-4471 (manager office)
- Coordinator's account of the receiving exception (manager office interview)

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).
- Follow recovery route REC-COLD-AISLE after incomplete synthesis. Turn to section [**265**](#section-265).
- Follow recovery route REC-MANAGER-MANIFEST after incomplete synthesis. Turn to section [**294**](#section-294).

---

<a id="section-237"></a>
## Section 237

### A kiváltó ok megszakítása

**Kérdés:** A felfüggesztés – nem egyedül az ajtóriasztó – okozta a tartós hőmérséklet-emelkedést?

**A konzultálandó rekordtípusok:**
- BMS command log (control room workstation)
- CZ-1 staging indicator panel (control room)
- CZ-1 supply air temperature trend export (control room workstation)

Jegyezd fel a használt rekordokat. Ha a szintézis sikertelen, jegyezd fel, mely helyeket fogja újra felkeresni.

**What do you do?**

- Mark synthesis complete if your answer is supported. Turn to section [**111**](#section-111).
- Mark synthesis incomplete and follow a recovery prompt in the recovery file. Turn to section [**297**](#section-297).
- Follow recovery route REC-CONTROL-TERM after incomplete synthesis. Turn to section [**291**](#section-291).
- Follow recovery route REC-COLD-DISPLAY after incomplete synthesis. Turn to section [**288**](#section-288).

---

<a id="section-258"></a>
## Section 258

### Break szekrény

Menjen a személyzet pihenőszobájába, és sétáljon a szekrény mellett. Ha még nem ellenőrizte a vállalkozói szekrényt, amely nyitva van, tedd meg most.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**547**](#section-547).

---

<a id="section-265"></a>
## Section 265

### Hideg folyosó

Térjen vissza a hűtőcsarnokba, és sétáljon végig a C folyosón. Ha még nem tette meg, keresse meg a padlón és a raklap felületén címkeragasztó-maradványokat.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**598**](#section-598).

---

<a id="section-288"></a>
## Section 288

### Hideg kijelző

Menjen vissza a hűtőcsarnokba, és olvasd el az élő CZ-1 befúvott levegő kijelzőt. Szinte nem kerül időbe, és megerősíti azt, amit egyébként egy export trend mutatna.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**598**](#section-598).

---

<a id="section-291"></a>
## Section 291

### Ellenőrző kifejezés

Térjen vissza az automatizálási vezérlőterembe, és közelítse meg a mérnöki munkaállomást CTRL-TERM-02. Tekintse át a BMS parancsnaplót, a lezárt karbantartási jegyet vagy a hőmérsékleti trend exportálását, amelyet még nem nyitott meg.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**619**](#section-619).

---

<a id="section-292"></a>
## Section 292

### Menedzserinterjú

Menjen a raktárvezetői irodába, és közvetlenül Lori Okonkwónak adja fel a fogadó kivételt. Hozd magaddal bármilyen nyilvánvaló vagy tárgyi bizonyítékot, amivel már rendelkezel – ez megváltoztatja, mennyit hajlandó elmondani.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**891**](#section-891).

---

<a id="section-294"></a>
## Section 294

### Kezelői jegyzék

Menjen a raktárkezelő irodájába, és hasonlítsa össze a MNF-IN-4471 jegyzéket a fogadó munkaállomáson lévő szállítói kézbesítési rekorddal.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**891**](#section-891).

---

<a id="section-297"></a>
## Section 297

### Keresse fel újra a feltáratlan forrásokat

Térjen vissza a rakodódokkhoz, és válassz ki azt a helyet, amelyiken van még bejegyzés, csekk vagy beszélgetés, amelyet még nem fejezte be. A teljes rekonstrukcióhoz minden szálat figyelembe kell venni.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**636**](#section-636).

---

<a id="section-304"></a>
## Section 304

### Biztonsági archívum

Térjen vissza a biztonsági irodába, és nyisd meg a jelvény-hozzáférési archív terminált. A lekérdező menüből futtassa azt a jelvényrekordot, amelyet még nem húzott le – a hűtőházi bejegyzést, a vezérlőterem bejegyzését vagy a vállalkozó kimenő vizsgálatát.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**963**](#section-963).

---

<a id="section-305"></a>
## Section 305

### Biztonsági kereszthivatkozás

Térjen vissza a biztonsági irodába, és hasonlítsa össze a riasztási előzményeket a már kihúzott jelvényrekordokkal. Sorolja egymás mellé az időbélyegeket.

**What do you do?**

- Go to the named location and take the action described above. Turn to section [**963**](#section-963).

---

<a id="section-326"></a>
## Section 326

**Scene transition**

### Az elszámoltatás előkészítése



A jegyzeteit szétteríti az eligazító asztalon, és elkezdi őket egy négyrészes elszámoltathatósági nyilatkozatba rendezni: ki, hogyan, mit és miért. Írás közben nem áll meg az óra.

**What do you do?**

- Continue this scene thread. Turn to section [**636**](#section-636).
- Return to the location base section for this area. Turn to section [**636**](#section-636).

---

<a id="section-327"></a>
## Section 327

**Scene transition**

### Opcionális szekrény ág



A pihenőszoba öltözősora továbbra is elérhető, amikor csak akarja. Semmi sem jár le, és semmi sem kényszeríti arra, hogy ellenőrizze.

**What do you do?**

- Continue this scene thread. Turn to section [**813**](#section-813).
- Return to the location base section for this area. Turn to section [**547**](#section-547).

---

<a id="section-355"></a>
## Section 355

**Scene transition**

### Fókuszált folyosói újralátogatás



Most, hogy látta a nyilvánvaló rést, a C folyosó másképp olvas. te már nem csak halad a sorban – nagyjából tudja, melyik raklapköteg érdemes egy második, közelebbi pillantást vetni.

**What do you do?**

- Continue this scene thread. Turn to section [**598**](#section-598).
- Return to the location base section for this area. Turn to section [**598**](#section-598).

---

<a id="section-373"></a>
## Section 373

**Scene transition**

### A címke részleteinek újralátogatása



Mivel a helyreállított címkeháttér már megtalálható az ügyiratban, visszaléphet, és összehasonlíthatja a nyomtatási időbélyegét a raklap átvételi rekordjaival anélkül, hogy újból a semmiből keresne.

**What do you do?**

- Continue this scene thread. Turn to section [**701**](#section-701).
- Return to the location base section for this area. Turn to section [**598**](#section-598).

---

<a id="section-376"></a>
## Section 376

**Scene transition**

### Vezérlőterem megközelítés



A vezérlőterem ajtaján van egy jelvényolvasó, amelyet nem használhat önállóan. Az, hogy most bejut, attól függ, hogy Elena aláírta-e már a kíséretet.

**What do you do?**

- Continue this scene thread. Turn to section [**619**](#section-619).
- Return to the location base section for this area. Turn to section [**619**](#section-619).
- Continue to scene SC-CONTROL-CLEARED. Turn to section [**400**](#section-400).
- Continue to scene SC-CONTROL-ESCORT-REQUIRED. Turn to section [**403**](#section-403).

---

<a id="section-388"></a>
## Section 388

**Scene transition**

### BMS felülvizsgálati jelenet



Miután egyszer elolvasta a parancsnaplót, most beállíthatja egymás mellett a felfüggesztési felfüggesztést és a némítási parancs időzítését, és megnézheti, milyen szorosan illeszkednek egymáshoz.

**What do you do?**

- Continue this scene thread. Turn to section [**619**](#section-619).
- Return to the location base section for this area. Turn to section [**619**](#section-619).

---

<a id="section-400"></a>
## Section 400

**Scene transition**

### A vezérlőterem törölve



Az ajtó panasz nélkül kinyílik. A feljegyzett kísérőengedélynek köszönhetően a mérnöki munkaállomásokon és a felállítási panelen felügyelet mellett dolgozhat.

**What do you do?**

- Continue this scene thread. Turn to section [**619**](#section-619).
- Return to the location base section for this area. Turn to section [**619**](#section-619).

---

<a id="section-403"></a>
## Section 403

**Scene transition**

### Escort szükséges



Az olvasó pirosan villog. Vissza kell mennie a dokkba, és meg kell kérnie Elenát, hogy írja alá a kísérőnaplót, mielőtt ez az ajtó kinyílik előtte.

**What do you do?**

- Continue this scene thread. Turn to section [**619**](#section-619).
- Return to the location base section for this area. Turn to section [**619**](#section-619).

---

<a id="section-413"></a>
## Section 413

**Scene transition**

### Dokk érkezési eligazítás



Elena végigvezeti az idővonalon az eligazító asztalnál: a 11:30 p.m. riasztást, az általa megrendelt állomásellenőrzéseket és a vezérlőterem kísérési szabályát. Gyorsan beszél, ahogy az emberek, amikor ma este már kétszer elmagyaráztak valamit, és arra számítanak, hogy újra elmagyarázzák.

**What do you do?**

- Continue this scene thread. Turn to section [**636**](#section-636).
- Return to the location base section for this area. Turn to section [**636**](#section-636).

---

<a id="section-429"></a>
## Section 429

**Scene transition**

### Első dokkfelmérés



Még semmi sem dőlt el. Sétál a dokk nyitott padlóján, és megjegyzi, hogy mely folyosókon jut el a hűtőház, az irodák és a biztonság – ez az elrendezés, amelyen egész éjszaka át-hátra fog menni.

**What do you do?**

- Continue this scene thread. Turn to section [**636**](#section-636).
- Return to the location base section for this area. Turn to section [**636**](#section-636).
- Continue to scene SC-DOCK-RESTRICTED. Turn to section [**434**](#section-434).
- Continue to scene SC-DOCK-INITIAL-SURVEY. Turn to section [**429**](#section-429).

---

<a id="section-434"></a>
## Section 434

**Scene transition**

### Dokk korlátozás aktív



A szalag most két öbölsávon fut át, és Elena maga hajtja végre. A dokkolón áthaladó lényegtelen mozgás itt megáll, amíg az áttekintése be nem fejeződik.

**What do you do?**

- Continue this scene thread. Turn to section [**636**](#section-636).
- Return to the location base section for this area. Turn to section [**636**](#section-636).

---

<a id="section-435"></a>
## Section 435

### Archív szinkronizálási szabályzat

**Csak rekordokat tartalmazó útvonal | Időköltség:** 2 perc

Az archív terminál mellé laminált hirdetmény van ragasztva, olyan kártya, amely túléli azt, aki feltette. Csak „Records Desk – J. Reeves” van aláírva, és úgy szól, mintha egy audit céljára írták volna, nem az te számára.

Az archív terminálon található iratokról szóló értesítés elmagyarázza, hogy a jelvények kötegelt feltöltése rögzített éjszakai ütemezés szerint történik. A szabványos szinkronizálás 2:30 a.m.-kor fejeződik be; a teljes lekérdezési mezők feloldása szinkronizálás után.

Nincs kivel vitatkozni rajta – a menetrend attól függ, hogy vár-e rá, vagy sem.

**What do you do?**

- Review the archive sync policy notice. Turn to section [**697**](#section-697).

---

<a id="section-436"></a>
## Section 436

**Scene transition**

### Menedzser interjú nyomás



A C folyosóból származó fizikai nyomok vagy maga a nyilvánvaló kivétel valami konkrétumot ad, amit Lori elé kell helyezni – és a válaszai megváltoznak, ha megteszi.

**What do you do?**

- Continue this scene thread. Turn to section [**891**](#section-891).
- Return to the location base section for this area. Turn to section [**891**](#section-891).

---

<a id="section-448"></a>
## Section 448

**Scene transition**

### Az archívum szinkronizálása befejeződött



Az archív terminál egyszer csenget, pontosan az ütemezés szerint, és a szinkronizálásra váró szalaghirdetés törlődik. A ma esti jelvényes tevékenység teljes rekordja végre ott áll, és arra vár, hogy lekérdezzék.

**What do you do?**

- Continue this scene thread. Turn to section [**963**](#section-963).
- Return to the location base section for this area. Turn to section [**963**](#section-963).
- Continue to scene SC-SECURITY-ARCHIVE-READY. Turn to section [**474**](#section-474).
- Continue to scene SC-SECURITY-ARCHIVE-PENDING. Turn to section [**457**](#section-457).

---

<a id="section-457"></a>
## Section 457

**Scene transition**

### Az archívum függőben van



Egy kis szinkronizálási ikon található a lekérdezési menü felében. Egyes jelvénymezők teljesen ki vannak szürkítve – a kötegelt feltöltés még nem fejeződött be, és egyetlen kattintás sem gyorsítja fel.

**What do you do?**

- Continue this scene thread. Turn to section [**963**](#section-963).
- Return to the location base section for this area. Turn to section [**963**](#section-963).

---

<a id="section-474"></a>
## Section 474

**Scene transition**

### Az archívum készen áll



Az archív terminál minden lekérdezési mezője aktív. A hűtőház-bejegyzések, a vezérlőterem-bejegyzések és a kivitelező kilépési szkennelése mind egy választásra van.

**What do you do?**

- Continue this scene thread. Turn to section [**963**](#section-963).
- Return to the location base section for this area. Turn to section [**963**](#section-963).

---

<a id="section-477"></a>
## Section 477

**Scene transition**

### Biztonsági kereszthivatkozás



Ha végre a kezében van egy jelvényrekord, az ébresztési előzmények mellé helyezi, és elkezdi egymás mellé sorba állítani az időbélyegeket – ajtót, jelvényt és riasztót, mind ugyanazon az órán.

**What do you do?**

- Continue this scene thread. Turn to section [**963**](#section-963).
- Return to the location base section for this area. Turn to section [**963**](#section-963).

---

<a id="section-484"></a>
## Section 484

**Scene transition**

### A biztonsági pult személyzet nélkül



Marcus széke üres – a menetrend szerint kötelező szünet –, de az archív terminál még mindig be van jelentkezve, és a riasztóközpont csendben végzi a dolgát nélküle.

**What do you do?**

- Continue this scene thread. Turn to section [**963**](#section-963).
- Return to the location base section for this area. Turn to section [**963**](#section-963).

---

<a id="section-503"></a>
## Section 503

**Time cost:** 2 min

### Aisle C



raklap shrink-wrap crinkles under the cold air draft as you step into the row. Aisle C runs between high raklap rows. The aisle holds still around you, waiting to be searched or left alone.

**What do you do?**

- Search the floor and pallet faces for label adhesive residue. Turn to section [**553**](#section-553).
- Return to the cold storage hall. Turn to section [**598**](#section-598).

---

<a id="section-514"></a>
## Section 514

**Time cost:** 3 min

### riasztástörténet



You scroll the alarm panel's history back past the noise of tonight's other notifications. riasztástörténet lists ALM-COLD-DOOR-AJAR at 11:18 p.m. and ALM-COLD-HIGH at 11:30 p.m. You copy both timestamps down before stepping back from the panel.

**What do you do?**

- Return to the security office. Turn to section [**963**](#section-963).

---

<a id="section-519"></a>
## Section 519

**Time cost:** 2 min

### belépőkártya archive terminal



The archive terminal's status field is the first thing you check before running any query. The belépőkártya archive terminal shows whether tonight's batch upload has finished. Whatever the sync status says, the query menu is still in front of you.

**What do you do?**

- Query cold storage inbound badge entries for tonight. Turn to section [**522**](#section-522).
- Query control room door entries for tonight. Turn to section [**544**](#section-544).
- Pull the contractor outbound dock scan record. Turn to section [**679**](#section-679).
- Return to the security office. Turn to section [**963**](#section-963).

---

<a id="section-522"></a>
## Section 522

**Time cost:** 4 min

### hűtőtár belépőkártya query



You filter the belépőkártya archive down to hűtőtár entries for tonight's shift. hűtőtár inbound log shows credential belépőkártya-DEV-TEMP at 11:14 p.m. You note the credential and timestamp before returning to the archive menu.

**What do you do?**

- Return to the badge archive menu. Turn to section [**519**](#section-519).

---

<a id="section-544"></a>
## Section 544

**Time cost:** 3 min

### automatika vezérlő belépőkártya query



You switch the filter to automatika vezérlő door entries for the same window. automatika vezérlő entry log shows belépőkártya belépőkártya-LORI at 11:20 p.m. You note the belépőkártya and timestamp before returning to the archive menu.

**What do you do?**

- Return to the badge archive menu. Turn to section [**519**](#section-519).

---

<a id="section-545"></a>
## Section 545

**Time cost:** 4 min

### BMS command log



You open the command history and scroll back to the window around the first alarm. The command log shows CMD-CZ1-MUTE-STAGE issued at 11:22 p.m. under maintenance session SVC-REFRG-MAINT. You copy the entry into your notes and back out to the workstation menu.

**What do you do?**

- Return to the engineering workstation menu. Turn to section [**985**](#section-985).

---

<a id="section-547"></a>
## Section 547

**Location:** A személyzet pihenőszobája | **Time cost:** 0 perc

### A személyzet pihenőszobája



A személyzeti pihenőhelyiségben automaták, zárható szekrények és a kikötő felé néző ablak található. Az automaták zümmögnek az egyik fal mellett, és egy félkész kávéscsésze elhagyottan hever az asztalon, ma este minden mással együtt kihűlt.

**What do you do?**

- Walk along the staff locker bank. Turn to section [**813**](#section-813).
- Look out toward the dock loading area. Turn to section [**641**](#section-641).
- Return to the loading dock. Turn to section [**636**](#section-636).
- Walk to the manager office through the staff corridor. Turn to section [**891**](#section-891).
- Follow the interior hallway to the security office. Turn to section [**963**](#section-963).
- Take the side passage toward the cold storage hall. Turn to section [**598**](#section-598).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Ask about unusual activity near the dock and cold hall. Turn to section [**935**](#section-935).
- Ask whether you could identify the person you saw. Turn to section [**943**](#section-943).
- Optionally inspect the staff locker bank. Turn to section [**327**](#section-327).

---

<a id="section-553"></a>
## Section 553

**Check:** one attempt

### Label search check



You commit to a close search of the aisle floor and raklap faces — one pass, no second look. Roll d20 plus your listed modifier once for this action.

**What do you do?**

- If your roll **succeeds**, turn to section [**749**](#section-749).
- If your roll **fails**, turn to section [**736**](#section-736).

---

<a id="section-556"></a>
## Section 556

**Check:** one attempt

### Latch észlelési ellenőrzés



You commit to a single careful look at the latch — there is no redoing this once you have decided. Roll d20 plus your listed modifier once for this action.

**What do you do?**

- If your roll **succeeds**, turn to section [**783**](#section-783).
- If your roll **fails**, turn to section [**761**](#section-761).

---

<a id="section-576"></a>
## Section 576

**Check:** one attempt

### Locker észlelési ellenőrzés



You commit to checking inside the ajar locker properly — one look, not a quick glance. Roll d20 plus your listed modifier once for this action.

**What do you do?**

- If your roll **succeeds**, turn to section [**817**](#section-817).
- If your roll **fails**, turn to section [**798**](#section-798).

---

<a id="section-590"></a>
## Section 590

**Check:** one attempt

### Trend export check



You commit to running the export through the BMS menus — one attempt, and the interface will not be forgiving of a wrong click. Roll d20 plus your listed modifier once for this action.

**What do you do?**

- If your roll **succeeds**, turn to section [**994**](#section-994).
- If your roll **fails**, turn to section [**990**](#section-990).

---

<a id="section-598"></a>
## Section 598

**Location:** Hűtőcsarnok | **Time cost:** 0 perc

### Hűtőcsarnok



Hideg levegő árad az előszoba ajtajából. A raklapsorok a CZ-1 zóna felé nyúlnak. A lélegzeted bepárásodik abban a pillanatban, amikor átléped a küszöböt, és a kompresszor zümmögése egy regiszterrel alacsonyabban szól a kelleténél. Az CZ-1 befúvott levegő kijelzője a csarnok túlsó végében világít, mintha pontozná.

**What do you do?**

- Examine the cold storage door latch and reader. Turn to section [**607**](#section-607).
- Walk the length of aisle C between the pallet rows. Turn to section [**503**](#section-503).
- Read the live CZ-1 supply air temperature display. Turn to section [**972**](#section-972).
- Follow the engineering passage to the automation control room. Turn to section [**376**](#section-376).
- Return to the loading dock. Turn to section [**636**](#section-636).
- Return toward the break room corridor. Turn to section [**547**](#section-547).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Continue scene SC-COLD-AISLE-FOCUSED. Turn to section [**355**](#section-355).
- Continue scene SC-COLD-LABEL-DETAIL. Turn to section [**373**](#section-373).

---

<a id="section-607"></a>
## Section 607

**Time cost:** 3 min

### hűtőtár door



Frost rimes the frame where the hűtőtár door meets the corridor air. The hűtőtár door has a belépőkártya-olvasó and a heavy latch. Whatever you decide to check, the door itself is not going anywhere.

**What do you do?**

- Check the latch hardware for recent disturbance. Turn to section [**556**](#section-556).
- Return to the cold storage hall. Turn to section [**598**](#section-598).

---

<a id="section-619"></a>
## Section 619

**Location:** Automatizálási vezérlőterem | **Time cost:** 0 perc

### Automatizálási vezérlőterem



Az automatizálási vezérlőteremben mérnöki munkaállomások és egy CZ-1 állomásjelző panel található. A szerverventilátorok folyamatosan zúgnak a fluoreszkáló fény alatt, és az állapotjelző LED-ek sorai villognak a szokásos mintájukban – kivéve egy panelt, amely egyáltalán nem villog.

**What do you do?**

- Approach the engineering workstation. Turn to section [**985**](#section-985).
- Inspect the CZ-1 staging indicator panel. Turn to section [**968**](#section-968).
- Return to the cold storage hall. Turn to section [**598**](#section-598).
- Return to the loading dock with the supervisor. Turn to section [**636**](#section-636).
- Return to the security office. Turn to section [**963**](#section-963).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Enter the control room after escort clearance. Turn to section [**400**](#section-400).
- Continue scene SC-CONTROL-BMS-REVIEW. Turn to section [**388**](#section-388).

---

<a id="section-623"></a>
## Section 623

### Fejlesztői jelvény

**Időköltség:** témánként változik

Ez kerül neki valamibe. Dev megdörzsöli a tarkóját, és nem fog egészen találkozni a szemével.

*Nyomja meg, hogy a vállalkozói jelvény elhagyta-e Önnel az épületet.*

**Dev Santos** azt mondja: "Lehet, hogy az ideiglenes jelvényemet a pihenőszoba öltözőszekrényében hagytam."

Úgy mondja, mintha azt remélné, hogy elmondja neki, hogy ez nem számít.

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-625"></a>
## Section 625

### Fejlesztő clo1847

**Időköltség:** témánként változik

Kérdés nélkül előhúzza a telefonján a lezárt jegyet, mint egy vállalkozó, aki a saját papírjait védi.

*Kérdezzen a CLO-1847 bezárási részleteiről.*

**Dev Santos** azt mondja: "A CLO-1847 jogos CZ-1 karbantartás volt. Lezártam a jegyet a mérnöki terminálon."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-626"></a>
## Section 626

### Fejlesztői kilépés

**Időköltség:** témánként változik

Dev még mindig kezeslábasát gombolva, szerszámos táskával a vállán, láthatóan kihúzta az ágyból Elena hívására érkezik a dokkba. Gyorsan válaszol, alig várja, hogy elszámoljon az estéjével.

*Erősítse meg, mikor hagyta el ma este a webhelyet.*

**Dev Santos** azt mondja: "Kicsit az 7:00 p.m. CLO-1847 befejezése után néztem ki a dokknál."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-629"></a>
## Section 629

### Fejlesztői munkamenet

**Időköltség:** témánként változik

Mostanra felhagyott a védekezéssel, és csak válaszolni kezdett – az a fajta fáradt őszinteség, amely azután jön, hogy már elvesztetted a vitát önmagával.

*Kérdezze meg, hogy maradt-e aktív karbantartási munkamenet CTRL-TERM-02-n.*

**Dev Santos** azt mondja: "Nem jelentkeztem ki a SVC-REFRG-MAINT munkamenetből a CTRL-TERM-02 napon. Ez volt a hiba a lezáráskor."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-636"></a>
## Section 636

**Location:** Rakodási dokk | **Time cost:** 0 perc

### Dokk betöltése



A rakodó dokkolót nátrium-lámpatestek világítják meg. A targoncák tétlenül ülnek. Elena Morales az öböl ajtaját figyeli, miközben a személyzet a dokk és az irodaszárny között mozog. A hideg hullámokban gördül le az öbölről, amikor egy ajtó megfordul, és a levegőben dízel és hűtőközeg szaga száll. Valahol 1:00 a.m. után az épület beilleszkedett egy műszak furcsa csendjébe, amely már elromlott.

**What do you do?**

- Walk through the dock corridor to the cold storage hall. Turn to section [**598**](#section-598).
- Head inside to the staff break room. Turn to section [**547**](#section-547).
- Cut through the warehouse corridor to the security office. Turn to section [**963**](#section-963).
- Take the office wing corridor to the warehouse manager office. Turn to section [**891**](#section-891).
- Review the supervisor briefing area. Turn to section [**638**](#section-638).
- Request escort clearance to the automation control room. Turn to section [**661**](#section-661).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Receive supervisor briefing at the loading dock. Turn to section [**413**](#section-413).
- Work under supervisor dock restriction enforcement. Turn to section [**434**](#section-434).
- Survey the dock and adjacent corridors. Turn to section [**429**](#section-429).
- Prepare final accountability documentation before the compliance threshold. Turn to section [**326**](#section-326).
- Confirm when you left the site tonight. Turn to section [**626**](#section-626).
- Ask about CLO-1847 closeout details. Turn to section [**625**](#section-625).
- Press about whether your contractor badge left the building with you. Turn to section [**623**](#section-623).
- Ask whether any maintenance session was left active on CTRL-TERM-02. Turn to section [**629**](#section-629).
- Ask what operational steps you ordered after the alarm. Turn to section [**660**](#section-660).
- Ask who was still on site working late. Turn to section [**656**](#section-656).
- Ask about dock access restrictions. Turn to section [**650**](#section-650).

---

<a id="section-638"></a>
## Section 638

**Time cost:** 2 min

### Supervisor briefing



You step up to the briefing table where Elena has laid out everything she has gathered so far. Elena points to a printed incident timeline on the briefing table. You note the timeline before stepping back toward the bay doors.

**What do you do?**

- Return to the loading dock. Turn to section [**636**](#section-636).

---

<a id="section-641"></a>
## Section 641

**Time cost:** 1 min

### Dock view from break room



You glance out the break room window toward the dock you just came from. Through the window you see the dock bay under sodium lights. You turn back into the room once you have seen enough.

**What do you do?**

- Return to the break room. Turn to section [**547**](#section-547).

---

<a id="section-650"></a>
## Section 650

### Elena korlátozza

**Időköltség:** témánként változik

Mostanra a dokk két öbölsávon át van szalaggal, Elena pedig úgy áll a határon, mintha bárkit is ok nélkül át akarna kelni rajta.

*Kérdezzen a dokkoló hozzáférési korlátozásairól.*

**Elena Morales** azt mondja: "3:15 a.m.-től a dokkolóhoz való hozzáférés a felülvizsgálat befejezéséig az alapvető mozgásokra korlátozódik."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-656"></a>
## Section 656

### Elena személyzet

**Időköltség:** témánként változik

Megérzi ezt, végigfutja a műszak beosztását a fejében, mielőtt válaszolna.

*Kérdezd meg, hogy ki dolgozott még mindig a helyszínen.*

**Elena Morales** azt mondja: "Lori még egyeztetett a manifesztekkel, amikor megérkeztem. Marcus körözött. Pat legénysége a vádlottak padján volt."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-660"></a>
## Section 660

### Elena sürgős

**Időköltség:** témánként változik

Elenának egyik kezében egy telefon, a másikban egy vágólap van, és úgy válaszol, ahogy ma este már három másik embernek válaszolt – gyorsan, lassítás nélkül.

*Kérdezze meg, milyen műveleti lépéseket rendelt el a riasztás után.*

**Elena Morales** azt mondja: "A 11:30-as riasztás után elrendeltem az állomásellenőrzést, és visszahívtam a fejlesztőt. A leírás tervezése akkor kezdődik meg, ha átlépjük a 5:00 a.m.-t."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**636**](#section-636).

---

<a id="section-661"></a>
## Section 661

**Time cost:** 3 min

### Escort granted



Elena does not argue when you ask for automatika vezérlő access — she just reaches for the escort log. Elena signs an escort log and walks you toward the engineering passage. With her signature down, you are cleared to make the walk on your own from here.

**What do you do?**

- Return to the loading dock. Turn to section [**636**](#section-636).

---

<a id="section-679"></a>
## Section 679

**Time cost:** 3 min

### Contractor exit scan



You pull the outbound dock scan log to check the contractor's departure. Outbound dock scan shows Dev Santos exited at 7:02 p.m. You note the exit time before returning to the archive menu.

**What do you do?**

- Return to the badge archive menu. Turn to section [**519**](#section-519).

---

<a id="section-697"></a>
## Section 697

### Archív szinkronizálási szabályzat

**Csak rekordokat tartalmazó útvonal | Időköltség:** 2 perc

Az archív terminál mellé laminált hirdetmény van ragasztva, olyan kártya, amely túléli azt, aki feltette. Csak „Records Desk – J. Reeves” van aláírva, és úgy szól, mintha egy audit céljára írták volna, nem az te számára.

Az archív terminálon található iratokról szóló értesítés elmagyarázza, hogy a jelvények kötegelt feltöltése rögzített éjszakai ütemezés szerint történik. A szabványos szinkronizálás 2:30 a.m.-kor fejeződik be; a teljes lekérdezési mezők feloldása szinkronizálás után.

Nincs kivel vitatkozni rajta – a menetrend attól függ, hogy vár-e rá, vagy sem.

**What do you do?**

- Return to the security office. Turn to section [**963**](#section-963).

---

<a id="section-701"></a>
## Section 701

**Time cost:** 4 min

### Label timestamp comparison



With the backing strip in hand, you lay it next to the raklap receipt printout. You compare the recovered backing print timestamp to raklap receipt records. The timestamp does not match the original partial-raklap location. You note the mismatch in your case file before returning to the aisle.

**What do you do?**

- Return to aisle C menu. Turn to section [**503**](#section-503).

---

<a id="section-736"></a>
## Section 736

**Time cost:** 5 min

### Label search — failure



You go over the floor and raklap faces as closely as you can manage. The floor and raklap faces show routine warehouse wear; no distinctive trace stands out. You come up empty and step back toward the aisle entrance.

**What do you do?**

- Return to aisle C menu. Turn to section [**503**](#section-503).

---

<a id="section-749"></a>
## Section 749

**Time cost:** 5 min

### Label search — success



You go over the floor and raklap faces inch by inch, ignoring the cold in your fingers. You recover a strip of label backing with fresh adhesive trace. You bag the strip carefully and head back toward the aisle entrance.

**What do you do?**

- Return to aisle C menu. Turn to section [**503**](#section-503).

---

<a id="section-761"></a>
## Section 761

**Time cost:** 4 min

### Latch check — failure



You crouch and check the latch plate as carefully as the light allows. The latch hardware looks ordinary from this angle; nothing useful stands out. Nothing here changes what you already knew, so you head back to the door.

**What do you do?**

- Return to the cold storage door menu. Turn to section [**607**](#section-607).

---

<a id="section-783"></a>
## Section 783

**Time cost:** 4 min

### Latch check — success



You crouch and run a light along the latch plate, looking past the obvious. Under the latch plate you notice fresh scuffing where hardware was recently handled. You note the wear pattern before straightening up and returning to the door.

**What do you do?**

- Return to the cold storage door menu. Turn to section [**607**](#section-607).

---

<a id="section-798"></a>
## Section 798

**Time cost:** 3 min

### Locker inspect — failure



You ease the ajar door open and check what is inside. The locker interior looks unremarkable at a glance. Nothing stands out, so you step back from the locker bank.

**What do you do?**

- Return to the locker menu. Turn to section [**813**](#section-813).

---

<a id="section-813"></a>
## Section 813

**Time cost:** 2 min

### Staff locker bank



The locker row smells like cold coffee and cleaning solution, mostly undisturbed. Several lockers are closed. One contractor locker door sits slightly open. The open locker door is not going to close itself while you decide.

**What do you do?**

- Inspect the ajar contractor locker. Turn to section [**576**](#section-576).
- Return to the break room. Turn to section [**547**](#section-547).

---

<a id="section-817"></a>
## Section 817

**Time cost:** 3 min

### Locker inspect — success



You ease the ajar door open and check past the folded coveralls inside. Inside the locker you find a contractor temporary belépőkártya that was not returned at exit. You note the belépőkártya and step back from the locker bank.

**What do you do?**

- Return to the locker menu. Turn to section [**813**](#section-813).

---

<a id="section-842"></a>
## Section 842

### Lori vezérlés min

**Időköltség:** témánként változik

Amikor megemlíti a vezérlőszobát, végre rád néz – röviden –, mielőtt visszafordulna a képernyőjéhez.

*Érdeklődjön a vezérlőterem látogatásáról 23:20 körül.*

**Lori Okonkwo** azt mondja: "11:20 körül rövid időre beléptem a vezérlőterembe, hogy megnézzem a képernyőn megjelenő üzenetet."

Kisebbnek hangzik, mint egy jelvénynapló.

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**891**](#section-891).

---

<a id="section-847"></a>
## Section 847

### Lori tagadja a hideget

**Időköltség:** témánként változik

Lori nem néz fel az egyeztető képernyőről, amikor belépsz. Válasza azonnali, lapos, és egyértelműen elhangzott, mielőtt még megkérdezted.

*Kérdezze meg, hogy bement-e a hűtőházba a munkaidő után.*

**Lori Okonkwo** azt mondja: "Ma este nem mentem hűtőházba. A munkavégzés miatt az íróasztalnál voltam."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**891**](#section-891).

---

<a id="section-852"></a>
## Section 852

### Lori címke

**Időköltség:** témánként változik

A címkemaradvány az, amivel nem tud vitatkozni. Bármilyen higgadtság is volt, végül elmegy.

*Nyomja meg a C folyosón talált címkemaradékot.*

**Lori Okonkwo** azt mondja: "Címkemaradványt talált. A fogadó rekordok és a padlómunkák a C folyosón össze vannak kapcsolva. Nem számítottam arra, hogy a riasztás továbbra is fennáll."

Ez van a legközelebb ahhoz, hogy sajnálja.

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**891**](#section-891).

---

<a id="section-855"></a>
## Section 855

### Lori nyomás

**Időköltség:** témánként változik

A nyilvánvaló kivételt maga elé tárja. Egy pillanatig csak nézi a számokat, és a megkomponált hang elcsúszik.

*Nézz szembe a MNF-IN-4471 nyilvánvaló kivételes bizonyítékaival.*

**Lori Okonkwo** azt mondja: "A MNF-IN-4471 nem egyezik a szolgáltató POD-jával. Megpróbáltam törölni a kivételt az ellenőrzési mintavétel előtt."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**891**](#section-891).

---

<a id="section-881"></a>
## Section 881

**Time cost:** 3 min

### Maintenance ticket



You pull up the maintenance ticket queue and find the most recently closed entry for CZ-1. Ticket CLO-1847 closed at 6:30 p.m. with a note that session SVC-REFRG-MAINT was left unlocked. You note the closeout comment and return to the workstation menu.

**What do you do?**

- Return to the engineering workstation menu. Turn to section [**985**](#section-985).

---

<a id="section-891"></a>
## Section 891

**Location:** Raktárvezető iroda | **Time cost:** 0 perc

### Raktárvezetői iroda



A raktárvezetői iroda vészhelyzetre nyitva tart. Lori Okonkwo fogadó munkaállomása továbbra is aktív egyeztetési képernyőt mutat. Az íróasztal nagy részét a jegyzéknyomatok kötegei borítják, és a fluoreszkáló lámpa a fej fölött éppen annyira villog, hogy észrevegye. Lori nem hagyta el tovább ezt a széket, mint amennyit a ma esti ébresztő önmagában megmagyarázna.

**What do you do?**

- Review the open receiving reconciliation screen. Turn to section [**901**](#section-901).
- Return to the loading dock. Turn to section [**636**](#section-636).
- Return to the break room. Turn to section [**547**](#section-547).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Ask whether you entered cold storage after hours. Turn to section [**847**](#section-847).
- Ask about your control room visit around 23:20. Turn to section [**842**](#section-842).
- Confront with manifest exception evidence from MNF-IN-4471. Turn to section [**855**](#section-855).
- Press about label residue found in aisle C. Turn to section [**852**](#section-852).
- Continue scene SC-MANAGER-PRESSURE-TOPIC. Turn to section [**436**](#section-436).

---

<a id="section-899"></a>
## Section 899

**Time cost:** 5 min

### bevételezési jegyzék comparison



You pull the bevételezési jegyzék up side by side with the scanned delivery record. bevételezési jegyzék MNF-IN-4471 shows eight cases received while carrier POD-4471 lists forty-eight. You note the quantity gap before returning to the receiving workstation.

**What do you do?**

- Return to the manifest menu. Turn to section [**901**](#section-901).

---

<a id="section-901"></a>
## Section 901

**Time cost:** 2 min

### Receiving workstation



The reconciliation screen is exactly how it was left, exception flag still lit. The receiving screen still flags bevételezési jegyzék MNF-IN-4471. The exception is still open, waiting on whichever record you check first.

**What do you do?**

- Compare manifest MNF-IN-4471 to the carrier delivery record. Turn to section [**899**](#section-899).
- Cross-reference the signed carrier POD against bay assignments. Turn to section [**958**](#section-958).
- Return to the manager office. Turn to section [**891**](#section-891).

---

<a id="section-907"></a>
## Section 907

### Marcus riasztó

**Időköltség:** témánként változik

A panelnél Marcus egy piros szövegsorra mutat, amely még mindig a riasztási előzményekben található. Ebben a részben biztos, mert végignézte, ahogy történik.

*Kérdezze meg, mikor jelent meg először a magas hőmérsékleti riasztás a panelen.*

**Marcus Hale** azt mondja: "A magas hőmérsékletű riasztó 11:30 p.m.-kor érte el a panelemet. Közvetlenül ezután hívtam Elenát."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**963**](#section-963).

---

<a id="section-917"></a>
## Section 917

### Marcus szakadék

**Időköltség:** témánként változik

Felemeli a jelvényolvasót a fiókja ellen, és Marcus magabiztossága először megvillan. te helyett az archív terminál felé pillant.

* Kérdezze meg, hogy a jelvényolvasó naplója eltérhet-e a reteszellenőrzéstől.*

**Marcus Hale** azt mondja: "Még nem húztam le a jelvényolvasó naplóját, amikor bejött a magas hőmérsékleti riasztás."

Ez nem vallomás – csak annak beismerése, hogy a körei és a rekordrendszer valójában soha nem beszéltek egymással ma este.

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**963**](#section-963).

---

<a id="section-934"></a>
## Section 934

### Marcus retesz

**Időköltség:** témánként változik

Marcus a biztonsági iroda riasztópultja mellett áll, a kulcsok még mindig az övére vannak akasztva. Már eldöntötte, hogy ez a beszélgetés arról szól, hogy megbizonyosodjon arról, hogy helyesen végezte a munkáját, és úgy válaszol, mintha egy körnaplóból olvasna.

*Kérdezd meg, mit ellenőriztél a hűtőkamra ajtaján a körök során.*

**Marcus Hale** azt mondja: "Megnéztem a hűtőház reteszét a 11:00 p.m.-nál, úgy tűnt, hogy be van kapcsolva."

A levegőbe csapja az időt, mintha az megoldaná az ügyet.

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**963**](#section-963).

---

<a id="section-935"></a>
## Section 935

### Pat ajtót

**Időköltség:** témánként változik

Pat még mindig egy felmosókocsit tol, amikor elkapod őket a pihenőhelyiség közelében. Egy korty automata kávé között válaszolnak, mintha ez csak egy újabb furcsa dolog, ami műszakban történt.

*Kérdezzen szokatlan tevékenységről a dokk és a hűtőcsarnok közelében.*

**Pat Nguyen** azt mondja: "Kitámasztottam egy kocsi dokk ajtaját 11:40 p.m. körül. Láttam valakit a hidegcsarnok közelében, de egy arcot nem."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**547**](#section-547).

---

<a id="section-943"></a>
## Section 943

### Pat sil

**Időköltség:** témánként változik

Többre törekszel, és Pat valójában ezen gondolkodik, ahelyett, hogy csak vállat vonna – ami azt jelzi, hogy nem titkolnak semmit, egyszerűen nincs mit találni.

*Kérdezze meg, hogy tudja-e azonosítani a látott személyt.*

**Pat Nguyen** azt mondja: "Úgy mozogtak, mint aki ismeri az elrendezést. Nem tudom megnevezni őket."

**What do you do?**

- Return to your current location menu or continue the conversation. Turn to section [**547**](#section-547).

---

<a id="section-958"></a>
## Section 958

**Time cost:** 3 min

### Carrier POD cross-reference



You flip open the carrier POD binder to check the bay assignment against what was actually logged. The signed POD assigns the full shipment to bay C3 expecting a complete lot scan. You note the assignment before returning to the receiving workstation.

**What do you do?**

- Return to the manifest menu. Turn to section [**901**](#section-901).

---

<a id="section-963"></a>
## Section 963

**Location:** Biztonsági iroda | **Time cost:** 0 perc

### Biztonsági iroda



A biztonsági iroda rendelkezik egy riasztó panellel és egy jelvényarchívum terminállal. Kis monitorok fala cikázik az üres folyosókon, és a riasztópanel hangszórója időnként kattog, mintha mondani akarna valamit, mielőtt ismét elhallgat.

**What do you do?**

- Review recent alarm history on the security panel. Turn to section [**514**](#section-514).
- Open the badge access archive terminal. Turn to section [**519**](#section-519).
- Return to the loading dock. Turn to section [**636**](#section-636).
- Return to the break room. Turn to section [**547**](#section-547).
- Open inference worksheet: A jelvény helytelenül van feltüntetve. Turn to section [**195**](#section-195).
- Open inference worksheet: Ellenőrzési hozzáférési eltérés. Turn to section [**214**](#section-214).
- Open inference worksheet: Bűnös támogatott. Turn to section [**218**](#section-218).
- Open inference worksheet: Tökéletes rekonstrukció. Turn to section [**224**](#section-224).
- Open inference worksheet: Újracímkézési csalás. Turn to section [**231**](#section-231).
- Open inference worksheet: A kiváltó ok megszakítása. Turn to section [**237**](#section-237).
- Return to security after the badge archive sync completes. Turn to section [**448**](#section-448).
- Use the security office while the guard is on mandatory break. Turn to section [**484**](#section-484).
- Review the records-only archive sync policy. Turn to section [**435**](#section-435).
- Ask what you checked on the cold storage door during rounds. Turn to section [**934**](#section-934).
- Ask whether the badge reader log could differ from a latch check. Turn to section [**917**](#section-917).
- Ask when the high-temperature alarm first appeared on your panel. Turn to section [**907**](#section-907).
- Return to query the synced badge archive. Turn to section [**474**](#section-474).
- Continue scene SC-SECURITY-CROSSREF. Turn to section [**477**](#section-477).

---

<a id="section-968"></a>
## Section 968

**Time cost:** 3 min

### Staging indicator panel



A single amber indicator on the staging panel is the only thing not blinking in sequence. The CZ-1 staging panel shows compressor staging suspended. You write down the panel state and turn back toward the room.

**What do you do?**

- Return to the control room. Turn to section [**619**](#section-619).

---

<a id="section-972"></a>
## Section 972

**Time cost:** 1 min

### Live temperature display



You wipe frost off the sensor display to get a clean reading. The live display reads CZ-1 supply air at a sustained rise above the cold-chain threshold. You log the number and turn back toward the rest of the hall.

**What do you do?**

- Return to the cold storage hall. Turn to section [**598**](#section-598).

---

<a id="section-985"></a>
## Section 985

**Time cost:** 1 min

### Engineering workstation



The workstation screen is still lit, exactly the way someone left it hours ago. Engineering workstation CTRL-TERM-02 is awake. The terminal is not locking itself while you decide what to open first.

**What do you do?**

- Review the BMS command log on this terminal. Turn to section [**545**](#section-545).
- Open the closed maintenance ticket for CZ-1. Turn to section [**881**](#section-881).
- Export the CZ-1 supply air temperature trend. Turn to section [**590**](#section-590).
- Return to the control room. Turn to section [**619**](#section-619).

---

<a id="section-990"></a>
## Section 990

**Time cost:** 5 min

### Trend export — failure



You start the export and wait through the progress bar. The export wizard closes with an error; no trend file is saved. You close the failed dialog and step back from the terminal.

**What do you do?**

- Return to the engineering workstation menu. Turn to section [**985**](#section-985).

---

<a id="section-994"></a>
## Section 994

**Time cost:** 5 min

### Trend export — success



You start the export and wait through the progress bar, watching it climb. The trend export completes. Supply air inflects upward after 11:27 p.m. You save the export locally and step back from the terminal.

**What do you do?**

- Return to the engineering workstation menu. Turn to section [**985**](#section-985).

---

# Környezet és objektumok interakciójának jóváhagyási jelentése – JÁTÉKOS TEST TULAJDONOS (Spoilermentes)

**Kaland:** A hűtőház riasztója  
**Színpadkapuk:** `környezet`, `tárgyak`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`

---

## Helyszín skála

| Metrikus | Állapot |
|--------|---------|
| Elsődleges vizsgálati helyszínek | 5 — rakodópálya, hűtőcsarnok, automatizálási vezérlőterem, biztonsági iroda, raktárvezetői iroda |
| Hub helye | 1 – személyzeti pihenőhelyiség |
| Kezdési hely | Rakodási dokk (technikus érkezése) |
| Rövid léptékű cél | Met |

---

## Navigáció és felfedezés

- Diegetikus mozgáscímkék mindenhol – nincsenek csupasz célkódok a játékosok számára.
- Minden kimenő navigációs linkhez meghatározott visszatérési útvonalak.
- Hub-csatlakozás: a pihenőszoba a dokkolóhoz, a menedzser irodához, a biztonsághoz és a hűtőtárolóhoz alternatív útvonalakon keresztül kapcsolódik.
- Több ésszerű útvonal a bizonyítékterületek között kényszerített lineáris sorrend nélkül.

---

## Idő- és állapotfüggő változatok

| Változat | A játékos által látható hatás |
|---------|-----------------------|
| Archívum szinkronizálása (~02:30) | A biztonsági jelvényrekordok lekérdezhetővé válnak |
| Dokk korlátozás (~03:15) | Dokk hozzáférési attribútumok változásai; felügyelői végrehajtás |
| Biztonsági szünet (~04:30) | Az őr átmenetileg nincs az asztaltól |
| Megfelelőségi küszöb (05:00) | Hűtési vészhelyzeti protokoll változat |
| Irányítóteremi kíséret | A mérnöki helyiség zárva van, amíg a felügyelő kíséretet meg nem kaptak a dokkban |

A változatok igazodnak a jóváhagyott NPC rendelkezésre állási ablakokhoz.

---

## Látogassa meg újra és legyen kitartása

- A fizikai változások, a felfedezett információk és az engedélyezett hozzáférés az ismételt látogatások alkalmával is fennáll.
- Nincs a hely vagy az objektum állapotának csendes visszaállítása.
- **Jelentős újralátogatás:** A biztonsági iroda az archívum szinkronizálása után feloldja a jelvényrekord-lekérdezéseket.
- **Választható hasznos ág:** A pihenőhelyiség öltözőszekrényének ellenőrzése és a kikötőre néző ablak megfigyelése.

---

## Objektum interakciós minőség

| Követelmény | Állapot |
|-------------|--------|
| Réteges interakciós mélység | Igen — megközelítés → vizsgálat/keresés → részletezés/összehasonlítás |
| Nincs információ egyedül a helymegadásról | Igen – minden dokumentumszerű/fizikai tényhez szükséges műveletek |
| Sikertelen ellenőrzések esetén védett rejtett részletek | Igen – külön hibaegységek, nincsenek kihagyott tartalomra vonatkozó tippek |
| Műszaki vizsgálat | Igen – BMS terminál export (műszaki ellenőrzés), állomásozó panel |
| Rendes fizikai vizsgálat | Igen – ajtózár, folyosói maradványok keresése, szekrény ellenőrzése |
| Nincs egyetlen objektum esetfeloldása | Igen – több rekordkészlet és fizikai nyomkövetés korrelációja szükséges |
| Nincsenek tetszőleges zárak vagy csupasz kódok | Igen – az idővonalhoz/NPC menetrendhez kötött kísérő és archív kapuk |
| Nincs leltár/újrapróbálkozás/hamis ellenőrzés/rejtvénymechanika | Igen |

Minden fontos művelet deklarálja a következőket: jogosultság, játékos címke, időköltség, állapothatás (ahol alkalmazható), információs hivatkozás, ismétlési szabályzat, visszatérési útvonal és kanonikus forrás.

---

## Játékos tudás helyőrző hivatkozás

Az NPC rétegből hat dokumentarista tudáshelyőrző engedélyezhető objektum-interakciókon keresztül:

- Jelvény bejegyzési rekord
- BMS parancsnapló
- A vezérlőterem belépési jegyzőkönyve
- Nyitott ajtó riasztás története
- Címke maradékanyag felfedezése
- bevételezési jegyzék/POD mennyiségi hézag

---

## Fennmaradó strukturális aggályok

1. A vizsgálati mag még nem jött létre – az információazonosítók helyőrzők maradnak a rétegek közötti kapcsolódásig.
2. Az objektumrétegben deklarált képesség-ellenőrző DC-k; teljes ellenőrzési definíciók várják a capability_checks szakaszt.
3. A JÁTÉKOS kézbesítési próza nem szerződik – csak strukturális csomagok.
4. A KNOW-* helyőrzőkre hivatkozó NPC beszélgetési csomópontok a vizsgálati mag huzalozásától függenek.
5. Escort-to-control művelet objektum szintű hozzáférés engedélyezése; beszélgetési szín NPC/sztori szakaszokra halasztott.

---

## Pontos jóváhagyási lehetőségek

| Választás | Opciók |
|--------|----------|
| **Környezeti és objektumrétegek jóváhagyása** | Folytassa a vizsgálat_mag generálásával |
| **Felülvizsgálat kérése** | Hely, navigáció, objektum vagy hozzáférési változások megadása |
| **Elutasítás** | Csővezeték leállítása; nem generál vizsgálati magot |

**Jelenlegi kapuk:** "környezet", "objektumok" — **AWAITING_APPROVAL**

---

## Érvényesítés állapota

- Környezeti érvényesítés – **PASS**
- Objektum interakció érvényesítése — **PASS**
- Világelső érvényesítés – **PASS**
- NPC érvényesítés - **PASS**

Nincs vizsgálati mag, áramlás, PLAYER, lejátszási idő, DM-feeling vagy csomagexport.
# NPC jóváhagyási jelentés – CSAK SZERZŐI / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Színpadkapu:** `npcs`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Ne ossza szét a játékosok között.**

---

## NPC névsor (6)

| ID | Név | Szerep | Megtévesztő profil |
|----|------|------|------------------|
| NPC-LORI | Lori Okonkwo | Logisztikai koordinátor | Magas kijátszás; elrejti az átcímkézést és a terminálhasználatot |
| NPC-MARCUS | Marcus Hale | Éjszakai biztonság | Őszinte, de tévedett az ajtóbiztonsággal kapcsolatban |
| NPC-DEV | Dev Santos | Hűtéstechnikai vállalkozó | Becsületes; elrejti az elfelejtett jelvényt és a feloldott munkamenetet |
| NPC-ELENA | Elena Morales | Ügyeleti felügyelő | Intézményi nyomás; védi a személyzetet kezdetben |
| NPC-PAT | Pat Nguyen | Tisztító ólom | Részleges tanú; csak sziluett |
| NPC-IT | Jordan Reeves | Csak rekordok | Archívum szinkronizálási szabályzata; nincs helyszíni párbeszéd |

---

## A tudás és a bizonyság eredete

Minden "information_known_model" bejegyzés deklarálja a "provenance_category"-t:

- **közvetlen_akció** — Lori újracímkézése, Fejlesztői karbantartás/kilépés, Elena korlátozás
- **közvetlen_megfigyelés** — Marcus reteszelés/riasztás, Pat dokk tevékenység
- **incorrect_sumption** — Marcus-jelvény felülvizsgálati hiányossága
- **elmondta** - Elena riasztási értesítés
- **kikövetkeztetve** - Elena Loriról, aki későn dolgozik (nincs tudomás az átcímkézésről)
- **házirend** — IT szinkronizálási ütemezés

Lori **nem tud** tanúbizonyságot tenni Dev privát cselekedeteiről forrás nélkül. Pat **nem tudja** azonosítani Lorit. A fejlesztő **nem tudja** átcímkézés.

---

## Ellentmondás támogatása

- **Marcus retesz vallomása** vs **jelvény bejegyzési rekord** (TOPIC-DOOR-ROUNDS ↔ TOPIC-belépőkártya-RECORDS)
- **Lori megtagadja** a hideg hozzáférést vs. **jelvénynapló** és **címkemaradvány**
- **A jelvényre utaló fejlesztő** vs **kilépési vizsgálat idővonala**

---

## A bizalom és a kapcsolat hatásai

- A **Dev** vádaskodása növeli **Lori** bizalmát (+10) – bűnbak ösztönzés
- **Lori** vádaskodása csökkenti **Elena** bizalmát (-15) – a felügyelő védelme
- A **Dev** vádaskodása csökkenti az **Elena** bizalmát (-20) – a gyártó védelme
- Az elbocsátás sürgőssége csökkenti **Elena** bizalmát (-12)

---

## A világállami idővonalhoz kötött elérhetőség

| NPC | A vizsgálat hatása |
|-----|-------------------------|
| Marcus | Elérhető LOC-SECURITY 04:30-ig; szünetben nem elérhető |
| Elena | Magas nyomás érkezéskor; kikényszeríti a dokk korlátozását 03:15 után |
| Dev | Rövid ideig csak telefonon, majd a helyszínen a dokknál |
| Lori | Kitérő a vezetői irodában |
| Pat | Megtekinthető 03:00-ig, majd telephelyen kívül |
| IT | Csak felvételek 02:30 után, archívum szinkronizálása |

---

## A beszélgetés szerkezetének összefoglalása

- **18 téma** vegyes feloldási típusokkal (világidő, bizalom, tudás_tartott, játékos_akció)
- **6 beszélgetési grafikon** (csak IT-rekordok a témán/irányelvön keresztül; nincs párbeszédgrafikon)
- **6 bizonyságtételi hivatkozás** a beszélgetési csomópontokhoz
- A nyomásérzékeny Lori csomópontokhoz player_action kapukra, valamint dokumentumfilmes/fizikai tudás-helyőrzőkre van szükség

---

## Jóváhagyást igénylő feltételezések

1. Vizsgálat Az alapvető tudásazonosítók (`KNOW-*`) helyőrzői egy későbbi szakaszban kapcsolódnak össze.  
2. A környezet/objektum/rekord rétegek által biztosított játékos tudás-helyőrzők (`KNOW-belépőkártya-ENTRY-RECORD` stb.).  
3. A `player_action` nyomáskapuk egy későbbi szakaszban a képesség-ellenőrzésekhez illeszkednek.  
4. NPC-IT csak rekordok kézbesítése archív témán keresztül, élő beszélgetés nem.

**Ne lépjen tovább a környezeti szakaszba, amíg az NPC kaput jóváhagyta.**
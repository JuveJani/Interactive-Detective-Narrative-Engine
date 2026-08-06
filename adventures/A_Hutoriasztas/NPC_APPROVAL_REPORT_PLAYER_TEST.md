# NPC jóváhagyási jelentés – JÁTÉKOS TEST TULAJDONOS (Spoilermentes)

**Kaland:** A hűtőház riasztója  
**Színpadkapu:** `npcs`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`

---

## NPC-szám és szerepkör

| Metrikus | Állapot |
|--------|---------|
| Helyszíni NPC-k | 5 – biztonsági, vállalkozó, logisztika, felügyelő, takarítóvezető |
| Csak rekordok szerepköre | 1 — jelvényarchívum adminisztrátor |
| Szereplefedettség | Üzemeltetési, biztonsági, szállítói, menedzsment, létesítmények, nyilvántartások |

Minden jóváhagyott rövid skálacél teljesül.

---

## A kapcsolatok bonyolultsága

- Supervisor ↔ személyzeti jelentési élek (logisztika, biztonság)
- Szállító ↔ létesítmény kapcsolat (vállalkozó)
- Kolléga él (biztonsági ↔ takarítás)
- A bizalommódosítók közé tartoznak a **pozitív és negatív** delták (nem globálisan pozitív)
- Kapcsolati reakciók a vád és a tanúvallomás kihívására

Nincsenek melodráma élek; a kapcsolatok munkahelyiek.

---

## Tudáshatár-minőség

- 18 információs bejegyzés mindegyik származási kategóriát deklarál (megfigyelés, cselekvés, feltételezés, elmondott, kikövetkeztetett, irányelv)
- Csak a rekordokat tartalmazó NPC csak a szabályzattal rendelkezik; nincs helyszíni beszélgetési grafikon
- A nagy megtévesztésű NPC-nek külön témái vannak az elkerülő és a nyomással függő felvételi témákról
- A tévesen őszinte NPC kifejezetten helytelen feltételezést tartalmaz
- A játékos tudás helyőrzői a rétegek közötti összekapcsoláshoz dokumentálva (még nincs a vizsgálati mag ismétlődése)

---

## A bizonyság sokfélesége

| Kategória | Jelen |
|----------|----------|
| Igazságos hiányos | Igen (biztonsági körök) |
| Hihető hibák | Igen (retesz és olvasóköz) |
| Kitérő tagadás | Igen (logisztikai koordinátor) |
| Vonakodó / kínos igazság | Igen (vállalkozói jelvény/munkamenet) |
| Részleges megfigyelés | Igen (tisztító ólom sziluett) |
| Az intézményi nyomás kialakítása | Igen (felügyelői sürgősség) |
| Csak rekordokra vonatkozó szabályzat | Igen (archívum szinkronizálása) |

Nincsenek kiállítási dump csomópontok; ismételje meg a házirendeket, ahol szükséges.

---

## Bizalom / nyomás rendszer lefedettsége

- NPC-nkénti kezdeti bizalom, gyanú, nyomásértékek
- Bizalmi küszöbök kényes témákban
- Játékos-akció kapuk nagynyomású belépőkhöz
- Állapothatások a kiválasztott csomópontokra (bizalom/gyanú delták)
- Vádmódosítók kapcsolatfeltételes előjellel

A társadalmi siker csak a nyilvánosságra hozatalt és az együttműködést változtatja meg – nincs igazságmutáció.

---

## Ellentmondás támogatása

- Kapcsolt témapárok ajtóvallomáshoz és jelvényrekordokhoz
- Nyomon követési csomópont, amelyhez a játékos dokumentációs ismerete szükséges a tévedés elfogadása előtt
- Több független NPC-perspektíva az átfedő időablakra vonatkozóan

---

## Időfüggő elérhetőség

- A szegmensek a jóváhagyott vizsgálati ablakhoz igazítva (01:00–05:00)
- Biztonsági pult rés a kötelező szünet alatt
- Dokkkorlátozás végrehajtása a vizsgálat közepén
- Vállalkozó távoli, majd helyszíni átállás
- A takarítás leadása csökkenti az interjúhoz való hozzáférést
- Az archívum szinkronizálása megnyitja a rekordok útvonalát

Az elérhetőség megváltoztatja a vizsgálati lehetőségeket, nem csak az ízt.

---

## Fennmaradó strukturális kockázatok

1. A vizsgálati alapcsomag még nem jött létre – a tudás/tanúságazonosítók a kapcsolódásra váró helyőrzők.  
2. A játékos tudás helyőrzői környezet/objektum/rekord rétegeket igényelnek a dokumentumismeret biztosításához.  
3. A „player_action” nyomásazonosítók egy későbbi szakaszban képesség-ellenőrzési leképezést igényelnek.  
4. NPC-IT a rekordok kézbesítési mechanizmusa a vizsgálati folyamat útválasztásától függ (még nincs megszerkesztve).

---

## Pontos jóváhagyási lehetőségek

| Választás | Opciók |
|--------|----------|
| **NPC-réteg jóváhagyása** | Tovább a környezet létrehozásához |
| **Felülvizsgálat kérése** | Adja meg az NPC-t, a témát vagy a rendelkezésre állás változásait |
| **Elutasítás** | Csővezeték leállítása; nem generál környezetet |

**Jelenlegi kapu:** `npcs` — **VÁR_JÓVÁHAGYÁS**

---

## Érvényesítés állapota

- `python3 -m idne.npc_investigation_validate` — **PASS**
- Világelső érvényesítés (változatlan igazságcsomag) - **PASS**

Nincs környezet, objektum, vizsgálati folyamat, PLAYER vagy „.idne” tartalom.
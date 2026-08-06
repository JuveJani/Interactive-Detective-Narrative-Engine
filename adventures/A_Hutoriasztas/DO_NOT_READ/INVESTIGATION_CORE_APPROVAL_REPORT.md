# Vizsgálati alapjóváhagyási jelentés – CSAK SZERZŐKNEK / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Színpad kapuja:** `vizsgáló_mag`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Ne ossza szét a játékosok között.**

---

## Entitás leltár

| Entitás | Gróf |
|--------|------:|
| Világtények | 22 (FACT-001–022 a jóváhagyott igazságból) |
| Tárgyi bizonyíték | 9 (EVD-* a világigazsághoz igazítva) |
| Észrevételek | 15 (objektum-kölcsönhatás forrása) |
| Tanúságtétel | 18 (TEST-* NPC témákhoz kapcsolódik) |
| Tudás | 40 kanonikus KNOW-* rekord |
| Kapcsolatok | 9 (támogat / ellentmond / független) |
| Hipotézisek | 6 (játékos szintézis szükséges) |
| Következtetések | 6 (visszanyerési útvonalakkal) |
| Következtetések | 5 (mi, hogyan, ki, motívum, tökéletes rekonstrukció) |
| Bizonyítékok | 9 (≥2 független útvonal a főbb következtetésekhez) |

---

## Helyőrző felbontás

| Régi helyőrző | Kánoni tudás |
|--------------------|----------------------|
| KNOW-belépőkártya-ENTRY-RECORD | KNOW-belépőkártya-COLD-ENTRY |
| KNOW-BMS-COMMAND-LOG | KNOW-BMS-COMMAND |
| KNOW-CONTROL-ROOM-ENTRY | KNOW-CONTROL-ENTRY |
| KNOW-DOOR-AJAR-ALARM | KNOW-DOOR-AJAR |
| KNOW-LABEL-RESIDUE | KNOW-LABEL-RESIDUE |
| KNOW-bevételezési jegyzék-POD-GAP | KNOW-bevételezési jegyzék-GAP |

A INFO-* objektumazonosítók az `object_interaction_links.info_id_to_knowledge_id`-n keresztül a KNOW-*-ra vannak leképezve.

---

## Bizonyító szerkezet (szerzői térkép)

**Bűnös (NPC-LORI):** PROOF-WHO-DOC (jelvény helytelen hozzárendelése + vezérlőbejegyzés + jegyzék) vs PROOF-WHO-PHYS (címkecsalás + maradék + jegyzék).

**Módszer (CMD-CZ1-MUTE-STAGE):** PROOF-HOW-TECH (BMS-parancs + szakaszolás + karbantartási munkamenet + hozzáférési eltérés) vs PROOF-HOW-PHYS (ajtóriasztás + parancs + szakaszolás + vezérlőbejegyzés).

**Termékkockázati ok:** PROOF-WHAT-TECH (hőmérséklet-trend + átmeneti ok + ajtó nyitva) vs PROOF-WHAT-OPS (BMS-parancs + felfüggesztés felfüggesztés + ajtó nyitva).

**Motívum (nyilvánvaló csalás):** PROOF-MOTIVE-DOC (nyilvánvaló hiányosság + felderítési kivétel + újracímkézési csalás) vs PROOF-MOTIVE-PHYS (maradék + időbélyeg + átcímkézési csalás).

**Tökéletes rekonstrukció:** A PROOF-PERFECT-FULL szintézist igényel KNOW-PERFECT-RECONSTRUCTION.

---

## Következtetési lánc

1. **INF-belépőkártya-MISATTRIBUTED** – vállalkozói kilépés vs. hideg belépés hitelesítő adatai  
2. **INF-STAGING-ROOT-CAUSE** – a felfüggesztési hajtások folyamatos emelkedése  
3. **INF-RELABEL-FRAUD** – az átcímkézés rövid hajót rejt  
4. **INF-CONTROL-ACCESS-MISMATCH** — logisztikai jelvény a gépházban némítás közben  
5. **INF-CULPRIT-SUPPORTED** – független adatfolyamok azonosítják a logisztikai koordinátort  
6. **INF-PERFECT-RECONSTRUCTION** — teljes mértékben támogatott idővonal a tökéletes befejező kapuhoz  

A sikertelen következtetés a tökéletlen következtetéseket bizonytalanná teszi; helyreállítási útvonalak neve végrehajtható objektum/NPC műveletek.

---

## Ellentmondáskezelés

- KNOW-MARCUS-LATCH-CHECK ellentmond a KNOW-belépőkártya-COLD-ENTRY → tudás szerint megoldva (jelvénynapló)

---

## Érvényesítést támogató melléktermék

Az "investigation_validator_package.json" kizárólag az integrált vizsgálat-ellenőrző futtatására lett létrehozva kapcsolt rétegeken. Nem szerzői játékosokkal szembeni színpad. A befejező elérhetőség szándékosan üres (a végződések nem generálódnak).

---

## Érvényesítés állapota

- Vizsgálati mag – **PASS**
- Vizsgálat Ellenőrző – **PASS**
- Világelső – **PASS**
- NPC - **PASS**
- Környezetvédelem — **PASS**
- Objektum interakció – **PASS**

Nincs vizsgálati folyamat, képességellenőrzés, PLAYER, játékidő, DM-feeling vagy csomagexport.

**Ne folytassa a vizsgálati folyamatot mindaddig, amíg a vizsgálati_mag kaput nem hagyták jóvá.**
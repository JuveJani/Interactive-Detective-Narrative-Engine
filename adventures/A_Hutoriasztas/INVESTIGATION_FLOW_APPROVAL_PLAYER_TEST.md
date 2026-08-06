# Vizsgálati folyamat és a befejezések jóváhagyási jelentése – JÁTÉKOS TEST TULAJDONOS (Spoilermentes)

**Kaland:** A hűtőház riasztója  
**Stage gate:** `investigation_flow`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`

---

## Spoilermentes áramlási értékelés

| Követelmény | Állapot |
|-------------|--------|
| Végrehajtható állapotvezérelt áramlás | Igen – 19 zászló/számláló deklarált kezdeti állapottal |
| Időtől/állapottól függő változatok | Igen – 5 óra a jóváhagyott idővonal-eseményekhez igazítva |
| Nincs korábbi utazás | Igen – csak előre állítható óramodell |
| Érvényes navigációs és helyreállítási útvonalak | Igen – 9 diegetikus helyreállítási útvonal hely/akció hivatkozásokkal |
| Értelmes újralátogatások | Igen – archív szinkronizálás, jegyzék → folyosó, kísérő engedélyezése, opcionális szekrény |
| Csak rekordokat tartalmazó NPC-útvonal végrehajtható fájl | Igen — IT archívum szinkronizálási házirend lépése az archívum ablakláncában |
| A sikertelen ellenőrzések megőrzik az alternatív útvonalakat | Igen – keresse fel újra az alternatívákat a címkekereséshez és a temp trend |
| A sikertelen következtetések megőrzik a vizsgálatot | Igen – mind a 6 következtetési kapu `failure_preserves_investigation` |
| Nincs egyszerű célkód-választás a folyamat metaadataiban | Igen — player_label a lépcsőn és a helyreállítási útvonalakon |

A jelenetláncok kiterjednek a nyitási nyomozásra, az archívum ablakára, a dokkkorlátozási nyomásra és az utolsó órás vádemelésre, a lineáris helymeghatározás kényszerítése nélkül.

---

## Spoilermentes befejezés értékelése

| Befejező kategória | Gróf | Az igazság feltárása |
|-----------------|------:|---------------|
| Tökéletes | 1 | Teljes (teljes rekonstrukciós szintézist igényel + helyes többrészes vád) |
| Részleges / tökéletlen | 4 | Korlátozott részleges hatótávolságok; nincs teljes igazság |
| Rejtett | 1 | Csak tipp hatóköre |
| Határidő | 1 | Nincs |
| Vizsgálat-folytató (dekoratív) | 1 | Nincs |

| Követelmény | Állapot |
|-------------|--------|
| A végső vád több összetevőt támogat | Igen — 4 kérdőíves kérdés (ki, hogyan, mi, indíték) |
| A végződések állapotból, bizonyításból és döntésekből származnak | Igen – állapotvezérelt és határidő lejárt triggerek |
| Nincs csak végső választási logika | Igen – ismeretek és következtetési kapuk szükségesek |
| Tökéletlen végződések átlátszatlan | Igen – max_knowledge_revealed_ids sapkák minden részleges/rejtett végződésnél |
| Egy teljes mértékben támogatott tökéletes befejezés | Igen — END-PERFECT a szükséges_teljes_próbával |
| Több vizsgálatot megőrző tökéletlen befejezés | Igen — 4 részleges + 1 dekoratív folytatás |
| Nincs automatikus tökéletes feloldás | Igen – következtetés_perfect_resolved flag |
| Határidő integrált | Igen — END-TIMEOUT T_DEADLINE-kor blokkolja a határidő utáni vádat |

---

## Fennmaradó strukturális aggályok

1. A képesség-ellenőrzési definíciók még nincsenek generálva – az ellenőrzési hiba váltakozása csak a folyamatban van deklarálva.
2. A PLAYER kézbesítési próza nincs szerzője – a scene_unit_ids strukturális helyőrzők.
3. Az NPC-csomag továbbra is tartalmaz örökölt helyőrző-azonosítókat; A flow újraexportálja a magfelbontási térképet a futásidejű kiértékeléshez.
4. END-NARRATIVE-CONTINUE dekoratív jelzéssel – a játéktesztnek meg kell erősítenie, hogy nem érzi magát kemény megállásnak.
5. B szintű játékteszt felülvizsgálata javasolt a vád határain lévő tökéletlen véget érő átlátszatlanság miatt.

---

## Pontos jóváhagyási lehetőségek

| Választás | Akció |
|--------|---------|
| **A vizsgálat folyamatának és befejezésének jóváhagyása** | Tovább a capability_checks generálásához |
| **Felülvizsgálat kérése** | A folyamat, a befejezés vagy a vád módosításainak megadása |
| **Elutasítás** | Csővezeték leállítása; ne generáljon képességellenőrzéseket |

**Jelenlegi kapu:** `investigation_flow` — **AWAITING_APPROVAL**

---

## Érvényesítés állapota

- Vizsgálati folyamat ellenőrzése (beleértve a befejező ellenőrzéseket) - **PASS**
- Vizsgálat Ellenőrző – **PASS**
- Vizsgálati mag – **PASS**
- Világelső – **PASS**
- NPC - **PASS**
- Környezetvédelem — **PASS**
- Objektum interakció – **PASS**

Nincs képesség-ellenőrzés, JÁTÉKOS, játékidő, DM-feeling vagy csomagexport.
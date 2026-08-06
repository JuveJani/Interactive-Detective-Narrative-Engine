# Képességellenőrzés jóváhagyási jelentés – CSAK SZERZŐI / SPOILERT TARTALMAZÓ

**Kaland:** A hűtőház riasztója  
**Stage gate:** `capability_checks`  
**Állapot:** `VÁRAKOZÁS_JÓVÁHAGYÁS`  
**Ne ossza szét a játékosok között.**

---

## Ellenőrizze a készletet

| Ellenőrizze az azonosítót | Szülői intézkedés | Képesség | DC | Sikertudás | Kötelező tisztességes út |
|----------|---------------|------------|---:|-------------------|-----------------------|
| CHK-PERCEPTION-LATCH | ACT-CHECK-LATCH-WEAR | felfogás | 13 | KNOW-LATCH-DISTURBANCE | Nem (választható íz) |
| CHK-PERCEPTION-LABEL | ACT-SEARCH-LABEL-RESIDUE | felfogás | 14 | KNOW-LABEL-RESIDUE | Nem |
| CHK-TECH-TEMP-TREND | ACT-EXPORT-TEMP-TREND | műszaki | 12 | KNOW-TEMP-TREND | Nem |
| CHK-PERCEPTION-LOCKER | ACT-INSPECT-LOCKER-14 | felfogás | 11 | KNOW-belépőkártya-LOCKER | Nem (nem kötelező ág) |

A jóváhagyott objektum-interakciós réteg által hivatkozott négy ellenőrzés definiálva van. Egyetlen NPC vagy környezetellenőrzési hivatkozás sem marad megoldatlan. Ebben a kalandban nincs szociális csekk.

---

## DC igazoló térkép

| Ellenőrizze | Band | Indoklás |
|-------|------|------------|
| RETESZ (13) | Kemény | Finom szerszámkopás fagyköd és ipari világítás mellett |
| CÍMKE (14) | Kemény | Finom ragasztónyomok keverednek a rutin folyosósúrolással |
| TEMP-TREND (12) | Közepesen magas | A BMS menük exportálása üzemidő nyomás alatt |
| LOCKER (11) | Közepes | Jelvény a kezeslábas alatt, zsúfolt szekrényben |

---

## Hiba és helyreállítás igazítása

| Ellenőrizze | Hibajelző | Alternatív útvonal (áramlás/IV) | Megőrzött vizsgálat |
|-------|------------------------------------------|--------------------------|
| CHK-PERCEPTION-LATCH | check_latch_failed | REC-SECURITY-ARCHIVE | Jelvényarchívum + Marcus retesz vallomása |
| CHK-PERCEPTION-LABEL | check_label_failed | REC-MANAGER-bevételezési jegyzék | Nyilvánvaló rés + koordinátori bizonyság szálak |
| CHK-TECH-TEMP-TREND | check_trend_failed | REC-COLD-DISPLAY | Élő hőmérséklet kijelzés + állomásozó panel + BMS parancs |
| CHK-PERCEPTION-LOCKER | check_locker_failed | REC-SECURITY-ARCHIVE | Jelvényarchívum rekordok téves hozzárendelési következtetéshez |

A meghibásodási egységek nem tartalmaznak rejtett sikerű szivárgást. Egyetlen ellenőrzés sem von le közvetlenül következtetéseket vagy tökéletes rekonstrukciót.

---

## Rögzített igazság invariánsai

Minden ellenőrzés hamisnak nyilvánítja a „changes_evidence_existence”, „changes_document_contents”, „changes_fixed_truth” és „changes_npc_fixed_knowledge”. A siker csak a jóváhagyott bizonyítékokhoz és tényekhez kötődő, már létező megfigyeléseket fedi fel.

---

## Módosító források

Hét módosító forrás deklarált (észlelés, érvelés, technikai, erő, mozgékonyság, meggyőzés, megfélemlítés). Mind a négy ellenőrzés explicit modifier_source_id összerendeléseket használ. Jogosultság: aktív nyomozó (egyedülálló); aktív nyomozó a helyszínen (két játékos).

---

## Érvényesítés

- Képességellenőrzés - **PASS**
- Vizsgálati folyamat – **PASS**
– Vizsgálat Ellenőrző (IV-CAPABILITY-DELEGATE) – **PASS**
- Objektum interakció – **PASS**
- NPC - **PASS**
- Vizsgálati mag – **PASS**
- Világelső – **PASS**

Csomag hash: "8c3d2448706524927cf1f0d157fc255d8c28364be5d98314e11fc6414cd245d4"

---

## Pontos jóváhagyási lehetőségek

| Választás | Akció |
|--------|---------|
| **A képességellenőrzések jóváhagyása** | Tovább a PLAYER (`story_player`) generációhoz |
| **Felülvizsgálat kérése** | Adja meg a DC, a hiba vagy az alternatív útvonal módosításainak ellenőrzését |
| **Elutasítás** | Csővezeték leállítása; ne generáljon PLAYER tartalmat |

**Ne lépjen tovább a story_playerhez, amíg a capability_checks kaput jóvá nem hagyták.**
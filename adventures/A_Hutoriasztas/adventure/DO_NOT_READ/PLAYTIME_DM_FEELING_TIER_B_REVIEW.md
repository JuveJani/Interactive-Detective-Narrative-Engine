# B szintű áttekintési anyag – CSAK SZERZŐKNEK

Emberi szemantikai áttekintés a játékidő és a DM érzés kapuihoz. PLAYER részleteket tartalmaz.

## Playtime Tier B

### PT-B-PATH-MEDIAN
- **Várható:** Erősítse meg a várható 120 perces egyéni munkamenet medián várható útvonalát
- **Megoldva:** Hamis

### PT-B-SCARCITY
- **Várható:** A teljes körű feltárás befejezése előtt erősítse meg, hogy a határidők nyomása érezhető
- **Megoldva:** Hamis

## DM Feeling Tier B

### DF-B-AGENCY-NAV (player_agency)
- **Várható:** A navigáció és az objektumválasztás diegetikus marad, csupasz kódok nélkül
- **Kivonat** `PLAYER/LOCATIONS.md` / Dokkoló betöltése:```
### Loading dock

**Location:** Loading dock | **Time cost:** 0 min

The loading dock is lit by sodium fixtures. Forklifts sit idle. Elena Morales watches the bay doors while staff move between the dock and the office wing. Cold rolls off the bay in waves whenever a door cycles, and the smell of diesel and refrigerant hangs in the air. Somewhere past 1:00 a.m., the building has settled into the strange quiet of a shift that has already gone wrong.

**What do you do?**

- Walk through the dock corridor to the cold storage hall.
- Head inside to the staff break room.
- Cut through the warehouse 
```- **Kivonat** `PLAYER/OBJECTS.md` / Jelvényarchívum terminál:```
### Badge archive terminal

**Time cost:** 2 min

The archive terminal's status field is the first thing you check before running any query. The badge archive terminal shows whether tonight's batch upload has finished. Whatever the sync status says, the query menu is still in front of you.

**What do you do?**

- Query cold storage inbound badge entries for tonight.
- Query control room door entries for tonight.
- Pull the contractor outbound dock scan record.
- Return to the security office.

<!-- unit:unit-badge-cold-entry -->
```### DF-B-következtetés-QUALITY (következtetési minőség)
- **Várható:** A következtetési munkalapok több rekordból álló szintézist igényelnek beágyazott válaszok nélkül
- **Kivonat** `PLAYER/következtetés.md` / A jelvény helytelenül hozzárendelve:```
### Badge misattributed

**Question:** Does the cold-storage badge entry still implicate the contractor after comparing exit timing?

**Record types to consult:**
- Cold storage inbound badge entry (security office archive)
- Contractor outbound dock scan (security office archive)
- Contractor's own account of the badge left behind (break room locker or interview)

Record the records you used. If synthesis fails, note which locations you will revisit.

**What do you do?**

- Mark synthesis complete if your answer is supported.
- Mark synthesis incomplete and follow a recovery prompt in the rec
```- **Kivonat** `PLAYER/következtetés.md` / Tökéletes rekonstrukció:```
### Perfect reconstruction

**Question:** Can you connect fraud concealment, unauthorized access, and staging suspension into one supported timeline?

**Record types to consult:**
- Every record thread listed in the worksheets above
- The maintenance ticket and door-ajar alarm history (control room and security office)

Record the records you used. If synthesis fails, note which locations you will revisit.

**What do you do?**

- Mark synthesis complete if your answer is supported.
- Mark synthesis incomplete and follow a recovery prompt in the recovery file.
```### DF-B-NPC-NEUTRALITY (beszélgetési_ügynökség)
- **Várható:** Az NPC párbeszéd megőrzi a gyanús semlegességet és a bizalomfüggő hangszínváltásokat
- **Kivonat** `PLAYER/NPCS.md` / Marcus retesz:```
### Marcus latch

**Time cost:** varies by topic

Marcus stands by the security office's alarm panel, keys still hooked to his belt from rounds. He has already decided this conversation is about confirming he did his job correctly, and he answers like he is reading from a rounds log.

*Ask what you checked on the cold storage door during rounds.*

**Marcus Hale** says: "I checked the cold storage latch at 11:00 p.m. It looked engaged."

He taps the time into the air like it settles the matter.

**What do you do?**

- Return to your current location menu or continue the conversation.

<!-- unit
```- **Kivonat** `PLAYER/NPCS.md` / Lori címke:```
### Lori label

**Time cost:** varies by topic

The label residue is the thing she cannot argue with. Whatever composure she was holding onto finally goes.

*Press about label residue found in aisle C.*

**Lori Okonkwo** says: "You found label residue. Receiving records and floor work in aisle C are connected. I did not expect the staging alarm to persist."

It is the closest she comes to sounding sorry.

**What do you do?**

- Return to your current location menu or continue the conversation.

<!-- unit:unit-elena-urgency -->
```### DF-B-ENDING-OPACITY (befejező_oksági összefüggés)
- **Várható:** A tökéletlen befejezések átlátszatlanok maradnak; A tökéletes befejezés teljes támogatott rekonstrukciót igényel
- **Kivonat** `PLAYER/ENDINGS.md` / Részlegesen hiányos:```
### Partial incomplete

Compliance documents operational response gaps — the alarm history, supervisor actions, and temperature readings are on file, but several record threads never made it into your statement. Without a completed synthesis, the write-off review proceeds on the operational facts alone, and the question of exactly who caused tonight's failure stays open past your shift.

<!-- unit:end-partial-wrong-culprit -->
```- **Kivonat** `PLAYER/ENDINGS.md` / Tökéletes:```
### Perfect

Your accountability statement matches independent badge, manifest, physical, and BMS records. Compliance accepts a full reconstruction timeline: Lori Okonkwo borrowed Dev's forgotten badge to enter cold storage, swapped pallet labels to hide the short-ship, and used his unattended maintenance session to issue the mute command that suspended CZ-1 staging. Northline closes the shift with the write-off avoided and a documented case for both personnel review and the carrier dispute.

<!-- unit:end-partial-incomplete -->
```### DF-B-TIME-PRESSURE (időnyomás)
- **Várható:** Az óra által vezérelt jelenetváltozások láthatók a PLAYER revisit prózában
- **Kivonat** `PLAYER/SCENES.md` / Archívum függőben:```
### Archive pending

**Scene transition**

A small sync-in-progress icon sits over half the query menu. Some badge fields are grayed out entirely — the batch upload has not finished yet, and no amount of clicking speeds it up.

**What do you do?**

- Continue this scene thread.
- Return to the location base section for this area.

<!-- unit:sc-control-approach -->
```- **Kivonat** `PLAYER/SCENES.md` / Dokk korlátozás aktív:```
### Dock restriction active

**Scene transition**

Tape now runs across two of the bay lanes, and Elena is enforcing it herself. Nonessential movement through the dock stops here until her review finishes.

**What do you do?**

- Continue this scene thread.
- Return to the location base section for this area.

<!-- unit:sc-security-unstaffed -->
```
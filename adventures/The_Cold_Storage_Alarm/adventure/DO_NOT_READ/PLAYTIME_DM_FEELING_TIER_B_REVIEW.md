# Tier B Review Material — AUTHOR ONLY

Human semantic review for playtime and DM feeling gates. Contains PLAYER excerpts.

## Playtime Tier B

### PT-B-PATH-MEDIAN
- **Expected:** Confirm median expected path matches intended 120-minute solo session
- **Resolved:** False

### PT-B-SCARCITY
- **Expected:** Confirm deadline pressure is felt before exhaustive exploration completes
- **Resolved:** False

## DM Feeling Tier B

### DF-B-AGENCY-NAV (player_agency)
- **Expected:** Navigation and object choices remain diegetic with no bare codes
- **Excerpt** `PLAYER/LOCATIONS.md` / Loading dock:

```
### Loading dock

**Location:** Loading dock | **Time cost:** 0 min

The loading dock is lit by sodium fixtures. Forklifts sit idle. Elena Morales watches the bay doors while staff move between the dock and the office wing. Cold rolls off the bay in waves whenever a door cycles, and the smell of diesel and refrigerant hangs in the air. Somewhere past 1:00 a.m., the building has settled into the strange quiet of a shift that has already gone wrong.

**What do you do?**

- Walk through the dock corridor to the cold storage hall.
- Head inside to the staff break room.
- Cut through the warehouse 
```

- **Excerpt** `PLAYER/OBJECTS.md` / Badge archive terminal:

```
### Badge archive terminal

**Time cost:** 2 min

The archive terminal's status field is the first thing you check before running any query. The badge archive terminal shows whether tonight's batch upload has finished. Whatever the sync status says, the query menu is still in front of you.

**What do you do?**

- Query cold storage inbound badge entries for tonight.
- Query control room door entries for tonight.
- Pull the contractor outbound dock scan record.
- Return to the security office.

<!-- unit:unit-badge-cold-entry -->
```

### DF-B-INFERENCE-QUALITY (inference_quality)
- **Expected:** Inference worksheets require multi-record synthesis without embedded answers
- **Excerpt** `PLAYER/INFERENCE.md` / Badge misattributed:

```
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
```

- **Excerpt** `PLAYER/INFERENCE.md` / Perfect reconstruction:

```
### Perfect reconstruction

**Question:** Can you connect fraud concealment, unauthorized access, and staging suspension into one supported timeline?

**Record types to consult:**
- Every record thread listed in the worksheets above
- The maintenance ticket and door-ajar alarm history (control room and security office)

Record the records you used. If synthesis fails, note which locations you will revisit.

**What do you do?**

- Mark synthesis complete if your answer is supported.
- Mark synthesis incomplete and follow a recovery prompt in the recovery file.
```

### DF-B-NPC-NEUTRALITY (conversation_agency)
- **Expected:** NPC dialogue preserves suspect neutrality and trust-gated tone shifts
- **Excerpt** `PLAYER/NPCS.md` / Marcus latch:

```
### Marcus latch

**Time cost:** varies by topic

Marcus stands by the security office's alarm panel, keys still hooked to his belt from rounds. He has already decided this conversation is about confirming he did his job correctly, and he answers like he is reading from a rounds log.

*Ask what you checked on the cold storage door during rounds.*

**Marcus Hale** says: "I checked the cold storage latch at 11:00 p.m. It looked engaged."

He taps the time into the air like it settles the matter.

**What do you do?**

- Return to your current location menu or continue the conversation.

<!-- unit
```

- **Excerpt** `PLAYER/NPCS.md` / Lori label:

```
### Lori label

**Time cost:** varies by topic

The label residue is the thing she cannot argue with. Whatever composure she was holding onto finally goes.

*Press about label residue found in aisle C.*

**Lori Okonkwo** says: "You found label residue. Receiving records and floor work in aisle C are connected. I did not expect the staging alarm to persist."

It is the closest she comes to sounding sorry.

**What do you do?**

- Return to your current location menu or continue the conversation.

<!-- unit:unit-elena-urgency -->
```

### DF-B-ENDING-OPACITY (ending_causality)
- **Expected:** Imperfect endings remain opaque; perfect ending requires full supported reconstruction
- **Excerpt** `PLAYER/ENDINGS.md` / Partial incomplete:

```
### Partial incomplete

Compliance documents operational response gaps — the alarm history, supervisor actions, and temperature readings are on file, but several record threads never made it into your statement. Without a completed synthesis, the write-off review proceeds on the operational facts alone, and the question of exactly who caused tonight's failure stays open past your shift.

<!-- unit:end-partial-wrong-culprit -->
```

- **Excerpt** `PLAYER/ENDINGS.md` / Perfect:

```
### Perfect

Your accountability statement matches independent badge, manifest, physical, and BMS records. Compliance accepts a full reconstruction timeline: Lori Okonkwo borrowed Dev's forgotten badge to enter cold storage, swapped pallet labels to hide the short-ship, and used his unattended maintenance session to issue the mute command that suspended CZ-1 staging. Northline closes the shift with the write-off avoided and a documented case for both personnel review and the carrier dispute.

<!-- unit:end-partial-incomplete -->
```

### DF-B-TIME-PRESSURE (time_pressure)
- **Expected:** Clock-driven scene changes are visible in PLAYER revisit prose
- **Excerpt** `PLAYER/SCENES.md` / Archive pending:

```
### Archive pending

**Scene transition**

A small sync-in-progress icon sits over half the query menu. Some badge fields are grayed out entirely — the batch upload has not finished yet, and no amount of clicking speeds it up.

**What do you do?**

- Continue this scene thread.
- Return to the location base section for this area.

<!-- unit:sc-control-approach -->
```

- **Excerpt** `PLAYER/SCENES.md` / Dock restriction active:

```
### Dock restriction active

**Scene transition**

Tape now runs across two of the bay lanes, and Elena is enforcing it herself. Nonessential movement through the dock stops here until her review finishes.

**What do you do?**

- Continue this scene thread.
- Return to the location base section for this area.

<!-- unit:sc-security-unstaffed -->
```


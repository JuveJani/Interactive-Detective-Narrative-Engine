# DO NOT READ: Pre-Logic Audit Resolution

## Purpose

This file records the categories resolved before detailed Adventure Logic. It deliberately avoids copying external review language and treats the canonical case documents as source of truth.

## Resolved now

### Physical state integrity

- Registered immutable item keys for badge clone, Elena tablet, purge log, spoof module, ledger, override token, footage, work order, and audit memo.
- Added explicit transit records for Dana's device stash, tablet lockup, override use at 18:52, and footage alteration branch.
- Enforced one-location-at-a-time state rule in `01` § 6 and `02`.

### NPC knowledge integrity

- Defined initial knowledge and disclosure stages for all eight NPCs.
- Registered seven `FACT_*` identifiers with ingestion templates.
- Prevented single-roll confessions; Dana and Vince require hard leverage.

### Timeline realism

- Standardized campus travel and action costs (`04`).
- Applied same movement rules to NPCs and players (`06`).
- Declared clock from 19:00 Saturday through `CLK_0030` Sunday deadline.

### Fair-play redundancy

- Four conclusion groups with four clues each (16 `ACTIVE` clues).
- Murder, fraud, credential, and culprit paths each have three or more independent routes (`07` § 6).
- Five skill checks each gate quality or speed, not sole access.

### Soft-lock prevention

- Alternate routes for SCADA export, finance access, badge proof, and maintenance device.
- Off-screen cleanup degrades evidence quality rather than erasing all proof (`EVT_801`, `EVT_802`).
- Dana flee (`EVT_803`) weakens custody ending, not truth discovery.

### Ending validation

- Accusations evidence-gated via `CON_*` thresholds and `EVT_410`.
- Wrong accusations receive target-specific rebuttals per suspect (`07` § 3).
- Murder proof, fraud exposure, credential proof, and custody scored independently (`01` § 9).

### Two-player operation

- Narrative roles replace player-facing P1/P2 labels; schema retains deprecated availability vars only.
- Three split windows with `EVT_150` and `EVT_300` regroup gates.
- Branch completion plus agreement drives regroup; shared `CLOCK` only (MBD-04).
- Participation audit summary in `08` § 9 points to `13` for authoritative tables.

## Deferred to playtesting

- exact node count distribution across ~34 EVT nodes;
- dialogue length and reading pace;
- whether campus travel costs feel too punishing;
- exact frequency of remote contact during splits;
- final balance between external preservation and Dana apprehension;
- participation audit metric completion when `13` is authored.

## Gate to Alpha 0.2b

Detailed investigation nodes may now be created because:

- all entities have stable keys (`00`);
- state variables exist (`01`);
- item matrix and time costs are defined (`02`, `04`);
- NPC information paths are traceable (`03`);
- backbone arcs and off-screen events are declared (`05`, `06`);
- soft-lock routes and accusation requirements are explicit (`07`, `08`).

Remaining logic-layer files (`10`–`17`, `13`, `14`) may proceed against this foundation.

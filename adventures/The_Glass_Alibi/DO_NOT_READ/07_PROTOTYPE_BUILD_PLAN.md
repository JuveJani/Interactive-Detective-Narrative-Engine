# DO NOT READ: Prototype Build Plan

## Completed in Alpha 0.1

- authoritative case solution in `00_CASE_OVERVIEW.md`;
- immutable world facts in `01_WORLD_BIBLE.md`;
- full background timeline in `02_MASTER_TIMELINE.md`;
- eight-character database (victim, five suspects, two supporting NPCs, off-screen counsel contact);
- seven-location database across campus zones;
- non-authoritative clue architecture pointer in `05_CLUE_ARCHITECTURE.md`;
- five-ending narrative framework in `06_ENDING_FRAMEWORK.md`;
- prototype brief alignment in `PROTOTYPE_BRIEF.md`.

## Required before player-book compilation

### Alpha 0.2: Adventure logic

Create under `DO_NOT_READ/LOGIC/`:

- `00_ENTITY_KEY_TABLE.md` — stable IDs for locations, NPCs, clues, conclusions, endings;
- `01_WORLD_STATE_VARIABLES.md` — trust, exposure tiers, report lock, Dana movement state;
- `02_ITEM_STATE_MATRIX.md` — workbook, exports, fob, spoof residue, body release;
- `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` — interview gates and lie breakpoints;
- `04_TIME_COST_MATRIX.md` — movement and action costs on Saturday night clock;
- `05_CORE_EVENT_GRAPH.md` — fixed murder window and institutional deadlines;
- `06_NPC_SCHEDULE_AND_PRIORITY.md` — Sable, Kevin, Dana off-screen movement;
- `07_EVIDENCE_VALIDATION.md` — proof classes and conclusion thresholds (**authoritative for clues**);
- `08_TWO_PLAYER_CORE_RULES.md` — split/regroup, participation audit, role emphasis;
- `10_INVESTIGATION_NODE_GRAPH.md` — playable nodes and terminal dispatch;
- `11_LOCATION_STATE_MACHINE.md` — access gates per location;
- `12_CLUE_DEPENDENCY_GRAPH.md` — clue redundancy and soft-lock edges (**authoritative for clue graph**);
- `13_SPLIT_AND_REGROUP_FLOW.md` — three split windows per prototype brief;
- `14_ENDING_TRIGGER_MATRIX.md` — maps evidence to five endings;
- `16_EVENT_GRAPH_MAPPING.md` — timeline to node binding;
- `17_CHECK_REGISTER.md` — five `CHK_*` skill checks for alpha.

Validation target: IDNE Milestone B gates V1–V11, V-CHK, V-SM, V-ST, participation audit, C6 (`two_player`).

### Alpha 0.3: Narrative compiler pass

Create under `PLAYER/narrative/`:

- shared opening at LOC_START (19:00);
- Investigator A private scenes (server room, bay controller terminals);
- Investigator B private scenes (Test Bay 3 physical scene, loading dock, maint tunnel);
- synchronized regroup nodes after each split window;
- interview prose keyed to disclosure gates;
- final accusation and report-lock sequence before 00:30.

### Alpha 0.4: Playable package

Create under `PLAYER/`:

- spoiler-free readme;
- quick rules reference;
- two player books with role emphasis notes;
- shared case file and campus map;
- printable notes and time tracker;
- facilitator-free setup;
- playtest questionnaire.

## Scope controls (The Glass Alibi)

The two-hour prototype should use approximately:

| Target | Planned |
|---|---:|
| Investigators | 2 |
| Major suspects | 5 |
| Primary locations | 7 (6 investigative zones + security hub) |
| Meaningful clues (`ACTIVE`) | 16 |
| Split windows | 3 |
| Terminal outcomes | 5 |
| Skill checks (`CHK_*`) | 5 |

Additional constraints:

- no supernatural routes or clues;
- no P1/P2 binding in design docs—role emphasis only;
- OCD trait for Investigator B appears as environmental detail, not mechanical bonus;
- red herrings must remain good-faith secrets (Marcus override, Priya rivalry, Tom tunnel access, Vince blind spots);
- Dana must remain plausible as cooperative liaison until Chain A or Chain D breaks.

Do not add new principal conspirators unless playtesting reveals a specific need.

## Content dependency order

1. `00`–`07` design foundation (**this alpha**)
2. `LOGIC/00`–`17` implementation layer
3. `ADVENTURE_DESIGN_PACKAGE_VALIDATION.md` gate review
4. `PLAYER/narrative/` authored records
5. compiled player books

## First internal review questions

1. Is the accident narrative fairly breakable without one mandatory clue?
2. Can players prove manual override through at least two independent classes?
3. Is Marcus suspicious without becoming the obvious default killer?
4. Does Tom Reyes read as suspicious before dock evidence clears him?
5. Can Dana's vendor-call alibi be broken by combining badge, witness, and call metadata?
6. Can players expose fraud without murder proof (partial ending) and murder without full fraud exposure?
7. Does each investigator role have unique useful access in split scenes?
8. Can the final act complete before 00:30 without one player becoming a spectator?
9. Do failed rolls create time cost or institutional friction rather than hard dead ends?
10. Is every ending in `06_ENDING_FRAMEWORK.md` reachable from at least two evidence paths?

## Alpha checklist (this adventure)

### Design foundation

- [x] `00_CASE_OVERVIEW.md`
- [x] `01_WORLD_BIBLE.md`
- [x] `02_MASTER_TIMELINE.md`
- [x] `03_CHARACTER_DATABASE.md`
- [x] `04_LOCATION_DATABASE.md`
- [x] `05_CLUE_ARCHITECTURE.md`
- [x] `06_ENDING_FRAMEWORK.md`
- [x] `07_PROTOTYPE_BUILD_PLAN.md`

### Logic layer (Alpha 0.2)

- [x] `LOGIC/00_ENTITY_KEY_TABLE.md`
- [x] `LOGIC/07_EVIDENCE_VALIDATION.md`
- [x] `LOGIC/12_CLUE_DEPENDENCY_GRAPH.md`
- [x] `LOGIC/14_ENDING_TRIGGER_MATRIX.md`
- [x] remaining logic documents per Milestone B
- [x] `ADVENTURE_DESIGN_PACKAGE_VALIDATION.md`

### Narrative layer (later)

- [ ] shared opening and split scenes
- [ ] NPC interview records
- [ ] terminal ending dispatch prose
- [ ] player books and case file

## Playtest success criteria

- median playtime 90–150 minutes;
- at least one playtest reaches END_JUSTICE without facilitator hints;
- at least one playtest reaches END_WRONG_ACCUSATION or END_ACCIDENT_VERDICT from plausible partial reasoning;
- participation audit shows both investigators materially contribute in split windows;
- no soft-lock observed where all murder-proof routes vanish after a single failed check.

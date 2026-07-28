# DO NOT READ: Split and Regroup Flow

## 1. Design objective

The two-player structure must create asymmetric discovery without forcing either player to wait for a clue held privately by the other during a live split scene.

## 2. Split One: opening investigation

### Player 1 branch

Primary locations:

- Elias apartment;
- Mina;
- rear service route;
- neighbour.

Primary outputs:

- staging evidence;
- first procedural suspicion;
- physical timeline.

### Player 2 branch

Primary locations:

- newsroom;
- Nadia;
- Marcus;
- archive/server material.

Primary outputs:

- harbor direction;
- disappearance-plan suspicion;
- upload and photograph context.

### Independence test

Player 1 can complete all apartment tasks without Player 2's information.

Player 2 can complete all newsroom tasks without Player 1's information.

Neither branch contains a code, lock, or immediate decision requiring the other branch.

### Regroup trigger

After both players have completed all legal actions in their split branches **or** when the shared world clock reaches approximately 21:30.

### Split completion (MBD-03)

During Split One, each player continues until they have no remaining legal actions. When finished, they wait. No forced movement, automatic jump, timer interruption, or pressure on the other player applies.

### Synchronization window (Split One)

| Field | Value |
|---|---|
| Start | `EVT_100_SHARED_BRIEFING` complete (~20:10) |
| Regroup target | `EVT_150_REGROUP_ONE` |
| Regroup availability | 21:20–21:40 (`08` § 5) |
| World-clock trigger | approximately 21:30 if branches still open |
| Wait behaviour | finished player waits (`WAIT_UNTIL_SYNC` at window level) |

---

## 3. Regroup One

Players may share:

- all clues they choose;
- suspicions;
- trust impressions;
- next destination.

The game records transferred clue IDs in `SHARED_KNOWLEDGE_SET`.

### Joint deduction opportunities

- staging;
- harbor direction;
- Nadia's withheld role;
- early police inconsistency.

### Choice architecture

Players choose separate midgame tracks based on complementary objectives, not arbitrary “left door/right door” branching.

---

## 4. Split Two: midgame specialization

Recommended combinations:

### Pair A

- Player 1: Mina/police procedure.
- Player 2: harbor archive/café research.

### Pair B

- Player 1: Iris medical trail.
- Player 2: Marcus/newsroom investigation.

### Pair C

- Player 1: terminal exterior reconnaissance.
- Player 2: Reed office/digital operational link.

### Local completeness rule

Each track provides:

- at least one meaningful clue;
- at least one decision;
- at least one consequence;
- an exit route back to regroup.

No track's core task depends on a code or instruction known only to the other player.

---

## 5. Legal communication during split

### Phone call

- costs 5 minutes;
- transfers one clue or one decision;
- not available inside Signal Room 4B;
- may be intercepted or raise awareness only when explicitly stated.

### Text message

- transfers one clue;
- delivery may occur at node completion;
- unsuitable for real-time coordinated puzzles.

### Emergency broadcast

- one-way;
- immediate;
- increases public or antagonist awareness.

The player books must never assume unrestricted table conversation during a declared isolated scene.

---

## 6. Regroup Two

Recommended deadline: 23:15.

### Synchronization window (Split Two)

| Field | Value |
|---|---|
| Start | `EVT_150_REGROUP_ONE` track assignment complete |
| Regroup target | `EVT_300_REGROUP_TWO` |
| Deadline | 23:15 |
| Wait behaviour | finished player waits (`WAIT_UNTIL_SYNC` at window level) |

### Mandatory planning outputs

The team assigns responsibility for:

- terminal entry;
- rescue arrangement;
- evidence handling;
- external communication.

### Required knowledge check

The game confirms whether players have:

1. a terminal route;
2. a room-identification route;
3. a rescue-control option;
4. a plan for evidence preservation.

Missing elements do not halt play. Instead, the node offers costly late failsafes.

---

## 7. Final-act split

Possible role pairs:

### Rescue / Evidence

- Player A secures Elias and coordinates evacuation.
- Player B completes key/code/upload sequence.

### Interior / Exterior

- Player A negotiates with Lena and Iris.
- Player B blocks or redirects Reed/Rook.

### Proof / Protection

- Player A preserves authenticated evidence.
- Player B secures a trusted medical route.

### Parity requirement

Each role must include:

- at least two decisions;
- one state-changing action;
- one meaningful risk;
- one route to partial success.

Neither role may reduce to “wait until the other player finishes reading.”

---

## 8. Conflict handling

If players disagree after regroup:

- each selects an actual action;
- the world resolves both if physically compatible;
- incompatible actions create a specific branch;
- no random tie-breaker replaces player agency.

Example categories, without final prose:

- rescue immediately vs copy evidence first;
- trust Mina vs remain fully covert;
- negotiate Reed vs evade him;
- official transfer vs public leak.

---

## 9. Participation audit fields (MBD-05)

**Audience:** developers only. Players never see this audit.

**Scope:** evaluate **all valid story paths** (see tables below). Do not privilege Pair A or any single canonical route. The audit is informational; it does not modify gameplay.

**Imbalance rule:** flag when any metric differs by more than 2× between roles on the same path, or when one role has zero decisions in a block.

### Opening / Split One — role comparison

| Metric | Apartment role | Newsroom role |
|---|---|---|
| Decision nodes (max) | 5 (`EVT_111`–`EVT_115`) | 3 (`EVT_121`–`EVT_123`) |
| Unique clues (max) | 4 | 5 |
| Locations | `LOC_ELIAS_APT`, service route | `LOC_NEWSROOM` |
| Social challenges | 1 (`EVT_111` approach) | 1 (`EVT_121` approach) |
| Physical challenges | 1 (`CHK_115_PERCEPTION`, DC 10) | 0 |
| Technical challenges | 0 | 0 |
| Gameplay time (min, typical max path) | 55–80 | 45–65 |
| Communication opportunities | phone (5 min), message per `§ 5` | phone (5 min), message per `§ 5` |

### Midgame / Split Two — three valid path pairs

| Metric | Pair A (police / harbor) | Pair B (medical / Marcus) | Pair C (recon / Reed) |
|---|---|---|---|
| Role A track nodes | `EVT_220`–`EVT_223` | `EVT_230`–`EVT_232` | `EVT_212` |
| Role B track nodes | `EVT_210`–`EVT_211` | `EVT_240`–`EVT_241` | `EVT_242`–`EVT_243` |
| Role A decisions (max) | 4 | 3 | 1 |
| Role B decisions (max) | 2 | 2 | 2 |
| Role A clues (max) | 4 | 3 | 2 |
| Role B clues (max) | 3 | 3 | 3 |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | phone, message per `§ 5` |

### Final act — three valid role-pair patterns (`§ 7`)

| Pattern | Role A nodes | Role B nodes | Role A decisions | Role B decisions |
|---|---|---|---|---|
| Rescue / Evidence | `EVT_400` | `EVT_410` | 2+ | 2+ |
| Interior / Exterior | `EVT_331` | `EVT_420` | 2+ | 2+ |
| Proof / Protection | `EVT_430` | `EVT_400` | 2+ | 2+ |

All patterns satisfy `§ 7` parity requirement (≥2 decisions, ≥1 state-changing action, ≥1 risk per role).

### Regroup blocks

| Block | Joint decisions | Clue transfer | Communication |
|---|---|---|---|
| Regroup One (`EVT_150`) | 1 (track assignment) | all chosen clues | all modes legal (`08` § 4) |
| Regroup Two (`EVT_300`) | 1 (final-act assignment) | all chosen clues | all modes legal (`08` § 4) |

**Audit status:** All blocks populated for declared `two_player` paths. No systematic imbalance flagged.

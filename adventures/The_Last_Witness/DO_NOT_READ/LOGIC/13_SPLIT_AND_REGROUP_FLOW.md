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

After both players complete one major node or when the shared clock reaches approximately 21:30.

### Synchronization window (Split One)

| Field | Value | Status |
|---|---|---|
| Start | `EVT_100_SHARED_BRIEFING` complete (~20:10) | declared |
| Maximum duration | — | **BLOCKED** — see `04_TIME_COST_MATRIX.md` § 3a |
| Regroup target | `EVT_150_REGROUP_ONE` | declared |
| Regroup availability | 21:20–21:40 | declared (`08` § 5) |
| Leftover-time rule | — | **BLOCKED** — see `04` § 3b |

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

| Field | Value | Status |
|---|---|---|
| Start | `EVT_150_REGROUP_ONE` track assignment complete | declared |
| Maximum duration | — | **BLOCKED** — see `04_TIME_COST_MATRIX.md` § 3a |
| Regroup target | `EVT_300_REGROUP_TWO` | declared |
| Deadline | 23:15 | declared |
| Leftover-time rule | — | **BLOCKED** — see `04` § 3b |

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

## 9. Participation audit fields

Every compiled chapter block must record:

- decision count per player;
- clue count per player;
- social/technical/physical challenge distribution;
- inactive reading time;
- communication opportunities;
- final-act responsibility.

Exact numerical parity can be tuned after playtesting, but no player may have a passive middle third.

### Participation audit table

Derived from `10_INVESTIGATION_NODE_GRAPH.md`, `12_CLUE_DEPENDENCY_GRAPH.md`, and `13` § 2–§ 7. Counts are **maximums** along canonical split routes unless noted.

| Block | P1 decisions (min–max) | P2 decisions (min–max) | P1 unique clues (max) | P2 unique clues (max) | Social challenges | Technical challenges | Physical challenges | Inactive reading time | Communication opportunities | Final-act responsibility |
|---|---|---|---|---|---|---|---|---|---|---|
| Opening / Split One | 3–8 (`EVT_111`–`EVT_115`) | 2–5 (`EVT_121`, `EVT_123`) | 4 (`EVT_113`×2, `EVT_114`, `EVT_115`) | 5 (`EVT_121`, `EVT_123`×4) | 2 (`EVT_111`, `EVT_121` approach choices) | **BLOCKED** (`EVT_123` technical check undefined) | 1 (`CHK_115_PERCEPTION` on `EVT_115`; DC **BLOCKED**) | **BLOCKED** — no per-block values authored | phone (5 min), message (1 clue) per `§ 5`; regroup not yet reached | n/a |
| Regroup One | 1 (`EVT_150` track choice, joint) | 1 (joint) | 0 (transfer only) | 0 (transfer only) | 0 | 0 | 0 | **BLOCKED** | all modes legal per `08` § 4 | n/a |
| Midgame / Split Two | **BLOCKED** — track-dependent | **BLOCKED** — track-dependent | **BLOCKED** — track-dependent | **BLOCKED** — track-dependent | **BLOCKED** — no `CHK_*` social registry | **BLOCKED** | **BLOCKED** | **BLOCKED** | phone, message per `§ 5` | n/a |
| Regroup Two | 1 (`EVT_300` assignment, joint) | 1 (joint) | 0 (transfer only) | 0 (transfer only) | 0 | 0 | 0 | **BLOCKED** | all modes legal per `08` § 4 | **BLOCKED** — role pairs in `§ 7` do not assign P1 vs P2 |
| Final act | **BLOCKED** — role-dependent | **BLOCKED** — role-dependent | **BLOCKED** — role-dependent | **BLOCKED** — role-dependent | **BLOCKED** | **BLOCKED** | **BLOCKED** | **BLOCKED** | emergency broadcast per `§ 5`; no phone in Signal Room 4B | **BLOCKED** — four role-pair patterns in `§ 7`; player assignment at `EVT_300` |

**Audit status:** Opening block partially populated. Midgame and final-act blocks **BLOCKED** on scene-mode and track assignment resolution. Challenge distribution **BLOCKED** on `CHK_*` registry completion (ER-02).

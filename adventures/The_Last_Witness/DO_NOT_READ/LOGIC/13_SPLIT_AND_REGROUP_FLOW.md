# DO NOT READ: Split and Regroup Flow

## 1. Design objective

The two-player structure must create asymmetric discovery without forcing either player to wait for a clue held privately by the other during a live split scene.

## 2. Split One: opening investigation

### Apartment-cluster branch

Primary locations:

- Elias apartment;
- Mina;
- rear service route;
- neighbour.

Primary outputs:

- staging evidence;
- first procedural suspicion;
- physical timeline.

### Newsroom-cluster branch

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

The occupant of the apartment-cluster role can complete all apartment tasks without the newsroom-cluster role's information.

The occupant of the newsroom-cluster role can complete all newsroom tasks without the apartment-cluster role's information.

Neither branch contains a code, lock, or immediate decision requiring the other branch.

### Regroup trigger

Regroup One (`EVT_150`) requires **both** split branches to be complete (no remaining legal actions per role) **and** both players agreeing to regroup. The shared world clock may make regroup **available** at approximately 21:30 (`04` § 3a) but does not force branch exit or interrupt play (MBD-03).

### Split completion (MBD-03)

During Split One, each player continues until they have no remaining legal actions. When finished, they wait. No forced movement, automatic jump, timer interruption, or pressure on the other player applies.

### Synchronization window (Split One)

| Field | Value |
|---|---|
| Start | `EVT_100_SHARED_BRIEFING` complete (~20:10) |
| Regroup target | `EVT_150_REGROUP_ONE` |
| Regroup availability | 21:20–21:40 (`08` § 5) |
| World-clock trigger | approximately 21:30 makes regroup **available** (optional) |
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

### Pair A — police-procedure / harbor-research

- **Police-procedure role:** Mina/police procedure (`EVT_220`–`EVT_223`).
- **Harbor-research role:** harbor archive/café research (`EVT_210`–`EVT_211`).

### Pair B — medical-trail / newsroom-investigation

- **Medical-trail role:** Iris medical trail (`EVT_230`–`EVT_232`).
- **Newsroom-investigation role:** Marcus/newsroom investigation (`EVT_240`–`EVT_241`).

### Pair C — terminal-recon / Reed-office

- **Terminal-recon role:** terminal exterior reconnaissance (`EVT_212`).
- **Reed-office role:** Reed office/digital operational link (`EVT_242`–`EVT_243`).

### Local completeness rule

Each track provides:

- at least one meaningful clue;
- at least one decision;
- at least one consequence;
- an exit route back to regroup.

No track's core task depends on a code or instruction known only to the other player.

---

## 5. Legal communication during split

Window-level `REMOTE_CONTACT` (this section) and `EMERGENCY_INTERRUPT` (`08` § 4) are not per-node metadata.

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

Recommended deadline: 23:15. Regroup Two (`EVT_300`) requires both split branches complete and player agreement; the deadline makes regroup **available** but does not force branch exit (MBD-03).

### Synchronization window (Split Two)

| Field | Value |
|---|---|
| Start | `EVT_150_REGROUP_ONE` track assignment complete |
| Regroup target | `EVT_300_REGROUP_TWO` |
| Deadline | 23:15 (makes regroup **available**) |
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

- Role A secures Elias and coordinates evacuation.
- Role B completes key/code/upload sequence.

### Interior / Exterior

- Role A negotiates with Lena and Iris.
- Role B blocks or redirects Reed/Rook.

### Proof / Protection

- Role A preserves authenticated evidence.
- Role B secures a trusted medical route.

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

**Imbalance rule:** flag when any metric differs by **more than** 2× between roles on the same path, or when one role has zero decisions in a block. Flags are for **manual author review only**; the audit does not auto-correct gameplay.

### Opening / Split One — role comparison

| Metric | Apartment role | Newsroom role | Imbalance flag |
|---|---|---|---|
| Decision nodes (max) | 5 (`EVT_111`–`EVT_115`) | 3 (`EVT_121`–`EVT_123`) | no |
| Unique clues (max) | 4 | 5 | no |
| Locations | `LOC_ELIAS_APT`, service route | `LOC_NEWSROOM` | — |
| Social challenges | 1 (`EVT_111` approach) | 1 (`EVT_121` approach) | no |
| Physical challenges | 1 (`CHK_115_PERCEPTION`, DC 10) | 0 | **review** — one role has zero physical `CHK_*` |
| Technical challenges | 0 | 0 | no |
| Gameplay time (min, typical max path) | 55–80 | 45–65 | no |
| Communication opportunities | phone (5 min), message per `§ 5` | phone (5 min), message per `§ 5` | no |
| Overall participation | high decision density | high clue density | no |

### Midgame / Split Two — Pair A (police / harbor)

| Metric | Police-procedure role | Harbor-research role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_220`–`EVT_223` | `EVT_210`–`EVT_211` | — |
| Decisions (max) | 4 | 2 | no (2× exactly) |
| Unique clues (max) | 4 | 3 | no |
| Locations | `LOC_POLICE_ANNEX` | `LOC_HARBOR_ARCHIVE`, `LOC_CAFE_ORPHEUS` | — |
| Challenges | social (`EVT_223`); no `CHK_*` | social (archive gate); no `CHK_*` | no |
| Gameplay time (min) | 70–95 | 45–65 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | procedure-heavy | research-heavy | no |

### Midgame / Split Two — Pair B (medical / Marcus)

| Metric | Medical-trail role | Newsroom-investigation role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_230`–`EVT_232` | `EVT_240`–`EVT_241` | — |
| Decisions (max) | 3 | 2 | no |
| Unique clues (max) | 3 | 3 | no |
| Locations | `LOC_IRIS_WORK` | `LOC_NEWSROOM` | — |
| Challenges | social/medical interpretation | social (`EVT_240` pressure) | no |
| Gameplay time (min) | 50–70 | 40–55 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | balanced | balanced | no |

### Midgame / Split Two — Pair C (recon / Reed)

| Metric | Terminal-recon role | Reed-office role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_212` | `EVT_242`–`EVT_243` | — |
| Decisions (max) | 1 | 2 | no |
| Unique clues (max) | 2 | 3 | no |
| Locations | `LOC_TERMINAL_EXT` | `LOC_REED_OFFICE` | — |
| Challenges | reconnaissance choices | social/negotiation (`EVT_243`) | no |
| Gameplay time (min) | 25–40 | 45–60 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | lighter decision load | heavier decision load | **review** — recon role low decision count |

### Final act — Rescue / Evidence

| Metric | Rescue-control role (`EVT_400`) | Evidence-recovery role (`EVT_410`) | Imbalance flag |
|---|---|---|---|
| Decisions (min) | 2+ | 2+ | no |
| Clues (typical) | rescue state, Elias condition | ledger, transfer prep | no |
| Locations | `LOC_SIGNAL_4B` | `LOC_SIGNAL_4B` | — |
| Challenges | state-changing rescue actions | evidence preservation | no |
| Gameplay time (min) | 30–50 | 25–45 | no |
| Communication | emergency broadcast only in-room | emergency broadcast only in-room | no |
| Overall participation | per `§ 7` parity | per `§ 7` parity | no |

### Final act — Interior / Exterior

| Metric | Negotiation role (`EVT_331`) | Confrontation role (`EVT_420`) | Imbalance flag |
|---|---|---|---|
| Decisions (min) | 2+ | 2+ | no |
| Clues (typical) | Lena/Iris trust | Reed/Rook exposure | no |
| Locations | `LOC_SIGNAL_4B` | `LOC_TERMINAL_EXT` | — |
| Challenges | social negotiation | confrontation | no |
| Gameplay time (min) | 25–40 | 25–40 | no |
| Communication | no phone in Signal Room 4B | phone per `§ 5` if exterior | no |
| Overall participation | per `§ 7` parity | per `§ 7` parity | no |

### Final act — Proof / Protection

| Metric | Transfer role (`EVT_430`) | Rescue route role (`EVT_400`) | Imbalance flag |
|---|---|---|---|
| Decisions (min) | 2+ | 2+ | no |
| Clues (typical) | transfer completion | rescue control | no |
| Locations | `LOC_SIGNAL_4B` / egress | `LOC_SIGNAL_4B` | — |
| Challenges | evidence transfer risk | medical rescue risk | no |
| Gameplay time (min) | 30–45 | 30–50 | no |
| Communication | emergency broadcast | emergency broadcast | no |
| Overall participation | per `§ 7` parity | per `§ 7` parity | no |

### Regroup blocks

| Block | Joint decisions | Clue transfer | Communication | Participation |
|---|---|---|---|---|
| Regroup One (`EVT_150`) | 1 (track assignment) | all chosen clues | all modes legal (`08` § 4) | joint only |
| Regroup Two (`EVT_300`) | 1 (final-act assignment) | all chosen clues | all modes legal (`08` § 4) | joint only |

### Imbalance summary (manual review queue)

| Path | Flag | Reason |
|---|---|---|
| Opening / Split One | **review** | apartment role has physical `CHK_*`; newsroom role has zero |
| Midgame Pair C | **review** | terminal-recon role lower decision count than Reed-office role |
| All other paths | none | within 2× rule; no zero-decision roles |

**Audit status:** All valid `two_player` paths populated across decisions, clues, locations, challenges, gameplay time, communication, and overall participation. Two items flagged for manual review only.

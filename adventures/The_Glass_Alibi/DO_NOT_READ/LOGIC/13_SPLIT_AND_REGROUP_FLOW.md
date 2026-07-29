# DO NOT READ: Split and Regroup Flow

## 1. Design objective

The two-player structure must create asymmetric discovery without forcing either player to wait for a clue held privately by the other during a live split scene.

Scene modes use **narrative roles**, not `P1`/`P2` labels in player-facing text. Schema keys `P1_*` / `P2_*` map to Role A / Role B for engine compatibility only.

---

## 2. Split One: opening investigation

### Tech / SCADA cluster (automation technician emphasis)

Primary locations:

- `LOC_SCADA_ROOM`;
- `LOC_TEST_BAY` (forensics path);
- Kevin Marsh (`NPC_KEVIN`).

Primary nodes: `EVT_110`, `EVT_111`, `EVT_112`, `EVT_113`, `EVT_115`, `EVT_123`.

Primary outputs:

- CO₂ anomaly and injury pattern;
- manual purge log and override auth;
- sensor spoof fragment;
- Elena tablet sync timestamps.

### Field / perimeter cluster (athletic investigator emphasis)

Primary locations:

- `LOC_SECURITY_DESK`;
- `LOC_MAINTENANCE_SHED` (orientation only — deep shed play in Split Two);
- loading dock and perimeter (`LOC_START` adjacency).

Primary nodes: `EVT_120`, `EVT_121`, `EVT_140`, `EVT_141`.

Primary outputs:

- after-hours access record;
- badge swipe mismatch;
- Dana desk-visit pattern;
- camera blind-spot context.

### Independence test

The occupant of the tech/SCADA role can complete all SCADA and test-bay tasks without the field role's information.

The occupant of the field role can complete all security-desk tasks without the tech role's information.

Neither branch contains a code, lock, or immediate decision requiring the other branch.

### Regroup trigger

Regroup One (`EVT_150`) requires **both** split branches complete (no remaining legal actions per role) **and** both players agreeing to regroup. The shared world clock may make regroup **available** at approximately 20:30 (`04` § 3a) but does not force branch exit (MBD-03).

### Split completion (MBD-03)

During Split One, each player continues until they have no remaining legal actions. When finished, they wait. No forced movement, automatic jump, timer interruption, or pressure on the other player applies.

### Synchronization window (Split One)

| Field | Value |
|---|---|
| Start | `EVT_100` briefing complete (~19:10) |
| Regroup target | `EVT_150` |
| Regroup availability | 20:20–20:40 (`08` § 5) |
| World-clock trigger | 20:30 makes regroup **available** (optional) |
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

- murder not accident if either branch reached `P_MURDER >= 2`;
- credential abuse if field branch opened;
- Dana as liaison of interest if two threads started.

### Choice architecture

Players choose Split Two tracks based on complementary objectives:

- **Finance track:** ledger, shell vendors, Dana approval bursts.
- **Ops / architect track:** Marcus hold order, Priya rivalry documents, vendor warning email.

Witness-preservation nodes (`EVT_220`, `EVT_240`) are reachable from either track assignment but do not require cross-track codes.

---

## 4. Split Two: midgame specialization

Recommended combinations:

### Pair A — finance track / ops track

- **Finance-track role:** `EVT_210`, `EVT_230`, `EVT_260`.
- **Ops-track role:** `EVT_250`, `EVT_270`, `EVT_271`.

### Pair B — finance track / architect-heavy ops

- **Finance-track role:** `EVT_210`, `EVT_260`.
- **Ops-track role:** `EVT_250`, `EVT_270`, `EVT_271`, `EVT_230` (Dana pressure deferred to Regroup Two planning).

### Pair C — credential maintenance / finance

- **Credential role:** `EVT_122` (forged work order, Tom interview).
- **Finance role:** `EVT_210`, `EVT_260`, `EVT_271`.

Pair C is valid when players prioritised field orientation in Split One and deferred maintenance shed depth.

### Local completeness rule

Each track provides:

- at least one meaningful clue;
- at least one decision;
- at least one consequence;
- an exit route toward `EVT_300`.

No track's core task depends on a code or instruction known only to the other player.

Optional witness nodes `EVT_220` and `EVT_240` may be taken by either role after their primary track exhausts legal actions.

---

## 5. Legal communication during split

Window-level `REMOTE_CONTACT` (this section) and `EMERGENCY_INTERRUPT` (`08` § 4) are not per-node metadata.

### Phone call

- costs 5 minutes;
- transfers one clue or one decision;
- not available inside RF-shielded test bay;
- may raise `A_CORPORATE` or `A_SECURITY` when explicitly stated.

### Text message

- transfers one clue;
- delivery may occur at node completion;
- unsuitable for real-time coordinated puzzles.

### Emergency broadcast

- one-way;
- immediate;
- may raise `A_CORPORATE`.

The player books must never assume unrestricted table conversation during a declared isolated scene.

---

## 6. Regroup Two

Recommended deadline: 22:45. Regroup Two (`EVT_300`) requires both split branches complete and player agreement; the deadline makes regroup **available** but does not force branch exit (MBD-03).

### Synchronization window (Split Two)

| Field | Value |
|---|---|
| Start | `EVT_150` track assignment complete |
| Regroup target | `EVT_300` |
| Deadline | 22:45 (makes regroup **available**) |
| Wait behaviour | finished player waits (`WAIT_UNTIL_SYNC` at window level) |

### Mandatory planning outputs

The team assigns responsibility for final-act parallel roles:

1. confront / trace Dana at finance or parking;
2. secure SCADA + security copies;
3. recover badge-clone device at maintenance shed;
4. preserve external evidence transmission.

Missing elements do not halt play. `EVT_300` offers costly late failsafes.

### Required knowledge check

The game confirms whether players have:

1. murder thread at conclusion threshold or within one clue;
2. fraud or credential thread open;
3. Dana suspicion with two supporting threads;
4. evidence preservation plan.

This is a planning checklist, not a D20 roll.

---

## 7. Final-act split (Split Three)

Possible role pairs after `EVT_300` assignment:

### Confront / Preserve

- Role A traces Dana at finance hub or parking (`EVT_330` confront variant).
- Role B preserves historian and footage (`EVT_220`, `EVT_330` preserve variant).

### Credential / Transmission

- Role A recovers clone device at maintenance shed (`EVT_312`).
- Role B coordinates Kevin export and external transmit (`EVT_220`).

### Interior documentation / Exterior relay

- Role A documents test-bay and tablet chain (`EVT_330` document variant).
- Role B files formal challenge and counsel relay (`EVT_330` challenge variant).

### Parity requirement

Each role must include:

- at least two decisions;
- one state-changing action;
- one meaningful risk;
- one route to partial success.

Neither role may reduce to "wait until the other player finishes reading."

Convergence targets: `EVT_410` (accusation) and/or `EVT_420` (preservation) before `EVT_900`.

---

## 8. Conflict handling

If players disagree after regroup:

- each selects an actual action;
- the world resolves both if physically compatible;
- incompatible actions create a specific branch;
- no random tie-breaker replaces player agency.

Example categories:

- accuse Dana immediately vs copy historian first;
- confront Tom vs trace Dana;
- file challenge vs secure clone device;
- trust Sable export vs remain covert.

---

## 9. Participation audit fields (MBD-05)

**Audience:** developers only. Players never see this audit.

**Scope:** evaluate **all valid story paths** (see tables below). Do not privilege Pair A or any single canonical route. The audit is informational; it does not modify gameplay.

**Imbalance rule:** flag when any metric differs by **more than** 2× between roles on the same path, or when one role has zero decisions in a block. Flags are for **manual author review only**.

### Opening / Split One — role comparison

| Metric | Tech/SCADA role | Field/perimeter role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_110`–`EVT_115`, `EVT_123` | `EVT_120`, `EVT_121`, `EVT_140`, `EVT_141` | — |
| Decision nodes (max) | 5 | 4 | no |
| Unique clues (max) | 5 | 4 | no |
| Locations | `LOC_SCADA_ROOM`, `LOC_TEST_BAY` | `LOC_SECURITY_DESK`, perimeter | — |
| Social challenges | 1 (`EVT_111` Kevin rapport) | 1 (`EVT_140` Sable rapport) | no |
| Physical challenges | 1 (`CHK_115_PERCEPTION`) | 0 | **review** — field role has no physical `CHK_*` in Split One |
| Technical challenges | 1 (`CHK_123_TECHNOLOGY`) | 0 | no |
| Gameplay time (min, typical max path) | 60–85 | 45–65 | no |
| Communication opportunities | phone (5 min), message per `§ 5` | phone (5 min), message per `§ 5` | no |
| Overall participation | high technical density | high procedural density | no |

### Midgame / Split Two — Pair A (finance / ops)

| Metric | Finance-track role | Ops/architect-track role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_210`, `EVT_230`, `EVT_260` | `EVT_250`, `EVT_270`, `EVT_271` | — |
| Decisions (max) | 4 | 3 | no |
| Unique clues (max) | 4 | 3 | no |
| Locations | `LOC_FINANCE_HUB` | `LOC_OPS_FLOOR`, `LOC_ARCHITECT_LAB` | — |
| Challenges | 1 (`CHK_210_INVESTIGATION`) | 0 | no |
| Gameplay time (min) | 55–80 | 50–70 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | fraud-heavy | motive/context-heavy | no |

### Midgame / Split Two — Pair B (finance-heavy / ops-heavy)

| Metric | Finance-track role | Ops-track role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_210`, `EVT_260` | `EVT_250`, `EVT_270`, `EVT_271`, `EVT_230` | — |
| Decisions (max) | 3 | 4 | no |
| Unique clues (max) | 3 | 4 | no |
| Locations | `LOC_FINANCE_HUB` | `LOC_OPS_FLOOR`, `LOC_ARCHITECT_LAB`, `LOC_FINANCE_HUB` (Dana) | — |
| Challenges | 1 (`CHK_210_INVESTIGATION`) | 0 | no |
| Gameplay time (min) | 45–65 | 60–85 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | balanced | balanced | no |

### Midgame / Split Two — Pair C (credential / finance)

| Metric | Credential role | Finance role | Imbalance flag |
|---|---|---|---|
| Track nodes | `EVT_122` | `EVT_210`, `EVT_260`, `EVT_271` | — |
| Decisions (max) | 2 | 3 | no |
| Unique clues (max) | 1 | 4 | no |
| Locations | `LOC_MAINTENANCE_SHED` | `LOC_FINANCE_HUB`, `LOC_ARCHITECT_LAB` | — |
| Challenges | 0 (athletics deferred to Split Three) | 1 (`CHK_210_INVESTIGATION`) | no |
| Gameplay time (min) | 25–40 | 55–75 | no |
| Communication | phone, message per `§ 5` | phone, message per `§ 5` | no |
| Overall participation | lighter clue load; sets up `EVT_312` | heavier clue load | **review** — credential role low clue count in Pair C |

### Final act — Confront / Preserve

| Metric | Confront role (`EVT_330` confront) | Preserve role (`EVT_220`) | Imbalance flag |
|---|---|---|---|
| Decisions (min) | 2 | 2 | no |
| State-changing actions | `A_DANA +1`; Dana pressure | `T_KEVIN +1`; export copy | no |
| Risk | Dana flee window | historian legal hold | no |
| Gameplay time (min) | 30–45 | 25–40 | no |
| Overall participation | balanced | balanced | no |

### Final act — Credential / Transmission

| Metric | Credential role (`EVT_312`) | Transmission role (`EVT_220`) | Imbalance flag |
|---|---|---|---|
| Decisions (min) | 2 | 2 | no |
| Challenges | 1 (`CHK_312_ATHLETICS`) | 0 | no |
| Unique clues (max) | 1 (`CLUE_BADGE_CLONE_DEVICE`) | 0 (confirms murder thread) | no |
| Gameplay time (min) | 30–45 | 25–40 | no |
| Overall participation | physical emphasis | systems emphasis | no |

### Final act — Documentation / Relay

| Metric | Documentation role | Relay role | Imbalance flag |
|---|---|---|---|
| Track variant | `EVT_330` document | `EVT_330` challenge + `EVT_420` | — |
| Decisions (min) | 2 | 2 | no |
| Gameplay time (min) | 25–35 | 30–45 | no |
| Overall participation | balanced | balanced | no |

### Audit summary

| Block | Status | Notes |
|---|---|---|
| Opening / Split One | **Complete** | Field role flagged: zero physical `CHK_*` in block |
| Regroup One | **Complete** | Joint only; clue transfer |
| Midgame / Split Two | **Complete** | Pair C credential clue load flagged |
| Regroup Two | **Complete** | Joint assignment |
| Final act | **Complete** | Three role-pair patterns compared |

When playtesting resolves flagged items, update flags here; the audit does not auto-correct gameplay.

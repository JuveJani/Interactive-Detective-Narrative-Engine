# DO NOT READ: Time Cost Matrix

## 1. Travel model

Greyhaven is compact but not magically folded like a cheap board game map. Transit costs include departure, route delay, and arrival setup.

### Standard travel costs

| From/to category | Vehicle/taxi | Public transport | Foot |
|---|---:|---:|---:|
| same district | 10 min | 15 min | 20 min |
| central to harbor | 25 min | 30 min | 45 min |
| police annex to harbor | 30 min | 40 min | 55 min |
| newsroom to apartment | 15 min | 20 min | 30 min |
| harbor archive to terminal | 10 min | 15 min | 20 min |
| terminal exterior to Signal 4B | 10-25 min | n/a | route-dependent |

Weather after 22:45 adds:

- +5 minutes to vehicle travel in harbor district;
- +10 minutes to foot travel;
- closes drainage entry at 23:30.

## 2. Investigation action costs

| Action | Base time |
|---|---:|
| rapid visual scan | 5 min |
| standard scene search | 15 min |
| deep forensic search | 25 min |
| short witness interview | 10 min |
| full structured interview | 20 min |
| digital metadata recovery | 20 min |
| difficult deleted-data recovery | 30 min |
| copy/preserve evidence | 10 min |
| transmit evidence externally | 15 min |
| persuade gatekeeper with leverage | 10 min |
| attempt risky alternate access | 10-20 min |
| regroup and exchange all notes | 10 min |
| remote call sharing one clue | 5 min, where signal exists |
| run the documented archive-recovery reset | 20 min, and the reset is logged |

## 3. Shared world clock (MBD-04)

The adventure uses **one shared world clock**. The world clock controls world state, NPC schedules, events, and deadlines (`01_WORLD_STATE_VARIABLES.md`; `06_NPC_SCHEDULE_AND_PRIORITY.md`).

During a split window, each player progresses through their assigned narrative role independently **while separated**. Temporary split durations do **not** create independent world timelines. When players regroup, play continues on the single shared world clock.

The engine does **not** maintain persistent per-player timelines and does **not** apply synchronization mathematics. Action costs advance the shared `CLOCK` when the adventure declares a time cost for a completed action.

`P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` are **deprecated** (`01_WORLD_STATE_VARIABLES.md` § 8). They are not written during play and are not used for routing or regroup. Regroup gates depend on split-branch completion and player agreement (`13_SPLIT_AND_REGROUP_FLOW.md` § 2, § 6).

### Split-window behaviour (MBD-03)

During Split, each player continues until they have no remaining legal actions. A finished player waits. Regroup gates (`EVT_150`, `EVT_300`) become available when both players have completed their split branches **or** when a declared world-clock threshold is reached (see § 3a).

### 3a. Synchronization windows

Each split window has a start condition, regroup target, and optional world-clock trigger. Maximum durations and leftover-time micro-rules are **not** simulated; pacing follows § 5 block targets.

| Window | Start condition | Regroup / sync target | World-clock trigger | Status |
|---|---|---|---|---|
| Split One (opening) | `EVT_100_SHARED_BRIEFING` complete (~20:10) | `EVT_150_REGROUP_ONE` | optional: clock approximately 21:30 makes regroup **available** if branches still open (`13` § 2) | declared |
| Split Two (midgame) | `EVT_150_REGROUP_ONE` track assignment complete | `EVT_300_REGROUP_TWO` | optional: deadline 23:15 makes regroup **available** (`13` § 6) | declared |
| Final-act parallel | `EVT_300_REGROUP_TWO` assignment complete | `EVT_440` / `EVT_900` convergence (`13` § 7) | role branches complete per assignment | declared |

**Declared timing (authoritative for prose and gates):**

- Regroup One availability window: 21:20–21:40 (`08_TWO_PLAYER_CORE_RULES.md` § 5; `EVT_150` **Recommended window**).
- Regroup scene cost: 10 minutes (`§ 2` "regroup and exchange all notes"; `EVT_150` / `EVT_300` **Cost**).
- Regroup Two deadline: no later than 23:15 (`13` § 6; `EVT_300` **Deadline**).

**Window-level mechanics** (not per-node metadata): `WAIT_UNTIL_SYNC` (finished player waits), `REMOTE_CONTACT` (phone/message per `08` § 4), `EMERGENCY_INTERRUPT` (emergency broadcast per `08` § 4).

## 4. Time-cost consistency rules

- NPCs use the same travel constraints as players unless they have a documented head start or special transport.
- No scene may assume instant communication inside Signal Room 4B.
- Police response time to terminal is at least 25 minutes after confirmed location, unless a unit is already nearby through a prior event.
- Ambulance arrival is 12-20 minutes after a trusted dispatch, plus terminal extraction time.
- Carrying Elias from Signal Room 4B to ambulance adds at least 10 minutes with a known route and 20 minutes through a hazardous route.

## 5. Pacing target

The two-hour real-world play session represents roughly six in-world hours. Player reading and discussion time is not identical to in-world action time. The books should present a limited menu of meaningful actions per block rather than simulate every minute.

Recommended four blocks:

1. `20:00-21:30`: establish staging and competing narratives.
2. `21:30-23:00`: identify harbor, betrayals, and compromised police.
3. `23:00-00:30`: locate terminal route and secure trusted rescue.
4. `00:30-02:00`: terminal confrontation, evacuation, transfer, accusation.

## 6. Anti-exploit rule

A location cannot be fully exhausted through repeated five-minute scans. Each location defines a limited set of action tiers. Repeating an exhausted action consumes time and yields no new critical clue.

# DO NOT READ: Time Cost Matrix

## 1. Travel model

Helix Meridian is a compact corporate campus. Transit costs include badge check, elevator wait, and escort delay where applicable.

### Standard travel costs

| From/to category | Cart / escort | Internal shuttle | Foot |
|---|---:|---:|---:|
| same building wing | 5 min | 8 min | 10 min |
| briefing to test bay | 8 min | 10 min | 12 min |
| test bay to SCADA | 10 min | 12 min | 15 min |
| any building to finance hub | 12 min | 15 min | 18 min |
| perimeter to maintenance shed | 10 min | n/a | 15 min |
| ops floor to architect lab | 8 min | 10 min | 12 min |

After `22:00` night skeleton crew:

- +3 minutes to escorted routes;
- unescorted finance and architect access may require badge challenge (+5 min).

## 2. Investigation action costs

| Action | Base time |
|---|---:|
| rapid visual scan | 5 min |
| standard scene search | 15 min |
| deep forensic search | 25 min |
| short witness interview | 10 min |
| full structured interview | 20 min |
| SCADA / digital metadata recovery | 20 min |
| difficult deleted-data recovery | 30 min |
| copy/preserve evidence | 10 min |
| transmit evidence externally | 15 min |
| persuade gatekeeper with leverage | 10 min |
| attempt risky alternate access | 10-20 min |
| regroup and exchange all notes | 10 min |
| remote call sharing one clue | 5 min, where campus comms allow |
| formal incident challenge filing | 20 min, logged |

## 3. Shared world clock (MBD-04)

The adventure uses **one shared world clock**. The world clock controls world state, NPC schedules, events, and deadlines (`01_WORLD_STATE_VARIABLES.md`; `06_NPC_SCHEDULE_AND_PRIORITY.md`).

During a split window, each player progresses through their assigned narrative role independently **while separated**. Temporary split durations do **not** create independent world timelines. When players regroup, play continues on the single shared world clock.

The engine does **not** maintain persistent per-player timelines and does **not** apply synchronization mathematics. Action costs advance the shared `CLOCK` when the adventure declares a time cost for a completed action.

`P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` are **deprecated** (`01_WORLD_STATE_VARIABLES.md` § 8). They are not written during play and are not used for routing or regroup. Regroup gates depend on split-branch completion and player agreement (`13_SPLIT_AND_REGROUP_FLOW.md` § 2, § 6).

### Split-window behaviour (MBD-03)

During Split, each player continues until they have no remaining legal actions. A finished player waits. Regroup gates (`EVT_150`, `EVT_300`) become available when both players have completed their split branches **or** when a declared world-clock threshold is reached (see § 3a).

### 3a. Synchronization windows

Three split windows. Each has a start condition, regroup target, and optional world-clock trigger.

| Window | Start condition | Regroup / sync target | World-clock trigger | Status |
|---|---|---|---|---|
| Split One (opening) | `EVT_100` briefing complete (~19:10) | `EVT_150` | optional: `20:30` makes regroup **available** if branches still open | declared |
| Split Two (midgame) | `EVT_150` track assignment complete | `EVT_300` | optional: `22:45` makes regroup **available** | declared |
| Split Three (final parallel) | `EVT_300` assignment complete | `EVT_410` / `EVT_900` convergence | role branches complete per assignment | declared |

**Declared timing (authoritative for prose and gates):**

- Regroup One availability window: 20:20–20:40 (`08_TWO_PLAYER_CORE_RULES.md` § 5; `EVT_150` **Recommended window**).
- Regroup scene cost: 10 minutes (`§ 2` "regroup and exchange all notes"; `EVT_150` / `EVT_300` **Cost**).
- Regroup Two deadline: no later than 22:45 (`13` § 6; `EVT_300` **Deadline**).
- Case deadline: `00:30` Sunday (`CLK_0030`).

**Window-level mechanics** (not per-node metadata): `WAIT_UNTIL_SYNC` (finished player waits), `REMOTE_CONTACT` (phone/message per `08` § 4), `EMERGENCY_INTERRUPT` (emergency broadcast per `08` § 4).

## 4. Time-cost consistency rules

- NPCs use the same travel constraints as players unless they have a documented head start or special transport.
- No scene may assume instant comms inside RF-shielded test bay without explicit relay.
- Corporate legal response to formal challenge is at least 20 minutes.
- Security backup to maintenance shed is 8-12 minutes after alarm.
- Dana off-campus exit requires 15 minutes from finance hub to parking garage plus gate delay.

## 5. Pacing target

The two-hour real-world play session represents roughly five and a half in-world hours (19:00–00:30). Player reading and discussion time is not identical to in-world action time. The books should present a limited menu of meaningful actions per block rather than simulate every minute.

Recommended four blocks:

1. `19:00-20:30`: establish scene, competing accident narrative, first split.
2. `20:30-22:00`: SCADA/finance/security trails; fraud and credential threads open.
3. `22:00-23:30`: suspect confrontation, Dana pressure, second regroup.
4. `23:30-00:30`: accusation, evidence preservation, terminal endings.

## 6. Anti-exploit rule

A location cannot be fully exhausted through repeated five-minute scans. Each location defines a limited set of action tiers. Repeating an exhausted action consumes time and yields no new critical clue.

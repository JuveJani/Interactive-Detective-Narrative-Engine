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

## 3. Parallel action model

When players split, each advances independently. Global clock advances to the earliest next event for the active player, but synchronization occurs before any shared node.

Example:

- Player 1 action ends 21:10.
- Player 2 action ends 21:25.
- Player 1 may take another action that ends no later than 21:25.
- A shared event cannot begin before both are available.

The compiler must avoid free extra turns created by one player's shorter action.

### 3a. Synchronization windows

Per `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4, each split window requires a start condition, maximum duration, and leftover-time rule.

| Window | Start condition | Maximum duration | Regroup / sync target | Leftover-time rule | Status |
|---|---|---|---|---|---|
| Split One (opening) | `EVT_100_SHARED_BRIEFING` complete (~20:10) | **BLOCKED** — no per-window maximum declared | `EVT_150_REGROUP_ONE`; trigger also `13` § 2 (~21:30) | **BLOCKED** — see § 3b | partial |
| Split Two (midgame) | `EVT_150_REGROUP_ONE` track assignment complete | **BLOCKED** — no per-window maximum declared | `EVT_300_REGROUP_TWO`; deadline `23:15` per `13` § 6 | **BLOCKED** — see § 3b | partial |
| Final-act parallel | `EVT_300_REGROUP_TWO` assignment complete | **BLOCKED** — no per-window maximum declared | `EVT_900_RESOLVE_ENDING` / `EVT_440` convergence per `13` § 7 | **BLOCKED** — see § 3b | partial |

**Declared timing (not maximum durations):**

- Regroup One availability window: 21:20–21:40 (`08_TWO_PLAYER_CORE_RULES.md` § 5; `EVT_150` **Recommended window**).
- Split One regroup trigger: both complete one major node **or** clock approximately 21:30 (`13_SPLIT_AND_REGROUP_FLOW.md` § 2).
- Regroup Two deadline: no later than 23:15 (`13` § 6; `EVT_300` **Deadline**).
- Regroup scene cost: 10 minutes (`§ 2` "regroup and exchange all notes"; `EVT_150` / `EVT_300` **Cost**).
- `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 9 prototype cap: 10–30 world minutes per window — **not mapped** to adventure windows.

### 3b. Leftover-time rule conflict

| Document | Rule |
|---|---|
| This document § 3 (example) | Shorter player may take another action ending no later than the slower player's end time |
| `engine/05_TWO_PLAYER_SYNCHRONIZATION.md` § 4 | Shorter action does not allow unlimited extra actions; remaining time resolved only through explicitly offered waiting, preparation, travel, or communication options |

**Status:** **BLOCKED.** A single authoritative leftover-time rule cannot be declared without choosing between these two specifications. Gate V8 remains **BLOCKED** until resolved.

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

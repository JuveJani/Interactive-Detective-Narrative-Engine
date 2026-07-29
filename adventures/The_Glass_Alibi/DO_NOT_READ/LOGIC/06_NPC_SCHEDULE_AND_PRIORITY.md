# DO NOT READ: NPC Schedule and Priority Matrix

## 1. Purpose

When players are absent, NPC actions still resolve. This file prevents impossible overlap, teleportation, and undefined off-screen conflict.

## 2. Priority principles

Priority is contextual, not a universal power score.

Resolution order:

1. prior physical control of location/item;
2. preparation and knowledge of route;
3. arrival time;
4. institutional authority;
5. willingness to escalate;
6. interruption by player-created safeguards or formal challenge.

## 3. Fixed schedules

### Sable

- 19:00 desk handoff from day shift;
- 19:00-20:30 processes incident log entries;
- 20:30 onward can export badge-camera subset if trust threshold met;
- after 22:00 limited to desk terminal; no bay entry;
- cannot leave desk unattended more than 10 minutes.

### Kevin

- 19:00-20:30 SCADA room primary;
- 20:30 historian rotation; may be recalled to ops floor;
- 21:00-22:30 available for export if not blocked by Marcus hold;
- after 22:30 legal hold may lock direct export;
- does not enter test bay without escort.

### Marcus

- 19:00 incident command at ops floor;
- 19:30 orders bay lockdown messaging;
- 20:30-21:30 enforces export hold if corporate unaware;
- 21:15 begins direct pressure if `A_CORPORATE >= 1`;
- 22:00 night skeleton briefing;
- cannot personally forge SCADA logs.

### Priya

- 19:00-21:00 architect lab;
- 21:00-22:00 may be called to ops for statement;
- 22:00 lab restricted unless players hold challenge filing;
- does not access finance hub without escort;
- remains on campus until 23:30.

### Vince

- 19:00-20:00 perimeter rounds;
- 20:00-21:00 attempts camera segment cleanup if `A_DANA >= 1`;
- 21:00-22:30 mobile between security office and maintenance;
- 22:30 may flee campus if fraud proof surfaced;
- minimum travel maintenance to finance: 12 minutes.

### Tom

- 19:00-20:30 maintenance shed;
- 20:30 tool crib alarm if unauthorized entry;
- 21:00-23:00 on-call elsewhere in campus unless summoned;
- cannot clone badges; lacks finance system access.

### Dana

- 19:00-19:20 visible at incident briefing edge;
- 19:20-20:30 finance hub and liaison calls;
- 20:30-22:00 coordinates narrative with Marcus;
- 22:00-23:30 parking-garage exit window if investigation lags;
- 23:30 report submission push;
- minimum travel finance hub to parking: 15 minutes.

## 4. Off-screen conflict outcomes

Each outcome is an off-screen event in `EVT_800-899`. Off-screen events are not player-reachable and are excluded from graph reachability.

| Identifier | Outcome |
|---|---|
| `EVT_801` | Dana attempts badge-clone device recovery at maintenance shed |
| `EVT_802` | Vince alters security footage segment |
| `EVT_803` | Dana exits campus before apprehension |
| `EVT_804` | Marcus submits uncontested accident report early |

### `EVT_801` Dana attempts device recovery

- Trigger: `A_DANA >= 2` and `ITEM_BADGE_CLONE` undiscovered past 21:30.
- Dana sends cutout; Tom may interrupt if players warned him.
- Success: device destroyed; credential route remains via auth logs and work order.
- Failure: device preserved; `A_DANA +1`.

### `EVT_802` Vince alters footage

- Trigger: `A_DANA >= 1`, players lack Sable Stage 2, clock past 20:30.
- Alters one badge-camera segment; unaltered copy still available via Kevin/Sable alternate export if trust earned before 22:00.
- Partial alteration never removes all credential proof.

### `EVT_803` Dana exits campus

- Trigger: `CON_CULPRIT_DANA` not met, clock past 22:45, no formal challenge.
- Dana reaches parking and leaves jurisdiction.
- Ending degrades to incomplete custody; fraud/murder proof may still succeed.

### `EVT_804` Marcus early report submission

- Trigger: `A_CORPORATE = 0`, no challenge filed, clock past 23:00.
- `REPORT_STATE` advances toward accident narrative early.
- Players may still overturn with preserved copies before `CLK_0030`.

## 5. Player interruption

Player presence overrides default outcome only if they arrive before the event's resolution time. Arriving after reveals consequences; routes remain legal with degraded quality.

## 6. Tie-breakers

When two NPC events target the same item:

- current holder acts first;
- prepared concealment beats unprepared search;
- external copy beats local deletion;
- if equal, earlier arrival wins;
- if simultaneous, create explicit confrontation event rather than silent resolution.

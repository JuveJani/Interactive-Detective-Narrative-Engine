# DO NOT READ: Item State Matrix

## Design rule

Every significant item movement requires a cause, actor, start time, end time, and destination. Discovery changes player knowledge, not physical location, unless the event explicitly moves or seizes the item.

## Badge clone device

### `ITEM_BADGE_CLONE`

| Time | State | Cause |
|---|---|---|
| before 18:40 | `HELD_BY(NPC_DANA)` | Dana used device off-campus |
| 18:40-19:05 | `CONCEALED_AT(LOC_MAINTENANCE_SHED)` | Dana stashed device in tool crib void |
| after discovery | held by players or seized by security depending branch | investigative outcome |

Players may find the device through maintenance search, badge-audit cross-reference, or Tom confrontation. Dana cannot recover it after `A_DANA >= 2` without triggering `EVT_801`.

## Elena's tablet

### `ITEM_ELENA_TABLET`

| Time | State | Cause |
|---|---|---|
| before 18:55 | `HELD_BY(NPC_ELENA)` | carried during bay test |
| 18:55-19:15 | `AT_LOCATION(LOC_TEST_BAY)` | dropped near console during incident |
| 19:15 onward | `AT_LOCATION(LOC_TEST_BAY)` in evidence lockup | campus security bags scene items |
| after `EVT_113` | `HELD_BY(players)` or `COPIED` digital state | lawful extraction or forensic imaging |

Tablet holds `ITEM_ELENA_AUDIT_MEMO` draft and sync timestamps linking to finance discrepancies. It cannot be wiped remotely after 19:30 historian snapshot.

## Purge controller log

### `ITEM_PURGE_LOG`

| Time | State | Cause |
|---|---|---|
| continuous | historian export on SCADA server | automatic logging |
| 19:00-20:30 | `AVAILABLE` digital at `LOC_SCADA_ROOM` | Kevin can export |
| after 20:30 | `LOCKED` unless Kevin trust +1 or corporate challenge | rotation + legal hold prep |
| after player export | `COPIED` | players preserve override sequence |

Log shows manual CO₂ purge override at 18:52 with auth token not matching maintenance schedule.

## Sensor spoof module

### `ITEM_SENSOR_SPOOF`

| Time | State | Cause |
|---|---|---|
| before 18:50 | installed in test-bay cable tray | Dana + Vince prep |
| 18:50-19:10 | active during incident | spoofed safe-readings |
| after 19:10 | `CONCEALED_AT(LOC_TEST_BAY)` partial module remains | damaged during purge |
| after `CHK_115_PERCEPTION` success or deep search | discoverable | players recover fragment |

## Finance ledger trail

### `ITEM_FINANCE_LEDGER`

| Time | State | Cause |
|---|---|---|
| ongoing | `AVAILABLE` digital at `LOC_FINANCE_HUB` | procurement system |
| after `CLK_2130` | `LOCKED` tier-2 unless audit challenge active | evening window closes |
| after export | `COPIED` or `TRANSMITTED` | player preservation choice |

Shows shell vendors, Dana approval bursts, and Elena-flagged anomalies.

## CO₂ override token

### `ITEM_CO2_OVERRIDE`

| Time | State | Cause |
|---|---|---|
| before 18:00 | `HELD_BY(NPC_TOM)` | legitimate maintainer custody |
| 18:00-18:45 | `IN_TRANSIT(NPC_DANA, LOC_FINANCE_HUB, LOC_TEST_BAY)` | cloned auth used via badge clone |
| 18:52 | used in manual purge | override recorded in `ITEM_PURGE_LOG` |
| after incident | `AT_LOCATION(LOC_TEST_BAY)` console housing | embedded auth chip |

Tom believes he still has the fob; physical mismatch is a credential-abuse clue.

## Security footage

### `ITEM_SECURITY_FOOTAGE`

Initial digital state: `AVAILABLE` with rolling retention.

Transitions:

- `20:30`: partial segment `ALTERED` if Dana cleanup succeeds off-screen (`EVT_802`);
- players with Sable trust +1: `COPIED` unaltered badge-camera subset;
- after `A_SECURITY = 2`: direct server access `LOCKED`; desk terminal copy remains alternate route.

## Maintenance work order

### `ITEM_MAINT_WORKORDER`

| Time | State | Cause |
|---|---|---|
| before 17:00 | forged digitally by Dana | falsified bay access justification |
| 17:00-19:00 | `AT_LOCATION(LOC_MAINTENANCE_SHED)` | posted for night crew |
| after comparison | forgery evident vs Tom's actual schedule | investigation outcome |

## Dana badge record

### `ITEM_DANA_BADGE_RECORD`

| Time | State | Cause |
|---|---|---|
| continuous | `AVAILABLE` at `LOC_SECURITY_DESK` | access control system |
| after clone use | shows impossible swipe overlap | automatic audit flag suppressed by Vince contract gap unless players restore |

## Elena audit memo

### `ITEM_ELENA_AUDIT_MEMO`

| Time | State | Cause |
|---|---|---|
| before death | on tablet and queued to finance secure mail | Elena prepared disclosure |
| after death | `LOCKED` in mail queue until finance or tablet access | corporate delay |
| after unlock | `COPIED` or `TRANSMITTED` | player preservation |

## Evidence preservation rule

When players acquire digital proof, they must choose one of:

- keep only on source system, fast but vulnerable;
- make local copy, moderate time;
- transmit to trusted external recipient (legal counsel, journalist endpoint), slower but durable.

This choice affects later seizure without erasing player achievement arbitrarily.

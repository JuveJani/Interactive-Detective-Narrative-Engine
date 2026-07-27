# DO NOT READ: Item State Matrix

## Design rule

Every significant item movement requires a cause, actor, start time, end time, and destination. Discovery changes player knowledge, not physical location, unless the event explicitly moves or seizes the item.

## Primary ledger

### `ITEM_LEDGER_PRIMARY`

| Time | State | Cause |
|---|---|---|
| before 18:57 | `HELD_BY(NPC_ELIAS)` | Elias carries it from apartment |
| 18:57-19:25 | `HELD_BY(NPC_ELIAS)` | enters terminal and retains it |
| 19:25-19:30 | `IN_TRANSIT(NPC_LENA, upper landing, LOC_SIGNAL_4B)` | Lena moves injured Elias and belongings |
| from 19:30 | `CONCEALED_AT(LOC_SIGNAL_4B)` | hidden inside battery access cavity |

Possible branch changes:

- copied by players/Nadia;
- seized by Rook;
- taken by Reed;
- transmitted successfully;
- left hidden after failed rescue.

It cannot be destroyed accidentally by ordinary scene failure. Destruction requires an explicit terminal event.

## Decoy ledger

### `ITEM_LEDGER_DECOY`

| Time | State | Cause |
|---|---|---|
| before 19:18 | `HELD_BY(NPC_ELIAS)` in messenger bag | prepared as decoy |
| 19:18-19:23 | `IN_TRANSIT(NPC_REED, LOC_TERMINAL_EXT, LOC_REED_OFFICE)` | Reed takes bag and leaves |
| 19:23-21:30 | `HELD_BY(NPC_REED)` | carried during retreat |
| 21:30 onward | normally `AT_LOCATION(LOC_REED_OFFICE)` | Reed attempts access |

If Reed flees before players arrive, he may carry the key. The branch must record this explicitly.

## Ferry photograph

### `ITEM_FERRY_PHOTO_ORIGINAL`

| Time | State | Cause |
|---|---|---|
| before 15:20 | `AT_LOCATION(LOC_NEWSROOM)` in Nadia archive |
| 15:20-16:00 | `HELD_BY(NPC_NADIA)` | used during meeting with Elias |
| 16:00-20:25 | returned to Nadia archive |
| 20:25-21:25 | `CONCEALED_AT(LOC_NEWSROOM)` in Marcus office | Marcus removes it while searching |
| after discovery | held by players, Nadia, or retained by Marcus depending confrontation |

The historical duplicate remains independently available at the archive.

## Timed crash device

### `ITEM_TIMED_CRASH_DEVICE`

- placed by Elias at 17:18;
- activates at 18:04;
- remains behind cabinet;
- removed at 22:15 by a loyal detective only if undiscovered and `A_ROOK_PLAYERS >= 2`.

This gives a fair, time-sensitive clue without making the conclusion impossible after removal.

## Lena phone

### `ITEM_PREPAID_PHONE_LENA`

- purchased 14:05;
- held by Lena throughout;
- call to Elias before terminal arrival;
- call to Iris at 19:31;
- may be surrendered voluntarily at high trust;
- may be seized in a hostile confrontation;
- phone records are independently recoverable through a slower route.

## Iris medical kit

### `ITEM_MEDICAL_KIT_IRIS`

- leaves workplace with Iris at 19:44;
- reaches terminal at 20:12;
- remains in Signal Room 4B;
- visible packaging may create a trail outside only after 22:30 due to disposal by Lena.

## Mina reports

### `ITEM_MINA_REPORT_ORIGINAL`

- created 20:35-20:45;
- cached locally and in version history;
- altered by Rook's staff after 20:45;
- not destroyed by ordinary deletion because metadata persists externally.

### `ITEM_ROOK_REPORT_ALTERED`

- becomes official version at 21:05;
- claims forced-entry indicators stronger than Mina observed;
- references Lena before police have a lawful identification path.

## Reed phone and laptop

`ITEM_REED_PHONE` may move with Reed. `ITEM_REED_LAPTOP` normally remains at the office until Krell's cleanup team arrives after 23:00.

If players miss the office before cleanup:

- the laptop is removed;
- a power log and network trace remain;
- Reed's phone or the decoy tracking service provides alternate proof.

## Newsroom upload

### `ITEM_NADIA_UPLOAD`

Initial state: `LOCKED`, incomplete.

Transitions:

- `00:00`: `AVAILABLE_FOR_COMPLETION` if Nadia still controls account;
- complete code plus primary archive: `TRANSMITTED` by 02:00;
- incomplete documents only: `TRANSMITTED_PARTIAL`;
- Rook gains server control: `INTERCEPTED` unless copied externally;
- Marcus cannot permanently delete the remote encrypted blocks.

## Evidence preservation rule

When players acquire digital proof, they must choose one of:

- keep only on source system, fast but vulnerable;
- make local copy, moderate time;
- transmit to trusted external recipient, slower but durable.

This choice affects later evidence seizure without erasing player achievement arbitrarily.

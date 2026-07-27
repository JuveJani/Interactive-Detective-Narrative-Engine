# DO NOT READ: World State Variables

## 1. Global clock

`CLOCK` stores absolute local time. The playable start is `20:00`. All actions consume explicit time. The compiler may display time in blocks, but the underlying state remains minute-based.

### Hard thresholds

- `22:00`: Iris's missing supplies become police-visible.
- `22:45`: storm surge begins.
- `23:30`: drainage access closes.
- `23:40`: Elias's neurological state becomes visibly critical.
- `00:00`: upload preparation begins.
- `00:20`: Reed enters terminal grounds if not interrupted.
- `01:00`: Elias becomes unresponsive without evacuation.
- `01:15`: earliest death threshold.
- `01:20`: Rook reaches terminal if location exposed.
- `01:45`: final reliable complete-transfer opportunity.
- `02:00`: scheduled transfer closes.

## 2. Case progress variables

| Variable | Type | Initial | Meaning |
|---|---|---:|---|
| `P_STAGED` | 0-3 | 0 | proof strength for staged disappearance |
| `P_HARBOR` | 0-3 | 0 | proof strength for harbor destination |
| `P_ROOM_4B` | 0-3 | 0 | ability to identify Signal Room 4B |
| `P_ROOK` | 0-5 | 0 | evidence strength against Rook |
| `P_MARCUS` | 0-4 | 0 | evidence strength against Marcus |
| `P_REED` | 0-4 | 0 | evidence strength for Reed's presence |
| `P_MEDICAL` | 0-2 | 0 | recognition of medical urgency |
| `P_CODE` | 0-3 | 0 | recovery-code completion |

A conclusion is unlocked by thresholds defined in `07_EVIDENCE_VALIDATION.md`; no single binary clue automatically proves a major conclusion.

## 3. Trust variables

Range: `-2` hostile, `-1` guarded, `0` neutral, `+1` cooperative, `+2` committed ally.

- `T_NADIA = 0`
- `T_MINA = 0`
- `T_LENA = -1`
- `T_IRIS = -1`
- `T_REED = -2`
- `T_MARCUS = -1`

Trust changes require recorded causes. Repeated generic persuasion checks cannot farm trust.

## 4. Antagonist awareness

| Variable | Range | Initial | Meaning |
|---|---:|---:|---|
| `A_ROOK_PLAYERS` | 0-4 | 0 | Rook's awareness of player progress |
| `A_ROOK_TERMINAL` | 0-3 | 1 | confidence terminal is relevant |
| `A_KRELL_TERMINAL` | 0-3 | 2 | confidence terminal is relevant |
| `A_REED_ROOM` | 0-3 | 0 | Reed's knowledge of exact room |
| `A_PUBLIC` | 0-3 | 0 | public visibility of case |

### Awareness effects

- Rook awareness `2`: access restrictions and questioning.
- Rook awareness `3`: evidence removal and false legal pressure.
- Rook awareness `4`: rapid terminal deployment.
- Public awareness `2+`: Rook loses freedom to quietly disappear evidence.

## 5. Elias medical state

`ELIAS_STATE` is one of:

1. `CRITICAL_RESPONSIVE`
2. `CRITICAL_CONFUSED`
3. `CRITICAL_UNRESPONSIVE`
4. `EVACUATING`
5. `IN_SURGERY`
6. `SURVIVED`
7. `DIED`

State changes depend on both clock and actions. Iris stabilization delays one deterioration transition by up to 20 minutes if her supplies remain intact. It never removes the requirement for hospital care.

## 6. Evidence object states

Each evidence item has exactly one physical or virtual state.

Allowed physical states:

- `AT_LOCATION(key)`
- `HELD_BY(key)`
- `IN_TRANSIT(actor, origin, destination, start, end)`
- `CONCEALED_AT(key)`
- `SEIZED_BY(key)`
- `DESTROYED(cause, time)`

Allowed digital states:

- `AVAILABLE`
- `LOCKED`
- `COPIED`
- `ALTERED`
- `DELETED_RECOVERABLE`
- `DELETED_FINAL`
- `TRANSMITTED`
- `INTERCEPTED`

No event may assign two simultaneous physical states.

## 7. Location state variables

### Elias apartment

`APT_STATE`:

- `SEALED_ACCESSIBLE_WITH_MINA`
- `RESTRICTED_BY_ROOK`
- `EVIDENCE_PARTIALLY_REMOVED`
- `INACCESSIBLE`

### Newsroom

`NEWS_STATE`:

- `OPEN_SUPERVISED`
- `MARCUS_DELETING`
- `MARCUS_ABSENT`
- `UPLOAD_ACTIVE`

### Reed office

`REED_OFFICE_STATE`:

- `EMPTY_INTACT`
- `REED_PRESENT`
- `ABANDONED`
- `SEARCHED_BY_KRELL`

### Terminal exterior

`TERMINAL_STATE` combines:

- weather: `DRY`, `SURGE`, `DRAINAGE_CLOSED`;
- hostile presence: none, Reed, police, both;
- access discovered: main, north gate, drainage, cable corridor, roof.

### Signal Room 4B

`ROOM_4B_STATE`:

- `HIDDEN_STABLE`
- `HIDDEN_MEDICAL_DECLINE`
- `FOUND_SECURE`
- `FOUND_CONTESTED`
- `EVACUATED`
- `OVERRUN`

## 8. Player synchronization variables

- `P1_LOCATION`
- `P2_LOCATION`
- `P1_AVAILABLE_AT`
- `P2_AVAILABLE_AT`
- `SHARED_KNOWLEDGE_SET`
- `P1_PRIVATE_KNOWLEDGE_SET`
- `P2_PRIVATE_KNOWLEDGE_SET`
- `REGROUP_REQUIRED`

A private clue may influence only the receiving player's choices until a legal communication or regroup event transfers it into `SHARED_KNOWLEDGE_SET`.

## 9. Ending variables

- `ELIAS_SURVIVAL`
- `LEDGER_PRIMARY_STATUS`
- `FULL_LEDGER_TRANSFERRED`
- `ROOK_EXPOSED_PRIVATE`
- `ROOK_EXPOSED_PUBLIC`
- `KRELL_VALE_EXPOSED`
- `TRUSTED_RESCUE_CONTROL`
- `PUBLIC_ACCUSATION_TARGET`
- `PUBLIC_ACCUSATION_SUPPORT`
- `MARCUS_CONFESSED`
- `REED_COOPERATED`
- `LENA_STATUS`
- `IRIS_STATUS`

Ending resolution uses these variables rather than a single branch label.

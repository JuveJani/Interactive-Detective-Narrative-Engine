# DO NOT READ: World State Variables

This document is the sole owner of every state variable. A variable that does not appear here is not declared.

**Initialization is not a writer.** Each variable records its initialization source as `INIT`. A variable whose only mutation is its initial assignment is a constant, not state, and is not declared here. Every variable below has at least one writer that is not `INIT`, and at least one reader.

Writers and readers are identifiers. They resolve to a node (`EVT_*`), a clock trigger (`CLK_*`), a state-machine transition (`TR_*`), an initialization source (`INIT`), or a gate evaluator (`EVAL_*`).

## 1. Global clock

`CLOCK` stores absolute local time. The playable start is `20:00`. All actions consume explicit time. The compiler may display time in blocks, but the underlying state remains minute-based.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `CLOCK` | minutes, 20:00 onward | `20:00` | `INIT` | every `EVT_*` time cost | every `CLK_*`, every node availability window, `EVAL_ENDING` | Global clock |

### Clock triggers

Every time-driven state change is a declared trigger. A trigger fires once, when `CLOCK` reaches its time and its stated condition holds.

| Trigger | Time | Condition | Writes |
|---|---|---|---|
| `CLK_2035` | 20:35 | none | `NEWS_STATE` |
| `CLK_2130` | 21:30 | none | `REED_OFFICE_STATE` |
| `CLK_2200` | 22:00 | none | `IRIS_WORK_STATE`, `CAFE_STATE` |
| `CLK_2205` | 22:05 | none | `REED_OFFICE_STATE` |
| `CLK_2215` | 22:15 | timed device undiscovered and `A_ROOK_PLAYERS >= 2` | fires `TR_DEVICE_SEIZED` |
| `CLK_2230` | 22:30 | none | `CAFE_STATE` |
| `CLK_2245` | 22:45 | none | `TERMINAL_WEATHER` |
| `CLK_2300` | 23:00 | none | `REED_OFFICE_STATE` |
| `CLK_2320` | 23:20 | none | `ARCHIVE_STATE`, `NEWS_STATE` |
| `CLK_2330` | 23:30 | none | `TERMINAL_WEATHER` |
| `CLK_2340` | 23:40 | none | `ELIAS_STATE` |
| `CLK_0000` | 00:00 | none | `NEWS_STATE` |
| `CLK_0020` | 00:20 | Reed not delayed or turned | `TERMINAL_HOSTILE` |
| `CLK_0100` | 01:00 | no definitive evacuation initiated | `ELIAS_STATE` |
| `CLK_0115` | 01:15 | no hospital transfer | `ELIAS_STATE` |
| `CLK_0120` | 01:20 | terminal exposure threshold reached | fires `TR_TERMINAL_HOSTILE_ROOK` |
| `CLK_0145` | 01:45 | none | read by `EVT_430` |
| `CLK_0200` | 02:00 | none | read by `EVAL_ENDING` |

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

## 2. Case progress totals

**These are derived quantities, not stored variables.** A total is computed from the held clue set and is never independently mutable. No document may store, increment or decrement one. The only operation that changes a total is `GRANT_CLUE`, which adds a clue to a knowledge set; the total is then recomputed.

Every clue is worth 1 point, so a total equals the number of held clues in its group. Each maximum below is computed from the group size in `12_CLUE_DEPENDENCY_GRAPH.md` and is not hand-maintained.

| Total | Clue group | Maximum | Read by |
|---|---|---:|---|
| `P_STAGED` | § 2 Staged disappearance | 7 | `EVAL_CON_STAGED_DISAPPEARANCE` |
| `P_HARBOR` | § 3 Harbor destination | 6 | `EVAL_CON_HARBOR_DESTINATION` |
| `P_ROOM_4B` | § 4 Signal Room 4B | 10 | `EVAL_CON_SIGNAL_4B` |
| `P_LENA_PROTECTING` | § 5 Lena's role | 6 | `EVAL_CON_LENA_PROTECTING` |
| `P_REED` | § 6 Reed's presence | 7 | `EVAL_CON_REED_PRESENT`, `EVAL_CON_REED_CAUSED_CONFRONTATION` |
| `P_MARCUS` | § 7 Marcus leak | 7 | `EVAL_CON_MARCUS_LEAK_PARTIAL`, `EVAL_CON_MARCUS_LEAK_PROVABLE` |
| `P_ROOK` | § 8 Rook compromised | 8 | `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED`, `EVAL_CON_ROOK_PUBLICLY_PROVABLE` |
| `P_MEDICAL` | § 9 Medical emergency | 5 | `EVAL_CON_MEDICAL_EMERGENCY` |
| `P_DECOY` | § 10 Primary vs decoy ledger | 5 | `EVAL_CON_DECOY_KEY` |
| `P_CODE` | § 11 Recovery code | 5 | `EVAL_CON_WINDOW_CODE` |
| passphrase total | § 11a Passphrase access | 2 | `EVAL_CON_PASSPHRASE_ACCESS` |

Group maxima sum to 68 across 66 distinct clues. `CLUE_PHOTO_WINDOW_MARKS` belongs to both § 4 and § 11, and `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` to both § 11 and § 11a; each contributes one point to each of its groups.

Section references are to `12_CLUE_DEPENDENCY_GRAPH.md`. Clue class tags and granting nodes are owned there.

A conclusion is unlocked by the thresholds in `07_EVIDENCE_VALIDATION.md` § 2; no single binary clue automatically proves a major conclusion.

## 3. Trust variables

Range: `-2` hostile, `-1` guarded, `0` neutral, `+1` cooperative, `+2` committed ally.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---:|---|---|---|---|
| `T_NADIA` | −2…+2 | `0` | `INIT` | `EVT_121`, `EVT_211` | `EVAL_NADIA_DISCLOSURE`, `EVAL_ENDING` | Nadia trust |
| `T_MINA` | −2…+2 | `0` | `INIT` | `EVT_111`, `EVT_220` | `EVT_112`, `EVT_220`, `EVAL_RESCUE_CONTROL` | Mina trust |
| `T_MARCUS` | −2…+2 | `−1` | `INIT` | `EVT_240` | `EVAL_MARCUS_DISCLOSURE` | Marcus trust |

Trust changes require recorded causes. Repeated generic persuasion checks cannot farm trust.

Lena, Iris and Reed have no trust variable. Their cooperation is gated on evidence and leverage, defined in `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` §§ 4, 5 and 7, not on a trust scalar.

## 4. Antagonist awareness

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---:|---|---|---|---|
| `A_ROOK_PLAYERS` | 0-4 | `0` | `INIT` | `EVT_111`, `EVT_112`, `EVT_221`, `EVT_223` | `TR_APT_A_TO_B`, `TR_ANNEX_A_TO_B`, `TR_ANNEX_B_TO_C`, `TR_DEVICE_SEIZED` | Rook awareness of players |
| `A_ROOK_TERMINAL` | 0-3 | `1` | `INIT` | `EVT_803` | `TR_TERMINAL_HOSTILE_ROOK` | Rook terminal confidence |
| `A_PUBLIC` | 0-3 | `0` | `INIT` | `EVT_440` | `EVAL_RESCUE_CONTROL`, `EVAL_ENDING` | Public awareness |

### Awareness effects

- Rook awareness `2`: access restrictions and questioning.
- Rook awareness `3`: evidence removal and false legal pressure.
- Rook awareness `4`: rapid terminal deployment.
- Public awareness `2+`: Rook loses freedom to quietly disappear evidence.

Krell's terminal confidence and Reed's knowledge of the exact room are not variables. Krell is remote throughout and his confidence never gates a resolvable event. Reed's ignorance of the room number is a fixed authored outcome, stated in `06_NPC_SCHEDULE_AND_PRIORITY.md` § 4.

## 5. Elias medical state

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `ELIAS_STATE` | 7-value enum below | `CRITICAL_RESPONSIVE` | `INIT` | `CLK_2340`, `CLK_0100`, `CLK_0115`, `EVT_330`, `EVT_400` | `EVT_331`, `EVT_400`, `EVAL_ENDING` | Elias medical |

`ELIAS_STATE` is one of:

1. `CRITICAL_RESPONSIVE`
2. `CRITICAL_CONFUSED`
3. `CRITICAL_UNRESPONSIVE`
4. `EVACUATING`
5. `IN_SURGERY`
6. `SURVIVED`
7. `DIED`

State changes depend on both clock and actions. Iris stabilization delays one deterioration transition by up to 20 minutes if her supplies remain intact. It never removes the requirement for hospital care.

Survival is read from `ELIAS_STATE`. It is not stored separately.

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

The status of the primary ledger is the state of `ITEM_LEDGER_PRIMARY`, owned by `02_ITEM_STATE_MATRIX.md`. It is not duplicated as a separate variable.

## 7. Location state variables

Each location state machine has exactly one variable.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `APT_STATE` | 4-value enum | `SEALED_ACCESSIBLE_WITH_MINA` | `INIT` | `TR_APT_A_TO_B`, `TR_APT_B_TO_C`, `TR_APT_C_TO_D` | `EVT_111`, `EVT_112`, `EVT_113` | Elias apartment |
| `NEWS_STATE` | 4-value enum | `OPEN_SUPERVISED` | `INIT` | `CLK_2035`, `CLK_2320`, `CLK_0000` | `EVT_121`, `EVT_122`, `EVT_123`, `EVT_240`, `EVT_430` | Newsroom |
| `CAFE_STATE` | 3-value enum | `OPEN_FULL_RECORDS` | `INIT` | `CLK_2200`, `CLK_2230` | `EVT_211` | Café Orpheus |
| `ANNEX_STATE` | 4-value enum | `NORMAL_ACCESS` | `INIT` | `TR_ANNEX_A_TO_B`, `TR_ANNEX_B_TO_C`, `TR_ANNEX_TO_D` | `EVT_220`, `EVT_221`, `EVT_222`, `EVT_223` | Police annex |
| `REED_OFFICE_STATE` | 4-value enum | `EMPTY_INTACT` | `INIT` | `CLK_2130`, `CLK_2205`, `CLK_2300` | `EVT_242` | Reed office |
| `IRIS_WORK_STATE` | 3-value enum | `SHIFT_ACTIVE` | `INIT` | `CLK_2200`, `TR_IRISWORK_SEIZED` | `EVT_230` | Iris workplace |
| `ARCHIVE_STATE` | 3-value enum | `OPEN_PUBLIC` | `INIT` | `CLK_2320`, `TR_ARCHIVE_EMERGENCY` | `EVT_210` | Harbor archive |
| `TERMINAL_WEATHER` | 3-value enum | `DRY` | `INIT` | `CLK_2245`, `CLK_2330` | `EVT_312` | Terminal weather |
| `TERMINAL_HOSTILE` | 4-value enum | `NONE` | `INIT` | `CLK_0020`, `TR_TERMINAL_HOSTILE_ROOK` | `EVT_314`, `EVT_420` | Terminal hostile presence |
| `TERMINAL_ROUTES_KNOWN` | subset of 5 route tokens | empty | `INIT` | `EVT_210`, `EVT_212`, `EVT_311`, `EVT_313` | `EVT_310`, `EVT_311`, `EVT_312`, `EVT_313`, `EVT_314` | Terminal known routes |
| `ROOM_4B_STATE` | 6-value enum | `HIDDEN_STABLE` | `INIT` | `EVT_330`, `EVT_400`, `EVT_420` | `EVAL_ENDING` | Signal Room 4B |

### Domains

`APT_STATE`:

- `SEALED_ACCESSIBLE_WITH_MINA`
- `RESTRICTED_BY_ROOK`
- `EVIDENCE_PARTIALLY_REMOVED`
- `INACCESSIBLE`

`NEWS_STATE`:

- `OPEN_SUPERVISED`
- `MARCUS_DELETING`
- `MARCUS_ABSENT`
- `UPLOAD_ACTIVE`

`CAFE_STATE`:

- `OPEN_FULL_RECORDS`
- `CLOSING_LIMITED`
- `CLOSED`

`ANNEX_STATE`:

- `NORMAL_ACCESS`
- `CONTROLLED_ACCESS`
- `HOSTILE_PROCEDURAL`
- `ROOK_CHALLENGED`

`REED_OFFICE_STATE`:

- `EMPTY_INTACT`
- `REED_PRESENT`
- `ABANDONED`
- `SEARCHED_BY_KRELL`

`IRIS_WORK_STATE`:

- `SHIFT_ACTIVE`
- `INCIDENT_REPORTED`
- `ROOK_SEIZED_RECORDS`

`ARCHIVE_STATE`:

- `OPEN_PUBLIC`
- `CLOSING_ARCHIVIST_PRESENT`
- `CLOSED_EMERGENCY`

`TERMINAL_WEATHER`:

- `DRY`
- `SURGE`
- `DRAINAGE_CLOSED`

`TERMINAL_HOSTILE`:

- `NONE`
- `REED`
- `ROOK_TEAM`
- `REED_AND_ROOK`

`TERMINAL_ROUTES_KNOWN` is a subset of:

- `MAIN`
- `NORTH_GATE`
- `DRAINAGE`
- `CABLE_CORRIDOR`
- `ROOF`

`ROOM_4B_STATE`:

- `HIDDEN_STABLE`
- `HIDDEN_MEDICAL_DECLINE`
- `FOUND_SECURE`
- `FOUND_CONTESTED`
- `EVACUATED`
- `OVERRUN`

The terminal exterior is three independent state machines, not one. Weather, hostile presence and known access routes change on separate triggers and are held in three variables.

## 8. Player synchronization variables

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `P1_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | `EVT_100`, `EVT_110`, every P1-eligible node declaring a Location | node entry conditions | Player 1 position |
| `P2_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | `EVT_100`, `EVT_120`, every P2-eligible node declaring a Location | node entry conditions | Player 2 position |
| `P1_AVAILABLE_AT` | time | `20:00` | `INIT` | — | — | **DEPRECATED** — not used for routing or regroup (MBD-04). Retained in schema only; do not write. |
| `P2_AVAILABLE_AT` | time | `20:00` | `INIT` | — | — | **DEPRECATED** — not used for routing or regroup (MBD-04). Retained in schema only; do not write. |
| `SHARED_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | `EVT_150`, `EVT_300` | conclusion evaluators | Shared knowledge |
| `P1_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | P1-eligible clue-granting nodes | `EVT_150`, `EVT_300` | Player 1 private knowledge |
| `P2_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | P2-eligible clue-granting nodes | `EVT_150`, `EVT_300` | Player 2 private knowledge |

A private clue may influence only the receiving player's choices until a legal communication or regroup event transfers it into `SHARED_KNOWLEDGE_SET`.

Whether a regroup may occur is determined by **branch completion** (each role has no remaining legal actions in the current split window) **and player agreement** to enter `EVT_150` or `EVT_300`. Optional world-clock thresholds in `04_TIME_COST_MATRIX.md` § 3a may make regroup **available** but do not force branch exit. `P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` are **deprecated** and are not read for regroup logic.

## 9. Ending variables

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `FULL_LEDGER_TRANSFERRED` | boolean | `false` | `INIT` | `EVT_430` | `EVAL_ENDING` | Transfer outcome |
| `ROOK_EXPOSED_PRIVATE` | boolean | `false` | `INIT` | `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED` | `EVT_400`, `EVAL_ENDING` | Rook exposure |
| `ROOK_EXPOSED_PUBLIC` | boolean | `false` | `INIT` | `EVT_440` | `EVAL_ENDING` | Rook exposure |
| `KRELL_VALE_EXPOSED` | boolean | `false` | `INIT` | `EVT_430`, `EVT_440` | `EVAL_ENDING` | Conspiracy exposure |
| `TRUSTED_RESCUE_CONTROL` | boolean | `false` | `INIT` | `EVT_400` | `EVAL_ENDING` | Rescue control |
| `PUBLIC_ACCUSATION_TARGET` | `NPC_*` or none | none | `INIT` | `EVT_440` | `EVAL_ENDING` | Accusation |
| `PUBLIC_ACCUSATION_SUPPORT` | 0…n | `0` | `INIT` | `EVT_440` | `EVAL_ENDING` | Accusation |
| `MARCUS_CONFESSED` | boolean | `false` | `INIT` | `EVT_241` | `EVAL_ENDING` | Marcus outcome |
| `REED_COOPERATED` | boolean | `false` | `INIT` | `EVT_243` | `EVAL_ENDING` | Reed outcome |
| `LENA_STATUS` | enum | `concealed` | `INIT` | `EVT_331`, `EVT_420` | `EVAL_ENDING` | Lena outcome |
| `IRIS_STATUS` | enum | `concealed` | `INIT` | `EVT_331`, `EVT_400` | `EVAL_ENDING` | Iris outcome |

Ending resolution uses these variables rather than a single branch label.

Elias's survival and the primary ledger's status are not listed. Both are derived: survival from `ELIAS_STATE` in § 5, ledger status from the state of `ITEM_LEDGER_PRIMARY` in `02_ITEM_STATE_MATRIX.md`.

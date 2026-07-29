# DO NOT READ: World State Variables

This document is the sole owner of every state variable. A variable that does not appear here is not declared.

**Initialization is not a writer.** Each variable records its initialization source as `INIT`. A variable whose only mutation is its initial assignment is a constant, not state, and is not declared here. Every variable below has at least one writer that is not `INIT`, and at least one reader.

Writers and readers are identifiers. They resolve to a node (`EVT_*`), a clock trigger (`CLK_*`), a state-machine transition (`TR_*`), an initialization source (`INIT`), or a gate evaluator (`EVAL_*`).

## 1. Global clock

`CLOCK` stores absolute local time. The playable start is `19:00` Saturday. All actions consume explicit time. The compiler may display time in blocks, but the underlying state remains minute-based.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `CLOCK` | minutes, 19:00 onward | `19:00` | `INIT` | every `EVT_*` time cost | every `CLK_*`, every node availability window, `EVAL_ENDING` | Global clock |

### Clock triggers

Every time-driven state change is a declared trigger. A trigger fires once, when `CLOCK` reaches its time and its stated condition holds.

| Trigger | Time | Condition | Writes |
|---|---|---|---|
| `CLK_1930` | 19:30 | none | `TEST_BAY_STATE` |
| `CLK_2030` | 20:30 | none | `SCADA_STATE`, `SECURITY_STATE` |
| `CLK_2130` | 21:30 | none | `FINANCE_STATE` |
| `CLK_2200` | 22:00 | none | `OPS_STATE`, `ARCHITECT_STATE` |
| `CLK_2330` | 23:30 | official report draft not challenged | `REPORT_STATE` |
| `CLK_0030` | 00:30 Sunday | none | fires `TR_CASE_CLOSED`; read by `EVAL_ENDING` |

### Hard thresholds

- `19:30`: test bay transitions from active cordon to evidence lockdown.
- `20:30`: SCADA historian rotation; security desk shift handoff notes become available.
- `21:30`: finance hub evening audit window closes unless players hold liaison clearance.
- `22:00`: operations floor night skeleton crew; Priya's lab access restricted.
- `23:30`: corporate incident report draft auto-submitted unless players have initiated formal challenge.
- `00:30`: case closes; terminal endings evaluated.

## 2. Case progress totals

**These are derived quantities, not stored variables.** A total is computed from the held clue set and is never independently mutable. No document may store, increment or decrement one. The only operation that changes a total is `GRANT_CLUE`, which adds a clue to a knowledge set; the total is then recomputed.

Every clue is worth 1 point, so a total equals the number of held clues in its group. Each maximum below is computed from the group size in `12_CLUE_DEPENDENCY_GRAPH.md` and is not hand-maintained.

| Total | Clue group | Maximum | Read by |
|---|---|---:|---|
| `P_MURDER` | § 2 Murder not accident | 4 | `EVAL_CON_MURDER_NOT_ACCIDENT` |
| `P_FRAUD` | § 3 Financial fraud | 4 | `EVAL_CON_FINANCIAL_FRAUD` |
| `P_CREDENTIAL` | § 4 Credential abuse | 4 | `EVAL_CON_CREDENTIAL_ABUSE` |
| `P_CULPRIT` | § 5 Culprit / Dana | 4 | `EVAL_CON_CULPRIT_DANA` |

Group maxima sum to 16 across 16 distinct clues. No clue belongs to more than one group in this adventure.

Section references are to `12_CLUE_DEPENDENCY_GRAPH.md`. Clue class tags and granting nodes are owned there.

A conclusion is unlocked by the thresholds in `07_EVIDENCE_VALIDATION.md` § 2; no single binary clue automatically proves a major conclusion.

## 3. Trust variables

Range: `-2` hostile, `-1` guarded, `0` neutral, `+1` cooperative, `+2` committed ally.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---:|---|---|---|---|
| `T_SABLE` | −2…+2 | `0` | `INIT` | `EVT_140`, `EVT_240` | `EVAL_SABLE_DISCLOSURE`, `EVAL_ENDING` | Sable trust |
| `T_KEVIN` | −2…+2 | `0` | `INIT` | `EVT_123`, `EVT_220` | `EVAL_KEVIN_DISCLOSURE`, `EVAL_ENDING` | Kevin trust |
| `T_MARCUS` | −2…+2 | `−1` | `INIT` | `EVT_250` | `EVAL_MARCUS_DISCLOSURE` | Marcus trust |

Trust changes require recorded causes. Repeated generic persuasion checks cannot farm trust.

Dana, Priya, Vince, and Tom have no trust variable. Their cooperation is gated on evidence and leverage in `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md`, not on a trust scalar.

## 4. Corporate and antagonist awareness

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---:|---|---|---|---|
| `A_CORPORATE` | 0-3 | `0` | `INIT` | `EVT_130`, `EVT_230`, `EVT_410` | `TR_FINANCE_SEALED`, `EVAL_ENDING` | Corporate legal awareness |
| `A_DANA` | 0-3 | `0` | `INIT` | `EVT_260`, `EVT_330` | `EVT_801`, `EVAL_ENDING` | Dana awareness of investigation |
| `A_SECURITY` | 0-2 | `0` | `INIT` | `EVT_141`, `EVT_312` | `SECURITY_STATE`, `EVAL_ENDING` | Campus security posture |

### Awareness effects

- Corporate awareness `2`: finance terminal access restricted; legal observer assigned.
- Corporate awareness `3`: evidence lockdown accelerates; hostile procedural pressure.
- Dana awareness `2`: off-screen cleanup attempts (`EVT_801`).
- Dana awareness `3`: direct misdirection and witness pressure.
- Security awareness `2`: badge records require warrant-equivalent authorization.

## 5. Victim and scene state

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `ELENA_STATUS` | enum below | `DECEASED_SCENE_INTACT` | `INIT` | `CLK_1930`, `EVT_115` | `EVAL_ENDING` | Victim scene |
| `REPORT_STATE` | enum below | `DRAFT_INTERNAL` | `INIT` | `CLK_2330`, `EVT_410` | `EVAL_ENDING` | Official report |

`ELENA_STATUS` is one of:

1. `DECEASED_SCENE_INTACT`
2. `EVIDENCE_PARTIALLY_CLEARED`
3. `EVIDENCE_SEALED_PLAYER`
4. `EVIDENCE_CORPORATE_SEIZED`

`REPORT_STATE` is one of:

1. `DRAFT_INTERNAL`
2. `CHALLENGED`
3. `SUBMITTED_ACCIDENT`
4. `SUBMITTED_HOMICIDE`
5. `SUBMITTED_INCOMPLETE`

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

Item-level states are owned by `02_ITEM_STATE_MATRIX.md`. They are not duplicated as separate variables here.

## 7. Location state variables

Each location state machine has exactly one variable.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `TEST_BAY_STATE` | 4-value enum | `CORDON_ACTIVE` | `INIT` | `CLK_1930`, `TR_TEST_BAY_SEALED` | `EVT_113`, `EVT_115` | Test bay |
| `SCADA_STATE` | 3-value enum | `NORMAL_ACCESS` | `INIT` | `CLK_2030`, `EVT_123` | `EVT_123`, `EVT_220` | SCADA room |
| `FINANCE_STATE` | 4-value enum | `OPEN_LIAISON` | `INIT` | `CLK_2130`, `TR_FINANCE_SEALED` | `EVT_210`, `EVT_260` | Finance hub |
| `SECURITY_STATE` | 3-value enum | `DESK_STAFFED` | `INIT` | `CLK_2030`, `A_SECURITY` | `EVT_140`, `EVT_141` | Security desk |
| `MAINT_STATE` | 3-value enum | `OPEN_UNSUPERVISED` | `INIT` | `EVT_122`, `EVT_312` | `EVT_122`, `EVT_312` | Maintenance shed |
| `OPS_STATE` | 3-value enum | `DAY_CREW` | `INIT` | `CLK_2200` | `EVT_250`, `EVT_271` | Operations floor |
| `ARCHITECT_STATE` | 3-value enum | `LAB_OPEN` | `INIT` | `CLK_2200` | `EVT_270`, `EVT_271` | Architect lab |

### Domains

`TEST_BAY_STATE`:

- `CORDON_ACTIVE`
- `EVIDENCE_LOCKDOWN`
- `PLAYER_SEALED`
- `CORPORATE_SEALED`

`SCADA_STATE`:

- `NORMAL_ACCESS`
- `HISTORIAN_ROTATION`
- `LEGAL_HOLD`

`FINANCE_STATE`:

- `OPEN_LIAISON`
- `AUDIT_WINDOW`
- `RESTRICTED`
- `SEALED`

`SECURITY_STATE`:

- `DESK_STAFFED`
- `RECORDS_LIMITED`
- `RECORDS_LOCKED`

`MAINT_STATE`:

- `OPEN_UNSUPERVISED`
- `TOOL_CRIB_ALARMED`
- `ACCESS_DENIED`

`OPS_STATE`:

- `DAY_CREW`
- `NIGHT_SKELETON`
- `INCIDENT_COMMAND`

`ARCHITECT_STATE`:

- `LAB_OPEN`
- `LAB_RESTRICTED`
- `LAB_SEALED`

## 8. Player synchronization variables

Scene modes use **narrative roles**, not `P1`/`P2` routing labels. The engine schema retains position keys for compatibility.

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `P1_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | role-assigned nodes | node entry conditions | Role A position |
| `P2_LOCATION` | `LOC_*` | `LOC_START` | `INIT` | role-assigned nodes | node entry conditions | Role B position |
| `P1_AVAILABLE_AT` | time | `19:00` | `INIT` | — | — | **DEPRECATED** — not used for routing or regroup (MBD-04). Retained in schema only; do not write. |
| `P2_AVAILABLE_AT` | time | `19:00` | `INIT` | — | — | **DEPRECATED** — not used for routing or regroup (MBD-04). Retained in schema only; do not write. |
| `SHARED_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | `EVT_150`, `EVT_300` | conclusion evaluators | Shared knowledge |
| `P1_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | role-A clue-granting nodes | `EVT_150`, `EVT_300` | Role A private knowledge |
| `P2_PRIVATE_KNOWLEDGE_SET` | set of `CLUE_*` | empty | `INIT` | role-B clue-granting nodes | `EVT_150`, `EVT_300` | Role B private knowledge |

A private clue may influence only the receiving role's choices until a legal communication or regroup event transfers it into `SHARED_KNOWLEDGE_SET`.

Whether a regroup may occur is determined by **branch completion** (each role has no remaining legal actions in the current split window) **and player agreement** to enter `EVT_150` or `EVT_300`. Optional world-clock thresholds in `04_TIME_COST_MATRIX.md` § 3a may make regroup **available** but do not force branch exit. `P1_AVAILABLE_AT` and `P2_AVAILABLE_AT` are **deprecated** and are not read for regroup logic.

## 9. Ending variables

| Variable | Domain | Initial | Init source | Writers | Readers | Owning state machine |
|---|---|---|---|---|---|---|
| `FRAUD_EXPOSED` | boolean | `false` | `INIT` | `EVAL_CON_FINANCIAL_FRAUD` | `EVAL_ENDING` | Fraud exposure |
| `MURDER_PROVEN` | boolean | `false` | `INIT` | `EVAL_CON_MURDER_NOT_ACCIDENT` | `EVAL_ENDING` | Murder proof |
| `CREDENTIAL_PROVEN` | boolean | `false` | `INIT` | `EVAL_CON_CREDENTIAL_ABUSE` | `EVAL_ENDING` | Credential proof |
| `CULPRIT_NAMED` | boolean | `false` | `INIT` | `EVAL_CON_CULPRIT_DANA` | `EVAL_ENDING` | Culprit identification |
| `PUBLIC_ACCUSATION_TARGET` | `NPC_*` or none | none | `INIT` | `EVT_410` | `EVAL_ENDING` | Accusation |
| `PUBLIC_ACCUSATION_SUPPORT` | 0…n | `0` | `INIT` | `EVT_410` | `EVAL_ENDING` | Accusation strength |
| `EVIDENCE_PRESERVED` | boolean | `false` | `INIT` | `EVT_420` | `EVAL_ENDING` | External copy status |
| `DANA_APPREHENDED` | boolean | `false` | `INIT` | `EVT_430`, `EVT_801` | `EVAL_ENDING` | Culprit custody |
| `WRONG_ACCUSATION` | boolean | `false` | `INIT` | `EVT_410` | `EVAL_ENDING` | Wrong-target flag |

Ending resolution uses these variables rather than a single branch label.

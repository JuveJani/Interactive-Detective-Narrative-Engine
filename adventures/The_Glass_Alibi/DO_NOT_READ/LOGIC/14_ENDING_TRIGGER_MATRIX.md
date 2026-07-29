# DO NOT READ: Ending Trigger Matrix

## 1. Resolution order

The ending resolver is `EVAL_ENDING`, declared here. It reads `CLOCK`, every `CLK_*` trigger, location state variables, awareness scalars, and every ending variable in `01_WORLD_STATE_VARIABLES.md` § 9. It writes no variable.

Endings are computed in this order:

1. determine whether the official report lock has passed;
2. determine murder, fraud, and credential proof status;
3. determine accusation target and support;
4. determine evidence preservation and Dana custody;
5. select narrative ending family;
6. attach partial-success modifiers.

### Ending-family priority order

Families are tested top to bottom. The first satisfied family is the ending. Overlapping conditions are resolved deterministically; partial achievements become modifiers under § 8, never second endings.

| Rank | Family | Terminal node | Primary determination |
|---:|---|---|---|
| 1 | `END_ACCIDENT_VERDICT` | `EVT_903` | report lock: accident narrative uncontested |
| 2 | `END_ESCAPE` | `EVT_905` | custody: Dana exits before apprehension |
| 3 | `END_WRONG_ACCUSATION` | `EVT_902` | accusation: wrong or unsupported target named |
| 4 | `END_PARTIAL_EXPOSURE` | `EVT_904` | proof split: fraud without murder, or murder without full preservation |
| 5 | `END_JUSTICE` | `EVT_901` | full success on proof, accusation, and preservation axes |

**Selection rule.** `EVAL_ENDING` tests families in rank order. Exactly one terminal node fires via `EVT_900` dispatch.

---

## 2. Proof outcome bands

### Murder proof

`MURDER_PROVEN = true` when `EVAL_CON_MURDER_NOT_ACCIDENT` holds (`P_MURDER >= 3` with class requirement).

### Fraud exposure

`FRAUD_EXPOSED = true` when `EVAL_CON_FINANCIAL_FRAUD` holds (`P_FRAUD >= 3` with class requirement).

### Credential proof

`CREDENTIAL_PROVEN = true` when `EVAL_CON_CREDENTIAL_ABUSE` holds (`P_CREDENTIAL >= 3` with procedural/digital requirement).

### Culprit identification

`CULPRIT_NAMED = true` when `EVAL_CON_CULPRIT_DANA` holds and `PUBLIC_ACCUSATION_TARGET = NPC_DANA` with sufficient `PUBLIC_ACCUSATION_SUPPORT`.

Every band reads conclusion evaluators, never raw point totals alone.

---

## 3. Report and deadline gates

| Condition | Effect |
|---|---|
| `REPORT_STATE = SUBMITTED_ACCIDENT` and `MURDER_PROVEN = false` at `CLK_2330` | strongly favors `END_ACCIDENT_VERDICT` unless challenge active |
| `REPORT_STATE = CHALLENGED` | blocks automatic accident submission; extends proof window to `CLK_0030` |
| `REPORT_STATE = SUBMITTED_HOMICIDE` | requires `MURDER_PROVEN`; supports `END_JUSTICE` or `END_PARTIAL_EXPOSURE` |
| `CLOCK >= CLK_0030` | case closes; `EVAL_ENDING` mandatory |

Players who file formal challenge at `EVT_410` set `REPORT_STATE = CHALLENGED` when murder proof meets threshold.

---

## 4. Evidence preservation

### Durable external copy

`EVIDENCE_PRESERVED = true` when `EVT_420` completes with at least one artifact among ledger, historian, footage, or tablet memo in `COPIED` or `TRANSMITTED` state before `CLK_0030` (`ARC_420`).

### Preservation without proof

External copy without murder proof may still support fraud exposure endings but not `END_JUSTICE`.

### No preservation

Missing external copy degrades ending quality; does not erase discovered truth or block terminal resolution.

---

## 5. Custody outcome

| Variable | Set by | Effect |
|---|---|---|
| `DANA_APPREHENDED = true` | `EVT_430` success, or security intercept before `EVT_803` | supports `END_JUSTICE` |
| `DANA_APPREHENDED = false` + `CON_CULPRIT_DANA` | Dana identified but `EVT_803` fired | `END_ESCAPE` if rank 2 conditions met |
| `A_DANA >= 2` without intercept | off-screen cleanup (`EVT_801`, `EVT_802`) | degrades evidence quality; not sole escape trigger |

---

## 6. Accusation gates

Accusation occurs at `EVT_410` (Joint). Players name one `NPC_*`.

| Target | Requirement | Failure result |
|---|---|---|
| `NPC_DANA` | `CON_CULPRIT_DANA` | under-supported rebuttal; may route to `END_PARTIAL_EXPOSURE` or `END_WRONG_ACCUSATION` |
| `NPC_MARCUS` | none — always available | `WRONG_ACCUSATION = true`; Marcus rebuttal (`07` § 3) |
| `NPC_PRIYA` | none — always available | `WRONG_ACCUSATION = true`; Priya rebuttal |
| `NPC_VINCE` | none — always available | `WRONG_ACCUSATION = true`; Vince rebuttal |
| `NPC_TOM` | none — always available | `WRONG_ACCUSATION = true`; Tom rebuttal |
| `NPC_SABLE` / `NPC_KEVIN` | none — always available | misdirection only; witness rebuttal |

`PUBLIC_ACCUSATION_SUPPORT` counts held culprit clues plus authenticated preserved artifacts referenced in the accusation.

---

## 7. Ending families

### `END_JUSTICE`

**Terminal node:** `EVT_901` — **Terminal type:** `VICTORY`

Requires all of:

- `MURDER_PROVEN = true`;
- `CULPRIT_NAMED = true` with `PUBLIC_ACCUSATION_TARGET = NPC_DANA`;
- `WRONG_ACCUSATION = false`;
- `EVIDENCE_PRESERVED = true`;
- `DANA_APPREHENDED = true`.

Fraud and credential proof may independently succeed; narrative text references all proven threads.

### `END_WRONG_ACCUSATION`

**Terminal node:** `EVT_902` — **Terminal type:** `CASE_UNRESOLVED`

Requires:

- `WRONG_ACCUSATION = true`; or
- `PUBLIC_ACCUSATION_TARGET != NPC_DANA` with `PUBLIC_ACCUSATION_SUPPORT < 2`.

Target-specific rebuttal from `07_EVIDENCE_VALIDATION.md` § 3 must appear in epilogue variant.

### `END_ACCIDENT_VERDICT`

**Terminal node:** `EVT_903` — **Terminal type:** `TIME_EXPIRED`

Requires:

- `MURDER_PROVEN = false` at resolution; and
- `REPORT_STATE = SUBMITTED_ACCIDENT` or players failed to challenge before `CLK_2330`; or
- `PUBLIC_ACCUSATION_SUPPORT = 0` and no formal challenge filed.

Private player knowledge may survive; institutional record accepts accident.

### `END_PARTIAL_EXPOSURE`

**Terminal node:** `EVT_904` — **Terminal type:** `PARTIAL_SUCCESS`

Requires one or more of:

- `FRAUD_EXPOSED = true` and `MURDER_PROVEN = false`;
- `MURDER_PROVEN = true` and `EVIDENCE_PRESERVED = false`;
- `CULPRIT_NAMED = true` with Dana under-supported accusation but fraud+credential proven;
- correct Dana accusation with `DANA_APPREHENDED = false` but preserved proof.

Does not apply when `END_JUSTICE` or `END_WRONG_ACCUSATION` ranks higher.

### `END_ESCAPE`

**Terminal node:** `EVT_905` — **Terminal type:** `NARRATIVE_FAILURE`

Requires:

- `CON_CULPRIT_DANA` threshold met or strong Dana suspicion (`P_CULPRIT >= 2`); and
- `DANA_APPREHENDED = false`; and
- `EVT_803` fired or clock past 22:45 without challenge and Dana exit window open.

Murder or fraud proof may still be true; custody and institutional closure fail.

---

## 8. Partial-success modifiers

Possible modifiers enriching epilogue without changing the selected family:

- Marcus referred for safety cover-up review;
- Priya stabilizes Elena's validation work;
- Tom exonerated via dock ticket entered into record;
- Vince loses contract; procurement review opened;
- Sable or Kevin named as preservation witnesses;
- partial footage alteration noted but overcome;
- Glassline shell vendors flagged for later prosecution.

---

## 9. Identifier status

This document owns the `END_` namespace and is the authoritative owner of ending trigger conditions.

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 5 | `END_JUSTICE` (`EVT_901`), `END_WRONG_ACCUSATION` (`EVT_902`), `END_ACCIDENT_VERDICT` (`EVT_903`), `END_PARTIAL_EXPOSURE` (`EVT_904`), `END_ESCAPE` (`EVT_905`) |

No ending identifier is `DEFINITION_ONLY`, `RESERVED`, or `DEPRECATED`. Terminal node identity is owned by `10_INVESTIGATION_NODE_GRAPH.md` § 14. Each `END_*` family is referenced from `EVT_900` dispatch and from at least one terminal node.

`EVAL_ENDING` is declared in this document and cross-referenced from `07_EVIDENCE_VALIDATION.md` § 7.

# DO NOT READ: Clue Dependency Graph

## 1. Notation and the progress model

This document is the clue register. It owns the `CLUE_` namespace.

The canonical progression is:

```text
Node outcome
     ↓
  Points
     ↓
  Clues
     ↓
Conclusions
```

`GRANT_CLUE(clue_identifier)` is the only operation a node may perform on investigative progress.

- A clue carries its own point value and class tags. There is no separate point award.
- **Every clue is worth 1 point.** Point totals are derived from the held clue set and are never stored as mutable state. No document may increment or decrement a total.
- **Clue acquisition is idempotent.** `GRANT_CLUE` on an already-held clue is a no-op with respect to points and classes. A clue reachable through several routes awards its value exactly once.
- `GRANT_CLUE` writes to the acting player's private knowledge set during `Split` scenes. A `Joint`-scene node writes to `SHARED_KNOWLEDGE_SET`. Regroup nodes `EVT_150` and `EVT_300` move clues from private sets into the shared set.
- A conclusion evaluator reads the union of `SHARED_KNOWLEDGE_SET` and the evaluating player's private set.

Class tags are drawn from the closed set owned by `07_EVIDENCE_VALIDATION.md` § 1. A multi-class tag records which classes a clue is eligible to fill; under the counting rule in that section a clue contributes exactly one class to any diversity count.

`Status` is `ACTIVE` where at least one node grants the clue.

---

## 2. Murder not accident

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_TEST_BAY_CO2_ANOMALY` | `PHYSICAL`, `PROCEDURAL` | 1 | `EVT_115` | `ACTIVE` |
| `CLUE_PURGE_MANUAL_OVERRIDE` | `DIGITAL`, `PROCEDURAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_SENSOR_SPOOF_TRACE` | `PHYSICAL` | 1 | `EVT_115` | `ACTIVE` |
| `CLUE_ELENA_INJURY_PATTERN` | `PHYSICAL`, `CONTEXTUAL` | 1 | `EVT_113` | `ACTIVE` |

**Group maximum:** 4.

### Deduction

`CON_MURDER_NOT_ACCIDENT`

Requires 3 points and at least 2 distinct classes, or `CLUE_PURGE_MANUAL_OVERRIDE` plus one `PHYSICAL` clue (`07_EVIDENCE_VALIDATION.md` § 2).

### Gates unlocked

- challenge corporate accident framing;
- Kevin Stage 1 disclosure;
- homicide challenge filing at `EVT_410`;
- `MURDER_PROVEN` via `EVAL_CON_MURDER_NOT_ACCIDENT`.

### Redundancy paths

- `ITEM_PURGE_LOG` via SCADA (`EVT_123`);
- test-bay physical anomaly (`EVT_115`);
- Kevin testimony after `FACT_MANUAL_PURGE` (`EVT_220`);
- Elena injury pattern via tablet forensics (`EVT_113`).

---

## 3. Financial fraud

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_FINANCE_DISCREPANCY` | `DIGITAL`, `PROCEDURAL` | 1 | `EVT_210` | `ACTIVE` |
| `CLUE_VENDOR_SHELL_COMPANY` | `PROCEDURAL`, `CONTEXTUAL` | 1 | `EVT_271` | `ACTIVE` |
| `CLUE_DANA_APPROVAL_PATTERN` | `PROCEDURAL`, `BEHAVIOURAL` | 1 | `EVT_260` | `ACTIVE` |
| `CLUE_ELENA_AUDIT_THREAD` | `DIGITAL`, `CONTEXTUAL` | 1 | `EVT_271`, `EVT_113` | `ACTIVE` |

**Group maximum:** 4.

### Deduction

`CON_FINANCIAL_FRAUD`

Requires 3 points and at least 2 distinct classes.

### Gates unlocked

- Dana pressure ladder Stage 2 (`EVT_230`);
- Priya documentary corroboration;
- Marcus finance-hold admission;
- `FRAUD_EXPOSED` via `EVAL_CON_FINANCIAL_FRAUD`.

### Redundancy paths

- finance hub ledger (`EVT_210`, `CHK_210_INVESTIGATION`);
- Elena audit memo on tablet (`EVT_113`);
- Priya email thread (`EVT_271`, `FACT_ELENA_VENDOR_WARNING`);
- shell vendor procedural cross-check (`EVT_260`).

---

## 4. Credential abuse

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_BADGE_CLONE_DEVICE` | `PHYSICAL` | 1 | `EVT_312` | `ACTIVE` |
| `CLUE_BADGE_SWIPE_MISMATCH` | `DIGITAL`, `PROCEDURAL` | 1 | `EVT_141` | `ACTIVE` |
| `CLUE_AFTER_HOURS_ACCESS` | `PROCEDURAL` | 1 | `EVT_140` | `ACTIVE` |
| `CLUE_MAINT_WORKORDER_FORGED` | `PROCEDURAL`, `PHYSICAL` | 1 | `EVT_122` | `ACTIVE` |

**Group maximum:** 4.

### Deduction

`CON_CREDENTIAL_ABUSE`

Requires 3 points and at least 1 point from a clue tagged `PROCEDURAL` or `DIGITAL`.

### Gates unlocked

- Sable Stage 2 export;
- Tom confrontation leverage;
- Vince cooperation gate;
- `CREDENTIAL_PROVEN` via `EVAL_CON_CREDENTIAL_ABUSE`.

### Redundancy paths

- badge swipe mismatch (`EVT_141`);
- badge clone device (`EVT_312`);
- forged maintenance work order (`EVT_122`);
- auth log duplicate session with Tom alibi (`EVT_123` metadata variant, `EVT_122`).

---

## 5. Culprit / Dana

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_DANA_PRESENCE_WINDOW` | `PROCEDURAL`, `DIGITAL` | 1 | `EVT_141` | `ACTIVE` |
| `CLUE_DANA_TABLET_SYNC` | `DIGITAL`, `PROCEDURAL` | 1 | `EVT_113` | `ACTIVE` |
| `CLUE_CO2_OVERRIDE_AUTH` | `PROCEDURAL`, `DIGITAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_DANA_FINANCE_LINK` | `CONTEXTUAL`, `PROCEDURAL` | 1 | `EVT_230` | `ACTIVE` |

**Group maximum:** 4.

### Deduction

`CON_CULPRIT_DANA`

Requires 3 points and 3 distinct classes; requires `CON_MURDER_NOT_ACCIDENT` and at least one of `CON_FINANCIAL_FRAUD` or `CON_CREDENTIAL_ABUSE` (`07_EVIDENCE_VALIDATION.md` § 2).

### Gates unlocked

- supported naming of `NPC_DANA` at `EVT_410`;
- Dana apprehension route at `EVT_430`;
- `CULPRIT_NAMED` via `EVAL_CON_CULPRIT_DANA`.

### Redundancy paths

- Dana presence window + CO₂ override auth (`EVT_141`, `EVT_123`);
- Dana tablet sync + finance approval pattern (`EVT_113`, `EVT_260`);
- badge audit suppression + shell vendor payment linking Dana approvals (`EVT_140`, `EVT_271`).

---

## 6. Cross-group dependency summary

| Conclusion | Minimum clues | Prerequisite conclusions |
|---|---|---|
| `CON_MURDER_NOT_ACCIDENT` | 3 from § 2 | none |
| `CON_FINANCIAL_FRAUD` | 3 from § 3 | none |
| `CON_CREDENTIAL_ABUSE` | 3 from § 4 | none |
| `CON_CULPRIT_DANA` | 3 from § 5 | `CON_MURDER_NOT_ACCIDENT` + (`CON_FINANCIAL_FRAUD` or `CON_CREDENTIAL_ABUSE`) |

No clue belongs to more than one group in this adventure. Sixteen clues; four groups of four; group maxima sum to 16.

---

## 7. Soft-lock prevention edges

| If players miss… | Fallback route | Cost |
|---|---|---|
| `EVT_115` sensor spoof | Kevin flatline export at `EVT_220` | +20 min; `T_KEVIN` required |
| `EVT_123` purge log | Kevin Stage 1 at `EVT_220` after any murder clue | trust or time |
| `EVT_210` deep ledger | Elena tablet memo at `EVT_113` | partial fraud only until `EVT_271` |
| `EVT_312` clone device | auth log mismatch + work order at `EVT_122`/`EVT_141` | no physical device |
| `EVT_141` badge export | Sable Stage 2 at `EVT_240` after credential thread | persuasion or trust |
| all Dana culprit clues | cannot reach `CON_CULPRIT_DANA`; partial endings remain | — |

Every mandatory conclusion has at least three independent granting routes declared in § 2–§ 5 and `07_EVIDENCE_VALIDATION.md` § 6.

---

## 8. Identifier status

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 16 | all `CLUE_*` in § 2–§ 5 |

No clue identifier is `DEFINITION_ONLY`, `RESERVED`, or `DEPRECATED`. Every `ACTIVE` clue has at least one granting node in `10_INVESTIGATION_NODE_GRAPH.md`.

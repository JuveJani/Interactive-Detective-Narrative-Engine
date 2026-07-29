# DO NOT READ: Evidence Validation and Fair-Play Gates

## 1. Proof classes

**This section is the canonical owner of the clue-class vocabulary.** The set is closed. Every clue carries at least one class drawn from it. No other document may declare, extend or redefine the set.

| Class | Meaning |
|---|---|
| `PHYSICAL` | object, trace or document |
| `DIGITAL` | recording, file, metadata payload or transmitted data |
| `TESTIMONIAL` | statement from an NPC |
| `PROCEDURAL` | log, authorization record or process artefact |
| `CONTEXTUAL` | motive, history or financial pressure |
| `BEHAVIOURAL` | contradiction or action observed by players |

A major accusation requires multiple independent classes.

### Class-diversity counting rule

Class diversity counts distinct classes across the held clue set. Each held clue is assigned to exactly one of its tagged classes, and the assignment is chosen to maximise the count. A clue therefore contributes one class, never two, and a requirement for N classes cannot be met by fewer than N clues.

A multi-class tag records which classes a clue is eligible to fill, not how many it contributes at once.

## 2. Conclusion thresholds

Every threshold is stated as a point sum plus a class-diversity requirement over the held clue set. Every clue is worth 1 point. Clues, classes, and granting nodes are owned by `12_CLUE_DEPENDENCY_GRAPH.md`.

Point totals are derived, never stored. `P_MURDER`, `P_FRAUD`, `P_CREDENTIAL`, and `P_CULPRIT` are declared in `01_WORLD_STATE_VARIABLES.md` § 2.

| Conclusion | Derived total | Threshold | Class requirement | Group maximum |
|---|---|---|---|---:|
| `CON_MURDER_NOT_ACCIDENT` | `P_MURDER` | 3 points | 2 distinct classes, or `CLUE_PURGE_MANUAL_OVERRIDE` plus one `PHYSICAL` clue | 4 |
| `CON_FINANCIAL_FRAUD` | `P_FRAUD` | 3 points | 2 distinct classes | 4 |
| `CON_CREDENTIAL_ABUSE` | `P_CREDENTIAL` | 3 points | at least 1 point from `PROCEDURAL` or `DIGITAL` | 4 |
| `CON_CULPRIT_DANA` | `P_CULPRIT` | 3 points | 3 distinct classes; requires `CON_MURDER_NOT_ACCIDENT` and at least one of `CON_FINANCIAL_FRAUD` or `CON_CREDENTIAL_ABUSE` | 4 |

`CON_CULPRIT_DANA` is the accusation-grade gate. Meeting it enables supported naming of `NPC_DANA` at `EVT_410`. Partial Dana suspicion below threshold may still inform narrative but triggers wrong-accusation handling if players accuse without support.

## 3. Wrong accusation handling

A wrong accusation never triggers a generic unexplained failure.

Each suspect has a specific rebuttal:

| Target | Rebuttal | Missing link |
|---|---|---|
| `NPC_MARCUS` | export hold is real but auth log shows purge token did not originate from ops console; Marcus lacked bay entry window | credential + timeline |
| `NPC_PRIYA` | rivalry and design dispute documented; badge and purge auth trace to finance liaison channel, not architect lab | credential / Dana link |
| `NPC_VINCE` | contractor enabled camera gaps and received shell payment; no finance approval authority and no purge auth | fraud authority / murder means |
| `NPC_TOM` | fob physically present; auth log shows duplicate session while Tom was shed CCTV-visible | clone / Dana presence |
| `NPC_DANA` (under-supported) | Dana had motive and access, but accusation lacks class diversity or murder proof | see threshold table |
| `NPC_SABLE` / `NPC_KEVIN` | witnesses preserved records inconsistent with guilt; no financial authority | n/a — misdirection only |

The ending text must state which evidence link is missing or contradicted.

## 4. Evidence preservation

A conclusion may be personally convincing but not publicly provable. Track:

- `KNOWN_TO_PLAYERS`
- `PRESERVED_COPY`
- `AUTHENTICATED`
- `PUBLICLY_DISCLOSED`

This distinction supports endings where players solve the case but fail to expose it before `CLK_0030`.

## 5. Skill-check rule

Critical clues are not erased by a single failed skill check.

Failure may cause:

- partial description;
- added time;
- antagonist awareness;
- loss of one access route;
- requirement for corroboration.

At least one non-skill-gated route remains for every mandatory conclusion.

Bound checks (`17_CHECK_REGISTER.md`):

| Check | Skill | Typical gate |
|---|---|---|
| `CHK_115_PERCEPTION` | Perception | sensor spoof fragment visibility |
| `CHK_123_TECHNOLOGY` | Technology | SCADA metadata depth |
| `CHK_210_INVESTIGATION` | Investigation | finance ledger deep search |
| `CHK_240_PERSUASION` | Persuasion | Sable/Kevin Stage 1 acceleration |
| `CHK_312_ATHLETICS` | Athletics | maintenance cable-tray access |

## 6. Soft-lock audit

### Murder / not accident

At least three independent routes:

- `ITEM_PURGE_LOG` via SCADA (`EVT_123`);
- test-bay physical anomaly (`EVT_115`);
- Kevin testimony after `FACT_MANUAL_PURGE`;
- Elena injury pattern via tablet or coroner summary.

### Financial fraud

At least three independent routes:

- finance hub ledger (`EVT_210`, `CHK_210_INVESTIGATION`);
- Elena audit memo on tablet;
- Priya email thread (`FACT_ELENA_VENDOR_WARNING`);
- shell vendor procedural cross-check.

### Credential abuse

At least three independent routes:

- badge swipe mismatch (`EVT_141`);
- badge clone device (`EVT_312`);
- forged maintenance work order;
- auth log duplicate session with Tom alibi.

### Culprit / Dana

At least two routes to `P_CULPRIT` threshold after prerequisite conclusions:

- Dana presence window + CO₂ override auth;
- Dana tablet sync timestamps + finance approval pattern;
- badge audit suppression + shell vendor payment to Vince linking Dana approvals.

### Accusation and deadline

- Supported Dana accusation remains reachable without all five checks succeeding.
- Missing external copy degrades ending; does not deadlock before `CLK_0030`.
- If Dana flees (`EVT_803`), murder/fraud proof endings still available; custody ending degrades.

## 7. Gate evaluators

This document owns the `EVAL_` namespace jointly with `14_ENDING_TRIGGER_MATRIX.md`, which declares `EVAL_ENDING`.

| Evaluator | Gate | Reads | Writes |
|---|---|---|---|
| `EVAL_CON_MURDER_NOT_ACCIDENT` | § 2 murder threshold | `P_MURDER`, held clue set | `MURDER_PROVEN` |
| `EVAL_CON_FINANCIAL_FRAUD` | § 2 fraud threshold | `P_FRAUD` | `FRAUD_EXPOSED` |
| `EVAL_CON_CREDENTIAL_ABUSE` | § 2 credential threshold | `P_CREDENTIAL` | `CREDENTIAL_PROVEN` |
| `EVAL_CON_CULPRIT_DANA` | § 2 culprit threshold | `P_CULPRIT`, prerequisite conclusions | `CULPRIT_NAMED` |
| `EVAL_SABLE_DISCLOSURE` | Sable stages in `03` § 2 | `T_SABLE`, credential clues | none |
| `EVAL_KEVIN_DISCLOSURE` | Kevin stages in `03` § 3 | `T_KEVIN`, murder clues | none |
| `EVAL_MARCUS_DISCLOSURE` | Marcus stages in `03` § 4 | `T_MARCUS`, fraud clues | none |

Every evaluator in this section has status `ACTIVE`.

Section references for clue groups are to `12_CLUE_DEPENDENCY_GRAPH.md`.

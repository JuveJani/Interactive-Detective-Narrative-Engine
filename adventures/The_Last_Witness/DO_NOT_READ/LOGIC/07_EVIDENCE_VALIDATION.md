# DO NOT READ: Evidence Validation and Fair-Play Gates

## 1. Proof classes

**This section is the canonical owner of the clue-class vocabulary.** The set is closed. Every clue carries at least one class drawn from it. No other document may declare, extend or redefine the set; other documents may summarise it only when the summary is explicitly marked non-authoritative.

| Class | Meaning |
|---|---|
| `PHYSICAL` | object, trace or document |
| `DIGITAL` | recording, file, metadata payload or transmitted data |
| `TESTIMONIAL` | statement from an NPC |
| `PROCEDURAL` | log, authorization record or process artefact |
| `CONTEXTUAL` | motive, history or financial pressure |
| `BEHAVIOURAL` | contradiction or action observed by players |

A major accusation requires multiple independent classes.

## 2. Conclusion thresholds

### Staged disappearance

Unlock when either:

- three points from at least two clue classes; or
- two strong physical/procedural clues plus Nadia admission.

Possible sources:

- preserved blood;
- missing medication/passport;
- service latch;
- timed device;
- neighbour identification;
- Nadia disclosure.

### Harbor destination

Unlock at three points from at least two routes:

- transit record;
- tide note;
- café footage/testimony;
- Elias search history;
- Nadia admission.

### Signal Room 4B

Unlock requires:

- room identifier evidence; and
- a route/access clue.

Room evidence:

- photo markings;
- archive numbering;
- Elias fragment;
- Lena/Iris disclosure.

Route evidence:

- cable map;
- drainage timing;
- north gate maintenance record;
- trusted emergency entry.

### Reed presence

Require at least two independent routes:

- decoy key possession;
- blood/harbor trace;
- Krell message;
- terminal access trace;
- Lena/Iris testimony;
- Reed admission.

### Rook compromised

Private operational conclusion: `P_ROOK >= 3`, with at least one procedural clue.  
Public accusation: `P_ROOK >= 4`, with at least three classes or preserved direct contact evidence.

Sources:

- unauthorized camera request;
- altered report metadata;
- false protection paperwork;
- Krell contact;
- fabricated Lena bulletin;
- Reed/Mina testimony.

### Marcus leak

Partial conclusion at two points. Full provable accusation at three points and two classes.

## 3. Wrong accusation handling

A wrong accusation never triggers a generic unexplained failure.

Each target has a specific rebuttal:

- Nadia: evidence shows she helped stage disappearance but did not transmit location to Reed.
- Lena: timing and medical trail show concealment after injury, not initial abduction.
- Marcus: leak is real but cannot explain police-system manipulation.
- Reed: caused confrontation but lacks authority and financial architecture.
- Mina: report version history supports her account.

The ending text must state which evidence link is missing or contradicted.

## 4. Evidence preservation

A conclusion may be personally convincing but not publicly provable. Track:

- `KNOWN_TO_PLAYERS`
- `PRESERVED_COPY`
- `AUTHENTICATED`
- `PUBLICLY_DISCLOSED`

This distinction supports endings where players solve the case but fail to expose it.

## 5. Skill-check rule

Critical clues are not erased by a single failed skill check.

Failure may cause:

- partial description;
- added time;
- antagonist awareness;
- loss of one access route;
- requirement for corroboration.

At least one non-skill-gated route remains for every mandatory conclusion.

## 6. Soft-lock audit

### Terminal access

At least two routes remain in every state:

- map/cable corridor;
- north gate through archivist or maintenance record;
- drainage before closure;
- emergency entry with Mina;
- main entrance during confrontation.

### Room identification

At least three sources exist:

- original photograph;
- archive duplicate;
- Elias fragment;
- Lena/Iris cooperation;
- generator/cable trace as late failsafe.

### Medical rescue

At least three rescue-control routes exist:

- Mina;
- independent paramedic/hospital contact;
- public exposure of Rook;
- direct private transport as dangerous fallback.

### Code recovery

If photograph is lost, archive duplicate plus Nadia fragment remains. If Nadia is hostile, partial transfer or later Elias testimony remains possible, producing a weaker ending rather than deadlock.

## 7. Gate evaluators

This document owns the `EVAL_` namespace jointly with `14_ENDING_TRIGGER_MATRIX.md`, which declares `EVAL_ENDING`. The evaluators below are declared here.

| Evaluator | Gate | Reads | Writes |
|---|---|---|---|
| `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED` | § 2 "Rook compromised", private operational conclusion | `P_ROOK`, procedural clue presence | `ROOK_EXPOSED_PRIVATE` |
| `EVAL_NADIA_DISCLOSURE` | Nadia's disclosure stages in `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` § 2 | `T_NADIA`, `P_HARBOR` | none |
| `EVAL_MARCUS_DISCLOSURE` | Marcus's confession gate in `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` § 8 | `T_MARCUS`, `P_MARCUS` | none |
| `EVAL_RESCUE_CONTROL` | trusted-rescue requirements in § 6 "Medical rescue" | `T_MINA`, `A_PUBLIC`, `ROOK_EXPOSED_PRIVATE` | none |

Each evaluator has status `ACTIVE`. The conclusion evaluators for the remaining clue groups are declared when the thresholds in § 2 are restated against the clue register.

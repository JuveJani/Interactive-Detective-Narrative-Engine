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

### Class-diversity counting rule

Class diversity counts distinct classes across the held clue set. Each held clue is assigned to exactly one of its tagged classes, and the assignment is chosen to maximise the count. A clue therefore contributes one class, never two, and a requirement for N classes cannot be met by fewer than N clues.

A multi-class tag records which classes a clue is eligible to fill, not how many it contributes at once.

## 2. Conclusion thresholds

Every threshold is stated as a point sum plus a class-diversity requirement over the held clue set. Every clue is worth 1 point. Clues, their classes and their granting nodes are owned by `12_CLUE_DEPENDENCY_GRAPH.md`; the group maxima below are computed from that register.

Point totals are derived, never stored. `P_STAGED`, `P_HARBOR`, `P_ROOM_4B`, `P_ROOK`, `P_MARCUS`, `P_REED`, `P_MEDICAL`, `P_CODE`, `P_LENA_PROTECTING` and `P_DECOY` name derived totals declared in `01_WORLD_STATE_VARIABLES.md` § 2.

| Conclusion | Derived total | Threshold | Class requirement | Group maximum |
|---|---|---|---|---:|
| `CON_STAGED_DISAPPEARANCE` | `P_STAGED` | 3 points | 2 distinct classes, or `CLUE_NADIA_PLAN_ADMISSION` plus one `PHYSICAL` clue | 7 |
| `CON_HARBOR_DESTINATION` | `P_HARBOR` | 3 points | 2 distinct classes | 6 |
| `CON_SIGNAL_4B` | `P_ROOM_4B` | 1 identifier point and 1 route point | none; the gate is structural | 10 |
| `CON_LENA_PROTECTING` | `P_LENA_PROTECTING` | 3 points | 2 distinct classes from `TESTIMONIAL`, `PROCEDURAL`, `BEHAVIOURAL` | 6 |
| `CON_REED_PRESENT` | `P_REED` | 2 points | at least 1 point from a clue not tagged `TESTIMONIAL` | 7 |
| `CON_REED_CAUSED_CONFRONTATION` | `P_REED` | `CON_REED_PRESENT` plus 1 further point | that point `PHYSICAL` or `TESTIMONIAL` | 7 |
| `CON_MARCUS_LEAK_PARTIAL` | `P_MARCUS` | 2 points | none | 7 |
| `CON_MARCUS_LEAK_PROVABLE` | `P_MARCUS` | 3 points | 2 distinct classes | 7 |
| `CON_ROOK_OPERATIONALLY_COMPROMISED` | `P_ROOK` | 3 points | at least 1 point from a `PROCEDURAL` clue | 8 |
| `CON_ROOK_PUBLICLY_PROVABLE` | `P_ROOK` | 4 points | 3 distinct classes, or preserved direct-contact evidence; plus one `AUTHENTICATED` or `PRESERVED_COPY` record under § 4 | 8 |
| `CON_MEDICAL_EMERGENCY` | `P_MEDICAL` | 2 points, or automatic on `EVT_330` | none | 5 |
| `CON_DECOY_KEY` | `P_DECOY` | 2 points, or `CLUE_DECOY_TRACKER` with `CLUE_DECOY_LIMITED_CONTENT` | none | 5 |
| `CON_WINDOW_CODE` | `P_CODE` | 1 fragment point and 1 interpretation point | none; the gate is structural | 5 |

`CON_MARCUS_LEAK` and `CON_ROOK_COMPROMISED` carry no threshold. They are `DEPRECATED` umbrella identifiers superseded by the tiered pairs above.

### Structural gates in full

`CON_SIGNAL_4B` requires one point from the identifier clues in `12_CLUE_DEPENDENCY_GRAPH.md` § 4 and one from the route clues in the same section. An identifier without a route and a route without an identifier are each insufficient regardless of class.

`CON_WINDOW_CODE` requires one point from `CLUE_NADIA_FIRST_THREE` or `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS`, and one from `CLUE_PHOTO_WINDOW_MARKS`, `CLUE_ARCHIVE_WINDOW_NUMBERING` or `CLUE_ELIAS_FRAGMENT_WINDOWS`.

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

### Conclusion evaluators

One evaluator per conclusion threshold in § 2. Each reads the held clue set, which is the union of `SHARED_KNOWLEDGE_SET` and the evaluating player's private set, and derives its total from it. None writes a stored total.

| Evaluator | Conclusion | Reads |
|---|---|---|
| `EVAL_CON_STAGED_DISAPPEARANCE` | `CON_STAGED_DISAPPEARANCE` | § 2 staged clue group |
| `EVAL_CON_HARBOR_DESTINATION` | `CON_HARBOR_DESTINATION` | § 3 harbor clue group |
| `EVAL_CON_SIGNAL_4B` | `CON_SIGNAL_4B` | § 4 identifier and route clue groups |
| `EVAL_CON_LENA_PROTECTING` | `CON_LENA_PROTECTING` | § 5 Lena clue group |
| `EVAL_CON_REED_PRESENT` | `CON_REED_PRESENT` | § 6 Reed clue group |
| `EVAL_CON_REED_CAUSED_CONFRONTATION` | `CON_REED_CAUSED_CONFRONTATION` | § 6 Reed clue group, plus `CON_REED_PRESENT` |
| `EVAL_CON_MARCUS_LEAK_PARTIAL` | `CON_MARCUS_LEAK_PARTIAL` | § 7 Marcus clue group |
| `EVAL_CON_MARCUS_LEAK_PROVABLE` | `CON_MARCUS_LEAK_PROVABLE` | § 7 Marcus clue group |
| `EVAL_CON_ROOK_OPERATIONALLY_COMPROMISED` | `CON_ROOK_OPERATIONALLY_COMPROMISED` | § 8 Rook clue group |
| `EVAL_CON_ROOK_PUBLICLY_PROVABLE` | `CON_ROOK_PUBLICLY_PROVABLE` | § 8 Rook clue group, plus the § 4 preservation record |
| `EVAL_CON_MEDICAL_EMERGENCY` | `CON_MEDICAL_EMERGENCY` | § 9 medical clue group, plus `EVT_330` |
| `EVAL_CON_DECOY_KEY` | `CON_DECOY_KEY` | § 10 decoy clue group |
| `EVAL_CON_WINDOW_CODE` | `CON_WINDOW_CODE` | § 11 code clue group |

Section references are to `12_CLUE_DEPENDENCY_GRAPH.md`.

Every evaluator in this section has status `ACTIVE`.

# DO NOT READ: Ending Trigger Matrix

## 1. Resolution order

The ending resolver is `EVAL_ENDING`, declared here. It reads `CLOCK`, `CLK_0200`, `ELIAS_STATE`, `ROOM_4B_STATE`, `A_PUBLIC`, `T_NADIA`, and every ending variable in `01_WORLD_STATE_VARIABLES.md` § 9. It writes no variable.

Endings are computed in this order:

1. determine Elias medical outcome;
2. determine ledger and transfer outcome;
3. determine rescue controller;
4. determine proof status against Rook;
5. determine proof status against Krell and Vale;
6. resolve public accusation;
7. resolve secondary character consequences;
8. select narrative ending family and modifiers.

## 2. Medical outcome

The medical outcome is read from `ELIAS_STATE`, owned by `01_WORLD_STATE_VARIABLES.md` § 5. It is not stored separately and is not inferred from prose. The seven values map onto the three outcome bands exhaustively.

| `ELIAS_STATE` | Outcome band |
|---|---|
| `SURVIVED` | High survival state |
| `IN_SURGERY` | High survival state, pending |
| `EVACUATING` | Conditional survival state |
| `CRITICAL_RESPONSIVE` | Conditional survival state, if evacuation is still reachable |
| `CRITICAL_CONFUSED` | Conditional survival state, if evacuation is still reachable |
| `CRITICAL_UNRESPONSIVE` | Conditional survival state, degraded |
| `DIED` | Death state |

### High survival state

Requires:

- evacuation initiated before or near 01:15;
- route reaches definitive care;
- no hostile interception that causes major delay.

### Conditional survival state

Late evacuation or compromised route.

### Death state

No effective evacuation, fatal delay, or hostile control preventing treatment.

The final text must never imply that Iris's field treatment alone cured the injury.

## 3. Evidence outcome

### Full authenticated transfer

Requires:

- primary key;
- complete recovery code;
- accessible upload route;
- sufficient time;
- transfer not successfully intercepted;
- preserved authentication.

### Partial official evidence

One or more of:

- incomplete archive;
- missing code;
- late upload;
- decoy contamination detected after transfer.

### Public leak

Evidence released without full verification or through Nadia's emergency publication route.

### Evidence lost

Primary key seized/destroyed and no adequate external copy.

## 4. Rook proof outcome

### Operationally exposed

Players know and can act on corruption, but public proof is incomplete.

### Publicly exposed

Requires `CON_ROOK_PUBLICLY_PROVABLE` and preserved evidence.

### Unexposed

Suspicion exists without sufficient authenticated support.

## 5. Accusation gates

### Rook

Public prosecution-style accusation appears only when public-proof threshold is met.

### Krell/Vale

Requires full ledger or multiple authenticated financial/contact routes.

### Marcus

Requires provable leak threshold. Even then, the ending must distinguish betrayal from masterminding the full scheme.

### Reed

Requires presence and confrontation proof. The ending must distinguish unlawful coercion from intentional murder.

### Lena/Nadia

Players may accuse them of obstruction or reckless conduct if supported, but not as sole architect of the corruption scheme without contradictory failure text.

## 6. Ending families

### `END_WITNESS_SPEAKS`

- Elias survives;
- full transfer;
- Rook exposed before rescue control;
- broader conspiracy sufficiently proven.

### `END_EVIDENCE_WITHOUT_WITNESS`

- Elias dies or cannot testify;
- full authenticated transfer succeeds.

### `END_LIFE_SAVED_TRUTH_DELAYED`

- Elias survives;
- full transfer fails;
- primary evidence or testimony potential remains.

### `END_PROTECTIVE_CUSTODY`

- Rook controls rescue/evidence;
- Rook not sufficiently exposed;
- evidence is seized, lost, or manipulated.

### `END_PUBLIC_LEAK`

- public disclosure occurs without full official authentication.

### `END_SILENT_TERMINAL`

- Elias not found or not rescued in time.

### `END_WRONG_ACCUSATION`

- players make a public unsupported or contradicted accusation;
- target-specific rebuttal resolves why it fails.

### `END_FRACTURED_TRUTH`

- player actions split rescue and evidence outcomes in incompatible ways.

## 7. Target-specific wrong-accusation logic

No generic “case dismissed” ending.

The compiler must select a rebuttal based on missing proof:

- wrong timeline;
- missing physical presence;
- inability to explain police manipulation;
- inability to explain financial architecture;
- evidence showing protective rather than initiating conduct;
- confession scope smaller than accusation scope.

## 8. Partial-success modifiers

Possible modifiers:

- Marcus confesses publicly;
- Reed cooperates;
- Mina preserves official records;
- Lena avoids arrest;
- Iris faces disciplinary consequences;
- Nadia publishes responsibly or recklessly;
- Vale escapes immediate arrest;
- Krell flees but assets are frozen.

These modifiers enrich the epilogue without replacing the main ending family.

---

## 9. Identifier status

This document owns the `END_` namespace and is the authoritative owner of ending trigger conditions. Every `END_` identifier declared here carries exactly one status, derived from reference count.

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 1 | `END_PROTECTIVE_CUSTODY`, referenced from `05_CORE_EVENT_GRAPH.md` § `ARC_400`. |
| `DEFINITION_ONLY` | 7 | `END_WITNESS_SPEAKS`, `END_EVIDENCE_WITHOUT_WITNESS`, `END_LIFE_SAVED_TRUTH_DELAYED`, `END_PUBLIC_LEAK`, `END_SILENT_TERMINAL`, `END_WRONG_ACCUSATION`, `END_FRACTURED_TRUTH`. |

No ending identifier is `RESERVED` or `DEPRECATED`. Node identity for these families is not yet assigned; it is owned by `10_INVESTIGATION_NODE_GRAPH.md`.

`CON_ROOK_PUBLICLY_PROVABLE`, referenced in § 4, is declared and status-carried in `00_ENTITY_KEY_TABLE.md`.

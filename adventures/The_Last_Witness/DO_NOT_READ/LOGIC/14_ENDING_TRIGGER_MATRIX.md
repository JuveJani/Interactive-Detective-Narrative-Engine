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

### Ending-family priority order

The trigger conditions in § 6 overlap by construction, so exclusivity is unavailable. `END_SILENT_TERMINAL` and `END_EVIDENCE_WITHOUT_WITNESS` can both hold when Elias dies; `END_PUBLIC_LEAK` can hold alongside `END_LIFE_SAVED_TRUTH_DELAYED`; `END_WRONG_ACCUSATION` is a player act independent of rescue and transfer. A deterministic priority order resolves this.

Families are tested top to bottom. The order follows the eight-step resolution order above: medical outcome, then transfer, then rescue controller, then proof, then accusation.

| Rank | Family | Terminal node | Determination it belongs to |
|---:|---|---|---|
| 1 | `END_SILENT_TERMINAL` | `EVT_906` | medical: Elias never located or never rescued |
| 2 | `END_EVIDENCE_WITHOUT_WITNESS` | `EVT_902` | medical and transfer: Elias lost, archive authenticated |
| 3 | `END_FRACTURED_TRUTH` | `EVT_908` | rescue and evidence outcomes incompatible |
| 4 | `END_PROTECTIVE_CUSTODY` | `EVT_904` | rescue controller: Rook holds rescue or evidence, unexposed |
| 5 | `END_WITNESS_SPEAKS` | `EVT_901` | proof: full success on every axis |
| 6 | `END_LIFE_SAVED_TRUTH_DELAYED` | `EVT_903` | transfer: Elias survives, full transfer failed |
| 7 | `END_WRONG_ACCUSATION` | `EVT_907` | accusation: public claim unsupported or contradicted |
| 8 | `END_PUBLIC_LEAK` | `EVT_905` | disclosure without full authentication |

**Selection rule.** Ending families are tested in the priority order above. The first family whose conditions are satisfied is the ending. Any other family whose conditions were also satisfied is recorded as a partial-success modifier under § 8, never as a second ending. Every reachable combination therefore resolves to exactly one ending.

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
- the passphrase itself, by Route B of `CON_PASSPHRASE_ACCESS`;
- complete recovery code;
- accessible upload route;
- sufficient time;
- transfer not successfully intercepted;
- preserved authentication.

Route A of `CON_PASSPHRASE_ACCESS` cannot reach this outcome. The reset it performs is logged, which downgrades authentication.

### Partial official evidence

One or more of:

- incomplete archive;
- missing code;
- late upload;
- decoy contamination detected after transfer;
- archive opened through Route A of `CON_PASSPHRASE_ACCESS`, whose logged reset downgrades authentication.

### Public leak

Evidence released without full verification or through Nadia's emergency publication route.

### Evidence lost

Primary key seized/destroyed and no adequate external copy, or neither route of `CON_PASSPHRASE_ACCESS` obtained so the archive never opens.

## 4. Rook proof outcome

### Operationally exposed

`CON_ROOK_OPERATIONALLY_COMPROMISED` holds. Players know and can act on corruption, but public proof is incomplete.

### Publicly exposed

Requires `CON_ROOK_PUBLICLY_PROVABLE` and preserved evidence.

### Unexposed

Neither Rook conclusion holds. Suspicion exists without sufficient authenticated support.

Every outcome in this section is read from a conclusion, never from a raw point total.

## 5. Accusation gates

### Rook

Requires `CON_ROOK_PUBLICLY_PROVABLE`. The public prosecution-style accusation option appears only when that conclusion holds.

### Krell/Vale

Requires `FULL_LEDGER_TRANSFERRED`, or multiple authenticated financial and contact routes.

### Marcus

Requires `CON_MARCUS_LEAK_PROVABLE`. Even then, the ending must distinguish betrayal from masterminding the full scheme.

### Reed

Requires `CON_REED_CAUSED_CONFRONTATION`. The ending must distinguish unlawful coercion from intentional murder.

### Lena/Nadia

Players may accuse them of obstruction or reckless conduct if supported, but not as sole architect of the corruption scheme without contradictory failure text. `CON_LENA_PROTECTING` is the conclusion that contradicts a sole-architect claim against Lena.

Every gate in this section reads a conclusion, never a raw point total.

## 6. Ending families

### `END_WITNESS_SPEAKS`

**Terminal node:** `EVT_901_END_WITNESS_SPEAKS` — **Terminal type:** `VICTORY`

- Elias survives;
- full transfer;
- Rook exposed before rescue control;
- broader conspiracy sufficiently proven.

### `END_EVIDENCE_WITHOUT_WITNESS`

**Terminal node:** `EVT_902_END_EVIDENCE_WITHOUT_WITNESS` — **Terminal type:** `PARTIAL_SUCCESS`

- Elias dies or cannot testify;
- full authenticated transfer succeeds.

### `END_LIFE_SAVED_TRUTH_DELAYED`

**Terminal node:** `EVT_903_END_LIFE_SAVED_TRUTH_DELAYED` — **Terminal type:** `PARTIAL_SUCCESS`

- Elias survives;
- full transfer fails;
- primary evidence or testimony potential remains.

### `END_PROTECTIVE_CUSTODY`

**Terminal node:** `EVT_904_END_PROTECTIVE_CUSTODY` — **Terminal type:** `NARRATIVE_FAILURE`

- Rook controls rescue/evidence;
- Rook not sufficiently exposed;
- evidence is seized, lost, or manipulated.

### `END_PUBLIC_LEAK`

**Terminal node:** `EVT_905_END_PUBLIC_LEAK` — **Terminal type:** `PARTIAL_SUCCESS`

- public disclosure occurs without full official authentication.

### `END_SILENT_TERMINAL`

**Terminal node:** `EVT_906_END_SILENT_TERMINAL` — **Terminal type:** `TIME_EXPIRED`

- Elias not found or not rescued in time.

### `END_WRONG_ACCUSATION`

**Terminal node:** `EVT_907_END_WRONG_ACCUSATION` — **Terminal type:** `CASE_UNRESOLVED`

- players make a public unsupported or contradicted accusation;
- target-specific rebuttal resolves why it fails.

### `END_FRACTURED_TRUTH`

**Terminal node:** `EVT_908_END_FRACTURED_TRUTH` — **Terminal type:** `PARTIAL_SUCCESS`

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

### Accusation target → rebuttal category mapping

Authoritative wiring for `EVT_440_FINAL_PUBLIC_POSITION` accusation options. When an accusation is unsupported or contradicted, `EVAL_ENDING` selects the rebuttal category from this table for `EVT_907_END_WRONG_ACCUSATION` variant dispatch.

| Accusation target | Primary rebuttal category | Secondary category (if applicable) | Source |
|---|---|---|---|
| `NPC_ROOK` | missing physical presence | inability to explain police manipulation | `07` § 3; `CONTENT_GENERATION_SPEC.md` § 6.5 |
| `NPC_KRELL`, `NPC_VALE` | inability to explain financial architecture | — | `07` § 3; `14` § 5 |
| `NPC_MARCUS` | inability to explain police manipulation | confession scope smaller than accusation scope | `07` § 3 |
| `NPC_REED` | confession scope smaller than accusation scope | inability to explain financial architecture | `07` § 3 |
| `NPC_LENA` | evidence showing protective rather than initiating conduct | — | `07` § 3; `14` § 5 |
| `NPC_NADIA` | evidence showing protective rather than initiating conduct | wrong timeline | `07` § 3; `14` § 5 |
| unsupported / arbitrary | wrong timeline | — | `05_CORE_EVENT_GRAPH.md` `ARC_440` |

Per-target rebuttal facts remain owned by `07_EVIDENCE_VALIDATION.md` § 3. Rebuttal prose is not authored in this milestone.

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
| `ACTIVE` | 8 | `END_WITNESS_SPEAKS` (`EVT_901`), `END_EVIDENCE_WITHOUT_WITNESS` (`EVT_902`), `END_LIFE_SAVED_TRUTH_DELAYED` (`EVT_903`), `END_PROTECTIVE_CUSTODY` (`EVT_904`), `END_PUBLIC_LEAK` (`EVT_905`), `END_SILENT_TERMINAL` (`EVT_906`), `END_WRONG_ACCUSATION` (`EVT_907`), `END_FRACTURED_TRUTH` (`EVT_908`). |

No ending identifier is `DEFINITION_ONLY`, `RESERVED` or `DEPRECATED`. Terminal node identity is owned by `10_INVESTIGATION_NODE_GRAPH.md` § 14; each `END_*` family is referenced from at least one terminal node and from `EVT_900_RESOLVE_ENDING`.

`CON_ROOK_PUBLICLY_PROVABLE`, referenced in § 4, is declared and status-carried in `00_ENTITY_KEY_TABLE.md`.

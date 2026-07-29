# DO NOT READ: Check Register

## 1. Purpose

This document owns the `CHK_*` namespace. Each record binds a referenced skill check to its parent `EVT_*` node, pass/fail outcomes, and variant keys already declared in `10_INVESTIGATION_NODE_GRAPH.md`.

Checks only select between existing branches. They do not create new routes, clues, endings, or gameplay content.

Required fields per `ENGINE_READINESS_PLAN.md` ER-02 and `BOOK_COMPILER_SPEC.md` MS-04: skill, DC, pass outcome, fail outcome, fallback route.

## 2. Resolution procedure (MBD-01)

Alpha 0.2c uses a simple D20 system.

### Roll

```text
roll = d20 + character_modifier
```

- `d20`: one twenty-sided die roll.
- `character_modifier`: skill modifier printed on the player character sheet for the listed skill.

### Success

```text
success when roll >= dc
```

### Multiple eligible players

When the story allows more than one player to attempt the same check, every eligible player rolls. The **highest successful result** determines the outcome. If no player succeeds, the check fails.

### Difficulty bands

| Band | DC | Use |
|---|---:|---|
| Easy | 5 | Low-friction observation or routine interaction |
| Medium | 10 | Standard investigative challenge |
| Hard | 15 | High-stakes or expert-level challenge |

Adventure authors assign one band per `CHK_*` record. The compiler emits the resolved DC value.

### Supported skills (engine taxonomy)

The engine must support these check types at minimum:

| Skill | Notes |
|---|---|
| Perception | Sensory observation, environmental detail |
| Investigation | Deliberate search, pattern analysis |
| Persuasion | Negotiation, rapport, social leverage |
| Intimidation | Pressure, threats, dominance |
| Stealth | Concealment, quiet movement |
| Technology | Digital systems, devices, metadata |
| Medicine | Clinical interpretation, triage |
| Athletics | Physical exertion, climbing, forcing |

The first prototype uses only the skills bound to authored `CHK_*` records below.

### Character modifiers

Modifiers are defined on the player character sheet, not in this register. The compiler references the skill name; the character sheet supplies the numeric modifier at play time.

## 3. Referenced checks inventory

| Reference | Parent `EVT_*` | Logic source | Formalizable as `CHK_*`? |
|---|---|---|---|
| Perception check | `EVT_115_SERVICE_CORRIDOR` | `10` **Failure transformation**; `perception_success` / `perception_failure` variants | **Yes** — `CHK_115_PERCEPTION` |
| Careful vs failed/rushed search | `EVT_113_APARTMENT_SEARCH` | `10` **Information routes**; six `careful_*` / `rushed_*` variants | **No** — pace choice, not a D20 roll |
| Technical check (implied) | `EVT_123_NEWSROOM_RECORDS` | `10` **Failure transformation** ("without a technical check") | **No** — observational bypass path; no `CHK_*` binding |
| Regroup Two "knowledge check" | `EVT_300_REGROUP_TWO` | `13_SPLIT_AND_REGROUP_FLOW.md` § 6 | **No** — planning checklist, not a player roll |
| Routine check (Rook) | narrative only | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | **No** — narrative constraint, not a formal check |

## 4. `CHK_*` records

### `CHK_115_PERCEPTION`

| Field | Value |
|---|---|
| `check_id` | `CHK_115_PERCEPTION` |
| `parent_evt` | `EVT_115_SERVICE_CORRIDOR` |
| `skill` | Perception |
| `dc_band` | Medium |
| `dc` | 10 |
| `pass_variant_key` | `perception_success` |
| `fail_variant_key` | `perception_failure` |
| `pass_effects` | `GRANT_CLUE(CLUE_APT_SERVICE_LATCH)` including fibre trace |
| `fail_effects` | corridor route known; latch direction confirmable later via Mina; no fibre trace |
| `fallback_route` | same node (`EVT_115`); Mina confirms latch direction later |
| `time_cost_minutes` | 15 (node default) |
| `eligible_players` | any player occupying the apartment-cluster role during Split One |

**Compilation status:** **ACTIVE** — all required fields declared.

Cross-reference: `EVT_115` **Failure transformation** → `CHK_115_PERCEPTION`.

No other `CHK_*` record is required for Alpha 0.2c logic.

## 5. Identifier status

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 1 | `CHK_115_PERCEPTION` |

No `CHK_*` identifier is `DEFINITION_ONLY`, `RESERVED`, `DEPRECATED`, or `BLOCKED`.

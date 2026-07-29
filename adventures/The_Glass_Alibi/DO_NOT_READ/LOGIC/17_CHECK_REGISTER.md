# DO NOT READ: Check Register

## 1. Purpose

This document owns the `CHK_*` namespace. Each record binds a referenced skill check to its parent `EVT_*` node, pass/fail outcomes, and variant keys declared in `10_INVESTIGATION_NODE_GRAPH.md`.

Checks only select between existing branches. They do not create new routes, clues, endings, or gameplay content.

Required fields: skill, DC band, pass outcome, fail outcome, fallback route.

---

## 2. Resolution procedure (MBD-01)

Alpha 0.2 uses a simple D20 system.

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

| Skill | Notes |
|---|---|
| Perception | Sensory observation, environmental detail |
| Investigation | Deliberate search, pattern analysis |
| Persuasion | Negotiation, rapport, social leverage |
| Technology | Digital systems, devices, metadata |
| Athletics | Physical exertion, climbing, forcing |

The first prototype uses only the skills bound to authored `CHK_*` records below.

Character modifiers are defined on the player character sheet, not in this register.

---

## 3. Referenced checks inventory

| Reference | Parent `EVT_*` | Logic source | Formalized as `CHK_*`? |
|---|---|---|---|
| Sensor spoof visibility | `EVT_115` | `10` **Failure transformation**; `perception_success` / `perception_failure` variants | **Yes** — `CHK_115_PERCEPTION` |
| SCADA metadata depth | `EVT_123` | `10` **Failure transformation**; `technology_success` / `technology_failure` variants | **Yes** — `CHK_123_TECHNOLOGY` |
| Finance ledger deep search | `EVT_210` | `10` **Information routes**; `investigation_success` / `investigation_failure` variants | **Yes** — `CHK_210_INVESTIGATION` |
| Sable/Kevin Stage 1 acceleration | `EVT_240` | `10` **Failure transformation**; `persuasion_success` / `persuasion_failure` variants | **Yes** — `CHK_240_PERSUASION` |
| Maintenance cable-tray access | `EVT_312` | `10` **Failure transformation**; `athletics_success` / `athletics_failure` variants | **Yes** — `CHK_312_ATHLETICS` |
| Regroup Two planning checklist | `EVT_300` | `13_SPLIT_AND_REGROUP_FLOW.md` § 6 | **No** — planning checklist, not a player roll |
| Tom nervous read | narrative only | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | **No** — narrative constraint |

---

## 4. `CHK_*` records

### `CHK_115_PERCEPTION`

| Field | Value |
|---|---|
| `check_id` | `CHK_115_PERCEPTION` |
| `parent_evt` | `EVT_115` |
| `skill` | Perception |
| `dc_band` | Medium |
| `dc` | 10 |
| `pass_variant_key` | `perception_success` |
| `fail_variant_key` | `perception_failure` |
| `pass_effects` | `GRANT_CLUE(CLUE_SENSOR_SPOOF_TRACE)`; fibre-residue detail on spoof fragment |
| `fail_effects` | CO₂ anomaly still granted; spoof fragment noted as "possible tamper" without trace ID |
| `fallback_route` | same node (`EVT_115`); Kevin flatline export at `EVT_220` confirms spoof |
| `time_cost_minutes` | 25 (deep forensic search default) |
| `eligible_players` | any player occupying the tech/SCADA narrative role during Split One |

**Compilation status:** **ACTIVE**

---

### `CHK_123_TECHNOLOGY`

| Field | Value |
|---|---|
| `check_id` | `CHK_123_TECHNOLOGY` |
| `parent_evt` | `EVT_123` |
| `skill` | Technology |
| `dc_band` | Medium |
| `dc` | 10 |
| `pass_variant_key` | `technology_success` |
| `fail_variant_key` | `technology_failure` |
| `pass_effects` | `GRANT_CLUE(CLUE_PURGE_MANUAL_OVERRIDE)`; `GRANT_CLUE(CLUE_CO2_OVERRIDE_AUTH)`; full override token metadata |
| `fail_effects` | partial purge flag visible; Kevin Stage 1 still reachable; override auth requires `EVT_220` |
| `fallback_route` | `EVT_220` Kevin historian export after any murder clue |
| `time_cost_minutes` | 20 |
| `eligible_players` | any player occupying the tech/SCADA narrative role during Split One |

**Compilation status:** **ACTIVE**

---

### `CHK_210_INVESTIGATION`

| Field | Value |
|---|---|
| `check_id` | `CHK_210_INVESTIGATION` |
| `parent_evt` | `EVT_210` |
| `skill` | Investigation |
| `dc_band` | Hard |
| `dc` | 15 |
| `pass_variant_key` | `investigation_success` |
| `fail_variant_key` | `investigation_failure` |
| `pass_effects` | `GRANT_CLUE(CLUE_FINANCE_DISCREPANCY)`; shell vendor names surfaced immediately |
| `fail_effects` | summary discrepancy only; full ledger requires `EVT_260` audit window or Elena memo |
| `fallback_route` | `EVT_260` evening audit window; `EVT_271` Priya email thread |
| `time_cost_minutes` | 30 |
| `eligible_players` | any player on the finance-track narrative role during Split Two |

**Compilation status:** **ACTIVE**

---

### `CHK_240_PERSUASION`

| Field | Value |
|---|---|
| `check_id` | `CHK_240_PERSUASION` |
| `parent_evt` | `EVT_240` |
| `skill` | Persuasion |
| `dc_band` | Medium |
| `dc` | 10 |
| `pass_variant_key` | `persuasion_success` |
| `fail_variant_key` | `persuasion_failure` |
| `pass_effects` | `T_SABLE +1` or `T_KEVIN +1` (player choice of witness); accelerates Stage 1 disclosure |
| `fail_effects` | witness remains Stage 0; procedural proof or credential clue still unlocks Stage 1 |
| `fallback_route` | `EVT_141` badge mismatch shown to Sable; murder clue shown to Kevin |
| `time_cost_minutes` | 10 |
| `eligible_players` | either player during Split Two witness-preservation track |

**Compilation status:** **ACTIVE**

---

### `CHK_312_ATHLETICS`

| Field | Value |
|---|---|
| `check_id` | `CHK_312_ATHLETICS` |
| `parent_evt` | `EVT_312` |
| `skill` | Athletics |
| `dc_band` | Medium |
| `dc` | 10 |
| `pass_variant_key` | `athletics_success` |
| `fail_variant_key` | `athletics_failure` |
| `pass_effects` | `GRANT_CLUE(CLUE_BADGE_CLONE_DEVICE)`; cable-tray adjacency path to tool crib void |
| `fail_effects` | Tom-assisted authorized search available (+15 min); clone findable without athletics |
| `fallback_route` | same node with Tom present; badge-audit cross-reference at `EVT_141` |
| `time_cost_minutes` | 15 |
| `eligible_players` | any player on the field/credential narrative role during Split Three |

**Compilation status:** **ACTIVE**

---

## 5. Identifier status

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 5 | `CHK_115_PERCEPTION`, `CHK_123_TECHNOLOGY`, `CHK_210_INVESTIGATION`, `CHK_240_PERSUASION`, `CHK_312_ATHLETICS` |

No `CHK_*` identifier is `DEFINITION_ONLY`, `RESERVED`, `DEPRECATED`, or `BLOCKED`. Inventory matches `00_ENTITY_KEY_TABLE.md` § Check inventory.

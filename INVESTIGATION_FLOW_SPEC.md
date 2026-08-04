# Investigation Flow — Normative Specification

**Milestone:** 5C — Investigation Flow & Ending System  
**Status:** Normative  
**Companion:** `ENDING_SYSTEM_SPEC.md`  
**Validation:** `python3 -m idne.investigation_flow_validate`

---

## 1. Purpose

Replace legacy **ending-condition tables** with a **state-driven investigation flow** model. Adventure progression is governed by declared state, time, knowledge held, and player actions — not static lookup tables.

**Uses existing systems:** Investigation Core (knowledge, conclusions, proofs), Environment (locations), Object Interaction and NPC Investigation (referenced via state and knowledge gates). **Does not redesign** those layers.

**Out of scope:** Adventure generation, Harborview migration, Delivery Adapter prose, capability check rewrite.

---

## 2. Layer position

Investigation Core → NPC Investigation (optional) → **Investigation Flow Package** → Adventure Logic → Delivery.

Investigation Flow owns **how play advances** and **when endings evaluate**. Investigation Core owns **what can be proved**. Ending prose is Delivery; **triggers and truth-reveal policy** are Flow.

---

## 3. State model

`state_model` declares machine state variables:

| Kind | Use |
|---|---|
| `flags` | Boolean adventure state (e.g. `office_searched`, `accusation_complete`) |
| `counters` | Numeric phase counters |
| `initial_state` | Values at case start |

All `required_state`, `state_updates`, and variant `when_state` references MUST use declared flags/counters.

**MUST NOT** invent state at delivery time.

---

## 4. Time model

`time_model` declares investigation clocks (`T0`, `T1`, …) and optional `deadline_clock`.

Supports:

- **Time-dependent scene chains** — chains active only between `active_from_clock` and `active_until_clock`
- **Deadline pressure** — see `ENDING_SYSTEM_SPEC.md` §4

`scene_time_cost_default_minutes` documents default cost per scene step (Adventure Logic applies).

---

## 5. Scene chains

`scene_chains` define ordered investigation beats gated by time and state:

```json
{
  "chain_id": "CHAIN-MORNING",
  "active_from_clock": "T0",
  "active_until_clock": "T1",
  "steps": [
    { "step_id": "SC-001", "scene_unit_id": "J-101", "requires_state": { "ready_to_accuse": false } },
    { "step_id": "SC-002", "scene_unit_id": "J-102", "requires_knowledge_ids": ["KNOW-001"], "allows_prior_acquisition": true }
  ]
}
```

Steps MAY require knowledge IDs from Investigation Core. First-step knowledge requirements MUST be obtainable on fair paths (`allows_prior_acquisition` or pre-case grants).

---

## 6. World-state scene variants

`world_state_variants` swap scene units for the same narrative slot based on state:

```json
{
  "variant_id": "VAR-LOBBY",
  "base_scene_unit_id": "J-100",
  "variants": [
    { "when_state": { "flag": "basement_open", "value": true }, "scene_unit_id": "J-100B" },
    { "when_state": { "flag": "basement_open", "value": false }, "scene_unit_id": "J-100A" }
  ]
}
```

Replaces implicit “if clue then different paragraph” tables with explicit state-driven variants.

---

## 7. Dynamic location revisits

`location_revisits` declare how returning to a location changes available content:

```json
{
  "location_id": "LOC-OFFICE",
  "revisit_rules": [
    {
      "rule_id": "REV-001",
      "when_knowledge_held": ["KNOW-002"],
      "unlocks_scene_unit_id": "J-201",
      "state_updates": { "office_searched": true }
    }
  ]
}
```

`location_id` MUST exist in linked Environment package when environment link is present.

---

## 8. Flow states

`flow_states` document high-level investigation phases (e.g. `FLOW-ACTIVE`, `FLOW-ACCUSATION`). Used by `ending_graph` edges and Adventure Logic transitions.

---

## 9. Links to upstream packages

```json
{
  "investigation_core_links": { "package_path": "DO_NOT_READ/investigation_core_package.json" },
  "environment_links": { "package_path": "DO_NOT_READ/environment_package.json" }
}
```

Knowledge, conclusion, and proof validation cross-checks use Investigation Core. Location validation uses Environment.

---

## 10. Declaration

`investigation_flow_manifest.json`:

```json
{
  "schema_version": "1.0",
  "investigation_flow_method": "canonical",
  "package_path": "DO_NOT_READ/investigation_flow_package.json"
}
```

Validator: `python3 -m idne.investigation_flow_validate <adventure_root>`

Legacy adventures without manifest: **SKIP**.

---

## 11. Design constraints

- **MUST NOT** replace Investigation Core proof graphs.
- **MUST NOT** replace NPC trust or conversation models.
- **MUST** drive ending evaluation from state + knowledge + accusation, not static END_* tables alone.
- Scene and revisit rules MUST be consistent with declared `state_model`.

---

## 12. Out of scope

Ending player wording, book layout, adventure generation, capability checks, inventory, retries.

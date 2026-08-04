# Object Interaction System — Normative Specification

**Milestone:** 4  
**Status:** Normative  
**Aligned with:** `ENVIRONMENT_SYSTEM_SPEC.md`, `WORLD_FIRST_GENERATION_SPEC.md`, `IDNE_ENGINE_v0.4.md`  
**Validation:** `python3 -m idne.object_interaction_validate`

---

## 1. Purpose

Players interact with **persistent world objects** instead of receiving clues directly from scenes.

Objects and hidden contents exist independently of check success. Checks determine perception, access, and understanding — never whether evidence exists.

**Mode-independent:** `single_investigator` and `two_player`.  
**Adapter-compatible:** static book/PDF and future AI-DM.

**Out of scope:** full Inventory System, retry mechanics, false checks, investigation/conclusion rewrite.

---

## 2. Fixed object truth

| Rule | Meaning |
|---|---|
| Object exists | Before any player action |
| Hidden content exists | Before successful perception |
| Failed check | Does not remove object; does not reveal what was missed |
| Document contents | Fixed; check does not author text |

---

## 3. Progressive interaction depth

Layers (do not collapse to generic “inspect”):

`known` → `visible` → `approached` → `examined` → `searched` → `hidden_detail_discovered` → `container_opened` → `content_accessed` → `information_interpreted`

Information granted only from layers actually accessed.

---

## 4. Player-directed actions

`player_label` MUST describe the action (Examine the desk. Try to open the cabinet.).

**MUST NOT** expose bare IDs (J-223, OBJ-14) in player-facing labels.

---

## 5. Separate result units

Check/decision units state: action, cost, condition, check+DC, success destination, failure destination.

**MUST NOT** reveal success or failure content in the same unit.

Only success destination may reveal hidden key; failure must not hint missed content.

---

## 6. Capability-check binding

| Field | Required |
|---|---|
| `check_id`, `capability`, `dc`, `eligible_character` | yes |
| `one_attempt` | default true |
| `success_destination`, `failure_destination` | separate units |
| `changes_world_truth` | MUST be false |
| `creates_evidence` | MUST be false |
| `determines_document_contents` | MUST be false |

---

## 7. One-attempt default

Record: `not_attempted` | `succeeded` | `failed`. No free re-roll in Milestone 4. Schema reserves `repeat_policy` for later milestones.

---

## 8. Object state

Adventure-defined states with explicit transitions: `cause`, `from_state`, `to_state`, `persists_on_revisit`, provenance.

---

## 9. Inventory references (not full system)

Actions MAY declare: `requires item`, `consumes item` — item IDs in `items_registry`. No capacity/transfer rules yet.

---

## 10. Time cost

Each action MAY declare `time_cost_minutes`. `cost_applied_once: true` — return navigation does not re-apply cost.

---

## 11. Return navigation

Result units and actions define `return_destination`. Revisit preserves discovered info, object state, check attempts, elapsed time.

---

## 12. Information boundaries

Player knowledge gains only from valid completed interactions. Environment description alone does not grant hidden object information.

---

## 13. Neutral presentation

No spotlight on solution-critical objects (Philosophy A2, U9).

---

## 14. Canonical object model

See `OBJECT_INTERACTION_SYSTEM_SCHEMA.md` for fields: object ID, parent, states, actions, check bindings, result units, transitions, provenance.

---

## 15. Declaration

`object_interaction_manifest.json`:

```json
{
  "schema_version": "1.0",
  "object_interaction_method": "canonical",
  "package_path": "DO_NOT_READ/object_interaction_package.json"
}
```

Legacy adventures without manifest: validator `SKIP`.

---

## 16. Layer stack

World Truth → Environment (locations) → **Object Interaction** → Adventure Logic → Delivery.

Objects bind to `location_id` or parent `object_id` from environment package.

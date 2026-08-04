# Environment System — Normative Specification

**Document type:** Engine companion (Milestone 3)  
**Status:** Normative for canonical environment adventures  
**Aligned with:** `IDNE_ENGINE_v0.4.md` §3, §7; `WORLD_FIRST_GENERATION_SPEC.md`; `SINGLE_INVESTIGATOR_MODE_SPEC.md`  
**Schema:** `ENVIRONMENT_SYSTEM_SCHEMA.md`  
**Validation:** `python3 -m idne.environment_validate`

---

## 1. Purpose

The Environment System represents **locations as persistent, stateful, explorable spaces** — not linear story scenes.

A location exists independently of whether the player visits it. World state, access, features, and navigation are authored in a **canonical environment model**; delivery scenes only **present** that model.

**Mode-independent:** same semantics for `single_investigator` and `two_player`.  
**Adapter-compatible:** static book and future AI-DM adapters consume the same package.

**Out of scope (Milestone 4):** detailed object interactions, inventory mechanics, check redesign.

---

## 2. Core principle

A player-facing location is structured data containing:

| Element | Owned by environment package |
|---|---|
| Location identity | ID, name, parent, type, provenance |
| Current world state | Variants, attributes, causes |
| Environmental features | Presence, visibility, broad state |
| People present | Via world-state timeline linkage |
| Object references | Feature IDs only — no actions yet |
| Entrances / exits | Navigation records |
| Movement destinations | Diegetic `player_label` + hidden IDs |
| Access conditions | Canonical basis required |
| Time-dependent changes | Clock/event-triggered variants |
| Action-dependent changes | Cause type `player_action` (declared, not implemented) |
| Passive information | Visibility layers without deep interaction |

---

## 3. Location identity

Every location MUST have:

| Field | Requirement |
|---|---|
| `location_id` | Stable canonical ID |
| `public_name` | Player-recognizable name |
| `parent_location_id` | Physical or logical parent (null for root) |
| `location_type` | Adventure-defined (not engine enum) |
| `description_source` | ID for delivery text source |
| `world_first_provenance` | Link to Fixed Truth / timeline |
| `state_owner` | MUST be `environment_package` |

Locations MUST NOT be invented at delivery time.

---

## 4. Location states

States change by:

- world time (`active_from_clock`, `trigger_event_id`)
- timeline events (`cause.type: timeline_event`)
- player actions (declared cause only — execution Milestone 4+)
- NPC actions
- access changes
- physical alteration

Each `location_state` MUST include:

- `state_id`, `location_id`, `variant_label`
- `attributes` — adventure-defined key/value (open/closed, lit/dark, etc.)
- `cause` — explicit type + ref

**MUST NOT** use universal engine constants for adventure-specific states.

---

## 5. Environmental visibility layers

| Layer | Meaning |
|---|---|
| `known_remotely` | Learnable without being present |
| `on_arrival` | Visible when entering location area |
| `after_entering` | Visible inside location |
| `approach_feature` | Visible when moving toward feature |
| `hidden_until_interaction` | Not player-visible until interaction (Milestone 4 executes) |

Milestone 3 defines layers and ownership. Features MAY reveal existence without full detail.

Delivery MUST NOT expose `hidden_until_interaction` features in PLAYER before interaction.

---

## 6. Environment features

Features (furniture, doors, documents, traces, people-as-feature refs) MUST have:

- `feature_id`, `location_id` binding
- `visibility`, `broad_state`
- `has_further_interaction` (boolean — actions deferred to Milestone 4)

**MUST NOT** define detailed feature actions in Milestone 3.

---

## 7. Navigation

Every movement option MUST use a **diegetic** `player_label`:

| Correct | Incorrect |
|---|---|
| Enter the manager's office. | Go to J-223. |
| Return to the corridor. | Choose scene R-212b. |

Internal IDs (`hidden_destination_id`, `nav_id`) are delivery metadata only.

Navigation records MUST define:

- `source_location_id`, `destination_location_id`
- `travel_cost_minutes` (optional)
- `access_condition`
- `return_nav_id` or `one_way_justification`
- Resulting location state (via destination's active variant)

---

## 8. Free authored exploration

Within the bounded authored graph, players choose among **currently legal** locations and visible features.

**MUST NOT** force fixed location order unless world state or physical access requires it.

Static media remain bounded — only authored destinations and actions.

---

## 9. Persistence and revisits

`revisit_rules` MUST declare:

| Rule | Default intent |
|---|---|
| `persist_physical_changes` | Damage, moved objects stay |
| `persist_acquired_objects` | Taken items stay taken |
| `persist_open_access` | Open doors stay open until changed |
| `suppress_repeat_one_time_observations` | No auto-repeat first look |
| `allow_time_variants` | Clock may change location variant |
| `reset_to_initial_on_revisit` | MUST be false when persist flags true |

**MUST NOT** silently reset location text/state on return.

---

## 10. World-First linkage

Every location, feature, access rule, and state transition MUST trace to:

- Fixed Truth / Causal Timeline / World-State Timeline (via `world_first_provenance`)
- or explicit `player_action` / `npc_action` cause
- or `explicit_adventure_extension` for container locations (documented)

**MUST NOT** add features because a later scene needs them.

Link via `world_first_links.truth_package_path` in environment package.

---

## 11. Information boundaries

PLAYER environment text MUST NOT reveal:

- hidden object presence
- failed-check content
- unseen evidence
- future state changes
- narrative importance
- investigative priorities

Descriptions use **neutral language**. No stylistic spotlight on solution-critical features (Philosophy A2, U9).

---

## 12. Scene relationship

A delivery scene/public unit MAY represent:

- arrival at a location
- a location-state variant
- approaching a visible feature
- leaving / travelling

**MUST NOT** invent environment state. Canonical package owns physical reality; delivery presents it.

Scene `asserted_fact_ids` in World-First narrative layer MUST align with environment state.

---

## 13. Declaration

`environment_manifest.json` at adventure root:

```json
{
  "schema_version": "1.0",
  "environment_method": "canonical",
  "package_path": "DO_NOT_READ/environment_package.json"
}
```

Or `generation_manifest.json` → `"environment": { "enabled": true, "package_path": "..." }`.

Legacy adventures without manifest: validator `SKIP`.

---

## 14. Compatibility

| Item | Status |
|---|---|
| `single_investigator` | Supported — same environment semantics |
| `two_player` | Supported — split scenes compile from same locations |
| World-First Generation | Required linkage when truth package present |
| Harborview / Glass Alibi | Not modified |
| Object Interaction (M4) | Deferred |

---

## 15. Out of scope

- Detailed object actions, inventory, check redesign
- Clue/ending mechanics redesign
- Adventure generation
- Environment migration for legacy content

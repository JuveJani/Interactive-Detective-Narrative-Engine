# Environment System — Data Schema

**Package:** `DO_NOT_READ/environment_package.json` (default)  
**Manifest:** `environment_manifest.json` or `generation_manifest.environment`  
**JSON Schema:** `idne/schemas/environment_package.schema.json`

See `ENVIRONMENT_SYSTEM_SPEC.md` for semantics.

---

## environment_manifest.json

| Field | Type | Required |
|---|---|---|
| `schema_version` | string | yes (`"1.0"`) |
| `environment_method` | string | yes (`"canonical"`) |
| `package_path` | string | yes |

---

## environment_package.json — sections

| Section | Purpose |
|---|---|
| `locations` | Identity and provenance |
| `location_states` | Variants and attributes |
| `features` | Feature references at locations |
| `navigation` | Diegetic movement |
| `state_transitions` | Caused state changes |
| `revisit_rules` | Return behavior |
| `mandatory_locations` | Fair-play reachability checks |
| `player_content_refs` | PLAYER files to lint |
| `world_first_links` | Path to truth package |

---

## Visibility enum

`known_remotely` | `on_arrival` | `after_entering` | `approach_feature` | `hidden_until_interaction`

---

## Cause types

`initial` | `timeline_event` | `world_time` | `player_action` | `npc_action` | `always`

---

## Example

See `tests/fixtures/env_valid_minimal/DO_NOT_READ/environment_package.json`.

# Object Interaction System — Schema

**Package:** `DO_NOT_READ/object_interaction_package.json`  
**JSON Schema:** `idne/schemas/object_interaction_package.schema.json`

## Root sections

| Section | Purpose |
|---|---|
| `objects` | Hierarchy and states |
| `actions` | Player labels, costs, check bindings |
| `result_units` | Separate success/failure destinations |
| `state_transitions` | Persistent state changes |
| `items_registry` | Item ID references (not full inventory) |
| `mandatory_information` | Fair-play reachability |
| `revisit_rules` | Persistence on return |
| `world_first_links` | Truth package path |
| `environment_links` | Environment package path |
| `player_content_refs` | PLAYER files to lint |

## Check binding

```json
{
  "check_id": "CHK-PERCEPTION-DESK",
  "capability": "perception",
  "dc": 15,
  "eligible_character": "investigator",
  "one_attempt": true,
  "success_destination": "UNIT-KEY-SUCCESS",
  "failure_destination": "UNIT-KEY-FAIL",
  "changes_world_truth": false,
  "information_on_success": ["INFO-KEY-LOC"],
  "information_on_failure": []
}
```

## Example

`tests/fixtures/obj_valid_nested/DO_NOT_READ/object_interaction_package.json`

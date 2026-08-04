# Capability Check System — Schema

**Package:** `DO_NOT_READ/capability_check_package.json`  
**JSON Schema:** `idne/schemas/capability_check_package.schema.json`

## Sections

| Section | Role |
|---|---|
| `modifier_sources` | Character modifier definitions |
| `resolution_model` | d20 + modifier formula |
| `difficulty_bands` | Easy/Medium/Hard DC guidance |
| `checks` | Canonical check records |
| `destination_units` | Separate success/failure prose units |
| `player_content_refs` | Delivery scan targets |

## Check record (minimal)

```json
{
  "check_id": "CHK-PERCEPTION-DESK",
  "parent_action_id": "ACT-SEARCH-DESK",
  "parent_action_layer": "object_interaction",
  "parent_action_type": "search",
  "capability_category": "perception_observation",
  "modifier_source_id": "MOD-PERCEPTION",
  "dc": 15,
  "dc_justification": "Key concealed under papers",
  "attempt_policy": { "default": "one_attempt", "retry_extension_point": "future_retry_policy" },
  "destinations": {
    "action_unit_id": "UNIT-CHK-DECL",
    "success_destination": "UNIT-KEY-SUCCESS",
    "failure_destination": "UNIT-KEY-FAIL"
  },
  "fixed_truth_invariants": {
    "changes_evidence_existence": false,
    "changes_document_contents": false,
    "changes_fixed_truth": false,
    "changes_npc_fixed_knowledge": false
  },
  "information_trace": {
    "fixed_truth_ref": "WF-KEY",
    "source_layer": "object",
    "source_id": "OBJ-KEY-HIDDEN",
    "observation_id": "OBS-KEY"
  }
}
```

Example: `tests/fixtures/cap_valid_perception_key/DO_NOT_READ/capability_check_package.json`

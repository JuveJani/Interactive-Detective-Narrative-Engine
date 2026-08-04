# Investigation Validator — Schema

**Package:** `DO_NOT_READ/investigation_validator_package.json`  
**Manifest:** `investigation_validator_manifest.json`  
**JSON Schemas:**

- `idne/schemas/investigation_validator_package.schema.json`
- `idne/schemas/investigation_validator_finding.schema.json`

---

## Package sections

| Section | Role |
|---|---|
| `layer_links` | Paths to Investigation Core, Flow, Environment, Object Interaction, Capability Check, NPC packages |
| `conclusion_traces` | End-to-end chains per required conclusion |
| `inference_questions` | Mandatory inference answerability metadata |
| `information_sufficiency` | Per-inference source graph and independence |
| `recovery_routes` | Executable continuations after failed/incomplete inference |
| `access_requirements` | Keys, passwords, items, locations — fair-path metadata |
| `mandatory_check_fairness` | Mandatory-path check fairness (delegates capability validator) |
| `npc_disclosure_routes` | Required NPC information routes |
| `time_validation` | Deadline, variants, loops |
| `ending_reachability` | Reachability and truth-leak flags per ending |
| `accusation_fairness` | Final accusation neutrality |
| `play_mode_constraints` | Solo vs two-player validity |
| `player_audit` | PLAYER cross-layer audit targets |
| `state_graph_config` | `max_states`, `max_depth`, optional `forced_explosion` (fixtures) |
| `tier_b_mandatory` | Human review items with `resolved` flag |

---

## Conclusion trace chain step

```json
{ "layer": "fixed_truth", "ref": "WF-KEY" }
```

Required layers per trace: `fixed_truth`, `location`, `player_action`, `knowledge`, `conclusion`, `proof`. Optional: `object`, `npc`, `capability_check`, `observation`, `ending`.

---

## Inference question (minimal)

```json
{
  "question_id": "INF-001",
  "hypothesis_id": "HYP-001",
  "player_facing_text": "Where was the key hidden?",
  "defined_terms": ["key", "hidden"],
  "undefined_terms": [],
  "required_knowledge_ids": ["KNOW-KEY"],
  "available_before_question": true,
  "accepted_hypothesis_id": "HYP-001",
  "equally_supported_alternatives": [],
  "question_reveals_answer": false,
  "requires_internal_ids": false
}
```

---

## Recovery route (minimal)

```json
{
  "route_id": "REC-OFFICE",
  "trigger": "inference_incomplete",
  "inference_id": "INF-001",
  "player_action_label": "Return to the manager's office.",
  "destination_ref": "LOC-OFFICE",
  "destination_legal": true,
  "changes_knowledge_or_access": true,
  "changes_state": true,
  "zero_cost_loop": false,
  "vague_instruction": false,
  "bare_page_code": false
}
```

---

## Finding record

See `investigation_validator_finding.schema.json`. Produced by `validate_investigation()` in `findings[]`.

Example fixture: `tests/fixtures/iv_complete_solo/DO_NOT_READ/investigation_validator_package.json`

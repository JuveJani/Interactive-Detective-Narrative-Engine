# World-First Generation — Data Schema

**Document type:** Machine-readable layer definitions  
**Package file:** `DO_NOT_READ/world_truth_package.json` (default path)  
**Manifest:** `generation_manifest.json` at adventure root  
**JSON Schema:** `idne/schemas/world_truth_package.schema.json`

---

## 1. generation_manifest.json

| Field | Type | Required | Description |
|---|---|---|---|
| `schema_version` | string | yes | `"1.0"` |
| `generation_method` | string | yes | MUST be `"world_first"` for validation |
| `package_path` | string | yes | Relative path to truth package |
| `gates` | object | yes | Gate ID → `{ "status": "PASS"|"FAIL", "validated_at": string? }` |

Required gate keys when scenes exist: `G-WF1` through `G-WF7`.

---

## 2. world_truth_package.json — root

| Field | Type | Required |
|---|---|---|
| `schema_version` | string | yes |
| `adventure_id` | string | yes |
| `fixed_truth` | object | yes |
| `causal_timeline` | object | yes |
| `world_state_timeline` | object | yes |
| `npc_knowledge` | object | yes |
| `evidence_provenance` | object | yes |
| `observable_information` | object | yes |
| `conclusion_requirements` | object | yes |
| `narrative_construction` | object | optional until G-WF7 |
| `ending_claims` | array | optional |

---

## 3. fixed_truth

```json
{
  "culprit_id": "NPC-A",
  "motive": "string",
  "method": "string",
  "opportunity": "string",
  "immutable_facts": [
    { "fact_id": "FACT-001", "statement": "Authoritative statement" }
  ]
}
```

---

## 4. causal_timeline

```json
{
  "clock_start": "2024-03-15T19:00:00",
  "events": [
    {
      "event_id": "EVT-001",
      "timestamp": "2024-03-15T19:35:00",
      "day_label": "Day 1 Saturday",
      "location_id": "LOC-BASEMENT",
      "description": "string",
      "participants": ["NPC-A", "NPC-VICTIM"],
      "causes": [],
      "reveals_facts": ["FACT-001"],
      "effects": ["FACT-002"]
    }
  ]
}
```

**Timestamp rules:** ISO-8601 `YYYY-MM-DDTHH:MM` or `YYYY-MM-DDTHH:MM:SS`.  
**Forbidden:** bare words (`evening`, `later`, `sometime`).  
**day_label:** REQUIRED when timestamp is not full ISO date-time.

---

## 5. world_state_timeline

```json
{
  "snapshots": [
    {
      "at_event_id": "EVT-001",
      "people_locations": { "NPC-A": "LOC-BASEMENT" },
      "object_states": { "OBJ-MOP": "wet" },
      "access_states": { "LOC-BASEMENT": "open" },
      "evidence_conditions": {}
    }
  ]
}
```

---

## 6. npc_knowledge

```json
{
  "npcs": [
    {
      "npc_id": "NPC-A",
      "knows": ["FACT-002"],
      "believes_incorrectly": [
        { "belief_fact_id": "FACT-X", "actual_fact_id": "FACT-Y", "cause": "misheard" }
      ],
      "witnessed_events": ["EVT-001"],
      "hides": ["FACT-002"],
      "behavior_rationale": "string"
    }
  ]
}
```

---

## 7. evidence_provenance

```json
{
  "evidence": [
    {
      "evidence_id": "EVD-001",
      "source_event_id": "EVT-002",
      "type": "physical|document|testimony",
      "description": "string",
      "establishes_fact_ids": ["FACT-003"],
      "misleading": false,
      "misleading_cause": null
    }
  ]
}
```

`source_event_id` MUST reference `causal_timeline.events[].event_id`.

---

## 8. observable_information

```json
{
  "observations": [
    {
      "observation_id": "OBS-001",
      "learnable_fact_id": "FACT-003",
      "source_evidence_id": "EVD-001",
      "requires": {
        "action": "search",
        "location_id": "LOC-BASEMENT",
        "prior_knowledge": [],
        "item_id": null,
        "check_id": null
      },
      "hidden_if_not_met": true
    }
  ]
}
```

---

## 9. conclusion_requirements

```json
{
  "questions": [
    {
      "question_id": "Q-CULPRIT",
      "answer_entity_id": "NPC-A",
      "required_fact_ids": ["FACT-002", "FACT-003"],
      "category": "culprit|method|motive|opportunity|custom"
    }
  ]
}
```

Every `required_fact_id` MUST be obtainable via observable chain or event effects.

---

## 10. narrative_construction

```json
{
  "scenes": [
    {
      "scene_id": "J-100",
      "asserted_fact_ids": ["FACT-003"],
      "asserted_culprit_id": null,
      "player_text_summary": "Non-authoritative summary for validation",
      "sources": ["OBS-001"]
    }
  ]
}
```

**MUST NOT** include `asserted_fact_ids` outside Fixed Truth / observable chain.  
**MUST NOT** set `asserted_culprit_id` ≠ `fixed_truth.culprit_id`.

---

## 11. ending_claims (optional validation aid)

```json
[
  {
    "ending_id": "E-CORRECT",
    "asserted_fact_ids": ["FACT-002"],
    "trigger_summary": "Sheet-checkable conditions"
  }
]
```

---

## 12. ID stability

All `fact_id`, `event_id`, `evidence_id`, `observation_id`, `npc_id`, `location_id` MUST be stable internal IDs — hidden from players in delivery.

---

## 13. Example minimal package

See `tests/fixtures/wf_valid_minimal/DO_NOT_READ/world_truth_package.json`.

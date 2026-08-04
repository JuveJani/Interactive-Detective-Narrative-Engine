# Investigation Core — Schema

**Package:** `DO_NOT_READ/investigation_core_package.json`  
**JSON Schema:** `idne/schemas/investigation_core_package.schema.json`

## Sections

| Section | Entity |
|---|---|
| `world_facts` | World Fact |
| `observations` | Observation |
| `physical_evidence` | Physical Evidence |
| `testimony` | Testimony |
| `knowledge` | Knowledge |
| `relationships` | Relationship |
| `hypotheses` | Hypothesis |
| `conclusions` | Conclusion |
| `proofs` | Proof |
| `compatibility_clue_map` | Legacy CLUE-* mapping |
| `acquisition_rules` | Acquisition metadata |

## Knowledge acquisition block

```json
{
  "knowledge_id": "KNOW-002",
  "statement": "Mop was wet after incident",
  "acquisition": {
    "source_type": "physical_evidence",
    "source_id": "EVD-001",
    "interaction_required": true
  }
}
```

## Proof

```json
{
  "proof_id": "PROOF-A",
  "conclusion_id": "CONC-CULPRIT",
  "required_knowledge_ids": ["KNOW-002", "KNOW-004"],
  "claims_independence": true,
  "independent_knowledge_subset": ["KNOW-002"]
}
```

Example: `tests/fixtures/inv_core_valid_minimal/DO_NOT_READ/investigation_core_package.json`

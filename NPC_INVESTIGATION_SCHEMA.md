# NPC Investigation — Schema

**Package:** `DO_NOT_READ/npc_investigation_package.json`  
**Manifest:** `npc_investigation_manifest.json`  
**JSON Schema:** `idne/schemas/npc_investigation_package.schema.json`

## Sections

| Section | Entity |
|---|---|
| `npcs` | NPC records (static + initial dynamic state) |
| `npc_graph` | NPC nodes and relationship edges |
| `information_known_model` | Per-NPC knowledge holdings |
| `topics` | Topic ids and unlock conditions |
| `conversation_graph` | Conversations, routes, nodes |
| `trust_model` | Range, modifiers, not-globally-positive flag |
| `relationship_reactions` | Event-driven trust/suspicion deltas |
| `testimony_links` | Conversation → testimony / knowledge grants |
| `investigation_core_links` | Path to Investigation Core package |

## NPC static properties

```json
{
  "npc_id": "NPC-A",
  "public_name": "Custodian",
  "static_properties": {
    "motivation": "Protect job",
    "honesty": 0.4,
    "deception": 0.6,
    "manipulation": 0.5,
    "loyalty": "employer",
    "fear": "arrest"
  },
  "relationships": [
    {
      "target_npc_id": "NPC-B",
      "relationship_type": "rival",
      "strength": 0.7
    }
  ],
  "initial_dynamic_state": {
    "trust": 40,
    "information_known": ["INFO-NPC-A-1"],
    "revealed_topics": [],
    "suspicion": 20,
    "pressure": 10
  }
}
```

## Topic unlock

```json
{
  "topic_id": "TOPIC-MOP",
  "unlock_conditions": [
    { "type": "object_discovered", "object_id": "OBJ-DESK" },
    { "type": "world_time", "clock": "T1" }
  ]
}
```

## Conversation route

```json
{
  "conversation_id": "CONV-NPC-B-INTRO",
  "npc_id": "NPC-B",
  "entry_topic_id": "TOPIC-ARGUMENT",
  "route_conditions": [
    { "type": "trust", "npc_id": "NPC-B", "min": 30 }
  ],
  "nodes": [
    {
      "node_id": "CN-001",
      "player_label": "Ask about the argument you heard.",
      "npc_response_unit": "UNIT-RESP-001",
      "unlocks_topic_ids": ["TOPIC-MOP"],
      "requires": { "trust_min": 30 }
    }
  ]
}
```

## Trust modifier (relationship reaction)

```json
{
  "modifier_id": "TRUST-ACCUSE-RIVAL",
  "trigger": "player_accuses_npc",
  "target_npc_id": "NPC-A",
  "subject_npc_id": "NPC-B",
  "relationship_reaction": {
    "if_relationship": "rival",
    "trust_delta": 15
  }
}
```

Example package: `tests/fixtures/npc_valid_minimal/DO_NOT_READ/npc_investigation_package.json`

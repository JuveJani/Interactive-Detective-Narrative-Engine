# NPC Investigation — Validation

**Harness:** `python3 -m idne.npc_investigation_validate <adventure_root>`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.16

## Skip behavior

| Condition | Result |
|---|---|
| No `npc_investigation_manifest.json` and no `generation_manifest.npc_investigation.enabled` | SKIP |
| `npc_investigation_method` ≠ `canonical` | SKIP |

Harborview and legacy adventures without declaration: SKIP (not FAIL).

## Automated checks

| ID | Validates |
|---|---|
| NPC-PKG-PRESENT | Package file exists |
| NPC-STATIC | All static properties and dynamic state fields on every NPC |
| NPC-GRAPH | Graph nodes/edges reference declared NPCs |
| NPC-INFO-KNOWN | `info_id` holders, valid `knowledge_id` / `topic_id` vs Investigation Core |
| NPC-TOPIC-UNLOCK | Every topic has `unlock_conditions` with allowed types |
| NPC-CONVERSATION | Routes, nodes, player labels, response units |
| NPC-TRUST | Not-globally-positive trust; accuse modifiers have relationship reactions |
| NPC-RELATION-REACT | Actor/target NPCs valid; at least one delta |
| NPC-TESTIMONY-LINK | Testimony and granted knowledge exist in Investigation Core |

## Tier B (manual / partial)

| ID | Validates |
|---|---|
| NPC-B-01 | Every fair-path knowledge from testimony has reachable conversation route |
| NPC-B-02 | Relationship reactions cover major accuse/defend pairs for primary suspects |

## Tier C (playtest)

| ID | Validates |
|---|---|
| NPC-H-01 | Players perceive trust as situational, not a single “goodness” meter |

## Fixtures

Nine fixtures under `tests/fixtures/npc_*`:

| Fixture | Expected |
|---|---|
| `npc_valid_minimal` | PASS |
| `npc_missing_static` | FAIL (NPC-STATIC) |
| `npc_orphan_graph` | FAIL (NPC-GRAPH) |
| `npc_topic_no_unlock` | FAIL (NPC-TOPIC-UNLOCK) |
| `npc_conversation_no_route` | FAIL (NPC-CONVERSATION) |
| `npc_info_invalid_knowledge` | FAIL (NPC-INFO-KNOWN) |
| `npc_trust_positive_only` | FAIL (NPC-TRUST) |
| `npc_reaction_invalid_npc` | FAIL (NPC-RELATION-REACT) |
| `npc_empty_conversation_nodes` | FAIL (NPC-CONVERSATION) |

# Story Validator — Schema

**Package:** `DO_NOT_READ/story_validator_package.json`  
**Manifest:** `story_validator_manifest.json`  
**JSON Schemas:**

- `idne/schemas/story_validator_package.schema.json`
- `idne/schemas/story_validator_finding.schema.json`

---

## Package sections

| Section | Role |
|---|---|
| `story_frame` | Spoiler-safe investigation frame |
| `timeline` | Anchors, events, temporal references |
| `causal_events` | Cause/consequence graph metadata |
| `information_facts` | Introduction and term tracking |
| `knowledge_order` | Per-scene required vs prior knowledge |
| `npc_consistency` | NPC behaviour and knowledge alignment |
| `location_object_continuity` | Object/location state vs prose |
| `narrative_neutrality` | Suspect spotlight flags (Tier B) |
| `inference_questions` | Question clarity metadata |
| `opening_transitions` | Opening and transition clarity |
| `ending_story` | Per-ending causal and truth alignment |
| `plain_language` | Clarity scan configuration |
| `player_audit` | PLAYER files to cross-check |
| `tier_b_mandatory` | Human review items |

---

## Finding record

Includes: `finding_id`, `severity`, `confidence`, `layer`, `source_file`, `entity_id`, `player_excerpt`, `expected_canonical`, `observed_issue`, `affected_question`, `affected_conclusion`, `affected_ending`, `script_detectable`, `tier`.

Example package: `tests/fixtures/sv_valid_clear/DO_NOT_READ/story_validator_package.json`

# Adventure Generator v2 — Schema

**Milestone:** 11

---

## 1. Adventure brief (`adventure_brief.json`)

| Field | Type | Required |
|---|---|---|
| `universe` | string | yes |
| `genre` | string | yes |
| `realism_level` | string | yes |
| `player_mode` | `single_investigator` \| `two_player` | yes |
| `investigator_character` | string | yes |
| `target_playtime_minutes` | integer | yes |
| `in_world_duration` | string | yes |
| `tone` | string | yes |
| `difficulty` | string | yes |
| `location_scale` | string | yes |
| `content_boundaries` | string | yes |
| `required_themes` | string[] | optional |
| `forbidden_themes` | string[] | optional |
| `author_notes` | string | optional |

---

## 2. Generation state (`generation_state.json`)

| Field | Type | Description |
|---|---|---|
| `schema_version` | string | `"1.0"` |
| `adventure_id` | string | Workspace identifier |
| `brief_version` | string | Brief revision |
| `stage_status` | map stage→status | `PENDING`, `RUNNING`, `COMPLETE`, `FAILED`, `BLOCKED`, `AWAITING_APPROVAL`, `INVALIDATED` |
| `input_hashes` | map | SHA-256 of inputs |
| `output_hashes` | map | SHA-256 per stage output |
| `validator_results` | map | Per-stage validator JSON |
| `repair_attempts` | array | Repair history entries |
| `human_approvals` | map | Approval records |
| `invalidated_stages` | array | Downstream invalidation list |
| `model_metadata` | object | Backend configuration snapshot |
| `token_estimates` | map | Context budget per stage |
| `timestamps` | map | ISO-8601 timestamps |
| `checkpoint_stage` | string | Resume pointer |
| `logic_validation_complete` | boolean | Logic layers validated |
| `readiness_status` | string | `IN_PROGRESS`, `PRE_PLAYTEST`, `PLAYTIME_MISMATCH`, `TIER_BC_INCOMPLETE`, `VALIDATION_FAILED` |
| `player_mapping_manifest` | object | Canonical→PLAYER unit map |

---

## 3. Model adapter config

| Field | Type | Default |
|---|---|---|
| `backend` | string | `mock` |
| `model_name` | string | `mock-deterministic` |
| `context_size` | integer | 8192 |
| `temperature` | float | 0.1 |
| `max_output_tokens` | integer | 2048 |
| `timeout_seconds` | float | 120 |
| `max_retries` | integer | 2 |
| `local_mode` | boolean | true |
| `endpoint_url` | string | optional |
| `cli_command` | string | optional |
| `extra` | object | optional overlay roots, etc. |

---

## 4. `.idne` package

ZIP archive containing:

| Path | Content |
|---|---|
| `package_manifest.json` | Entry list with SHA-256 |
| `package_checksum.sha256` | Checksum file |
| `adventure/` | Adventure root tree |
| `generation/` | Generation state and reports |
| `brief/` | Approved brief |

---

## 5. Stage IDs

Canonical stage identifiers match `idne/generate/stages.py` `STAGE_ORDER`.

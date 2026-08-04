# NPC Investigation System — Normative Specification

**Milestone:** 5B — NPC Investigation System  
**Status:** Normative  
**Aligned with:** `INVESTIGATION_CORE_SPEC.md`, `IDNE_ENGINE_v0.4.md`  
**Validation:** `python3 -m idne.npc_investigation_validate`

---

## 1. Purpose

Define the canonical **NPC investigation model**: static character properties, dynamic conversational state, relationship-aware trust, information held per NPC, topic unlocking, and conversation routing.

**Does not redesign:** Investigation Core entities (Knowledge, Testimony, Proof), endings, capability checks, or Object Interaction.

**Out of scope:** Adventure generation, Harborview migration, dialogue delivery mechanics (result units / book layout), inventory, retries, false checks, ending evaluation.

---

## 2. Layer position

World Truth → Environment → Object Interaction → Investigation Core → **NPC Investigation Package** → Adventure Logic → Delivery.

NPC Investigation binds Investigation Core `testimony` and `knowledge` to per-NPC state and conversation graphs. It does **not** replace Knowledge acquisition rules in Investigation Core — it declares how NPC dialogue **grants** testimony-linked knowledge when routes open.

---

## 3. NPC record

Each `npc_id` MUST declare:

### 3.1 Static properties (immutable for adventure)

| Property | Role |
|---|---|
| `motivation` | Primary drive (string) |
| `relationships` | Typed edges to other NPCs (see §6) |
| `honesty` | Baseline truthfulness (0–1) |
| `deception` | Baseline concealment tendency (0–1) |
| `manipulation` | Baseline steering tendency (0–1) |
| `loyalty` | Primary allegiance label (string) |
| `fear` | Primary fear label (string) |

### 3.2 Dynamic state (initial values; runtime mutable)

| Field | Role |
|---|---|
| `trust` | Player–NPC rapport (numeric; not globally positive — see §5) |
| `information_known` | `info_id` entries this NPC holds at start |
| `revealed_topics` | `topic_id` list already surfaced to player |
| `suspicion` | NPC suspicion of player or case direction |
| `pressure` | Interrogation / deadline pressure on NPC |

---

## 4. NPC graph

Machine graph of declared NPCs and relationship edges:

- `nodes`: every `npc_id`
- `edges`: `from_npc_id`, `to_npc_id`, `relationship_type`

Graph nodes MUST reference declared NPCs. Used for relationship reaction resolution and validation cross-checks.

---

## 5. Trust model

Trust is **not globally positive**. The same player action MAY increase trust with one NPC and decrease it with another depending on relationships.

### 5.1 Requirements

- `trust_model.default_range` declares min/max (typically 0–100).
- `trust_model.not_globally_positive: true` MUST be set for canonical adventures.
- When `not_globally_positive` is true, the package MUST document at least one **negative** `trust_delta` via modifiers or `relationship_reactions`, OR set `negative_trust_documented: true` with explicit design note.

### 5.2 Modifiers

`trust_model.modifiers` bind triggers (e.g. `player_accuses_npc`) to `relationship_reaction` blocks:

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

Accusing NPC-B may **increase** trust with rival NPC-A. Accusing an ally MUST use negative `trust_delta`.

### 5.3 Relationship reactions

`relationship_reactions` declare per-actor effects when world/player events fire:

- `actor_npc_id` — who reacts
- `trigger` — e.g. `accuse_npc`, `defend_npc`
- `target_npc_id` — subject of event
- `relationship_type` — which edge type gates the reaction
- `trust_delta`, `suspicion_delta` — at least one required

---

## 6. Relationship model

Per-NPC `relationships` array:

```json
{
  "target_npc_id": "NPC-B",
  "relationship_type": "rival",
  "strength": 0.7
}
```

`relationship_type` is adventure-defined (e.g. `ally`, `rival`, `family`, `employer`). Reactions and trust modifiers match on `relationship_type`.

Symmetric edges SHOULD be declared explicitly when both NPCs hold the relationship.

---

## 7. InformationKnown model

`information_known_model` maps what each NPC knows before and during play:

| Field | Role |
|---|---|
| `info_id` | Stable reference |
| `npc_id` | Holder |
| `knowledge_id` | Investigation Core Knowledge ID |
| `topic_id` | Optional topic this information unlocks or belongs to |

`knowledge_id` MUST exist in linked Investigation Core package when core is present.

NPC `initial_dynamic_state.information_known` lists `info_id` values from this model.

---

## 8. Topic unlocking

`topics` declare conversational subjects. Each `topic_id` MUST have `unlock_conditions` — at least one condition from:

| `type` | Opens when |
|---|---|
| `trust_threshold` | NPC trust ≥ `min` |
| `knowledge_held` | Player holds `knowledge_id` |
| `player_action` | Declared action id / label |
| `world_state` | Environment or logic flag |
| `world_time` | Clock / phase (`clock`) |
| `object_discovered` | Object interaction state |
| `information_known` | NPC holds `info_id` |

Topics gate conversation entry and node availability.

---

## 9. Conversation graph

`conversation_graph` entries:

| Field | Role |
|---|---|
| `conversation_id` | Stable id |
| `npc_id` | Speaker |
| `entry_topic_id` | Topic that opens this conversation |
| `route_conditions` | How conversation becomes available (see below) |
| `nodes` | Player choices and NPC responses |

### 9.1 Route conditions

Every conversation MUST declare `route_conditions`. Allowed `type` values:

| `type` | Meaning |
|---|---|
| `trust` | NPC trust band |
| `information` | Player or NPC information state |
| `player_action` | Prior player action |
| `world_state` | World flag |
| `world_time` | Time gate |
| `object_discovered` | Object discovery |

Routes open through trust, information, player actions, world state, time, and object discoveries — not solely through trust.

### 9.2 Conversation nodes

Each node MUST have:

- `node_id`
- `player_label` — human action text (no bare internal codes)
- `npc_response_unit` — delivery unit id (adapter resolves prose)
- Optional `unlocks_topic_ids`, `requires` (e.g. `trust_min`)

---

## 10. Testimony links

`testimony_links` connect Investigation Core testimony to conversation outcomes:

```json
{
  "testimony_id": "TEST-001",
  "conversation_node_id": "CN-001",
  "grants_knowledge_id": "KNOW-003"
}
```

`testimony_id` and `grants_knowledge_id` MUST exist in Investigation Core when linked.

---

## 11. Investigation Core link

```json
"investigation_core_links": {
  "package_path": "DO_NOT_READ/investigation_core_package.json"
}
```

NPC Investigation MUST NOT duplicate Knowledge definitions — it references Investigation Core IDs.

---

## 12. Declaration

`npc_investigation_manifest.json`:

```json
{
  "schema_version": "1.0",
  "npc_investigation_method": "canonical",
  "package_path": "DO_NOT_READ/npc_investigation_package.json"
}
```

Or `generation_manifest.json` → `npc_investigation.enabled: true` with `package_path`.

Validator: `python3 -m idne.npc_investigation_validate <adventure_root>`

Legacy adventures (e.g. Harborview) without manifest: **SKIP**.

---

## 13. Design constraints

- **MUST NOT** redefine Investigation Core proof, conclusion, or acquisition graphs.
- **MUST NOT** grant knowledge without Investigation Core `knowledge_id` or declared testimony link.
- **MUST NOT** assume trust increases are always desirable for the player.
- **MUST** support relationship-conditioned trust deltas (accuse ally vs rival).

---

## 14. Example (relationship reaction)

Player accuses NPC-B. NPC-A (rival of B) gains trust (+10); NPC-A defending an ally of B would lose trust (−20). Same action, opposite trust effects — relationship reactions, not a global trust slider.

---

## 15. Out of scope

Ending evaluation, capability check rewrite, inventory, retries, false checks, adventure generation, Delivery Adapter layout.

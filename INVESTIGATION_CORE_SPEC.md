# Investigation Core — Normative Specification

**Milestone:** 5A — Investigation Core  
**Status:** Normative  
**Supersedes:** clue-ID-driven investigation as primary model (legacy clues compatibility-only)

---

## 1. Purpose

Replace the legacy **clue-driven** investigation model with a canonical **investigation data model** linking world truth to player knowledge, hypotheses, conclusions, and proof.

**Not in scope (5A):** NPC conversation systems, trust, InformationKnown, dialogue progression, ending evaluation, deadline endings, capability rewrite, inventory rewrite, retries, false checks.

---

## 2. Canonical entities

| Entity | Role |
|---|---|
| **World Fact** | Immutable objective truth atom (from World-First Fixed Truth) |
| **Observation** | Perceptual record available via environment/object interaction |
| **Physical Evidence** | Material trace with mandatory provenance |
| **Testimony** | NPC-originated statement record (no dialogue system in 5A) |
| **Knowledge** | Investigative information the player may acquire |
| **Relationship** | Typed link: supports, contradicts, derives_from, requires, independent_of |
| **Hypothesis** | Player-synthesizable proposition; not auto-proved |
| **Conclusion** | Answerable case question (culprit, method, motive, etc.) |
| **Proof** | Knowledge set that makes a conclusion provable |

Legacy `CLUE-*` IDs map via `compatibility_clue_map` only — **MUST NOT** drive investigation logic.

---

## 3. Information acquisition

Knowledge is acquired only through declared `acquisition` paths:

| `source_type` | Source |
|---|---|
| `observation` | Observation ID |
| `physical_evidence` | Evidence ID (+ interaction) |
| `testimony` | Testimony ID (no dialogue engine) |
| `world_fact` | World Fact ID (rare direct grant) |
| `hypothesis` | Hypothesis ID after player synthesis |
| `synthesis` | Declared synthesis step |

**MUST NOT** grant knowledge via scene Auto-clue pattern as primary driver.

---

## 4. Conclusions become provable

Each `conclusion_id` MUST have ≥1 `proof` record listing `required_knowledge_ids`.

Fair play: every required knowledge item MUST be obtainable via acquisition chain from observations, evidence, testimony, or valid hypothesis synthesis.

---

## 5. Proof independence

Final conclusions SHOULD have ≥2 **independent** proof routes where engine fair-play requires redundancy (Engine §2.3).

Independence rules:

- Proof routes MUST differ in `independent_knowledge_subset` or documented disjoint knowledge cores.
- Identical `required_knowledge_ids` sets across proofs FAIL unless `same_route_justification`.

---

## 6. Contradiction handling

`relationships` with `type: contradicts` MUST declare:

- `resolution` (e.g. `red_herring`, `resolved_by_knowledge`, `timeline_order`), OR
- `allow_unresolved_red_herring: true` for intentional unresolved tension.

Unresolved contradictions between proof-critical knowledge FAIL validation.

---

## 7. Evidence provenance

Every `physical_evidence` MUST cite `provenance.world_fact_id` and/or `provenance.source_event_id` from World-First timeline.

Evidence existence is **not** check-dependent (Object Interaction Milestone 4 alignment).

---

## 8. Testimony (structure only)

Testimony records require `source_npc_id` and `content_knowledge_id` or `asserts_world_fact_id`.

`dialogue_system: false` in 5A — no trust, branching dialogue, or InformationKnown.

---

## 9. Hypotheses

- `player_synthesis_required: true` by default.
- **MUST NOT** `auto_proven` or `granted_without_synthesis`.
- `yields_knowledge_id` enters acquisition graph after synthesis.

Replaces legacy Infer as graph concept — Infer delivery mechanics unchanged until later milestones.

---

## 10. Declaration

`investigation_manifest.json`:

```json
{
  "schema_version": "1.0",
  "investigation_method": "canonical",
  "package_path": "DO_NOT_READ/investigation_core_package.json"
}
```

Validator: `python3 -m idne.investigation_core_validate`

---

## 11. Layer position

World Truth → Environment → Object Interaction → **Investigation Core** → Adventure Logic → Delivery.

---

## 12. Legacy clue compatibility

```json
{
  "legacy_clue_id": "CLUE-C06",
  "knowledge_id": "KNOW-002",
  "compatibility_only": true
}
```

Harborview-era clue registers remain for migration reference; new adventures use Knowledge IDs.

---

## 13. Out of scope

Ending evaluation, NPC conversation, capability rewrite, inventory, retries, false checks, adventure generation.

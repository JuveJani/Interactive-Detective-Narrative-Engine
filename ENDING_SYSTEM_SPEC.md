# Ending System — Normative Specification

**Milestone:** 5C — Investigation Flow & Ending System  
**Status:** Normative  
**Companion:** `INVESTIGATION_FLOW_SPEC.md`  
**Package section:** `endings`, `ending_graph`, `deadline`, `accusation_questionnaire`

---

## 1. Purpose

Define canonical **ending architecture**: state-driven triggers, ending graphs, partial/hidden/perfect endings, deadline endings, final accusation questionnaire, and **truth-reveal policy**.

Ending **text** is Delivery Adapter output. Ending **selection logic** is Investigation Flow.

---

## 2. Ending types

| `ending_type` | Role |
|---|---|
| `perfect` | Player solved the case; may reveal **complete truth** |
| `partial` | Some conclusions correct or incomplete proof |
| `hidden` | Special trigger; not advertised in player materials |
| `deadline` | Time expired (`deadline_expired` trigger) |
| `failure` / `narrative_failure` | Fair failure paths |

---

## 3. Truth-reveal policy (normative)

| Rule | Meaning |
|---|---|
| **Perfect ending** | MAY set `reveals_full_truth: true` and `truth_reveal_scope: complete` |
| **Imperfect endings** | MUST set `reveals_full_truth: false` and `truth_reveal_scope` ≠ `complete` |
| **Partial scope** | Use `truth_reveal_scope: partial` and `max_knowledge_revealed_ids` to cap what ending prose may assert |
| **Logical follow-through** | Ending MUST explain only what follows from the player's investigation path — no culprit's full motive/method unless knowledge on that path supports it |

Validator check: `FLOW-TRUTH-LEAK`.

---

## 4. Deadline ending

When `deadline.enabled`:

```json
{
  "enabled": true,
  "deadline_clock": "T_DEADLINE",
  "deadline_ending_id": "END-TIMEOUT",
  "blocks_accusation_after": true
}
```

- `deadline_ending_id` MUST reference an ending with `ending_type: deadline`
- Deadline ending MUST NOT `reveals_full_truth`
- Trigger type: `deadline_expired`

Validator check: `FLOW-DEADLINE`.

---

## 5. State-driven triggers

Replace ending-condition tables with `trigger` objects on each ending:

```json
{
  "type": "state_driven",
  "required_knowledge_ids": ["KNOW-002", "KNOW-004"],
  "required_accusation": { "Q-CULPRIT": "NPC-A", "Q-METHOD": "METHOD-PUSH" },
  "required_state": { "accusation_complete": true },
  "requires_full_proof": true
}
```

| Trigger field | Role |
|---|---|
| `required_knowledge_ids` | Player must hold these Knowledge IDs |
| `required_accusation` | Questionnaire answers must match |
| `required_state` | Flags/counters must match |
| `min_knowledge_count` | Partial endings — minimum facts gathered |
| `wrong_accusation_allowed` | Partial ending despite wrong culprit |
| `requires_full_proof` | Perfect ending — must cover at least one Investigation Core proof route |

**MUST NOT** combine `deadline_expired` with `required_knowledge_ids` on the same trigger.

---

## 6. Ending graph

`ending_graph` declares nodes, transitions, and **evaluation order**:

```json
{
  "nodes": ["END-PERFECT", "END-PARTIAL", "END-HIDDEN", "END-TIMEOUT"],
  "edges": [
    { "from": "FLOW-ACTIVE", "to": "END-PERFECT", "condition": "accusation_correct" },
    { "from": "FLOW-ACTIVE", "to": "END-TIMEOUT", "condition": "deadline" }
  ],
  "evaluation_order": ["END-PERFECT", "END-HIDDEN", "END-PARTIAL", "END-TIMEOUT"]
}
```

- Every `ending_id` MUST appear in `nodes`
- `evaluation_order` defines priority when multiple triggers could match (higher priority first)
- Hidden endings MAY be omitted from player-facing materials but MUST be in the graph

Validator checks: `FLOW-ENDING-GRAPH`, `FLOW-IMPOSSIBLE`, `FLOW-UNREACHABLE`.

---

## 7. Partial endings

Partial endings grant narrative closure without full solution:

- `wrong_accusation_allowed: true` on trigger
- `max_knowledge_revealed_ids` caps truth exposed in ending delivery
- **MUST NOT** reveal culprit + method + motive completely unless player earned that knowledge

---

## 8. Hidden endings

`hidden: true` endings use non-obvious triggers (e.g. `found_secret_diary` flag). They:

- MAY appear in `evaluation_order` after perfect but before partial
- MUST NOT `reveals_full_truth` unless upgraded to `perfect` type (hidden perfect is allowed if trigger requires full proof)

---

## 9. Perfect ending

Perfect ending requirements:

1. Correct accusation questionnaire answers aligned with Investigation Core `conclusions.answer_entity_id`
2. `requires_full_proof: true` — `required_knowledge_ids` MUST be a superset of at least one proof's `required_knowledge_ids` for culprit conclusion
3. `reveals_full_truth: true` — complete truth reveal permitted **only here**

Validator check: `FLOW-UNSUPPORTED-ACCUSATION`.

---

## 10. Final accusation questionnaire

```json
{
  "questionnaire_id": "ACC-FINAL",
  "required_before_ending_eval": true,
  "questions": [
    { "question_id": "Q-CULPRIT", "conclusion_id": "CONC-CULPRIT", "answer_type": "npc_id" },
    { "question_id": "Q-METHOD", "conclusion_id": "CONC-METHOD", "answer_type": "entity_id" }
  ]
}
```

- Each `conclusion_id` MUST exist in Investigation Core
- Each conclusion MUST have ≥1 proof route when core is linked
- Player-facing questionnaire is Delivery; this block is machine truth for accusation evaluation

---

## 11. Impossible and unreachable endings

**Impossible:** triggers with contradictory requirements (conflicting accusation vs state, `impossible_by_design`, deadline + knowledge requirements).

**Unreachable:** scene chain first steps requiring unobtainable knowledge; `never_reachable` triggers; chains marked `unreachable_by_design`.

Validator checks: `FLOW-IMPOSSIBLE`, `FLOW-UNREACHABLE`.

---

## 12. Engine alignment

- Engine §8.3: sheet-checkable conditions — accusation questionnaire + recorded knowledge/state
- Engine §8.4: every ending reachable on at least one legal path
- QA ending prose rules: imperfect endings MUST NOT leak full solution (`FLOW-TRUTH-LEAK`)

---

## 13. JSON Schema

`idne/schemas/investigation_flow_package.schema.json`

Example: `tests/fixtures/iflow_valid_minimal/DO_NOT_READ/investigation_flow_package.json`

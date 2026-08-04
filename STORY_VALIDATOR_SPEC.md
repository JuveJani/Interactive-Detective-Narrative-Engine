# Story Validator — Normative Specification

**Milestone:** 8 — Story Validator  
**Status:** Normative  
**Validation:** `python3 -m idne.story_validate`

---

## 1. Purpose

Check whether the mystery is **understandable**, **causally coherent**, **temporally clear**, and **consistently communicated** to the player.

Does **not** judge literary taste.

Detects story information that is contradictory, incomplete, temporally ambiguous, causally unsupported, introduced without explanation, assumed before revelation, or phrased so unclearly that required reasoning becomes impossible.

**Supports:** `single_investigator`, `two_player`.

**Out of scope:** Playtime Calibration, DM Feeling Validator, paid retries, false checks, Inventory System, PLAYER auto-rewrite, adventure generation.

---

## 2. Declaration

`story_validator_manifest.json`:

```json
{
  "schema_version": "1.0",
  "story_validator_method": "canonical",
  "package_path": "DO_NOT_READ/story_validator_package.json"
}
```

---

## 3. Validation layers

| Layer | Validates |
|---|---|
| Timeline | Unambiguous temporal frames; anchors for relative references |
| Causal coherence | Causes, consequences, actors, traces, ending support |
| Information introduction | First mention, explanation, no half-information |
| Knowledge order | Scenes do not assume unavailable knowledge |
| Story frame | Spoiler-safe opening frame; PLAYER communicates it |
| NPC consistency | Motivation, knowledge, testimony, behaviour alignment |
| Location/object continuity | Prose matches canonical environment state |
| Narrative neutrality | Suspect spotlight (Tier B review) |
| Inference explainability | Questions understandable from prose |
| Opening/transitions | Purpose, actions, causal movement |
| Ending story | Causal outcomes; truth/timeline alignment |
| Plain language | Measurable clarity (length, acronyms, jargon, naming) |
| PLAYER cross-check | Actual PLAYER text scanned; absent → BLOCKED |

---

## 4. Outcomes

| Outcome | Meaning |
|---|---|
| PASS | No proven Tier A defects; Tier B mandatory resolved |
| FAIL | Proven Tier A defect |
| CONDITIONAL_PASS | Tier B findings or mandatory review pending |
| BLOCKED | PLAYER text absent when required |
| SKIP | Validator not declared |

Story PASS is forbidden while mandatory Tier B semantic review remains unresolved.

---

## 5. Tier B mandatory review

Human review for: new-player understandability, timeline clarity without rereading, believable motivations, natural information delivery, neutral suspect presentation, understandable inference questions, engagement support, causally earned endings.

Engagement cannot be fully automated.

---

## 6. Related documents

- `STORY_VALIDATOR_SCHEMA.md`
- `STORY_VALIDATOR_REPORT_FORMAT.md`
- `INVESTIGATION_VALIDATOR_SPEC.md`
- `IDNE_ADVENTURE_QA_SPEC.md` §5.20

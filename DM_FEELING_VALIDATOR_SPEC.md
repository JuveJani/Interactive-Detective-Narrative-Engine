# DM Feeling Validator — Normative Specification

**Milestone:** 10  
**Status:** Normative  
**Validation:** `python3 -m idne.dm_feeling_validate`

## Purpose

Integrated validator determining whether an adventure feels like a **bounded simulated investigation** rather than a branching storybook, passive reading, clue checklist, or navigation menu.

Supports: `single_investigator`, `two_player`, static-book delivery, future AI-DM delivery.

Does **not** claim subjective enjoyment is fully automatable.

## Evaluation categories (reported separately)

1. Player agency  
2. Discovery vs delivery  
3. Exploration depth  
4. Inference quality  
5. Aha potential  
6. World responsiveness  
7. Time pressure (may delegate playtime calibration)  
8. Failure quality  
9. Conversation agency  
10. Ending causality  
11. Mode-specific quality  

## Outcomes

PASS | FAIL | CONDITIONAL_PASS | BLOCKED

DM Feeling PASS forbidden when mandatory Tier B or Tier C playtest evidence is missing.

## Tier separation

- **Script (Tier A):** structural metrics from canonical package + PLAYER scan  
- **Tier B:** semantic review with PLAYER excerpts export  
- **Tier C:** human playtest questionnaire (`DM_FEELING_PLAYTEST_QUESTIONNAIRE.md`)

## Reports

JSON stdout; optional Markdown and Tier B JSON under `DO_NOT_READ/dm_feeling_reports/`.

## Related

- `DM_FEELING_VALIDATOR_SCHEMA.md`
- `DM_FEELING_VALIDATOR_REPORT_FORMAT.md`
- `IDNE_ADVENTURE_QA_SPEC.md` §5.22

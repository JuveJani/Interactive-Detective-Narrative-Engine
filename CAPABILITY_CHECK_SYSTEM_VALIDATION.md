# Capability Check System — Validation

**Harness:** `python3 -m idne.capability_check_validate <adventure_root>`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.18

## Automated checks

| ID | Validates |
|---|---|
| CAP-PKG-PRESENT | Package exists |
| CAP-FIXED-TRUTH | No `changes_fixed_truth` |
| CAP-DOC-CONTENTS | No `changes_document_contents` |
| CAP-EVIDENCE-EXIST | No `changes_evidence_existence` |
| CAP-CAP-MISMATCH | Capability matches `parent_action_type` |
| CAP-MEANINGLESS | No meaningless/guaranteed roll gates |
| CAP-PASS-FAIL-UNIT | No combined outcome prose |
| CAP-FAIL-LEAK | Failure does not leak hidden success |
| CAP-REPEAT | One-attempt default not duplicated |
| CAP-FREE-RETRY | No free second-player retry |
| CAP-UNRELATED-CONCLUSION | Success does not grant full solution |
| CAP-ONLY-ROUTE | Mandatory checks have alternate routes |
| CAP-DESTINATIONS | Success/failure destinations declared |
| CAP-SAME-DEST | Pass/fail dest differ or justified |
| CAP-DUP-COST | No duplicated time costs |
| CAP-NPC-UNKNOWN | NPC does not reveal unknown info |
| CAP-INTIMIDATION-TRUST | Intimidation not treated as trust |
| CAP-PROVENANCE | Knowledge grants have trace |
| CAP-DC-JUST | DC has justification |
| CAP-GUARANTEED | Ordinary actions not gated |
| CAP-MODIFIER | Valid modifier/capability category |
| CAP-SOLO-P2 | Solo does not require Player 2 |
| CAP-STATE-CONFLICT | No object state contradiction |
| CAP-BARE-CODE | No bare J-/OBJ- choices |

## Tier B (semantic review)

CAP-B-01 capability matches task; CAP-B-02 DC proportionate; CAP-B-03 failure wording; CAP-B-04 meaningful tension; CAP-B-05 check frequency; CAP-B-06 failure fairness; CAP-B-07 social consistency.

## Fixtures

22 fixtures under `tests/fixtures/cap_*` (5 valid, 17 failure cases).

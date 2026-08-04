# Investigation Flow & Ending System — Validation

**Harness:** `python3 -m idne.investigation_flow_validate <adventure_root>`  
**Specs:** `INVESTIGATION_FLOW_SPEC.md`, `ENDING_SYSTEM_SPEC.md`  
**JSON Schema:** `idne/schemas/investigation_flow_package.schema.json`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.17

## Skip behavior

| Condition | Result |
|---|---|
| No `investigation_flow_manifest.json` and no `generation_manifest.investigation_flow.enabled` | SKIP |
| `investigation_flow_method` ≠ `canonical` | SKIP |

Harborview and legacy adventures: SKIP.

## Automated checks

| ID | Validates |
|---|---|
| FLOW-PKG-PRESENT | Package file exists |
| FLOW-STATE | `initial_state` keys declared in `state_model` |
| FLOW-SCENE-CHAIN | Time clocks, chain steps, knowledge references |
| FLOW-WORLD-VARIANT | Variant `when_state` references valid flags |
| FLOW-REVISIT | Location and knowledge references |
| FLOW-DEADLINE | Deadline ending exists, type `deadline`, no full truth leak |
| FLOW-ENDING-GRAPH | Graph nodes match endings, evaluation order valid |
| FLOW-TRUTH-LEAK | Imperfect endings MUST NOT `reveals_full_truth` or `complete` scope |
| FLOW-STATE-INCONSIST | Triggers reference unknown or contradictory state |
| FLOW-IMPOSSIBLE | Contradictory triggers, impossible-by-design markers |
| FLOW-UNSUPPORTED-ACCUSATION | Questionnaire conclusions have proofs; perfect accusation aligned |
| FLOW-UNREACHABLE | Unobtainable chain entry knowledge; `never_reachable` triggers |

## Tier B (manual / partial)

| ID | Validates |
|---|---|
| FLOW-B-01 | Fair-path reachability for perfect ending |
| FLOW-B-02 | Ending prose (Delivery) respects `max_knowledge_revealed_ids` |

## Tier C (playtest)

| ID | Validates |
|---|---|
| FLOW-H-01 | Players understand why each ending occurred from sheet state |

## Fixtures

Nine fixtures under `tests/fixtures/iflow_*`:

| Fixture | Expected failure |
|---|---|
| `iflow_valid_minimal` | PASS |
| `iflow_impossible_ending` | FLOW-IMPOSSIBLE |
| `iflow_deadline_missing` | FLOW-DEADLINE |
| `iflow_unsupported_accusation` | FLOW-UNSUPPORTED-ACCUSATION |
| `iflow_truth_leak` | FLOW-TRUTH-LEAK |
| `iflow_state_inconsistent` | FLOW-STATE-INCONSIST |
| `iflow_unreachable_chain` | FLOW-UNREACHABLE |
| `iflow_unreachable_ending` | FLOW-UNREACHABLE |
| `iflow_missing_questionnaire` | FLOW-UNSUPPORTED-ACCUSATION |

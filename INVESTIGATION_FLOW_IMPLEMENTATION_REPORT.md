# Investigation Flow & Ending System — Implementation Report

**Milestone:** 5C  
**Branch:** `cursor/investigation-flow-ending-bad4`  
**Status:** Complete

## Deliverables

- `INVESTIGATION_FLOW_SPEC.md` — state-driven flow, scene chains, variants, revisits
- `ENDING_SYSTEM_SPEC.md` — endings, graph, deadline, accusation, truth-reveal policy
- `INVESTIGATION_FLOW_VALIDATION.md`
- `idne/schemas/investigation_flow_package.schema.json`
- `idne/investigation_flow_validate.py` — 12 automated checks
- 9 fixtures, 10 unit tests

## Validation

- Full suite: **163 tests OK**
- `iflow_valid_minimal`: PASS
- 8 failure fixtures: FAIL (expected)
- Harborview: SKIP

## Design notes

- Replaces ending-condition tables with `state_driven` triggers on `endings`
- Perfect ending may reveal complete truth; all imperfect endings forbidden from `reveals_full_truth`
- Final accusation questionnaire binds to Investigation Core conclusions and proofs
- Scene chains, world-state variants, location revisits, and deadline ending supported

## Blockers / deferred

- Delivery Adapter ending prose audit (FLOW-B-02) — Tier B
- Full fair-path graph reachability (FLOW-B-01) — Tier B
- Harborview migration — not in scope

## Milestone 5C complete: **YES**

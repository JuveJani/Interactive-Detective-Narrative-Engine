# Object Interaction System — Validation

**Harness:** `python3 -m idne.object_interaction_validate <adventure_root>`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.14

## Automated (Tier A)

| Check | Failure |
|---|---|
| OBJ-PKG-PRESENT | Package missing |
| OBJ-DECLARED | Object/parent invalid |
| OBJ-NO-CYCLE | Cyclic containment |
| OBJ-CHILD-VIS | Child visible before parent |
| OBJ-HIDDEN-PARENT | Parent text reveals hidden children |
| OBJ-ACTION | Bad check, destinations, labels |
| OBJ-RETURN | Missing return route |
| OBJ-STATE | Transition/revisit conflicts |
| OBJ-COLLECTED | Collected item still present |
| OBJ-MANDATORY | Required info not grantable |
| OBJ-WF | Contradicts world truth |
| OBJ-BARE-CODE | Bare J/P/R/OBJ choices |
| OBJ-PASS-FAIL-UNIT | Both outcomes in one unit |

## Tier B

OBJ-B-01 neutral object descriptions; OBJ-B-02 failure unit prose audit.

## Tier C

OBJ-H-01 players describe actions not codes; OBJ-H-02 failed check does not telegraph miss.

## Fixtures

15 fixtures under `tests/fixtures/obj_*` per implementation report.

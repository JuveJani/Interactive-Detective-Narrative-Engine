# Investigation Core — Validation

**Harness:** `python3 -m idne.investigation_core_validate <adventure_root>`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.15

## Automated checks

| ID | Validates |
|---|---|
| INV-PKG-PRESENT | Package exists |
| INV-ENTITIES | Core sections populated |
| INV-EVIDENCE-PROV | Physical evidence provenance |
| INV-TESTIMONY-SRC | Testimony has NPC source |
| INV-ACQUISITION | Knowledge acquisition paths |
| INV-HYPOTHESIS | No auto-proved hypotheses |
| INV-CONCLUSION-PROV | Conclusions have proofs |
| INV-PROOF-INDEP | Independent proof routes |
| INV-CONTRADICTION | Contradiction resolution |
| INV-LEGACY-CLUE | Clues compatibility-only |
| INV-ORPHAN | Knowledge used in proof chain |

## Tier B

INV-B-01 fair-path reachability; INV-B-02 legacy clue not in proof drivers.

## Tier C

INV-H-01 players articulate knowledge not clue codes.

## Fixtures

12 fixtures under `tests/fixtures/inv_*`.

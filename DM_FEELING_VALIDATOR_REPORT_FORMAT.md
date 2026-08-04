# DM Feeling Validator — Report Format

**Harness:** `python3 -m idne.dm_feeling_validate <adventure_root>`

## JSON output

Includes `status`, `category_scores` (per category PASS/FAIL/CONDITIONAL_PASS), `checks`, `findings`, `tier_b_pending`, `tier_c_complete`, `report_paths`.

No single opaque overall percentage.

## Check keys

`DF-PKG-PRESENT`, `DF-STATE-GRAPH`, `DF-AGENCY`, `DF-DISCOVERY`, `DF-EXPLORATION`, `DF-INFERENCE`, `DF-AHA`, `DF-WORLD`, `DF-TIME`, `DF-FAILURE`, `DF-CONVERSATION`, `DF-ENDING`, `DF-MODE`, `DF-PLAYTIME-DELEGATE`

## Finding IDs (representative)

`DF-BARE-CODE`, `DF-UNEXPLAINED-CHOICE`, `DF-FAKE-BRANCH`, `DF-PASSIVE-READING`, `DF-AUTO-MAJOR-GRANT`, `DF-INFERENCE-THEATRE`, `DF-ANSWER-IN-QUESTION`, `DF-DIRECT-CONCLUSION`, `DF-RESET-LOCATION`, `DF-INERT-TIME`, `DF-IRRELEVANT-DEADLINE`, `DF-FAILURE-NO-EFFECT`, `DF-FAIL-LEAK`, `DF-EXPOSITION-MENU`, `DF-TRUST-UNUSED`, `DF-FINAL-CHOICE-ONLY`, `DF-ENDING-TRUTH-LEAK`, `DF-LITTLE-JOINT`, `DF-STATE-EXPLOSION`, `DF-TIER-B-*`, `DF-TIER-C-MISSING`

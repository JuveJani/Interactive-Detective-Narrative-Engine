# Investigation Validator — Report Format

**Harness:** `python3 -m idne.investigation_validate <adventure_root>`  
**Output:** JSON on stdout; exit code `0` for PASS/SKIP/CONDITIONAL_PASS, `1` for FAIL, `2` for BLOCKED.

---

## Top-level report

```json
{
  "adventure_root": "/path/to/adventure",
  "status": "PASS",
  "findings": [],
  "warnings": [],
  "checks": {
    "IV-PKG-PRESENT": "PASS",
    "IV-CAPABILITY-DELEGATE": "PASS",
    "IV-TRACE": "PASS",
    "IV-INFERENCE": "PASS",
    "IV-SUFFICIENCY": "PASS",
    "IV-RECOVERY": "PASS",
    "IV-ACCESS": "PASS",
    "IV-CHECK-FAIRNESS": "PASS",
    "IV-NPC": "PASS",
    "IV-TIME": "PASS",
    "IV-ENDING": "PASS",
    "IV-PLAY-MODE": "PASS",
    "IV-PLAYER": "PASS",
    "IV-STATE-GRAPH": "PASS"
  },
  "tier_b_pending": [],
  "state_graph": {
    "explored_states": 8,
    "max_depth_reached": 3,
    "truncated": false,
    "blocked": false,
    "reason": ""
  }
}
```

---

## Status values

| `status` | Meaning |
|---|---|
| `PASS` | No proven Tier A defects; Tier B mandatory resolved |
| `FAIL` | At least one proven Tier A finding |
| `CONDITIONAL_PASS` | Tier B mandatory pending or non-proven findings only |
| `BLOCKED` | State graph limit exceeded (`IV-STATE-GRAPH`: `BLOCKED`) |
| `SKIP` | Validator not declared on adventure |

---

## Check rollup IDs

| Check key | Layer |
|---|---|
| `IV-PKG-PRESENT` | Package exists |
| `IV-CAPABILITY-DELEGATE` | Delegated `capability_check_validate` |
| `IV-TRACE` | Conclusion traces complete |
| `IV-INFERENCE` | Inference answerability |
| `IV-SUFFICIENCY` | Information sufficiency |
| `IV-RECOVERY` | Recovery route executability |
| `IV-ACCESS` | Access solvability |
| `IV-CHECK-FAIRNESS` | Mandatory check fairness |
| `IV-NPC` | NPC disclosure routes |
| `IV-TIME` | Time-state validation |
| `IV-ENDING` | Ending reachability and accusation fairness |
| `IV-PLAY-MODE` | Solo / two-player constraints |
| `IV-PLAYER` | PLAYER cross-layer audit |
| `IV-STATE-GRAPH` | Integrated state graph (`PASS` or `BLOCKED`) |

---

## Finding categories (representative IDs)

| Finding ID | Scenario |
|---|---|
| `IV-INFERENCE-MISSING-INFO` | Required knowledge not obtainable |
| `IV-INFO-AFTER-INFERENCE` | Facts only after question |
| `IV-UNDEFINED-TERM` | Undefined term in question |
| `IV-EQUAL-ALTERNATIVES` | Equally supported unresolved answers |
| `IV-VAGUE-RECOVERY` | Vague recovery instruction |
| `IV-RECOVERY-BARE-CODE` | Bare page/code recovery |
| `IV-ZERO-COST-LOOP` | Zero-cost recovery loop |
| `IV-KEY-OWN-LOCK` | Key behind own lock |
| `IV-PASSWORD-NO-ROUTE` | Password without derivation |
| `IV-ITEM-CONSUMED-EARLY` | Mandatory item consumed early |
| `IV-CHECK-DESTROYS-ROUTES` | Check failure destroys all routes |
| `IV-NPC-UNREACHABLE` | NPC disclosure unreachable |
| `IV-UNDEFINED-TRUST` | Undefined trust condition |
| `IV-NPC-LEAVES-EARLY` | NPC leaves before interview |
| `IV-TIME-VARIANT` | Revisit ignores time variant |
| `IV-DEADLINE-EXCEEDED` | Mandatory paths exceed deadline |
| `IV-UNREACHABLE-ENDING` | Unreachable non-decorative ending |
| `IV-DECORATIVE-IMPOSSIBLE` | Decorative ending impossible trigger |
| `IV-ENDING-TRUTH-LEAK` | Imperfect ending leaks full truth |
| `IV-ACCUSATION-REVEALS` | Accusation reveals correct answer |
| `IV-PLAYER-NO-SOURCE` | PLAYER information without source |
| `IV-PLAYER-MISSING-ACTION` | Canonical action missing from PLAYER |
| `IV-PASS-FAIL-LEAK` | Pass/fail in same unit |
| `IV-DESTINATION-MISSING` | Result destination missing |
| `IV-LOCATION-RESET` | Location state resets on return |
| `IV-SOLO-REQUIRES-P2` | Solo route requires player 2 |
| `IV-TWO-PLAYER-PRIVATE` | Two-player private info unshared |
| `IV-STATE-EXPLOSION` | State graph blocked |

Tier B findings use prefix `IV-TIER-B-<review_id>`.

---

## Confidence and severity

- **proven** + **critical** + **tier A** → contributes to FAIL
- **likely** / **tier B** → CONDITIONAL_PASS when no proven A defects
- **human_approval_needed: true** → requires human sign-off before release

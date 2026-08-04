# Playtime Calibration — Report Format

**Harness:** `python3 -m idne.playtime_validate <adventure_root>`  
**Exit:** `0` PASS/SKIP/CONDITIONAL_PASS; `1` FAIL; `2` BLOCKED

## Top-level

```json
{
  "status": "PASS",
  "checks": {
    "PT-PKG-PRESENT": "PASS",
    "PT-METADATA": "PASS",
    "PT-TARGET": "PASS",
    "PT-TWO-PLAYER-FORMULA": "PASS",
    "PT-MUTEX": "PASS",
    "PT-ACTIVITIES": "PASS",
    "PT-SCARCITY": "PASS",
    "PT-SPLIT-BALANCE": "PASS",
    "PT-CALIBRATION": "PASS"
  },
  "estimate": {
    "wall_clock_median_minutes": 118.0,
    "wall_clock_shortest_minutes": 88.5,
    "wall_clock_longest_minutes": 135.7,
    "in_world_total_minutes": 480.0,
    "paths": [],
    "two_player": null
  },
  "findings": []
}
```

## Representative finding IDs

`PT-TARGET-HARD-LOW`, `PT-TARGET-HARD-HIGH`, `PT-PARALLEL-SUMMED`, `PT-MUTEX-SUMMED`, `PT-SIMPLE-AS-COMPLEX`, `PT-FAKE-DECISION-CREDIT`, `PT-CHECKBOX-PUZZLE`, `PT-SCARCITY-NO-PRESSURE`, `PT-DEADLINE-BEFORE-SOLUTION`, `PT-TIME-GATED-UNREACHABLE`, `PT-SPLIT-IMBALANCE`, `PT-METADATA-MISSING`, `PT-CAL-SINGLE-OBS`, `PT-CAL-ERROR`

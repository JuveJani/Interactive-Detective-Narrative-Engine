# Playtime Calibration — Schema

**Package:** `DO_NOT_READ/playtime_calibration_package.json`  
**Manifest:** `playtime_calibration_manifest.json`  
**Schemas:** `idne/schemas/playtime_calibration_package.schema.json`, `playtime_calibration_finding.schema.json`

## Key sections

| Section | Role |
|---|---|
| `target_playtime_minutes` | Authored target (e.g. 120) |
| `reading_assumptions` | Seconds/word, callback minutes |
| `activity_class_defaults` | Default bounds per activity class |
| `wall_clock_paths` | Path-specific activity lists |
| `two_player_model` | Joint, split windows, regroup, ending |
| `in_world_time` | In-world domain only |
| `coverage_assumptions` | Required vs optional exploration fractions |
| `time_scarcity` | Deadline effectiveness cross-check |
| `playtest_calibration` | Observations and recommendations |
| `tier_b_mandatory` | Human review items |

## Activity record (minimal)

```json
{
  "activity_id": "ACT-001",
  "activity_class": "simple_reading",
  "word_count": 300,
  "complexity": "simple",
  "authored_expected_minutes": 5
}
```

Example: `tests/fixtures/pt_valid_solo_120/DO_NOT_READ/playtime_calibration_package.json`

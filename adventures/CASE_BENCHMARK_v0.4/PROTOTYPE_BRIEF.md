# Harborview Arcade — v0.4 Benchmark Brief

**Engine:** IDNE v0.4  
**Source brief:** `/ADVENTURE_BRIEF.md`  
**Status:** Generated benchmark adventure

## Target experience

- ~120 minutes wall-clock cooperative play
- Player-directed hub investigation under time scarcity
- People / Records asymmetric cooperation
- Three infer worksheets; zero Auto major clues
- Five endings with sheet-checkable dispatch

## Engine features under test

See `BENCHMARK_CHECKLIST.md` for full gate traceability.

## Content budget (as built)

| Item | Count |
|---|---:|
| Major suspects | 4 |
| Primary locations | 5 |
| Active clues | 14 |
| Infer beats | 3 |
| Split windows | 2 |
| Clock thresholds | 3 |
| Checks | 4 |
| Terminal endings | 5 |

## Validation

- PLAYER structural validation: `python3 PLAYER/validate_player_package.py`
- Human playtest: **required** for v0.4 Ready (not yet recorded)

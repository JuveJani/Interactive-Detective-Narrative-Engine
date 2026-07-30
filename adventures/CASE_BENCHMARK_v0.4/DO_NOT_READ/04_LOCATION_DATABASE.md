# Location Database

**Adventure:** CASE_BENCHMARK_v0.4

---

## Primary locations (5)

### LOC_LOBBY — Front lobby

| Field | Value |
|---|---|
| Access | Always |
| Actions | Hub menus; brief Officer Park; orient |
| Clues | Orientation only (no major Auto) |

### LOC_STAIRWELL — Rear service stairwell

| Field | Value |
|---|---|
| Access | After J-110 |
| Actions | Examine pad, measure scuffs, photograph |
| Clues | `CLUE_C01` (Observe, Joint) |

### LOC_BAKERY — Harborview Bakery

| Field | Value |
|---|---|
| Access | Until T1 (20:00) for evening interview |
| Actions | Interview Mira, view camera still, speak to staff |
| Clues | `CLUE_C03`, `CLUE_C07` |
| T1 gate | After 20:00: bakery interview closed; fallback via staff phone (+15 min) |

### LOC_MANAGER — Manager office

| Field | Value |
|---|---|
| Access | Always with appointment |
| Actions | Interview Diane, request logs, request email access |
| Clues | `CLUE_C09`, `CLUE_C11` |
| Notes | Diane defensive; not steering |

### LOC_BASEMENT — Basement storage

| Field | Value |
|---|---|
| Access | Open until T3 (22:00); after T3 needs `ACCESS_MANAGER_KEY` (+10 min) |
| Actions | Search storage, tool board, mop area |
| Clues | `CLUE_C02`, `CLUE_C04`, `CLUE_C05`, `CLUE_C06`, `CLUE_C10` |
| T3 gate | Standard fair path uses basement before 22:00; fallback subpoena route +20 min, degraded certainty |

## Secondary (mention only)

- `LOC_DRYCLEAN` — closed unit; no visit required
- `LOC_UNIT_3B` — victim unit; sealed by police

## Locked / gated

| Location | Gate |
|---|---|
| LOC_BAKERY evening | T1 |
| LOC_BASEMENT extended | T3 without key |
| James lobby interview | T2 (he uses side entrance) |

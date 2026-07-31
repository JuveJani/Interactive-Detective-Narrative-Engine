# World State Variables

**Adventure:** CASE_BENCHMARK_v0.4

---

## Clock

| Variable | Start | Writers | Readers |
|---|---|---|---|
| `WORLD_CLOCK` | 19:00 | All action costs, sync max() | Hubs, endings, thresholds |

## Threshold flags

| Variable | Set by | Effect |
|---|---|---|
| `THRESHOLD_T1` | `WORLD_CLOCK >= 20:00` | Bakery evening interview closed |
| `THRESHOLD_T2` | `WORLD_CLOCK >= 21:00` | James lobby path closed |
| `THRESHOLD_T3` | `WORLD_CLOCK >= 22:00` | Basement requires key action |

## Proof tags (player sheet)

| Variable | Set by | Readers |
|---|---|---|
| `PROOF_METHOD` | C01+C04 or C10 | I03, endings |
| `PROOF_MOTIVE` | C05 or C11 or (MOTIVE_WITNESS and (C05 or C11 or C14)) | I02, I03, endings |
| `PROOF_OPPORTUNITY` | C06 + (C12 or C13) | I03, endings |
| `INFER_I01` | J-210 worksheet | Hub 2 |
| `INFER_I02` | J-410 worksheet | Hub 3 |
| `INFER_I03` | J-510 worksheet | Endings |

## Access

| Variable | Set by | Readers |
|---|---|---|
| `ACCESS_MANAGER_KEY` | P-112 or R-111 | T3 basement |
| `VISITED_STAIRWELL` | J-110 | Hub 1 |
| `VISITED_BASEMENT` | R-211 | — |

## Witness state (public tags only)

| Variable | Values | Writers |
|---|---|---|
| `MOTIVE_WITNESS` | set at P-112 | I02, endings |
| `WITNESS_MIRA` | COOPERATIVE / SHUT_DOWN | P-111, CHK_MIRA_CALM |
| `WITNESS_JAMES` | COOPERATIVE / SHUT_DOWN | P-211, CHK_JAMES_PRESS |

## Accusation

| Variable | Writers | Readers |
|---|---|---|
| `ACCUSED_NPC` | J-500 | Endings |

## Hidden (compiler-internal)

| Variable | Purpose |
|---|---|
| `SPLIT1_COMPLETE_A` | Sync tracking |
| `SPLIT1_COMPLETE_B` | Sync tracking |

Player text MUST NOT reference hidden variables.

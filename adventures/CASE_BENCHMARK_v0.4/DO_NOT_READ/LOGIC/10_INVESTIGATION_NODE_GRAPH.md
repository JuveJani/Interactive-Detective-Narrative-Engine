# Investigation Node Graph

**Adventure:** CASE_BENCHMARK_v0.4

---

## Graph summary

| Metric | Value |
|---|---:|
| Playable units | 25 |
| Terminal units | 5 |
| Split windows | 2 |
| Hubs | 3 |

---

## Flow

```text
J-100 → J-110 → J-120 (Hub 1)
  ├→ J-121 (Park briefing)
  ├→ J-130 (Split 1)
  │    ├ People: P-111 → P-112 / P-113
  │    └ Records: R-111 → R-112 → R-113
  └→ J-200 (Regroup) → J-210 (Infer I01) → J-300 (Hub 2)
        → J-330 (Split 2)
             ├ People: P-211 → P-212 → P-213
             └ Records: R-211 → R-212 → R-213
        → J-400 (Regroup) → J-410 (Infer I02) → J-500 (Hub 3)
        → J-510 (Infer I03) → J-600 → ENDINGS
```

---

## Hub 1 (J-120) — decision unit

| Action | Cost | Destination |
|---|---|---|
| Inspect the rear stairwell | 15 min | J-110 |
| Speak with Officer Park in the lobby | 10 min | J-121 |
| Interview bakery staff and tenant | 20 min | J-130 (People path) |
| Pull building records from manager | 20 min | J-130 (Records path) |
| Review case notes together | 10 min | J-122 |

No consequences listed on J-120.

---

## Hub 2 (J-300) — decision unit

| Action | Cost | Destination | Gate |
|---|---|---|---|
| Interview fourth-floor tenant Holt | 25 min | J-330 People | — |
| Search basement storage | 25 min | J-330 Records | T3: needs key if ≥22:00 |
| Revisit stairwell measurements | 15 min | J-110 | once per hub |
| Request manager key for basement | 10 min | sets ACCESS_MANAGER_KEY | if T3 |
| Review timeline on case sheet | 10 min | J-301 | — |

---

## Hub 3 (J-500) — decision unit

| Action | Cost | Destination |
|---|---|---|
| File accusation against a suspect | 15 min | J-510 |
| Request final lab comparison | 20 min | J-511 (optional C10 boost) |
| File without accusation | 10 min | E-905 |
| Wait for clock expiry | — | E-904 if ≥23:00 |

---

## Wall-clock estimate

| Segment | Minutes |
|---|---:|
| Joint opening (J-100–J-130) | 38 |
| Split 1 max | 10 |
| Regroup + Infer 1 | 18 |
| Hub 2 + launch | 8 |
| Split 2 max | 12 |
| Regroup + Infer 2–3 + end | 35 |
| Buffer | 9 |
| **Total** | **~120** |

Longest individual branch: ~55 min (Records split 2 full path + joint blocks)

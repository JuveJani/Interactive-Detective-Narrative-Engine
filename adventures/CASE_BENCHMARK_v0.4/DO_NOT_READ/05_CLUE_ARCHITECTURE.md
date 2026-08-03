# Clue Architecture

**Adventure:** CASE_BENCHMARK_v0.4  
**Active clues:** 14  
**Infer beats:** 3

---

## Clue register

| ID | Title | Mode | Category | Grants |
|---|---|---|---|---|
| CLUE_C01 | Scuff and wet transfer pattern | Observe | Method | Joint stairwell exam |
| CLUE_C02 | Broken storage latch | Observe | Method | Records basement search |
| CLUE_C03 | Camera entry timestamp | Earn | Opportunity | Records bakery stills |
| CLUE_C04 | Mop bucket placement | Observe | Method | Records basement |
| CLUE_C05 | Duplicate vendor invoices | Earn | Motive | Records invoice check (CHK_01) |
| CLUE_C06 | Tool sign-out discrepancy | Earn | Opportunity | Records tool board |
| CLUE_C07 | Rent dispute timeline | Earn | Motive (red herring) | People Mira interview |
| CLUE_C08 | James visit admission | Earn | Opportunity (red herring) | People James (CHK_02) |
| CLUE_C09 | Diane–Okonkwo alibi block | Earn | Opportunity | People/Records cross |
| CLUE_C10 | Boot impression partial | Earn | Method | Records (CHK_03) |
| CLUE_C11 | Elena draft complaint email | Earn | Motive | Records manager files |
| CLUE_C12 | Okonkwo thump timing | Earn | Opportunity | People Okonkwo |
| CLUE_C13 | Gym receipt timestamp | Earn | Opportunity | People James follow-up |
| CLUE_C14 | Maintenance vendor phone log | Earn | Motive | Records basement file |

**Auto major clues:** 0  
**Orientation Auto (minor):** building map on J-100 only — not counted as major

---

## Acquisition mode totals

| Mode | Count |
|---|---:|
| Observe | 4 |
| Earn | 10 |
| Infer | 3 (worksheet beats) |
| Auto (major) | 0 |

---

## Infer beats

| ID | When | Inputs required | Output |
|---|---|---|---|
| INFER_I01 | J-210 | C01 + C06 | Eliminate pure accident theory (method/opportunity) |
| INFER_I02 | J-410 | C05 + C07 + C11 | Rent dispute insufficient motive; fraud line |
| INFER_I03 | J-500 | C06 + C10 + C12 + motive line | Name opportunity+method toward Tomás |

---

## Redundancy (fair paths)

**Route A (records-heavy):** C05, C06, C10, C11 → I02, I03  
**Route B (people-heavy):** C07, C08, C12, C13 + C06 from split → I01, I03

Both reach `END_CORRECT` with method+motive+opportunity.

---

## Dependency graph (simplified)

```text
C01 ──┬── I01 ──┐
C06 ──┘         ├── I03 ── END_CORRECT
C05 ──┬── I02 ──┤
C11 ──┘         │
C10 ────────────┘
C07 (red herring) ── misleads only if alone
```

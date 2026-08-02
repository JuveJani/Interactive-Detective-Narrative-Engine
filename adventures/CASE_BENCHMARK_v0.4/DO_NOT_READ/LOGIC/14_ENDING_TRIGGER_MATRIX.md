# Ending Trigger Matrix

**Adventure:** CASE_BENCHMARK_v0.4

---

## Evaluation order

| Priority | Ending | Conditions |
|---:|---|---|
| 1 | E-904 TIMEOUT | `WORLD_CLOCK >= 23:00` |
| 2 | E-905 DECLINE | Hub 3 action = decline |
| 3 | E-901 CORRECT | `ACCUSED` set AND `PROOF_METHOD` AND `PROOF_MOTIVE` AND `PROOF_OPPORTUNITY` AND `INFER_I03` AND evaluator matches truth |
| 4 | E-902 WRONG | `ACCUSED` set AND any proof tag AND NOT E-901 conditions |
| 5 | E-903 INCOMPLETE | `ACCUSED` set AND missing proof tag |

---

## Proof tag logic

### PROOF_METHOD

`(CLUE_C01 AND CLUE_C04) OR CLUE_C10`

### PROOF_MOTIVE

`CLUE_C05 OR CLUE_C11 OR (MOTIVE_WITNESS AND (CLUE_C05 OR CLUE_C11 OR CLUE_C14))`

### PROOF_OPPORTUNITY

`CLUE_C06 AND (CLUE_C12 OR CLUE_C13)`

---

## Wrong-accusation feedback mapping

| Accused | Misleading clue if primary |
|---|---|
| Mira | C07 alone |
| James | C08 alone |
| Diane | Incomplete visitor copy anxiety |

---

## Reachability

Each ending reachable on at least one legal path per v0.4 §8.4.

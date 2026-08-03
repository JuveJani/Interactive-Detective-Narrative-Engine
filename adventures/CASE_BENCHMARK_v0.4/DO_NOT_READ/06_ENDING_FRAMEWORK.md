# Ending Framework

**Adventure:** CASE_BENCHMARK_v0.4

---

## Priority order (highest first)

1. `END_TIMEOUT` — clock ≥ 23:00
2. `END_DECLINE` — Hub 3 decline chosen
3. `END_CORRECT` — Tomás + proof set
4. `END_WRONG` — innocent accused with partial set
5. `END_INCOMPLETE` — accusation without required categories

---

## Terminal definitions

### END_CORRECT (E-901)

**Requires on case sheet:**

- Accused: Tomás Reyes
- `PROOF_METHOD` tag set (C01 or C10 + C04)
- `PROOF_MOTIVE` tag set (C05 or C11)
- `PROOF_OPPORTUNITY` tag set (C06 + C12 or C13 eliminated others)
- `INFER_I03` completed

**Feeling:** Earned certainty — narrative cites causal chain.

### END_WRONG (E-902)

**Requires:**

- Accused: Mira, James, or Diane
- At least one proof tag set (players acted on theory)

**Feeling:** Consequence clarity — which clue misled.

### END_INCOMPLETE (E-903)

**Requires:**

- Accused anyone
- Missing any of METHOD / MOTIVE / OPPORTUNITY tags

### END_TIMEOUT (E-904)

**Requires:**

- `CLOCK >= 23:00` without earlier terminal

**Feeling:** Bitter plausibility — report filed incomplete.

### END_DECLINE (E-905)

**Requires:**

- Hub 3: "File without accusation" chosen

**Feeling:** Qualified relief / professional cost.

---

## Player communication

Ending pages cite satisfied sheet conditions and narrate causation per v0.4 §8.3.

No honor-system "were you right?"

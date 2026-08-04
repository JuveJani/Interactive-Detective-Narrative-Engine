# Playtime Calibration — Normative Specification

**Milestone:** 9 — Playtime Calibration  
**Status:** Normative  
**Validation:** `python3 -m idne.playtime_validate`  
**Estimation:** `idne.playtime_estimate`

---

## 1. Purpose

Canonical **real wall-clock playtime** model for IDNE adventures — separate from in-world time.

Supports: `single_investigator`, `two_player`, static book/PDF delivery, future AI-DM delivery.

Does **not** judge literary quality or pad duration with meaningless prose.

---

## 2. Time domains (never combined)

| Domain | Examples |
|---|---|
| **In-world time** | Walking, searching, NPC questioning, waiting for events |
| **Wall-clock playtime** | Reading, discussing, deciding, rolling, note-taking, puzzles, navigation |

---

## 3. Solo formula (§5.4.1 aligned)

```text
estimated_wall_clock = sum(sequential activities along legal path) + ending
```

Components: opening/setup, reading, inspection, decisions, checks, notes, inference, puzzles, navigation, revisits, recovery, ending.

**MUST NOT** use word count alone or two-player split formula.

---

## 4. Two-player formula (§5.4 aligned)

```text
estimated_wall_clock =
    sum(joint activities)
  + sum_over_split_windows(max(branch_A, branch_B))
  + regroup/discussion
  + ending
```

Also report: per-player active/waiting time, split imbalance, shared vs private time.

**MUST NOT** sum both players' parallel reading times.

---

## 5. Activity taxonomy

Reusable classes: simple/complex reading, rereading, decisions, navigation, dice/check, note-taking, object search, clue comparison, callback lookup, inference, puzzles (simple/medium/complex), NPC conversation, player discussion, failed-inference recovery, revisit, ending questionnaire/reading, joint scene, regroup.

Each activity declares estimation method, lower/expected/upper bounds, confidence, authored metadata.

---

## 6. Reading model (configurable baseline)

- Simple text: ~1 second/word  
- Complex text: ~2 seconds/word  
- Rereading expected: full reading again + 10 seconds  
- Callback lookup: +2 minutes (recent) or +5 minutes (≥1 hour earlier)

---

## 7. Path-sensitive estimation

Per valid path report: shortest, median expected, longest before deadline, intended target, perfect ending, common imperfect paths.

Stated playtime **MUST NOT** sum all optional mutually exclusive content.

---

## 8. Target compliance bands (default)

| Band | Range (% of target) |
|---|---|
| Hard fail low | &lt; 75% |
| Hard fail high | &gt; 140% |
| Major warning | &lt; 85% or &gt; 120% |

Report shows raw predicted minutes.

---

## 9. Playtest calibration

Record predicted vs actual per playtest. Multiple observations required before changing global defaults. Single playtest cannot alter canonical model.

---

## 10. Validation outcomes

PASS | FAIL | CONDITIONAL_PASS | BLOCKED (missing timing metadata)

---

## Related

- `PLAYTIME_CALIBRATION_SCHEMA.md`
- `IDNE_ENGINE_v0.4.md` §5.4, §5.4.1
- `IDNE_ADVENTURE_QA_SPEC.md` §5.21

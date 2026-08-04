# World-First Generation — Migration Guide

**Audience:** Authors, generators, QA operators  
**See also:** `WORLD_FIRST_GENERATION_SPEC.md`, `SINGLE_INVESTIGATOR_MODE_SPEC.md`

---

## 1. What changes for new adventures

### 1.1 Generation order

New adventures MUST follow World-First layer order (Spec §6). The Delivery Adapter MUST NOT run before G-WF7.

### 1.2 Required artifacts

| Artifact | Purpose |
|---|---|
| `generation_manifest.json` | Declares `world_first` and gate status |
| `DO_NOT_READ/world_truth_package.json` | Machine-readable truth layers |
| Human-readable World Bible | MAY be generated from package for review |

### 1.3 Validation in pipeline

- Stage 2 (Generation): record gate PASS at each layer stop
- Stage 3 (Hygiene): run `python3 -m idne.world_first_validate`
- Stage 4 (Adventure QA): WF-B review + standard QA

### 1.4 Play modes

World-First is mode-independent. One truth package feeds both `single_investigator` and `two_player` delivery when dual-mode is declared.

---

## 2. What remains unchanged

- Engine immutable principles U1–U12
- Single Investigator Mode (Milestone 1)
- Two-player cooperation rules for legacy and new two-player delivery
- Adventure QA spoiler, fairness, navigation checks
- Hygiene validators
- Check mechanics (fixed-world principle unchanged — enforced, not redesigned)
- Clue modes (Observe/Earn/Infer/Auto) — delivery taxonomy unchanged

---

## 3. Why existing adventures are not automatically World-First

Harborview (`CASE_BENCHMARK_v0.4`) and The Glass Alibi were generated under prior workflow:

```text
World Bible (prose) → Logic → PLAYER
```

They lack `generation_manifest.json` and `world_truth_package.json`. Validator returns **SKIP** — not a failure, not World-First certified.

These adventures MAY contain retroactive consistency enforced by human revision (Harborview v0.4.1 QA), but they were not machine-gated layer-by-layer at generation time.

**Do not convert** existing adventures in Milestone 2.

---

## 4. Retroactive explanation failure class

Benchmark playtests and pre-playtest review identified defects consistent with scene-first generation:

| Failure class | World-First prevention |
|---|---|
| Culprit in ending/spoiler text | Endings derived from Fixed Truth only |
| Clues without causal source | Evidence Provenance gate |
| NPC knowledge gaps | NPC Knowledge Model gate |
| Timeline ambiguity | Explicit timestamps + day_label |
| Scene invents fact | Narrative Construction after observable layer |
| Check creates evidence | Fixed-world invariant §4 |

Root cause for many Harborview Critical fixes: **delivery layer owned facts** that logic layer should have fixed first. World-First blocks scene generation until truth is complete.

---

## 5. How to declare and prove World-First

### Checklist

- [ ] `generation_manifest.json` with `generation_method: world_first`
- [ ] Complete `world_truth_package.json` per schema
- [ ] Gates G-WF1–G-WF6 PASS before scenes authored
- [ ] `world_first_validate` → PASS
- [ ] WF-B Critical review complete
- [ ] Standard Adventure QA PASS

### Proof artifacts

1. Validator JSON output
2. Gate status in manifest matching validator
3. QA report §5.12 rows
4. Optional: human sign-off WF-H-01 through WF-H-04

---

## 6. Generator migration

Generators MUST:

- Implement layer-stopped authoring with gate recording
- Revalidate dependent layers on upstream changes
- Emit manifest + package before PLAYER
- Run `world_first_validate` in CI for World-First adventures

Generators MUST NOT:

- Emit scenes before G-WF7
- Add clues without evidence provenance
- Auto-convert legacy adventures

---

## 7. FAQ

**Does World-First replace World Bible markdown?**  
No — markdown remains useful for human review; package is the machine gate.

**Does this start Environment or Object systems?**  
No — Milestone 3+.

**Can I waive WF checks?**  
Critical WF-B checks follow standard QA waiver rules (Critical never waived).

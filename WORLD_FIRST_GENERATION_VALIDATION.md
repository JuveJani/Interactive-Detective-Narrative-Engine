# World-First Generation — Validation Specification

**Harness:** `python3 -m idne.world_first_validate <adventure_root>`  
**QA cross-reference:** `IDNE_ADVENTURE_QA_SPEC.md` §5.12  
**Spec:** `WORLD_FIRST_GENERATION_SPEC.md`

---

## 1. Applicability

| Condition | Validator result |
|---|---|
| No `generation_manifest.json` | `SKIP` — not World-First |
| `generation_method` ≠ `world_first` | `SKIP` |
| World-First declared | `PASS` or `FAIL` |

`SKIP` is not PASS for World-First readiness.

---

## 2. Generation gates (automated)

| Gate / Check | Validates | Tier |
|---|---|---|
| **G-WF1** | Fixed Truth fields + immutable_facts | A |
| **G-WF2** | Timeline order, causes exist, no time-before-cause | A |
| **G-WF3** | Snapshots reference valid events; presence consistency | A |
| **G-WF4** | NPC knows only witness-derived facts | A |
| **G-WF5** | Evidence `source_event_id` valid | A |
| **G-WF6** | Conclusion `required_fact_ids` obtainable | A |
| **G-WF7** | Scenes only if gates pass; no invented facts/culprit | A |

---

## 3. Additional automated checks

| Check ID | Failure condition | Tier |
|---|---|---|
| **WF-PKG-PRESENT** | Package file missing | A |
| **WF-TIME-AMBIGUOUS** | Vague timestamp (`evening`, `later`, etc.) | A |
| **WF-TRAVEL-PRESENCE** | NPC at location without event participation | A |
| **WF-NPC-OVERKNOW** | NPC knows without witness chain | A |
| **WF-EVIDENCE-SOURCE** | Evidence without source event | A |
| **WF-CONCLUSION-COVERAGE** | Required facts not learnable | A |
| **WF-SCENE-TRUTH** | Scene asserts unknown fact or wrong culprit | A |
| **WF-ENDING-TRUTH** | Ending claims unestablished facts | A |

---

## 4. AI-review checks (Tier B)

Subjective mystery quality is **not** fully automatable.

| Check ID | Reviewer task | Severity |
|---|---|---|
| **WF-B-01** | Misleading evidence has believable timeline cause | Major |
| **WF-B-02** | False beliefs have documented causes | Major |
| **WF-B-03** | No equally valid alternate culprit on fair path (QA-FR-02 class) | Critical |
| **WF-B-04** | Observable layer covers all proof-critical facts | Critical |
| **WF-B-05** | Player text does not telegraph culprit (QA-FR-03 class) | Critical |
| **WF-B-06** | Checks are fixed-world — fail does not erase evidence | Major |
| **WF-B-07** | Off-screen events documented in timeline, not scenes | Major |
| **WF-B-08** | Dual-mode adventures: same truth package for both play modes | Major |

AI MUST cite package IDs and quotes for every FAIL.

---

## 5. Human-review checks (Tier C)

| Check ID | Measures |
|---|---|
| **WF-H-01** | Author confirms generation followed layer order |
| **WF-H-02** | Blind culprit read before mid-case Infer (playtest) |
| **WF-H-03** | Timeline readable by non-author reviewer |
| **WF-H-04** | Gate sign-off per layer before scenes authored |

---

## 6. Pre-Playtest Ready (World-First adventures)

When `generation_method` is `world_first`:

1. `world_first_validate` → `PASS`
2. All Critical WF-B checks reviewed
3. Gate records in manifest match validator outcomes
4. Standard Adventure QA (spoiler, fairness, navigation) still applies

---

## 7. Regression fixtures

| Fixture | Expected |
|---|---|
| `tests/fixtures/wf_valid_minimal` | PASS |
| `tests/fixtures/wf_contradictory_timeline` | FAIL |
| `tests/fixtures/wf_npc_overknow` | FAIL |
| `tests/fixtures/wf_evidence_no_source` | FAIL |
| `tests/fixtures/wf_conclusion_missing` | FAIL |
| `tests/fixtures/wf_ambiguous_date` | FAIL |
| `tests/fixtures/wf_scene_contradicts_truth` | FAIL |

---

## 8. What automation cannot claim

- Narrative quality, pacing, emotional stake
- Whether investigation *feels* open vs linear
- Full travel-time physics across complex geographies
- Complete proof-path uniqueness without logic graph integration
- Language localization load

These remain Tier B/C per `IDNE_ADVENTURE_QA_SPEC.md`.

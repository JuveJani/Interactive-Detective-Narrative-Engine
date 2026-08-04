# Environment System — Validation Specification

**Harness:** `python3 -m idne.environment_validate <adventure_root>`  
**QA:** `IDNE_ADVENTURE_QA_SPEC.md` §5.13

---

## 1. Applicability

| Condition | Result |
|---|---|
| No environment manifest | `SKIP` |
| `environment_method` ≠ `canonical` | `SKIP` |
| Canonical declared | `PASS` or `FAIL` |

---

## 2. Automated checks (Tier A)

| Check ID | Failure condition |
|---|---|
| ENV-PKG-PRESENT | Package missing |
| ENV-LOC-DECLARED | Empty locations |
| ENV-FEAT-LOC | Feature without valid `location_id` |
| ENV-STATE-CAUSE | State/transition without `cause` |
| ENV-NAV-DECLARED | Nav source/dest undeclared; bad `player_label` |
| ENV-NAV-RETURN | Broken `return_nav_id`; one-way without justification |
| ENV-TRANS-CAUSE | Transition without cause |
| ENV-REVISIT-PERSIST | Conflicting revisit reset vs persist |
| ENV-VIS-HIDDEN | Hidden feature in `exposed_feature_ids` |
| ENV-MANDATORY-ACCESS | Mandatory location `access: impossible` |
| ENV-MANDATORY-REACH | Mandatory location unreachable in nav graph |
| ENV-WF-LINK | Missing provenance; contradicts truth package |
| ENV-BARE-CODE | Player choice is bare node code (`Go to J-223`, etc.) |

---

## 3. AI-review (Tier B)

| Check ID | Task | Severity |
|---|---|---|
| ENV-B-01 | Neutral location prose — no spotlight | Critical |
| ENV-B-02 | Access condition has visible or canonical basis | Major |
| ENV-B-03 | Time variant readable to player | Major |
| ENV-B-04 | Feature visible in PLAYER matches canonical visibility | Major |
| ENV-B-05 | No failed-check content in environment text | Critical |
| ENV-B-06 | Dual-mode: same environment for both play modes | Major |

---

## 4. Human playtest (Tier C)

| Check ID | Measures |
|---|---|
| ENV-H-01 | Players navigate by place names, not codes |
| ENV-H-02 | Revisit preserves physical changes |
| ENV-H-03 | Exploration feels non-linear within bounds |
| ENV-H-04 | No hidden mandatory location frustration |

---

## 5. Regression fixtures

| Fixture | Expected |
|---|---|
| `env_valid_minimal` | PASS |
| `env_undeclared_dest` | FAIL |
| `env_feature_no_location` | FAIL |
| `env_hidden_exposed` | FAIL |
| `env_unexplained_transition` | FAIL |
| `env_broken_return` | FAIL |
| `env_state_reset_revisit` | FAIL |
| `env_bare_page_code` | FAIL |
| `env_impossible_access` | FAIL |
| `env_wf_contradict` | FAIL |

---

## 6. Non-automatable

Subjective sense of space, aesthetic description quality, and full travel-time physics remain human/AI review.

# Adventure QA Report Template

**Spec:** `IDNE_ADVENTURE_QA_SPEC.md`  
**Instructions:** Copy this file to `adventures/<ADVENTURE>/QA/ADVENTURE_QA_REPORT.md` (or repo root `QA_REPORTS/`) and fill every section. Do not delete check rows — mark N/A only with justification.

---

## 0. Header

| Field | Value |
|---|---|
| Adventure name / folder | |
| Engine version | IDNE v0.4 |
| Brief / codename | |
| QA date | |
| QA operator(s) | |
| Generation commit / PR | |
| Hygiene validation | PASS / FAIL — link: |
| Tier A suite run ID / log | |
| Tier B reviewer (AI or human) | |
| **Gate status** | QA FAIL / Pre-Playtest Ready / Waived Ready / Adventure Ready |

---

## 1. Executive result

| Band | Count PASS | Count FAIL | Count WAIVED | Count N/A |
|---|---:|---:|---:|---:|
| Critical | | | | |
| Major | | | | |
| Minor | | | | |

**One-paragraph summary:**  
_(What would a playtester most likely experience? What blocks Ready?)_

**Global evaluation answers (spec §11):**

| Question | Answer (Yes/No + note) |
|---|---|
| 1. Book reveals culprit without Infer? | |
| 2. One name dominates first hour? | |
| 3. One silent player still completes proof? | |
| 4. Hub first-option ≈ all options? | |
| 5. Ignoring clock changes nothing? | |
| 6. Mid-game rules already reveal outcome? | |

---

## 2. Inputs reviewed

| Input | Path | Reviewed |
|---|---|---|
| Adventure Brief | | ☐ |
| World Bible / Case Overview | | ☐ |
| Clue architecture / proof matrix | | ☐ |
| Ending trigger matrix | | ☐ |
| Logic graph / split flow | | ☐ |
| PLAYER package (all) | | ☐ |
| Compilation / estimate report | | ☐ |
| Prior QA / playtest notes | | ☐ |

---

## 3. Tier A — Automated results

Paste machine summary or check boxes after script run.

| Check ID | Result | Evidence / metric | Notes |
|---|---|---|---|
| QA-SP-03 | PASS / FAIL | | |
| QA-NS-01 | PASS / FAIL / REVIEW | | |
| QA-NS-04 | PASS / FAIL | | |
| QA-ST-01 | PASS / FAIL / REVIEW | | |
| QA-FA-01 | PASS / FAIL | | |
| QA-IN-02 | PASS / FAIL | | |
| QA-CL-01 | PASS / FAIL | | |
| QA-CL-04 | PASS / FAIL | | |
| QA-RC-01 | PASS / FAIL | | |
| QA-RC-03 | PASS / FAIL | | |
| QA-NV-01 | PASS / FAIL | | |
| QA-NV-02 | PASS / FAIL | | |
| QA-NV-03 | PASS / FAIL | | |
| QA-TM-04 | PASS / FAIL | | |
| QA-SI-01 | PASS / FAIL / N/A | | Solo only — validator JSON |
| QA-SI-02 | PASS / FAIL / N/A | | |
| QA-SI-03 | PASS / FAIL / N/A | | |
| QA-SI-04 | PASS / FAIL / N/A | | |
| QA-SI-11 | PASS / FAIL / N/A | | |

**Partial auto → escalate to Tier B:**

| Check ID | Auto signal | Tier B disposition |
|---|---|---|
| QA-SP-01 | | |
| QA-FA-02 | | |
| QA-CL-03 | | |
| QA-RC-02 | | |
| QA-NV-04 | | |
| QA-TM-03 | | |
| QA-FR-01 | | |
| QA-FR-05 | | |

---

## 4. Tier B — AI / structured review

For each FAIL: quote player-facing text. For each Critical PASS: state why failure class is absent.

### 4.1 Spoilers & spotlight

| Check ID | Result | Severity | Quote / evidence | Disposition |
|---|---|---|---|---|
| QA-SP-01 | | Critical | | |
| QA-SP-02 | | Critical | | |
| QA-SP-04 | | Major | | |
| QA-NS-02 | | Major | | |
| QA-NS-03 | | Critical | | |
| QA-FR-03 | | Critical | | |

### 4.2 Steering & agency

| Check ID | Result | Severity | Quote / evidence | Disposition |
|---|---|---|---|---|
| QA-ST-02 | | Major | | |
| QA-ST-03 | | Major | | |
| QA-ST-04 | | Major | | |
| QA-FA-03 | | Major | | |

### 4.3 Inference & clues

| Check ID | Result | Severity | Quote / evidence | Disposition |
|---|---|---|---|---|
| QA-IN-01 | | Critical | | |
| QA-IN-03 | | Major | | |
| QA-CL-02 | | Major | | |
| QA-CL-03 | | Critical | | |

### 4.4 Roles, navigation, time, fairness

| Check ID | Result | Severity | Quote / evidence | Disposition |
|---|---|---|---|---|
| QA-RC-02 | | Major | | |
| QA-RC-04 | | Critical | | |
| QA-NV-05 | | Major | | |
| QA-TM-01 | | Major | | |
| QA-TM-02 | | Major | | |
| QA-TM-03 | | Critical | | |
| QA-FR-01 | | Critical | | |
| QA-FR-02 | | Critical | | |
| QA-FR-04 | | Major | | |
| QA-FR-05 | | Critical | | |
| QA-SI-05 | | Critical | | Solo only |
| QA-SI-06 | | Major | | Solo only |
| QA-SI-09 | | Critical | | Solo only |
| QA-SI-10 | | Critical | | Solo only — conclusions path |

---

## 5. Waivers

Critical waivers are **forbidden**.

| Check ID | Severity | Reason | Mitigation | Approver | Expiry / version |
|---|---|---|---|---|---|
| | Major | | | | |

---

## 6. Issue register (all FAIL / REVIEW)

| ID | Check | Severity | Summary | Player impact | Recommended fix class | Status |
|---|---|---|---|---|---|---|
| ISS-01 | | | | | content / logic / delivery | open / fixed |

---

## 7. Pre-playtest gate decision

| Criterion | Met? |
|---|---|
| Hygiene PASS | ☐ |
| All Critical PASS | ☐ |
| All Major PASS or waived | ☐ |
| Tier A run attached | ☐ |
| Tier B Critical/Major complete | ☐ |
| This report filed | ☐ |

**Decision:** ☐ QA FAIL  ☐ Pre-Playtest Ready  ☐ Waived Ready

**Decision rationale:**  
_

**Signed:** _________________ **Date:** ________

---

## 8. Tier C — Human playtest (post gate)

_Complete after Pre-Playtest Ready. Required for Adventure Ready._

### 8.1 Session metadata

| Field | Value |
|---|---|
| Date | |
| Players (roles) | |
| Facilitator | |
| Recorded? (notes/audio) | |
| Actual wall-clock minutes | |
| Estimated wall-clock minutes | |
| Longest wait (minutes, which split) | |

### 8.2 Human checks

| Check ID | Result | Notes / quotes |
|---|---|---|
| QA-HP-01 Lived wall-clock (±15) | PASS / FAIL | |
| QA-HP-02 Felt agency | PASS / FAIL | |
| QA-HP-03 Idle wait ≤5 | PASS / FAIL | |
| QA-HP-04 Culprit lock timing | PASS / FAIL | |
| QA-HP-05 Infer ownership | PASS / FAIL | |
| QA-HP-06 Cooperation ≥3/5 both | PASS / FAIL | |
| QA-HP-07 Ending clarity | PASS / FAIL | |
| QA-HP-08 Confusion stalls <3 | PASS / FAIL | |
| QA-HP-09 Stake recall | PASS / FAIL | |
| QA-HP-10 Language load | PASS / FAIL | |

### 8.3 Player debrief (raw)

1. When did you first suspect someone, and why?  
2. What decision felt most meaningful?  
3. What felt fake or guided?  
4. Did both of you matter to the solution?  
5. Did the ending follow from your sheet?

### 8.4 Final Ready decision

| Criterion | Met? |
|---|---|
| Pre-Playtest Ready still holds | ☐ |
| All Tier C Critical/Major experience fails addressed or waived | ☐ |

**Decision:** ☐ Adventure Ready  ☐ Return to QA FAIL  ☐ Limited Ready (document)

**Signed:** _________________ **Date:** ________

---

## 9. Appendix — metrics dump

_Paste automated JSON / tables here._

```text
(name frequencies, hub collisions, clue mode counts, role grant %, wall-clock formula)
```

---

*Template version: 1.0 — aligned to IDNE_ADVENTURE_QA_SPEC.md*

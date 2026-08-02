# Harborview Arcade v0.4.1 — Adventure QA Report

**Adventure:** `adventures/CASE_BENCHMARK_v0.4/`  
**Version:** 0.4.1  
**Spec:** `IDNE_ADVENTURE_QA_SPEC.md`  
**Prior review:** `HARBORVIEW_PRE_PLAYTEST_REVIEW.md`  
**QA date:** 2026-07-31  
**Gate status:** **Pre-Playtest Ready** (pending human Tier C)

---

## 1. Executive result

| Band | PASS | FAIL | WAIVED | N/A |
|---|---:|---:|---:|---:|
| Critical (pre-review) | 4 | 0 | 0 | 0 |
| Major (pre-review) | 9 | 0 | 2 | 0 |
| Minor (pre-review) | 2 | 0 | 3 | 0 |

**Structural validation:** `python3 PLAYER/validate_player_package.py` → **PASS**

### Critical elimination statement

**Every Critical issue identified in `HARBORVIEW_PRE_PLAYTEST_REVIEW.md` has been eliminated in v0.4.1:**

| Review ID | Issue | v0.4.1 status |
|---|---|---|
| S1 | Culprit named in J-600 | **ELIMINATED** — proof-tag dispatch only |
| S2 / H2 | I-01 parenthetical answer | **ELIMINATED** |
| H1 | Forced C-01 before hub | **ELIMINATED** — stairwell is hub choice |
| I1 | Tomás over-spotlight (finder + I-01 focus) | **ELIMINATED** — neutral briefing; C-15 earned at interview; generic infer language |

---

## 2. Pre-playtest review remediation map

### Major issues

| Review ID | Issue | v0.4.1 status | Evidence |
|---|---|---|---|
| S3 | E-904 names Tomás | **FIXED** | `ENDINGS.md` E-904 |
| S4 | Medic telegraph at J-110 | **FIXED** | Medic line removed |
| S5 | Case file checklist toward Tomás | **FIXED** | Blank clue log; generic infer prompts |
| S6 / L1 | Fake hub → same split | **FIXED** | Single honest split action per hub |
| H3 | R-112 phantom claim | **FIXED** | Board-only C-06 |
| H4 | J-511 / J-410 bailouts | **FIXED** | Scenes removed |
| H5 | Boot cast job steering | **FIXED** | Neutral boot wording |
| B1 | Motive Records-only | **FIXED** | MOTIVE_WITNESS + proof combo |
| B2 | I-01 hard-lock without C-06 | **FIXED** | +15 min board copy at J-210 |
| D1 | R-212b missing continue | **FIXED** | Continue to R-213/R-214 |
| D2 | Unreachable early-finish | **FIXED** | Linked P-113, P-215, R-114, R-214 |
| D3 | Orphan P-213b | **FIXED** | Renamed **P-214** |
| Split §9 | Records-heavy split 2 | **MITIGATED** | P-212 C-15 + P-214/P-215; **WAIVED** pending human timing confirm |
| P1 | Linear opening | **FIXED** | Hub-first flow |
| P2 | Short playtime risk | **WAIVED** | ~120 min estimate retained; human QA-HP-01 required |
| I2 | Diane thinner | **PARTIAL** | MOTIVE_WITNESS enriches P-112; full parity not required for gate |
| I3 | Tomás-centered worksheets | **FIXED** | Generic infer language |
| U1 | James path low cost | **PARTIAL** | Still possible to get C-12 without C-13; acceptable |
| U2 | Honor-system proof tags | **FIXED** | Accusation guide on case file + J-600 |

### Minor issues

| Review ID | Status |
|---|---|
| B3 unused C-02/C-03 | **PARTIAL** — J-301 timeline includes C-02, C-03 |
| B4 easy opportunity | **OPEN (minor)** — C-12 still on standard People path |
| P3 padding scenes | **OPEN (minor)** — J-122/J-301 retained |
| P4 soft T1 | **OPEN (minor)** — bakery gate timing unchanged |
| H6 clue title spoilers | **FIXED** — blank log |
| D4 partial C-09 | **FIXED** — removed from J-121 |
| D5 follow-up placement | **FIXED** — moved to top of joint file |
| L2 shallow branches | **OPEN (minor)** |

---

## 3. Tier A — Automated results

| Check ID | Result | Notes |
|---|---|---|
| QA-SP-03 | PASS | No END_* logic pre-terminal |
| QA-ST-01 | PASS | No steering keywords |
| QA-FA-01 | PASS | No duplicate hub destinations (fake pairs removed) |
| QA-NV-02 | PASS | Continuations present (spot-check + script) |
| QA-NV-03 | PASS | Scene codes resolve |
| QA-CL-01 | PASS | No Auto major proof clues |
| QA-RC-01 | PASS | Motive witness improves People share |
| QA-TM-04 | PASS | Estimate unchanged ~120 min |

**Custom v0.4.1 guards (validate_player_package.py):**

| Guard | Result |
|---|---|
| No Tomás in J-600 dispatch | PASS |
| No answered infer parenthetical | PASS |
| No verbal claim in Records | PASS |
| No soft bailout phrases | PASS |

---

## 4. Tier B — Structured review (summary)

| Check ID | Result | Notes |
|---|---|---|
| QA-SP-01 | PASS | Dispatch uses proof tags only |
| QA-SP-02 | PASS | Infer prompts unanswered |
| QA-SP-04 | PASS | No phantom cross-booklet knowledge |
| QA-NS-01 | REVIEW | Culprit mention count reduced; human blind-guess still advised |
| QA-NS-02 | PASS | Equal intro blocks at J-121 |
| QA-NS-03 | PASS | Finder spotlight reduced; not eliminated (role remains in fiction) |
| QA-ST-02 | PASS | No NPC next-location steering |
| QA-ST-03 | PASS | Bailouts removed |
| QA-ST-04 | PASS | Check outcomes descriptive |
| QA-FA-03 | PASS | No forced major clue pre-hub |
| QA-IN-01 | PASS | Infer requires prior clues |
| QA-IN-02 | PASS | Earn/Observe dominant |
| QA-IN-03 | PASS | I-02 requires competing motive lines |
| QA-CL-03 | PASS | Both roles needed for full proof paths |
| QA-RC-02 | WAIVED | Split 2 balance — mitigated, human confirm |
| QA-RC-04 | PASS | Solo-solve blocked without both roles |
| QA-TM-01 | PASS | T2/T3 gate meaningful options |
| QA-TM-02 | PASS | Cannot do all options within clock |
| QA-FR-01 | PASS | Proof dependencies closed |
| QA-FR-02 | PASS | Single fair culprit among majors |
| QA-FR-03 | REVIEW | Recommend blind culprit read before playtest |
| QA-FR-04 | PASS | Demeanor not sufficient for E-901 |

---

## 5. Waivers

| Check ID | Reason | Mitigation | Expiry |
|---|---|---|---|
| QA-RC-02 | Split 2 People/Records delta not machine-verified | P-215/R-214 early-finish; C-15 added to People path | Revoke if QA-HP-03 FAIL |
| QA-TM-04 / P2 | Word-count vs wall-clock unverified | Human playtest timing | Revoke if QA-HP-01 FAIL |

**Critical waivers:** none (forbidden).

---

## 6. Global evaluation (QA spec §11)

| Question | Answer |
|---|---|
| 1. Book reveals culprit without Infer? | **No** — dispatch uses proof tags |
| 2. One name dominates first hour? | **Reduced** — monitor at playtest |
| 3. One silent player completes proof? | **No** — MOTIVE_WITNESS + documents |
| 4. Hub first-option ≈ all options? | **No** — fake pairs removed |
| 5. Ignoring clock changes nothing? | **No** — thresholds gate access |
| 6. Mid-game rules reveal outcome? | **No** |

---

## 7. Pre-playtest gate decision

| Criterion | Met? |
|---|---|
| Hygiene PASS | ☑ |
| All Critical PASS | ☑ |
| All Major PASS or waived | ☑ |
| Tier A run attached | ☑ |
| Tier B Critical/Major complete | ☑ |
| Report filed | ☑ |

**Decision:** ☑ **Pre-Playtest Ready**

**Rationale:** All mandatory pre-playtest Critical findings eliminated. Major findings fixed or waived with human follow-up on split timing and wall-clock. Adventure is safe to invite human playtesters for Tier C validation.

**Not yet:** Adventure Ready (requires recorded human playtest per v0.4 §13.2).

---

## 8. Recommended human playtest focus

1. QA-HP-03 — split 2 idle wait  
2. QA-HP-01 — actual wall-clock vs ~120 min  
3. QA-HP-04 — culprit lock timing (blind guess protocol)  
4. QA-HP-05 — players articulate theory before accusation  
5. QA-HP-06 — both players rate contribution  

---

*End of QA report.*

# Harborview Arcade v0.4.1 — Changelog

**Base version:** v0.4.0 (initial benchmark generation)  
**Revision:** v0.4.1  
**Authority:** `HARBORVIEW_PRE_PLAYTEST_REVIEW.md` (mandatory fixes)  
**Preserved:** Culprit, motive, method, solution, ~120 min target, core cast and setting

---

## Summary

Localized revision eliminating all **Critical** pre-playtest findings and all **Major** findings that were practical to fix without redesign. Story, mystery, and solution unchanged.

---

## Change log

### CHG-01 — Remove culprit from ending dispatch (S1)

| Field | Value |
|---|---|
| **Review IDs** | S1 |
| **Files** | `PLAYER/JOINT_SCENES.md` |
| **Change** | J-600 uses proof tags + I-03 + accused name; no named correct suspect |
| **Why it fixes** | Players no longer see the win condition before endings |
| **No new problems** | E-901 still validates full proof chain; wrong/partial paths use E-902/E-903 |

---

### CHG-02 — Remove answered Infer I-01 (S2, H2)

| Field | Value |
|---|---|
| **Review IDs** | S2, H2 |
| **Files** | `PLAYER/JOINT_SCENES.md`, `PLAYER/SHARED/CASE_FILE.md` |
| **Change** | Removed parenthetical answer; generic sign-out vs scuff question |
| **Why it fixes** | Players must state the weakened theory themselves |
| **No new problems** | J-210 adds +15 min recovery if C-06 missing (B2) without answering infer |

---

### CHG-03 — Stairwell as hub choice, not forced tour (H1, P1)

| Field | Value |
|---|---|
| **Review IDs** | H1, P1 |
| **Files** | `PLAYER/JOINT_SCENES.md` |
| **Change** | J-100 → J-120; C-01 only on choosing “Examine rear stairwell” |
| **Why it fixes** | Player-directed investigation starts at first hub |
| **No new problems** | Fair path still obtains C-01 before I-01 via hub or revisit |

---

### CHG-04 — Neutral Park briefing; reduced finder spotlight (I1, I3)

| Field | Value |
|---|---|
| **Review IDs** | I1, I3, S4 (partial) |
| **Files** | `PLAYER/JOINT_SCENES.md`, `PLAYER/BOOKLET_PEOPLE.md` |
| **Change** | Park lists four suspects neutrally; report time only; removed medic telegraph from J-110; handyman departure moved to earned C-15 at P-212 |
| **Why it fixes** | Less genre spotlight on finder role at intro; alibi claim earned in interview |
| **No new problems** | Solution unchanged; C-15 pairs with C-06 for opportunity at accusation |

---

### CHG-05 — Remove phantom 19:30 claim from Records (H3)

| Field | Value |
|---|---|
| **Review IDs** | H3 |
| **Files** | `PLAYER/BOOKLET_RECORDS.md` |
| **Change** | R-112 shows board sign-out to 20:15 only; no verbal claim |
| **Why it fixes** | Records no longer knows testimony before People interview |
| **No new problems** | Contradiction discovered via C-06 + C-15 at regroup |

---

### CHG-06 — Honest hub menus; remove fake split labels (S6, L1)

| Field | Value |
|---|---|
| **Review IDs** | S6, L1 |
| **Files** | `PLAYER/JOINT_SCENES.md` |
| **Change** | Hub 1: one “Split up…” action; Hub 2: one split action; removed duplicate bakery/records and Holt/basement fake choices |
| **Why it fixes** | Menu labels match outcomes; no cosmetic agency |
| **No new problems** | Split roles unchanged; less misleading choice noise |

---

### CHG-07 — Remove soft clue bailouts (H4)

| Field | Value |
|---|---|
| **Review IDs** | H4 |
| **Files** | `PLAYER/JOINT_SCENES.md` |
| **Change** | Removed J-511 boot grant; removed J-410 fax free clue; I-02 requires three facts or return to play |
| **Why it fixes** | Earn/scarcity preserved; no catch-up gifts |
| **No new problems** | CHK fail paths and partner sharing still provide degraded routes |

---

### CHG-08 — Neutral boot-cast wording (H5)

| Field | Value |
|---|---|
| **Review IDs** | H5 |
| **Files** | `PLAYER/BOOKLET_RECORDS.md` |
| **Change** | “Standard work boot from building supply locker” |
| **Why it fixes** | Less job-title steering toward handyman |
| **No new problems** | C-10 still supports PROOF_METHOD |

---

### CHG-09 — People motive contribution (B1)

| Field | Value |
|---|---|
| **Review IDs** | B1 |
| **Files** | `PLAYER/BOOKLET_PEOPLE.md`, `PLAYER/SHARED/CASE_FILE.md`, `DO_NOT_READ/LOGIC/*` |
| **Change** | P-112 grants MOTIVE_WITNESS; PROOF_MOTIVE allows witness + document combo; I-02 includes MOTIVE_WITNESS |
| **Why it fixes** | People track contributes to motive proof, not only red herrings |
| **No new problems** | Records documents still required for full motive tag unless C-14 degraded path |

---

### CHG-10 — C-06 recovery at Infer 1 (B2)

| Field | Value |
|---|---|
| **Review IDs** | B2 |
| **Files** | `PLAYER/JOINT_SCENES.md` |
| **Change** | +15 min request tool board copy if C-06 missing before I-01 |
| **Why it fixes** | Infer 1 cannot hard-lock if Records early-finishes |
| **No new problems** | Costs time; does not grant free unrelated clues |

---

### CHG-11 — Navigation fixes (D1, D2, D3)

| Field | Value |
|---|---|
| **Review IDs** | D1, D2, D3 |
| **Files** | `PLAYER/BOOKLET_PEOPLE.md`, `PLAYER/BOOKLET_RECORDS.md`, `PLAYER/NAVIGATION_INDEX.md` |
| **Change** | R-212b continues; P-214 gym scene (not under P-213); P-113/P-215/R-114/R-214 linked from live paths; split early-finish called out at J-130/J-330 |
| **Why it fixes** | No orphan scenes; anti-idle reachable |
| **No new problems** | All paths still terminate at regroup |

---

### CHG-12 — Split 2 balance (People workload)

| Field | Value |
|---|---|
| **Review IDs** | Split imbalance (§9) |
| **Files** | `PLAYER/BOOKLET_PEOPLE.md` |
| **Change** | P-212 grants C-15; P-214/P-215 added; James fail path explicit |
| **Why it fixes** | People split 2 has more substantive scenes vs Records |
| **No new problems** | Estimates remain within ±5 min band on paper |

---

### CHG-13 — Case file de-checklist (S5, H6, U2)

| Field | Value |
|---|---|
| **Review IDs** | S5, H6, U2, D5 |
| **Files** | `PLAYER/SHARED/CASE_FILE.md`, `PLAYER/JOINT_SCENES.md` |
| **Change** | Blank clue titles; generic infer prompts; accusation guide; follow-up moved to top of joint file; split time tracker |
| **Why it fixes** | Less form-filling toward one suspect; clearer ending rules |
| **No new problems** | Proof rules still sheet-checkable per v0.4 §8.3 |

---

### CHG-14 — E-904 spoiler removed (S3)

| Field | Value |
|---|---|
| **Review IDs** | S3 |
| **Files** | `PLAYER/ENDINGS.md` |
| **Change** | “Suspects remain on site” — no named handyman |
| **Why it fixes** | Timeout ending does not reveal killer |
| **No new problems** | E-901 may name accused after correct proof (post-resolution) |

---

### CHG-15 — Ending and logic alignment

| Field | Value |
|---|---|
| **Review IDs** | U2, B3 (partial) |
| **Files** | `PLAYER/ENDINGS.md`, `DO_NOT_READ/LOGIC/14_ENDING_TRIGGER_MATRIX.md`, `05_CLUE_ARCHITECTURE.md` |
| **Change** | E-901/E-902 text uses proof chain; C-15 added; C-02 referenced in J-301 timeline |
| **Why it fixes** | Endings match sheet logic; fewer orphan clues |
| **No new problems** | Truth layer unchanged |

---

### CHG-16 — Validation harness

| Field | Value |
|---|---|
| **Files** | `PLAYER/validate_player_package.py` |
| **Change** | Anti-spoiler checks, bailout ban, 15 clues |
| **Why it fixes** | Regression guard for v0.4.1 class defects |
| **No new problems** | Structural checks only |

---

## Files modified (complete list)

- `README.md`
- `PROTOTYPE_BRIEF.md`
- `PLAYER/JOINT_SCENES.md`
- `PLAYER/BOOKLET_PEOPLE.md`
- `PLAYER/BOOKLET_RECORDS.md`
- `PLAYER/SHARED/CASE_FILE.md`
- `PLAYER/ENDINGS.md`
- `PLAYER/NAVIGATION_INDEX.md`
- `PLAYER/COMPILATION_REPORT.md`
- `PLAYER/validate_player_package.py`
- `DO_NOT_READ/00_CASE_OVERVIEW.md`
- `DO_NOT_READ/05_CLUE_ARCHITECTURE.md`
- `DO_NOT_READ/LOGIC/00_ENTITY_KEY_TABLE.md`
- `DO_NOT_READ/LOGIC/01_WORLD_STATE_VARIABLES.md`
- `DO_NOT_READ/LOGIC/14_ENDING_TRIGGER_MATRIX.md`

---

*End of changelog.*

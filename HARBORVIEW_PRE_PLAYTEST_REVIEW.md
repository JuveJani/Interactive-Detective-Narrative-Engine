# Harborview Arcade — Pre-Playtest Review

**Subject:** `adventures/CASE_BENCHMARK_v0.4/` (PLAYER + DO_NOT_READ)  
**Scope:** This adventure only — engine assumed fixed  
**Goal:** Predict player experience before first human playtest  
**Non-goals:** Redesign adventure or engine; rewrite scenes

---

## Verdict in one line

The bones are playable and mostly fair, but several authored moments **hand the solution**, **fake hub agency**, and **spoil the culprit in player-visible rules** — those will contaminate playtest data if left unchanged.

---

## 1. Accidental steering

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| S1 | **Critical** | **J-600 ending dispatch names Tomás Reyes as the correct accusation.** Players see the win condition before opening endings. | `JOINT_SCENES.md` J-600 step 3: “accused Tomás Reyes with all proof tags” |
| S2 | **Critical** | **I-01 answers itself.** Joint worksheet asks what theory is weakened, then parenthetical supplies “(Accident without struggle.).” | `JOINT_SCENES.md` J-210 |
| S3 | **Major** | **E-904 timeout ending still names Tomás Reyes** as remaining on site — spoiler for players who never accused anyone. | `ENDINGS.md` E-904 |
| S4 | **Major** | Opening medic note telegraphs method: injury “inconsistent with a simple backward fall” before players choose to investigate. | `JOINT_SCENES.md` J-110 |
| S5 | **Major** | Infer worksheets and proof-tag formulas on the **case file** are a checklist that points at Tomás’s 19:30 claim and basement access. Players may “solve” by filling forms, not reasoning. | `SHARED/CASE_FILE.md` I-01, I-03, PROOF_* |
| S6 | **Minor** | Hub menus are diegetic (good), but **two Hub 1 actions and two Hub 2 actions both dump into the same split launch** — agency is cosmetic. | J-120 bakery & records → both `J-130`; J-300 Holt & basement → both `J-330` |

**Predicted player effect:** Early suspicion of Tomás from finder + I-01 focus; late confirmation from J-600 text even if theory was weak. Playtest will under-measure “discovery.”

---

## 2. Moments where the mystery is handed, not discovered

| ID | Severity | Finding |
|---|---|---|
| H1 | **Critical** | Forced path **J-100 → J-110** grants **C-01** before any hub choice. First major method clue is a tour stop, not a decision. Brief / engine intent: observation after choosing to look. |
| H2 | **Critical** | J-210 / I-01 parenthetical (S2) removes the first infer beat’s cognitive work. |
| H3 | **Major** | **R-112** states Tomás’s “verbal claim was 19:30” before Records has heard Tomás speak (People only hears that at **P-212**, split 2). Phantom knowledge = handed contradiction. |
| H4 | **Major** | **J-511** can grant missing **C-10**; **J-410** fax bailout grants missing **C-05/C-11**. Softens Earn scarcity into catch-up gifts. |
| H5 | **Major** | Boot-cast pass text ties impression to “maintenance issue boots” — points at the handyman’s job without player synthesis. |
| H6 | **Minor** | Case-file clue titles already encode meaning (“Tool sign-out discrepancy,” “Duplicate vendor invoices”) before scenes are played if players skim the blank log. |

**Predicted player effect:** “We collected cards and checked boxes” more than “we figured it out” — same failure mode the benchmark was meant to beat.

---

## 3. Clue bottlenecks

| ID | Severity | Finding |
|---|---|---|
| B1 | **Major** | **Motive proof is Records-only** (C-05 or C-11). People track cannot contribute motive. Fair for asymmetry, but claim of “Route B people-heavy fair path” in `05_CLUE_ARCHITECTURE.md` is **false** without Records motive grants. |
| B2 | **Major** | **I-01 hard-requires C-06** at J-210. C-06 only exists on Records split-1 path (R-112). If Records early-finishes incorrectly or skips (see D3), Infer 1 stalls with no recovery text. |
| B3 | **Minor** | **C-02** (broken latch) and **C-03** (camera entry) never appear in proof tags or infer worksheets. Players will log them and wonder why they matter — feel like dead weight. |
| B4 | **Minor** | **PROOF_OPPORTUNITY** needs C-12 or C-13. C-12 is nearly automatic on People split 2 (P-213). Opportunity is hard to miss once split 2 runs — low tension. |

**Predicted player effect:** People player may feel like a red-herring specialist; Records carries method + motive + opportunity documents.

---

## 4. Pacing issues

| ID | Severity | Finding |
|---|---|---|
| P1 | **Major** | First ~15–20 minutes are **linear**: arrival → forced stairwell → hub. Player-directed investigation starts late. |
| P2 | **Major** | Published wall-clock table (~120) assumes dense reading. Actual table talk + short scenes may land nearer **80–100** unless hubs are looped — risk of short session again. |
| P3 | **Minor** | **J-122** / **J-301** (“no new clue”) and stairwell revisit (**J-110** again) are low-value time sinks if chosen. |
| P4 | **Minor** | Threshold T1 (bakery) often fires *after* split 1 already interviewed Mira — tooth feels soft on standard path. T2/T3 more likely to matter. |

**Predicted player effect:** Front half feels escorted; back half checklist-y; time pressure uneven.

---

## 5. Boring investigation loops

| ID | Severity | Finding |
|---|---|---|
| L1 | **Major** | Hub 1/2 “choices” that both open the same split teach players that menus don’t matter → they stop reading options carefully. |
| L2 | **Minor** | Split paths are mostly **linear chains** (P-111→112→…; R-111→112→113). Branch points are shallow A/B with similar destinations. |
| L3 | **Minor** | Tomás interview (**P-212**) grants **no clue** and exists mainly to deliver the 19:30 claim — feels like filler if Records already “knows” the claim from R-112. |

---

## 6. Suspect imbalance

| ID | Severity | Finding |
|---|---|---|
| I1 | **Critical** | **Tomás is the body-finder who called 911**, warned about wet stairs, signed the mop kit, and is the focus of I-01. Classic genre spotlight despite equal one-line intros at J-121. |
| I2 | **Major** | Mira/James get vivid red-herring scenes; Diane is thinner. Tomás gets late interview with “no clue.” Emotional weight ≠ equal narrative importance. |
| I3 | **Major** | Case-file and J-210 language repeatedly center Tomás’s alibi before other suspects are fully tested. |

**Predicted player effect:** At least one player locks Tomás early (same intro-leak class as Glass Alibi, via *role* not adjectives).

---

## 7. Hidden dead ends & broken navigation

| ID | Severity | Finding |
|---|---|---|
| D1 | **Major** | **R-212b** (“Skim”) advances +5 min but **does not say Continue to R-213**. Players may stall. |
| D2 | **Major** | **Early-finish scenes P-113 / R-114 / R-214** are not linked from decision menus. Linear paths go past them to regroup. Anti-idle design is mostly **unreachable**. |
| D3 | **Major** | **P-213b** gym follow-up is orphaned: fail at P-211a says “needs P-213 follow-up,” but **P-213 is Okonkwo**, not gym. Players won’t know when to open P-213b. |
| D4 | **Minor** | J-121 “Partial C-09 setup” — unclear whether to tick C-09. Full C-09 arrives at P-112. Double-count / confusion risk. |
| D5 | **Minor** | Follow-up response table sits **after J-600** in the joint file — easy to miss when hubs say “use follow-up.” |

---

## 8. Unfair or fragile deductions

| ID | Severity | Finding |
|---|---|---|
| U1 | **Major** | If players take **P-211b** (relationship only), they miss C-08 entirely — fine — but opportunity still auto-completes via C-12. Wrong-path James barely costs. |
| U2 | **Major** | Correct ending requires players to **self-check proof tags** against formulas. Mis-ticking tags can yield E-901 or E-903 incorrectly — honor-system adjacent. |
| U3 | **Minor** | `CHK_INVOICE` fail grants C-14 and marks degraded certainty, but C-14 is **not** in PROOF_MOTIVE formula. Fail path needs J-410 fax or C-11 — recoverable, but opaque mid-scene. |

---

## 9. Split imbalance

| Window | Written estimate | Likely real engagement | Risk |
|---|---|---|---|
| Split 1 | People 10 / Records 10 | Records: 3 scenes + more text; People: 2 interviews | Records finishes later (~3–6 min) |
| Split 2 | People 12 / Records 12 | Records: basement + 2 checks + invoices + email; People: James + Tomás (empty) + Okonkwo | **Records heavier**; People waits — echoes Glass Alibi first-split wait |

Early-finish mitigations exist on paper but are **not reachable from play flow** (D2).

**Predicted player effect:** People idle in Split 2; frustration at “balanced” claim.

---

## 10. Confusion hotspots (player-facing)

1. **Hub actions that claim different investigations but open the same split** — “Did we interview bakery or not?”
2. **Clock math** — “longer split time your table used” without a per-scene elapsed tracker on the sheet.
3. **When thresholds apply** — T1 bakery closed after Mira already interviewed on standard path.
4. **Proof tags vs clue titles** — players may check PROOF_METHOD from C-01 alone without C-04.
5. **Private Tomás claim vs Records R-112** — partners will argue who “knew” the 19:30 line first.
6. **I-02 “need at least three of C-05, C-07, C-11”** — C-07 is red herring; combining it with motive docs is good design, but players may think they must treat rent as part of the solution.

---

## 11. What is likely to work well

- Contained setting and clear stakes (grant deadline) are easy to grasp.
- Nervous Mira / evasive James are believable red herrings.
- Decision isolation is mostly respected (outcomes in lettered destinations).
- No meta “recommended” language in menus.
- Ending E-901’s causal narration is strong **if** reached without J-600 spoiling the name first.
- Dual-role structure is clear at setup.

---

## 12. Issue summary by severity

### Critical (fix before playtest or data is contaminated)

1. J-600 names Tomás as correct (S1)  
2. I-01 parenthetical answers the infer (S2 / H2)  
3. Forced C-01 before player-directed play (H1)  
4. Tomás over-spotlight as finder + I-01 focus (I1)

### Major (likely to cause wait, confusion, or handed mystery)

5. Hub fake choices → same split (S6 / L1)  
6. R-112 phantom 19:30 claim (H3)  
7. Split 2 Records heavier; early-finish unreachable (imbalance + D2)  
8. Orphan P-213b / broken R-212b continue (D1 / D3)  
9. Soft clue bailouts J-410 / J-511 (H4)  
10. E-904 names Tomás (S3)  
11. Motive Records-only vs claimed people-heavy route (B1)

### Minor

12. Unused C-02/C-03; soft T1; padding scenes; clue-title spoilers on blank log

---

## 13. Approval for human playtesting

### **YES WITH MINOR CHANGES**

**Why not YES:** Critical spoilers and answered inferences would make the playtest measure the wrong thing (checklist compliance and “finder is guilty” genre tropes), not v0.4 investigation quality.

**Why not NO:** The adventure is structurally complete, fair enough to finish, linguistically clear, and close to brief targets. The blocking issues are **localized edits** (dispatch wording, remove parenthetical answers, fix hub destinations / early-finish links, move Tomás claim to People-only, rebalance or gate Split 2), not a full rewrite.

**Approve for playtest only after** at least:

1. Remove culprit name from J-600 (and E-904).  
2. Remove answer text from I-01 / J-210.  
3. Make Hub 1/2 actions lead to **distinct** content or stop presenting them as alternatives.  
4. Fix R-112 / P-213b / R-212b navigation.  
5. Expose early-finish options from the live paths.

Until those land, treat this package as **author QA**, not playtest-ready.

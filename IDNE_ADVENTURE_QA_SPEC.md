# IDNE Adventure QA Specification

**Document type:** Permanent post-generation quality assurance layer  
**Applies to:** Every generated IDNE adventure before human playtesting  
**Engine alignment:** IDNE Engine v0.4 (§13 Readiness) + Design Philosophy Category A  
**Status:** Normative for Adventure QA (does not modify the engine)  
**Companion:** `ADVENTURE_QA_REPORT_TEMPLATE.md`

---

## 1. Executive Summary

Structural validation can prove an adventure is *complete*. It cannot prove the adventure is *good detective play*.

This specification defines a reusable **Adventure QA** layer that sits **after** generation / compilation and **before** human playtesting. It detects cases where an adventure obeys file, graph, and keyword rules yet still produces:

- handed solutions
- telegraphed culprits
- fake menus
- inference theatre
- one-player dominance
- soft time pressure
- navigation traps

**Core claim:** An adventure may pass hygiene and still fail Adventure QA. Adventure QA PASS is required before inviting human playtesters. Human playtest remains the final experience gate (v0.4 §13.2).

**Method:** Three tiers — (A) fully automatable scripts, (B) AI-assisted structured review, (C) human playtest-only measurements. Subjective experience is never claimed as script-complete.

**Failure classes** below are generalized from engine philosophy, red-team risks, and observed generation failure modes (including Harborview Arcade as an *example class*, not the sole scope).

---

## 2. QA pipeline position

```text
Adventure Brief
      ↓
World Bible + Adventure Logic
      ↓
Delivery Adapter → PLAYER package
      ↓
Hygiene validation (identifiers, reachability, inventory)     ← necessary, not sufficient
      ↓
★ ADVENTURE QA (this document) ★
      ├── A. Automated checks
      ├── B. AI review checks
      └── Gate: Pre-Playtest Ready?
            ↓ YES
      C. Human playtest checks
            ↓
      Adventure Ready / Waived / Failed
```

| Layer | Owns | Does not own |
|---|---|---|
| Engine spec | Reusable rules | Adventure content QA |
| Hygiene validators | Structural completeness | Experience quality |
| **Adventure QA** | Pre-playtest experience risk | Engine redesign |
| Human playtest | Lived experience truth | Spec authorship |

Adventure QA evaluates the adventure **globally** (culprit exposure, role ownership of proof, hub agency across the graph) as well as locally (scene text).

---

## 3. Mandatory pre-playtest gates

An adventure is **Pre-Playtest Ready** only if:

1. Hygiene validation PASS (or documented hygiene exceptions that do not affect play).
2. **All Critical** Adventure QA checks PASS.
3. **All Major** Adventure QA checks PASS, or each has an **approved waiver** (§8).
4. Automated suite (Tier A) has been run and attached to the QA report.
5. AI review (Tier B) has been completed for all B-class checks.
6. QA report filed using `ADVENTURE_QA_REPORT_TEMPLATE.md`.

Human playtest (Tier C) is **not** required for Pre-Playtest Ready. It **is** required for full **Adventure Ready** under v0.4 §13.2.

| Status | Meaning |
|---|---|
| **QA FAIL** | Do not playtest; fix or waive |
| **Pre-Playtest Ready** | Safe to invite playtesters |
| **Adventure Ready** | Pre-Playtest Ready + recorded human playtest against Tier C |
| **Waived Ready** | Pre-Playtest Ready with documented Major waivers only (no Critical waivers) |

---

## 4. Severity model

| Severity | Definition | Gate effect |
|---|---|---|
| **Critical** | Contaminates playtest data or breaks fair detective identity (spoilers, handed guilt, unsolvable fair path, fake Ready) | Blocks Pre-Playtest Ready; **no waiver** |
| **Major** | Likely poor experience (imbalance, soft agency, soft scarcity, role optional) | Blocks Pre-Playtest Ready unless approved waiver |
| **Minor** | Polish, padding, low-risk confusion | Does not block; must be logged |

---

## 5. Check catalog

Each check uses this schema:

- **Check ID**
- **Name**
- **Purpose**
- **Failure condition**
- **Severity**
- **Automatable** (Yes / Partial / No)
- **Tier** (A / B / C)
- **Required inputs**
- **Metric / heuristic**
- **False-positive risk**
- **Human review**
- **Example failure pattern**
- **Pass criteria**

---

### 5.1 Accidental spoilers

#### QA-SP-01 — Culprit named in player-facing rules

| Field | Value |
|---|---|
| **Purpose** | Prevent ending/dispatch logic from revealing the correct accused before play concludes |
| **Failure condition** | PLAYER materials (excluding sealed ending pages reached only after accusation) name the culpable NPC as the correct accusation, win condition, or “true” killer |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Culprit key from World Bible; all PLAYER text except sealed endings after dispatch |
| **Metric** | Regex/name match of culprit display name in HOW_TO_PLAY, CASE_FILE, JOINT dispatch, SETUP, hubs |
| **False-positive risk** | Medium — innocent mentions of the character as a suspect are allowed |
| **Human review** | Confirm context is “correct answer” vs “listed suspect” |
| **Example** | Ending dispatch: “If accused [Culprit] with all proof tags → Correct” |
| **Pass criteria** | No player-facing rule text identifies which named person yields the victory ending |

#### QA-SP-02 — Parenthetical or inline answers to inferences

| Field | Value |
|---|---|
| **Purpose** | Keep Infer beats player-owned |
| **Failure condition** | Infer worksheet or joint-reasoning scene supplies the conclusion in parentheses, “hint,” or “expected answer” alongside the question |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Infer scenes; case-file worksheets |
| **Metric** | Detect parenthetical after theory questions; phrases like “this weakens,” “therefore X is guilty” |
| **False-positive risk** | Low–Medium |
| **Human review** | Distinguish clarifying definitions from answer keys |
| **Example** | “What theory does this weaken? (Accident without struggle.)” |
| **Pass criteria** | Infer prompts ask; they do not answer |

#### QA-SP-03 — Ending logic leak outside sealed endings

| Field | Value |
|---|---|
| **Purpose** | Keep trigger matrices and truth statements out of mid-play materials |
| **Failure condition** | Non-terminal PLAYER units contain ending IDs mapped to truth, “correct/wrong” labeled by culprit, or internal END_* condition prose |
| **Severity** | Critical |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | PLAYER corpus; ending key list |
| **Metric** | Presence of END_/E-9xx condition explanations before J-terminal; truth words near ending codes |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | Timeout ending text naming the killer while players never accused |
| **Pass criteria** | Pre-terminal PLAYER text never discloses which ending is “true” |

#### QA-SP-04 — Phantom knowledge spoilers

| Field | Value |
|---|---|
| **Purpose** | Prevent one booklet from stating facts the role has not obtained |
| **Failure condition** | A role’s private text asserts another role’s private testimony/finding before any share/sync rule grants it |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Knowledge ownership matrix; split booklets |
| **Metric** | Cross-booklet claim audit against disclosure graph |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Records booklet cites suspect’s verbal alibi before People interview exists |
| **Pass criteria** | Each stated fact is obtainable in that role’s prior path or shared sheet |

---

### 5.2 Narrative spotlight imbalance

#### QA-NS-01 — Suspect mention frequency skew

| Field | Value |
|---|---|
| **Purpose** | Detect disproportionate name presence |
| **Failure condition** | In PLAYER text before accusation hub, one major suspect’s name appears ≥2× the median of other major suspects **and** that suspect is the culprit |
| **Severity** | Major (Critical if ≥3× and culprit) |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Major suspect list; culprit; PLAYER corpus |
| **Metric** | Name-token counts per act / full pre-accusation corpus |
| **False-positive risk** | Medium — body-finder roles naturally recur; flag for review |
| **Human review** | Required when automated flag trips |
| **Example** | Culprit named in discovery, tool logs, infer prompts, and interview while others appear once |
| **Pass criteria** | Culprit not uniquely dominant by ≥2× without documented role justification **and** compensating equal-weight intro |

#### QA-NS-02 — Intro equal-weight budget

| Field | Value |
|---|---|
| **Purpose** | Operationalize U9 / equal narrative weight |
| **Failure condition** | At first joint introduction of major suspects, word counts differ by >25% **or** unique epithets/spotlight stage business attach to only one suspect |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Intro scene(s) |
| **Metric** | Word count per suspect block; banned epithet list |
| **False-positive risk** | Low–Medium |
| **Human review** | Tone pass required |
| **Example** | Culprit gets longest calm paragraph and a helpful offer |
| **Pass criteria** | Intro blocks within 25%; no unique villain diction |

#### QA-NS-03 — Structural spotlight (role-of-finder / only-calm)

| Field | Value |
|---|---|
| **Purpose** | Catch genre telegraphs beyond adjectives |
| **Failure condition** | Culprit uniquely holds ≥2 of: body discovery, sole access to method tool, exclusive focus of first Infer, narrator “warning” speech — without equal false holders for innocents |
| **Severity** | Critical |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | Truth layer + PLAYER presentation |
| **Metric** | Spotlight checklist score |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Finder + mop kit + Infer about their alibi before other suspects tested |
| **Pass criteria** | No unique multi-signal spotlight cluster on culprit alone |

#### QA-NS-04 — Formatting / quotation emphasis leak

| Field | Value |
|---|---|
| **Purpose** | Catch emphasis leaks via bold, quotes, or typography |
| **Failure condition** | Culprit’s name uniquely bolded, italicized, or repeatedly quoted in neutral briefing text relative to peers |
| **Severity** | Minor–Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | PLAYER markdown |
| **Metric** | Emphasis markup counts per suspect |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | Only culprit name bolded in liaison briefing |
| **Pass criteria** | No unique emphasis on culprit in shared briefings |

---

### 5.3 Steering

#### QA-ST-01 — Meta recommended language

| Field | Value |
|---|---|
| **Purpose** | Enforce C-04 / U10 |
| **Failure condition** | PLAYER text contains recommended / preferred / best / “you should” coaching for actions |
| **Severity** | Critical |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | PLAYER corpus |
| **Metric** | Keyword ban list with context filter |
| **False-positive risk** | Medium — “you should” in NPC denial of advice needs exclusion list |
| **Human review** | On flagged hits |
| **Example** | “Recommended: search the basement” |
| **Pass criteria** | Zero coaching hits after human confirmation of flags |

#### QA-ST-02 — NPC names next correct location/action

| Field | Value |
|---|---|
| **Purpose** | Block in-world coaching that recreates meta steering (RT-06) |
| **Failure condition** | Authoritative NPC (officer, manager, liaison) tells players the specific next location/action that is on the critical fair path, unless that advice is sometimes wrong or costly |
| **Severity** | Major |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | NPC scenes; critical path map |
| **Metric** | Manual/AI path-match of NPC directives |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | “If I were you, I’d start in the SCADA room” |
| **Pass criteria** | No authoritative NPC uniquely points to the critical next step |

#### QA-ST-03 — Soft bailout restores missing solution clues

| Field | Value |
|---|---|
| **Purpose** | Prevent catch-up gifts that erase scarcity and Earn |
| **Failure condition** | A late joint scene grants a missing major proof clue with little/no new action cost relative to the original Earn path |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Clue acquisition map; late scenes |
| **Metric** | Count of “if you lack C-xx, gain it now” patterns on proof-critical clues |
| **False-positive risk** | Medium — intentional degraded recovery allowed if costly |
| **Human review** | Required |
| **Example** | Fax grants missing motive clue; lab scene grants missing method clue |
| **Pass criteria** | Proof-critical recoveries either absent or strictly costlier/degraded |

#### QA-ST-04 — Check outcomes steer next investigation

| Field | Value |
|---|---|
| **Purpose** | Keep check results descriptive, not tour guides |
| **Failure condition** | Pass/fail text tells players which location or person to investigate next |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Check destinations |
| **Metric** | Directive language after rolls |
| **False-positive risk** | Low–Medium |
| **Human review** | Required |
| **Example** | “Success: you realize you must confront Tomás in the basement” |
| **Pass criteria** | Outcomes grant info/cost changes only |

---

### 5.4 Fake agency

#### QA-FA-01 — Distinct labels, identical destination

| Field | Value |
|---|---|
| **Purpose** | Detect cosmetic hub choices |
| **Failure condition** | Two or more hub actions with different diegetic labels share the same destination unit and identical declared cost/outcome class |
| **Severity** | Critical |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Hub decision tables; graph edges |
| **Metric** | Destination collision rate among labeled alternatives |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | “Interview bakery” and “Pull records” both → same split launch |
| **Pass criteria** | Every labeled alternative differs in destination **or** cost **or** information outcome |

#### QA-FA-02 — Distinct destinations, identical information & cost

| Field | Value |
|---|---|
| **Purpose** | Detect fake branches that reconverge with no difference |
| **Failure condition** | Branches diverge then reconverge with no unique clue, tag, time delta, or NPC state difference |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Graph + clue grants |
| **Metric** | Unique grant/tag/cost diff per branch |
| **False-positive risk** | Medium |
| **Human review** | Required for reconvergent graphs |
| **Example** | A/B interview questions that grant the same clue at same cost |
| **Pass criteria** | Each presented alternative changes at least one of: info, cost, access, risk |

#### QA-FA-03 — Forced tour before first hub

| Field | Value |
|---|---|
| **Purpose** | Preserve player-directed start |
| **Failure condition** | ≥1 major clue is granted on a mandatory path with no player action choice before the first investigation hub |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Opening chain; clue modes |
| **Metric** | Major clue grants before first hub decision |
| **False-positive risk** | Low–Medium — orientation-only Auto allowed |
| **Human review** | Required |
| **Example** | Forced stairwell exam grants method clue before hub |
| **Pass criteria** | Pre-hub grants are orientation only, or hub exists before first major clue |

---

### 5.5 Inference theatre

#### QA-IN-01 — Worksheet restates provided answer

| Field | Value |
|---|---|
| **Purpose** | Block Infer-as-checkbox (RT-03) |
| **Failure condition** | Infer prompt can be completed correctly using only a conclusion already stated in the same scene or immediately prior forced text |
| **Severity** | Critical |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | Infer scenes + preceding units |
| **Metric** | Answer-source distance (must require ≥2 independent prior clue IDs) |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Scene says accident is unlikely; worksheet asks to rule out accident |
| **Pass criteria** | Each Infer requires combining ≥2 independently obtained facts not restated as the answer |

#### QA-IN-02 — Minimum non-Auto major clues on fair path

| Field | Value |
|---|---|
| **Purpose** | Prevent Auto-collectathon with one Infer sticker |
| **Failure condition** | Fair path to correct ending has Auto major clues > 3 **or** Observe+Earn major clues < 8 (adjustable by brief; defaults from v0.4 short-case guidance) |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Clue mode register; fair path |
| **Metric** | Counts by mode |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | 12 Auto location dumps + 1 regroup checkbox |
| **Pass criteria** | Mode counts meet adventure brief / defaults; ≥1 Infer on fair path with QA-IN-01 PASS |

#### QA-IN-03 — Competing theories required before accusation

| Field | Value |
|---|---|
| **Purpose** | Ensure synthesis chooses among alternatives |
| **Failure condition** | Accusation prep Infer has only one named theory path with no competing innocent explanation considered |
| **Severity** | Major |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | Accusation worksheets |
| **Metric** | Presence of ≥2 theory slots or explicit eliminate-alternative step |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Worksheet only asks “who did it?” after text already named them |
| **Pass criteria** | Players must reject ≥1 plausible alternative using evidence |

---

### 5.6 Clue delivery problems

#### QA-CL-01 — Major Auto without necessity

| Field | Value |
|---|---|
| **Purpose** | Prefer Observe/Earn (Philosophy A8) |
| **Failure condition** | Major clue mode = Auto and clue is on a proof tag / ending requirement |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Clue register; proof matrix |
| **Metric** | Auto ∩ proof-critical set size (must be 0) |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | Enter room → guilt-relevant ledger auto-granted |
| **Pass criteria** | No proof-critical Auto majors |

#### QA-CL-02 — Repeat-until-impossible-to-miss

| Field | Value |
|---|---|
| **Purpose** | Detect hammered reveals |
| **Failure condition** | Same proof-critical fact restated in ≥3 separate player units before Infer that uses it |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | PLAYER units; clue IDs |
| **Metric** | Restatement count |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Wet stairs mentioned in arrival, exam, NPC warning, and infer prompt |
| **Pass criteria** | ≤2 presentations of a proof-critical fact before its Infer |

#### QA-CL-03 — Asymmetric complete-solution route

| Field | Value |
|---|---|
| **Purpose** | Ensure both roles needed; catch single-route dumps |
| **Failure condition** | One role’s private path alone can satisfy all proof categories without the other role’s unique required clue category |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Proof category ownership by role |
| **Metric** | Per-role coverage of METHOD/MOTIVE/OPPORTUNITY (or adventure-equivalent) |
| **False-positive risk** | Low–Medium |
| **Human review** | Required |
| **Example** | Records path alone yields method+motive+opportunity |
| **Pass criteria** | Each fair path requires ≥1 unique contribution from each role |

#### QA-CL-04 — Orphan / unused logged clues

| Field | Value |
|---|---|
| **Purpose** | Reduce dead-weight collectibles |
| **Failure condition** | ≥20% of active clues never referenced by Infer, proof tags, or ending evaluators |
| **Severity** | Minor |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Clue register; evaluator refs |
| **Metric** | Unused clue ratio |
| **False-positive risk** | Medium — flavour clues allowed if labeled optional |
| **Human review** | Optional |
| **Example** | Broken latch and camera still never used |
| **Pass criteria** | Unused ratio <20% or optional clues explicitly marked |

---

### 5.7 Role and cooperation imbalance

#### QA-RC-01 — Decisive evidence ownership skew

| Field | Value |
|---|---|
| **Purpose** | Keep partners co-owners of the case |
| **Failure condition** | One role grants >70% of proof-critical clues |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Clue grant map by role/mode |
| **Metric** | % proof-critical grants per role |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | People only get red herrings; Records gets all proof |
| **Pass criteria** | Each role ≤70% of proof-critical grants; both >15% |

#### QA-RC-02 — Split wall-clock delta

| Field | Value |
|---|---|
| **Purpose** | Enforce balance gate |
| **Failure condition** | Estimated engagement delta between roles in any split window >5 minutes (or brief target) |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Per-scene time estimates; early-finish reachability |
| **Metric** | \|A−B\| per window; early-finish must be graph-reachable |
| **False-positive risk** | Medium — reading speed variance |
| **Human review** | Required if borderline |
| **Example** | Records 3 checks + basement vs People short chats |
| **Pass criteria** | Delta ≤ target; early-finish options reachable from live paths |

#### QA-RC-03 — Joint clue-grant share

| Field | Value |
|---|---|
| **Purpose** | Prevent two solo novels |
| **Failure condition** | Joint clue-granting units <40% (or brief floor) without waiver |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Unit mode + clue grants |
| **Metric** | Joint / total clue-granting units (define unit = scene with ≥1 clue or Infer) |
| **False-positive risk** | Medium — micro-unit gaming; require minute-weighted metric if available |
| **Human review** | Spot-check unit slicing |
| **Example** | Eight tiny Joint stubs pad ratio while investigation is split |
| **Pass criteria** | Ratio ≥ floor using declared metric documented in brief |

#### QA-RC-04 — Solo-solvable case

| Field | Value |
|---|---|
| **Purpose** | Detect optional partner |
| **Failure condition** | A legal path exists where one player never opens their private booklet yet still reaches correct ending conditions |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Graph; proof dependencies |
| **Metric** | Reachability with one role’s grants removed |
| **False-positive risk** | Low |
| **Human review** | Required |
| **Example** | All proof in Joint + one booklet |
| **Pass criteria** | Removing either role’s unique grants blocks correct ending |

---

### 5.8 Navigation and state errors

#### QA-NV-01 — Orphan / unreachable scenes

| Field | Value |
|---|---|
| **Purpose** | Catch dead content and anti-idle lies |
| **Failure condition** | Scene code listed in index/booklet has zero inbound edges from any reachable unit |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Full graph from PLAYER destinations |
| **Metric** | Reachability from start |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | Early-finish scenes never linked from decisions |
| **Pass criteria** | All playable units reachable OR explicitly marked unused draft |

#### QA-NV-02 — Missing continuation

| Field | Value |
|---|---|
| **Purpose** | Prevent stalls |
| **Failure condition** | Non-terminal unit lacks Continue/Go-to destination |
| **Severity** | Critical |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | PLAYER units |
| **Metric** | Terminal vs continuation annotation |
| **False-positive risk** | Low |
| **Human review** | Optional |
| **Example** | Skim scene advances time with no next code |
| **Pass criteria** | Every non-terminal has ≥1 valid next reference |

#### QA-NV-03 — Broken references

| Field | Value |
|---|---|
| **Purpose** | Link integrity |
| **Failure condition** | Destination code does not exist |
| **Severity** | Critical |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Code inventory |
| **Metric** | Dangling refs = 0 |
| **False-positive risk** | Low |
| **Human review** | None |
| **Example** | Go to P-213b but only P-213 exists as Okonkwo |
| **Pass criteria** | Zero dangling references |

#### QA-NV-04 — Impossible state combinations in player text

| Field | Value |
|---|---|
| **Purpose** | Visible mechanics consistency |
| **Failure condition** | PLAYER conditional references tag/state never writable or mutually exclusive pair required |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | State writers/readers |
| **Metric** | Writer coverage for every player-facing condition |
| **False-positive risk** | Low–Medium |
| **Human review** | Required for complex flags |
| **Example** | “If they trust you” with no trust tracker |
| **Pass criteria** | Every PLAYER conditional has a sheet field/tag writer |

#### QA-NV-05 — Endings cite unavailable information

| Field | Value |
|---|---|
| **Purpose** | Ending fairness |
| **Failure condition** | Ending prose asserts facts/clue IDs that cannot be held on that ending’s legal trigger set |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Ending matrix; ending text |
| **Metric** | Clue ID ⊆ possible held set |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Timeout ending names killer and method players never proved |
| **Pass criteria** | Ending text only uses facts consistent with trigger conditions |

---

### 5.9 Time and pacing

#### QA-TM-01 — Cosmetic thresholds

| Field | Value |
|---|---|
| **Purpose** | Time with teeth |
| **Failure condition** | Declared threshold does not remove/worsen a meaningful option on a standard fair path |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Threshold table; hub options |
| **Metric** | Gate impact score (critical vs flavour) |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Threshold locks vending only; murder routes unchanged |
| **Pass criteria** | Each threshold gates ≥1 high-value option on standard path |

#### QA-TM-02 — No real trade-off (can do nearly everything)

| Field | Value |
|---|---|
| **Purpose** | Scarcity as decision engine |
| **Failure condition** | Sum of all optional investigation time costs ≤ remaining clock budget on standard pace (players can complete ≥90% of optional actions) |
| **Severity** | Major |
| **Automatable** | Partial |
| **Tier** | B |
| **Required inputs** | Action cost matrix; clock span |
| **Metric** | Optional-action coverage ratio |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | 4-hour clock, 90 minutes of content |
| **Pass criteria** | Completing all options exceeds clock **or** forces missing a proof-relevant action |

#### QA-TM-03 — Unavoidable timing softlock

| Field | Value |
|---|---|
| **Purpose** | Protect fair paths (U7) |
| **Failure condition** | Essential fair-path action is only available before a threshold that always fires before players can reach it on minimum legal timing |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Min path timing; thresholds |
| **Metric** | Feasibility of fair path under min costs |
| **False-positive risk** | Low |
| **Human review** | Required |
| **Example** | Bakery interview required but T1 always elapsed before hub |
| **Pass criteria** | ≥1 fair path remains timing-feasible |

#### QA-TM-04 — Wall-clock estimate formula & volume consistency

| Field | Value |
|---|---|
| **Purpose** | Prevent Glass Alibi estimate failure class |
| **Failure condition** | Estimate sums both roles **or** estimate vs word-count heuristic differs by >25% |
| **Severity** | Major |
| **Automatable** | Yes |
| **Tier** | A |
| **Required inputs** | Compilation report; PLAYER word counts |
| **Metric** | §5.4 formula check; words÷reading-rate band |
| **False-positive risk** | Medium |
| **Human review** | Optional |
| **Example** | 120 min claimed for ~6k words of sparse menus |
| **Pass criteria** | Formula correct; volume band within ±25% or explained |

---

### 5.10 Fairness

#### QA-FR-01 — Required conclusion lacks evidence

| Field | Value |
|---|---|
| **Purpose** | Fair play U3 |
| **Failure condition** | Correct ending requires a fact never obtainable on that path |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Ending matrix; clue graph |
| **Metric** | Dependency closure |
| **False-positive risk** | Low |
| **Human review** | Required |
| **Example** | Motive required but motive clue only in unused branch |
| **Pass criteria** | Every correct-path requirement is obtainable |

#### QA-FR-02 — Multiple explanations fit equally (no resolution)

| Field | Value |
|---|---|
| **Purpose** | Avoid unsolvable ambiguity |
| **Failure condition** | After all fair-path clues, ≥2 suspects remain equally consistent with all proof tags with no distinguishing Infer |
| **Severity** | Critical |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | Truth; full clue set |
| **Metric** | Eliminability audit |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Method and opportunity fit two people; motive never distinguishes |
| **Pass criteria** | Fair-path evidence uniquely supports culprit among majors |

#### QA-FR-03 — Culprit detectable by emphasis, not evidence

| Field | Value |
|---|---|
| **Purpose** | Bind NS + FR |
| **Failure condition** | Blind reader identifying culprit from PLAYER tone/structure alone (spoiler sheet hidden) succeeds before mid-case Infer |
| **Severity** | Critical |
| **Automatable** | No |
| **Tier** | B (+ optional C early-stop probe) |
| **Required inputs** | PLAYER only |
| **Metric** | Blind culprit-guess protocol |
| **False-positive risk** | Medium |
| **Human review** | Required |
| **Example** | Reviewer names finder as killer from opening alone |
| **Pass criteria** | Blind guess not reliably correct before evidence Infer |

#### QA-FR-04 — Suspicious innocence treated as proof

| Field | Value |
|---|---|
| **Purpose** | Protect A3 |
| **Failure condition** | Ending or worksheet treats nervous/evasive innocent behaviour as sufficient proof of guilt |
| **Severity** | Major |
| **Automatable** | No |
| **Tier** | B |
| **Required inputs** | Wrong-ending logic; worksheets |
| **Metric** | Proof sufficiency rules exclude demeanor-only |
| **False-positive risk** | Low |
| **Human review** | Required |
| **Example** | Accuse nervous tenant with only demeanor tag → “correct” |
| **Pass criteria** | Guilt requires evidence categories, not affect alone |

#### QA-FR-05 — Failed checks erase only fair solution

| Field | Value |
|---|---|
| **Purpose** | U7 soft-lock prevention |
| **Failure condition** | Any check fail permanently removes the only route to a required proof category without recovery/degraded alternative |
| **Severity** | Critical |
| **Automatable** | Partial |
| **Tier** | A+B |
| **Required inputs** | Check register; redundancy graph |
| **Metric** | Fail → still solvable? |
| **False-positive risk** | Low |
| **Human review** | Required |
| **Example** | Fail invoice check → no motive path remains |
| **Pass criteria** | Every fail has recovery, substitute, or intentional visible failure ending |

---

## 6. Tier separation

### A. Fully automatable

Run as scripts/CI on every generation:

`QA-SP-03`, `QA-NS-01`, `QA-NS-04`, `QA-ST-01`, `QA-FA-01`, `QA-IN-02`, `QA-CL-01`, `QA-CL-04`, `QA-RC-01`, `QA-RC-03`, `QA-NV-01`, `QA-NV-02`, `QA-NV-03`, `QA-TM-04`  
Plus partial automation feeding B: `QA-SP-01`, `QA-FA-02`, `QA-CL-03`, `QA-RC-02`, `QA-NV-04`, `QA-TM-03`, `QA-FR-01`, `QA-FR-05`

### B. AI-reviewable

Structured prompts with mandatory evidence citations (file + quote). AI may **flag**, not waive:

All Partial/No automatable checks above, especially:  
`QA-SP-02`, `QA-SP-04`, `QA-NS-02`, `QA-NS-03`, `QA-ST-02`, `QA-ST-03`, `QA-ST-04`, `QA-FA-03`, `QA-IN-01`, `QA-IN-03`, `QA-CL-02`, `QA-RC-04`, `QA-NV-05`, `QA-TM-01`, `QA-TM-02`, `QA-FR-02`, `QA-FR-03`, `QA-FR-04`

**AI review rule:** Every FAIL must quote player-facing text. Every PASS on Critical B-checks must state why the Harborview-class failure is absent.

### C. Human-playtest only

Cannot be certified by scripts or AI alone:

| Check ID | Name | Measures |
|---|---|---|
| QA-HP-01 | Lived wall-clock | Actual session vs estimate (±15 min band) |
| QA-HP-02 | Felt agency | Players report choosing investigations, not following a tour |
| QA-HP-03 | Idle wait | Max observed wait during splits ≤5 min |
| QA-HP-04 | Culprit lock timing | No reliable pre-evidence culprit lock from tone alone |
| QA-HP-05 | Infer ownership | Players can articulate theory in their own words before ending |
| QA-HP-06 | Cooperation feel | Both players rate contribution ≥3/5 |
| QA-HP-07 | Ending clarity | Players cite sheet conditions for outcome without confusion |
| QA-HP-08 | Confusion incidents | Count of “what do we do?” stalls; investigate if ≥3 |
| QA-HP-09 | Emotional stake recall | Each player can state why the case matters before accusation |
| QA-HP-10 | Language load | Players flag unreadably dense passages |

---

## 7. Automated checks (implementation notes)

Minimum automated harness:

1. **Inventory graph builder** — parse PLAYER destinations → adjacency list.  
2. **Suspect corpus counter** — name frequencies.  
3. **Steering linter** — keyword ban with allowlist.  
4. **Hub collision detector** — identical destinations in decision tables.  
5. **Clue mode auditor** — Auto ∩ proof-critical.  
6. **Role grant auditor** — proof-critical %.  
7. **Continuation linter** — missing Go-to / Continue.  
8. **Estimate formula checker** — reject sum-of-roles.

Automations emit machine-readable JSON consumed by the QA report template.

---

## 8. Pass / Fail / Waiver rules

### Pass

- Critical: all PASS  
- Major: all PASS or waived  
- Minor: logged  

### Fail

- Any Critical FAIL  
- Any unwaived Major FAIL  
- Incomplete Tier A run  
- Incomplete Tier B on Critical/Major B-checks  

### Waiver rules

| Severity | Waiver allowed? | Authority |
|---|---|---|
| Critical | **Never** | — |
| Major | Yes, written | Adventure owner + one reviewer |
| Minor | Not required | Log only |

Waiver MUST include: check ID, reason, player-impact mitigation, expiry (adventure version).  
Waivers that recreate Harborview-class Critical patterns are invalid even if labeled Major.

### Relationship to engine Ready

| Engine §13.2 gate | Covered primarily by |
|---|---|
| Wall-clock estimate | QA-TM-04, QA-HP-01 |
| Shared investigation | QA-RC-03, QA-HP-06 |
| Split balance | QA-RC-02, QA-HP-03 |
| Decision isolation | Hygiene + QA-ST-04 / scene lint |
| No steering | QA-ST-01, QA-ST-02 |
| Visible mechanics | QA-NV-04 |
| Time teeth | QA-TM-01 |
| Discovery / Infer | QA-IN-01, QA-IN-02, QA-CL-01 |
| Ending clarity | QA-NV-05, QA-HP-07 |
| Suspect weight | QA-NS-01–03, QA-FR-03 |
| Human playtest | Tier C suite |

Adventure QA **extends** engine gates with spoiler, fake-agency, inference-theatre, and spotlight classes that structural Ready can miss.

---

## 9. QA report template

Use companion file:

**`ADVENTURE_QA_REPORT_TEMPLATE.md`**

Every adventure MUST attach a filled report before Pre-Playtest Ready.

---

## 10. Recommended first implementation order

### Wave 1 — Stop contaminated playtests (P0)

1. QA-SP-01, QA-SP-02, QA-SP-03 (spoilers)  
2. QA-FA-01 (identical destinations)  
3. QA-ST-01 (meta steering lint)  
4. QA-NV-01, QA-NV-02, QA-NV-03 (navigation)  
5. Report template + gate status field  

### Wave 2 — Experience risk (P0/P1)

6. QA-NS-01, QA-NS-03 (spotlight)  
7. QA-IN-01, QA-IN-02 (inference theatre)  
8. QA-CL-01, QA-CL-03, QA-RC-01, QA-RC-04 (clue/role)  
9. QA-ST-03 (soft bailouts)  
10. QA-TM-04 (estimate formula)  

### Wave 3 — Scarcity & fairness depth (P1)

11. QA-TM-01, QA-TM-02, QA-TM-03  
12. QA-FR-01, QA-FR-02, QA-FR-05  
13. QA-RC-02, QA-RC-03  
14. Blind culprit protocol QA-FR-03  

### Wave 4 — Human suite (P1)

15. Instrument Tier C checklist into playtest script  
16. Compare Harborview-class failures as regression fixtures (do not ship until Wave 1 green)

---

## 11. Global evaluation mandates

QA reviewers MUST answer these **adventure-level** questions (not only scene diffs):

1. If we remove all Infer worksheets, can the book still tell players who did it?  
2. If we shuffle suspect intro order, does one name still dominate the first hour?  
3. If either player is silent, can the other still complete proof tags?  
4. If players always pick the first hub option, do they miss meaningful content — or is every option the same?  
5. If the clock is ignored, does anything change?  
6. Does the sealed ending add information, or did mid-game rules already reveal the outcome?

Any “yes” to 1, 3 (as problem), 4-same, 5-nothing, or 6-already-revealed → investigate Critical/Major checks above.

---

## 12. Non-goals

This QA layer does **not**:

- rewrite the engine
- replace human playtesting
- grade literary prose quality beyond clarity stalls
- guarantee fun
- auto-approve AI-mass-generated libraries without Tier B+C sampling

---

*End of IDNE Adventure QA Specification.*

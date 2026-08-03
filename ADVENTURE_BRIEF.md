# Adventure Brief — IDNE v0.4 Benchmark Case

**Document type:** Design specification (pre-generation)  
**Engine target:** IDNE Engine v0.4  
**Philosophy:** `IDNE_DESIGN_PHILOSOPHY.md` Category A  
**Purpose:** Benchmark adventure to validate whether v0.4 delivers a **significantly better player experience** than prototype *The Glass Alibi*  
**Status:** Editable draft — human review before generation  
**Constraint:** This document MUST NOT contain story prose, scene text, dialogue, or spoilers.

---

## 0. Document control

| Field | Value |
|---|---|
| Working codename | `CASE_BENCHMARK_v0.4` |
| Intended adventure folder | `adventures/CASE_BENCHMARK_v0.4/` *(create at generation)* |
| Benchmark baseline | `adventures/The_Glass_Alibi/` (prototype-era; experience failures documented) |
| Generation scope | Design package + logic layer + Delivery Adapter output — **not** this brief |
| Human edit notes | *(add reviewer comments below before generation)* |

---

## 1. Mission

Produce a **fair-play, two-player cooperative detective mystery** that stress-tests every v0.4 **experience gate** (§13.2) and every Category A philosophy principle the Glass Alibi playtest exposed as weak in practice.

### 1.1 Success criteria (playtest)

The benchmark passes if a recorded two-player session shows **measurable improvement** over Glass Alibi on:

| Experience dimension | Glass Alibi failure (observed) | Benchmark MUST achieve |
|---|---|---|
| Wall-clock playtime | ~70 min actual vs 90–150 estimated (summed roles) | ~110–130 min wall-clock; estimate within ±15 min using §5.4 formula |
| Shared vs split | Felt almost entirely split | ≥40% clue-granting units Joint; partners describe investigating **together** |
| Split balance | First split ~10 min idle wait | Every split window ≤5 min estimated delta per role |
| Player direction | “Go to S-210” style menus | Diegetic action menus at hubs; players name what they chose to do |
| Clue delivery | Mostly handed on scene entry | Majority of major clues Observe or Earn; ≤3 Auto major clues |
| Inference | Little reasoning; collection tour | ≥2 substantive Infer beats before accusation; players articulate theory |
| Innocent suspects | Nervous innocents worked | ≥2 innocent suspects with credible nervous/evasive behaviour |
| Suspect weight | Early tone leak to one suspect | No player names culprit before mid-investigation without evidence |
| Time pressure | Inconsistent clock; no felt teeth | Every threshold closes a **meaningful** option; players cite a missed opportunity |
| Steering | Recommended choices appeared | Zero meta-steering; NPCs do not name next locations |
| Ending | Disconnected; unsure if correct | Sheet-checkable outcome; players cite which evidence justified result |
| Investment | Finished to finish | Players can state personal/institutional stake before accusation |
| Language | Unnecessarily difficult | Plain-language prose; no undefined mechanics |

### 1.2 Non-goals

- Beat Glass Alibi on **plot novelty** alone.
- Maximize branch count or page count.
- Introduce supernatural, fantasy, or science-fiction elements.
- Serve as a campaign pilot or series opener.

---

## 2. Player specification

| Parameter | Requirement |
|---|---|
| Player count | 2 (cooperative only for this benchmark) |
| Character level | 1 — competence implied; no advancement mechanics |
| Role model | Asymmetric **capabilities**, symmetric **protagonist importance** |
| Delivery model | Model B — separate player booklets + shared joint file + shared case sheet (v0.4 §11) |

### 2.1 Investigator roles (capability split, not story)

Define two player-facing roles without pre-written backstory. Players assign themselves at setup.

| Role | Primary capability focus | Must remain essential for |
|---|---|---|
| **Role A — People track** | Interviews, rapport, witness demeanor, social access | Motive reconstruction, alibi testing, nervous-innocent scenes |
| **Role B — Records track** | Documents, access logs, physical scene detail, timelines | Method reconstruction, opportunity windows, contradictions |

**Design rule:** Neither role can reach a fair accusation alone. Both must contribute at least one **required** clue category (method, motive, or opportunity) on every fair path.

### 2.2 Participation parity

- Both roles MUST have at least one **solo-relevant** action per split window.
- Neither role is “support” or “driver.”
- Longest individual branch estimate MUST NOT exceed joint estimate by more than 15 minutes.

---

## 3. World and genre parameters

| Parameter | Specification |
|---|---|
| Era | Present day |
| Realism | Completely realistic contemporary setting |
| Supernatural | Forbidden |
| Fantasy | Forbidden |
| Science fiction | Forbidden |
| Tone | Serious, grounded, believable |
| Violence presentation | Referenced factually; no graphic exploitation |
| Institutional context | Everyday bureaucracy and social pressure — not exotic |

### 3.1 Setting (structural, not narrative)

| Parameter | Specification | Rationale |
|---|---|---|
| **Location type** | Single mixed-use building: ground-floor commercial units + upper-floor residential units + shared service areas | Contained map; natural split (public floor vs units vs records); differs from Glass Alibi industrial campus |
| **Geography scale** | One building + immediate exterior (alley, street front, small rear yard) | Walkable in fiction; 4–7 primary locations without travel montage |
| **Population at scene** | Weekend evening into night; limited but non-empty occupancy | Explains who is present without crowd management |
| **Jurisdiction** | Local police already notified; players are **authorized investigators** (consultants, inspectors, or assigned pair — pick one at generation) | Removes “why are we here” friction without NPC tour guide |

**Human edit slot:** Replace building type if desired (e.g., community clinic, transit depot annex) — keep **single contained site** constraint.

### 3.2 Location budget (v0.4 §15)

| Target | Count | Notes |
|---|---:|---|
| Primary investigable locations | **5** | Each must offer ≥3 distinct investigative actions at least once |
| Secondary mention-only sites | ≤2 | No visit required for fair solution |
| Locked/inaccessible locations | ≥1 | Becomes relevant when a clock threshold fires |

**Suggested primary location categories** *(assign names at generation)*:

1. Ground-floor commercial unit (occupied)
2. Ground-floor commercial unit (closed / different tenant type)
3. Residential unit tied to incident
4. Shared building office or manager space
5. Service area (basement, utility, storage, or roof access)
6. *(optional)* Exterior rear / loading area

---

## 4. Mystery design parameters

### 4.1 Mystery type

| Parameter | Specification |
|---|---|
| **Mystery type** | Closed-environment **whodunit** with **method + motive reconstruction** |
| **Crime type** | Unexplained death initially ambiguous (accident vs negligence vs intentional); fair path must support intentional act as correct conclusion |
| **Solution shape** | Single correct perpetrator; guilt requires connecting **opportunity + method + motive** — no single “smoking gun” clue |
| **Twist policy** | No mastermind reveal; no hidden second killer; no “everyone was in on it” |

### 4.2 Victim profile (structural)

| Parameter | Specification |
|---|---|
| Role in setting | Person with legitimate reason to be in the building that night |
| Social position | Mid-level — not so powerful the case becomes political thriller, not so marginal that nobody cares |
| Relationship web | Connected to ≥3 major suspects through work, residence, or building affairs |
| Narrative function | Victim’s **routine and conflicts** supply motive seeds; victim is **not** a secret villain |

### 4.3 Cast and suspect parameters

| Parameter | Target | Hard limits (v0.4 §15) |
|---|---:|---|
| Named NPCs with dialogue | 8–10 | — |
| **Major suspects** | **4** | 3–5 |
| Minor witnesses / functionaries | 3–4 | No dialogue depth parity required |
| Investigators (players) | 2 | — |

**Major suspect design rules:**

- Each suspect MUST have a **credible innocent explanation** for suspicious facts.
- ≥2 suspects MUST exhibit nervous, evasive, or self-protective behaviour **without being guilty**.
- All 4 introductions MUST pass equal-weight review (§2.4): comparable word budget, neutral diction, no unique villain epithets, no “only calm one” trope.
- No suspect is introduced last with disproportionate helpfulness or spotlight.

**Human edit slot:** Adjust suspect count within 3–5 if cast needs simplification.

### 4.4 Red herring policy

| Allowed | Forbidden |
|---|---|
| Innocent nervousness | Cartoon decoys |
| Misleading timelines from honest mistake | Fabricated nonsense clues |
| Self-incriminating behaviour protecting unrelated secret | Coincidence that implicates exactly one person |
| Incomplete records | Records that contradict fixed truth |

---

## 5. Investigation design

### 5.1 Investigation style

| Parameter | Specification |
|---|---|
| **Primary mode** | Player-directed hub investigation under scarcity |
| **Hub model** | 3 investigation hubs (opening, mid-case, pre-accusation) each exposing **≥4 diegetic actions** simultaneously |
| **Revisit policy** | Players MAY revisit a location once per hub phase at declared time cost; second revisit closes after first clock threshold |
| **Ask-the-world** | Shared case sheet includes “Follow up on: ___” slot resolving to a **pre-authored** response or “nothing new” — max 2 uses |
| **Rail tolerance** | Linear **sequence of hubs** allowed; within each hub, action order is player-chosen |

This implements the **Static Medium Contract**: bounded authored action space, not freeform parser.

### 5.2 Clue economy

| Parameter | Target | Notes |
|---|---:|---|
| Meaningful clues (active) | **14** | Within 12–20 guidance |
| Clue acquisition — Observe | ≥4 | Sensory/detail on scene entry after choosing to look |
| Clue acquisition — Earn | ≥6 | Check, cost, leverage, or time cost required |
| Clue acquisition — Infer | ≥3 | Player synthesis steps (see §5.3) |
| Clue acquisition — Auto | ≤3 | **Major** clues only; minor flavour Auto allowed |
| Independent routes to final conclusion | ≥2 | v0.4 §2.3 redundancy |
| Clue density | Medium-high | ~1 meaningful clue per 8–10 minutes wall-clock |

**Anti-pattern (Glass Alibi):** Do not grant a major clue merely for entering a scene. Entry may grant **orientation** only.

### 5.3 Inference difficulty

| Parameter | Specification |
|---|---|
| Difficulty label | **Medium** — requires thinking; solvable without external research |
| Infer beat 1 (mid-case) | Regroup: combine two Earn/Observe facts to eliminate one suspect category (method OR opportunity) |
| Infer beat 2 (late-case) | Regroup: choose between two competing theories using ≥3 held clues; wrong choice costs time, not auto-fail |
| Infer beat 3 (accusation prep) | Joint: map motive to perpetrator using timeline + one document clue + one witness fact |
| Infer presentation | Structured worksheet on case file — **not** a single checkbox |
| Forbidden | Deduction requiring specialist knowledge not taught in play |

### 5.4 Checks (Category B)

| Parameter | Specification |
|---|---|
| Check count | 3–4 total |
| Check purpose | Gate **quality or speed** of Earn clues — not sole access to fair solution |
| Failure effect | Higher time cost, degraded certainty tag, or alternate Earn path |
| Isolation | Pass/fail outcomes in **destination units**, not decision units (v0.4 §7.2 / RT-07) |

---

## 6. Cooperation and scene structure

### 6.1 Cooperation style

| Parameter | Specification |
|---|---|
| **Target cooperation model** | Shared case ownership with **perspective splits** and **mandatory joint synthesis** |
| Joint clue-granting share | **≥45%** of clue-granting units (exceeds §6.3 SHOULD floor deliberately) |
| Joint reasoning scenes | **≥2** structured beats where both players must contribute private facts to resolve a contradiction |
| Communication while split | Allowed via short phone/text with **10-minute world-time cost** per exchange; content is player-spoken, not pre-printed dump |
| Anti-pattern | Two parallel solo mysteries that trade note cards at sync |

### 6.2 Scene mode budget

| Phase | Joint | Split | Notes |
|---|---:|---:|---|
| Opening (first 20 min) | **100%** | 0% | Establish stakes, hub, first cooperative choices |
| Act 1 | 50% | 50% | One short split window |
| Act 2 | 40% | 60% | One split window — balanced paths |
| Act 3 (endgame) | **≥70%** | ≤30% | Accusation prep and resolution together |

### 6.3 Split windows

| Parameter | Specification |
|---|---|
| Split window count | **2** | ≤3 per v0.4 §15 |
| Window 1 placement | Early Act 1 — **≤12 min** per role estimate |
| Window 2 placement | Act 2 — **≤15 min** per role estimate |
| Balance rule | Each window: \|Role A − Role B\| ≤ **4 min** estimated |
| Early-finish options | Predefined “review notes / stake out / call in” actions that cost time but avoid idle wait |
| Sync terminators | Rejoin in person both times; no free async drift |

### 6.4 Wall-clock playtime model

Design to **~120 minutes** real cooperative time.

```text
estimated_wall_clock =
    sum(joint_scene_play_estimates)
  + sum_over_split_windows( max(role_A_estimate, role_B_estimate) )
  + endgame_estimate
```

| Segment | Target estimate |
|---|---:|
| Opening joint block | 20 min |
| Act 1 (incl. split 1) | 30 min |
| Act 2 (incl. split 2) | 35 min |
| Act 3 + endings | 25 min |
| Buffer (table talk, sheet updates) | 10 min |
| **Total target** | **~120 min** |

**MUST NOT** estimate by summing both players’ full paths. Report longest individual branch separately.

---

## 7. Time pressure and pacing

### 7.1 World clock

| Parameter | Specification |
|---|---|
| Clock span | **Single continuous evening** — ~4 hours in-world |
| Start time | *(assign at generation)* |
| Hard deadline | Building lockdown / suspect departure / official report filing |
| Clock display | Shared case sheet only; monotonic increase |
| Advance rule | Per-action costs + max(role elapsed) at sync (v0.4 §5.3) |

### 7.2 Thresholds (must have teeth)

Declare **3** thresholds. Each MUST remove or worsen a **meaningful** investigation option.

| Threshold | In-world trigger (example slot) | Must gate |
|---|---|---|
| T1 (~+60 min) | *(e.g., business closes)* | One ground-floor interview OR one document source |
| T2 (~+120 min) | *(e.g., residents retire / logs rotate)* | One residential access OR one witness availability |
| T3 (~+180 min) | *(e.g., building secures)* | Rear/service access OR extended search; triggers endgame pressure |

**Forbidden:** Threshold that only locks a flavour option (vending machine, gift shop).  
**Required:** At least one gated option is on a **standard fair path** — missing it forces fallback route with higher cost.

### 7.3 Pacing curve

| Act | Pacing intent |
|---|---|
| Opening | Orient, establish stakes, first player-chosen actions — **no split** |
| Act 1 | Expand action space; introduce 2 suspects; first Infer setup |
| Act 2 | Scarcity bites; nervous innocents; split + regroup synthesis |
| Act 3 | Narrow field; second Infer; accusation hub; cooperative decision |
| Endgame | Short — resolution and consequence, not new investigation continent |

### 7.4 Emotional tone and stakes

| Parameter | Specification |
|---|---|
| **Emotional tone** | Quiet urgency; interpersonal friction; institutional inconvenience — not melodrama |
| **Stakes (visible)** | Players learn within opening **why this case matters to them professionally or personally** — one sentence each role |
| **Stakes (institutional)** | If deadline missed, a defined bad outcome occurs (wrong person released, report filed incomplete, innocent harmed) |
| **Investment source** | Deadline + human cost + professional reputation — **not** twist density (Philosophy A17) |
| **Avoid** | Shock reveals, villain monologues, grief exploitation |

---

## 8. Endings

### 8.1 Terminal outcomes

| Parameter | Target |
|---|---:|
| Terminal count | **5** |
| Categories required | Correct accusation; wrong accusation; incomplete case; time expired with partial truth; intentional fair failure *(e.g., chose not to accuse)* |

### 8.2 Desired ending feeling

| Outcome type | Player should feel |
|---|---|
| Correct accusation | **Earned certainty** — “we proved it because of X, Y, Z” |
| Wrong accusation | **Consequence clarity** — which evidence misled them |
| Incomplete / time out | **Bitter plausibility** — case still open; they know what they missed |
| Partial success | **Qualified relief** — right direction, insufficient proof |

### 8.3 Ending communication rules (v0.4 §8.3)

- Selection MUST be sheet-checkable (clue IDs + public tags).
- Ending text MUST narrate the **causal chain**, not only list condition codes.
- Priority order declared in logic layer.
- No “were you right?” honor system.

---

## 9. Player experience constraints (v0.4 MUST / SHOULD)

### 9.1 Decision presentation

| Rule | Requirement |
|---|---|
| Diegetic choices | “Interview the building manager,” not “go to B-210” |
| Decision isolation | Decision units: action + destination only |
| Consequence location | Destination units only |
| Fake choices | No two options with identical cost and outcome |
| Hub size | ≥4 actions at each investigation hub |

### 9.2 Neutrality and steering

| Forbidden | Allowed |
|---|---|
| “Recommended,” “best,” “you should” | Neutral action lists |
| NPC naming next location to investigate | NPC expressing self-interest or institutional policy |
| Page codes as choices | Codes after action labels only |
| Unequal suspect intro emphasis | Equal-weight intro audit |

### 9.3 Player-visible mechanics

Every conditional in player text MUST map to case sheet field or public tag.

| Likely sheet fields (cap within budget §4.4) | Purpose |
|---|---|
| World clock | Time |
| Clue log (by ID) | Evidence |
| Theory worksheet | Infer beats |
| Threshold flags T1–T3 | Gated options |
| Access tags | Location availability |
| Certainty / degradation tags | Check failures |

**Forbidden:** “If they trust you” without trust tracker. Prefer stage tags: `WITNESS_COOPERATIVE` / `WITNESS_SHUT_DOWN`.

### 9.4 Language

- Short sentences; common vocabulary.
- Explain institutional terms on first use.
- Reading level target: general adult, not legal/technical jargon without gloss.

---

## 10. v0.4 experience gates — explicit test matrix

This adventure is the **reference proof** for Version 0.4 Ready (Refactoring Plan M6). Generation MUST enable verification of:

| Gate (v0.4 §13.2) | How this brief tests it |
|---|---|
| Wall-clock estimate | §6.4 formula and segment budget |
| Shared investigation | §6.1 ≥45% Joint clue units |
| Split balance | §6.3 ≤4 min delta per window |
| Decision isolation | §9.1 |
| No steering | §9.2 |
| Visible mechanics | §9.3 |
| Time teeth | §7.2 three meaningful gates |
| Discovery / Infer | §5.2–5.3 ≥3 Infer beats; Auto cap |
| Ending clarity | §8.3 causal narration |
| Suspect weight | §4.3 equal-weight rules |
| Human playtest | Recorded session vs §1.1 success criteria |

**Waiver policy for this benchmark:** No waivers on shared investigation, split balance, or Infer quality. If a gate fails, fix the adventure — do not waive.

---

## 11. Anti-patterns checklist (do not generate)

- [ ] Obvious murderer from intro tone or suspect order
- [ ] Mastermind / hidden puppeteer twist
- [ ] Narrator voice that knows guilt
- [ ] Guilt by coincidence
- [ ] Deduction without fairly obtainable clues
- [ ] Hidden information that was never discoverable
- [ ] NPC dialogue that tells players where to go next
- [ ] Standalone puzzles disconnected from investigation
- [ ] Major clues granted on scene entry (Auto dump)
- [ ] Single checkbox Infer to satisfy gate
- [ ] Split-majority scene graph with token Joint stubs
- [ ] Cosmetic time thresholds
- [ ] Undefined trust/nervousness/mechanics
- [ ] Recommended choice language
- [ ] Consequence spoilers on decision pages
- [ ] Ending that asks players to self-judge correctness

---

## 12. Content budget summary

| Item | Target |
|---|---:|
| Investigators | 2 |
| Major suspects | 4 |
| Primary locations | 5 |
| Meaningful clues | 14 |
| Infer beats | 3 |
| Split windows | 2 |
| Clock thresholds | 3 |
| Skill checks | 3–4 |
| Terminal endings | 5 |
| Investigation hubs | 3 |
| Joint reasoning scenes | 2 |
| Estimated wall-clock | ~120 min |

---

## 13. Generation pipeline notes

1. **World Bible** — objective truth, timeline, NPC knowledge/beliefs only.  
2. **Adventure Logic** — authoritative; actions, costs, gates, evaluators.  
3. **Delivery Adapter** — compile PLAYER from logic; enforce §9.  
4. **Validation** — hygiene PLUS §10 gate matrix; human playtest mandatory.

**Do not** manually approximate PLAYER booklets without logic compilation (Glass Alibi failure mode).

---

## 14. Human editor checklist (before generation)

- [ ] Confirm setting type in §3.1 (or substitute equivalent contained site)
- [ ] Confirm investigator authority model (consultants vs inspectors)
- [ ] Confirm suspect count (4) within team preference
- [ ] Confirm clock span and threshold times fit ~2h wall-clock
- [ ] Add any locale-specific legal constraints (optional)
- [ ] Sign off: “Approved for generation” + date + name

---

*End of Adventure Brief. No adventure content follows this document.*

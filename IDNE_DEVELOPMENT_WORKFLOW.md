# IDNE Development Workflow

**Document type:** Official development lifecycle  
**Applies to:** Every future IDNE adventure from idea to release  
**Status:** Normative process (does not modify the engine, QA spec, or adventures)  
**Aligned with:** `IDNE_ENGINE_v0.4.md`, `IDNE_DESIGN_PHILOSOPHY.md`, `IDNE_ADVENTURE_QA_SPEC.md`, `ADVENTURE_QA_REPORT_TEMPLATE.md`, `SINGLE_INVESTIGATOR_MODE_SPEC.md`, `WORLD_FIRST_GENERATION_SPEC.md`, `ENVIRONMENT_SYSTEM_SPEC.md`, `OBJECT_INTERACTION_SYSTEM_SPEC.md`, `INVESTIGATION_CORE_SPEC.md`

---

## 0. Purpose

This workflow is the permanent path by which IDNE adventures move from idea to release.

It exists to scale to **hundreds of adventures** without:

- treating one bad playtest as an engine crisis
- shipping tours that pass file checks
- endless redesign loops
- overfitting rules to a single case (e.g. one Harborview-class failure)

**Hard rule:** Classify the defect **before** choosing the fix layer. Never skip classification.

---

## 1. Workflow diagram

```text
┌─────────────────────┐
│ 0. Idea / Request   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ 1. Adventure Brief  │◄──────────────────────────────┐
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 2. Generation       │  World-First → Logic → PLAYER │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 3. Technical        │  Hygiene / structural         │
│    Validation       │                               │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐     FAIL                      │
│ 4. Adventure QA     │──────────────► Fix (stage 9)  │
│  (Tier A+B)         │               then re-enter   │
└──────────┬──────────┘               at 3 or 4       │
           │ Pre-Playtest Ready                       │
           ▼                                          │
┌─────────────────────┐                               │
│ 5. Human Playtest   │                               │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 6. Playtest Report  │                               │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 7. Root Cause       │                               │
│    Classification   │                               │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 8. Layer Decision   │                               │
│ Engine│Generator│   │                               │
│ Brief│Adventure│QA  │                               │
└──────────┬──────────┘                               │
           ▼                                          │
┌─────────────────────┐                               │
│ 9. Fix (one layer)  │───────────────────────────────┘
└──────────┬──────────┘   (brief/gen/adventure/QA/engine*)
           ▼
┌─────────────────────┐
│ 10. Regression QA   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐     if experience-affecting
│ 11. Regression      │     Critical/Major fix
│     Playtest?       │──── yes ──► stage 5 (scoped)
└──────────┬──────────┘
           │ no / pass
           ▼
┌─────────────────────┐
│ 12. Release         │
└─────────────────────┘

* Engine fixes require the Engine Change Protocol (§4.3).
  Never enter engine fix from a single adventure without protocol.
```

**Status labels used throughout:**

| Status | Meaning |
|---|---|
| Brief Approved | Human signed the Adventure Brief |
| Generated | Design package + PLAYER exist |
| Hygiene PASS | Technical validation passed |
| Pre-Playtest Ready | Adventure QA gate passed (`IDNE_ADVENTURE_QA_SPEC`) |
| Playtested | Tier C session recorded |
| Adventure Ready | Playtest + classification closed; experience gates met |
| Released | Published under Release Policy (§6) |

---

## 2. Stage descriptions

### Stage 1 — Adventure Brief

| Field | Value |
|---|---|
| **Purpose** | Lock design targets before content exists so generation is constrained, not freestyle |
| **Required inputs** | Engine v0.4 complexity guidance; Design Philosophy Category A; product request (players, length, tone) |
| **Expected outputs** | `ADVENTURE_BRIEF.md` (or adventure-scoped brief) — parameters only, **no story prose** |
| **Exit criteria** | Brief states `play_modes`, player count, wall-clock target (§5.4 or §5.4.1 per mode), cast/location/clue budgets; cooperation/split targets when `two_player`; solo routing intent when `single_investigator` |
| **Responsible actor** | **Human** owns approval; **AI** may draft |

**Anti-mistake:** Do not generate World Bible or PLAYER before Brief Approved. Do not smuggle plot spoilers into the brief.

---

### Stage 2 — Adventure Generation

| Field | Value |
|---|---|
| **Purpose** | Implement the brief as a fair mystery world + playable delivery |
| **Required inputs** | Approved brief; engine v0.4; philosophy |
| **Expected outputs** | `generation_manifest.json` + `world_truth_package.json` (World-First); `DO_NOT_READ/` World Bible + Logic; `PLAYER/` via Delivery Adapter; `play_manifest.json` when applicable; compilation report with §5.4 / §5.4.1 wall-clock |
| **Exit criteria** | Package complete per brief; World-First gates G-WF1–G-WF7 PASS when declared; internal IDs stable; PLAYER spoiler-isolated |
| **Responsible actor** | **AI** / generator primary; **Human** spot-checks scope drift |

**Order inside generation (mandatory for World-First):**

1. Fixed Truth → … → Conclusions (gates G-WF1–G-WF6)  
2. Environment Package (locations, states, navigation — `ENVIRONMENT_SYSTEM_SPEC.md`)  
3. Object Interaction Package  
4. Investigation Core Package (`INVESTIGATION_CORE_SPEC.md`)  
5. Adventure Logic  
6. Delivery Adapter → PLAYER

**Order for legacy (non-World-First):**

1. World Bible (fixed truth)  
2. Adventure Logic  
3. Delivery Adapter → PLAYER  

**Anti-mistake:** Do not hand-write PLAYER that contradicts Logic or World Truth Package.

---

### Stage 3 — Technical Validation (Hygiene)

| Field | Value |
|---|---|
| **Purpose** | Prove structural completeness — necessary, **never sufficient** for release |
| **Required inputs** | Generated package; hygiene validators; `world_first_validate`; `environment_validate`; `object_interaction_validate`; `investigation_core_validate`; `single_investigator_validate` when declared |
| **Expected outputs** | Hygiene report (identifiers, reachability, terminals, clue inventory, sheet fit) |
| **Exit criteria** | Hygiene PASS (or documented non-play-blocking exceptions) |
| **Responsible actor** | **Script** primary; **Human** reviews failures |

**Anti-mistake:** **Never** accept an adventure for playtest or release on hygiene PASS alone. Harborview-class failures can be Hygiene PASS and still QA FAIL.

---

### Stage 4 — Adventure QA

| Field | Value |
|---|---|
| **Purpose** | Detect poor detective experience before humans play (spoilers, fake agency, inference theatre, imbalance, etc.) |
| **Required inputs** | Hygiene PASS package; `IDNE_ADVENTURE_QA_SPEC.md`; report template |
| **Expected outputs** | Filled `ADVENTURE_QA_REPORT` (Tier A + Tier B); gate status |
| **Exit criteria** | **Pre-Playtest Ready** or **Waived Ready** per QA spec (all Critical PASS; Majors PASS or approved waiver) |
| **Responsible actor** | **Script** (Tier A); **AI** (Tier B flags); **Human** confirms Critical B passes and waivers |

**On QA FAIL:** Go to Stage 9 (Fix) targeting the classified layer — usually **Adventure** or **Generator**, rarely Brief. Re-enter at Stage 3 or 4. Do **not** jump to Engine.

**Anti-mistake:** Do not invite playtesters on QA FAIL. Do not waive Critical checks.

---

### Stage 5 — Human Playtest

| Field | Value |
|---|---|
| **Purpose** | Establish lived experience as primary truth for Tier C gates |
| **Required inputs** | Pre-Playtest Ready package; QA report; playtest script (QA-HP-01–10) |
| **Expected outputs** | Raw session notes / recording; timing log; player debrief answers |
| **Exit criteria** | Full session attempted (or documented abort); Tier C checklist filled |
| **Responsible actor** | **Human** players + facilitator; **AI** may assist note structure only |

**Anti-mistake:** Do not coach players mid-session. Do not treat a skim read as a playtest. Do not change content mid-session.

---

### Stage 6 — Playtest Report

| Field | Value |
|---|---|
| **Purpose** | Convert raw play into durable, spoiler-controlled findings |
| **Required inputs** | Session notes; QA report; brief success criteria |
| **Expected outputs** | Playtest report: wall-clock, waits, agency, cooperation, infer ownership, ending clarity, confusion count, stake recall; issue list with severity |
| **Exit criteria** | Every observed problem has a written finding ID; no silent “felt fine” without Tier C scores |
| **Responsible actor** | **Human** owns; **AI** may draft from notes |

**Anti-mistake:** Do not bury Critical experience failures as “nice to have.” Do not mix engine speculation into the report’s factual section — keep “what happened” separate from “why.”

---

### Stage 7 — Root Cause Classification

| Field | Value |
|---|---|
| **Purpose** | Explain *why* each finding occurred before any fix |
| **Required inputs** | Playtest report; adventure package; engine rules cited; brief; QA report (did QA miss it?) |
| **Expected outputs** | Per-finding root cause record: Class, evidence, confidence, proposed layer |
| **Exit criteria** | Every Critical/Major finding classified; confidence stated; no finding left as “just fix the text” without class |
| **Responsible actor** | **Human** lead; **AI** may propose classes with evidence |

**Anti-mistake:** Skipping this stage causes engine edits for content bugs and content rewrites for engine gaps.

---

### Stage 8 — Layer Decision

| Field | Value |
|---|---|
| **Purpose** | Choose exactly one primary fix layer per finding (see §4) |
| **Required inputs** | Root cause records |
| **Expected outputs** | Decision log: finding → layer → change ticket |
| **Exit criteria** | No finding assigned to two layers as “primary”; Engine assignments invoke Engine Change Protocol |
| **Responsible actor** | **Human** (project owner) |

---

### Stage 9 — Fix

| Field | Value |
|---|---|
| **Purpose** | Apply the smallest correct change at the decided layer |
| **Required inputs** | Decision log; scoped ticket |
| **Expected outputs** | Diff in one primary layer; changelog note |
| **Exit criteria** | Fix matches class; no drive-by edits to other layers; version bumped if engine |
| **Responsible actor** | **AI** and/or **Human** implementers |

**Fix routing:**

| Layer | Typical fix | Re-entry |
|---|---|---|
| Adventure | PLAYER / Logic content | Stage 3 → 4 |
| Generator | Prompts, adapter rules, templates | Regenerate or patch → 3 → 4 |
| Adventure Brief | Targets/budgets/constraints | Stage 1 → 2… |
| QA | New check, metric, false-positive fix | Re-run Stage 4 on fixtures |
| Engine | Spec change via protocol | Version bump → update fixtures → 4 → maybe 5 |

**Anti-mistake:** One finding → one primary layer. Do not “also tweak the engine while we’re here.”

---

### Stage 10 — Regression QA

| Field | Value |
|---|---|
| **Purpose** | Prove the fix closed the finding without reopening Critical QA classes |
| **Required inputs** | Fixed package; prior QA report; failing check IDs |
| **Expected outputs** | Regression QA report: failed checks now PASS; no new Critical FAIL |
| **Exit criteria** | All targeted checks PASS; full Tier A green; Tier B re-run on touched Critical classes |
| **Responsible actor** | **Script** + **AI** Tier B; **Human** sign-off on Critical |

**Anti-mistake:** Do not re-playtest before Regression QA is green.

---

### Stage 11 — Regression Playtest (if needed)

| Field | Value |
|---|---|
| **Purpose** | Re-validate lived experience when the fix could change play feel |
| **Required inputs** | Regression QA PASS; scoped playtest plan |
| **Expected outputs** | Short playtest report focused on previously failing Tier C items |
| **Exit criteria** | Previously failing experience metrics pass **or** new classification opened |
| **Responsible actor** | **Human** |

**When required (mandatory):**

- Any fix for Tier C Critical/Major experience failure  
- Any Engine change that alters player-facing rules  
- Any change to proof/ending/Infer structure  

**When optional:**

- Pure navigation typos with QA-NV coverage  
- Minor prose clarity with no mechanic change  

---

### Stage 12 — Release

| Field | Value |
|---|---|
| **Purpose** | Publish only Adventure Ready builds |
| **Required inputs** | Adventure Ready evidence pack (see §6) |
| **Expected outputs** | Released adventure tag; public PLAYER package; internal DO_NOT_READ retained private |
| **Exit criteria** | Release Policy checklist complete |
| **Responsible actor** | **Human** release owner; **Script** may package |

---

## 3. Decision tree after every playtest

```text
Playtest complete
        │
        ▼
Write Playtest Report (Stage 6)
        │
        ▼
For EACH finding (Critical → Major → Minor):
        │
        ▼
    Classify root cause (Stage 7)
        │
        ├──► QA miss? (should Tier A/B have caught it?)
        │         YES → also open QA finding (improve QA)
        │         NO  → continue
        │
        ▼
    Assign ONE primary layer (Stage 8)
        │
        ├── Adventure ──► Fix content ──► Reg QA ──► Reg Playtest if needed
        ├── Generator ──► Fix generator ──► Regen/patch ──► Reg QA ──► …
        ├── Brief ──────► Revise brief ──► Regen from Stage 2 ──► …
        ├── QA ─────────► Add/fix check ──► Re-run QA on this + fixtures
        └── Engine ─────► Engine Change Protocol (§4.3)
                              │
                              ├── Rejected ──► reclassify to Adventure/Generator/Brief
                              └── Accepted ──► versioned engine change
                                               ──► update fixtures
                                               ──► Reg QA on ≥1 reference adventure
                                               ──► Reg Playtest if player-facing
        │
        ▼
All Critical/Major findings closed?
        │
        ├── NO ──► continue fix loop (cap: §7.2)
        └── YES ──► Adventure Ready ──► Release (§6)
```

**Stop conditions for the loop:** see Continuous Improvement (§7).

---

## 4. Issue classification rules

### 4.1 Classes

| Class | Definition | Example pattern |
|---|---|---|
| **Engine** | Defect in reusable rules; would recur across adventures even with perfect content | Rule allows cosmetic thresholds; formula sums roles; Critical waiver allowed |
| **Generator** | Defect in how content is produced from a good brief/engine (prompts, adapter, templates) | Systematically emits identical hub destinations; always answers Infer in parentheses |
| **Adventure Brief** | Targets underspecified or contradictory; generation followed a bad contract | Brief allows 0 Infer quality; impossible wall-clock vs budget |
| **Adventure** | Local content/logic error in this package only | One ending dispatch names culprit; one orphan scene |
| **QA** | Check missing, too weak, or false-positive; bad adventure slipped to playtest | No check for parenthetical Infer answers |

A finding may list a **secondary** class (e.g. Adventure primary, QA secondary miss) but only **one primary fix layer**.

### 4.2 Classification tests (apply in order)

For each finding, answer:

1. **Would a correct adventure still hit this if the engine rule stayed as-is?**  
   - Yes → lean **Engine** (then apply §4.3).  
2. **Did the brief forbid this and generation still did it?**  
   - Yes → **Generator** (or Adventure if manual edit).  
3. **Did the brief allow or require the bad pattern?**  
   - Yes → **Brief** (then regenerate).  
4. **Is it unique wording/graph in this package?**  
   - Yes → **Adventure**.  
5. **Should Pre-Playtest Ready have blocked this?**  
   - Yes → open **QA** ticket (secondary or primary if only process failed).

**Default when unsure:** Classify as **Adventure** or **Generator**, **not Engine**. Engine is opt-in via protocol.

### 4.3 Engine Change Protocol (anti-overfit)

An Engine change is allowed only if **all** hold:

1. Finding reproduced or clearly implied in **≥2** adventures **or** contradicted by Design Philosophy Category A / explicit engine MUST.  
2. Written RFC: rule to change, adventures affected, migration plan, risk to existing Ready titles.  
3. Approval by project owner (Human).  
4. Version bump (`v0.4.x` / `v0.5`) — never silent edit.  
5. Update Adventure QA checks if the new rule is experience-facing.  
6. Regression QA on **at least one** reference adventure; playtest if player-facing.

**Single-adventure pain is not sufficient for Engine change.**  
Harborview-class issues default to Adventure/Generator/QA unless they prove a missing reusable rule.

### 4.4 Forbidden misroutes

| Mistake | Correct move |
|---|---|
| Bad scene → rewrite engine | Fix Adventure; maybe add QA check |
| Engine bug → rewrite one adventure only and claim Ready forever | Fix Engine via protocol; migrate |
| Hygiene PASS → Release | Must pass Adventure QA + playtest |
| Playtest dislike of setting → Engine identity change | Brief / Adventure content |
| One Infer wording bug → ban all worksheets in engine | Adventure + QA-IN-01 |

---

## 5. Regression policy

### 5.1 Always

After any Stage 9 fix:

1. Re-run **Tier A** full suite.  
2. Re-run **Tier B** on any Critical class touched.  
3. Update the Adventure QA report (delta section).  
4. Keep prior failing evidence until PASS recorded.

### 5.2 Fixture set

Maintain a small **regression fixture list** (not the entire library):

- Current reference / benchmark adventure(s)  
- At least one known failure corpus snippet per Critical QA class (can be minimized excerpts)  
- `tests/fixtures/solo_minimal` and `tests/fixtures/solo_invalid_split` for Single Investigator regression
- `tests/fixtures/wf_valid_minimal` and failure-class WF fixtures for World-First regression
- `tests/fixtures/env_valid_minimal` and failure-class ENV fixtures for Environment regression
- `tests/fixtures/obj_valid_nested` and failure-class OBJ fixtures
- `tests/fixtures/inv_core_valid_minimal` and failure-class INV fixtures

Generator or Engine changes must run fixtures before merge.

### 5.3 Regression playtest triggers

See Stage 11. If triggered and unavailable, status stays **Pre-Playtest Ready** or **Conditional** — **not Released**.

### 5.4 No silent regressions

If Regression QA introduces a new Critical FAIL, the fix is rejected even if the original finding is gone.

---

## 6. Release policy

### 6.1 Evidence pack (required)

| Artifact | Required |
|---|---|
| Approved Adventure Brief | Yes |
| Hygiene PASS | Yes |
| Adventure QA report → Pre-Playtest Ready (Critical clean) | Yes |
| Human playtest report + Tier C | Yes |
| Root cause log for all Critical/Major playtest findings | Yes (or “none”) |
| Regression QA after final fixes | Yes |
| Regression playtest if Stage 11 triggered | Yes if triggered |
| Version / changelog entry | Yes |

### 6.2 What may be released

| Package | Audience |
|---|---|
| `PLAYER/` | Players / public |
| Brief (spoiler-free summary only) | Optional public |
| `DO_NOT_READ/` | Internal only |
| QA / playtest / root-cause reports | Internal (spoiler risk) |

### 6.3 What must not be labeled Released

- Hygiene-only PASS  
- QA FAIL or unwaived Major  
- Playtest with open Critical experience findings  
- Engine-draft adventures without Adventure Ready  

### 6.4 Versioning adventures

`adventure@version` independent of engine when content-only; if built for engine `v0.4.x`, record `engine_compat` in release metadata.

### 6.5 Withdrawal

If a Released adventure is found to violate Critical QA class in the wild, withdraw or patch; open classification — do not quietly edit Engine to match the mistake.

---

## 7. Continuous improvement policy

### 7.1 Feedback sinks (where learning goes)

| Signal | Preferentially improves |
|---|---|
| Repeated content bug across titles | Generator + QA check |
| Missed by QA, caught in playtest | QA spec (new/harder check) |
| Brief targets produce bad play | Brief template / Stage 1 checklist |
| Rule conflict with Philosophy | Engine via §4.3 |
| One-off prose/graph bug | Adventure only |

### 7.2 Loop caps (prevent endless redesign)

| Cap | Rule |
|---|---|
| Content fix cycles per adventure before release | ≤ **3** full Stage 5–11 loops for Critical/Major; then escalate (Brief rewrite, Generator fix, or cancel) |
| Engine RFCs from one adventure | **0** unless §4.3 multi-adventure/philosophy bar met |
| Scope creep | No new mystery redesign after Playtested unless Brief is reopened deliberately |
| Waiver creep | Majors waived >2 on one title → Generator/Brief review, not more waivers |

### 7.3 Anti-overfit rules

1. Do not encode a single adventure’s setting tropes into Engine MUST rules.  
2. Do not delete a mechanic from the engine because one author misused it — fix Generator/QA.  
3. Philosophy Category A changes require explicit project decision; not a side effect of one playtest.  
4. Benchmark adventures (e.g. Harborview-class) are **fixtures**, not the definition of IDNE identity.

### 7.4 Cadence suggestions (process, not calendar promises)

- After every N Released adventures (project chooses N), review QA false negatives and promote Wave checks.  
- Engine minor versions batch multiple justified RFCs — avoid one-line thrash.

### 7.5 Roles summary

| Actor | Owns |
|---|---|
| **Human** | Brief approval; playtest; classification; engine RFC approval; release |
| **AI** | Draft brief/content; Tier B QA; draft reports; implement fixes under direction |
| **Script** | Hygiene; Tier A QA; packaging; estimate formula checks |

---

## 8. Quick reference — common mistakes prevented

| Common mistake | Workflow control |
|---|---|
| Modify engine because of one bad adventure | §4.3 Engine Change Protocol |
| Modify adventure only when engine formula is wrong | Classification tests §4.2 → Engine |
| Accept after technical validation only | Stage 3 insufficient; Stage 4+5 required |
| Endless redesign loops | §7.2 loop caps |
| Overfit engine to one playtest | §7.3 anti-overfit; fixtures ≠ identity |
| Playtest before QA | Stage 4 exit required |
| Fix without classification | Stages 7–8 mandatory |
| Ship with open Critical QA | Release Policy §6 |

---

## 9. Relationship to existing docs

| Document | Role in lifecycle |
|---|---|
| `IDNE_DESIGN_PHILOSOPHY.md` | Identity constraints on Brief, Engine RFC, and QA |
| `IDNE_ENGINE_v0.4.md` | Rules generation must obey; Ready gates |
| `IDNE_ADVENTURE_QA_SPEC.md` | Stage 4 definition |
| `ADVENTURE_QA_REPORT_TEMPLATE.md` | Stage 4 / 10 artifact |
| Adventure Brief template / `ADVENTURE_BRIEF.md` | Stage 1 artifact |
| This workflow | **Authoritative lifecycle** connecting them |

Conflicts: Philosophy > Engine > this workflow’s process rules for *when* to edit; this workflow is authoritative for *process*. QA spec is authoritative for Pre-Playtest Ready criteria.

---

## 10. One-page creed

1. Brief before generation.  
2. Logic before PLAYER.  
3. Hygiene then Adventure QA then playtest — never skip QA.  
4. Classify before you fix.  
5. One finding, one primary layer.  
6. Engine changes are rare, versioned, and multi-adventure justified.  
7. Regress QA before you re-playtest; re-playtest before you release when feel changed.  
8. Improve the generator and QA from repeats; don’t overfit the engine to one case.

---

*End of IDNE Development Workflow — official development lifecycle.*

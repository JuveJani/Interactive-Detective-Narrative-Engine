# CHANGELOG — IDNE Engine Version 0.4

**Document:** First draft engine rewrite  
**Normative output:** `IDNE_ENGINE_v0.4.md`  
**Sources:** `IDNE_DESIGN_PHILOSOPHY.md`, `ENGINE_REFACTORING_PLAN.md`, Engine 2.0 draft (`engine/01`–`06`), playtest-driven findings  
**Scope:** Engine specification only — adventures not upgraded in this change

---

## Summary

Version 0.4 shifts IDNE from a **gamebook-production engine** to a **Dungeon Master–style fair mystery simulation engine** with print/digital delivery as an adapter.

All P0 refactors from the Refactoring Plan are applied. Supporting P1 items are included where required for architectural coherence (shared/split targets, record-sheet visibility, time teeth, split balance, clue discovery modes, ending communication, diegetic choices).

---

## Breaking changes

| Change | Motivation |
|---|---|
| Global engine identity is DM simulation, not gamebook | Philosophy A6; Refactor C-07 |
| Structural PASS is no longer sufficient for Ready | Refactor C-02; playtest false confidence |
| Decision units may not contain consequence text | Refactor C-03; playtest CRITICAL |
| “Recommended” / steering language forbidden | Refactor C-04; Philosophy A10 |
| Playtime estimates must use wall-clock max formula | Refactor C-05 |
| Player conditionals must be sheet-visible | Refactor C-06; Philosophy + playtest undefined trust |
| Compiler repositioned as Delivery Adapter | Refactor C-07; Philosophy A6 |
| Pre-0.4 adventures are prototype-era unless upgraded | Refactor N-06 / Plan §16 |

---

## Significant modifications

### 1. Philosophy made normative (C-01)

**Was (2.0):** Engine opened as “fair-play interactive detective **gamebooks**” (`engine/01` §1.1; `00` §1).

**Now (0.4):** §0 Identity defines DM-simulated fair mystery; `IDNE_DESIGN_PHILOSOPHY.md` Category A is normative; philosophy wins conflicts.

**Why:** Refactoring Plan C-01; Philosophy document as source of truth.

---

### 2. Immutable principles table (U1–U12)

**Was:** Principles scattered across `engine/02` without a locked immutable set tied to playtest philosophy.

**Now:** §1 lists U1–U12 including equal suspect weight, no coaching, realism over drama, DM identity.

**Why:** Plan §2 “things that must never change”; Philosophy A2–A4, A10–A11.

---

### 3. Discovery / connection and clue modes (M-05, Philosophy A1/A8)

**Was:** Clue redundancy (`00` §3.6; `06` §5) without acquisition-mode doctrine; auto-grants unconstrained.

**Now:** §2.2 defines Observe / Earn / Infer / Auto; final conclusion path MUST include an Infer step; auto-delivery of conclusions discouraged.

**Why:** Playtest — mystery worked but clues were handed; Philosophy A1, A8; Plan M-05.

---

### 4. Suspect presentation (M-08, Philosophy A2–A3)

**Was:** No equal-weight intro rule; nervous innocents not framed as intentional feature.

**Now:** §2.4 equal narrative weight; suspicious innocents encouraged when credible.

**Why:** Playtest tone leak; Philosophy A2–A3; Plan M-08.

---

### 5. Architecture: Delivery Adapter (C-07)

**Was:** Narrative Compiler as central product layer producing Public Static Nodes as engine identity (`03` §3.6–3.7).

**Now:** §3.3 Delivery Adapter translates simulation into artifacts; Public Static Nodes remain a valid **form**, not identity.

**Why:** Philosophy A6; Plan C-07; playtest felt like page navigation.

**Preserved:** Layered ownership, single source of truth, hidden internal IDs, formatter boundaries.

---

### 6. Player-visible mechanics / record sheet (C-06, M-02)

**Was:** Public conditions and sheet budget existed (`04` §4, §7; `02` §2.9–2.10) but PLAYER practice referenced undefined trust.

**Now:** §4.3 hard MUST — every player conditional maps to sheet/tag; hidden vars stay internal.

**Why:** Playtest undefined “if trusts you”; Plan C-06, M-02.

---

### 7. Time as scarcity with teeth (M-03, Philosophy A7)

**Was:** Shared clock + sync windows (`00` §3.1; `05`); leftover-time rules; adventure-scoped MBD-04 conflict with `05` §2.

**Now:** §5 scarcity-first; thresholds MUST gate visible options; parallel advance uses **max** of role elapsed at sync; no invented PLAYER clock values.

**Why:** Playtest inert checkpoints and 00:20 inconsistency; Philosophy A7; Plan M-03, C-05 dependency.

**Removed/demoted:** Treating sync leftover micro-rules as the primary design center; flavour-only clocks.

---

### 8. Wall-clock playtime formula (C-05)

**Was:** Prototype budget “90–150 minutes” (`06` §4) without defining wall-clock vs summed roles.

**Now:** §5.4 explicit formula: joint + Σ max(parallel roles); longest branch separate; MUST NOT sum both players.

**Why:** Playtest ~70 vs inflated estimate; Plan C-05.

---

### 9. Shared investigation target (M-01, Philosophy A9)

**Was:** Two-player sync without shared/split ratio (`05`); prototype “≤3 split windows” only.

**Now:** §6.3 SHOULD ≥40% clue-granting units Joint; MUST NOT be two solo novels.

**Why:** Playtest “almost entirely split”; Philosophy A9; Plan M-01.

---

### 10. Split balance gate (M-04)

**Was:** Participation audit informational; wait-until-done without hard delta (`05`; MBD-03).

**Now:** §6.4 ≤5 minute wall-clock delta target; idle wait without options is a defect when exceeded.

**Why:** Playtest first-split ~10 min wait; Plan M-04.

---

### 11. Decision isolation (C-03)

**Was:** Player material MUST NOT contain “unrevealed consequences” (`01` §1.6) but no hard same-unit isolation rule.

**Now:** §7.2 decision units = actions + destinations only; consequences only in destinations.

**Why:** Playtest CRITICAL spoiler-in-choice; Plan C-03.

---

### 12. Diegetic choices (M-06, Philosophy A5)

**Was:** Choices could be graph navigation in practice.

**Now:** §7.1 actions in-world; page codes not the choice text.

**Why:** Playtest “Go to S-210”; Philosophy A5; Plan M-06.

---

### 13. No steering (C-04, Philosophy A10)

**Was:** No ban on “recommended” labels.

**Now:** §7.3 MUST NOT recommend/prefer/suggest choices.

**Why:** Playtest forbidden steering; Plan C-04.

---

### 14. Ending communication (M-07)

**Was:** Terminal types and ending reachability; player ending selection underspecified.

**Now:** §8.3 sheet-checkable resolution, priority order, cite satisfied conditions; no hidden “were you right?”.

**Why:** Playtest ending disconnect; Plan M-07.

**Preserved:** Terminal vs intermediate classification; fair endings; logic owns triggers.

---

### 15. Readiness redefined (C-02)

**Was:** Prototype success criteria mixed structural and playtest (`06` §8); practice treated structural PASS as ready.

**Now:** §13 hygiene necessary but insufficient; experience gates + human playtest required for Ready.

**Why:** False PASS vs playtest failure; Plan C-02.

---

### 16. Language accessibility (N-01, partial)

**Was:** “Clear, adult, genre-literate” without accessibility MUST.

**Now:** §10.4 SHOULD clear/accessible; MUST explain required technical terms in plain language.

**Why:** Playtest language difficulty; Plan N-01 (supporting).

---

## Removed or demoted

| Item | Treatment | Why |
|---|---|---|
| Gamebook as primary identity language | Removed from purpose statements | Philosophy A6 |
| Compiler as investigation designer | Demoted to Delivery Adapter | C-07 |
| Structural PASS = Ready | Removed | C-02 |
| Consequence tables on decision pages | Forbidden | C-03 |
| Recommended choice labels | Forbidden | C-04 |
| Summing both players for playtime | Forbidden | C-05 |
| Undefined player trust conditionals | Forbidden | C-06 |
| Adventure-specific Last Witness profile inside global engine (`05` §10) | Removed from global 0.4 text | Engine MUST NOT contain adventure-specific plot/profile as global law (`00` §2) |
| Solo mode as required for prototype success | Deferred (0.4 focus two-player; Solo OPTIONAL) | Plan postpone; Philosophy open question |
| D20 as engine mandate | Demoted to Category B optional checks | Philosophy Category B; Plan keep resolution optional |

---

## Preserved from Engine 2.0 (still supports philosophy)

| Preserved concept | 0.4 location | Why kept |
|---|---|---|
| Fixed objective truth | §1 U1, §2 | Philosophy A12; U1 |
| Knowledge ≠ truth | §1 U2, §4 | Philosophy A12 |
| Narrator honesty | §1 U4 | U4 |
| World continues independently | §1 U5, §9 | Philosophy A13 |
| Causal state changes | §1 U6, §4.2 | U6 |
| Failure changes path / soft-lock prevention | §1 U7, §2.3 | Philosophy A14 |
| Fair play boundaries | §2.1 | Philosophy A11 |
| Clue redundancy minima | §2.3 | Soft-lock intent |
| Layered architecture & single source | §3 | U12 |
| Hidden internal IDs | §3.5, §10 | Spoiler safety |
| One authoritative clock | §5.1 | Time coherence |
| Joint / Split modes & knowledge isolation | §6 | Two-player cooperation |
| Sync without free drift | §6.7 | Temporal consistency |
| Public condition tags | §4.3, §10.2 | Play-time transparency |
| Compile-time vs play-time | §10.1 | `04` separation |
| Terminal classification | §8.1 | Graph integrity |
| Off-screen predefined events | §9 | World simulation |
| Optional real-time disable | §5.5 | Accessibility |
| Two-player equality | §6.1 | Philosophy A9 / `02` §2.13 |
| Physical play without mandatory digital | §0.3 | `01` §1.7 |
| Deferred heavy tooling | §14 | Plan postpone list |

---

## Mapping: Refactoring Plan → 0.4 sections

| Plan item | Applied in |
|---|---|
| C-01 Philosophy charter | §0, preamble |
| C-02 Ready ≠ structural PASS | §13 |
| C-03 Decision isolation | §7.2 |
| C-04 No steering | §7.3 |
| C-05 Wall-clock estimate | §5.4 |
| C-06 Visible mechanics | §4.3 |
| C-07 Compiler as adapter | §3.3, §10 |
| M-01 Shared/split | §6.3 |
| M-02 Record sheet | §4.3–4.4 |
| M-03 Time teeth | §5.2–5.3 |
| M-04 Split balance | §6.4 |
| M-05 Clue doctrine | §2.2 |
| M-06 Diegetic choices | §7.1 |
| M-07 Ending communication | §8.3 |
| M-08 Tone neutrality | §2.4 |
| N-01 Language | §10.4 |
| N-06 Grandfathering | §16 |

---

## Not done in this draft (intentionally)

Per Refactoring Plan postpone / later waves:

- Executable compiler implementation;
- Rewriting existing adventures to 0.4;
- Solo mode full specification;
- Exact automated linters/CI;
- Digital DM;
- Emotional-stakes guidance beyond creed (N-05 remains optional guidance, lightly reflected in §17).

---

## Migration note for authors

To claim **0.4 Ready**, an adventure must satisfy §13 experience gates and attach a human playtest report. Prototype-era packages may remain in-repo without that claim.

---

*End of CHANGELOG_v0.4.md*

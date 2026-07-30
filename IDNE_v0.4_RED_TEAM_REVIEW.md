# IDNE v0.4 Red Team Review

**Reviewer role:** Senior tabletop RPG / detective game designer (adversarial)  
**Subject:** `IDNE_ENGINE_v0.4.md` (first draft), judged on its own merits  
**Assumption:** This engine will be used to generate **100** detective adventures (often by AI authors)  
**Non-goals:** Comparing to 2.0; inventing new philosophy; rewriting the engine

---

## Verdict in one line

v0.4 states a coherent identity and bans several known failure modes, but it still **under-specifies how a static artifact becomes a DM-simulated investigation**. At mass-generation scale, most adventures will satisfy the letter of the gates while remaining guided menus with checklist endings.

---

## Issues

### RT-01 — DM simulation is declared; play-time is still a static graph walk

| Field | Value |
|---|---|
| **Severity** | **Critical** |
| **Why it matters** | Identity (§0.1, U11) promises players choose what to investigate under a living world. Play-time (§10.1) still reduces to: read unit → choose listed action → go to destination. That is a constrained gamebook with better vocabulary, not a DM. Without an operational model for *open intent* (“I want to search the parking lot” when that unit was not authored), generators will keep shipping closed menus. |
| **Example failure** | Players ask “Can we go back to the loading dock?” The book has no unit. The adventure is “fair” and “Ready,” but agency collapses to the five printed verbs. |
| **Priority** | **P0** — define what “player-directed” means for static delivery (action catalogs, revisit rules, ask-the-world protocol) or stop claiming DM simulation for print-only runs. |

---

### RT-02 — Soft gates (SHOULD + waiver) will be waived into irrelevance

| Field | Value |
|---|---|
| **Severity** | **Critical** |
| **Why it matters** | Shared investigation (§6.3) and split balance (§6.4) are SHOULD, with Ready allowing “approved waiver” (§13.2). Under production pressure, waivers become the default. The hard MUST NOT (“two solo novels”) is too vague to fail a cleverly split design that is *almost* two solos. |
| **Example failure** | 35% Joint clue units, waiver “story requires parallel forensics.” Players again wait and feel like parallel solo games. Adventure marked Ready. |
| **Priority** | **P0** — promote shared/split and balance to MUST, or define non-gameable waiver criteria. |

---

### RT-03 — “Infer step” is trivially gameable

| Field | Value |
|---|---|
| **Severity** | **Critical** |
| **Why it matters** | §2.2 MUST requires one Infer step on a fair path. A single regroup checkbox (“combine C-03 and C-07”) satisfies the rule while 95% of clues remain Auto. Players still collect cards; synthesis is theatrical. |
| **Example failure** | Endgame: “If you hold any two murder clues, tick Established.” That is Infer by paperwork, not detective reasoning. |
| **Priority** | **P0** — require Infer quality constraints (e.g., conclusion not named until player selects among competing theories; or minimum number of non-Auto major clues). |

---

### RT-04 — “Routinely” / “primarily” weasel language

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §2.2: conclusions MUST *primarily* be player-reconstructed; MUST NOT *routinely* auto-deliver guilt narration. AI authors treat soft adverbs as permission. Validators cannot score “routinely.” |
| **Example failure** | Half the scenes end with “It is clear someone staged this.” Author argues it was not “routine.” |
| **Priority** | **P1** — replace with countable limits (max Auto major clues; ban conclusion-language in Observe text). |

---

### RT-05 — Equal suspect weight is untestable

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §2.4 / U9 / Ready gate “equal-weight review” has no operational rubric. Tone leaks (adjective choice, name order, dialogue length, who speaks first) will keep happening. AI is especially bad at this. |
| **Example failure** | Culprit is introduced last, with the longest calm paragraph and a helpful offer of coffee. One player locks on them in minute five. Reviewer shrugs—“felt equal.” |
| **Priority** | **P1** — measurable checks (word budget per suspect in intro; speaking order rotation; ban unique epithets). |

---

### RT-06 — In-world pressure recreates steering

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §7.3 bans meta “recommended” but allows NPC urging and deadline threat. Generators will put the correct next step in an NPC’s mouth (“You really should check the purge logs”). Functionally identical to coaching. |
| **Example failure** | Liaison: “If I were you, I’d start in the SCADA room.” Players obey. Agency illusion. |
| **Priority** | **P1** — constrain authoritative NPCs from naming specific next locations/actions unless that advice is sometimes wrong or costly. |

---

### RT-07 — Decision isolation vs check resolution gap

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §7.2 forbids consequence text on decision units. §7.5 allows checks but never says pass/fail outcomes must be separate units. Generators will keep Choice|Effect tables for rolls. |
| **Example failure** | “Roll Investigation. Success: you find the ledger. Failure: you find a summary.” Same page as the choice to search. |
| **Priority** | **P0** — extend isolation to check outcomes (destination variants or sealed result paragraphs). |

---

### RT-08 — Scarcity without a minimum action space collapses to binary forks

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §5.2 prefers many actions + insufficient time. Print budgets and AI habits produce 2–3 options. Scarcity philosophy then becomes ordinary branching again—only with a clock sticker. |
| **Example failure** | At each hub: Talk / Search / Leave. Time advances. Players never feel a real portfolio of leads. |
| **Priority** | **P1** — require investigation hubs to expose a minimum open lead list (e.g., ≥N available actions or locations) when scarcity is claimed. |

---

### RT-09 — `max()` time advance can punish efficiency and confuse bookkeeping

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §5.3 advances by the slower parallel role. The faster player’s careful short path is absorbed. Also: reading time ≠ world minutes; balance uses “wall-clock engagement estimates” (§6.4) while sync uses world elapsed—two clocks, easy to mis-author. |
| **Example failure** | Field finishes in 8 minutes of reading / 40 world-min. Systems takes 20 minutes reading / 90 world-min. Clock jumps 90. Field feels their choices didn’t matter; estimates still claimed “balanced.” |
| **Priority** | **P1** — clarify relationship of reading-time balance vs world-time advance; give the early finisher meaningful optional actions that still matter. |

---

### RT-10 — “Playable unit” undefined → metric gaming

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §6.3 40% Joint measured by “unit count or declared metric.” Authors can slice Joint into many micro-units or merge Split into few long units to fake the ratio. |
| **Example failure** | One long Split forensics path counts as 1 unit; eight tiny Joint “discuss clue” stubs pad to 40%. |
| **Priority** | **P0** — define unit granularity (or measure by clue-grant weight / estimated minutes, not raw unit count). |

---

### RT-11 — Time teeth can be cosmetic

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §5.2 requires each threshold to change “at least one” visible option. Authors will gate a trivial option (“gift shop closed”) while critical paths stay open. |
| **Example failure** | At 22:00, “vending machine locked.” Murder routes unchanged. Gate passes; tension fake. |
| **Priority** | **P1** — require thresholds to affect a critical or high-value investigation option on standard paths. |

---

### RT-12 — Ending clarity can become a cold checklist

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §8.3 fixes “were you right?” ambiguity by sheet conditions. That can yield bureaucratic endings: tick boxes → epilogue. Players feel audited, not triumphant. Mystery catharsis ≠ form completion. |
| **Example failure** | J-900-style resolver with five AND gates. Correct accusation feels like tax software. |
| **Priority** | **P2** — require ending presentation to narrate the causal chain players proved, not only cite condition IDs. |

---

### RT-13 — Cooperation ≠ information swap

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | Engine pushes Joint clue-granting (§6.3) but never requires joint *reasoning* moments. Two players can still gather separately and dump cards at regroup—same failure mode as the playtest, with more Joint “be in a room together.” |
| **Example failure** | Joint scene: both present while one player reads a terminal aloud. Shared location, solo cognition. |
| **Priority** | **P1** — require at least one structured joint inference / contradiction-resolution beat per adventure. |

---

### RT-14 — Human playtest gate cannot scale to 100 adventures

| Field | Value |
|---|---|
| **Severity** | **Critical** (for mass generation) |
| **Why it matters** | §13.2 requires a recorded human playtest for Ready. If the pipeline generates 100 adventures, either (a) most skip the gate, or (b) playtests become rubber stamps. Either way Ready becomes meaningless again. |
| **Example failure** | Studio ships 80 AI adventures “Ready” with 15-minute skim playtests that never hit split wait or ending confusion. |
| **Priority** | **P0** — define tiered Ready (prototype / limited / full) and sampling rules for batch generation; or accept that AI mass-gen without humans is out of scope. |

---

### RT-15 — No operational model for AI-authored consistency

| Field | Value |
|---|---|
| **Severity** | **Critical** |
| **Why it matters** | U8/U9, Infer quality, believable behaviour, and anti-steering require judgment. LLMs fail these silently. The engine has almost no machine-checkable proxies beyond keyword bans. |
| **Example failure** | Generator produces equal *word count* per suspect but makes the culprit the only one who “smiles too calmly.” Humans catch it in playtest #1 of 100; the other 99 ship. |
| **Priority** | **P0** — add deterministic authoring constraints AI can follow (budgets, banned patterns, required wrong-advice NPCs, Infer templates). |

---

### RT-16 — Replayability is effectively unspecified

| Field | Value |
|---|---|
| **Severity** | **Minor** |
| **Why it matters** | Fixed truth (U1) plus reconverging scarcity menus yields one satisfying playthrough and a hollow second. Not fatal for one-shots; bad if marketed as replayable. |
| **Example failure** | Second run: players rush known critical path; scarcity never bites; endings feel predetermined. |
| **Priority** | **P3** — either claim one-shot focus explicitly or require at least two meaningfully different satisfying routes. |

---

### RT-17 — Destination metadata can still telegraph importance

| Field | Value |
|---|---|
| **Severity** | **Minor** |
| **Why it matters** | §7.1 allows codes after labels. Longer destination sections, booklet placement, or “talk to X → deep interview / talk to Y → three lines” leak salience. |
| **Example failure** | Culprit interview is a full page; red herring is a stub. Players notice. |
| **Priority** | **P2** — length parity guidelines for early interviews; delay depth until earned. |

---

### RT-18 — Sheet budget vs simulation ambition

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | §4.1 demands rich state; §4.4 demands one shared + one private sheet. Authors will oversimplify trust/time/access until “time teeth” and visible mechanics are thin. Or they overflow the sheet and break usability. |
| **Example failure** | Trust, three awareness tracks, four location states, eight ending flags—unplayable bookkeeping—or all compiled away so nothing feels reactive. |
| **Priority** | **P1** — cap *public* tracks with a hard MUST number; define which simulation stays purely internal. |

---

### RT-19 — Fair-failure / degraded outcomes can be miserable without labeling

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | U7 and §2.3 allow degraded solvable outcomes and intentional failure endings. Generators will call a nearly impossible path “degraded but solvable.” Players feel cheated, not challenged. |
| **Example failure** | Miss one early scene → only path left is a Hard check with 15% success and a bleak ending otherwise. Technically fair; experientially hostile. |
| **Priority** | **P1** — define minimum remaining route quality (time cost band, check difficulty band) for “still solvable.” |

---

### RT-20 — Dual normative documents create conflict fog

| Field | Value |
|---|---|
| **Severity** | **Minor** |
| **Why it matters** | Philosophy wins over engine (§0 preamble; §0.4). Authors/AI must reconcile two texts. Subtle mismatches (creed vs MUST tables; SHOULD ratios) produce inconsistent adventures. |
| **Example failure** | Generator follows creed slogan, ignores §6.3 metric, claims philosophy compliance. |
| **Priority** | **P2** — single normative engine file with philosophy inlined or strictly subordinated. |

---

### RT-21 — Solo is named in use case but deferred in practice

| Field | Value |
|---|---|
| **Severity** | **Minor** |
| **Why it matters** | §0.3 allows one player; §14 defers solo. Half of tabletop demand may be solo. Generators will emit broken solo ports of two-player scarcity designs. |
| **Example failure** | Solo player told to “wait for partner” at sync. |
| **Priority** | **P2** — either forbid solo claims in 0.4 or ship a minimal solo sync rule now. |

---

### RT-22 — No stakes / investment requirement

| Field | Value |
|---|---|
| **Severity** | **Major** |
| **Why it matters** | A fair, balanced, non-steering mystery can still feel like paperwork. Playtest already showed low emotional engagement. v0.4 gates fairness and process, not *why the player cares before the deadline*. |
| **Example failure** | Perfect Infer chain, equal suspects, good scarcity—victim is a stranger, institution is abstract, ending is a form. Players finish to finish. |
| **Priority** | **P1** — without new philosophy: require visible personal/institutional stakes that change if the clock expires (already compatible with A7/A17). |

---

## Cross-cutting failure modes (100-adventure lens)

| Failure mode | How v0.4 still allows it |
|---|---|
| Guided tourism | Soft shared gates; NPC steering; small action menus |
| Collectathon | Gameable Infer; Auto clues unconstrained by counts |
| Split boredom | SHOULD balance + vague MUST NOT |
| False Ready | Waivers + skim playtests at scale |
| Tone-leak culprit | Untestable equal-weight |
| Checklist ending | Sheet-only resolution without catharsis requirement |
| Fake DM promise | Static graph walk unchanged |

---

## What v0.4 already does well (credit where due)

- Clear ban on meta recommended choices.  
- Decision isolation stated as MUST (even if checks underspecified).  
- Wall-clock estimate formula (max, not sum).  
- Player-visible conditionals requirement.  
- Explicit rejection of structural-only PASS.  
- Identity statement is coherent even if delivery cannot fully realize it yet.

These reduce *some* known disasters. They do not yet make satisfying detective play the default output of generation.

---

## Final estimate

### If this engine generated 100 adventures today, what percentage would likely provide a genuinely satisfying detective experience?

**Estimate: 15–25%.**

**Point estimate used for planning: ~20%.**

### Justification (not optimism)

| Band | Approx. share | Rationale |
|---|---:|---|
| Structurally “compliant” on paper | 60–80% | Keyword bans and hygiene are easy for AI; waivers absorb hard SHOULDs |
| Survives a real two-player playtest without major pacing/agency complaints | 25–35% | Balance, tone, and menu-size failures remain common |
| Feels like *detecting* (inference, investment, earned ending)—not collecting | **15–25%** | Infer is gameable; stakes ungated; DM promise unmet in static form |
| Excellent / memorable | &lt;10% | Requires authorial taste v0.4 cannot encode |

Assumptions baked into the estimate:

1. Most adventures are AI-assisted or AI-first.  
2. Human playtesting is scarce relative to 100 titles.  
3. Print/static delivery dominates (no live DM).  
4. “Satisfying” means: fair mystery, felt agency, cooperation without long idle, earned conclusion, emotional reason to care—not merely “we finished and the rules didn’t crash.”

If every adventure had a rigorous human playtest *and* no waivers on §6.3–6.4, the satisfying band might rise toward **35–45%**—still not a majority, because RT-01, RT-03, RT-05, and RT-22 remain.

---

## Recommended fix order (for the IDNE team; not redesign here)

1. **P0:** RT-01, RT-02, RT-03, RT-07, RT-10, RT-14, RT-15  
2. **P1:** RT-04, RT-05, RT-06, RT-08, RT-09, RT-11, RT-13, RT-18, RT-19, RT-22  
3. **P2–P3:** RT-12, RT-16, RT-17, RT-20, RT-21  

---

*End of red team review. No engine text was modified by this document’s recommendations beyond filing the review itself.*

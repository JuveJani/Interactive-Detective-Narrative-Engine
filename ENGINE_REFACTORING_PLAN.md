# IDNE Engine Refactoring Plan — Version 0.4

**Status:** Planning document only  
**Role:** Lead architect roadmap  
**Not in scope:** Writing new engine rules, redesigning systems, modifying adventures, implementing fixes  
**Inputs:** Current `engine/` (2.0), `IDNE_DESIGN_PHILOSOPHY.md`, playtest-driven root-cause findings, compliance audit findings  
**Target:** Organize work for **Version 0.4 Ready**

---

## 1. Executive Summary

Version 0.4 is the first engine release that aligns **documented identity** (DM-simulated fair mystery) with **authoring and validation gates** that prevent shipping tour-style gamebooks that pass paper checks and fail human play.

The current engine (2.0 chapters `01`–`06` plus companion specs) already contains durable foundations: fixed objective truth, knowledge separation, fair play, compile-time vs play-time, two-player sync concepts, and layered architecture. Those foundations **remain**.

What must change is the **center of gravity**: from graph/gamebook completeness toward **world simulation, player-directed investigation, scarcity-driven decisions, and experience-level validation**.

| Keep | Change | Remove / demote | Rewrite | Postpone |
|---|---|---|---|---|
| Fair play, fixed truth, knowledge ≠ truth | Philosophy-first identity in engine index | Structural-only PASS as release gate | Player-facing decision / consequence model | Full digital DM runtime |
| Layered pipeline concept | Playtime, balance, shared/split gates | Recommended-choice language | Time as scarcity (felt options) | Solo mode completion |
| Soft-lock prevention intent | Clue discovery vs auto-delivery norms | Page-code-as-choice as acceptable form | Ending communication / evaluator binding | Campaign / multi-case |
| Two-player cooperation intent | Validation against playtest metrics | Wait-as-content without balance gate | Narrative compiler contract vs DM vision | Full JSON Schema / CI |

**Version 0.4 success condition:** An adventure cannot be declared ready unless it satisfies philosophy-aligned gates *and* a recorded human playtest against those gates — not file inventory alone.

---

## 2. Things that must never change

These are locked for Version 0.4 planning (Category A identity + proven engine cores).

| ID | Immutable principle | Source |
|---|---|---|
| U1 | Objective truth is fixed; play does not rewrite history | Philosophy A1/A12; `engine/02` §2.1 |
| U2 | Knowledge is separate from truth (players/NPCs may be wrong) | Philosophy A12; `engine/02` §2.2 |
| U3 | Fair play: solution must be derivable from obtainable information | Philosophy A11; `engine/01` |
| U4 | Narrator does not lie about sensory facts | `engine/02` §2.3 |
| U5 | World can continue while players are elsewhere | Philosophy A13; `engine/02` §2.4 |
| U6 | Meaningful change requires a traceable cause | `engine/02` §2.5 |
| U7 | Failure should change path, not silently erase the only fair solution | Philosophy A14; `engine/02` §2.7 |
| U8 | Suspicious innocents and believable behaviour are valid | Philosophy A3–A4 |
| U9 | Equal narrative weight for suspects (no tone leaks) | Philosophy A2 |
| U10 | Players investigate; engine does not coach the “right” move | Philosophy A5, A10 |
| U11 | Long-term identity is DM simulation, not branching novel | Philosophy A6 |
| U12 | Layered ownership: World Bible / Logic / Compiler / Formatter remain separated in concept | `engine/03` |

**Do not reopen in 0.4:** genre as supernatural-default, random rewriting of case truth, or abandoning fair-play solvability.

---

## 3. Critical refactors (P0)

Work without which Version 0.4 cannot claim identity alignment.

### C-01 — Adopt philosophy as normative engine preface

| Field | Value |
|---|---|
| **Group** | Engine philosophy |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Engine chapters predate `IDNE_DESIGN_PHILOSOPHY.md`; practice drifted into gamebook completeness |
| **Dependencies** | None (philosophy doc already exists) |
| **Impact** | Medium (docs), High (downstream gates) |
| **Risk to existing adventures** | Low if framed as version bump; High if applied retrospectively without grandfathering |
| **Plan (organize only)** | Bind philosophy into engine index / 0.4 charter; mark contradictions with current chapters for later rewrite queues |

---

### C-02 — Redefine “ready” away from structural PASS

| Field | Value |
|---|---|
| **Group** | Validation |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Structural validators and design-package PASS enabled false confidence; playtest failed |
| **Dependencies** | C-01 (know what “ready” means) |
| **Impact** | High |
| **Risk** | High for currently “PASS” packages (Glass Alibi, Last Witness claims) |
| **Plan** | Specify experience gates (wall-clock, wait, shared ratio, isolation, no steering) as release blockers; demote file-count checks to hygiene only |

---

### C-03 — Decision isolation as hard authoring contract

| Field | Value |
|---|---|
| **Group** | Narrative compilation / Player package |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Choice scenes revealed consequences in-place (playtest CRITICAL) |
| **Dependencies** | C-01 |
| **Impact** | High on PLAYER authoring and compiler Stage 3/6 |
| **Risk** | High — all current PLAYER choice tables need later rewrite |
| **Plan** | Queue contract: decision units list only actions + destinations; consequences only in destination units. Do not draft the wording here |

---

### C-04 — Ban meta-steering (“recommended” choices)

| Field | Value |
|---|---|
| **Group** | Adventure generation / Player package |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Playtest: recommended options forbade agency |
| **Dependencies** | C-01 |
| **Impact** | Low–Medium |
| **Risk** | Low |
| **Plan** | Add to 0.4 forbidden-authoring list; validation grep scheduled after C-02 |

---

### C-05 — Wall-clock playtime model (max, not sum)

| Field | Value |
|---|---|
| **Group** | Time system / Validation / Two-player |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Estimates summed roles; real play ~70 vs 90–150 claimed |
| **Dependencies** | Clarified split timing model (see M-03) |
| **Impact** | Medium |
| **Risk** | Low for logic; Medium for briefs/reports |
| **Plan** | Define estimate formula as wall-clock = joint + Σ max(parallel roles); longest-branch reported separately |

---

### C-06 — Player-visible mechanics only

| Field | Value |
|---|---|
| **Group** | State system / Player package |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Trust/conditions referenced without case-file definitions |
| **Dependencies** | C-01; record-sheet contract (M-02) |
| **Impact** | High |
| **Risk** | High — logic trust scalars vs sheet exposure must be reconciled later |
| **Plan** | Mandate: every PLAYER conditional maps to an exposed tracker or public condition tag; hidden vars stay compiler-internal |

---

### C-07 — Reposition compiler relative to DM vision

| Field | Value |
|---|---|
| **Group** | Narrative compilation |
| **Severity** | Critical |
| **Priority** | P0 |
| **Issue** | Compiler/gamebook pipeline dominated identity; play felt like page navigation |
| **Dependencies** | C-01 |
| **Impact** | High |
| **Risk** | High for `BOOK_COMPILER_SPEC` / `CONTENT_GENERATION_SPEC` |
| **Plan** | Charter 0.4: compiler is a **delivery adapter** for simulated world actions, not the source of investigation shape. Schedule rewrite of compiler goals without implementing them yet |

---

## 4. Major refactors (P1)

### M-01 — Shared vs split cooperation targets

| Field | Value |
|---|---|
| **Group** | Two-player / Adventure generation |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Play felt almost entirely split; philosophy A9 |
| **Dependencies** | C-01, C-02 |
| **Impact** | High on adventure graphs |
| **Risk** | High for Glass Alibi–style graphs |
| **Plan** | Define target bands for shared investigation (clue-granting Joint share); keep exact % as later rule text |

---

### M-02 — Record sheet / public condition contract

| Field | Value |
|---|---|
| **Group** | State system / Player package |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | `engine/04` §7 sheet limit vs undeclared fields; playtest undefined mechanics |
| **Dependencies** | C-06 |
| **Impact** | High |
| **Risk** | Medium–High |
| **Plan** | Inventory allowed player-visible state classes; map logic variables to sheet or forbid PLAYER mention |

---

### M-03 — Time as scarcity with teeth

| Field | Value |
|---|---|
| **Group** | Time system |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Clock flavour without felt option change; invented thresholds in PLAYER; engine/05 vs MBD-04 tension |
| **Dependencies** | C-05 |
| **Impact** | High |
| **Risk** | High |
| **Plan** | Reconcile sync-point vs per-action clock models; require each declared threshold to gate at least one option; forbid undeclared times in PLAYER |

---

### M-04 — Split balance / anti-idle gate

| Field | Value |
|---|---|
| **Group** | Two-player / Validation |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | First split ~10 min wait; MBD-03 wait became content |
| **Dependencies** | C-05 |
| **Impact** | Medium |
| **Risk** | Medium |
| **Plan** | Define max wall-clock delta per split window; waiting without alternate actions fails readiness |

---

### M-05 — Clue acquisition doctrine (discovery + connection)

| Field | Value |
|---|---|
| **Group** | Clue system / Adventure generation |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Auto-grants; little reasoning; philosophy A1/A8 |
| **Dependencies** | C-01, C-02 |
| **Impact** | High |
| **Risk** | High for clue graphs designed as location dumps |
| **Plan** | Classify acquisition modes (observe / earn / infer / auto); set caps or requirements for inference steps before conclusions |

---

### M-06 — Choice form: diegetic intent, not page codes

| Field | Value |
|---|---|
| **Group** | Narrative compilation / Player package |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | “Go to S-210” decisions |
| **Dependencies** | C-03, C-07 |
| **Impact** | Medium–High |
| **Risk** | Medium |
| **Plan** | Authoring contract: action labels in-world; destinations as navigation metadata only |

---

### M-07 — Ending resolution communication

| Field | Value |
|---|---|
| **Group** | Ending system / Player package |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Ending felt disconnected; PLAYER honor-system ≠ logic evaluators |
| **Dependencies** | M-02, C-06 |
| **Impact** | High |
| **Risk** | Medium–High |
| **Plan** | Plan binding of ending selection to player-checkable conditions that mirror evaluators; ending text cites satisfied conditions |

---

### M-08 — Suspect introduction / tone neutrality gate

| Field | Value |
|---|---|
| **Group** | Adventure generation / Narrative compilation |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Early suspect from intro wording |
| **Dependencies** | C-01 |
| **Impact** | Medium |
| **Risk** | Low–Medium |
| **Plan** | Authoring review checklist for equal weight; optional lint for spotlight language later |

---

### M-09 — Demote gamebook-first README chapter list conflict

| Field | Value |
|---|---|
| **Group** | Engine philosophy / Architecture |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | `engine/README.md` planned chapters still novel/gamebook-centric; incomplete vs 2.0 reality |
| **Dependencies** | C-01, C-07 |
| **Impact** | Medium |
| **Risk** | Low |
| **Plan** | Reorder planned chapters around simulation (world, actions, scarcity, knowledge) with delivery adapters last |

---

### M-10 — Adventure generation brief for 0.4

| Field | Value |
|---|---|
| **Group** | Adventure generation |
| **Severity** | Major |
| **Priority** | P1 |
| **Issue** | Generators optimized for logic completeness |
| **Dependencies** | C-01–C-07, M-01, M-05 |
| **Impact** | High |
| **Risk** | High for automated generation prompts |
| **Plan** | New generation checklist ordered by philosophy; postpone rewriting Glass Alibi until gates exist |

---

## 5. Minor improvements (P2–P3)

### N-01 — Plain-language / reading-level guidance

| Field | Value |
|---|---|
| **Group** | Narrative compilation |
| **Severity** | Minor |
| **Priority** | P2 |
| **Dependencies** | C-01 |
| **Impact** | Medium (player experience) |
| **Risk** | Low |
| **Plan** | Add language guidance to authoring norms; not a full style engine |

---

### N-02 — Fake-choice detection

| Field | Value |
|---|---|
| **Group** | Validation / Decisions |
| **Severity** | Minor |
| **Priority** | P2 |
| **Dependencies** | C-03 |
| **Impact** | Medium |
| **Risk** | Low |
| **Plan** | Flag decisions with identical destinations and costs |

---

### N-03 — Graph impact metrics (linearity detectors)

| Field | Value |
|---|---|
| **Group** | Validation / Adventure generation |
| **Severity** | Minor |
| **Priority** | P2 |
| **Dependencies** | C-02 |
| **Impact** | Medium |
| **Risk** | Low |
| **Plan** | Measure mid-chain branch rate and permanent divergence; informational then gating |

---

### N-04 — Reconcile companion specs supersession

| Field | Value |
|---|---|
| **Group** | Validation / Architecture |
| **Severity** | Minor |
| **Priority** | P2 |
| **Dependencies** | C-07 |
| **Impact** | Medium |
| **Risk** | Medium (doc churn) |
| **Plan** | Mark which of `BOOK_COMPILER_SPEC` / `CONTENT_GENERATION_SPEC` / Milestone B docs are normative for 0.4 vs historical |

---

### N-05 — Emotional stakes guidance (non-twist)

| Field | Value |
|---|---|
| **Group** | Adventure generation |
| **Severity** | Minor |
| **Priority** | P3 |
| **Dependencies** | C-01 |
| **Impact** | Low–Medium |
| **Risk** | Low |
| **Plan** | Guidance that investment comes from stakes/deadline/people, not mandatory twist count |

---

### N-06 — Grandfathering policy for pre-0.4 adventures

| Field | Value |
|---|---|
| **Group** | Validation |
| **Severity** | Minor |
| **Priority** | P2 |
| **Dependencies** | C-02 |
| **Impact** | Low |
| **Risk** | Low if explicit |
| **Plan** | Label Last Witness / Glass Alibi as prototype-era; 0.4 gates apply to new work unless upgraded |

---

## 6. Dependency graph

```text
C-01 Philosophy charter
   ├── C-02 Ready ≠ structural PASS
   │      ├── M-01 Shared/split targets
   │      ├── M-05 Clue doctrine
   │      ├── M-10 Generation brief
   │      ├── N-03 Linearity metrics
   │      └── N-06 Grandfathering
   ├── C-03 Decision isolation ── M-06 Diegetic choices ── N-02 Fake-choice
   ├── C-04 No steering
   ├── C-05 Wall-clock estimate ── M-03 Time teeth
   │                         └── M-04 Split balance
   ├── C-06 Visible mechanics ── M-02 Record sheet ── M-07 Ending communication
   ├── C-07 Compiler as adapter ── M-09 Chapter roadmap ── N-04 Spec supersession
   ├── M-08 Tone neutrality
   └── N-01 / N-05 Language & stakes guidance
```

**Critical path:** C-01 → C-02 → (M-01, M-05, M-03) → M-10 → human playtest gate definition → **0.4 Ready**.

---

## 7. Suggested implementation order

### Wave 0 — Charter (no adventure edits)

1. C-01 Philosophy normative for 0.4  
2. C-07 Compiler role reframed in charter  
3. C-02 Ready criteria draft (experience gates listed, not coded)

### Wave 1 — Hard authoring bans

4. C-03 Decision isolation contract  
5. C-04 No steering  
6. C-06 Visible mechanics  
7. C-05 Wall-clock formula  

### Wave 2 — Systems alignment

8. M-02 Record sheet contract  
9. M-03 Time scarcity reconciliation  
10. M-04 Split balance gate  
11. M-01 Shared/split targets  
12. M-05 Clue discovery doctrine  
13. M-07 Ending communication binding  

### Wave 3 — Generation & delivery

14. M-06 Diegetic choice form  
15. M-08 Tone neutrality checklist  
16. M-09 Engine README / chapter plan update  
17. M-10 Adventure generation brief rewrite  
18. N-01–N-04 hygiene  

### Wave 4 — Prove 0.4

19. Apply gates to one reference adventure upgrade (chosen later)  
20. Recorded human playtest against 0.4 definition  
21. Freeze Version 0.4 Ready  

**Explicitly out of order for 0.4:** rewriting Glass Alibi for fun; building AI DM; solo mode; full schema CI.

---

## 8. Estimated milestones

Milestones are **work packages**, not calendar estimates.

| Milestone | Contents | Exit criteria |
|---|---|---|
| **M0 — 0.4 Charter** | C-01, C-07 framing, immutable list published | Philosophy cited as normative for 0.4 work |
| **M1 — Authoring Contracts** | C-03, C-04, C-05, C-06 | Written contracts exist; no implementation required yet |
| **M2 — Experience Gates Spec** | C-02 + M-01, M-04, M-05 draft gates | “Ready” checklist no longer equals file PASS |
| **M3 — World Systems Spec Sync** | M-02, M-03, M-07 | Time/state/ending communication contracts consistent |
| **M4 — Delivery Adapter Spec** | M-06, M-09, N-04 | Compiler described as adapter; chapter map updated |
| **M5 — Generation Realignment** | M-08, M-10, N-01, N-05 | New generation brief exists |
| **M6 — Reference Proof** | One adventure upgraded or new 0.4 sample + playtest | Playtest report attached; gates pass or waivers documented |
| **Version 0.4 Ready** | All P0 + agreed P1 closed | See §10 |

**Postpone beyond 0.4 (P3+ backlog):**

- Executable Narrative Compiler / Book Formatter products  
- Live digital DM  
- Solo mode  
- Full JSON Schema + CI  
- Multi-case campaigns  
- Competitive / traitor modes  

---

## 9. Risks

| Risk | Why it matters | Mitigation in plan |
|---|---|---|
| **Identity vs installed base** | Existing adventures “PASS” under old gates | N-06 grandfathering; 0.4 is a version bump |
| **Over-correcting into sandbox chaos** | Open investigation without constraints breaks print prototypes | Keep scarcity (time) as primary constraint; postpone free-text AI DM |
| **Doc sprawl** | Companion specs contradict engine | N-04 supersession pass in Wave 3 |
| **Premature adventure rewrite** | Fixing Glass Alibi before gates wastes work | M-10 after contracts; no adventure redesign in this plan |
| **Compiler paralysis** | Reframing C-07 blocks all output | Treat print adapter as still valid delivery; change *goals*, not delete pipeline |
| **Metric gaming** | New gates become checkbox theatre again | Require human playtest in §10 |
| **Scope creep into “solve playtest”** | Plan turns into redesign | This document forbids solutions; only organizes |

---

## 10. Definition of Version 0.4 Ready

Version 0.4 is **Ready** when all of the following are true:

### Must have (P0)

- [ ] Philosophy document is cited as normative identity for 0.4  
- [ ] Immutable principles (§2) are explicitly adopted  
- [ ] “Ready” is defined by experience gates, not structural file PASS alone  
- [ ] Decision isolation contract written  
- [ ] No-steering contract written  
- [ ] Wall-clock estimate formula written (max, not sum)  
- [ ] Player-visible mechanics contract written  
- [ ] Compiler positioned as delivery adapter under DM vision  

### Should have (P1 agreed set)

- [ ] Shared/split target guidance written  
- [ ] Record-sheet / public condition contract written  
- [ ] Time-scarcity reconciliation plan written (single clock model chosen)  
- [ ] Split balance gate written  
- [ ] Clue discovery/connection doctrine written  
- [ ] Ending communication binding plan written  
- [ ] Adventure generation brief for 0.4 written  

### Proof

- [ ] At least one reference play path evaluated against the new gates  
- [ ] A human playtest report exists for that reference (pass or documented waivers)  
- [ ] Pre-0.4 adventures labeled prototype-era or upgraded  

### Explicitly not required for 0.4 Ready

- Working automated compiler binary  
- Rewritten Glass Alibi PLAYER  
- Solo mode  
- Full schema CI  
- Resolution of every Minor (N-*) item  

---

## Appendix A — Issue → work-item index

| Playtest / audit theme | Work items |
|---|---|
| Playtime estimate wrong | C-05 |
| Too much split | M-01 |
| Split One wait | M-04, C-05 |
| Hard language | N-01 |
| Page-code decisions | M-06, C-03 |
| Undefined trust | C-06, M-02 |
| Consequence spoilers | C-03 |
| Weak agency / auto-clues | M-05 |
| Recommended choices | C-04 |
| Low suspense / investment | N-05 (guidance only) |
| Ending disconnect | M-07 |
| Inert / inconsistent time | M-03 |
| Linear feel vs graph | N-03 |
| Structural false PASS | C-02, N-06 |
| Gamebook identity drift | C-01, C-07, M-09 |
| Tone leak on suspects | M-08 |
| Generation optimizes wrong target | M-10 |

---

## Appendix B — Unchanged technical assets (for continuity)

Keep using until explicitly superseded in later waves:

- Prefix / ownership discipline in adventure logic  
- Soft-lock prevention *intent*  
- Two-player knowledge isolation *intent*  
- Check resolution as *an* implementation option (Category B)  
- Layered World Bible → Logic → Delivery separation  

---

*End of refactoring plan. No engine rules were authored. No systems were redesigned. No repository implementation work is authorized by this document alone.*

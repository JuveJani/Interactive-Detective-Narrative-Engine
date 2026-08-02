# Offline Explainer / Repair Advisor — Independent Review

**Reviewer posture:** adversarial. Do not trust `EXPLAINER_IMPLEMENTATION_REPORT.md`, the 58 passing tests, the readiness verdict, or generated example reports without re-execution.  
**Subject:** PR #23 (`cursor/idne-explainer-bad4`, commit `e0b505d`)  
**Review date:** 2026-08-02  
**Method:** full source re-read of `simulator/`, `idne_sim.py`, tests, prompts, `sim_adapter.json`, prior V1/V2 simulator reviews; independent probes; required CLI re-runs  
**No product code was modified for this review** (review document only).

---

## Executive verdict

PR #23 **does improve** several V2 simulator blockers (deadline halt, Hub-2 revisit return, hub-target keying, trust downgrade of `SIM-FAKE-*`, clock cap, `max_states` / memory guard hooks). The explainer/repair/AI-export CLI path **runs offline** and **does not auto-edit the repository**.

It is **not** ready to treat as a trustworthy offline diagnosis-and-repair system for Harborview quantitative tuning:

1. Keyword phone follow-ups are **dead code** (0 hits across all nodes) while trust text claims “keyword heuristics” partial support.
2. Zero correct endings in a 200-run batch produce **no finding** when trust is already down (`SIM-NO-WIN` gate bug).
3. Reports still publish ending rates / fiction averages in a form humans will read as results; executive “proven” section collapses to empty even for proven trust facts.
4. Ambiguity #5 is still **stale** (`once_per_hub` *is* tracked); trust cites “5 unresolved ambiguities” including that false claim.
5. P-112 still always grants the manager key; incomplete I-02 still retries for **0 minutes**.
6. `repair-plan --finding` **overwrites** the full repair backlog with a single finding’s options.
7. Local AI context for trust findings omits the actual ambiguity list and useful engine excerpts; prompts are helpful but insufficient to stop rate-based “tuning” advice.

**Safe for offline diagnosis:** YES, with caveats (qualitative / trust-gated only).  
**Safe for offline repair planning:** CONDITIONAL — suggestions are generic and non-destructive, but backlog overwrite and overconfident confidence labels create real misuse risk.  
**Safe for quantitative adventure tuning:** **NO**.

---

## Re-execution evidence (this review)

| Command | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | **58 OK** |
| `./run_full_diagnostic.sh 200 42` | **Fails** on Linux with Termux-only shebang (`cannot execute: required file not found`). Succeeds via `bash ./run_full_diagnostic.sh 200 42` |
| Full diagnostic output | `simulation_output/20260802_164414_099731_simulate_0` — 200 runs; E-901:**0**, E-904:163, E-902:19, E-905:18; fiction avg **232.3**; `simulator_trustworthy: false` |
| `bash ./explain_latest.sh SIM-TRUST-DOWNGRADE` | Wrote `explanations/SIM-TRUST-DOWNGRADE.md` |
| `bash ./export_latest_for_ai.sh SIM-TRUST-DOWNGRADE` | Wrote `local_ai_context/finding_context_SIM-TRUST-DOWNGRADE.{md,json}` — no culprit/truth strings |
| `python3 idne_sim.py repair-plan … --finding SIM-FAKE-J-122` | Wrote placeholder `proposed_fix_SIM-FAKE-J-122.{md,patch}`; **adapter hash unchanged**; **backlog reduced to that finding only** |
| Independent interrupt probe | Partial run saved findings + executive diagnostic (`runs: 2`) after `RunInterrupted` |
| Oracle+clue-seeking 100 | E-901:**7**, E-904:69, E-902:24 — win reachable under forced correct accuse, rare |

---

## Checklist verification (1–15)

### 1. Deadline, hub revisit, follow-up, trust-downgrade fixes

| Claim | Verdict | Evidence |
|---|---|---|
| Deadline | **Mostly fixed** | At clock 1380, `hub_options` on J-300 → `[]` then `step` → `J-600:deadline`; `advance_minutes` caps at 1380; fiction max in 50 random runs = **240** |
| Hub-2 revisit | **Fixed** | `stairwell_revisit` → J-110 with `return_hub=J-300` → returns **J-300**; Hub-1 stairwell still → J-120 |
| `hub_targets` collision | **Fixed** | Keys `(1,'J-110')` and `(2,'J-110')` both present |
| Trust downgrade of `SIM-FAKE-*` | **Fixed** | Layers = `UNDETERMINED`, confidence `low` while untrusted |
| Follow-ups | **Partial / misleading** | James `needs_followup` → P-214 **is forced** even when chooser avoids it. Adapter `follow_ups` keyword matcher: **0 hits** on every node (see OE-03) |
| I-02 loop inflation | **Mitigated, not fixed** | Fiction no longer reaches thousands; incomplete I-02 still returns with **0 minute charge**; 35/50 random paths contain `blocked-I-02` |

### 2. Unsupported mechanics prevent trusted quantitative output

**Directionally yes, incompletely.**  
`simulator_trustworthy` is false when `ambiguities[]` or loader-injected `simulator_partial` is non-empty. Adventure-blaming layers downgrade.  

Gaps: ending rates still printed prominently in `summary.md`; `SIM-NO-WIN` suppressed whenever untrusted even if engine prechecks pass (OE-01); stale ambiguity #5 still counted (OE-04); keyword follow-up described as “partial” when it never fires (OE-03).

### 3. Explanations match actual evidence

**Mixed.**  
`SIM-TRUST-DOWNGRADE` evidence string matches trust blockers.  
`SIM-FAKE-*` evidence matches `fake_choice` marking.  
Bottleneck findings: evidence is accurate, but plain-language template falls back to `"The simulator found: …"` with little translation.  
Trust text says “keyword heuristics” — **overstates** what the engine actually does (OE-03).

### 4. Plain-language without engine expertise

**Partial pass.**  
Trust and fake-choice templates are readable. Bottleneck / generic findings still expose raw IDs (`C-06`, `R-112`) without defining them. Abbreviations like E-901 appear in summary without expansion. Executive diagnostic is the best human entry point but currently under-reports proven facts (OE-02).

### 5. Repair options distinguish facts / hypotheses / design choices

**Weak.**  
Options are layer-templated (“Clarify or fix adapter entry for X”, “Run a manual playtest”). They do not label which premises are proven vs design choice. Root-cause fields in explanations are hypotheses but executive “suspected” section mixes them with the proven trust downgrade (OE-02).

### 6. Repair advice inventing story or engine rules

**Mostly avoided.**  
No invented NPC/story facts observed in repair options or AI context for reviewed findings. Engine snippets are short canned strings; trust context only got the fair-play line. Risk is **generic over-advice** (“fix adapter”) rather than invented canon.

### 7. Finding ownership

**Improved for fake-choices; still soft.**  
`SIM-FAKE-*` → `UNDETERMINED` while untrusted (V2-06 addressed).  
Trust finding itself is `UNDETERMINED` (reasonable).  
No `SIM-NO-WIN` / no-win ownership when rates are 0% under trust-down (OE-01).  
Bottlenecks keep **confidence=high** while `trust_affects_conclusion=True` (OE-05).

### 8. Local AI context has all necessary evidence

**No for trust / adapter work.**  
`finding_context_SIM-TRUST-DOWNGRADE.json` lacks: the five ambiguity strings, P-112 node excerpt, follow-up rule text, engine deadline/follow-up rules (only fair-play), and source excerpts.  
`node_excerpt` is `{}` because identifier is `"ambiguities"`. Insufficient to repair without reopening the repo.

### 9. Local AI prompts prevent hallucinated fixes

**Helpful, not sufficient.**  
System prompt forbids inventing engine rules / story and requires approval. It does **not** forbid recommending adventure balance changes from untrusted ending rates, nor require quoting only context-file evidence for quantitative claims. Context packages still embed `ending_distribution` under `simulator_evidence`.

### 10. Spoiler-sensitive data limited

**Mostly yes for filtered export.**  
Trust AI JSON contains no `truth` / culprit strings. `metrics.json` does not embed `adapter_snapshot`.  
Residual: full adventure reload is available to CLI on the device; unfiltered export of many findings still avoids truth, but suspicion names appear in strategies/public suspect lists if those nodes are exported. Acceptable for author tooling; not player-safe if shared carelessly.

### 11. Patch files never applied automatically

**PASS.**  
`write_proposed_patch` writes placeholders only; no `git apply` / file rewrite of adventure or engine. Adapter SHA unchanged after `repair-plan`.

### 12. Termux scripts fully offline

**CONDITIONAL PASS on device; FAIL as portable `./` scripts.**  
Shebang is `/data/data/com.termux/files/usr/bin/bash` only — correct for Pixel Termux, broken elsewhere (including this review host). Scripts call local `python3 idne_sim.py` only (offline). Docs tell users to `chmod +x` and `./` — works on Termux, fails on standard Linux without `bash script`.

### 13. Memory / state guards enforced

**Partially.**  
`SimulationLimitError` on `max_states` per engine run: confirmed.  
`memory_guard_mb` via `ru_maxrss`: confirmed trips at 0.  
Monte Carlo does **not** accumulate states across runs toward `max_states` (each run resets; typical `states_explored≈18`). Guard is per-playthrough, not batch-wide. Default 256 MB is fine for phone; claim of strong batch protection is overstated.

### 14. Interrupted runs preserve usable partial output

**PASS (basic).**  
Forced `RunInterrupted` after 2 runs still wrote findings, metrics (`runs: 2`), and `executive_diagnostic.md`. Log notes interruption. No crash.

### 15. Deterministic reports for same seed

**PASS for analysis/explanation content.**  
Same seed → same endings/fiction; `explain_all` dicts identical across re-runs. Output **folder names** use timestamps (by design).  
Caveat: `repair-plan --finding` mutates shared artifacts non-deterministically relative to prior full backlog (OE-06).

---

## Adapter ambiguities (special attention)

| # | Text | Material? | Status after PR #23 |
|---|---|---|---|
| 1 | J-121 → J-120 or J-130 | Low | Still listed; modeled as `next_options` |
| 2 | P-112 always grants manager key | **Yes** | **Unresolved** — flags still include `ACCESS_MANAGER_KEY` unconditionally |
| 3 | Bakery-closed phone / follow-ups | **Yes** | Gate skip exists; joint keyword follow-ups **never fire** |
| 4 | R-212b fake_choice | Low | Correctly flagged |
| 5 | “once_per_hub not tracked” | **Stale** | **False** — revisit filtered when used; still counted in “5 ambiguities” |

Loader also injects `simulator_partial` at runtime (not written into `sim_adapter.json` on disk). Trust blockers mention P-112 and “keyword heuristics” — the latter is inaccurate (OE-03).

---

## Issue register

### OE-01 — Zero-win silence while untrusted

| Field | Value |
|---|---|
| **Severity** | **critical** (diagnostic) |
| **File/function** | `simulator/diagnostics.py` `analyze_simulation` |
| **Evidence** | 200×42 run: E-901 = **0**; findings list has no `SIM-NO-WIN` / no-win notice because gate requires `trustworthy` true, and suppressed branch only fires when precheck/engine fail |
| **Consequence** | Humans can miss that no simulated path won; executive says “No critical findings” |
| **Required correction** | Emit an explicit untrusted/info finding when `e901==0` (e.g. `SIM-NO-WIN-UNTRUSTED`) stating rates are observed-but-untrusted |
| **Invalidates** | **Diagnosis** (completeness); repair planning priority; quantitative output already untrusted |

### OE-02 — Executive “proven” empties all UNDETERMINED facts

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/explainer.py` `_trust_affects`; `advisory_output.py` `_executive_diagnostic` |
| **Evidence** | Any `layer==UNDETERMINED` ⇒ `trust_affects_conclusion=True` ⇒ proven list empty; trust downgrade itself appears only under “suspected” |
| **Consequence** | Phone users cannot see what *is* proven (trust gate fired; graph flags exist) |
| **Required correction** | Treat trust-gate findings and topology facts as proven; only adventure-blame claims go to suspected |
| **Invalidates** | **Diagnosis** clarity; repair planning triage |

### OE-03 — Keyword follow-up matcher never fires (dead code)

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `_resolve_follow_up` |
| **Evidence** | Probe over all adapter nodes: **0** keyword hits. Rules need `"gym"` / `"james alibi"` / `"vendor"` / `"phone log"` inside a label built from `node id + type + check id` — those substrings never appear. Trust text still says “Phone follow-ups use keyword heuristics” |
| **Consequence** | C-13/C-14 recovery via case-file follow-up slots not simulated; trust rationale misdescribes the gap; authors may think heuristics exist |
| **Required correction** | Implement real follow-up selection **or** list `simulator_unsupported: ["follow_ups keyword slots unimplemented"]` and remove “heuristics” wording |
| **Invalidates** | **Quantitative** clue/ending rates; diagnosis of follow-up fairness; repair advice that assumes partial keyword support |

### OE-04 — Stale ambiguity #5 still blocks/trust-messages

| Field | Value |
|---|---|
| **Severity** | **major** (trust hygiene) |
| **File/function** | `adventures/CASE_BENCHMARK_v0.4/sim_adapter.json` `ambiguities[4]` (read by trust gate); engine already tracks `once_per_hub` |
| **Evidence** | After using revisit, hub options omit `stairwell_revisit`; ambiguity text still claims not tracked |
| **Consequence** | Trust downgrade reason list is partly wrong; wastes author attention |
| **Required correction** | Remove or rewrite ambiguity #5; prefer material blockers (P-112, follow-ups) in `simulator_unsupported` |
| **Invalidates** | Trust **messaging**; not the decision to stay untrusted (other blockers remain) |

### OE-05 — High confidence retained on trust-affected findings

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/explainer.py` `explain_finding` confidence line |
| **Evidence** | `confidence="low" if trust and finding.confidence != "high" else finding.confidence` — bottlenecks stay **high** while `trust_affects_conclusion=True` |
| **Consequence** | Reports sound more certain than evidence supports |
| **Required correction** | Cap confidence at `low`/`medium` whenever trust affects conclusion |
| **Invalidates** | **Diagnosis** certainty; repair priority |

### OE-06 — `repair-plan --finding` overwrites full backlog

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/commands.py` `cmd_repair_plan` → `write_advisory_outputs(..., options)` |
| **Evidence** | After full diagnostic, `repair-plan --finding SIM-FAKE-J-122` left `repair_backlog.md` / `repair_options.json` containing **only** that finding’s options |
| **Consequence** | Offline workflow destroys prior repair plan; easy to lose trust/bottleneck items |
| **Required correction** | Write finding-scoped files; do not replace global backlog unless `--replace-backlog` |
| **Invalidates** | **Repair planning** artifact integrity |

### OE-07 — P-112 manager key still always granted

| Field | Value |
|---|---|
| **Severity** | **major** (simulator fidelity; known V2 material ambiguity) |
| **File/function** | `sim_adapter.json` `nodes.P-112.flags`; not fixed in engine |
| **Evidence** | Flags still `MOTIVE_WITNESS` + `ACCESS_MANAGER_KEY`; loader only documents partial support |
| **Consequence** | Basement/T3 access rates biased easy |
| **Required correction** | Conditional grant vs Records partner state, **or** keep unsupported and exclude access metrics from trusted claims |
| **Invalidates** | **Quantitative** opportunity/access/ending rates |

### OE-08 — Incomplete I-02 still free to retry

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `step` I-02 branch |
| **Evidence** | Blocked I-02 → J-300 with clock delta **0**; 35/50 random runs show `blocked-I-02`; deadline cap prevents multi-thousand fiction but E-904 still dominates (81.5% in 200-run batch) |
| **Consequence** | Strategies burn the clock on free hub loops; ending mix still not a fair model of intended infer cost |
| **Required correction** | Charge infer minutes and/or require new evidence before re-attempt |
| **Invalidates** | **Quantitative** ending/time distributions |

### OE-09 — Summary presents untrusted rates as ordinary results

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/output.py` `write_summary` |
| **Evidence** | `summary.md` shows fiction avg and ending counts with only a boolean trustworthy line; no “DO NOT TUNE FROM THESE RATES” banner |
| **Consequence** | Phone users skim numbers and may adjust adventure difficulty anyway |
| **Required correction** | When untrusted, prefix rates with untrusted warning; move rates under a clearly labeled untrusted section |
| **Invalidates** | Human use of **quantitative** output |

### OE-10 — Placeholder `.patch` files invite false confidence

| Field | Value |
|---|---|
| **Severity** | **minor–major** |
| **File/function** | `simulator/repair_advisor.py` `write_proposed_patch` |
| **Evidence** | File contains only comments: “Generate real diff after human selects an approach.” Extension `.patch` suggests `git apply` readiness |
| **Consequence** | Users may think a fix was generated; empty apply fails or confuses |
| **Required correction** | Use `.patch.txt` / omit `.patch` until a real diff exists; state “NOT A PATCH” in first line more clearly |
| **Invalidates** | Repair planning UX (not auto-apply — auto-apply remains prevented) |

### OE-11 — AI trust context missing material evidence

| Field | Value |
|---|---|
| **Severity** | **major** (local-AI handoff) |
| **File/function** | `simulator/ai_context.py` `build_finding_context` |
| **Evidence** | Trust context: empty `node_excerpt`; no ambiguities array; engine_rules = fair-play only; no P-112 / follow_ups excerpts |
| **Consequence** | Local model must invent or the human must reopen the repo — defeats compact handoff goal |
| **Required correction** | For trust findings, attach `ambiguities`, `simulator_partial`, follow_ups, and cited node snippets |
| **Invalidates** | **Local-AI handoff** completeness |

### OE-12 — Termux shebang non-portable / docs assume `./` works everywhere

| Field | Value |
|---|---|
| **Severity** | **minor** on Pixel Termux; **major** if scripts are claimed universal |
| **File/function** | `run_full_diagnostic.sh`, `explain_latest.sh`, `export_latest_for_ai.sh` shebang |
| **Evidence** | `./run_full_diagnostic.sh` → `required file not found` on Linux review host; `bash ./…` works |
| **Consequence** | Copying repo to non-Termux environments breaks one-command flow |
| **Required correction** | Prefer `#!/usr/bin/env bash` (Termux provides it) or document `bash ./script` |
| **Invalidates** | Termux readiness claim only if device lacks that path (it has it) |

### OE-13 — Harborview-specific `return_hub` / risky hardcoding remains

| Field | Value |
|---|---|
| **Severity** | **minor** (simulator generality) |
| **File/function** | `engine.py` `hub_id != 1`; `public_options` risky id set; `CooperationStrategy` action ids |
| **Evidence** | Revisit return gated on `hub_id != 1`; risky ids hardcode Harborview verbs |
| **Consequence** | Next adventure may mis-simulate revisit/risk |
| **Required correction** | Drive from adapter flags (`returns_to_hub`, `risky: true`) |
| **Invalidates** | Cross-adventure quantitative claims |

### OE-14 — Tests do not catch OE-01 / OE-03 / OE-06

| Field | Value |
|---|---|
| **Severity** | **major** (assurance) |
| **File/function** | `tests/test_explainer.py` et al. |
| **Evidence** | 58 tests pass; no assertion that keyword follow-ups fire; no assertion that 0% E-901 emits a finding when untrusted; no test that repair-plan preserves backlog |
| **Consequence** | Regressions and known gaps stay green |
| **Required correction** | Add adversarial tests for dead follow-ups, no-win untrusted finding, backlog non-clobber |
| **Invalidates** | Confidence in “tests passing ⇒ ready” |

---

## Prior V2 items — disposition after PR #23

| V2 ID | Disposition |
|---|---|
| V2-01 deadline restore | **Fixed** (with clock cap) |
| V2-02 I-02 time bomb | **Partially mitigated** (cap yes; free retry remains — OE-08) |
| V2-03 Hub-2 revisit → Hub-1 | **Fixed** |
| V2-04 hub_targets collision | **Fixed** |
| V2-05 follow-up slots | **Not truly implemented** (OE-03); forced P-214 path works |
| V2-06 SIM-FAKE ownership | **Fixed** |
| V2-07 PoorDecisions / priority | **Improved** (culprit can be picked; defaults remain Harborview-flavored) |
| V2-08 James → P-214 | **Fixed** under probe |
| V2-09 memory/max_states | **Partially fixed** (per-run; batch accumulation weak) |

---

## Scores and gates

| Score | /10 | Rationale |
|---|---:|---|
| **Simulator correctness** | **6.5** | Deadline/revisit/target/P-214/trust-fake fixed; P-112, dead follow-ups, free I-02 retry remain |
| **Explanation quality** | **5** | Structure good; certainty bugs (OE-02/05); generic bottleneck prose; trust wording inaccurate on follow-ups |
| **Repair usefulness** | **4.5** | Non-destructive and layered, but generic; backlog clobber (OE-06); placeholder patches (OE-10) |
| **Local-AI handoff quality** | **4** | Prompts OK; trust context missing material excerpts (OE-11); rates still shipped to the model |
| **Termux readiness** | **CONDITIONAL PASS** | Offline python path works; Termux shebang OK on Pixel; Linux `./` fails; guards exist but batch-weak |

| Gate | Answer |
|---|---|
| **Safe for offline diagnosis** | **YES** — qualitative trust-gated reading only; always open `executive_diagnostic.md` and treat rates as untrusted |
| **Safe for offline repair planning** | **YES, narrowly** — use options as discussion prompts; do not treat placeholders as patches; re-run full diagnostic after any `repair-plan --finding` |
| **Safe for quantitative adventure tuning** | **NO** |

---

## Minimum fixes remaining

1. Emit an observed-no-win finding when E-901 rate is 0 even if untrusted (OE-01).  
2. Fix or delete keyword `_resolve_follow_up`; set honest `simulator_unsupported` (OE-03).  
3. Remove stale ambiguity #5; keep material P-112 / follow-up blockers (OE-04).  
4. Cap explanation confidence when trust affects conclusion; fix executive proven/suspected split (OE-02, OE-05).  
5. Stop `repair-plan --finding` from wiping the global backlog (OE-06).  
6. Banner untrusted rates in `summary.md` (OE-09).  
7. Enrich trust AI context with ambiguities + cited nodes (OE-11).  
8. Charge time (or gate) incomplete I-02 retries (OE-08).  
9. Resolve or fully isolate P-112 key grant (OE-07).  
10. Add regression tests for OE-01/03/06 (OE-14).

Until 1–7 land, treat PR #23 as a **usable offline report formatter on top of a still-untrusted simulator**, not as a green light for adventure balance numbers.

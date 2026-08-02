# IDNE Simulator — Independent Review

**Reviewer posture:** adversarial; do not trust `SIMULATOR_IMPLEMENTATION_REPORT.md`, prior PASS claims, or generated reports without re-execution.  
**Branch under review:** `cursor/idne-simulator-bad4`  
**Review date:** 2026-08-02  
**Scope:** `idne_sim.py`, `simulator/`, `tests/`, `adventures/CASE_BENCHMARK_v0.4/` (PLAYER + `sim_adapter.json` + LOGIC), `IDNE_ENGINE_v0.4.md`, `IDNE_ADVENTURE_QA_SPEC.md`  
**Method:** full source read + independent probes + required CLI/test runs  
**No simulator code was modified.**

---

## Executive verdict

The simulator is a useful **scaffold**, not a trustworthy simulation of IDNE v0.4 Harborview play.

**E-901 (correct win) is unreachable under the current engine** due to Infer I-03 ordering. Combined with **double-charged hub destination time** and **cumulative split role-minutes corrupting parallel wall-clock**, ending-frequency and time metrics are **not safe for engine or adventure decisions**.

Unit tests pass (21/21) but **do not cover** the failure modes that invalidate Monte Carlo outputs.

---

## Re-execution evidence (this review)

| Command | Result |
|---|---|
| `python3 -m unittest discover -s tests -v` | **21 OK** |
| `validate adventures/CASE_BENCHMARK_v0.4` | `simulation_output/20260802_072143` — 0 findings |
| `simulate … --runs 1000 --seed 42` | `simulation_output/20260802_072206` — **E-901 = 0 / 1000**; E-904 = 749; avg “wall” = **3014.59** fiction-minutes |
| `trace … --seed 42` | `simulation_output/20260802_072207` — ending **E-902**; accused Tomás; **infers = [I-01] only**; clock 22:21 |
| `compare … --runs-per-strategy 100` | `simulation_output/20260802_072144` — 800 runs; **E-901 = 0**; E-904 = 560 |

**Same-second output collision:** validate/simulate/trace/compare launched in one shell overwrote folders when timestamps matched (only last writer survives). That is a tooling defect (see ISS-14).

---

## Review by required topic

### 1. Parser and adapter correctness

There is **no Markdown parser**. Simulation authority is `sim_adapter.json` (hand-authored). `loader.py` loads JSON + optional PLAYER text for light static scans.

| Assessment | Detail |
|---|---|
| Strength | Explicit adapter avoids nondeterministic MD parsing |
| Weakness | `validate.py` barely checks adapter↔PLAYER congruence (empty clue cross-check loop at lines 69–75) |
| Consequence | Adapter drift from PLAYER is easy to miss |

### 2. `sim_adapter.json` vs canonical logic vs PLAYER

| Source | Hub 1 actions | Simulator follows |
|---|---|---|
| PLAYER v0.4.1 `JOINT_SCENES.md` | stairwell / Park / **one** split / notes | **Yes** |
| LOGIC `10_INVESTIGATION_NODE_GRAPH.md` (stale v0.4.0) | bakery vs records as **separate** hub actions | **No** |

Adapter `player_version: 0.4.1` and documented `ambiguities[]` correctly prefer PLAYER over stale LOGIC for hub shape. That is the right Delivery Adapter choice **if** LOGIC is marked non-authoritative for play — but findings never emit a **LOGIC↔PLAYER mismatch** finding, so authors may think LOGIC was validated.

**Classification of prior BLK-04:** real divergence; severity is **documentation/authority**, not a simulation runtime blocker by itself. Current outputs are not invalidated solely by BLK-04.

### 3. Graph fidelity

`graph.py` reachability: 48/48 nodes reachable; no dead ends; endings linked from `J-600`. Graph CSV is structurally coherent.

Gaps:

- `once_per_hub` present on `J-300.stairwell_revisit` but **ignored** by `engine.step` hub handling.
- `follow_ups` / `follow_up_max` in adapter **never read** by engine.
- Check `needs_followup: P-214` on `CHK_JAMES_PRESS` fail is **never enforced**.

### 4. State transitions

Critical defects in `SimulationEngine.step` / `resolve_split` / infer handling (see issues below). Clue idempotence (`GameState.grant_clue`) is correct. Threshold flags apply on clock advance.

### 5–7. Shared clock, parallel wall-clock, split/regroup

Engine **intends** IDNE §5.3 `max(role_A, role_B) + sync`, and `resolve_split` computes that formula — but **feeds it the wrong inputs** after split 1:

```text
Evidence (clue-seeking seed 99):
  split1: people=25, records=26, wall=31   ← plausible window totals
  split2: people=55, records=48, wall=60   ← cumulative (25+30, 26+22)
  Correct split2 wall ≈ max(30,22)+5 = 35
  Overcharge ≈ +25 fiction-minutes on split2 alone
```

Cause: `run_role_path` clones full state (including prior `role_minutes`), then `resolve_split` uses those totals as if they were **window-local**.

Additionally, hub choices charge minutes **and** destination nodes charge the same minutes again (ISS-02).

Together these inflate clock → **false E-904 dominance**. `avg_wall_minutes` ≈ 3000 on a 240-minute deadline window is diagnostic of loops/bugs, not Harborview design.

### 8. Strategy hidden-information leakage

| Leak | Location | Evidence |
|---|---|---|
| Hardcoded culprit heuristic | `strategies.py` `Strategy.pick_accused` | `if PROOF_OPPORTUNITY and "C-15" → "Tomás Reyes"` |
| Future clue preview | `engine.enrich_options` | Options carry `grants_clues` from destination + check pass/fail branches before visit |
| Adapter `truth` | passed into strategy ctor | Not read by strategies today, but API encourages leakage |

Trace seed 42: accused **Tomás Reyes** with **PROOF_MOTIVE false** and only I-01 complete — accusation driven by C-15 heuristic, not fair synthesis.

### 9. Clue / conclusion reachability

Static graph can reach nodes that grant all proof clues. **Dynamic** fair win is blocked by ISS-01 (I-03 never marked). Force-path probe with perfect accusation still never produced E-901 (0/200) under current engine; manually adding `I-03` to `infers_done` after J-510 yields E-901.

### 10. Checks / fallbacks

| Check | Issue |
|---|---|
| `roll_check` | Focus bonus hardcoded `2` for both roles (`checks.py`) — role distinction nonexistent |
| `apply_check_outcome` | Fail path adds `extra_minutes` **twice** for `CHK_INVOICE` (branch + `if not passed` re-read) → **30** instead of **15** |
| `needs_followup` | Documented in adapter; ignored by engine |
| Fail still grants major alternate clues | Modeled for invoice; OK if intentional |

### 11. Ending dispatch / priority

`endings.py` order matches PLAYER J-600 for timeout → decline → correct → wrong/incomplete.

Bugs:

- E-901 requires `"I-03" in infers_done`, but engine never sets I-03 (ISS-01).
- Wrong full-proof accusation correctly → E-902 when I-03 present.
- Redundant branch at lines 33–38 always collapses to E-902 when `any_proof`.

### 12. Fake-choice detection

Detects adapter `fake_choice` flag and hubs with duplicate targets. Harborview flags `J-122`, `R-212b`. Does **not** detect semantic fake agency (identical information, different labels) without flags — incomplete vs QA-FA-01/02.

### 13. Role-balance metrics

`_split_balance_stats` averages **`joint_minutes`**, not per-role split deltas. Compare output: `split_balance.avg_joint_minutes ≈ 3199` — useless for §6.4 (≤5 min role delta). **Role-balance diagnostics are not operational.**

### 14. Finding ownership classification

`SIM-NO-WIN` attributed to **ADVENTURE** with medium confidence after 0/800 E-901. Independent analysis shows root cause is **SIMULATOR** (I-03 ordering + clock bugs). Misclassification would send authors to rewrite Harborview incorrectly.

Bottleneck findings for C-06/C-12 are plausible adventure notes but confidence/layer presented as if simulation-proven fairness defects.

### 15. Deterministic seeds

`run_batch` with same `(strategy, seed)` reproduces ending/clues (verified). Good.

`simulate` uses only **random** strategy — seed sweeps RNG, not strategy diversity. Documented CLI example implies Monte Carlo of “play,” but it is Monte Carlo of one biased policy.

### 16. Phone / Termux safety

| Guard | Declared (`config.py`) | Enforced |
|---|---|---|
| `timeout_seconds` | yes | yes in `cmd_simulate` |
| `max_runs` | yes | yes |
| `progress_interval` | yes | yes |
| Ctrl+C partial save | claimed | saves completed runs after interrupt; **does not** checkpoint mid-run |
| `memory_guard_mb` | 256 | **never referenced** in runner/engine |
| `max_states` | 500_000 | **never referenced** |
| Unbounded recursion | avoided (iterative loops) | ok |
| Output collision | — | second-resolution folders collide |

Termux readiness: **CONDITIONAL PASS** (runs; hard limits incomplete).

### 17. Test quality

Tests verify happy-path fragments. **Missing** critical cases:

- E-901 reachable via full engine run
- Hub destination not double-charged
- Split2 wall uses window-local minutes only
- I-02 incomplete must not silently proceed (or must be documented)
- I-03 mark after accusation
- Check fail extra_minutes once
- Strategy cannot prefer culprit via C-15 hardcode / grants_clues peek
- `once_per_hub` / follow-up limits
- Role-balance metric correctness
- Output folder uniqueness under rapid successive runs

Passing 21 tests **does not** imply simulation correctness.

### 18. Prior BLK-01 … BLK-06 classification audit

| Prior ID | Claim | Independent classification | Correct? |
|---|---|---|---|
| BLK-01 `once_per_hub` | SIMULATOR minor | **SIMULATOR / minor–major** (infinite revisit inflates time/E-904) | Understated |
| BLK-02 follow-up slots | SIMULATOR | **SIMULATOR / major** for opportunity recovery paths (C-13/C-14) | Understated |
| BLK-03 I-02 failure loop | SIMULATOR | **SIMULATOR / major** — incomplete I-02 still advances to J-500 | Correct layer; severity understated in prior report tone |
| BLK-04 LOGIC v0.4.0 vs PLAYER v0.4.1 | DELIVERY_ADAPTER | **DELIVERY_ADAPTER / minor** for runtime (adapter follows PLAYER); **major** if LOGIC treated as canonical without warning finding | Mostly correct |
| BLK-05 fiction vs real wall-clock | HUMAN_PLAYTEST | **SIMULATOR reporting defect** first: metrics name `wall_minutes` but store **fiction clock deltas**; then HUMAN_PLAYTEST for real session length | Misclassified as playtest-only |
| BLK-06 high E-904 | ADVENTURE tuning | **Primarily SIMULATOR** (clock bugs + strategy bias). Residual adventure deadline pressure unknown until bugs fixed | **Incorrect** |

### 19. Missing blockers (not in BLK list)

See ISS-01 through ISS-15 below. Highest missing items: **I-03 never marked**, **split minute accumulation**, **hub double-charge**, **check fail ×2 minutes**, **strategy culprit leak**, **finding mis-ownership**, **output folder collision**.

---

## Issue register

### ISS-01 — Infer I-03 never marked → E-901 impossible

| Field | Value |
|---|---|
| **Severity** | **critical** |
| **File/function** | `simulator/engine.py` `SimulationEngine.step` (infer branch); `simulator/state.py` `can_complete_infer("I-03")`; `simulator/endings.py` `evaluate_ending` |
| **Evidence** | After stepping J-510 with full proof + accuse Tomás: `accused` set, `I-03` **not** in `infers_done`. `can_complete_infer(I-03)` requires accused **before** mark; accuse happens **after** the check. Forced I-03 insertion → E-901. Monte Carlo: **0/1000** and **0/800** E-901. |
| **Consequence** | Correct win ending unreachable; `SIM-NO-WIN` falsely blames adventure |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Set accused first (or allow I-03 without prior accused), then re-evaluate infer completion before leaving J-510; require I-03 only when worksheet complete |
| **Invalidates outputs?** | **YES** — all ending distributions and win-rate findings |

### ISS-02 — Hub choice time double-charged with destination minutes

| Field | Value |
|---|---|
| **Severity** | **critical** |
| **File/function** | `simulator/engine.py` `step` (hub) + `apply_node_effects`; `sim_adapter.json` nodes `J-110`/`J-121`/… |
| **Evidence** | Stairwell: hub +15 then J-110 +15 → clock +30 for one 15-min PLAYER action. Probe: 19:00 → 19:30 for single stairwell visit. |
| **Consequence** | Artificial deadline pressure; inflated E-904 |
| **Owning layer** | **SIMULATOR** (or adapter authoring error if destination minutes meant to be zero when hub pays) |
| **Required correction** | Charge cost once (prefer edge/hub cost; destination `minutes: 0` when already paid) |
| **Invalidates outputs?** | **YES** — time, threshold, ending frequency |

### ISS-03 — Split role-minutes accumulate across windows; parallel wall uses totals

| Field | Value |
|---|---|
| **Severity** | **critical** |
| **File/function** | `simulator/engine.py` `run_role_path`, `resolve_split` |
| **Evidence** | Split2 `people_minutes=55` includes split1’s 25; wall 60 vs ~35 correct |
| **Consequence** | Violates IDNE §5.3; clock jumps; E-904 overrepresented |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Track window-local elapsed; `max(local_A, local_B)+overhead` only |
| **Invalidates outputs?** | **YES** |

### ISS-04 — Strategy hardcoded Tomás via C-15

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/strategies.py` `Strategy.pick_accused` |
| **Evidence** | Lines 78–79; trace seed 42 accuses Tomás without PROOF_MOTIVE |
| **Consequence** | Contaminates ending mix; not “blind” play |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Accuse from public proof tags + suspect list without adventure-specific culprit keys; or mark strategy as oracle-assisted |
| **Invalidates outputs?** | **YES** for strategy compare / accusation fairness |

### ISS-05 — `enrich_options` leaks future clue grants to chooser

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `enrich_options`; consumers in `strategies.py` |
| **Evidence** | Hub stairwell option exposes `grants_clues: ["C-01"]` before visit; clue-seeking sorts on that |
| **Consequence** | Strategies play with meta-knowledge humans lack |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Strategies see labels/costs/visited only; optional separate oracle mode |
| **Invalidates outputs?** | **YES** for strategy-based diagnostics |

### ISS-06 — CHK_INVOICE fail applies +15 minutes twice

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/checks.py` `apply_check_outcome` |
| **Evidence** | Fail returns **30**; adapter specifies 15 once |
| **Consequence** | Distorts Records path timing and check-failure analysis |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Apply `extra_minutes` once from selected branch |
| **Invalidates outputs?** | **YES** for check/time metrics |

### ISS-07 — I-02 incomplete still advances to J-500

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/engine.py` `step` infer (`elif infer_id == "I-02": pass`) |
| **Evidence** | Trace seed 42: completes run with `infers=['I-01']` only, never blocked at J-410 |
| **Consequence** | Skips PLAYER rule “return to investigation — no shortcut” |
| **Owning layer** | **SIMULATOR** (adapter fidelity) |
| **Required correction** | Block or loop to hub until requirement met; count as failed path if abandoned |
| **Invalidates outputs?** | **YES** for deduction reachability |

### ISS-08 — Follow-ups and `once_per_hub` not simulated

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | Adapter fields present; absent from `engine.py` |
| **Evidence** | `follow_ups`, `follow_up_max`, `once_per_hub: true` unused |
| **Consequence** | Missing recovery routes; infinite stairwell revisit possible |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Implement or emit HIGH confidence “unimplemented rule” findings and exclude affected metrics |
| **Invalidates outputs?** | **Partial** — opportunity/motive recovery and hub revisit stats |

### ISS-09 — `SIM-NO-WIN` / ending findings mis-owned as ADVENTURE

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `simulator/diagnostics.py` `analyze_simulation` |
| **Evidence** | Finding layer=ADVENTURE while ISS-01/02/03 explain zero wins |
| **Consequence** | Unsafe for adventure/engine decision-making |
| **Owning layer** | **SIMULATOR** / **VALIDATOR** |
| **Required correction** | Gate adventure findings on engine self-tests; default unexplained zero-win to SIMULATOR |
| **Invalidates outputs?** | **YES** for finding-driven decisions |

### ISS-10 — Role-balance / wall metrics wrong or misnamed

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `diagnostics._split_balance_stats`; `RunResult.wall_minutes`; reports |
| **Evidence** | Balance uses `joint_minutes`; avg ~3000; name “wall” means fiction clock |
| **Consequence** | Confuses IDNE §5.4 real playtime with WORLD_CLOCK; useless §6.4 balance |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Separate `fiction_minutes` vs estimated `real_play_minutes`; compute per-split role deltas |
| **Invalidates outputs?** | **YES** for pacing/balance |

### ISS-11 — Focus bonus ignores role

| Field | Value |
|---|---|
| **Severity** | **minor** |
| **File/function** | `simulator/checks.py` `roll_check` |
| **Evidence** | `focus = 2 if role == "people" else 2` |
| **Consequence** | Role check asymmetry untestable |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Read focus from character sheets / adapter |
| **Invalidates outputs?** | Partial (check success rates) |

### ISS-12 — James fail follow-up not forced

| Field | Value |
|---|---|
| **Severity** | **minor–major** |
| **File/function** | Adapter `CHK_JAMES_PRESS.fail.needs_followup`; engine ignores |
| **Evidence** | Field never read |
| **Consequence** | C-13 path under-modeled on fail |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Force P-214 on fail when C-13 absent |
| **Invalidates outputs?** | Partial |

### ISS-13 — Memory/state guards not enforced

| Field | Value |
|---|---|
| **Severity** | **major** (Termux safety) |
| **File/function** | `simulator/config.py` vs `runner.py`/`engine.py` |
| **Evidence** | `memory_guard_mb`, `max_states` never referenced |
| **Consequence** | Phone OOM risk on large runs / long paths |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Enforce or remove claims from README |
| **Invalidates outputs?** | No (correctness), yes (safety claims) |

### ISS-14 — Output directory second-collision

| Field | Value |
|---|---|
| **Severity** | **major** (tooling) |
| **File/function** | `simulator/output.py` `make_output_dir` |
| **Evidence** | Rapid CLI sequence wrote multiple modes into same timestamp; earlier results overwritten |
| **Consequence** | Lost validate/simulate artifacts; silent data loss |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Include mode + pid/monotonic counter in folder name |
| **Invalidates outputs?** | Risk of attributing wrong report to a command |

### ISS-15 — Tests do not catch ISS-01–03

| Field | Value |
|---|---|
| **Severity** | **major** |
| **File/function** | `tests/*` |
| **Evidence** | 21 OK while E-901 impossible and clock double-charged |
| **Consequence** | False confidence |
| **Owning layer** | **SIMULATOR** |
| **Required correction** | Add regression tests listed in §17 |
| **Invalidates outputs?** | Indirectly (process) |

### ISS-16 — Split launch hub cost semantics ambiguous

| Field | Value |
|---|---|
| **Severity** | **minor** (parser ambiguity) |
| **File/function** | `sim_adapter.json` J-120 `split1` 20 min; PLAYER “Split up… 20 min → J-130” |
| **Evidence** | Adapter then runs full private paths with additional minutes — may or may not match table intent (setup vs included) |
| **Consequence** | Possible systematic +20/+25 if launch cost was meant to be estimate of split, not additive |
| **Owning layer** | **DELIVERY_ADAPTER** / adventure packaging |
| **Required correction** | Document whether hub split cost is setup-only or inclusive; align adapter |
| **Invalidates outputs?** | Until clarified, time metrics remain ambiguous |

---

## Report epistemology (requirement 16)

Current reports **do not** clearly distinguish:

| Kind | Present? |
|---|---|
| Proven facts (graph edge exists) | Partially (`graph.csv`) |
| Heuristics (impactful %, strategy accusation) | Not labeled |
| Parser/adapter ambiguity | Only in adapter `ambiguities[]`, not findings |
| Human-playtest-only | Not labeled; `HUMAN_PLAYTEST` layer almost unused |

`findings.md` mixes structural observations with causal claims about the adventure without an evidence tier. **Not decision-safe.**

---

## Scores and gates

| Score | Value | Rationale |
|---|---:|---|
| **Correctness** | **3 / 10** | Core win ending unreachable; clock math wrong; checks double-penalize; strategies leak |
| **Diagnostic usefulness** | **4 / 10** | Graph CSV and static spoiler scans useful; Monte Carlo ending/time/balance findings currently misleading |
| **Termux readiness** | **CONDITIONAL PASS** | Runs offline with timeout/progress; memory/state guards unimplemented; output collision |

| Decision gate | Answer |
|---|---|
| **Safe for engine decisions** | **NO** |
| **Safe for adventure tuning** | **NO** |
| **Safe for Delivery Adapter decisions** | **NO** (except narrow static graph/spoiler checks after manual review) |

---

## Minimum fixes before first serious simulation run

Must-fix (block serious use):

1. **ISS-01** — Mark I-03 correctly so E-901 is reachable when proof+accusation valid.  
2. **ISS-03** — Window-local split minutes for `max()` wall advance.  
3. **ISS-02** — Single charge for hub destinations.  
4. **ISS-06** — Check fail extra minutes once.  
5. **ISS-04 + ISS-05** — Remove culprit hardcode and future-clue enrichment from default strategies.  
6. **ISS-09** — Stop emitting ADVENTURE `SIM-NO-WIN` until engine self-test proves E-901 reachable.  
7. **ISS-15** — Add regression tests for 1–6.  
8. **ISS-14** — Unique output directories.

Should-fix before trusting pacing/QA:

9. ISS-07 I-02 gate · 10. ISS-08 follow-ups / once_per_hub · 11. ISS-10 metric naming/balance · 12. ISS-13 memory guard.

---

## What remains usable today (narrow)

Without the above fixes, the following may be used **cautiously** as structural hygiene only:

- Adapter/PLAYER scene-code presence (after fixing validate’s empty clue loop)
- Broken edge detection
- J-600 spoiler string scan
- Hand inspection of `graph.csv` topology

Do **not** use ending frequencies, avg wall minutes, split_balance, strategy compare, or `SIM-NO-WIN` for Harborview or engine changes.

---

## Appendix — Independent probe commands (non-mutating)

Reproduced in this review environment:

- Hub stairwell double-charge: 15+15 → +30  
- Split2 cumulative minutes: 55/48 vs local ~30/22  
- J-510 step: accused set, I-03 absent  
- Manual I-03 → E-901  
- CHK_INVOICE fail extra = 30  
- Strategy pick with C-15 → Tomás  
- Per-strategy 100-run ending tables (E-901 always 0)

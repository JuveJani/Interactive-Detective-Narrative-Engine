# Simulator Adapter — Independent Review

**Reviewer posture:** adversarial. Do not trust `SIMULATOR_ADAPTER_CLOSURE_REPORT.md` or the 91 passing tests without re-execution and independent probes.  
**Subject:** `cursor/simulator-adapter-closure-bad4` (commit `aaba81d`) / Harborview `CASE_BENCHMARK_v0.4`  
**Review date:** 2026-08-03  
**Against:** V2 residuals in `OFFLINE_EXPLAINER_INDEPENDENT_REVIEW_V2.md` (P-112 unconditional key; 4 ambiguities; legacy `follow_ups`; free I-02 retry)

---

## Verdict (short)

Eight of nine verification claims **PASS** under live probes against PLAYER/LOGIC sources. Claim 7 **FAILS**: `simulator_trustworthy()` can still return true after regressing P-112 to an unconditional key grant or removing I-02 `blocked_*` fields.

Harborview’s **currently authored** adapter is behaviorally correct on P-112, follow-ups, I-02 cost, and the four former ambiguities. Quantitative rates may be used for Harborview tuning, with the trust-gate regression hole listed as a remaining soft blocker.

| Gate | Result |
|------|--------|
| **Correctness** | **8 / 10** |
| **Offline diagnosis** | **YES** |
| **Offline repair planning** | **YES** |
| **Quantitative tuning** | **YES** (current Harborview adapter; see remaining blockers) |
| **Termux readiness** | **YES** |

---

## Method (what was actually done)

| Step | Result |
|------|--------|
| Adversarial probe script (`/tmp/verify_adapter_closure.py`) | **8 PASS / 1 FAIL** |
| Extra live split / skim / source checks | P-112 merge OK; R-212b **can** depth-loop; J-121 PLAYER matches adapter |
| `python3 -m unittest discover -s tests -v` | **91 OK** (informational only) |
| `./run_full_diagnostic.sh 1000 42` | `simulator_trustworthy: true`; endings E-901:**5**, E-902:91, E-904:824, E-905:80 |
| PLAYER / LOGIC cross-read | Booklet P-112, P-111, JOINT J-121 / J-410, LOGIC vars + entity table |
| Prior vs new diagnostic | Prior `20260803_075004_576678_simulate_0` and new `20260803_091954_419392_simulate_0` both trusted |

Passing unit tests were **not** treated as proof.

---

## Claim-by-claim verification

### 1. P-112 manager key only under canonical conditions — **PASS**

| Check | Result |
|-------|--------|
| Authoritative rule | `PLAYER/BOOKLET_PEOPLE.md` §P-112: *“Mark ACCESS_MANAGER_KEY if Records partner lacks it.”* |
| LOGIC | `01_WORLD_STATE_VARIABLES.md`: key from P-112 **or** R-111 |
| Adapter | P-112 `flags` = `MOTIVE_WITNESS` only; `partner_conditional_flags` present |
| People path alone | Does **not** grant `ACCESS_MANAGER_KEY` before merge |
| Full split, Records lacks key, P-112 visited | Key **granted** at merge |
| Full split, skip P-112 and R-111b | Key **absent** |
| Records takes R-111b | Key present via Records (canonical alternate source) |

Closure report’s behavioral claim holds. Loader no longer injects `simulator_partial` for P-112.

---

### 2. Every claimed adapter ambiguity genuinely resolved — **PASS** (with residuals)

| ID | Authoritative source | Live / text check | Status |
|----|----------------------|-------------------|--------|
| AMB-J121 | `PLAYER/JOINT_SCENES.md` §J-121: *Continue to J-120 or J-130* | Adapter `next_options: [J-120, J-130]` matches PLAYER | Resolved |
| AMB-P112 | Booklet §P-112 | Conditional merge (claim 1) | Resolved |
| AMB-P111 | Booklet §P-111 closed bakery phone (+15, partial C-07) | Gate `branch_choices` skip vs phone; live phone grants C-07 ≥15 min; skip does not | Resolved |
| AMB-R212B | Adapter `fake_choice` + PLAYER skim as low-value | Marked `fake_choice`; diagnostics emit `SIM-FAKE-R-212b` | Documented |

`ambiguities[]` is empty; entries live under `resolved_ambiguities[]`.

**Residuals (do not flip claim to FAIL):**

1. **AMB-J121 cites `sim_adapter.json` as authoritative** — circular. PLAYER §J-121 is the real source and agrees; citation quality only.
2. **AMB-R212B resolution text says “engine does not loop”** — **false**. Adversarial always-skim burns role path until depth limit (`mins≈1250`, path length 500). `fake_choice` is a diagnostic marker, not a loop break. Closure report overclaims here.

---

### 3. Unresolved ambiguity still blocks quantitative trust — **PASS**

Injecting `ambiguities: ["forced…"]` → `simulator_trustworthy` false with blocker *“adapter documents 1 unresolved ambiguities”*.  
`SIM-TRUST-DOWNGRADE` still emits under forced ambiguity.

---

### 4. Legacy keyword follow-ups never execute — **PASS**

| Check | Result |
|-------|--------|
| Adapter `follow_ups` key | **Absent** |
| `legacy_keyword_follow_ups()` | `[]` |
| `_resolve_follow_up` stub | Always **0** |
| Injected keyword array + hub step | Does **not** grant C-13 |

PLAYER `JOINT_SCENES.md` still documents the free-text table (gym / vendor / other). That is player prose; simulation uses `follow_up_actions` only. No partially active keyword mechanic in the engine.

---

### 5. Explicit follow-ups work and respect limits — **PASS**

| Check | Result |
|-------|--------|
| Eligible when fail flag + missing C-13 | `FU_GYM_ALIBI` appears at J-300 |
| Cost / grant | +10 min, grants C-13 once |
| Per-action max | Second apply returns 0 |
| Global `follow_up_max` | No eligible options when budget exhausted |
| Hub `step` path | Applies FU and stays at hub |

**Residual (from V2, still true):** `needs_followup → P-214` visit still increments `follow_ups_used` inside `run_role_path`, coupling forced scene follow-ups to the phone-slot budget.

---

### 6. I-02 retry cost canonical and applied once — **PASS** (interpretive residual)

| Check | Result |
|-------|--------|
| Adapter | `blocked_return: J-300`, `blocked_minutes: 10` |
| Incomplete I-02 | Returns to J-300; clock **+10**; infer not marked |
| Second blocked visit | Charges **+10** again (once per visit, not once per case) |
| Successful I-02 | +10 and advances to J-500 |

**Authoritative reading:**

- `PLAYER/JOINT_SCENES.md` §J-410 places *“Advance +10 min. Continue to J-500”* **after** *“Mark I-02 complete when done.”* Incomplete path says return / no shortcut but does **not** explicitly restate a minute cost.
- Closure applied **10** as the J-410 scene cost on both paths — same number as the authored success cost; not an invented free number.
- `DO_NOT_READ/LOGIC/00_ENTITY_KEY_TABLE.md` lists J-410 duration **12**, conflicting with PLAYER/adapter **10**. Adapter follows PLAYER (correct precedence for player-facing cost). Entity-table drift is a residual documentation inconsistency, not an adapter miss.

Verdict: mechanics correct; canonicity of charging the incomplete path is a reasonable reading of scene cost, not a wild guess. If stricter policy were required (“no authored blocked cost → unsupported”), this would have been marked unsupported — it was not, and the applied value matches PLAYER’s authored +10.

---

### 7. Quantitative trust cannot become true via missing/default values — **FAIL**

`simulator_trustworthy()` checks: non-empty `ambiguities`, legacy keyword arrays, `simulator_unsupported` / `simulator_partial`, I-02 `blocked_return` **without** `blocked_minutes`, reachability.

It does **not** verify:

| Regression | Trust after regression | Engine behavior |
|------------|------------------------|-----------------|
| Restore unconditional `ACCESS_MANAGER_KEY` on P-112; drop `partner_conditional_flags`; keep `ambiguities: []` | **TRUE** | Wrong key grant returns |
| Remove `blocked_return` **and** `blocked_minutes` from J-410 | **TRUE** | Free I-02 retry returns (engine defaults return to J-300, charges 0) |
| Omit `ambiguities` key entirely | TRUE | Vacuous “nothing unresolved” |

**Partial positive:** `blocked_return` present with `blocked_minutes` missing **does** block trust.

**Conclusion:** Claim 7 fails. The trust flag is not a structural proof of P-112 canonicity or I-02 cost presence. Current Harborview happens to be correctly authored; the gate would not catch a silent regression of those fields if `ambiguities` stayed empty.

---

### 8. Ending, time, balance, strategy metrics internally consistent — **PASS**

Independent 200×42 batch and full 1000×42 diagnostic:

| Metric | 200×42 probe | 1000×42 diagnostic |
|--------|--------------|--------------------|
| Ending sum = runs | yes | 1000 |
| Rates match counts | yes | yes |
| Valid ending codes only | yes | E-901/902/904/905 |
| Fiction minutes ≤ deadline window | yes | avg **233.4** |
| `split_balance` present | yes | avg role Δ ≈ **11.8** min |
| Strategy label | `random` | consistent |
| `simulator_trustworthy` | true | **true**, blockers `[]` |
| Precheck / engine E-901 | — | both true |

Ending mix is harsh under random (E-904 dominant). That is a play/strategy observation now that trust is up — not an adapter integrity failure.

---

### 9. Local-AI reports distinguish qualitative vs quantitative — **PASS**

| Artifact | Trusted Harborview | Forced-untrusted probe |
|----------|--------------------|------------------------|
| `summary.md` | No `QUANTITATIVE RESULTS UNTRUSTED` banner; `Simulator trustworthy: True` | Banner + blockers when ambiguities forced |
| `executive_diagnostic.md` | “Quantitative results trusted: **yes**”; qual diagnosis yes; repair = suggestions only | Trust section lists blockers when untrusted |
| AI context sections | Present | `PROVEN_FACTS` / `SIMULATION_OBSERVATIONS` / `AMBIGUITIES` / `HYPOTHESES` / `FORBIDDEN_CONCLUSIONS` |
| Culprit leak in trust package | — | Not observed |

---

## Closure report accuracy check

| Closure claim | Independent finding |
|---------------|---------------------|
| All four V2 blockers resolved | **Mostly yes** — behaviors hold |
| Quantitative trustworthy | **Yes for current adapter**; trust **gate** incomplete (claim 7) |
| R-212b “engine does not loop” | **False** — adversarial skim loops until depth limit |
| 91 tests / diagnostic trusted | Re-run confirms 91 OK and trusted metrics |

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Correctness** | **8 / 10** | P-112, follow-ups, I-02, ambiguities behaviorally correct; −1 trust-gate hole; −1 R-212b overclaim / skim loop |
| Offline diagnosis | **YES** | Findings + explainer + executive split work offline |
| Offline repair planning | **YES** | Suggestions / backlog / AI context; no auto-edits |
| Quantitative tuning | **YES** | Current Harborview adapter verified by live probes |
| Termux readiness | **YES** | `run_full_diagnostic.sh`, explain/export scripts, offline artifacts |

---

## Remaining blockers

1. **Trust-gate structural gap (claim 7):** does not require `partner_conditional_flags` on P-112 or presence of I-02 `blocked_minutes` when `blocked_return` is absent. Silent regression can keep `simulator_trustworthy: true`.
2. **R-212b skim:** `fake_choice` does not stop adversarial role-path loops; resolution text overclaims.
3. **I-02 documentation drift:** ENTITY_KEY_TABLE (12) vs PLAYER/adapter (10); blocked-path cost is interpretive of scene cost.
4. **V2 residual:** forced `needs_followup` visits still increment `follow_ups_used`.
5. **Play observation (not an adapter blocker):** random strategy ≈82% E-904 at 1000×42 — use for tuning carefully with better strategies / human playtest.

None of (2)–(5) re-open the four V2 material adapter blockers for the current authored package.

---

## Final answers

| Question | Answer |
|----------|--------|
| **Correctness /10** | **8** |
| **Offline diagnosis** | **YES** |
| **Offline repair planning** | **YES** |
| **Quantitative tuning** | **YES** |
| **Remaining blockers** | Trust-gate regression hole; R-212b loop overclaim; I-02 entity-table drift; `needs_followup` budget coupling; high random E-904 (play) |
| **Termux readiness** | **YES** |

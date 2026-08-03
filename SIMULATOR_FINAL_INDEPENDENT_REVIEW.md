# Simulator Final Fixes — Independent Review

**Reviewer posture:** adversarial. Do not trust `SIMULATOR_FINAL_FIX_REPORT.md` or the 111 passing tests without re-execution and independent probes.  
**Subject:** `cursor/simulator-trust-loop-fix-bad4` (commits `5fb8926`…`2d745cc`) / Harborview `CASE_BENCHMARK_v0.4`  
**Review date:** 2026-08-03  
**Against:** prior residuals in `SIMULATOR_ADAPTER_INDEPENDENT_REVIEW.md` (trust-gate hole, R-212b loop, I-02 10↔12, `needs_followup` budget)

---

## Verdict (short)

All **nine** verification claims **PASS** under live mutation probes, PLAYER/LOGIC cross-reads, and a fresh Harborview diagnostic. The final-fix branch closes the prior review’s claim-7 trust-gate hole and the R-212b depth burn.

| Gate | Result |
|------|--------|
| **Correctness** | **9 / 10** |
| **Offline diagnosis** | **YES** |
| **Offline repair planning** | **YES** |
| **Quantitative tuning** | **YES** |
| **Termux readiness** | **PASS** |

---

## Method (what was actually done)

| Step | Result |
|------|--------|
| Adversarial probe script (`/tmp/verify_final_fixes.py` + corrected residual checks) | **9/9 PASS** after fixing two probe string-match false negatives |
| Live mutations | P-112, I-02, follow-ups, empty ambiguities, R-212b loop restore |
| PLAYER / LOGIC cross-read | Booklet R-212b; JOINT J-410 +10; entity table J-410 = 12 |
| `python3 -m unittest discover -s tests -v` | **111 OK** (informational only) |
| `./run_full_diagnostic.sh 1000 42` | `simulator_trustworthy: true`; E-901:**4**, E-902:71, E-904:864, E-905:61 |

Passing unit tests were **not** treated as proof.

---

## Claim-by-claim verification

### 1. Trust becomes false when P-112 eligibility is removed — **PASS**

| Mutation | `simulator_trustworthy` | Blockers (sample) |
|----------|-------------------------|-------------------|
| Drop `partner_conditional_flags` + restore unconditional `ACCESS_MANAGER_KEY` | **false** | unconditional grant; missing partner rules |
| Drop `partner_conditional_flags` only (empty `ambiguities`) | **false** | missing `partner_conditional_flags` |

Canonical adapter remains trusted. Behavioral P-112 merge rule from prior review is unchanged and still required by the gate.

---

### 2. Trust becomes false when I-02 required fields are removed — **PASS**

| Mutation | Result |
|----------|--------|
| Remove `blocked_return` + `blocked_minutes` | **false** (both reported) |
| Remove `blocked_minutes` only | **false** |
| Remove `minutes_cost_resolution` | **false** |

Empty `ambiguities` does not rescue these regressions.

---

### 3. Trust becomes false when required follow-up definitions are missing — **PASS**

| Mutation | Result |
|----------|--------|
| `follow_up_actions = []` | **false** |
| Remove `FU_GYM_ALIBI` only | **false** |
| Delete `follow_up_actions` key | **false** (required field + empty list) |

---

### 4. Empty `ambiguities` cannot falsely produce trustworthy status — **PASS**

| Case | Result |
|------|--------|
| Empty `ambiguities` + otherwise canonical | **true** (correct — invariants hold) |
| Empty `ambiguities` + no P-112 partner rules | **false** |
| Empty `ambiguities` + free I-02 (no blocked fields) | **false** |
| Omit `ambiguities` key entirely | **false** (required schema field) |

This closes the prior independent-review claim-7 failure mode.

---

### 5. R-212b no longer loops to depth limit — **PASS**

| Check | Result |
|-------|--------|
| PLAYER §R-212b | *Advance +5 min. **Continue to R-212** or **R-214**.* |
| Adapter | `next_options: [R-212, R-214]`; skim `once_per_role_path: true` |
| Adversarial always-skim | **1** skim visit; **33** minutes; path length **6**; exits via R-214 |
| Restored auto-`next: R-212` without once-limit | Trust **false**; burns to depth (`mins=200`, path length 80 at `max_path_steps=80`) |

**Note:** `once_per_role_path` is an interpretation of PLAYER “Skim and move on” / retry-R-212a flavor. Returning to R-212 after skim can still choose duplicates (R-212a), which matches the booklet’s retry intent without re-burning skim. Not a conflicting-source ambiguity.

---

### 6. I-02 cost matches authoritative source (or trust-blocking ambiguity) — **PASS**

| Source | Value |
|--------|-------|
| `PLAYER/JOINT_SCENES.md` §J-410 | **+10 min** |
| `DO_NOT_READ/LOGIC/00_ENTITY_KEY_TABLE.md` | **12** |
| Adapter `minutes` / `blocked_minutes` | **10** |
| `minutes_cost_resolution` | authoritative 10; documents entity-table conflict; `unresolved: false` |

Precedence used: `sim_adapter.json` description (“Authoritative for simulation; PLAYER markdown cross-checked”) + PLAYER timing → **10**. Entity table is documented drift, not simulated.

Live incomplete I-02 charges **+10** once. Marking `unresolved: true` or setting minutes to **12** without updating resolution → trust **false**.

---

### 7. `needs_followup` alone does not consume phone budget — **PASS**

| State | Budget |
|-------|--------|
| Visit `P-214` via `pending_followup` | `follow_ups_used` unchanged (**0**) |
| `eligible_follow_up_options` (availability) | no consumption |
| `apply_follow_up(FU_GYM_ALIBI)` (execution) | increments to **1** |

Scene-forced follow-up routing is separated from hub phone-slot budget.

---

### 8. Quantitative results only when every trust invariant passes — **PASS**

| Condition | Observation |
|-----------|-------------|
| Canonical adapter | `simulator_trustworthy: true`; no `SIM-TRUST-DOWNGRADE`; summary has **no** UNTRUSTED banner; fake findings layer `ADVENTURE` |
| Mutate away P-112 partner rules | `simulator_trustworthy: false`; `SIM-TRUST-DOWNGRADE` emits; summary shows `QUANTITATIVE RESULTS UNTRUSTED`; fake findings layer `UNDETERMINED` |

Fresh diagnostic (`20260803_095243_158078_simulate_0`): trusted; blockers `[]`; ending rates emitted without untrusted banner.

---

### 9. Offline reports still explain failures clearly — **PASS**

| Artifact | Untrusted (P-112 mutated) | Trusted (canonical) |
|----------|---------------------------|---------------------|
| `summary.md` | UNTRUSTED banner + blockers | `Simulator trustworthy: True`; no banner |
| `executive_diagnostic.md` | `Quantitative results trusted: **no**` + blockers | `… trusted: **yes**` |
| Explainer on `SIM-TRUST-DOWNGRADE` | `plain_problem`, `where_to_look`, validation steps present | — |
| AI context | `PROVEN_FACTS` / `SIMULATION_OBSERVATIONS` / `AMBIGUITIES` / `HYPOTHESES` / `FORBIDDEN_CONCLUSIONS` | — |

---

## Fix-report accuracy check

| Fix-report claim | Independent finding |
|------------------|---------------------|
| Trust-gate hole closed | **Confirmed** (claims 1–4) |
| R-212b no longer depth-loops | **Confirmed** (claim 5) |
| I-02 cost = PLAYER 10 with documented conflict | **Confirmed** (claim 6) |
| `needs_followup` no longer burns phone budget | **Confirmed** (claim 7) |
| 111 tests / diagnostic trusted | Re-run confirms 111 OK and trusted metrics |

---

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| **Correctness** | **9 / 10** | Structural trust gate + loop/budget/cost fixes hold under mutation; −1 for adventure-hardcoded invariant IDs in `trust_gate.py` (Harborview-specific but intentional) and interpretive `once_per_role_path` |
| Offline diagnosis | **YES** | Findings + explainer + executive split work offline |
| Offline repair planning | **YES** | Suggestions / backlog / AI context; no auto-edits |
| Quantitative tuning | **YES** | Trust requires structural invariants; Harborview passes |
| Termux readiness | **PASS** | Scripts + offline artifacts; diagnostic completed |

---

## Remaining blockers

None material for the four final-fix targets.

Soft residuals (do not block readiness):

1. **Play observation:** random strategy ≈86% E-904 at 1000×42 — tuning input, not adapter defect.  
2. **Entity table drift:** J-410 listed as 12 in `DO_NOT_READ` while PLAYER/adapter use 10 — documented, not simulated.  
3. **`trust_gate.py` Harborview hardcoding:** P-112 / J-410 / R-212b / FU IDs are adventure-specific invariants — appropriate for this package; a multi-adventure gate would need generalization later.

---

## Final answers

| Question | Answer |
|----------|--------|
| **Correctness /10** | **9** |
| **Offline diagnosis** | **YES** |
| **Offline repair planning** | **YES** |
| **Quantitative tuning** | **YES** |
| **Termux readiness** | **PASS** |
| **Remaining blockers** | None material; soft: random E-904 rate, entity-table 12 drift, Harborview-specific trust IDs |

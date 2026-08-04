# Investigation Validator — Normative Specification

**Milestone:** 7 — Investigation Validator  
**Status:** Normative  
**Validation:** `python3 -m idne.investigation_validate`

---

## 1. Purpose

Define one **integrated Investigation Validator** that proves a generated adventure is investigable from beginning to end — not merely that files, IDs, scenes, clues, or schemas exist.

The validator verifies that a player can:

- access required locations;
- perform required interactions;
- obtain enough understandable information;
- answer required inference questions;
- continue after incomplete reasoning;
- reach valid ending chains;
- do so without hidden meta knowledge.

**Supports:** `single_investigator`, `two_player` (does not assume two-player paths are valid solo).

**Integrates with:** Investigation Core, Investigation Flow, Environment, Object Interaction, Capability Check, NPC Investigation, Ending System.

**Delegates to:** `capability_check_validate` for capability-check rules (does not reimplement contradictory check logic).

**Out of scope:** Story Validator, Playtime Calibration, paid retries, false checks, Inventory System, adventure generation, content auto-rewrite.

---

## 2. Declaration

`investigation_validator_manifest.json`:

```json
{
  "schema_version": "1.0",
  "investigation_validator_method": "canonical",
  "package_path": "DO_NOT_READ/investigation_validator_package.json"
}
```

Or `generation_manifest.json` → `investigation_validator.enabled: true`.

---

## 3. Validation layers

### 3.1 End-to-end investigation chain

For every required conclusion, validate trace:

Fixed Truth → source event → world state → location → object or NPC → legal player action → capability check (if any) → observation / testimony / evidence → player knowledge → inference question → conclusion → proof → ending or investigation consequence.

Missing links produce findings at the exact broken layer.

### 3.2 Answerability

Every mandatory inference question must be answerable from player-accessible information:

- terms defined in player-facing material;
- required facts obtainable before the question;
- accepted answer follows from available information;
- question does not reveal the answer;
- no internal IDs required;
- no equally supported unresolved alternatives (unless `intentionally_ambiguous`).

### 3.3 Information sufficiency

Per inference: required information, optional support, contradiction resolution, minimum independent sources, acquisition routes.

Flag: missing/inaccessible sources, late sources, failed-only routes, duplicated independence, unexplained half-information, hidden-world-truth dependence.

### 3.4 Executable recovery routes

On inference failure/incompleteness, every continuation must name an in-world action, have a legal destination, change knowledge/access/state/time, and avoid zero-cost infinite loops.

Reject vague instructions (“investigate again”, bare page codes, unavailable locations).

### 3.5 Object and access solvability

Mandatory keys, passwords, items, documents, NPCs, and locations must have at least one fair path (key not behind its own lock, password derivable, item not consumed before mandatory use).

### 3.6 Capability-check fairness

Mandatory-path checks: success/failure routes, failure does not destroy all fair routes, alternate access when information is mandatory, one-attempt policy, no failure leak, check does not change fixed truth, capability matches task. **Uses Capability Check validator.**

### 3.7 NPC conversation solvability

Required NPC routes: NPC holds information, disclosure route exists, trust/topic/pressure achievable, consistent relationships, meaningful dialogue choices, NPC available before deadline.

### 3.8 Time-state validation

Mandatory routes fit deadline; time variants activate; expired routes redirect; NPC movement represented; revisit uses current variant; deadline ending global; no mutually impossible clocks; no zero-cost infinite investigation.

Does **not** perform real-world playtime calibration.

### 3.9 Ending reachability

Every ending: reachable or flagged decorative; imperfect endings do not reveal full truth; perfect ending requires complete solution; accusation options neutral; deadline ending reachable when time expires.

### 3.10 Player-facing navigation

Reject choices whose meaning depends only on internal codes (J-223, R-212b, bare page numbers). Cross-check actual PLAYER package.

### 3.11 PLAYER cross-layer audit

Detect orphan information, missing canonical actions, pass/fail leaks, missing destinations, location resets, ending contradictions, undefined trust conditions.

### 3.12 Graph and state analysis

Integrated state graph: location, time, object, inventory refs, knowledge, NPC, check attempts, inference, ending. Configurable limits; honest BLOCKED on explosion — no silent truncation PASS.

---

## 4. Validation outcomes

| Outcome | Meaning |
|---|---|
| **PASS** | No proven Tier A defects; Tier B mandatory resolved |
| **FAIL** | Proven Tier A defect |
| **CONDITIONAL_PASS** | Tier B mandatory pending or likely findings only |
| **BLOCKED** | State graph explosion or limits exceeded |
| **SKIP** | Validator not declared |

Structural PASS is forbidden when Tier B mandatory checks remain unresolved.

---

## 5. Tier B mandatory review

Human review required for:

- inference question understandability;
- prose sufficiency of available information;
- fair exclusion of alternative explanations;
- NPC dialogue believability;
- meaningful player choice communication;
- mystery discovered vs delivered;
- final option neutrality;
- imperfect endings avoiding accidental confirmation.

Tier B items in package `tier_b_mandatory` with `resolved: false` block unconditional PASS.

---

## 6. Machine-readable findings

Each finding includes: `finding_id`, `severity`, `confidence`, `layer`, `source_file`, `canonical_id`, `broken_trace`, `expected_rule`, `actual_state`, `affected_conclusions`, `affected_endings`, `suggested_review_action`, `automatically_fixable`, `human_approval_needed`, `tier`.

Schema: `idne/schemas/investigation_validator_finding.schema.json`.

---

## 7. Related documents

- `INVESTIGATION_VALIDATOR_SCHEMA.md` — package schema
- `INVESTIGATION_VALIDATOR_REPORT_FORMAT.md` — report JSON shape
- `INVESTIGATION_CORE_SPEC.md`, `INVESTIGATION_FLOW_SPEC.md`, `CAPABILITY_CHECK_SYSTEM_SPEC.md`
- `IDNE_ADVENTURE_QA_SPEC.md` §5.19

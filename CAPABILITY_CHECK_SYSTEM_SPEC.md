# Capability Check System — Normative Specification

**Milestone:** 6 — Capability Check System Rewrite  
**Status:** Normative  
**Validation:** `python3 -m idne.capability_check_validate`

---

## 1. Purpose

Define the canonical **capability-check system**: `d20 + modifier` resolution, fixed-world invariants, separate result units, one-attempt default, social/NPC integration, and two-player eligibility — without changing Fixed Truth.

**Integrates with:** Object Interaction, Environment, Investigation Core, NPC Investigation, Investigation Flow.

**Does not redesign:** those layers. **Out of scope:** paid retries, false checks, full Inventory, Playtime Calibration, adventure generation.

---

## 2. Core invariant

A check MAY change: what is noticed, understood, whether an action succeeds, available routes, time/resources spent, NPC dynamic state (trust/pressure/suspicion).

A check MUST NEVER change: object existence, document objective contents, past events, culprit, NPC fixed knowledge, evidence provenance, Fixed Truth, canonical world state before the attempt.

---

## 3. Layer position

Object Interaction Package → **Capability Check Package** → Investigation Core → …

Object Interaction and NPC routes **reference** `check_id` from this package. Check definitions are authoritative here.

---

## 4. Resolution

`result = d20 + character_modifier`  
Success when `result >= DC`.

Canonical difficulty bands: Easy 5, Medium 10, Hard 15. Higher/lower DCs require `dc_justification`.

---

## 5. Capability taxonomy

Adventure-defined capabilities under categories:

| Category | Examples |
|---|---|
| `perception_observation` | notice, search, spot |
| `reasoning_interpretation` | interpret document, deduce |
| `technical_operation` | login, operate device |
| `physical_strength` | force, lift |
| `agility` | climb, sneak |
| `social_persuasion` | persuade, negotiate |
| `social_intimidation` | intimidate, pressure |
| `social_deception` | bluff, lie |

Every check names the capability tested. Reject checks whose real subject is truth existence, plot randomness, or ending selection.

---

## 6. One-attempt default

`attempt_policy.default: one_attempt`. Track `NOT_ATTEMPTED | SUCCEEDED | FAILED`. No free re-roll. `retry_extension_point` reserved for future paid retries (not implemented).

---

## 7. Separate result units

Declaration unit: player action, cost, capability, DC, success destination, failure destination — **no outcome prose**.

Success/failure content only in `destination_units`.

---

## 8. Failure information boundary

Failure MUST NOT reveal hidden objects, missed information, correct interpretation, or success results. Failure text states only what the character experiences.

---

## 9. Success information boundary

Success reveals only information from Fixed Truth / current state / attempted action / tested capability. No unrelated deductions or complete solutions.

---

## 10. Action vs check

No check for: obvious actions, clear text, unlocked doors, pure player judgment. Check only when capability materially affects success, both routes are authored, failure remains fair.

---

## 11. Social checks

May open dialogue routes, reveal NPC-held information, modify trust/pressure/suspicion. May NOT invent NPC knowledge, change fixed motivation, force impossible confessions, or convert lies into truth. Intimidation ≠ trust increase unless `intimidation_not_trust_justified`.

---

## 12. Multi-character (`two_player`)

Declare eligibility by role, location, capability. Cooperative policy must explicitly allow joint attempts before counting higher result. No free second-player retry after first failure unless `explicit_joint_attempt_allowed`.

`single_investigator`: active character only.

---

## 13. Time and cost

`time_cost_minutes` once per action. `failure_time_cost_minutes` only when authored, once. Revisit does not re-apply cost without new action.

---

## 14. Check fairness metadata

Each check declares: `why_check_exists`, `dc_justification`, `success_enables`, `failure_consequence`, `alternate_route_exists` when mandatory for fair path.

---

## 15. Information trace

`information_trace`: Fixed Truth → source layer/id → check → success → observation/knowledge ID.

---

## 16. Declaration

`capability_check_manifest.json`:

```json
{
  "schema_version": "1.0",
  "capability_check_method": "canonical",
  "package_path": "DO_NOT_READ/capability_check_package.json"
}
```

Validator: `python3 -m idne.capability_check_validate <adventure_root>`

Legacy adventures: **SKIP**.

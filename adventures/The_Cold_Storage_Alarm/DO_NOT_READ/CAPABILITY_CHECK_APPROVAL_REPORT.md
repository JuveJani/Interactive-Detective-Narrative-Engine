# Capability Checks Approval Report — AUTHOR-ONLY / SPOILER-CONTAINING

**Adventure:** The Cold Storage Alarm  
**Stage gate:** `capability_checks`  
**Status:** `AWAITING_APPROVAL`  
**Do not distribute to players.**

---

## Check inventory

| Check ID | Parent action | Capability | DC | Success knowledge | Mandatory fair path |
|----------|---------------|------------|---:|-------------------|----------------------|
| CHK-PERCEPTION-LATCH | ACT-CHECK-LATCH-WEAR | perception | 13 | KNOW-LATCH-DISTURBANCE | No (optional flavour) |
| CHK-PERCEPTION-LABEL | ACT-SEARCH-LABEL-RESIDUE | perception | 14 | KNOW-LABEL-RESIDUE | No |
| CHK-TECH-TEMP-TREND | ACT-EXPORT-TEMP-TREND | technical | 12 | KNOW-TEMP-TREND | No |
| CHK-PERCEPTION-LOCKER | ACT-INSPECT-LOCKER-14 | perception | 11 | KNOW-BADGE-LOCKER | No (optional branch) |

All four checks referenced by the approved object-interaction layer are defined. No NPC or environment check references remain unresolved. No social checks in this adventure.

---

## DC justification map

| Check | Band | Rationale |
|-------|------|-----------|
| LATCH (13) | Hard | Subtle tool wear under frost haze and industrial lighting |
| LABEL (14) | Hard | Fine adhesive trace blends with routine aisle scuffing |
| TEMP-TREND (12) | Medium-high | BMS export menus under facility time pressure |
| LOCKER (11) | Medium | Badge beneath coveralls in cluttered locker |

---

## Failure and recovery alignment

| Check | Failure flag | Alternate route (flow/IV) | Preserved investigation |
|-------|--------------|---------------------------|-------------------------|
| CHK-PERCEPTION-LATCH | check_latch_failed | REC-SECURITY-ARCHIVE | Badge archive + Marcus latch testimony |
| CHK-PERCEPTION-LABEL | check_label_failed | REC-MANAGER-MANIFEST | Manifest gap + coordinator testimony threads |
| CHK-TECH-TEMP-TREND | check_trend_failed | REC-COLD-DISPLAY | Live temp display + staging panel + BMS command |
| CHK-PERCEPTION-LOCKER | check_locker_failed | REC-SECURITY-ARCHIVE | Badge archive records for misattribution inference |

Failure units contain no hidden-success leakage. No check grants conclusions or perfect reconstruction directly.

---

## Fixed-truth invariants

Every check declares `changes_evidence_existence`, `changes_document_contents`, `changes_fixed_truth`, and `changes_npc_fixed_knowledge` as false. Success reveals only pre-existing observations tied to approved evidence and facts.

---

## Modifier sources

Seven modifier sources declared (perception, reasoning, technical, strength, agility, persuasion, intimidation). All four checks use explicit modifier_source_id bindings. Eligibility: active investigator (single); active investigator at scene (two-player).

---

## Validation

- Capability Check validation — **PASS**
- Investigation Flow — **PASS**
- Investigation Validator (IV-CAPABILITY-DELEGATE) — **PASS**
- Object Interaction — **PASS**
- NPC — **PASS**
- Investigation Core — **PASS**
- World First — **PASS**

Package hash: `8c3d2448706524927cf1f0d157fc255d8c28364be5d98314e11fc6414cd245d4`

---

## Exact approval choices

| Choice | Action |
|--------|--------|
| **Approve capability checks** | Proceed to PLAYER (`story_player`) generation |
| **Request revision** | Specify check DC, failure, or alternate-route changes |
| **Reject** | Halt pipeline; do not generate PLAYER content |

**Do not proceed to story_player until capability_checks gate approved.**

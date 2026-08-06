# képességellenőrzéss Approval Report — PLAYER TEST OWNER (Spoiler-Free)

**Adventure:** A hűtőriasztás  
**Stage gate:** `capability_checks`  
**Status:** `AWAITING_APPROVAL`

---

## Spoiler-free capability-check assessment

| Requirement | Status |
|-------------|--------|
| All referenced checks defined | Yes — 4 checks resolve object-interaction bindings |
| Fixed truth and evidence preserved | Yes — all invariants declare no world-truth mutation |
| Checks affect perception/access/action success only | Yes — no evidence creation or document rewriting |
| One-attempt default | Yes — all checks use `one_attempt` policy |
| Separate success and failure destinations | Yes — distinct destination units per check |
| Failure does not reveal hidden success content | Yes — failure units flagged no-hint; validator CAP-FAIL-LEAK PASS |
| DCs justified and consistent | Yes — dc_justification on all checks; bands 11–14 |
| Investigator eligibility explicit | Yes — active investigator / at-scene for two-player |
| No free retries | Yes — one_attempt with future extension point only |
| No false checks | Yes — all checks gate real optional-or-alternate observations |
| No dedicated puzzle mechanics | Yes — standard d20 + modifier resolution |
| No check grants final solution | Yes — success grants observation-level knowledge only |
| Ending reachability compatible | Yes — Investigation Validator state graph PASS (131,072 states) |

| Check category | Count | Notes |
|----------------|------:|-------|
| Perception / observation | 3 | Cold aisle search, latch wear, locker inspect |
| Technical operation | 1 | Engineering terminal trend export |
| Social | 0 | No NPC checks in this adventure |

---

## Spoiler-free failure and recovery assessment

| Check type | On failure | Investigation preserved via |
|------------|------------|----------------------------|
| Physical search (aisle) | No trace recovered | Manager bevételezési jegyzék records and interview threads |
| Physical search (locker) | Locker inconclusive | Security archive belépőkártya queries |
| Physical search (latch) | Hardware appears routine | Security archive and rounds vallomás |
| Technical export | Export error | Live temperature display and staging panel review |

All four checks declare `alternate_route_exists: true` with helyreállítási úts already authored in the investigation flow layer. Flow revisit alternates for label and trend failures remain wired. No mandatory-path check can destroy all routes (IV-CHECK-FAIRNESS PASS).

---

## Remaining structural concerns

1. PLAYER delivery prose not authored — destination unit player_text is structural placeholder only.
2. Flow flags for latch and locker check failure are declared in capability metadata but not yet mirrored in flow initial state (optional flavour checks).
3. NPC package still contains legacy placeholder IDs; runtime resolution continues via investigation-core map.
4. Tier B playtest recommended to confirm failure prose feels fair at the table without hinting missed content.
5. Paid retry extension point reserved but not implemented in engine.

---

## Exact approval choices

| Choice | Action |
|--------|--------|
| **Approve képességellenőrzéss** | Proceed to PLAYER (`story_player`) generation |
| **Request revision** | Specify check DC, failure, or alternate-route changes |
| **Reject** | Halt pipeline; do not generate PLAYER content |

**Current gate:** `capability_checks` — **AWAITING_APPROVAL**

---

## Validation status

- képességellenőrzés validation — **PASS**
- Investigation Flow validation — **PASS**
- Investigation Validator — **PASS**
- Object Interaction — **PASS**
- NPC — **PASS**
- nyomozási mag — **PASS**
- World First — **PASS**

No PLAYER, playtime, DM-feeling, or package export generated.

# DO NOT READ: Clue Dependency Graph

## 1. Notation and the progress model

This document is the clue register. It owns the `CLUE_` namespace.

The canonical progression is:

```text
Node outcome
     ↓
  Points
     ↓
  Clues
     ↓
Conclusions
```

`GRANT_CLUE(clue_identifier)` is the only operation a node may perform on investigative progress.

- A clue carries its own point value and class tags. There is no separate point award.
- **Every clue is worth 1 point.** Point totals are derived from the held clue set and are never stored as mutable state. No document may increment or decrement a total.
- **Clue acquisition is idempotent.** `GRANT_CLUE` on an already-held clue is a no-op with respect to points and classes. A clue reachable through several routes awards its value exactly once.
- `GRANT_CLUE` writes to the acting player's private knowledge set. A joint-scene node writes to `SHARED_KNOWLEDGE_SET`. Regroup nodes `EVT_150` and `EVT_300` move clues from private sets into the shared set.
- A conclusion evaluator reads the union of `SHARED_KNOWLEDGE_SET` and the evaluating player's private set.

A clue may support multiple conclusions. `CLUE_PHOTO_WINDOW_MARKS` belongs to both § 4 and § 11: it is one clue contributing one point to each group, not two clues.

Class tags are drawn from the closed set owned by `07_EVIDENCE_VALIDATION.md` § 1. A multi-class tag records which classes a clue is eligible to fill; under the counting rule in that section a clue contributes exactly one class to any diversity count.

`Status` is `ACTIVE` where at least one node grants the clue, and `DEFINITION_ONLY` where no node grants it yet.

## 2. Staged disappearance

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_APT_BLOOD_OLD` | `PHYSICAL` | 1 | `EVT_113` | `ACTIVE` |
| `CLUE_APT_MEDICATION_MISSING` | `PHYSICAL`, `CONTEXTUAL` | 1 | `EVT_113` | `ACTIVE` |
| `CLUE_APT_PASSPORT_MISSING` | `PHYSICAL`, `CONTEXTUAL` | 1 | `EVT_113` | `ACTIVE` |
| `CLUE_APT_SERVICE_LATCH` | `PHYSICAL` | 1 | `EVT_115` | `ACTIVE` |
| `CLUE_APT_TIMED_DEVICE` | `PHYSICAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_NEIGHBOUR_EXIT_BEFORE_CRASH` | `TESTIMONIAL` | 1 | `EVT_114` | `ACTIVE` |
| `CLUE_NADIA_PLAN_ADMISSION` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |

**Group maximum:** 7.

### Deduction

`CON_STAGED_DISAPPEARANCE`

Requires either:

- 3 points and at least 2 distinct classes; or
- `CLUE_NADIA_PLAN_ADMISSION` plus one corroborating `PHYSICAL` clue.

### Gates unlocked

- challenge official abduction narrative;
- raise Mina trust;
- pressure Nadia toward fuller disclosure;
- reduce credibility of Rook's immediate framing.

---

## 3. Harbor destination

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_TRANSIT_HARBOR_STOP` | `PROCEDURAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_CAFE_TIDE_NOTE` | `PHYSICAL` | 1 | `EVT_211` | `ACTIVE` |
| `CLUE_CAFE_OLD_LINE_QUESTION` | `TESTIMONIAL` | 1 | `EVT_211` | `ACTIVE` |
| `CLUE_CAFE_FOOTAGE` | `DIGITAL` | 1 | `EVT_211` | `ACTIVE` |
| `CLUE_NADIA_HARBOR_RESEARCH` | `TESTIMONIAL`, `CONTEXTUAL` | 1 | `EVT_121` | `ACTIVE` |
| `CLUE_IRIS_DIRECTION_HARBOR` | `TESTIMONIAL`, `PROCEDURAL` | 1 | `EVT_230` | `ACTIVE` |

**Group maximum:** 6.

### Deduction

`CON_HARBOR_DESTINATION`

Requires 3 points and at least 2 distinct classes.

### Gates unlocked

- terminal reconnaissance;
- harbor archive relevance;
- targeted search rather than city-wide search.

---

## 4. Signal Room 4B

### Identifier clues

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_PHOTO_WINDOW_MARKS` | `PHYSICAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_ARCHIVE_ROOM_INDEX` | `PROCEDURAL` | 1 | `EVT_210` | `ACTIVE` |
| `CLUE_ELIAS_FRAGMENT_4B` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_LENA_ROOM_DISCLOSURE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_IRIS_ROOM_DISCLOSURE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |

### Route clues

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_CABLE_CORRIDOR_MAP` | `PHYSICAL` | 1 | `EVT_210` | `ACTIVE` |
| `CLUE_NORTH_GATE_RECORD` | `PROCEDURAL` | 1 | `EVT_311` | `ACTIVE` |
| `CLUE_DRAINAGE_TIDE_WINDOW` | `CONTEXTUAL` | 1 | `EVT_312` | `ACTIVE` |
| `CLUE_EMERGENCY_ENTRY_AUTH` | `PROCEDURAL` | 1 | `EVT_313` | `ACTIVE` |
| `CLUE_GENERATOR_TRACE` | `PHYSICAL` | 1 | `EVT_212` | `ACTIVE` |

**Group maximum:** 10, being 5 identifier and 5 route.

### Deduction and gate

`CON_SIGNAL_4B`

Requires:

- at least 1 point from the identifier clues; and
- at least 1 point from the route clues.

Class diversity is not required. The gate is structural, because an identifier without a route and a route without an identifier are each insufficient regardless of class.

Late failsafe:

- two strong terminal-local traces plus generator/cable logic may substitute for an explicit identifier, but costs 20 additional minutes and increases hostile-arrival risk.

---

## 5. Lena's role

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_ELIAS_ARRIVED_BEFORE_LENA` | `PROCEDURAL` | 1 | `EVT_231` | `ACTIVE` |
| `CLUE_LENA_CALLED_IRIS_AFTER_INJURY` | `PROCEDURAL`, `DIGITAL` | 1 | `EVT_231` | `ACTIVE` |
| `CLUE_MEDICAL_SUPPLY_TRAIL` | `PHYSICAL` | 1 | `EVT_212`, `EVT_230` | `ACTIVE` |
| `CLUE_REED_CONFRONTATION_ADMISSION` | `TESTIMONIAL` | 1 | `EVT_243` | `ACTIVE` |
| `CLUE_LENA_VERIFIABLE_FALL_DETAIL` | `TESTIMONIAL`, `BEHAVIOURAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_NO_RANSOM_OR_DEMAND` | `BEHAVIOURAL` | 1 | none | `DEFINITION_ONLY` |

**Group maximum:** 6.

### Deduction

`CON_LENA_PROTECTING`

Requires 3 points and at least 2 distinct classes drawn from `TESTIMONIAL`, `PROCEDURAL` and `BEHAVIOURAL`.

This deduction does not declare Lena legally innocent. It establishes that “kidnapper” is an incomplete and misleading model.

---

## 6. Reed's presence

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_REED_DECOY_KEY` | `PHYSICAL` | 1 | `EVT_242` | `ACTIVE` |
| `CLUE_REED_HARBOR_RESIDUE` | `PHYSICAL` | 1 | `EVT_242` | `ACTIVE` |
| `CLUE_REED_BLOOD_TRACE` | `PHYSICAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_KRELL_RECOVERY_MESSAGE` | `DIGITAL` | 1 | `EVT_242` | `ACTIVE` |
| `CLUE_TERMINAL_ACCESS_TRACE` | `PHYSICAL` | 1 | `EVT_212` | `ACTIVE` |
| `CLUE_LENA_OR_IRIS_TESTIMONY` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_REED_PARTIAL_ADMISSION` | `TESTIMONIAL` | 1 | `EVT_243` | `ACTIVE` |

**Group maximum:** 7.

### Deduction

`CON_REED_PRESENT`

Requires 2 points, of which at least 1 is from a clue not tagged `TESTIMONIAL`.

### Stronger deduction

`CON_REED_CAUSED_CONFRONTATION`

Requires:

- `CON_REED_PRESENT`;
- 1 further point from a `PHYSICAL` or `TESTIMONIAL` account of the struggle;
- no contradictory evidence of deliberate planned killing.

---

## 7. Marcus leak

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_MARCUS_ACCOUNT_ACCESS` | `PROCEDURAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_MARCUS_DELETED_CALL` | `DIGITAL`, `PROCEDURAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_CARRIER_CALL_RECORD` | `PROCEDURAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_PAYMENT_RECORD` | `PROCEDURAL`, `CONTEXTUAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_INTERMEDIARY_VOICEMAIL` | `DIGITAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_REED_SOURCE_REFERENCE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_MARCUS_CONFESSION` | `TESTIMONIAL` | 1 | `EVT_241` | `ACTIVE` |

**Group maximum:** 7.

### Deductions

`CON_MARCUS_LEAK_PARTIAL`

- 2 points.

`CON_MARCUS_LEAK_PROVABLE`

- 3 points;
- at least 2 distinct classes.

### Narrative resolution requirement

If the leak is exposed, the player-facing ending must clarify that Marcus transmitted partial operational information, not the exact room or complete conspiracy design.

---

## 8. Rook compromised

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_ROOK_CAMERA_UNAUTHORIZED` | `PROCEDURAL` | 1 | `EVT_221` | `ACTIVE` |
| `CLUE_ROOK_REPORT_ALTERED` | `PROCEDURAL`, `DIGITAL` | 1 | `EVT_220` | `ACTIVE` |
| `CLUE_ROOK_PROTECTION_ORDER_FALSE` | `PROCEDURAL` | 1 | `EVT_222` | `ACTIVE` |
| `CLUE_ROOK_KRELL_CONTACT` | `DIGITAL`, `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_ROOK_LENA_BULLETIN_FALSE` | `PROCEDURAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_REED_NAMES_ROOK_LINK` | `TESTIMONIAL` | 1 | `EVT_243` | `ACTIVE` |
| `CLUE_MINA_AUTHENTICATES_REPORT` | `TESTIMONIAL`, `PROCEDURAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_EVIDENCE_ROOM_PHOTO_PATH` | `PROCEDURAL` | 1 | none | `DEFINITION_ONLY` |

**Group maximum:** 8.

### Deductions

`CON_ROOK_OPERATIONALLY_COMPROMISED`

- 3 points;
- at least 1 point from a clue tagged `PROCEDURAL`.

`CON_ROOK_PUBLICLY_PROVABLE`

- 4 points;
- at least 3 distinct classes, or preserved direct-contact evidence;
- at least one `AUTHENTICATED` or `PRESERVED_COPY` record under § 4 of `07_EVIDENCE_VALIDATION.md`.

### Gates

- trusted rescue planning;
- Rook accusation option;
- Mina intervention;
- public-exposure route.

---

## 9. Medical emergency

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_IRIS_SUPPLY_SELECTION` | `PHYSICAL` | 1 | `EVT_230` | `ACTIVE` |
| `CLUE_IRIS_ASSESSMENT` | `TESTIMONIAL` | 1 | `EVT_232` | `ACTIVE` |
| `CLUE_ELIAS_VOMITING_CONFUSION` | `BEHAVIOURAL` | 1 | `EVT_330` | `ACTIVE` |
| `CLUE_ELIAS_UNEQUAL_PUPILS` | `PHYSICAL` | 1 | `EVT_330` | `ACTIVE` |
| `CLUE_MEDICAL_REFERENCE` | `CONTEXTUAL` | 1 | `EVT_232` | `ACTIVE` |

**Group maximum:** 5.

### Deduction

`CON_MEDICAL_EMERGENCY`

- 2 points before discovery;
- automatic on entering `EVT_330`, which sets `P_MEDICAL` to its threshold directly.

### Gate

Unlocks rescue-priority decisions and prevents the narrative from treating further delay as harmless.

---

## 10. Primary vs decoy ledger

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_DECOY_LIMITED_CONTENT` | `DIGITAL` | 1 | `EVT_242` | `ACTIVE` |
| `CLUE_DECOY_TRACKER` | `DIGITAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_ELIAS_FRAGMENT_BLACK_FALSE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_HASH_MISMATCH` | `DIGITAL` | 1 | `EVT_410` | `ACTIVE` |
| `CLUE_NADIA_DECOY_KNOWLEDGE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |

**Group maximum:** 5.

### Deduction

`CON_DECOY_KEY`

- 2 points, unless `CLUE_DECOY_TRACKER` and `CLUE_DECOY_LIMITED_CONTENT` are both held, which satisfies the gate on its own.

### Gate

Prevents complete-transfer option from accepting the wrong hardware key.

---

## 11. Recovery code

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_NADIA_FIRST_THREE` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_PHOTO_WINDOW_MARKS` | `PHYSICAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_ARCHIVE_WINDOW_NUMBERING` | `PROCEDURAL` | 1 | `EVT_210` | `ACTIVE` |
| `CLUE_ELIAS_FRAGMENT_WINDOWS` | `TESTIMONIAL` | 1 | none | `DEFINITION_ONLY` |
| `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` | `DIGITAL` | 1 | `EVT_123` | `ACTIVE` |

**Group maximum:** 5. `CLUE_PHOTO_WINDOW_MARKS` is also a § 4 identifier clue and contributes one point to each group.

### Deduction

`CON_WINDOW_CODE`

Requires:

- 1 point from `CLUE_NADIA_FIRST_THREE` or `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS`; and
- 1 point from `CLUE_PHOTO_WINDOW_MARKS` or `CLUE_ARCHIVE_WINDOW_NUMBERING` or `CLUE_ELIAS_FRAGMENT_WINDOWS`.

### Fallback

If Nadia remains hostile, players may preserve the primary key and achieve rescue or partial-evidence endings without a complete transfer.

---

## 11a. Passphrase access

| Clue | Classes | Points | Granting nodes | Status |
|---|---|---:|---|---|
| `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` | `DIGITAL` | 1 | `EVT_123` | `ACTIVE` |
| `CLUE_ELIAS_FRAGMENT_PASSPHRASE` | `TESTIMONIAL` | 1 | `EVT_330` | `ACTIVE` |

**Group maximum:** 2. `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` is also a § 11 clue and contributes one point to each group.

### Deduction

`CON_PASSPHRASE_ACCESS`

Requires 1 point. The two routes are not equivalent in quality:

- **Route A**, `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS`, unlocks the documented recovery procedure. It does not reveal the passphrase. With the hardware key present and the complete recovery code entered, it permits a reset in place of entry. The reset costs 20 minutes and is logged, which downgrades authentication, so it reaches partial official evidence and never full authenticated transfer. It is granted at `EVT_123`, a Player 2 opening node in the 20:10-20:25 window, so it is available before discovery and well before 01:00.
- **Route B**, `CLUE_ELIAS_FRAGMENT_PASSPHRASE`, is the passphrase itself, stated by Elias as a fragment. It is available from discovery until `ELIAS_STATE` reaches `CRITICAL_UNRESPONSIVE` at 01:00. It preserves authentication and is the only route to full authenticated transfer.

Route B is post-discovery, which is not circular for this conclusion. The passphrase is needed only once the primary key is held, and the primary key is inside Signal Room 4B by `01_WORLD_BIBLE.md` § 14. A route that unlocks at room discovery therefore cannot gate the thing that reaches it.

The routes share no granting node, no source actor and no location: Route A comes from Nadia's upload at `LOC_NEWSROOM` via `EVT_123`, Route B from Elias at `LOC_SIGNAL_4B` via `EVT_330`.

### Failure transformation

Neither route obtained means the archive never opens. This does not deadlock. It routes to "Evidence lost" or "Public leak" in `14_ENDING_TRIGGER_MATRIX.md` § 3, depending on whether an external copy exists.

---

## 12. Critical-route audit

Independent routes counts the clues in each group that at least one node grants. `DEFINITION_ONLY` clues are excluded, because a clue no node grants is not a route.

| Critical objective | Group maximum | Routes with a granting node | Threshold | Satisfiable |
|---|---:|---:|---|---|
| infer staging | 7 | 5 | 3 points, 2 classes | Yes |
| identify harbor | 6 | 5 | 3 points, 2 classes | Yes |
| identify room | 10 | 7, being 2 identifier and 5 route | 1 identifier, 1 route | Yes |
| identify Lena's role | 6 | 4 | 3 points, 2 classes | Yes |
| identify Reed | 7 | 5 | 2 points, 1 non-testimonial | Yes |
| provable Marcus leak | 7 | 3 | 3 points, 2 classes | Yes |
| challenge Rook privately | 8 | 4 | 3 points, 1 procedural | Yes |
| challenge Rook publicly | 8 | 4 | 4 points, 3 classes | Yes |
| recognize medical danger | 5 | 5 | 2 points | Yes |
| distinguish decoy | 5 | 2 | 2 points | Yes |
| complete code | 5 | 3 | 1 fragment, 1 interpretation | Yes |
| open the primary archive | 2 | 2 | 1 point | Yes, 2 independent routes |

No single locked container, technical check, or NPC confession is a mandatory single point of failure.

---

## 13. Identifier status

Every `CLUE_` identifier declared in this document carries exactly one status, recorded in its group table. `ACTIVE` means at least one node grants the clue. `DEFINITION_ONLY` means no node grants it yet.

| Status | Count |
|---|---:|
| `ACTIVE` | 43 |
| `DEFINITION_ONLY` | 23 |

No clue identifier is `RESERVED` or `DEPRECATED`.

Sixty-six distinct identifiers appear across sixty-eight listings. Total available points across all groups is 68, because `CLUE_PHOTO_WINDOW_MARKS` contributes one point to each of §§ 4 and 11, and `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS` one point to each of §§ 11 and 11a.

# DO NOT READ: Clue Dependency Graph

## 1. Notation

- `C:` clue
- `D:` deduction
- `G:` gameplay gate
- `E:` ending proof

A clue may support multiple deductions. A deduction becomes available only when its threshold and class requirements are satisfied.

## 2. Staged disappearance

### Clues

- `CLUE_APT_BLOOD_OLD` — physical
- `CLUE_APT_MEDICATION_MISSING` — physical/contextual
- `CLUE_APT_PASSPORT_MISSING` — physical/contextual
- `CLUE_APT_SERVICE_LATCH` — physical
- `CLUE_APT_TIMED_DEVICE` — physical/technical
- `CLUE_NEIGHBOUR_EXIT_BEFORE_CRASH` — testimonial
- `CLUE_NADIA_PLAN_ADMISSION` — testimonial

### Deduction

`CON_STAGED_DISAPPEARANCE`

Requires:

- 3 points;
- at least 2 clue classes;
- or Nadia admission plus one corroborating physical clue.

### Gates unlocked

- challenge official abduction narrative;
- raise Mina trust;
- pressure Nadia toward fuller disclosure;
- reduce credibility of Rook's immediate framing.

---

## 3. Harbor destination

### Clues

- `CLUE_TRANSIT_HARBOR_STOP` — procedural
- `CLUE_CAFE_TIDE_NOTE` — physical
- `CLUE_CAFE_OLD_LINE_QUESTION` — testimonial
- `CLUE_CAFE_FOOTAGE` — digital
- `CLUE_NADIA_HARBOR_RESEARCH` — testimonial/contextual
- `CLUE_IRIS_DIRECTION_HARBOR` — testimonial/procedural

### Deduction

`CON_HARBOR_DESTINATION`

Requires 3 points across 2 classes.

### Gates unlocked

- terminal reconnaissance;
- harbor archive relevance;
- targeted search rather than city-wide search.

---

## 4. Signal Room 4B

### Identifier clues

- `CLUE_PHOTO_WINDOW_MARKS`
- `CLUE_ARCHIVE_ROOM_INDEX`
- `CLUE_ELIAS_FRAGMENT_4B`
- `CLUE_LENA_ROOM_DISCLOSURE`
- `CLUE_IRIS_ROOM_DISCLOSURE`

### Route clues

- `CLUE_CABLE_CORRIDOR_MAP`
- `CLUE_NORTH_GATE_RECORD`
- `CLUE_DRAINAGE_TIDE_WINDOW`
- `CLUE_EMERGENCY_ENTRY_AUTH`
- `CLUE_GENERATOR_TRACE`

### Deduction and gate

`CON_SIGNAL_4B` requires:

- one identifier clue;
- one route clue.

Late failsafe:

- two strong terminal-local traces plus generator/cable logic may substitute for an explicit identifier, but costs 20 additional minutes and increases hostile-arrival risk.

---

## 5. Lena's role

### Clues

- `CLUE_ELIAS_ARRIVED_BEFORE_LENA`
- `CLUE_LENA_CALLED_IRIS_AFTER_INJURY`
- `CLUE_MEDICAL_SUPPLY_TRAIL`
- `CLUE_REED_CONFRONTATION_ADMISSION`
- `CLUE_LENA_VERIFIABLE_FALL_DETAIL`
- `CLUE_NO_RANSOM_OR_DEMAND`

### Deduction

`CON_LENA_PROTECTING`

Requires 3 points across testimonial/procedural/behavioural classes.

This deduction does not declare Lena legally innocent. It establishes that “kidnapper” is an incomplete and misleading model.

---

## 6. Reed's presence

### Clues

- `CLUE_REED_DECOY_KEY`
- `CLUE_REED_HARBOR_RESIDUE`
- `CLUE_REED_BLOOD_TRACE`
- `CLUE_KRELL_RECOVERY_MESSAGE`
- `CLUE_TERMINAL_ACCESS_TRACE`
- `CLUE_LENA_OR_IRIS_TESTIMONY`
- `CLUE_REED_PARTIAL_ADMISSION`

### Deduction

`CON_REED_PRESENT`

Requires two independent routes, at least one not purely testimonial.

### Stronger deduction

`CON_REED_CAUSED_CONFRONTATION`

Requires:

- presence;
- physical or testimonial account of struggle;
- no contradictory evidence of deliberate planned killing.

---

## 7. Marcus leak

### Clues

- `CLUE_MARCUS_ACCOUNT_ACCESS`
- `CLUE_MARCUS_DELETED_CALL`
- `CLUE_CARRIER_CALL_RECORD`
- `CLUE_PAYMENT_RECORD`
- `CLUE_INTERMEDIARY_VOICEMAIL`
- `CLUE_REED_SOURCE_REFERENCE`
- `CLUE_MARCUS_CONFESSION`

### Deduction

`CON_MARCUS_LEAK_PARTIAL` at 2 points.

`CON_MARCUS_LEAK_PROVABLE` at 3 points, 2 classes.

### Narrative resolution requirement

If the leak is exposed, the player-facing ending must clarify that Marcus transmitted partial operational information, not the exact room or complete conspiracy design.

---

## 8. Rook compromised

### Clues

- `CLUE_ROOK_CAMERA_UNAUTHORIZED` — procedural
- `CLUE_ROOK_REPORT_ALTERED` — procedural/digital
- `CLUE_ROOK_PROTECTION_ORDER_FALSE` — procedural
- `CLUE_ROOK_KRELL_CONTACT` — digital/testimonial
- `CLUE_ROOK_LENA_BULLETIN_FALSE` — procedural
- `CLUE_REED_NAMES_ROOK_LINK` — testimonial
- `CLUE_MINA_AUTHENTICATES_REPORT` — testimonial/procedural
- `CLUE_EVIDENCE_ROOM_PHOTO_PATH` — procedural

### Deductions

`CON_ROOK_OPERATIONALLY_COMPROMISED`

- threshold 3;
- must include one procedural clue.

`CON_ROOK_PUBLICLY_PROVABLE`

- threshold 4;
- at least 3 classes or preserved direct-contact evidence;
- at least one authenticated/preserved copy.

### Gates

- trusted rescue planning;
- Rook accusation option;
- Mina intervention;
- public-exposure route.

---

## 9. Medical emergency

### Clues

- `CLUE_IRIS_SUPPLY_SELECTION`
- `CLUE_IRIS_ASSESSMENT`
- `CLUE_ELIAS_VOMITING_CONFUSION`
- `CLUE_ELIAS_UNEQUAL_PUPILS`
- `CLUE_MEDICAL_REFERENCE`

### Deduction

`CON_MEDICAL_EMERGENCY`

- 2 points before discovery;
- automatic after observing definitive late symptoms.

### Gate

Unlocks rescue-priority decisions and prevents the narrative from treating further delay as harmless.

---

## 10. Primary vs decoy ledger

### Clues

- `CLUE_DECOY_LIMITED_CONTENT`
- `CLUE_DECOY_TRACKER`
- `CLUE_ELIAS_FRAGMENT_BLACK_FALSE`
- `CLUE_HASH_MISMATCH`
- `CLUE_NADIA_DECOY_KNOWLEDGE`

### Deduction

`CON_DECOY_KEY`

Requires two routes, unless tracker and content mismatch are directly observed together.

### Gate

Prevents complete-transfer option from accepting the wrong hardware key.

---

## 11. Recovery code

### Clues

- `CLUE_NADIA_FIRST_THREE`
- `CLUE_PHOTO_WINDOW_MARKS`
- `CLUE_ARCHIVE_WINDOW_NUMBERING`
- `CLUE_ELIAS_FRAGMENT_WINDOWS`
- `CLUE_UPLOAD_RECOVERY_INSTRUCTIONS`

### Deduction

`CON_WINDOW_CODE`

Requires:

- Nadia fragment or upload instructions;
- photo/window interpretation route.

### Fallback

If Nadia remains hostile, players may preserve the primary key and achieve rescue or partial-evidence endings without a complete transfer.

---

## 12. Critical-route audit

| Critical objective | Independent routes |
|---|---:|
| infer staging | 4+ |
| identify harbor | 4+ |
| identify room | 5 identifier / 5 route |
| identify Reed | 5+ |
| challenge Rook | 6+ |
| recognize medical danger | 4+ |
| distinguish decoy | 4+ |
| complete code | 4+ |

No single locked container, technical check, or NPC confession is a mandatory single point of failure.

---

## 13. Identifier status

Every `CLUE_` identifier declared in this document carries exactly one status. Status is derived from reference count: an identifier referenced somewhere other than its own declaring row is `ACTIVE`; an identifier that appears only in its declaring row is `DEFINITION_ONLY`.

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` | 1 | `CLUE_PHOTO_WINDOW_MARKS`, declared in § 4 and referenced again in § 11. It is one clue contributing to two conclusion groups, not two clues. |
| `DEFINITION_ONLY` | 64 | Every other clue identifier declared in §§ 2–11. |

No clue identifier is `RESERVED` or `DEPRECATED`.

Sixty-five distinct identifiers appear across sixty-six listings. The sixty-four `DEFINITION_ONLY` clues are declared and not yet referenced because no node grants a clue yet; that changes when clue grants are authored.

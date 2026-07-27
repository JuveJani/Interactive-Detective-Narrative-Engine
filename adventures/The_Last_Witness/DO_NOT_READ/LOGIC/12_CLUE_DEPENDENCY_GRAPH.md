# DO NOT READ: Clue Dependency Graph

## 1. Notation

- `C:` clue
- `D:` deduction
- `G:` gameplay gate
- `E:` ending proof

A clue may support multiple deductions. A deduction becomes available only when its threshold and class requirements are satisfied.

## 2. Staged disappearance

### Clues

- `C_APT_BLOOD_OLD` — physical
- `C_APT_MEDICATION_MISSING` — physical/contextual
- `C_APT_PASSPORT_MISSING` — physical/contextual
- `C_APT_SERVICE_LATCH` — physical
- `C_APT_TIMED_DEVICE` — physical/technical
- `C_NEIGHBOUR_EXIT_BEFORE_CRASH` — testimonial
- `C_NADIA_PLAN_ADMISSION` — testimonial

### Deduction

`D_STAGED_DISAPPEARANCE`

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

- `C_TRANSIT_HARBOR_STOP` — procedural
- `C_CAFE_TIDE_NOTE` — physical
- `C_CAFE_OLD_LINE_QUESTION` — testimonial
- `C_CAFE_FOOTAGE` — digital
- `C_NADIA_HARBOR_RESEARCH` — testimonial/contextual
- `C_IRIS_DIRECTION_HARBOR` — testimonial/procedural

### Deduction

`D_HARBOR_DESTINATION`

Requires 3 points across 2 classes.

### Gates unlocked

- terminal reconnaissance;
- harbor archive relevance;
- targeted search rather than city-wide search.

---

## 4. Signal Room 4B

### Identifier clues

- `C_PHOTO_WINDOW_MARKS`
- `C_ARCHIVE_ROOM_INDEX`
- `C_ELIAS_FRAGMENT_4B`
- `C_LENA_ROOM_DISCLOSURE`
- `C_IRIS_ROOM_DISCLOSURE`

### Route clues

- `C_CABLE_CORRIDOR_MAP`
- `C_NORTH_GATE_RECORD`
- `C_DRAINAGE_TIDE_WINDOW`
- `C_EMERGENCY_ENTRY_AUTH`
- `C_GENERATOR_TRACE`

### Deduction and gate

`D_SIGNAL_4B` requires:

- one identifier clue;
- one route clue.

Late failsafe:

- two strong terminal-local traces plus generator/cable logic may substitute for an explicit identifier, but costs 20 additional minutes and increases hostile-arrival risk.

---

## 5. Lena's role

### Clues

- `C_ELIAS_ARRIVED_BEFORE_LENA`
- `C_LENA_CALLED_IRIS_AFTER_INJURY`
- `C_MEDICAL_SUPPLY_TRAIL`
- `C_REED_CONFRONTATION_ADMISSION`
- `C_LENA_VERIFIABLE_FALL_DETAIL`
- `C_NO_RANSOM_OR_DEMAND`

### Deduction

`D_LENA_PROTECTING`

Requires 3 points across testimonial/procedural/behavioural classes.

This deduction does not declare Lena legally innocent. It establishes that “kidnapper” is an incomplete and misleading model.

---

## 6. Reed's presence

### Clues

- `C_REED_DECOY_KEY`
- `C_REED_HARBOR_RESIDUE`
- `C_REED_BLOOD_TRACE`
- `C_KRELL_RECOVERY_MESSAGE`
- `C_TERMINAL_ACCESS_TRACE`
- `C_LENA_OR_IRIS_TESTIMONY`
- `C_REED_PARTIAL_ADMISSION`

### Deduction

`D_REED_PRESENT`

Requires two independent routes, at least one not purely testimonial.

### Stronger deduction

`D_REED_CAUSED_CONFRONTATION`

Requires:

- presence;
- physical or testimonial account of struggle;
- no contradictory evidence of deliberate planned killing.

---

## 7. Marcus leak

### Clues

- `C_MARCUS_ACCOUNT_ACCESS`
- `C_MARCUS_DELETED_CALL`
- `C_CARRIER_CALL_RECORD`
- `C_PAYMENT_RECORD`
- `C_INTERMEDIARY_VOICEMAIL`
- `C_REED_SOURCE_REFERENCE`
- `C_MARCUS_CONFESSION`

### Deduction

`D_MARCUS_LEAK_PARTIAL` at 2 points.

`D_MARCUS_LEAK_PROVABLE` at 3 points, 2 classes.

### Narrative resolution requirement

If the leak is exposed, the player-facing ending must clarify that Marcus transmitted partial operational information, not the exact room or complete conspiracy design.

---

## 8. Rook compromised

### Clues

- `C_ROOK_CAMERA_UNAUTHORIZED` — procedural
- `C_ROOK_REPORT_ALTERED` — procedural/digital
- `C_ROOK_PROTECTION_ORDER_FALSE` — procedural
- `C_ROOK_KRELL_CONTACT` — digital/testimonial
- `C_ROOK_LENA_BULLETIN_FALSE` — procedural
- `C_REED_NAMES_ROOK_LINK` — testimonial
- `C_MINA_AUTHENTICATES_REPORT` — testimonial/procedural
- `C_EVIDENCE_ROOM_PHOTO_PATH` — procedural

### Deductions

`D_ROOK_OPERATIONALLY_COMPROMISED`

- threshold 3;
- must include one procedural clue.

`D_ROOK_PUBLICLY_PROVABLE`

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

- `C_IRIS_SUPPLY_SELECTION`
- `C_IRIS_ASSESSMENT`
- `C_ELIAS_VOMITING_CONFUSION`
- `C_ELIAS_UNEQUAL_PUPILS`
- `C_MEDICAL_REFERENCE`

### Deduction

`D_MEDICAL_EMERGENCY`

- 2 points before discovery;
- automatic after observing definitive late symptoms.

### Gate

Unlocks rescue-priority decisions and prevents the narrative from treating further delay as harmless.

---

## 10. Primary vs decoy ledger

### Clues

- `C_DECOY_LIMITED_CONTENT`
- `C_DECOY_TRACKER`
- `C_ELIAS_FRAGMENT_BLACK_FALSE`
- `C_HASH_MISMATCH`
- `C_NADIA_DECOY_KNOWLEDGE`

### Deduction

`D_DECOY_KEY`

Requires two routes, unless tracker and content mismatch are directly observed together.

### Gate

Prevents complete-transfer option from accepting the wrong hardware key.

---

## 11. Recovery code

### Clues

- `C_NADIA_FIRST_THREE`
- `C_PHOTO_WINDOW_MARKS`
- `C_ARCHIVE_WINDOW_NUMBERING`
- `C_ELIAS_FRAGMENT_WINDOWS`
- `C_UPLOAD_RECOVERY_INSTRUCTIONS`

### Deduction

`D_WINDOW_CODE`

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

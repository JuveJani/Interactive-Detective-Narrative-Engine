# Single Investigator Mode — Normative Specification

**Document type:** Engine companion (Milestone 1)  
**Status:** Normative for `single_investigator` play mode  
**Aligned with:** `IDNE_ENGINE_v0.4.md` §0.5, §5.4.1, §6.8; `IDNE_DESIGN_PHILOSOPHY.md` A5, A7, A9  
**Validation:** `IDNE_ADVENTURE_QA_SPEC.md` §5.11; `python3 -m idne.single_investigator_validate`

---

## 1. Purpose

Single Investigator Mode is the canonical **one real player** play mode for IDNE adventures.

It is **not** a two-player adventure with Player 2 removed. It defines one investigator, one knowledge state, one inventory, one world clock, player-directed navigation, and ending evaluation for a solo session.

Two-player mode (`two_player`) remains unchanged. An adventure supports solo play only when it **declares** and **validates** `single_investigator`.

---

## 2. Play mode declaration

Every adventure MUST declare supported modes in `play_manifest.json` at the adventure root.

```json
{
  "schema_version": "1.0",
  "adventure_id": "EXAMPLE",
  "play_modes": ["single_investigator"],
  "single_investigator": {
    "character_sheet": "PLAYER/CHARACTERS/CHARACTER_SHEET.md",
    "record_sheet": "PLAYER/SHARED/CASE_FILE.md",
    "scene_package": "PLAYER/INVESTIGATION_SCENES.md",
    "navigation_index": "PLAYER/NAVIGATION_INDEX.md",
    "endings": "PLAYER/ENDINGS.md",
    "inventory_owner": "investigator",
    "clock_model": "single_sequential",
    "wall_clock_target_minutes": 90,
    "start_scene": "J-100"
  }
}
```

| Field | Requirement |
|---|---|
| `play_modes` | Non-empty list of `single_investigator` and/or `two_player` only |
| `single_investigator.*` | Required when `single_investigator` is listed |
| `inventory_owner` | MUST be `investigator` |
| `clock_model` | MUST be `single_sequential` or `single_world_clock` |
| `wall_clock_target_minutes` | REQUIRED positive integer — solo wall-clock target |
| `start_scene` | OPTIONAL; default first scene code in scene package |

**MUST NOT:** Infer solo support from file layout or from a `two_player` package alone.

**MAY:** Declare both modes when `two_player` routing (role booklets, split flow) and `single_investigator` routing (unified scene package) are each complete and validated.

Dual-mode manifest MUST also include a `two_player` block with `people_booklet`, `records_booklet`, and related routing paths.

---

## 3. Investigator model

| Dimension | Single investigator rule |
|---|---|
| Player characters | Exactly one investigator character |
| Knowledge state | One sheet-backed knowledge state on `record_sheet` |
| Private booklets | **MUST NOT** use `BOOKLET_PEOPLE.md`, `BOOKLET_RECORDS.md`, or role-private scene codes (`P-*`, `R-*`) in the solo scene package |
| Split / regroup | **MUST NOT** use split windows, regroup scenes, wait-for-partner, or parallel role paths |
| Role balance | Not applicable — no role-balance requirement |
| Communication cost while split | Not applicable |

The investigator performs all checks, holds all inventory, and records all clues on the shared case file.

---

## 4. Scene eligibility

### 4.1 Solo scene package

Solo adventures use a **single unified scene package** (`scene_package`), typically `PLAYER/INVESTIGATION_SCENES.md`.

Every playable unit in that package:

- MUST be reachable by one investigator following legal navigation (no role gate).
- MUST NOT require a second player's private knowledge to understand or continue.
- MUST NOT be split-only or regroup-only (no "wait until your partner returns").
- MAY use Joint-style scene codes (e.g. `J-*`) as generic investigation units; role prefixes `P-*` / `R-*` are forbidden in the solo package.

### 4.2 Navigation

`navigation_index` MUST describe complete one-player routing among authored locations and scene entry points.

**MUST NOT** reference two-player private booklets or split/regroup procedures as mandatory steps.

Player-directed investigation (Philosophy A5): hubs offer distinct investigative actions with time cost; the player chooses order within authored availability.

---

## 5. Time model

### 5.1 World clock

One shared world clock (Engine §5.1). All time advances apply to the single investigator session.

`clock_model` values:

| Value | Meaning |
|---|---|
| `single_sequential` | Scene estimates sum along the investigator's path (default) |
| `single_world_clock` | Same clock semantics; adventure documents threshold gates on one timeline |

**MUST NOT:** Use cooperative split-window timing or `max(role_A, role_B)` parallel-time calculation.

### 5.2 Wall-clock playtime estimation

Use Engine §5.4.1:

```text
estimated_wall_clock =
    sum(sequential_scene_play_estimates_along_legal_paths)
  + endgame_estimate
```

Reports MUST state **longest legal path** separately.

Compilation reports for solo adventures MUST NOT use the two-player §5.4 formula.

---

## 6. Inventory

- One inventory owned by `investigator`.
- All takeable items, keys, and documents MUST be obtainable and spendable without a second role.
- **MUST NOT** require an item held only on an absent partner's sheet.

Manifest field `inventory_owner` MUST be `investigator`. Item gates in scene text MUST reference fields on the solo character or case file.

---

## 7. Checks

Checks use the same **fixed-world** principle (Engine §7): world state does not change because the player failed a roll; failure changes path, cost, or certainty.

- One investigator performs every check declared for solo play.
- Check outcomes MUST not assume a second player to retry, hold tools, or witness results.
- Failed checks MUST comply with U7 (Engine §1 U7): no silent erasure of the only fair solution unless a visible failure ending was intended.

---

## 8. Conclusions and Infer

- Infer steps and conclusion worksheets live on the solo `record_sheet` / character sheet.
- Conclusions MUST be based on information the one investigator can acquire and reason about.
- **MUST NOT** require clues granted only in an absent role's private booklet.
- **MUST NOT** require "compare with your partner's notes" as a mandatory Infer step.

Mandatory conclusions (culprit, method, motive, or adventure-defined proof tags) MUST be achievable on at least one valid solo path (QA-SI-CONCLUSIONS).

---

## 9. Ending evaluation

Endings file (`endings`) MUST evaluate against the solo investigator's sheet state only.

- **MUST NOT** depend on two-player-only flags (partner trust, split completion, role-specific worksheet sections).
- **MUST NOT** require both investigators to confirm accusation.
- Timeout, partial-success, and wrong-accusation endings MUST be reachable without a second player.

Ending prose MUST cite only facts obtainable on the ending's legal trigger set (QA-NV-05, QA-SI-ENDING).

---

## 10. Delivery Adapter requirements

When emitting `single_investigator` in `play_modes`, the Delivery Adapter MUST:

1. Produce all artifacts listed in §2 (character sheet, record sheet, scene package, navigation index, endings).
2. Omit role-private booklets from the solo PLAYER bundle (or exclude them from solo manifest paths).
3. Emit `play_manifest.json` with a complete `single_investigator` block.
4. Compile wall-clock estimate using §5.4.1 in the compilation report.
5. **MUST NOT** emit `single_investigator` unless solo validation prerequisites pass (or CI will FAIL).

For dual-mode adventures, emit **both** routing trees without cross-contaminating solo scenes with split-only units.

---

## 11. AI generation requirements

When generating a **single-investigator** adventure, the generator MUST produce:

| Artifact | Content |
|---|---|
| Adventure Brief | `play_modes: [single_investigator]`; solo wall-clock target; no split/regroup targets |
| World Bible + Logic | Fixed truth; proof graph with solo-reachable grants |
| Character sheet | One investigator — skills, limits, inventory slots |
| Record / case file | One knowledge state — clues, Infer, accusation fields |
| Scene package | Unified investigation scenes — hubs, locations, checks, Infer, accusation |
| Navigation index | Location and scene routing for one player |
| Inventory handling | All items on investigator inventory or case file |
| Checks | Declared costs, outcomes, sheet writers — solo performer |
| Conclusions | Infer gates and proof tags acquirable solo |
| Endings | Sheet-checkable triggers for one investigator |
| Playtime target | `wall_clock_target_minutes` + §5.4.1 compilation |
| `play_manifest.json` | Full declaration per §2 |
| Validation evidence | `single_investigator_validate` JSON + Adventure QA §5.11 |

**MUST NOT** generate solo by copying a two-player graph and deleting one booklet.

---

## 12. Validation summary

Mandatory checks are defined in `IDNE_ADVENTURE_QA_SPEC.md` §5.11.

Automated harness: `python3 -m idne.single_investigator_validate <adventure_root>`

| Result | Meaning |
|---|---|
| `SKIP` | No manifest or `single_investigator` not in `play_modes` — solo validation not applicable (not a PASS for solo) |
| `PASS` | All automated QA-SI checks passed |
| `FAIL` | Solo declared but package invalid |

**False PASS guard:** Declaring `single_investigator` while only two-player booklets exist MUST FAIL (QA-SI-NO-FALSE-PASS).

Two-player-only adventures (e.g. Harborview without manifest) return `SKIP` — they are **not** solo-compatible by default.

---

## 13. Relationship to two-player mode

| Topic | Two-player | Single investigator |
|---|---|---|
| Scene modes | Joint / Split / optional Solo | Investigation units only — no Split |
| Private knowledge | Role booklets | None |
| Wall-clock formula | §5.4 split windows | §5.4.1 sequential sum |
| Role balance | QA-RC-01–03 | N/A |
| Solo-solve blocked | QA-RC-04 (must NOT be solo-solvable accidentally) | N/A — solo is intentional |
| Cooperation QA | Required | N/A when solo-only |

When both modes are declared, run full two-player QA plus full §5.11 solo QA.

---

## 14. Out of scope (Milestone 1)

- New clue, puzzle, environment, retry, or object systems
- Mystery model redesign
- Converting existing two-player adventures to solo
- Full logic-graph CI for every conclusion path (partial automation + Tier B review)
- Digital DM runtime

See `SINGLE_INVESTIGATOR_MODE_MIGRATION.md` for adoption guidance.

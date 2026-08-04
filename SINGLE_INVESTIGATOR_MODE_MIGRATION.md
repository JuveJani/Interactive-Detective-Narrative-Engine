# Single Investigator Mode — Migration Guide

**Audience:** Adventure authors, generators, QA operators  
**Status:** Milestone 1 adoption guide  
**See also:** `SINGLE_INVESTIGATOR_MODE_SPEC.md`, `IDNE_ENGINE_v0.4.md` §6.8

---

## 1. What changes for new adventures

### 1.1 Declaration is mandatory for solo

New adventures intended for one player MUST:

1. Set `play_modes` to include `single_investigator` in `play_manifest.json`.
2. Provide a complete `single_investigator` routing block (see spec §2).
3. Ship a **unified solo scene package** — not a truncated two-player booklet set.
4. Pass `python3 -m idne.single_investigator_validate` and Adventure QA §5.11.
5. Use wall-clock formula §5.4.1 in compilation reports.

### 1.2 PLAYER layout for solo

| Artifact | Solo adventure | Two-player adventure |
|---|---|---|
| Character | `CHARACTER_SHEET.md` (one) | `CHARACTER_SHEET_PEOPLE.md` + `CHARACTER_SHEET_RECORDS.md` |
| Case knowledge | `SHARED/CASE_FILE.md` (one state) | Shared + private booklets |
| Scenes | `INVESTIGATION_SCENES.md` | `BOOKLET_PEOPLE.md` + `BOOKLET_RECORDS.md` (+ joint) |
| Navigation | `NAVIGATION_INDEX.md` (solo routes) | Split/regroup index |
| Endings | `ENDINGS.md` (solo triggers) | May reference role flags |

### 1.3 QA pipeline

- **Solo-only brief:** Run Tier A+B for general checks; run all §5.11 QA-SI checks; **skip** QA-RC-01–04 (role cooperation) as N/A.
- **Dual-mode brief:** Run full two-player QA **and** full solo QA.
- **Two-player-only brief:** Run standard QA; solo checks **SKIP** (not PASS).

### 1.4 Development workflow

Stage 2 generation MUST produce `play_manifest.json` before Stage 4 QA.

Stage 3 hygiene MAY invoke `idne.single_investigator_validate` when manifest declares solo.

Stage 4 Adventure QA MUST attach solo validator JSON when `single_investigator` is declared.

---

## 2. What remains unchanged

- Immutable engine principles (U1–U12)
- Fair mystery, Infer requirement, ending sheet-checkability
- Fixed-world check principle
- Two-player cooperation rules (§6.1–§6.7) for `two_player` adventures
- Hygiene validators (identifiers, terminals, clue inventory)
- Harborview (`CASE_BENCHMARK_v0.4`) and The Glass Alibi — **not modified** by Milestone 1
- Mystery model, clue taxonomy, environment, object interaction — deferred milestones

Existing two-player adventures continue to work as `two_player` when they declare that mode (or when no manifest exists and they are treated as legacy two-player content).

---

## 3. Why existing two-player adventures are not automatically solo-compatible

Harborview-class benchmarks were authored and validated for **cooperative two-investigator** play:

| Two-player dependency | Why solo fails without redesign |
|---|---|
| Private booklets | Proof-critical clues live in both `BOOKLET_PEOPLE` and `BOOKLET_RECORDS` |
| Split windows | Parallel paths assume two readers and sync terminators |
| QA-RC-04 | Case is **designed** so one role alone cannot reach correct ending |
| Role balance | Engagement and clue grants are split across roles |
| Wall-clock §5.4 | Session length uses `max(role_A, role_B)` per split window |

Removing Player 2's booklet does not merge graphs, does not relocate clues, and does not remove split-only gates. Validators that only check file presence would **false PASS** if they ignored undeclared solo mode — hence `SKIP` when no solo declaration.

**Example:** Harborview has no `play_manifest.json`. Solo validator returns `SKIP`. It is **not** solo-ready.

---

## 4. How a future adventure declares and proves single-investigator support

### 4.1 Authoring checklist

- [ ] Brief states `single_investigator` and solo wall-clock target
- [ ] Logic graph: every proof-critical clue grant reachable by one investigator
- [ ] No split/regroup units in solo scene package
- [ ] One character sheet + one case file
- [ ] Navigation index complete for solo hubs
- [ ] Endings evaluate solo sheet only
- [ ] `play_manifest.json` with full `single_investigator` block
- [ ] Compilation report uses §5.4.1

### 4.2 Proof artifacts (attach to QA report)

1. **Validator JSON** — `python3 -m idne.single_investigator_validate adventures/<ID>/`
2. **QA report** — all §5.11 rows PASS or waived (Critical never waived)
3. **Reachability evidence** — QA-SI-REACH graph or manual Tier B sign-off
4. **Conclusion path** — QA-SI-CONCLUSIONS: at least one fair solo path to mandatory proof
5. **Playtime** — QA-SI-PLAYTIME + QA-TM-04 with solo formula

### 4.3 Dual-mode adventures

To support **both** modes:

```json
{
  "play_modes": ["two_player", "single_investigator"],
  "two_player": {
    "people_booklet": "PLAYER/BOOKLET_PEOPLE.md",
    "records_booklet": "PLAYER/BOOKLET_RECORDS.md",
    "people_sheet": "PLAYER/CHARACTERS/CHARACTER_SHEET_PEOPLE.md",
    "records_sheet": "PLAYER/CHARACTERS/CHARACTER_SHEET_RECORDS.md"
  },
  "single_investigator": { ... }
}
```

Both routing packages MUST be complete. Solo validation MUST NOT PASS on two-player files alone.

---

## 5. Generator migration

Generators MUST:

- Branch Delivery Adapter output by declared `play_modes`
- Never emit `single_investigator` in `play_modes` from a two-player-only logic graph
- Include solo wall-clock in compilation when solo is declared
- Run `single_investigator_validate` in CI when manifest includes solo

Generators MUST NOT auto-convert two-player adventures to solo.

---

## 6. FAQ

**Can I play Harborview alone?**  
Not as an official `single_investigator` session. It was not designed or validated for solo.

**Does SKIP mean PASS?**  
No. `SKIP` means solo validation did not apply. Solo readiness requires explicit declaration and `PASS`.

**Can I waive QA-SI checks?**  
Critical QA-SI checks follow standard waiver rules: Critical waivers forbidden.

**Do I need a reference solo adventure for Milestone 1?**  
No. Milestone 1 delivers spec, validation, and docs. Reference solo content is a later product task.

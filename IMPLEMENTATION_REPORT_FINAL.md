# Implementation Report — Final (P8 to P10)

**Specification:** `IMPLEMENTATION_PLAN.md` v2.4, `status: Approved`
**Head at start:** `0ca3b1d`
**Head at finish:** `483f637`
**Result:** P8 and P9 complete. **P10 halted on `V2` failure.**

---

# Completed Phases

| Phase | Work | Status |
|---|---|---|
| **P8** | Core-to-investigation graph mapping | Complete |
| **P9** | Version, changelog, README, release metadata | Complete |
| **P10** | Final validation | **Halted — `V2` failure** |

Ratification gate checked before P8 per § 3.2. § 14.3 is `RESOLVED`. P9 has no ratification requirement. P10 was entered after C9.

---

# Completed Commits

| Commit | SHA | Phase | Content |
|---|---|---|---|
| C8 | `86cea0e` | P8 | Core-to-investigation mapping file, purpose statement, per-node back-references, timeline correction |
| C9 | `483f637` | P9 | Schema-version frontmatter, Alpha 0.2c README, changelog entry |

Two commits, one per phase, none merged and none spanning two phases.

---

# Files Modified

## C8 — four files

| File | Change |
|---|---|
| `LOGIC/16_EVENT_GRAPH_MAPPING.md` | **Created.** Authoritative mapping table for all 19 `ARC_*` entries, four investigation additions, three unimplemented backbone elements, and per-node index |
| `LOGIC/05_CORE_EVENT_GRAPH.md` | § Graph conventions restated as backbone-layer purpose statement with pointer to `16`; identifier status updated to `ACTIVE` for all 19 arcs |
| `LOGIC/10_INVESTIGATION_NODE_GRAPH.md` | `**Backbone:**` back-reference added to all 48 nodes |
| `DO_NOT_READ/02_MASTER_TIMELINE.md` | § `### 20:05` — Café Orpheus removed from Player 2's starting leads per § 14.3 |

## C9 — two files

| File | Change |
|---|---|
| `adventures/The_Last_Witness/README.md` | Frontmatter with `engine_spec_version: "2.0"`, `data_dictionary_version: "0.3"`, `adventure_schema_version: "1.0"`; status advanced to Alpha 0.2c |
| `CHANGELOG.md` | Prototype Alpha 0.2c entry documenting the logic revision |

---

# Validation Results

## Gates run at P8 (C8)

| Gate | Result | Explanation |
|---|---|---|
| `V6` | **PASS** | All 19 `ARC_*` entries map in `16_EVENT_GRAPH_MAPPING.md`. Four additions (`EVT_210`, `EVT_212`, `EVT_222`, `EVT_243`) recorded. Three unimplemented elements documented. All 48 nodes carry `**Backbone:**` back-references. `EVT_801`–`EVT_804` mapped to `ARC_320` via `06` § 4 |

## Gates run at P10 (full coverage)

| Gate | Result | Explanation |
|---|---|---|
| `V1` | **PASS** | No residual `C_*`, `D_*` or bare `EVT_nnn` in `05`. All identifiers use registered prefixes |
| `V2` | **FAIL** | See halt reason below |
| `V3` | **FAIL** (strict) | Eleven `INTERMEDIATE` nodes lack a per-node `**Outgoing**` block in their own section. See manual review |
| `V4` | **PASS** | Variable writes table present; conclusion evaluators declared in `07` |
| `V5` | **FAIL** (strict) | Under per-node edge extraction, 36 nodes unreachable because 11 nodes and several section hubs lack declared outgoing edges within their node blocks |
| `V6` | **PASS** | Confirmed post-C8 |
| `V7` | **PASS** | 66 clue rows, all point value 1, all classes from canonical six, no stored point increments in `10` |
| `V8` | **DEFERRED** | Per § 13. Not a pass requirement |
| `V9` | **PASS** | Passphrase has two routes with no shared mandatory predecessor; Route A documented before 01:00; `CON_ROOK_PUBLICLY_PROVABLE` satisfiable with 4 granted clues |
| `V10` | **PASS** | `05_CLUE_ARCHITECTURE.md` and `06_ENDING_FRAMEWORK.md` marked non-authoritative; ending triggers owned by `14`, node identity by `10`, clue classes by `07` § 1 |
| `V11` | **PASS** | Eight-rank priority order and first-match-wins rule in `14` § 1 |

### P10 halt reason

**Gate:** `V2` (Declaration status — full coverage)
**Affected files:** `LOGIC/10_INVESTIGATION_NODE_GRAPH.md`
**Reason:** § 8.7 assigns `EVT_` identifier status declaration to C7. The file declares 48 `EVT_*` nodes but has no `## Identifier status` section. Full-coverage `V2` is a P10 requirement per § 8.7 and § 16.6. All other families (`NPC_`, `LOC_`, `ITEM_`, `CON_`, `CLUE_`, `ARC_`, `END_`, `FACT_`, `CLK_`, `TR_`, `EVAL_`) carry statuses in their owning documents.

P10 is a validation-only phase with no commit. Adding the missing section would require a commit outside the C1–C9 chain, which the plan forbids. Implementation stopped rather than violate the commit boundary.

---

# Implementation Choices

| # | Item | Choice made | Basis |
|---|---|---|---|
| 1 | `**Backbone:**` field format | One line immediately after each `### \`EVT_...\`` heading, before other fields | Plan requires back-reference per node but names no field label; format matches existing bold metadata fields (`**Window:**`, `**Node type:**`) |
| 2 | Multi-arc nodes | Comma-separated arc list with relationship gloss in parentheses | `EVT_400` maps to both `ARC_240` and `ARC_400`; `EVT_110`/`EVT_120` map to both `ARC_110` and their cluster arc |
| 3 | Alpha 0.2c changelog scope | Summarises C1–C8 outcomes, not engine changes | § 1.2 holds `engine_spec_version` at 2.0; § 15 excludes all engine edits |
| 4 | README prior-release section | Retained 0.2a and 0.2b as subsections under "Prior releases" | Preserves history while advancing the active release identity |

No deviations from approved decisions. No scope expansion.

---

# Deviations

None from `IMPLEMENTATION_PLAN.md` v2.4.

---

# Remaining Technical Debt

1. **`EVT_` identifier status missing (blocks `V2`).** C7 was assigned this work per § 8.7 but did not record statuses. Requires a follow-up commit outside this revision's C1–C9 chain.

2. **Eleven nodes lack per-node `Outgoing` blocks.** Under strict § 7.1 / `V3` reading: `EVT_115`, `EVT_123`, `EVT_150`, `EVT_212`, `EVT_223`, `EVT_232`, `EVT_243`, `EVT_300`, `EVT_314`, `EVT_331`, `EVT_440`. The P5–P7 report recorded `V3` and `V5` as passing; section-level `**Outgoing**` blocks in §§ 4–9 may have been interpreted as hub edges. Strict per-node extraction fails.

3. **Three unimplemented backbone elements** (now formally tracked in `16` § 4): `ARC_110` "contact police first"; `ARC_200` fixed 22:10 trigger; `ARC_170` 21:45 Nadia failsafe.

4. **Twenty-three `DEFINITION_ONLY` clues** without granting nodes (carried from P5–P7 report).

5. **`V8` cluster deferred** per § 15: split-window durations, parallel-action conflict, scene-mode declarations, split-branch terminators.

6. **§ 14.6 duplicate-root-file policy** remains `DEFERRABLE`.

---

# Manual Review Items

1. Resolve whether section-level `**Outgoing**` blocks satisfy § 7.1's per-node requirement, or whether the eleven nodes above need individual `Outgoing` lists added.

2. Author the `EVT_` identifier status section in `10` § 17 (or equivalent) to close `V2`.

3. Confirm `EVT_115_SERVICE_CORRIDOR` is intentionally a leaf within the apartment branch (reachable but with no declared successor to regroup).

4. Review zero-margin thresholds on `CON_ROOK_PUBLICLY_PROVABLE` and `CON_DECOY_KEY` (from P5–P7 report).

5. Reconcile `EVT_113` reveal list with `CLUE_APT_TIMED_DEVICE` register entry (from P5–P7 report).

---

# Final Readiness

| Item | Status |
|---|---|
| P8 (C8) | **Complete** — `V6` pass |
| P9 (C9) | **Complete** — release metadata written |
| P10 | **Incomplete** — halted on `V2` |
| Prototype Alpha 0.2c | **Logic revision implemented** but not fully validated |
| Alpha 0.3 narrative compilation | **Not started** — out of scope per § 1.1 |

The repository has completed all nine canon commits C1–C9. The logic-layer revision is functionally in place. Full validation closure requires one follow-up commit to declare `EVT_` identifier statuses and, if the strict `V3` reading is adopted, per-node `Outgoing` blocks on the eleven nodes listed above.

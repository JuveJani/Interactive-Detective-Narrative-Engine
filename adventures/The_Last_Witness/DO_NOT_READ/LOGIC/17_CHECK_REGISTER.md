# DO NOT READ: Check Register

## 1. Purpose

This document owns the `CHK_*` namespace. Each record binds a referenced skill check to its parent `EVT_*` node, pass/fail outcomes, and variant keys already declared in `10_INVESTIGATION_NODE_GRAPH.md`.

Records are declared only when every required field is already defined or deterministically derivable from existing logic. Fields that cannot be derived are marked `BLOCKED` with the missing specification cited.

Required fields per `ENGINE_READINESS_PLAN.md` ER-02 and `BOOK_COMPILER_SPEC.md` MS-04: skill, DC, pass outcome, fail outcome, fallback route.

## 2. Referenced checks inventory

| Reference | Parent `EVT_*` | Logic source | Formalizable as `CHK_*`? |
|---|---|---|---|
| Perception check | `EVT_115_SERVICE_CORRIDOR` | `10` **Failure transformation**; `perception_success` / `perception_failure` variants | **Partial** — pass/fail outcomes defined; **DC not defined** |
| Careful vs failed/rushed search | `EVT_113_APARTMENT_SEARCH` | `10` **Information routes**; six `careful_*` / `rushed_*` variants | **No** — not named as a skill check; outcome is a pace choice, not a D20 roll |
| Technical check (implied) | `EVT_123_NEWSROOM_RECORDS` | `10` **Failure transformation** ("without a technical check") | **No** — check scope, skill, DC, and per-route binding undefined |
| Regroup Two "knowledge check" | `EVT_300_REGROUP_TWO` | `13_SPLIT_AND_REGROUP_FLOW.md` § 6 | **No** — planning checklist, not a player roll |
| Routine check (Rook) | narrative only | `03_NPC_KNOWLEDGE_AND_DISCLOSURE.md` | **No** — narrative constraint, not a formal check |

## 3. `CHK_*` records

### `CHK_115_PERCEPTION`

| Field | Value | Status |
|---|---|---|
| `check_id` | `CHK_115_PERCEPTION` | declared |
| `parent_evt` | `EVT_115_SERVICE_CORRIDOR` | derived from `10` |
| `skill` | perception | named in `10` **Failure transformation** |
| `dc` | — | **BLOCKED** — no DC values exist anywhere in repository |
| `pass_variant_key` | `perception_success` | derived from `10` § 1a **Variants** |
| `fail_variant_key` | `perception_failure` | derived from `10` § 1a **Variants** |
| `pass_effects` | `GRANT_CLUE(CLUE_APT_SERVICE_LATCH)` including fibre trace | derived from `10` **Variants** |
| `fail_effects` | corridor route known; latch direction confirmable later via Mina; no fibre trace | derived from `10` **Failure transformation** |
| `fallback_route` | same node (`EVT_115`); Mina confirms latch direction later | derived from `10` **Failure transformation** |
| `time_cost_minutes` | 15 | derived from `EVT_115` **Cost** |

**Compilation status:** **BLOCKED** until `dc` is authored. Cross-reference: `EVT_115` **Failure transformation** → `CHK_115_PERCEPTION`.

No other `CHK_*` record can be completed without inventing skill, DC, or route bindings.

## 4. Identifier status

| Status | Count | Identifiers |
|---|---:|---|
| `ACTIVE` (partial — blocked on DC) | 1 | `CHK_115_PERCEPTION` |
| `BLOCKED` (incomplete) | 1 | `CHK_115_PERCEPTION` (DC field) |

No `CHK_*` identifier is `DEFINITION_ONLY`, `RESERVED`, or `DEPRECATED`.

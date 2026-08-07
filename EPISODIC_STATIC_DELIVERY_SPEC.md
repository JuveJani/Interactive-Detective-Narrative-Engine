# Episodic Static Delivery Specification

**Status:** Normative for static gamebook / PLAYER delivery projection when epistemic progression uses materialized state snapshots.

## Problem

Materialized epistemic packages represent **exact state snapshots** with filtered structured actions and materialized destination IDs. Static delivery must not collapse those snapshots back into template-level choice supersets.

**Incorrect pattern (forbidden):**

```
template prose unit  →  union(all snapshot action labels)  →  one public section
```

**Required pattern:**

```
canonical template
  → epistemic materialized snapshot (exact actions + materialized destinations)
  → state-specific delivery projection (prose alias + exact action set)
  → state-specific opaque public section
```

## Authority

| Layer | Owns |
|-------|------|
| Canonical / epistemic packages | World truth, eligibility, structured actions, materialized destinations |
| PLAYER markdown (template units) | Reusable prose, meta, titles — **not** delivery choice authority |
| GAMEBOOK / manifest | Delivery projection only |

PLAYER prose must never be the source of knowledge/world/interaction gating.

## Materialized delivery identity

- Internal delivery unit ID = materialized epistemic `unit_id` (e.g. `UNIT-DOCK-BASE`, `UNIT-DOCK-BASE--S-abc123`).
- Prose/meta may alias from `template_unit_id` when body text is unchanged.
- Each delivered section renders **only** the structured actions present on that exact materialized event.
- Choice destinations remain **materialized** unit IDs; public section numbers are assigned 1:1 at build time.

## Build pipeline

1. Load materialized `epistemic_progression_package.json`.
2. Parse template PLAYER units (prose library).
3. For each materialized event, project a delivery unit:
   - `unit_id` = materialized id
   - prose/meta from template alias
   - **no** template choice list copied
4. Build navigation graph from materialized `structured_actions` (exact labels + exact materialized destinations).
5. Supplement unreachable template-only units (e.g. capability-check leaf results) via heuristic graph; never override materialized edges.
6. Assign deterministic opaque public section numbers to all delivery unit IDs.
7. Render `GAMEBOOK.md` from delivery units + graph + section map.
8. Write manifest `units` keyed by delivery unit ID with exact per-section choices.

## State-aware narrative delivery

For each materialized snapshot at render time:

1. Render reusable template/base prose.
2. Select `content_blocks` whose knowledge/world prerequisites match the snapshot state.
3. Append eligible blocks in deterministic `(presentation_order, block_id)` order.
4. Render that snapshot's exact structured choices.

Content blocks describe **current player-visible state**, not assumed recent actions. Blocks may use:

| Field | Purpose |
|-------|---------|
| `requires_knowledge_ids` | show when knowledge present |
| `forbidden_knowledge_ids` | hide when knowledge present |
| `requires_world_state` | show when world flag/value matches |
| `forbidden_world_state` | hide when world flag/value matches |
| `presentation_order` | deterministic ordering among eligible blocks |

Duplicate block text in one section is suppressed at render time.

## Clickable section navigation

Each public section renders as:

```markdown
<a id="section-615"></a>
## Section 615
```

Choice lines link same-document targets while preserving visible numbers:

```markdown
- … Turn to section [**615**](#section-615).
```

Validators require one anchor per public section and valid link targets.

## Opening invariant (Cold Storage)

At initial state (`UNIT-DOCK-BASE` with initial knowledge only), the loading dock delivery section exposes **exactly**:

1. Talk to Elena Morales.
2. Walk through the dock corridor to the cold storage hall.
3. Talk to a dock worker.

Deferred dock navigation, briefing/scene actions, inference worksheets, and NPC dialogue topics must not appear until their epistemic prerequisites are satisfied.

Location hubs must not flatten NPC dialogue topics into the location menu.

## Validation

For materialized packages, validators must **not** union action labels across snapshots of a template.

Per reachable materialized event, validate the delivered manifest/gamebook section:

| Finding | Condition |
|---------|-----------|
| missing eligible choice | structured action absent from delivery |
| extra choice | delivery label not in event structured actions |
| wrong destination | manifest destination ≠ materialized destination unit id |
| flattened dialogue | dialogue topic on location hub |
| early exposure | inference / later-state action on opening snapshot |

Reject template-union / superset GAMEBOOKs.

## Section numbering

Public section numbers remain opaque and deterministic. When delivery unit count exceeds legacy three-digit span, numbering auto-expands — correctness over fixed section budget.

## Non-goals

- Do not require duplicate authored prose per snapshot when visible text is unchanged.
- Do not require players to track hidden state manually.
- Do not collapse materialized states to preserve small GAMEBOOK size.

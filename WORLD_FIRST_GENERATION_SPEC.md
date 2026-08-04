# World-First Generation — Normative Specification

**Document type:** Generation architecture (Milestone 2)  
**Status:** Normative for new adventures using World-First Generation  
**Aligned with:** `IDNE_ENGINE_v0.4.md` §3, §1 U1–U6; `IDNE_DESIGN_PHILOSOPHY.md` A1, A3, A6  
**Schema:** `WORLD_FIRST_GENERATION_SCHEMA.md`  
**Validation:** `WORLD_FIRST_GENERATION_VALIDATION.md`; `python3 -m idne.world_first_validate`

---

## 1. Purpose

World-First Generation requires every mystery to be authored from **fixed reality** before scenes, clues, checks, or endings exist.

The engine MUST NOT support:

```text
Story idea → scenes → clues → retroactive explanation
```

The required direction is:

```text
Fixed Truth
  → Causal Timeline
  → World-State Timeline
  → NPC Knowledge Model
  → Evidence Provenance
  → Observable Information
  → Player-accessible Actions
  → Scenes and Navigation
  → Conclusions and Endings
```

Truth and causality are complete before player-facing narrative construction begins.

World-First Generation is **mode-independent** — applies equally to `single_investigator` and `two_player` adventures.

---

## 2. Forbidden generation patterns

| Pattern | Why forbidden |
|---|---|
| Clue invented because plot needs it | Violates U1, evidence provenance |
| Scene text establishes new objective fact | Violates layer ownership §3 |
| Check success creates evidence that did not exist | Violates fixed-world checks |
| Ending asserts facts not in Fixed Truth | Violates fair play |
| Culprit identifiable by wording emphasis | Violates U9, QA-FR-03 class |
| NPC knows fact without access path | Violates knowledge separation U2 |
| Timeline with ambiguous day/date | Breaks causality validation |
| Retroactive timeline edit without revalidation | Breaks dependent layers |

---

## 3. Canonical layers

### 3.1 Fixed Truth

**Owns:** What actually happened — immutable for play.

| Element | Required |
|---|---|
| Culprit | `culprit_id` |
| Motive | `motive` |
| Method | `method` |
| Opportunity | `opportunity` |
| Immutable facts | `immutable_facts[]` with `fact_id` + `statement` |

Facts in this layer NEVER change during play or delivery compilation.

### 3.2 Causal Timeline

**Owns:** Ordered events with explicit time, location, participants, causes, and effects.

Each event MUST have:

- `event_id`, `timestamp` (ISO-8601 local or explicit clock), `day_label`
- `location_id`, `participants[]`, `causes[]` (prior event IDs)
- `effects[]` / `reveals_facts[]` (fact IDs produced)

Cause-effect MUST be consistent: no event before its causes.

### 3.3 World-State Timeline

**Owns:** Snapshots of locations, objects, access, evidence condition, and people locations **derived from** the causal timeline.

Snapshots MUST reference `at_event_id` from the causal timeline.

State changes MUST trace to timeline events or documented off-screen rules — not to player checks.

### 3.4 NPC Knowledge Model

**Owns:** Per-NPC knowledge, false beliefs, witnessed events, concealment, and behavior rationale.

| Field | Meaning |
|---|---|
| `knows` | Facts NPC correctly holds |
| `believes_incorrectly` | Wrong beliefs with documented cause |
| `witnessed_events` | Events NPC perceived |
| `hides` | Facts NPC withholds |
| `behavior_rationale` | Why NPC acts as they do |

NPC knowledge MUST derive from presence, access, communication, or documented off-screen learning — not plot convenience.

### 3.5 Evidence Provenance

**Owns:** Physical and documentary evidence linked to source events.

Every evidence record MUST have `source_event_id` referencing a causal timeline event.

Misleading evidence MUST have a believable cause in the timeline (lie, forgery, coincidence) — not author convenience.

### 3.6 Observable Information

**Owns:** What can be learned, under which action/location/condition, and what remains hidden.

Each observation links `learnable_fact_id` to `source_evidence_id` or event-derived facts with `requires` (action, location, prior knowledge, item).

Missing player information means **non-access** or **non-perception** — not world mutation.

### 3.7 Narrative Construction

**Owns:** Scene graph, player text, navigation — **only after gates G-WF1–G-WF6 pass**.

Player-facing text MAY NOT invent new `fact_id` values.

Scene `asserted_fact_ids` MUST reference Fixed Truth or observable chain.

Wording MUST NOT reveal narrative importance (Philosophy A2, U9).

---

## 4. Mandatory invariants

1. The world is fixed before checks.
2. Checks never determine whether evidence exists.
3. The same event produces the same underlying evidence on every path.
4. Missing information = player did not access/perceive — not world changed.
5. Every conclusion question answerable from obtainable information.
6. Every required answer has traceable evidence chain.
7. Dates and relative times explicit and unambiguous.
8. No PLAYER information without defined source in observable layer.
9. No ending asserts fact not established in Fixed Truth.
10. No culprit identifiable through wording emphasis rather than evidence.

---

## 5. Generation gates

The AI MUST stop after each layer and validate before continuing.

| Gate | Layer complete when |
|---|---|
| **G-WF1** | Fixed Truth complete — culprit, motive, method, opportunity, immutable facts |
| **G-WF2** | Timeline causally consistent — ordered times, valid causes, no contradictions |
| **G-WF3** | World states derived from timeline snapshots |
| **G-WF4** | NPC knowledge derived from presence and access |
| **G-WF5** | Evidence provenance complete — every item traces to event |
| **G-WF6** | All conclusion questions answerable from observable chain |
| **G-WF7** | Scene generation permitted — gates 1–6 PASS; narrative does not invent truth |

If a later layer requires changing earlier truth, the generator MUST return to that layer and revalidate **all dependent layers**.

Gate status is recorded in `generation_manifest.json` (see schema).

---

## 6. Authoring order (mandatory)

1. Fixed Truth (`world_truth_package.fixed_truth`)
2. Causal Timeline
3. World-State Timeline
4. NPC Knowledge Model
5. Evidence Provenance
6. Observable Information
7. Conclusion Requirements
8. Adventure Logic (actions, costs, checks — fixed-world compatible only)
9. Narrative Construction / Delivery Adapter → PLAYER

**MUST NOT** begin step 9 before G-WF7 prerequisites satisfied.

---

## 7. Declaration

World-First adventures declare in `generation_manifest.json` at adventure root:

```json
{
  "schema_version": "1.0",
  "generation_method": "world_first",
  "package_path": "DO_NOT_READ/world_truth_package.json",
  "gates": { "G-WF1": { "status": "PASS" }, ... }
}
```

Legacy adventures without this manifest are **not** World-First validated (validator returns `SKIP`).

---

## 8. Compatibility

| Mode | World-First |
|---|---|
| `single_investigator` | Supported — observable layer mode-independent |
| `two_player` | Supported — split scenes compile from same truth package |
| Harborview / Glass Alibi | Not modified — legacy generation |
| Environment System | Not in scope (Milestone 3+) |
| Object Interaction System | Not in scope (Milestone 4+) |

---

## 9. Relationship to existing layers

World-First replaces **generation order** and **validation** — not the engine's layer stack (Engine §3.1).

| Existing layer | World-First role |
|---|---|
| World Bible | May be compiled **from** Fixed Truth + Timeline for human reading |
| Adventure Logic | Built after observable layer; MUST not contradict package |
| Delivery Adapter | Narrative Construction only after G-WF7 |
| PLAYER | Never authoritative for truth |

---

## 10. Out of scope (Milestone 2)

- Environment System (location affordances as first-class layer)
- Object Interaction System
- Investigation Rewrite / Capability Check Rewrite
- Playtime Calibration milestone
- Generating a new reference adventure
- Converting Harborview or Glass Alibi
- Redesigning clue/ending mechanics beyond fixed-world enforcement
- Claiming subjective mystery quality is fully automatable

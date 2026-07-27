# 04. Execution Model and Layer Boundaries

## 1. Purpose

This chapter defines when rules are evaluated, which layer owns each decision, and what remains for the player during play. Its purpose is to prevent ambiguity between the World Bible, Adventure Logic, Narrative Compiler, Book Formatter, and player-facing runtime.

## 2. Authoritative Pipeline

```text
Engine Specification
        ↓
Data Dictionary and Schemas
        ↓
World Bible
        ↓
Adventure Logic
        ↓
Narrative Compiler
        ↓
Book Formatter
        ↓
Player Output
```

Each layer may consume the validated output of the layer above it. A lower layer must not redefine objective facts owned by a higher layer.

## 3. Compile-Time and Play-Time Separation

### 3.1 Compile-time

Compile-time includes all processing performed before the playable artifact is delivered.

The compiler shall:

- validate entity and event references;
- evaluate objective world facts against event conditions;
- produce all permitted public event variants;
- merge variants that produce identical player-facing results;
- remove internal identifiers and hidden state information;
- verify that every public choice resolves to a valid target;
- verify clue redundancy, terminal states, and required recovery paths.

The formatter shall:

- assign public node numbers or page references;
- produce player-specific output artifacts;
- apply layout, typography, navigation, and media rules;
- obscure internal IDs without changing game logic.

### 3.2 Play-time

The physical or static prototype has no runtime compiler. During play, players only:

- read public nodes;
- make choices;
- record explicitly exposed state changes;
- advance the shared world clock when instructed;
- resolve lightweight checks defined by the adventure rules;
- move to the referenced public node.

Players must never evaluate raw internal conditions, inspect hidden variables, or manually simulate off-screen NPC logic.

## 4. Public Condition Tags

When a public choice depends on known player state, the compiled output may use a standardized player-facing condition tag.

Examples:

```text
[IF YOU HAVE ITEM_04]
[IF PLAYER 2 KNOWS CLUE_07]
[IF WORLD TIME IS 18:00 OR LATER]
```

These tags are generated from internal conditions. They are not the internal condition language itself.

A public condition tag must:

- reference only information the relevant player is allowed to know;
- be directly checkable from the player record sheet;
- avoid exposing hidden state names or unrevealed facts;
- resolve to a valid alternative when the condition is false.

## 5. Variant Control and Node Merging

The engine shall not create a separate public node for every theoretical combination of world variables.

The compiler shall create a new public variant only when the player-facing outcome materially changes, including:

- available choices;
- revealed clues;
- time cost;
- item or state updates;
- NPC presence or behavior;
- terminal outcome.

Variants with identical player-facing consequences shall be merged.

This rule limits state explosion while preserving deterministic world logic.

## 6. Formatter Boundary

The Book Formatter must not:

- evaluate hidden world conditions;
- invent or remove choices;
- alter time costs;
- modify clue content;
- change state updates;
- decide which narrative variant is correct.

Those responsibilities belong to the Narrative Compiler and Adventure Logic.

## 7. Prototype Constraint

For the first two-hour prototype, all playable state must fit on one shared record sheet plus one private knowledge sheet per player. Any mechanic requiring more administration must be simplified, automated during compilation, or deferred to a later engine release.

---
engine_spec_version: "2.0"
data_dictionary_version: "0.3"
adventure_schema_version: "1.0"
---

# The Last Witness

**Prototype Alpha 0.2c: Logic Revision**  
**Engine baseline:** IDNE 0.3 / Engine Specification 2.0  
**Target playtime:** approximately 2 hours  
**Players:** 2  
**Status:** compiler-ready core logic with normalized identifiers, progress model and complete node graph

## Spoiler warning

Everything inside `DO_NOT_READ` contains the solution and implementation logic. Players must use only the future `PLAYER` package.

## What this release adds

Alpha 0.2c completes the logic-layer revision specified in the implementation plan. It adds:

- adventure-local prefix registry and canonical ownership rules;
- mechanical identifier migration (`CLUE_*`, `CON_*`, `ARC_*` backbone namespace);
- derived progress totals with atomic `GRANT_CLUE` operations;
- canonical six-class clue vocabulary with diversity counting;
- passphrase access routes and failure transformation;
- `NODE_TYPE`, `Outgoing` edges and eight terminal ending nodes on every playable node;
- core-to-investigation backbone mapping with tracked unimplemented elements;
- schema-version metadata (`adventure_schema_version: 1.0`).

Alpha 0.2a and 0.2b content remains the foundation: world-state variables, item matrix, NPC schedules, investigation graph, location state machines, clue dependency graph, split/regroup flow and ending trigger matrix.

The release does not yet contain finished player prose. Narrative compilation is reserved for Alpha 0.3.

## Prior releases

### Prototype Alpha 0.2b

Added the detailed investigation graph, location state machine, clue-dependency graph, split/regroup flow, and ending trigger matrix.

### Prototype Alpha 0.2a

Converted the case foundation into a deterministic world-state model with entity identifiers, state variables, time costs, core event graph and evidence validation.

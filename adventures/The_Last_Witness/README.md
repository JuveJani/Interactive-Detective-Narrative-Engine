# The Last Witness

**Prototype Alpha 0.2a: Core Logic**  
**Engine baseline:** IDNE 0.3  
**Target playtime:** approximately 2 hours  
**Players:** 2  
**Status:** objective reality plus compiler-ready core logic

## Spoiler warning

Everything inside `DO_NOT_READ` contains the solution and implementation logic. Players must use only the future `PLAYER` package.

## What this release adds

Alpha 0.2a converts the case foundation into a deterministic world-state model. It adds:

- immutable entity identifiers;
- global and local state variables;
- explicit item movement records;
- NPC knowledge-ingestion paths;
- standardized travel and action costs;
- a core event graph;
- off-screen NPC schedules and priority rules;
- evidence validation requirements for accusation and rescue;
- split-party safety constraints;
- pre-logic audit resolutions.

The release does not yet contain finished player prose. It is the logical layer from which the investigation flow will be compiled.

## Prototype Alpha 0.2b

This release adds the detailed investigation graph, location state machine, clue-dependency graph, split/regroup flow, and ending trigger matrix.

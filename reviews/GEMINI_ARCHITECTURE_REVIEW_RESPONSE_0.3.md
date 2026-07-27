# Response to External Architecture Review

## Review Context

An external architecture review identified strengths and risks involving schema contracts, compiler boundaries, state growth, two-player synchronization, replayability, and automated validation.

Release 0.3 accepts the review selectively according to the project's immediate objective: produce and test a complete two-hour solo and two-player detective prototype without abandoning the long-term reusable-engine direction.

## Accepted for Immediate Implementation

### Compile-Time and Play-Time Boundary

Accepted. The specification now states that hidden conditions and narrative variants are resolved before delivery. Players do not execute a runtime compiler.

### Two-Player Synchronization

Accepted. Split scenes now use synchronization windows, one authoritative world clock, forced rejoin states, and explicit knowledge transfer.

### Minimal Schema Versioning

Accepted. Version metadata is introduced before adventure production so future formal schemas have a migration anchor.

### Soft-Lock Recovery

Accepted. The prototype requires clue redundancy and authored fallback events for critical investigation paths.

### Prototype Validation Gate

Accepted. The project now separates features required for Prototype 1 from valuable but deferrable infrastructure.

## Accepted as Future Work

### Executable JSON Schema

Architecturally valuable, but not required before the first prototype. It should be implemented once real adventure records expose which fields require formal validation.

### CI/CD Graph Validation

Strongly recommended after the first adventure graph exists. The initial validation suite should detect broken references, orphan nodes, zero-cost loops, and undeclared terminals.

### Automated Compiler or GUI

The architecture should remain compatible with future automation. Building the software pipeline is deferred until the manual specification has survived at least one full playtest.

### Campaign State Serialization

Deferred. Prototype 1 is standalone.

## Partially Accepted

### Exponential Node Growth

The risk is real, but separate public nodes are required only when player-facing consequences materially differ. Compile-time variant merging is now an explicit engine rule.

### Human Runtime Overhead

This is a physical-format constraint rather than an architectural failure. The prototype imposes a strict bookkeeping budget to prevent it from damaging playability.

### Seeded Replayability

Useful, but secondary. Prototype 1 permits limited controlled seeds while keeping the primary case truth fixed unless multi-culprit validation is deliberately authored.

## Not Adopted for Prototype 1

### General Timestamp Event Queue

A full event queue would overcomplicate the static prototype. Authored timestamp triggers and synchronization windows are sufficient for the current design.

### Mandatory Separate Commercial PDF Pipeline

Separate player outputs are required for private split scenes, but commercial publication tooling is deferred.

## Result

The external review does not trigger a redesign. It produces a focused Release 0.3 that closes immediate architecture gaps and then moves the project into adventure production and playtesting.

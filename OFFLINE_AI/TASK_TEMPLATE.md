# Task Template

Copy and fill for scoped agent or human tasks.

---

## Goal

_One sentence: what must be true when done?_

## Allowed scope

- Files/subsystems that may change:
- Commands that may be run:

## Forbidden scope

- Engine behavior changes (unless explicitly listed above)
- Validator weakening
- Harborview / Glass Alibi edits
- Full adventure generation in one response
- New runtime dependencies (RAG, DB, MCP) unless approved

## Authoritative files

_List specs and code paths to read first._

- 
- 

## Expected output

- [ ] Code changes (if any) with minimal diff
- [ ] Tests added/updated (if any)
- [ ] Docs updated (if state changed)
- [ ] `SESSION_HANDOFF.md` updated (if significant)

## Validation commands

```bash
# Focused
python -m unittest tests.test_<module> -v

# Full suite
python -m unittest discover -s tests

# Package validation (if applicable)
python -m idne.validate_adventure tests/fixtures/sim_v2_solo

# Simulator (if applicable)
python -m idne.sim_v2 validate tests/fixtures/sim_v2_solo.idne
```

## Completion report

Provide:

1. Branch and commit hash
2. Files created or modified
3. Commands actually run and results
4. Facts vs observations vs assumptions
5. Unresolved blockers
6. Whether the stated goal is complete

---

## Example (documentation-only)

**Goal:** Add OFFLINE_AI workspace files.  
**Forbidden:** Any Python module under `idne/`, `simulator_v2/`, `tests/`.  
**Validation:** `python -m unittest discover -s tests` → 433 OK.

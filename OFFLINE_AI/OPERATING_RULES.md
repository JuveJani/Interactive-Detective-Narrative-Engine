# Operating Rules

Normative behavior for humans and AI agents working in this repository.

## Before editing

1. Read `AGENTS.md` and `OFFLINE_AI/CURRENT_STATE.md`.
2. Identify authoritative specs for the layer you will touch.
3. Inspect existing code, tests, and fixtures — match conventions.

## Planning

- Plan before large or cross-layer changes.
- State allowed scope and forbidden scope explicitly (use `TASK_TEMPLATE.md`).
- Prefer minimal diffs that solve the stated problem.

## Truth and validation

- **Preserve approved fixed world truth.** Do not mutate immutable facts to fix symptoms.
- **Never weaken validators** to obtain PASS or trusted simulator results.
- Run layer validator or integrated validation after package changes.
- Stop on unresolved **FAIL** or **BLOCKED**; report ownership (PACKAGE, GENERATOR, SIMULATOR, UNDETERMINED).

## Testing

1. Run focused tests for the subsystem changed.
2. Run full suite: `python -m unittest discover -s tests`.
3. Record exact commands and results in `SESSION_HANDOFF.md`.
4. **Never claim tests passed** unless they were actually executed in this environment.

## Generator discipline

- One human-approved brief per generation run.
- One canonical layer per stage; validate before continuing.
- **Do not generate a full adventure in one model response.**
- Do not skip integrated validation before calling export complete.

## Simulator discipline

- Use `python -m idne.sim_v2` for canonical `.idne` packages.
- Respect trust gate: untrusted quantitative results are observations, not adventure facts.
- Exhaustive mode may return BLOCKED on state explosion — that is not a silent success.

## Evidence labeling

| Label | Meaning |
|-------|---------|
| **Fact** | Directly from authoritative spec, passing test, or validated package field |
| **Observation** | Simulator or validator output (may be untrusted) |
| **Assumption** | Reasonable guess not yet verified |
| **Proposal** | Suggested change requiring review |

## Git and branches

- Branch from latest `main` unless task specifies otherwise.
- Commit with complete sentences describing what and why.
- Do not force-push or rewrite history unless requested.

## Session handoff

After significant work, update `OFFLINE_AI/SESSION_HANDOFF.md`:

- branch and commit
- completed work
- commands and tests actually run
- decisions made
- unresolved blockers
- exact next safe action

## Prohibited

- Inventing schema fields or validator rules not in specs.
- Editing Harborview or Glass Alibi unless explicitly tasked.
- Adding RAG, embeddings, or new runtime dependencies without approval.
- Creating a parallel source of engine truth outside canonical specs.

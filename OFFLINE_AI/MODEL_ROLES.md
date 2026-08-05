# Model Roles

Suggested **task roles** for local LM Studio models. These are **not permanent quality claims** — benchmark on real IDNE tasks before relying on them.

Record measured results in `LOCAL_SETUP.md` when available.

## Models (intended roles)

| Model | Intended role | Typical tasks |
|-------|---------------|---------------|
| **Qwen3.5 9B** | Discussion, report explanation, planning, small scoped work | Explain simulator findings, draft briefs, review plans |
| **Qwen2.5 Coder 7B** | Quick code assistance, small edits | Single-file fixes, test interpretation, doc tweaks |
| **Qwen2.5 Coder 14B** | Normal offline programming | Feature implementation within one subsystem, test additions |
| **Qwen3.6 35B-A3B** | Complex agentic coding, repository reasoning, staged adventure generation | Multi-file changes, generator stage authoring, architecture tasks |

## Assignment rules

1. Match model size to task scope — do not use 35B for typo fixes or 7B for cross-layer refactors.
2. **Always provide repository context** via `AGENTS.md`, `OFFLINE_AI/`, and relevant specs — not long chat history.
3. For adventure generation: **one layer per invocation**; validate before next stage.
4. Require the model to label facts vs observations vs assumptions.
5. Human reviews all generated canonical JSON before merge.

## Benchmarking required

Before finalizing role assignments, run comparable tasks and record:

- pass rate on validator after generation stage
- tokens/latency on target hardware (e.g. Acer Swift Go 14, 32 GB RAM)
- failure modes (schema drift, truth leakage, validator BLOCKED)

Until benchmarks exist, treat this table as **provisional**.

## Cursor vs local LM Studio

- **Cursor native Agent** may use cloud models; do not assume it routes through localhost LM Studio.
- **Cline** inside Cursor can be configured for local endpoints — see `LOCAL_SETUP.md`.
- **CLI / scripted agents** should use `idne/model_adapter/` backends when integrated.

## When to escalate

| Symptom | Action |
|---------|--------|
| Repeated validator FAIL on same layer | Smaller scope per call or larger model |
| Schema field invention | Re-read spec; reduce temperature; add explicit schema excerpt |
| Simulator trust false | Fix package/validation — do not blame adventure from untrusted metrics |

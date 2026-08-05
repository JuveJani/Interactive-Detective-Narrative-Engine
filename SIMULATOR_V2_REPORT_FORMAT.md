# Simulator v2 Report Format

Each run creates `simulation_output_v2/<timestamp>_<mode>_<n>/`.

## Required files

| File | Content |
|------|---------|
| executive_diagnostic.md | Trust status, critical findings, simulation summary |
| findings.md | Human-readable finding list |
| findings.json | Machine-readable full diagnostic report |
| metrics.json | Time and simulation metrics |
| repair_backlog.md | Suggested repairs (no auto-edits) |
| strategy_comparison.csv | Ending frequencies per strategy |
| paths.csv | Trace action sequence |
| endings.csv | Monte Carlo ending counts |
| time_analysis.csv | In-world vs wall-clock vs active time |
| state_transitions.csv | Step/action/kind trace |
| human_playtest_questions.md | Table prompts for live playtest |
| simulator_log.txt | Run log |
| parse_errors.md | Parse/derivation errors |
| run_manifest.json | Run metadata |

## Optional subfolders

- `explanations/<finding_id>.md` — per-finding explainer
- `repair_options/<finding_id>.json` — repair option details
- `ai_context/<finding_id>/` — offline AI handoff (via export command)

## Trust annotations

When `trust.trusted` is false, executive diagnostic and AI context mark quantitative rates as untrusted observations, not adventure facts.

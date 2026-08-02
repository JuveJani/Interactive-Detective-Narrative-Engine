# Offline Finding Explainer and Repair Advisor

## What this adds

After each simulator run, you get human-readable explanations, repair suggestions, and compact files for a local AI on your phone — no internet required.

## Termux (Google Pixel 10 Pro)

```bash
cd ~/idne   # or your clone path
pkg install python
chmod +x run_full_diagnostic.sh explain_latest.sh export_latest_for_ai.sh
./run_full_diagnostic.sh 200 42
```

Open `simulation_output/<latest>/executive_diagnostic.md` in any text editor.

## CLI commands

```bash
python3 idne_sim.py explain simulation_output/<folder>
python3 idne_sim.py explain simulation_output/<folder> --finding SIM-FAKE-J-122
python3 idne_sim.py repair-plan simulation_output/<folder> --finding SIM-TRUST-DOWNGRADE
python3 idne_sim.py export-ai-context simulation_output/<folder> --finding SIM-TRUST-DOWNGRADE
```

## Output files (per run)

| File | Purpose |
|------|---------|
| `executive_diagnostic.md` | Eight-question summary for humans |
| `repair_backlog.md` | Prioritized repair options |
| `repair_options.json` | Machine-readable repair list |
| `engine_findings.md` | Engine-layer items only |
| `adventure_findings.md` | Adventure and undetermined items |
| `delivery_findings.md` | Adapter and player package |
| `simulator_findings.md` | Simulator code issues |
| `human_playtest_questions.md` | Table questions |
| `explanations/<ID>.md` | One file per finding |
| `local_ai_context/finding_context_<ID>.md` | Compact AI handoff |

## Trust gate

When `simulator_trustworthy` is false, adventure-blaming findings are marked **UNDETERMINED** and quantitative metrics must not be treated as proof.

## Patches

`repair-plan --finding <ID>` may write `proposed_fix_<ID>.md` and `.patch` placeholders only. Applying changes remains a manual step.

See also: `OFFLINE_REPAIR_WORKFLOW.md`, `OFFLINE_AI_WORKFLOW.md`.

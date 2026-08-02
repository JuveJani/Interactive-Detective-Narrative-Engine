# Offline Repair Workflow

## Principles

1. **Simulator first** — Fix simulator blockers before trusting adventure findings.
2. **Options, not auto-edits** — The tool suggests repairs; you apply them.
3. **Layer ownership** — Engine changes only when an engine rule is violated.
4. **Human approval** — Gameplay and player text changes need author sign-off.

## Steps

### 1. Run diagnostic

```bash
./run_full_diagnostic.sh
```

### 2. Read executive summary

Open `executive_diagnostic.md` in the latest `simulation_output/` folder.

### 3. Explain one finding

```bash
./explain_latest.sh SIM-TRUST-DOWNGRADE
```

### 4. Get repair plan

```bash
python3 idne_sim.py repair-plan simulation_output/<folder> --finding <ID>
```

Review `proposed_fix_<ID>.md` if generated. Do not apply `.patch` files blindly.

### 5. Validate after any change

```bash
python3 idne_sim.py validate adventures/CASE_BENCHMARK_v0.4
python3 idne_sim.py simulate adventures/CASE_BENCHMARK_v0.4 --runs 200 --seed 42
./explain_latest.sh
```

### 6. Optional local AI

```bash
./export_latest_for_ai.sh SIM-FAKE-J-122
```

Feed `local_ai_context/finding_context_<ID>.md` plus `OFFLINE_AI_SYSTEM_PROMPT.md` to your on-device model.

## What not to change yet

- Engine specification (unless a true engine rule violation is proven)
- Adventure proof rules while `simulator_trustworthy` is false
- Player story content based only on simulator hypotheses

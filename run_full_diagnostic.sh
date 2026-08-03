#!/usr/bin/env bash
# Full offline diagnostic: validate, simulate, explain, export AI context
set -euo pipefail
cd "$(dirname "$0")"
ADV="adventures/CASE_BENCHMARK_v0.4"
RUNS="${1:-200}"
SEED="${2:-42}"
echo "== validate =="
OUT_V=$(python3 idne_sim.py validate "$ADV" | tail -1)
echo "== simulate ($RUNS runs) =="
OUT_S=$(python3 idne_sim.py simulate "$ADV" --runs "$RUNS" --seed "$SEED" | tail -1)
echo "== explain =="
python3 idne_sim.py explain "$OUT_S"
echo "== export AI context =="
python3 idne_sim.py export-ai-context "$OUT_S"
echo ""
echo "Output folder: $OUT_S"
echo "Read: $OUT_S/executive_diagnostic.md"

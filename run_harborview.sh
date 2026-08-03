#!/data/data/com.termux/files/usr/bin/bash
# Quick Harborview Arcade simulation presets (Termux-safe defaults)
set -euo pipefail
cd "$(dirname "$0")"
ADV="adventures/CASE_BENCHMARK_v0.4"
CMD="${1:-validate}"
shift || true
case "$CMD" in
  validate)
    python3 idne_sim.py validate "$ADV" "$@"
    ;;
  simulate)
    python3 idne_sim.py simulate "$ADV" --runs 1000 --seed 42 "$@"
    ;;
  trace)
    python3 idne_sim.py trace "$ADV" --seed 42 "$@"
    ;;
  compare)
    python3 idne_sim.py compare "$ADV" --runs-per-strategy 200 --seed 42 "$@"
    ;;
  *)
    echo "Usage: $0 {validate|simulate|trace|compare} [extra args]"
    exit 1
    ;;
esac

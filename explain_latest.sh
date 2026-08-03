#!/data/data/com.termux/files/usr/bin/bash
# Explain findings from the most recent simulation_output folder
set -euo pipefail
cd "$(dirname "$0")"
LATEST=$(ls -td simulation_output/*/ 2>/dev/null | head -1)
if [ -z "$LATEST" ]; then
  echo "No simulation_output folders found. Run ./run_full_diagnostic.sh first."
  exit 1
fi
FINDING="${1:-}"
if [ -n "$FINDING" ]; then
  python3 idne_sim.py explain "$LATEST" --finding "$FINDING"
else
  python3 idne_sim.py explain "$LATEST"
fi
echo "Explanations: ${LATEST}explanations/"

#!/data/data/com.termux/files/usr/bin/bash
# Install IDNE simulator on Termux (Google Pixel / aarch64)
set -euo pipefail
cd "$(dirname "$0")"
pkg update -y
pkg install -y python
python3 -m pip install --upgrade pip 2>/dev/null || true
chmod +x idne_sim.py run_harborview.sh
echo "IDNE simulator ready. Run: ./run_harborview.sh validate"

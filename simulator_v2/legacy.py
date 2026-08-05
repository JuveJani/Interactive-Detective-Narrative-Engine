"""Legacy simulator compatibility boundary."""

from __future__ import annotations

from pathlib import Path

LEGACY_SIMULATOR_MARKER = "legacy_sim_adapter_required"
LEGACY_SIMULATOR_MODULE = "simulator"


def is_legacy_simulator_path(adventure_root: Path) -> bool:
    """Return True when adventure requires legacy sim_adapter.json."""
    root = Path(adventure_root).resolve()
    adapter = root / "sim_adapter.json"
    generation = root / "generation_manifest.json"
    if adapter.exists() and not generation.exists():
        return True
    if (root / "SIM_ADAPTER.json").exists() and not generation.exists():
        return True
    return False


def legacy_simulator_notice() -> str:
    return (
        "Legacy simulator (simulator/) requires sim_adapter.json. "
        "Use simulator_v2 for Generator v2 .idne packages."
    )

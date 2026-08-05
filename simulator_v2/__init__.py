"""Simulator v2 — canonical package-driven simulation foundation."""

from simulator_v2.legacy import LEGACY_SIMULATOR_MARKER, is_legacy_simulator_path
from simulator_v2.package_loader import PackageLoadResult, load_simulator_package
from simulator_v2.service import SimulatorService

__version__ = "2.0.0-part1"

__all__ = [
    "LEGACY_SIMULATOR_MARKER",
    "PackageLoadResult",
    "SimulatorService",
    "is_legacy_simulator_path",
    "load_simulator_package",
]

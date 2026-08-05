"""Simulator v2 — canonical package-driven simulation foundation."""

from simulator_v2.legacy import LEGACY_SIMULATOR_MARKER, is_legacy_simulator_path
from simulator_v2.engine import EngineConfig, SimulationEngine
from simulator_v2.modes import MonteCarloConfig, SimulationModes
from simulator_v2.package_loader import PackageLoadResult, load_simulator_package
from simulator_v2.service import SimulatorService
from simulator_v2.strategies import STRATEGIES, create_strategy

__version__ = "2.0.0-part2"

__all__ = [
    "LEGACY_SIMULATOR_MARKER",
    "EngineConfig",
    "MonteCarloConfig",
    "PackageLoadResult",
    "SimulationEngine",
    "SimulationModes",
    "SimulatorService",
    "STRATEGIES",
    "create_strategy",
    "is_legacy_simulator_path",
    "load_simulator_package",
]

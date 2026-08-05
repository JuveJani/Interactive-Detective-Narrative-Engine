"""Trust gate for quantitative simulation findings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.types import PackageLoadResult


@dataclass
class TrustEvaluation:
    trusted: bool
    ownership: str
    blockers: list[str] = field(default_factory=list)
    coverage: str = ""
    mechanics_supported: bool = False
    package_integrity: bool = False
    strategies_blind: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "trusted": self.trusted,
            "ownership": self.ownership,
            "blockers": self.blockers,
            "coverage": self.coverage,
            "mechanics_supported": self.mechanics_supported,
            "package_integrity": self.package_integrity,
            "strategies_blind": self.strategies_blind,
        }


REQUIRED_MECHANICS = (
    "world_truth",
    "environment",
    "object_interaction",
    "investigation_core",
    "npc_investigation",
    "investigation_flow",
    "capability_check",
)


def evaluate_trust(
    load: PackageLoadResult,
    model: CanonicalSimulationModel | None,
    coverage: str = "",
) -> TrustEvaluation:
    blockers: list[str] = []
    package_integrity = load.checksum_valid and load.status.value == "READY"
    if not package_integrity:
        blockers.append("package_integrity_failed")

    mechanics_supported = True
    if model:
        for layer in REQUIRED_MECHANICS:
            if layer not in model.raw_packages:
                mechanics_supported = False
                blockers.append(f"missing_mechanic:{layer}")
        if model.report.errors:
            blockers.append("derivation_errors")
            mechanics_supported = False
    else:
        mechanics_supported = False
        blockers.append("no_model")

    if load.integrated_validation_status not in ("PASS",):
        blockers.append(f"integrated_validation:{load.integrated_validation_status}")

    trusted = package_integrity and mechanics_supported and not blockers
    ownership = "ADVENTURE" if trusted else "SIMULATOR"
    if not package_integrity:
        ownership = "PACKAGE"
    elif not mechanics_supported:
        ownership = "GENERATOR"
    elif blockers:
        ownership = "UNDETERMINED"

    return TrustEvaluation(
        trusted=trusted,
        ownership=ownership,
        blockers=blockers,
        coverage=coverage,
        mechanics_supported=mechanics_supported,
        package_integrity=package_integrity,
        strategies_blind=True,
    )

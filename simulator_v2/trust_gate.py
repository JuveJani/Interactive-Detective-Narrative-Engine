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
    integrated_validation_status: str = "MISSING"

    def to_dict(self) -> dict[str, Any]:
        return ensure_trust_blockers({
            "trusted": self.trusted,
            "ownership": self.ownership,
            "blockers": list(self.blockers),
            "coverage": self.coverage,
            "mechanics_supported": self.mechanics_supported,
            "package_integrity": self.package_integrity,
            "strategies_blind": self.strategies_blind,
            "integrated_validation_status": self.integrated_validation_status,
        })


REQUIRED_MECHANICS = (
    "world_truth",
    "environment",
    "object_interaction",
    "investigation_core",
    "npc_investigation",
    "investigation_flow",
    "capability_check",
)

TRUSTED_INTEGRATED_STATUSES = frozenset({"PASS"})


def integrated_validation_status(load: PackageLoadResult) -> str:
    status = load.integrated_validation_status
    if not status:
        return "MISSING"
    return str(status)


def ensure_trust_blockers(trust_dict: dict[str, Any]) -> dict[str, Any]:
    """Untrusted results must always carry explicit blockers."""
    trusted = bool(trust_dict.get("trusted"))
    blockers = list(trust_dict.get("blockers") or [])
    if not trusted and not blockers:
        ivs = trust_dict.get("integrated_validation_status") or "MISSING"
        if ivs not in TRUSTED_INTEGRATED_STATUSES:
            blockers.append(f"integrated_validation:{ivs}")
        elif not trust_dict.get("coverage"):
            blockers.append("trust_gate:missing_coverage")
        elif not trust_dict.get("mechanics_supported", True):
            blockers.append("trust_gate:mechanics_unsupported")
        elif not trust_dict.get("package_integrity", True):
            blockers.append("trust_gate:package_integrity_failed")
        else:
            blockers.append("trust_gate:quantitative_trust_denied")
    trust_dict["blockers"] = blockers
    return trust_dict


def evaluate_trust(
    load: PackageLoadResult,
    model: CanonicalSimulationModel | None,
    coverage: str = "",
) -> TrustEvaluation:
    blockers: list[str] = []
    ivs = integrated_validation_status(load)

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

    if ivs not in TRUSTED_INTEGRATED_STATUSES:
        blockers.append(f"integrated_validation:{ivs}")

    trusted = (
        package_integrity
        and mechanics_supported
        and ivs in TRUSTED_INTEGRATED_STATUSES
        and not blockers
    )
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
        integrated_validation_status=ivs,
    )


def trust_dict_for_mode(
    load: PackageLoadResult,
    model: CanonicalSimulationModel | None,
    coverage: str,
) -> dict[str, Any]:
    return evaluate_trust(load, model, coverage=coverage).to_dict()

"""Trust evaluation for human-delivery simulation."""

from __future__ import annotations

from typing import Any

from simulator_v2.human_delivery.types import DeliveryFinding


def evaluate_human_delivery_trust(
    *,
    delivery_validation_status: str,
    gamebook_checks_pass: bool,
    visible_navigation_complete: bool,
    route_equivalence: str,
    hidden_boundary_violation: bool,
    canonical_validation_status: str,
    epistemic_validation_status: str = "SKIP",
    epistemic_eligibility_failures: int = 0,
    findings: list[DeliveryFinding],
) -> dict[str, Any]:
    blockers: list[str] = []
    if delivery_validation_status != "PASS":
        blockers.append(f"delivery_validation:{delivery_validation_status}")
    if not gamebook_checks_pass:
        blockers.append("gamebook_navigation_failed")
    if not visible_navigation_complete:
        blockers.append("visible_navigation_incomplete")
    if route_equivalence != "PASS":
        blockers.append(f"route_equivalence:{route_equivalence}")
    if hidden_boundary_violation:
        blockers.append("hidden_information_boundary_violation")
    if canonical_validation_status not in ("PASS", "CONDITIONAL_PASS"):
        blockers.append(f"canonical_validation:{canonical_validation_status}")
    if epistemic_validation_status not in ("PASS", "SKIP"):
        blockers.append(f"epistemic_validation:{epistemic_validation_status}")
    if epistemic_eligibility_failures and epistemic_validation_status not in ("PASS", "SKIP"):
        blockers.append(f"epistemic_eligibility_failures:{epistemic_eligibility_failures}")

    delivery_defects = [
        f
        for f in findings
        if (f.defect_class.value if hasattr(f.defect_class, "value") else f.defect_class)
        == "delivery_defect"
    ]
    if delivery_defects:
        blockers.append(f"delivery_defects:{len(delivery_defects)}")

    trusted = not blockers
    return {
        "trusted": trusted,
        "layer": "human_delivery",
        "blockers": blockers,
        "ownership": "ADVENTURE" if trusted else "SIMULATOR",
        "note": "Monte Carlo statistics untrusted when blockers present",
    }

"""DM Feeling diagnostic categories (Milestone 10)."""

from __future__ import annotations

from typing import Any

CATEGORIES = (
    "player_agency",
    "discovery_delivery",
    "exploration_depth",
    "inference_quality",
    "aha_potential",
    "world_responsiveness",
    "time_pressure",
    "failure_quality",
    "conversation_agency",
    "ending_causality",
    "mode_specific",
)

CATEGORY_LABELS = {
    "player_agency": "Player agency",
    "discovery_delivery": "Discovery vs delivery",
    "exploration_depth": "Exploration depth",
    "inference_quality": "Inference quality",
    "aha_potential": "Aha potential",
    "world_responsiveness": "World responsiveness",
    "time_pressure": "Time pressure",
    "failure_quality": "Failure quality",
    "conversation_agency": "Conversation agency",
    "ending_causality": "Ending causality",
    "mode_specific": "Mode-specific quality",
}


def score_category(findings: list[Any], category: str) -> str:
    """PASS if no proven Tier A critical in category; FAIL if critical proven; else CONDITIONAL."""
    cat_findings = [f for f in findings if f.category == category]
    if not cat_findings:
        return "PASS"
    critical_a = [
        f for f in cat_findings
        if f.tier == "A" and f.confidence == "proven" and f.severity == "critical"
    ]
    if critical_a:
        return "FAIL"
    if cat_findings:
        return "CONDITIONAL_PASS"
    return "PASS"


def category_scores(findings: list[Any]) -> dict[str, str]:
    return {cat: score_category(findings, cat) for cat in CATEGORIES}

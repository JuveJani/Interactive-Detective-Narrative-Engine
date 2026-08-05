"""Unified diagnostic findings for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DiagnosticFinding:
    """Canonical finding record with ownership and trust metadata."""

    finding_id: str
    severity: str
    confidence: str
    canonical_source: str
    source_file: str
    affected_entity: str
    affected_paths: list[str]
    simulation_evidence: str
    expected_behavior: str
    observed_behavior: str
    trust_impact: str
    likely_owner: str
    repair_eligible: bool
    human_approval_required: bool
    validator: str = ""
    tier: str = "A"
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "canonical_source": self.canonical_source,
            "source_file": self.source_file,
            "affected_entity": self.affected_entity,
            "affected_paths": self.affected_paths,
            "simulation_evidence": self.simulation_evidence,
            "expected_behavior": self.expected_behavior,
            "observed_behavior": self.observed_behavior,
            "trust_impact": self.trust_impact,
            "likely_owner": self.likely_owner,
            "repair_eligible": self.repair_eligible,
            "human_approval_required": self.human_approval_required,
            "validator": self.validator,
            "tier": self.tier,
            **self.extra,
        }

    @classmethod
    def from_validator_finding(cls, validator: str, raw: dict[str, Any]) -> DiagnosticFinding:
        fid = raw.get("finding_id") or raw.get("id", "UNKNOWN")
        layer = raw.get("layer", raw.get("likely_owner", "PACKAGE"))
        return cls(
            finding_id=f"{validator.upper()[:3]}-{fid}" if not str(fid).startswith(validator[:3].upper()) else str(fid),
            severity=raw.get("severity", "major"),
            confidence=raw.get("confidence", "proven"),
            canonical_source=str(raw.get("canonical_id") or raw.get("entity_id") or raw.get("identifier", "")),
            source_file=str(raw.get("source_file") or raw.get("file", "")),
            affected_entity=str(raw.get("entity_id") or raw.get("canonical_id") or raw.get("identifier", "")),
            affected_paths=list(raw.get("broken_trace") or raw.get("affected_paths") or []),
            simulation_evidence=str(raw.get("observed_issue") or raw.get("actual_state") or raw.get("evidence", "")),
            expected_behavior=str(raw.get("expected_canonical") or raw.get("expected_rule", "")),
            observed_behavior=str(raw.get("observed_issue") or raw.get("actual_state") or raw.get("evidence", "")),
            trust_impact="none" if layer in ("SIMULATOR", "VALIDATOR") else "may_downgrade_quantitative",
            likely_owner=_normalize_owner(layer),
            repair_eligible=bool(raw.get("automatically_fixable") or raw.get("auto_fix_possible") or raw.get("script_detectable")),
            human_approval_required=bool(raw.get("human_approval_needed") or raw.get("human_approval_required", True)),
            validator=validator,
            tier=str(raw.get("tier", "A")),
            extra={k: v for k, v in raw.items() if k not in {
                "finding_id", "id", "severity", "confidence", "layer", "source_file", "file",
            }},
        )


def _normalize_owner(layer: str) -> str:
    mapping = {
        "ADVENTURE": "GENERATOR",
        "PACKAGE": "PACKAGE",
        "SIMULATOR": "SIMULATOR",
        "VALIDATOR": "SIMULATOR",
        "ENGINE": "SIMULATOR",
        "DELIVERY_ADAPTER": "PACKAGE",
        "PLAYER_PACKAGE": "GENERATOR",
        "UNDETERMINED": "UNDETERMINED",
        "HUMAN_PLAYTEST": "UNDETERMINED",
    }
    return mapping.get(layer.upper(), layer.upper() if layer else "UNDETERMINED")

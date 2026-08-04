"""Playtime Calibration validator (Milestone 9)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.playtime_estimate import estimate_playtime


@dataclass
class Finding:
    finding_id: str
    severity: str
    confidence: str
    player_mode: str
    path_or_split: str
    predicted_lower_minutes: float
    predicted_expected_minutes: float
    predicted_upper_minutes: float
    target_minutes: float
    source_components: list[str]
    assumption_set: str
    error_or_uncertainty: str
    gameplay_risk: str
    human_measurement_required: bool
    tier: str = "A"

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "confidence": self.confidence,
            "player_mode": self.player_mode,
            "path_or_split": self.path_or_split,
            "predicted_lower_minutes": round(self.predicted_lower_minutes, 2),
            "predicted_expected_minutes": round(self.predicted_expected_minutes, 2),
            "predicted_upper_minutes": round(self.predicted_upper_minutes, 2),
            "target_minutes": self.target_minutes,
            "source_components": self.source_components,
            "assumption_set": self.assumption_set,
            "error_or_uncertainty": self.error_or_uncertainty,
            "gameplay_risk": self.gameplay_risk,
            "human_measurement_required": self.human_measurement_required,
            "tier": self.tier,
        }


@dataclass
class ValidationResult:
    adventure_root: Path
    status: str
    findings: list[Finding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, str] = field(default_factory=dict)
    tier_b_pending: list[str] = field(default_factory=list)
    estimate: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_root": str(self.adventure_root),
            "status": self.status,
            "findings": [f.to_dict() for f in self.findings],
            "warnings": self.warnings,
            "checks": self.checks,
            "tier_b_pending": self.tier_b_pending,
            "estimate": self.estimate,
        }


def load_manifest(root: Path) -> dict[str, Any] | None:
    for name in ("playtime_calibration_manifest.json", "PLAYTIME_CALIBRATION_MANIFEST.json"):
        path = root / name
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    gen = root / "generation_manifest.json"
    if gen.exists():
        data = json.loads(gen.read_text(encoding="utf-8"))
        pt = data.get("playtime_calibration")
        if isinstance(pt, dict) and pt.get("enabled"):
            return {
                "schema_version": data.get("schema_version", "1.0"),
                "playtime_calibration_method": "canonical",
                "package_path": pt.get("package_path", "DO_NOT_READ/playtime_calibration_package.json"),
            }
    return None


def load_package(root: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    rel = manifest.get("package_path", "DO_NOT_READ/playtime_calibration_package.json")
    path = root / rel
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _add(
    result: ValidationResult,
    finding_id: str,
    player_mode: str,
    path_or_split: str,
    expected_min: float,
    predicted: float,
    target: float,
    error: str,
    risk: str,
    components: list[str] | None = None,
    tier: str = "A",
    confidence: str = "proven",
    human: bool = False,
    severity: str = "critical",
) -> None:
    margin = 0.15
    result.findings.append(
        Finding(
            finding_id=finding_id,
            severity=severity,
            confidence=confidence,
            player_mode=player_mode,
            path_or_split=path_or_split,
            predicted_lower_minutes=predicted * (1 - margin),
            predicted_expected_minutes=predicted,
            predicted_upper_minutes=predicted * (1 + margin),
            target_minutes=target,
            source_components=components or [],
            assumption_set="canonical_baseline",
            error_or_uncertainty=error,
            gameplay_risk=risk,
            human_measurement_required=human,
            tier=tier,
        )
    )


def validate_playtime(adventure_root: str | Path) -> ValidationResult:
    root = Path(adventure_root).resolve()
    result = ValidationResult(adventure_root=root, status="PASS")

    manifest = load_manifest(root)
    if not manifest:
        result.status = "SKIP"
        result.warnings.append("no playtime_calibration_manifest — not declared")
        return result

    if manifest.get("playtime_calibration_method") != "canonical":
        result.status = "SKIP"
        result.warnings.append("playtime_calibration_method not canonical")
        return result

    package = load_package(root, manifest)
    if not package:
        result.status = "BLOCKED"
        result.checks["PT-PKG-PRESENT"] = "BLOCKED"
        _add(result, "PT-PKG-MISSING", "", "", 0, 0, 0, "package missing", "cannot estimate")
        return result
    result.checks["PT-PKG-PRESENT"] = "PASS"

    # Required metadata check → BLOCKED
    required = ("target_playtime_minutes", "play_modes", "wall_clock_paths")
    missing_meta = [k for k in required if not package.get(k)]
    timing_entries = package.get("wall_clock_paths", []) or []
    if timing_entries and not package.get("activity_class_defaults"):
        missing_meta.append("activity_class_defaults")
    if package.get("metadata_incomplete"):
        missing_meta.append("metadata_incomplete")

    if missing_meta:
        result.status = "BLOCKED"
        result.checks["PT-METADATA"] = "BLOCKED"
        _add(
            result,
            "PT-METADATA-MISSING",
            str(package.get("play_modes", [])),
            "",
            0,
            0,
            float(package.get("target_playtime_minutes", 0)),
            f"missing: {missing_meta}",
            "cannot estimate without authored timing",
        )
        return result
    result.checks["PT-METADATA"] = "PASS"

    est_result = estimate_playtime(package)
    result.estimate = est_result.to_dict()
    target = float(package.get("target_playtime_minutes", 0))
    compliance = package.get("target_compliance", {}) or {}
    hard_low = float(compliance.get("hard_fail_low_pct", 75))
    hard_high = float(compliance.get("hard_fail_high_pct", 140))
    warn_low = float(compliance.get("major_warning_low_pct", 85))
    warn_high = float(compliance.get("major_warning_high_pct", 120))
    play_mode = est_result.play_mode

    median = est_result.wall_clock_median_minutes
    pct = (median / target * 100) if target else 0

    target_ok = True
    if target and pct < hard_low:
        target_ok = False
        _add(
            result,
            "PT-TARGET-HARD-LOW",
            play_mode,
            "median",
            target,
            median,
            target,
            f"median {median:.1f}min is {pct:.0f}% of target",
            "adventure too short for stated target",
        )
    elif target and pct > hard_high:
        target_ok = False
        _add(
            result,
            "PT-TARGET-HARD-HIGH",
            play_mode,
            "median",
            target,
            median,
            target,
            f"median {median:.1f}min is {pct:.0f}% of target",
            "adventure too long for stated target",
        )
    elif target and (pct < warn_low or pct > warn_high):
        _add(
            result,
            "PT-TARGET-WARNING",
            play_mode,
            "median",
            target,
            median,
            target,
            f"median {median:.1f}min is {pct:.0f}% of target",
            "outside major warning band",
            severity="major",
        )
    result.checks["PT-TARGET"] = "PASS" if target_ok else "FAIL"

    # Two-player parallel sum
    tp_ok = True
    if est_result.two_player and est_result.two_player.incorrectly_summed_parallel:
        tp_ok = False
        _add(
            result,
            "PT-PARALLEL-SUMMED",
            "two_player",
            "split_windows",
            target,
            est_result.two_player.total_expected_minutes,
            target,
            "parallel branches summed instead of max",
            "overstates session duration",
        )
    result.checks["PT-TWO-PLAYER-FORMULA"] = "PASS" if tp_ok else "FAIL"

    # Mutually exclusive summed
    mutex_ok = not est_result.mutually_exclusive_summed
    if est_result.mutually_exclusive_summed:
        mutex_ok = False
        _add(
            result,
            "PT-MUTEX-SUMMED",
            play_mode,
            "paths",
            target,
            est_result.exhaustive_content_minutes,
            target,
            "mutually exclusive paths summed",
            "inflated playtime claim",
        )
    result.checks["PT-MUTEX"] = "PASS" if mutex_ok else "FAIL"

    # Per-path / activity checks from package flags
    activity_ok = True
    for path in package.get("wall_clock_paths", []) or []:
        pid = str(path.get("path_id", ""))
        for act in path.get("activities", []) or []:
            if act.get("complexity_misclassified_as_complex"):
                activity_ok = False
                _add(
                    result,
                    "PT-SIMPLE-AS-COMPLEX",
                    play_mode,
                    pid,
                    target,
                    0,
                    target,
                    f"activity {act.get('activity_id', '')}",
                    "reading time inflated",
                )
            if act.get("bare_destination_code") and act.get("meaningful_decision_credit"):
                activity_ok = False
                _add(
                    result,
                    "PT-FAKE-DECISION-CREDIT",
                    play_mode,
                    pid,
                    target,
                    0,
                    target,
                    "bare code choice given decision credit",
                    "decision time inflated",
                )
            if act.get("checkbox_masquerade") and act.get("puzzle_expected_minutes", 0) > 2:
                activity_ok = False
                _add(
                    result,
                    "PT-CHECKBOX-PUZZLE",
                    play_mode,
                    pid,
                    target,
                    float(act.get("puzzle_expected_minutes", 0)),
                    target,
                    "checkbox given substantial puzzle time",
                    "puzzle time inflated",
                )
            if act.get("missing_timing_metadata"):
                activity_ok = False
                _add(
                    result,
                    "PT-ACTIVITY-METADATA",
                    play_mode,
                    pid,
                    target,
                    0,
                    target,
                    f"missing timing on {act.get('activity_id', '')}",
                    "incomplete metadata",
                )
    result.checks["PT-ACTIVITIES"] = "PASS" if activity_ok else "FAIL"

    # Time scarcity
    scarcity_ok = True
    scarcity = package.get("time_scarcity", {}) or {}
    if scarcity.get("scarcity_intended") and scarcity.get("exhaustive_fits_before_deadline"):
        scarcity_ok = False
        _add(
            result,
            "PT-SCARCITY-NO-PRESSURE",
            play_mode,
            "in_world",
            target,
            est_result.exhaustive_content_minutes,
            float(scarcity.get("deadline_in_world_minutes", 0)),
            "exhaustive exploration fits comfortably",
            "time scarcity ineffective",
        )
    if scarcity.get("fair_solution_after_deadline"):
        scarcity_ok = False
        _add(
            result,
            "PT-DEADLINE-BEFORE-SOLUTION",
            play_mode,
            "in_world",
            target,
            0,
            float(scarcity.get("deadline_in_world_minutes", 0)),
            "fair solution not achievable before deadline",
            "impossible deadline",
        )
    if scarcity.get("time_gated_event_unreachable"):
        scarcity_ok = False
        _add(
            result,
            "PT-TIME-GATED-UNREACHABLE",
            play_mode,
            "in_world",
            target,
            0,
            float(scarcity.get("deadline_in_world_minutes", 0)),
            "time-gated event never reachable",
            "missed world change",
        )
    result.checks["PT-SCARCITY"] = "PASS" if scarcity_ok else "FAIL"

    # Split imbalance
    split_ok = True
    if est_result.two_player:
        imbalance_limit = float(package.get("split_balance_limit_minutes", 5))
        if est_result.two_player.split_imbalance_minutes > imbalance_limit:
            split_ok = False
            _add(
                result,
                "PT-SPLIT-IMBALANCE",
                "two_player",
                "split_windows",
                target,
                est_result.two_player.split_imbalance_minutes,
                target,
                f"imbalance {est_result.two_player.split_imbalance_minutes:.1f}min",
                "severe split wait imbalance",
                severity="major",
            )
    result.checks["PT-SPLIT-BALANCE"] = "PASS" if split_ok else "FAIL"

    # Playtest calibration
    cal_ok = True
    cal = package.get("playtest_calibration", {}) or {}
    observations = cal.get("observations", []) or []
    min_for_change = int(cal.get("min_observations_for_default_change", 3))
    if observations:
        errors = []
        for obs in observations:
            pred = float(obs.get("predicted_minutes", 0))
            actual = float(obs.get("actual_minutes", 0))
            if pred:
                errors.append(abs(actual - pred) / pred)
        if len(observations) == 1 and cal.get("attempted_default_change"):
            cal_ok = False
            _add(
                result,
                "PT-CAL-SINGLE-OBS",
                play_mode,
                "calibration",
                target,
                observations[0].get("predicted_minutes", 0),
                target,
                "one playtest insufficient for default change",
                "premature calibration",
            )
        if len(observations) >= min_for_change and cal.get("recommendation"):
            result.warnings.append(f"calibration recommendation: {cal.get('recommendation')}")
        for obs in observations:
            pred = float(obs.get("predicted_minutes", 0))
            actual = float(obs.get("actual_minutes", 0))
            if pred and abs(actual - pred) / pred > 0.4:
                _add(
                    result,
                    "PT-CAL-ERROR",
                    obs.get("mode", play_mode),
                    "playtest",
                    pred,
                    actual,
                    target,
                    f"error {(actual - pred):.1f}min",
                    "prediction mismatch",
                    severity="major",
                    human=True,
                )
    result.checks["PT-CALIBRATION"] = "PASS" if cal_ok else "FAIL"

    # Path report completeness
    path_types = {p.path_type for p in est_result.paths}
    required_paths = {"shortest_valid", "median_expected", "longest_valid_before_deadline"}
    if package.get("require_path_report") and not required_paths.issubset(path_types):
        _add(
            result,
            "PT-PATH-REPORT",
            play_mode,
            "paths",
            target,
            median,
            target,
            f"missing path types: {required_paths - path_types}",
            "incomplete path report",
            severity="major",
        )

    # Tier B
    for item in package.get("tier_b_mandatory", []) or []:
        tid = str(item.get("review_id", ""))
        if not item.get("resolved"):
            result.tier_b_pending.append(tid)
            _add(
                result,
                f"PT-TIER-B-{tid}",
                play_mode,
                tid,
                target,
                median,
                target,
                "pending human review",
                item.get("expected", "tier B review"),
                tier="B",
                confidence="likely",
                human=True,
                severity="major",
            )

    # Outcome
    proven_a = [f for f in result.findings if f.tier == "A" and f.confidence == "proven" and f.severity == "critical"]
    if result.checks.get("PT-METADATA") == "BLOCKED":
        result.status = "BLOCKED"
    elif proven_a:
        result.status = "FAIL"
    elif result.tier_b_pending or any(f.tier == "B" for f in result.findings):
        result.status = "CONDITIONAL_PASS"
    elif any(f.severity == "major" for f in result.findings):
        result.status = "CONDITIONAL_PASS"
    else:
        result.status = "PASS"

    return result


def main(argv: list[str] | None = None) -> int:
    import sys

    args = argv or sys.argv[1:]
    if not args:
        print("Usage: python3 -m idne.playtime_validate <adventure_root>")
        return 2
    res = validate_playtime(args[0])
    print(json.dumps(res.to_dict(), indent=2))
    if res.status == "BLOCKED":
        return 2
    return 0 if res.status in ("PASS", "SKIP", "CONDITIONAL_PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())

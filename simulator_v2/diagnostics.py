"""Integrated diagnostics: validators + simulation evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from idne.dm_feeling_validate import validate_dm_feeling
from idne.investigation_validate import validate_investigation
from idne.playtime_validate import validate_playtime
from idne.story_validate import validate_story
from idne.validate_adventure.runner import validate_adventure
from simulator_v2.derivation import CanonicalSimulationModel
from simulator_v2.findings import DiagnosticFinding, _normalize_owner
from simulator_v2.modes import ExhaustiveConfig, MonteCarloConfig, SimulationModes
from simulator_v2.trust_gate import evaluate_trust
from simulator_v2.types import PackageLoadResult


VALIDATOR_FNS = {
    "investigation": validate_investigation,
    "story": validate_story,
    "playtime": validate_playtime,
    "dm_feeling": validate_dm_feeling,
}


@dataclass
class DiagnosticReport:
    adventure_id: str
    play_mode: str
    integrated_validation: dict[str, Any]
    trust: dict[str, Any]
    findings: list[DiagnosticFinding] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    simulation: dict[str, Any] = field(default_factory=dict)
    parse_errors: list[str] = field(default_factory=list)
    log: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_id": self.adventure_id,
            "play_mode": self.play_mode,
            "integrated_validation": self.integrated_validation,
            "trust": self.trust,
            "findings": [f.to_dict() for f in self.findings],
            "metrics": self.metrics,
            "simulation": self.simulation,
            "parse_errors": self.parse_errors,
        }


def _extract_validator_findings(validator: str, adventure_root: Path) -> list[DiagnosticFinding]:
    fn = VALIDATOR_FNS.get(validator)
    if not fn:
        return []
    manifest_name = {
        "investigation": "investigation_validator_manifest.json",
        "story": "story_validator_manifest.json",
        "playtime": "playtime_calibration_manifest.json",
        "dm_feeling": "dm_feeling_validator_manifest.json",
    }.get(validator, "")
    if manifest_name and not (adventure_root / manifest_name).exists():
        return []
    try:
        if validator == "dm_feeling":
            result = fn(adventure_root, write_report_files=False)
        else:
            result = fn(adventure_root)
    except Exception as exc:
        return [
            DiagnosticFinding(
                finding_id=f"SIM-PARSE-{validator.upper()}",
                severity="critical",
                confidence="proven",
                canonical_source=manifest_name,
                source_file=manifest_name,
                affected_entity=validator,
                affected_paths=[str(adventure_root)],
                simulation_evidence=str(exc),
                expected_behavior="Validator runs without error",
                observed_behavior=f"Validator raised: {exc}",
                trust_impact="blocks_trust",
                likely_owner="SIMULATOR",
                repair_eligible=False,
                human_approval_required=True,
                validator=validator,
            )
        ]
    if getattr(result, "status", "") == "SKIP":
        return []
    findings: list[DiagnosticFinding] = []
    for raw in getattr(result, "findings", []) or []:
        data = raw.to_dict() if hasattr(raw, "to_dict") else dict(raw)
        findings.append(DiagnosticFinding.from_validator_finding(validator, data))
    for err in getattr(result, "errors", []) or []:
        findings.append(
            DiagnosticFinding(
                finding_id=f"{validator.upper()}-ERR-{len(findings)}",
                severity="major",
                confidence="proven",
                canonical_source=validator,
                source_file="",
                affected_entity=validator,
                affected_paths=[],
                simulation_evidence=str(err),
                expected_behavior="No validator errors",
                observed_behavior=str(err),
                trust_impact="blocks_trust",
                likely_owner="PACKAGE",
                repair_eligible=False,
                human_approval_required=True,
                validator=validator,
            )
        )
    return findings


def _simulation_findings(
    load: PackageLoadResult,
    model: CanonicalSimulationModel | None,
    sim_data: dict[str, Any],
    trust: dict[str, Any],
) -> list[DiagnosticFinding]:
    findings: list[DiagnosticFinding] = []
    if not load.simulation_ready:
        findings.append(
            DiagnosticFinding(
                finding_id="SIM-LOAD-BLOCKED",
                severity="critical",
                confidence="proven",
                canonical_source=load.adventure_id,
                source_file=str(load.package_path),
                affected_entity=load.adventure_id,
                affected_paths=[str(load.package_path)],
                simulation_evidence="; ".join(load.errors) or load.status.value,
                expected_behavior="Package loads with READY status and simulation_ready",
                observed_behavior=f"status={load.status.value}",
                trust_impact="blocks_trust",
                likely_owner="PACKAGE",
                repair_eligible=False,
                human_approval_required=True,
                validator="simulator",
            )
        )
        return findings

    if not trust.get("trusted"):
        for blocker in trust.get("blockers", []):
            findings.append(
                DiagnosticFinding(
                    finding_id=f"SIM-TRUST-{blocker[:24].upper().replace(':', '-')}",
                    severity="major",
                    confidence="proven",
                    canonical_source="trust_gate",
                    source_file="simulator_v2/trust_gate.py",
                    affected_entity=load.adventure_id,
                    affected_paths=[],
                    simulation_evidence=blocker,
                    expected_behavior="Trust gate passes for quantitative findings",
                    observed_behavior=blocker,
                    trust_impact="blocks_trust",
                    likely_owner=_normalize_owner(trust.get("ownership", "SIMULATOR")),
                    repair_eligible=False,
                    human_approval_required=True,
                    validator="simulator",
                )
            )

    mc = sim_data.get("monte_carlo", {})
    endings = mc.get("ending_frequencies", {})
    if trust.get("trusted") and model and endings:
        total = sum(endings.values())
        for eid, ent in model.endings.items():
            if ent.payload.get("ending_type") == "perfect" and total >= 10:
                if endings.get(eid, 0) == 0:
                    findings.append(
                        DiagnosticFinding(
                            finding_id="SIM-PERFECT-UNREACHABLE",
                            severity="major",
                            confidence="suspected",
                            canonical_source=eid,
                            source_file="DO_NOT_READ/investigation_flow_package.json",
                            affected_entity=eid,
                            affected_paths=[],
                            simulation_evidence=f"0/{total} Monte Carlo runs reached {eid}",
                            expected_behavior="Perfect ending reachable under some legal strategy",
                            observed_behavior=f"Not observed in {total} runs",
                            trust_impact="none",
                            likely_owner="GENERATOR",
                            repair_eligible=True,
                            human_approval_required=True,
                            validator="simulator",
                        )
                    )
                break

    exhaustive = sim_data.get("exhaustive", {})
    if exhaustive.get("status") == "BLOCKED":
        findings.append(
            DiagnosticFinding(
                finding_id="SIM-EXHAUSTIVE-BLOCKED",
                severity="info",
                confidence="proven",
                canonical_source="exhaustive_mode",
                source_file="simulator_v2/modes.py",
                affected_entity=load.adventure_id,
                affected_paths=[],
                simulation_evidence=str(exhaustive.get("blocked_reason", "unknown")),
                expected_behavior="Bounded exhaustive completes or reports partial coverage",
                observed_behavior=f"BLOCKED: {exhaustive.get('blocked_reason')}",
                trust_impact="coverage_incomplete",
                likely_owner="SIMULATOR",
                repair_eligible=False,
                human_approval_required=False,
                validator="simulator",
            )
        )

    return findings


def run_integrated_diagnostics(
    package_path: str | Path,
    *,
    config: Any = None,
    run_simulation: bool = True,
    cancel_flag: list[bool] | None = None,
    checkpoint_path: Path | None = None,
    resume: bool = False,
) -> DiagnosticReport:
    from simulator_v2.config import RunnerConfig
    from simulator_v2.package_loader import load_simulator_package
    from simulator_v2.derivation import derive_simulation_model

    cfg = config or RunnerConfig()
    log: list[str] = []
    parse_errors: list[str] = []

    load = load_simulator_package(package_path)
    log.append(f"loaded {load.adventure_id} status={load.status.value}")

    adventure_root = load.adventure_root
    integrated = validate_adventure(adventure_root).to_dict() if adventure_root else {"status": "BLOCKED"}
    log.append(f"integrated validation={integrated.get('status')}")

    findings: list[DiagnosticFinding] = []
    if adventure_root:
        for vname in VALIDATOR_FNS:
            vf = _extract_validator_findings(vname, adventure_root)
            findings.extend(vf)
            log.append(f"{vname} validator: {len(vf)} finding(s)")

    model = None
    if load.adventure_root and load.status.value == "READY":
        try:
            model = derive_simulation_model(load.adventure_root, load.play_mode)
        except Exception as exc:
            parse_errors.append(str(exc))
            log.append(f"derivation error: {exc}")

    sim_data: dict[str, Any] = {}
    metrics: dict[str, Any] = {"in_world_minutes": 0, "wall_clock_minutes": 0}

    if run_simulation and load.simulation_ready and model:
        modes = SimulationModes(str(package_path))
        trace = modes.trace(cfg.strategy, seed=cfg.seed)
        sim_data["trace"] = trace.to_dict()
        log.append(f"trace status={trace.status} ending={trace.ending_id}")

        mc_runs = min(cfg.monte_carlo_runs, cfg.max_runs)
        sim_data["monte_carlo"] = modes.monte_carlo(
            MonteCarloConfig(runs=mc_runs, seed=cfg.seed),
            strategy=cfg.strategy,
        )
        log.append(f"monte_carlo runs={mc_runs}")

        sim_data["compare"] = modes.compare_strategies(
            runs_per_strategy=min(cfg.compare_runs_per_strategy, 50),
            seed=cfg.seed,
        )

        if resume and checkpoint_path and checkpoint_path.exists():
            try:
                sim_data["exhaustive"] = json.loads(checkpoint_path.read_text(encoding="utf-8"))
                log.append("resumed exhaustive from checkpoint")
            except Exception as exc:
                parse_errors.append(f"checkpoint read: {exc}")

        if "exhaustive" not in sim_data:
            sim_data["exhaustive"] = modes.exhaustive(
                ExhaustiveConfig(
                    max_states=min(cfg.max_states, 200_000),
                    timeout_seconds=cfg.exhaustive_timeout_seconds,
                ),
                cancel_flag=cancel_flag,
            )
            if checkpoint_path:
                checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
                checkpoint_path.write_text(json.dumps(sim_data["exhaustive"], indent=2), encoding="utf-8")

        sim_data["path_analysis"] = modes.path_analysis(cfg.strategy, seed=cfg.seed)

        metrics.update({
            "trace_steps": trace.metrics.steps,
            "trace_ending": trace.ending_id,
            "monte_carlo": sim_data.get("monte_carlo", {}),
            "exhaustive_states": sim_data.get("exhaustive", {}).get("states_explored", 0),
            "in_world_minutes": trace.metrics.in_world_minutes,
            "player_active_minutes": trace.metrics.player_active_minutes,
        })

    coverage = sim_data.get("exhaustive", {}).get("coverage", "monte_carlo")
    trust_eval = evaluate_trust(load, model, coverage=coverage)
    trust = trust_eval.to_dict()
    findings.extend(_simulation_findings(load, model, sim_data, trust))

    return DiagnosticReport(
        adventure_id=load.adventure_id,
        play_mode=load.play_mode,
        integrated_validation=integrated,
        trust=trust,
        findings=findings,
        metrics=metrics,
        simulation=sim_data,
        parse_errors=parse_errors,
        log=log,
    )

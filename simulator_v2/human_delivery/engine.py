"""Human-delivery simulation engine."""

from __future__ import annotations

from typing import Any

from simulator_v2.human_delivery.loader import AdventureWorkspace
from simulator_v2.human_delivery.parse import extract_start_section, parse_gamebook
from simulator_v2.human_delivery.player_view import HiddenInformationAccessError, HumanDeliveryPlayerView
from simulator_v2.human_delivery.strategies import HumanDeliveryStrategy, create_human_strategy
from simulator_v2.human_delivery.trust import evaluate_human_delivery_trust
from simulator_v2.human_delivery.types import DeliveryDefectClass, DeliveryFinding, HumanDeliveryResult, HumanTraceStep
from simulator_v2.human_delivery.validate import validate_human_delivery
from simulator_v2.package_loader import load_simulator_package
from simulator_v2.rng import DeterministicRNG


def _finding_from_dict(raw: dict) -> DeliveryFinding:
    dc = raw.get("defect_class", "delivery_defect")
    if isinstance(dc, str):
        dc = DeliveryDefectClass(dc)
    return DeliveryFinding(
        finding_id=raw["finding_id"],
        message=raw["message"],
        defect_class=dc,
        severity=raw.get("severity", "error"),
        context=raw.get("context") or {},
    )


def _section_maps(manifest: dict) -> tuple[dict[int, str], dict[str, int]]:
    unit_to_sec: dict[str, int] = {}
    for uid, entry in (manifest.get("units") or {}).items():
        sec = entry.get("public_section")
        if sec is None and manifest.get("public_sections"):
            sec = manifest["public_sections"].get(uid)
        if sec is not None:
            unit_to_sec[uid] = int(sec)
    sec_to_unit = {v: k for k, v in unit_to_sec.items()}
    return sec_to_unit, unit_to_sec


def _manifest_choice_dest(manifest: dict, unit_id: str, dest_section: int, sec_to_unit: dict[int, str]) -> str | None:
    dest_unit = sec_to_unit.get(dest_section)
    if not dest_unit:
        return None
    entry = (manifest.get("units") or {}).get(unit_id, {})
    for edge in entry.get("choices") or []:
        if edge.get("destination_unit_id") == dest_unit:
            return dest_unit
    return dest_unit


def _check_canonical_edge(manifest: dict, from_unit: str, to_unit: str) -> str:
    """Verify manifest declares a visible edge between mapped units."""
    from_entry = (manifest.get("units") or {}).get(from_unit, {})
    for edge in from_entry.get("choices") or []:
        if edge.get("destination_unit_id") == to_unit:
            return "PASS"
    if from_unit.startswith("END-"):
        return "PASS"
    return "FAIL"


class HumanDeliveryEngine:
    def __init__(self, workspace: AdventureWorkspace) -> None:
        self.workspace = workspace
        self.manifest = workspace.manifest
        self.sec_to_unit, self.unit_to_sec = _section_maps(self.manifest)
        self.parsed = parse_gamebook(workspace.gamebook_path, self.sec_to_unit)
        start_file, start_section, _ = extract_start_section(self.manifest)
        self.start_file = start_file
        self.start_section = start_section
        self._canonical_validation_status = "UNKNOWN"

    def _canonical_status(self) -> str:
        if self._canonical_validation_status == "UNKNOWN":
            load = load_simulator_package(str(self.workspace.adventure_root))
            self._canonical_validation_status = load.integrated_validation_status or "UNKNOWN"
        return self._canonical_validation_status

    def run_trace(
        self,
        strategy: str | HumanDeliveryStrategy = "human_random_legal",
        seed: int = 42,
        max_steps: int = 200,
        *,
        skip_validation: bool = False,
        skip_trust: bool = False,
    ) -> HumanDeliveryResult:
        if skip_validation:
            delivery = {"status": "PASS", "findings": []}
            findings: list[DeliveryFinding] = []
        else:
            delivery = validate_human_delivery(self.workspace)
            findings = [_finding_from_dict(f) for f in delivery.get("findings", [])]
        strat = create_human_strategy(strategy) if isinstance(strategy, str) else strategy
        rng = DeterministicRNG(seed)

        result = HumanDeliveryResult(
            status="BLOCKED" if delivery["status"] != "PASS" else "IN_PROGRESS",
            adventure_id=self.workspace.adventure_id,
            start_file=self.start_file,
            start_section=self.start_section,
            findings=findings,
        )

        if delivery["status"] != "PASS":
            result.status = "BLOCKED"
            result.trust = evaluate_human_delivery_trust(
                delivery_validation_status=delivery["status"],
                gamebook_checks_pass=False,
                visible_navigation_complete=False,
                route_equivalence="FAIL",
                hidden_boundary_violation=False,
                canonical_validation_status="UNKNOWN",
                findings=findings,
            )
            return result

        cur_sec = self.start_section
        visited: set[int] = set()
        steps: list[HumanTraceStep] = []
        hidden_violation = False
        equiv_failures = 0

        for step_idx in range(max_steps):
            if cur_sec not in self.parsed:
                steps.append(
                    HumanTraceStep(
                        step=step_idx + 1,
                        public_section=cur_sec,
                        internal_unit_id=self.sec_to_unit.get(cur_sec, ""),
                        visible_choices=[],
                        chosen_label="",
                        chosen_dest_section=None,
                        dest_internal_unit_id=None,
                        blocked_reason=f"section {cur_sec} not in parsed gamebook",
                        route_equivalence="FAIL",
                    )
                )
                result.status = "BLOCKED"
                break

            ps = self.parsed[cur_sec]
            visited.add(cur_sec)
            view = HumanDeliveryPlayerView(
                start_filename=self.start_file,
                start_section=self.start_section,
                current_section=ps,
                visited_sections=frozenset(visited),
            )

            try:
                chosen = strat.choose(view, rng)
            except HiddenInformationAccessError:
                hidden_violation = True
                steps.append(
                    HumanTraceStep(
                        step=step_idx + 1,
                        public_section=cur_sec,
                        internal_unit_id=ps.unit_id,
                        visible_choices=list(ps.choices),
                        chosen_label="",
                        chosen_dest_section=None,
                        dest_internal_unit_id=None,
                        blocked_reason="hidden information access attempted",
                        route_equivalence="FAIL",
                        author_only_access_attempted=True,
                    )
                )
                result.status = "BLOCKED"
                break

            if chosen is None:
                if ps.unit_id.startswith("END-"):
                    result.ending_unit_id = ps.unit_id
                    result.status = "COMPLETED"
                    break
                steps.append(
                    HumanTraceStep(
                        step=step_idx + 1,
                        public_section=cur_sec,
                        internal_unit_id=ps.unit_id,
                        visible_choices=list(ps.choices),
                        chosen_label="",
                        chosen_dest_section=None,
                        dest_internal_unit_id=None,
                        blocked_reason="no legal visible choice",
                        route_equivalence="PASS",
                    )
                )
                result.status = "INCOMPLETE"
                break

            dest_sec = chosen.destination_section
            dest_unit = self.sec_to_unit.get(dest_sec, "") if dest_sec else None
            equiv = "PASS"
            if dest_unit and ps.unit_id:
                edge = _check_canonical_edge(self.manifest, ps.unit_id, dest_unit)
                if edge == "FAIL":
                    equiv = "FAIL"
                    equiv_failures += 1

            d20_roll = None
            check_branch = None
            if chosen.branch_kind in ("check_success", "check_failure"):
                check_branch = chosen.branch_kind.replace("check_", "")
                d20_roll = rng.d20()

            steps.append(
                HumanTraceStep(
                    step=step_idx + 1,
                    public_section=cur_sec,
                    internal_unit_id=ps.unit_id,
                    visible_choices=list(ps.choices),
                    chosen_label=chosen.label,
                    chosen_dest_section=dest_sec,
                    dest_internal_unit_id=dest_unit,
                    d20_roll=d20_roll,
                    check_branch=check_branch,
                    player_visible_state=view.snapshot_state(),
                    route_equivalence=equiv,
                )
            )

            if dest_sec is None:
                result.status = "BLOCKED"
                break

            if dest_unit and dest_unit.startswith("END-"):
                result.ending_unit_id = dest_unit
                visited.add(dest_sec)
                result.status = "COMPLETED"
                cur_sec = dest_sec
                break

            cur_sec = dest_sec
        else:
            result.status = "INCOMPLETE"

        result.steps = steps
        result.visited_sections = sorted(visited)
        result.canonical_equivalence = "PASS" if equiv_failures == 0 else "FAIL"
        if result.status == "IN_PROGRESS":
            result.status = "COMPLETED"
        if not skip_trust:
            canonical_status = self._canonical_status()
            result.trust = evaluate_human_delivery_trust(
                delivery_validation_status=delivery["status"],
                gamebook_checks_pass=True,
                visible_navigation_complete=True,
                route_equivalence=result.canonical_equivalence,
                hidden_boundary_violation=hidden_violation,
                canonical_validation_status=canonical_status,
                findings=findings,
            )
        return result

    def monte_carlo(self, runs: int, seed: int, strategy: str = "human_random_legal") -> dict[str, Any]:
        delivery = validate_human_delivery(self.workspace)
        endings: dict[str, int] = {}
        incomplete = 0
        equiv_failures = 0
        hidden_violation = False
        for i in range(runs):
            trace = self.run_trace(
                strategy=strategy, seed=seed + i, max_steps=120, skip_validation=True, skip_trust=True
            )
            if trace.ending_unit_id:
                endings[trace.ending_unit_id] = endings.get(trace.ending_unit_id, 0) + 1
            else:
                incomplete += 1
            if trace.canonical_equivalence == "FAIL":
                equiv_failures += 1
            if any(s.author_only_access_attempted for s in trace.steps):
                hidden_violation = True
        sample = self.run_trace(strategy=strategy, seed=seed, skip_validation=True, skip_trust=True)
        route_equiv = "PASS" if equiv_failures == 0 else "FAIL"
        trust = evaluate_human_delivery_trust(
            delivery_validation_status=delivery["status"],
            gamebook_checks_pass=delivery["status"] == "PASS",
            visible_navigation_complete=delivery["status"] == "PASS",
            route_equivalence=route_equiv,
            hidden_boundary_violation=hidden_violation,
            canonical_validation_status=self._canonical_status(),
            findings=[_finding_from_dict(f) for f in delivery.get("findings", [])],
        )
        return {
            "status": "COMPLETED",
            "runs": runs,
            "strategy": strategy,
            "ending_frequencies": endings,
            "incomplete_runs": incomplete,
            "trust": trust,
            "canonical_equivalence": route_equiv,
            "delivery_validation": delivery,
        }

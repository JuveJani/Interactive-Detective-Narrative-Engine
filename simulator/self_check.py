"""Simulator self-checks and diagnostic confidence gates."""

from __future__ import annotations

from typing import Any

from simulator.endings import evaluate_ending
from simulator.follow_ups import legacy_keyword_follow_ups
from simulator.graph import unreachable_nodes
from simulator.models import Finding
from simulator.state import GameState


class SimulatorSelfCheck:
    """Preconditions that must pass before adventure-blaming findings."""

    def __init__(self, package: dict[str, Any]):
        self.package = package
        self.adapter = package["adapter"]
        self.issues: list[str] = []

    def run_all(self) -> bool:
        self.issues = []
        self._check_e901_synthetic()
        self._check_ending_priority()
        return len(self.issues) == 0

    def _check_e901_synthetic(self) -> None:
        st = GameState(node="J-600", clock=1300)
        st.infers_done = {"I-01", "I-02", "I-03"}
        st.accused = self.adapter["truth"]["culprit"]
        st.clues = {"C-01", "C-04", "C-05", "C-06", "C-12"}
        st.flags = {"MOTIVE_WITNESS"}
        if evaluate_ending(st, self.adapter) != "E-901":
            self.issues.append("E-901 not returned for synthetic valid state")

    def _check_ending_priority(self) -> None:
        st = GameState(node="J-600", clock=1380)
        st.filed_without_accusation = True
        if evaluate_ending(st, self.adapter) != "E-904":
            self.issues.append("Timeout must beat decline (E-904 before E-905)")

    def findings(self) -> list[Finding]:
        if not self.issues:
            return []
        return [
            Finding(
                id="SIM-PRECHECK-FAIL",
                severity="critical",
                confidence="high",
                evidence="; ".join(self.issues),
                file="simulator/self_check.py",
                identifier="SimulatorSelfCheck",
                expected_rule="Simulator correctness preconditions before adventure findings",
                layer="SIMULATOR",
                auto_fix_possible=True,
                human_approval_required=False,
            )
        ]


def _material_ambiguities(adapter: dict[str, Any]) -> list[str]:
    amb = adapter.get("ambiguities", [])
    if not amb:
        return []
    out: list[str] = []
    for item in amb:
        if isinstance(item, dict):
            out.append(item.get("description", item.get("id", str(item))))
        else:
            out.append(str(item))
    return out


def _human_resolution_blockers(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for nid, spec in adapter.get("nodes", {}).items():
        if spec.get("requires_human_resolution"):
            blockers.append(f"{nid} requires human resolution")
    for item in adapter.get("requires_human_resolution", []):
        blockers.append(str(item))
    return blockers


def _infer_retry_blockers(adapter: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for nid, spec in adapter.get("nodes", {}).items():
        if spec.get("type") != "infer":
            continue
        infer_id = spec.get("infer")
        if infer_id != "I-02":
            continue
        if spec.get("blocked_return") and spec.get("blocked_minutes") is None:
            blockers.append(
                f"{nid} I-02 blocked retry has no canonical blocked_minutes in adapter"
            )
        if spec.get("infer_retry_unsupported"):
            blockers.append(f"{nid} I-02 retry marked unsupported")
    return blockers


def simulator_trustworthy(adapter: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return whether Monte Carlo metrics may be reported as trustworthy."""
    blockers: list[str] = []

    ambiguities = _material_ambiguities(adapter)
    if ambiguities:
        blockers.append(f"adapter documents {len(ambiguities)} unresolved ambiguities")

    blockers.extend(_human_resolution_blockers(adapter))
    blockers.extend(_infer_retry_blockers(adapter))

    if legacy_keyword_follow_ups(adapter):
        blockers.append("legacy keyword follow_ups remain active in adapter")

    unsupported = adapter.get("simulator_unsupported", [])
    for item in unsupported:
        blockers.append(item)

    partial = adapter.get("simulator_partial", [])
    for item in partial:
        blockers.append(f"partial support: {item}")

    unreachable = unreachable_nodes(adapter)
    if unreachable:
        blockers.append(f"deterministic reachability failed: {sorted(unreachable)}")

    return len(blockers) == 0, blockers

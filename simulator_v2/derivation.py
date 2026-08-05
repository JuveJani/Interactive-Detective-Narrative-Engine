"""Deterministic derivation from canonical package files."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from simulator_v2.types import CanonicalRef, DerivationStatus

PACKAGE_FILES: dict[str, str] = {
    "world_truth": "DO_NOT_READ/world_truth_package.json",
    "environment": "DO_NOT_READ/environment_package.json",
    "object_interaction": "DO_NOT_READ/object_interaction_package.json",
    "investigation_core": "DO_NOT_READ/investigation_core_package.json",
    "npc_investigation": "DO_NOT_READ/npc_investigation_package.json",
    "investigation_flow": "DO_NOT_READ/investigation_flow_package.json",
    "capability_check": "DO_NOT_READ/capability_check_package.json",
}


@dataclass
class DerivedEntity:
    entity_type: str
    entity_id: str
    ref: CanonicalRef
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "ref": self.ref.to_dict(),
            "payload_keys": sorted(self.payload.keys()),
        }


@dataclass
class DerivationReport:
    adventure_id: str
    play_mode: str
    entities: list[DerivedEntity] = field(default_factory=list)
    fixed_truth_immutable: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    status: str = "OK"

    def to_dict(self) -> dict[str, Any]:
        return {
            "adventure_id": self.adventure_id,
            "play_mode": self.play_mode,
            "status": self.status,
            "entity_count": len(self.entities),
            "entities": [e.to_dict() for e in self.entities],
            "fixed_truth_keys": sorted(self.fixed_truth_immutable.keys()),
            "errors": self.errors,
        }


@dataclass
class CanonicalSimulationModel:
    adventure_id: str
    play_mode: str
    fixed_truth: dict[str, Any]
    locations: dict[str, DerivedEntity]
    objects: dict[str, DerivedEntity]
    npcs: dict[str, DerivedEntity]
    knowledge: dict[str, DerivedEntity]
    hypotheses: dict[str, DerivedEntity]
    conclusions: dict[str, DerivedEntity]
    checks: dict[str, DerivedEntity]
    endings: dict[str, DerivedEntity]
    flow_flags: list[str]
    flow_initial_state: dict[str, Any]
    clocks: list[str]
    raw_packages: dict[str, dict[str, Any]]
    report: DerivationReport

    def entity_by_id(self, entity_id: str) -> DerivedEntity | None:
        for bucket in (
            self.locations,
            self.objects,
            self.npcs,
            self.knowledge,
            self.conclusions,
            self.checks,
            self.endings,
        ):
            if entity_id in bucket:
                return bucket[entity_id]
        return None


def _load_package(adventure_root: Path, rel: str) -> dict[str, Any] | None:
    path = adventure_root / rel
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _derive_list(
    report: DerivationReport,
    package_key: str,
    adventure_root: Path,
    array_key: str,
    entity_type: str,
    id_key: str,
) -> dict[str, DerivedEntity]:
    rel = PACKAGE_FILES[package_key]
    pkg = _load_package(adventure_root, rel)
    out: dict[str, DerivedEntity] = {}
    if not pkg:
        report.errors.append(f"missing package: {rel}")
        return out
    for item in pkg.get(array_key, []) or []:
        if not isinstance(item, dict):
            continue
        eid = str(item.get(id_key, ""))
        if not eid:
            continue
        ref = CanonicalRef(
            canonical_entity_id=eid,
            source_file=rel,
            package_path=rel,
            derivation_status=DerivationStatus.OK,
        )
        entity = DerivedEntity(entity_type=entity_type, entity_id=eid, ref=ref, payload=item)
        out[eid] = entity
        report.entities.append(entity)
    return out


def derive_simulation_model(adventure_root: Path, play_mode: str) -> CanonicalSimulationModel:
    """Build internal simulation model deterministically from canonical packages."""
    adventure_root = adventure_root.resolve()
    wt = _load_package(adventure_root, PACKAGE_FILES["world_truth"]) or {}
    adventure_id = str(wt.get("adventure_id", adventure_root.name))

    report = DerivationReport(adventure_id=adventure_id, play_mode=play_mode)

    fixed_truth = wt.get("fixed_truth", {})
    if not isinstance(fixed_truth, dict):
        fixed_truth = {}
    report.fixed_truth_immutable = json.loads(json.dumps(fixed_truth))

    locations = _derive_list(report, "environment", adventure_root, "locations", "location", "location_id")
    objects = _derive_list(report, "object_interaction", adventure_root, "objects", "object", "object_id")
    npcs = _derive_list(report, "npc_investigation", adventure_root, "npcs", "npc", "npc_id")
    knowledge = _derive_list(
        report, "investigation_core", adventure_root, "knowledge", "knowledge", "knowledge_id"
    )
    conclusions = _derive_list(
        report, "investigation_core", adventure_root, "conclusions", "conclusion", "conclusion_id"
    )
    hypotheses = _derive_list(
        report, "investigation_core", adventure_root, "hypotheses", "hypothesis", "hypothesis_id"
    )
    checks = _derive_list(report, "capability_check", adventure_root, "checks", "check", "check_id")
    endings = _derive_list(report, "investigation_flow", adventure_root, "endings", "ending", "ending_id")

    raw_packages: dict[str, dict[str, Any]] = {}
    for key, rel in PACKAGE_FILES.items():
        pkg = _load_package(adventure_root, rel)
        if pkg:
            raw_packages[key] = pkg

    flow_pkg = raw_packages.get("investigation_flow") or {}
    state_model = flow_pkg.get("state_model", {}) if isinstance(flow_pkg.get("state_model"), dict) else {}
    flow_flags = list(state_model.get("flags", []) or [])
    flow_initial = dict(state_model.get("initial_state", {}) or {})
    time_model = flow_pkg.get("time_model", {}) if isinstance(flow_pkg.get("time_model"), dict) else {}
    clocks = list(time_model.get("clocks", []) or [])

    if report.errors:
        report.status = "BLOCKED"

    return CanonicalSimulationModel(
        adventure_id=adventure_id,
        play_mode=play_mode,
        fixed_truth=report.fixed_truth_immutable,
        locations=locations,
        objects=objects,
        npcs=npcs,
        knowledge=knowledge,
        hypotheses=hypotheses,
        conclusions=conclusions,
        checks=checks,
        endings=endings,
        flow_flags=flow_flags,
        flow_initial_state=flow_initial,
        clocks=clocks,
        raw_packages=raw_packages,
        report=report,
    )

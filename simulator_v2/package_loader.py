"""Load Generator v2 .idne archives and canonical adventure directories."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from idne.idne_package import (
    MANIFEST_NAME,
    PACKAGE_VERSION,
    read_idne_package,
    verify_extracted_package,
)
from idne.validate_adventure.runner import validate_adventure
from simulator_v2.legacy import is_legacy_simulator_path
from simulator_v2.types import SUPPORTED_PACKAGE_VERSIONS, LayerStatus, LoadStatus, PackageLoadResult

SIMULATION_LAYERS: list[tuple[str, str, str]] = [
    ("world_truth", "generation_manifest.json", "DO_NOT_READ/world_truth_package.json"),
    ("environment", "environment_manifest.json", "DO_NOT_READ/environment_package.json"),
    ("object_interaction", "object_interaction_manifest.json", "DO_NOT_READ/object_interaction_package.json"),
    ("investigation_core", "investigation_manifest.json", "DO_NOT_READ/investigation_core_package.json"),
    ("npc_investigation", "npc_investigation_manifest.json", "DO_NOT_READ/npc_investigation_package.json"),
    ("investigation_flow", "investigation_flow_manifest.json", "DO_NOT_READ/investigation_flow_package.json"),
    ("capability_check", "capability_check_manifest.json", "DO_NOT_READ/capability_check_package.json"),
]


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _resolve_adventure_root(path: Path) -> tuple[Path, Path | None, bool]:
    """Return (adventure_root, package_root, is_idne_archive)."""
    path = path.resolve()
    if path.suffix.lower() == ".idne" and path.is_file():
        extract = Path(tempfile.mkdtemp(prefix="sim_v2_"))
        read_result = read_idne_package(path, extract)
        if read_result.adventure_root and read_result.adventure_root.exists():
            return read_result.adventure_root, extract, True
        return extract / "adventure", extract, True

    if (path / MANIFEST_NAME).exists() and (path / "adventure").is_dir():
        return path / "adventure", path, True

    if (path / "generation_manifest.json").exists() or (path / "environment_manifest.json").exists():
        return path, None, False

    if path.is_dir():
        return path, None, False

    raise FileNotFoundError(f"package path not found: {path}")


def _detect_play_mode(adventure_root: Path, package_root: Path | None) -> str:
    candidates: list[Path] = []
    if package_root:
        candidates.append(package_root / "brief" / "adventure_brief.json")
    candidates.extend(
        [
            adventure_root / "brief" / "adventure_brief.json",
            adventure_root / "play_manifest.json",
        ]
    )
    for candidate in candidates:
        data = _read_json(candidate)
        if not data:
            continue
        mode = data.get("player_mode") or data.get("play_modes")
        if isinstance(mode, list) and mode:
            return str(mode[0])
        if isinstance(mode, str):
            return mode

    story_pkg = _read_json(adventure_root / "DO_NOT_READ" / "story_validator_package.json")
    if story_pkg:
        mode = story_pkg.get("player_mode")
        if isinstance(mode, str):
            return mode
    return ""


def _load_generation_state(package_root: Path | None, adventure_root: Path) -> dict[str, str]:
    paths: list[Path] = []
    if package_root:
        paths.append(package_root / "generation" / "generation_state.json")
    paths.append(adventure_root.parent / ".generation" / "generation_state.json")
    for path in paths:
        data = _read_json(path)
        if data and isinstance(data.get("stage_status"), dict):
            return {str(k): str(v) for k, v in data["stage_status"].items()}
    return {}


def _layer_statuses(adventure_root: Path) -> list[LayerStatus]:
    layers: list[LayerStatus] = []
    for layer_id, manifest_rel, package_rel in SIMULATION_LAYERS:
        manifest_path = adventure_root / manifest_rel
        package_path = adventure_root / package_rel
        if layer_id == "world_truth":
            present = manifest_path.exists() and package_path.exists()
        else:
            present = manifest_path.exists() and package_path.exists()
        layers.append(
            LayerStatus(
                layer_id=layer_id,
                manifest_path=manifest_rel,
                package_path=package_rel,
                present=present,
                loaded=present and _read_json(package_path) is not None,
            )
        )
    return layers


def load_simulator_package(path: str | Path) -> PackageLoadResult:
    """Load .idne archive or unpacked canonical directory for Simulator v2."""
    source = Path(path)
    result = PackageLoadResult(status=LoadStatus.FAIL, package_path=source.resolve())

    try:
        adventure_root, package_root, is_archive = _resolve_adventure_root(source)
    except FileNotFoundError as exc:
        result.errors.append(str(exc))
        return result

    result.adventure_root = adventure_root

    if is_legacy_simulator_path(adventure_root):
        result.requires_legacy_adapter = True
        result.status = LoadStatus.BLOCKED
        result.errors.append("legacy adventure requires sim_adapter.json; use legacy simulator")
        return result

    if is_archive and package_root:
        if not verify_extracted_package(package_root):
            read_back = read_idne_package(source, package_root)
            result.checksum_valid = read_back.checksum_valid
            if not result.checksum_valid:
                result.status = LoadStatus.BLOCKED
                result.errors.extend(read_back.errors or ["checksum verification failed"])
                return result
        else:
            result.checksum_valid = True

        manifest = _read_json(package_root / MANIFEST_NAME)
        if manifest:
            result.package_version = str(manifest.get("schema_version", ""))
            result.adventure_id = str(manifest.get("adventure_id", ""))
        else:
            result.package_version = PACKAGE_VERSION
    else:
        result.checksum_valid = True
        result.package_version = PACKAGE_VERSION
        gen = _read_json(adventure_root / "generation_manifest.json")
        if gen:
            result.adventure_id = str(gen.get("adventure_id", adventure_root.name))

    if result.package_version and result.package_version not in SUPPORTED_PACKAGE_VERSIONS:
        result.status = LoadStatus.BLOCKED
        result.errors.append(f"unsupported package version: {result.package_version}")
        return result

    result.layers = _layer_statuses(adventure_root)
    missing = [layer.layer_id for layer in result.layers if not layer.present]
    if missing:
        result.status = LoadStatus.BLOCKED
        result.errors.append(f"missing simulation layers: {', '.join(missing)}")
        return result

    result.play_mode = _detect_play_mode(adventure_root, package_root)
    if not result.play_mode:
        result.status = LoadStatus.BLOCKED
        result.errors.append("play mode not declared in brief or play_manifest")
        return result

    result.generation_stage_status = _load_generation_state(package_root, adventure_root)

    validation = validate_adventure(adventure_root)
    result.integrated_validation_status = validation.status
    result.integrated_validation_failures = list(validation.mandatory_failures)
    if validation.status in ("FAIL", "BLOCKED"):
        result.status = LoadStatus.BLOCKED
        result.errors.append(f"integrated validation {validation.status}")
        return result

    if not result.adventure_id:
        wt = _read_json(adventure_root / "DO_NOT_READ" / "world_truth_package.json")
        if wt:
            result.adventure_id = str(wt.get("adventure_id", ""))

    result.status = LoadStatus.READY
    return result


def cleanup_extracted_package(package_root: Path | None) -> None:
    if package_root and package_root.name.startswith("sim_v2_"):
        shutil.rmtree(package_root, ignore_errors=True)

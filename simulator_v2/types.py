"""Shared types for Simulator v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


SUPPORTED_PACKAGE_VERSIONS = frozenset({"1.0"})


class LoadStatus(str, Enum):
    READY = "READY"
    BLOCKED = "BLOCKED"
    FAIL = "FAIL"


class DerivationStatus(str, Enum):
    OK = "OK"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CanonicalRef:
    """Traceability back to canonical package source."""

    canonical_entity_id: str
    source_file: str
    package_path: str
    derivation_status: DerivationStatus = DerivationStatus.OK

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_entity_id": self.canonical_entity_id,
            "source_file": self.source_file,
            "package_path": self.package_path,
            "derivation_status": self.derivation_status.value,
        }


@dataclass
class LayerStatus:
    layer_id: str
    manifest_path: str
    package_path: str
    present: bool
    loaded: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer_id": self.layer_id,
            "manifest_path": self.manifest_path,
            "package_path": self.package_path,
            "present": self.present,
            "loaded": self.loaded,
        }


@dataclass
class PackageLoadResult:
    status: LoadStatus
    adventure_root: Path | None = None
    package_path: Path | None = None
    package_version: str = ""
    adventure_id: str = ""
    play_mode: str = ""
    checksum_valid: bool = False
    layers: list[LayerStatus] = field(default_factory=list)
    generation_stage_status: dict[str, str] = field(default_factory=dict)
    integrated_validation_status: str = "SKIP"
    integrated_validation_failures: list[str] = field(default_factory=list)
    requires_legacy_adapter: bool = False
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "adventure_root": str(self.adventure_root) if self.adventure_root else None,
            "package_path": str(self.package_path) if self.package_path else None,
            "package_version": self.package_version,
            "adventure_id": self.adventure_id,
            "play_mode": self.play_mode,
            "checksum_valid": self.checksum_valid,
            "layers": [layer.to_dict() for layer in self.layers],
            "generation_stage_status": self.generation_stage_status,
            "integrated_validation_status": self.integrated_validation_status,
            "integrated_validation_failures": self.integrated_validation_failures,
            "requires_legacy_adapter": self.requires_legacy_adapter,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    @property
    def simulation_ready(self) -> bool:
        return (
            self.status == LoadStatus.READY
            and self.checksum_valid
            and all(layer.present for layer in self.layers)
            and self.integrated_validation_status == "PASS"
            and not self.requires_legacy_adapter
        )

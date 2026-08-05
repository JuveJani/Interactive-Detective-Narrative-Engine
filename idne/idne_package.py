"""Unified .idne adventure package builder and reader."""

from __future__ import annotations

import hashlib
import json
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PACKAGE_VERSION = "1.0"
MANIFEST_NAME = "package_manifest.json"
CHECKSUM_NAME = "package_checksum.sha256"


@dataclass
class PackageManifest:
    adventure_id: str
    schema_version: str = PACKAGE_VERSION
    entries: list[dict[str, str]] = field(default_factory=list)
    brief_path: str = "brief/adventure_brief.json"
    generation_state_path: str = "generation/generation_state.json"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "adventure_id": self.adventure_id,
            "entries": self.entries,
            "brief_path": self.brief_path,
            "generation_state_path": self.generation_state_path,
        }


@dataclass
class PackageReadResult:
    status: str
    adventure_root: Path | None = None
    manifest: dict[str, Any] | None = None
    checksum_valid: bool = False
    errors: list[str] = field(default_factory=list)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_adventure_files(adventure_root: Path) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for path in sorted(adventure_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(adventure_root).as_posix()
        if rel.startswith(".generation/"):
            continue
        files.append((rel, path))
    return files


def build_idne_package(
    adventure_root: Path,
    output_path: Path,
    adventure_id: str,
    extra_roots: dict[str, Path] | None = None,
) -> PackageManifest:
    """Create a .idne ZIP from adventure_root and optional generation metadata."""
    adventure_root = adventure_root.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    entries: list[dict[str, str]] = []
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel, path in _collect_adventure_files(adventure_root):
            arc = f"adventure/{rel}"
            zf.write(path, arc)
            entries.append({"path": arc, "sha256": _sha256_file(path)})

        if extra_roots:
            for prefix, root in extra_roots.items():
                root = root.resolve()
                if not root.exists():
                    continue
                for path in sorted(root.rglob("*")):
                    if not path.is_file():
                        continue
                    rel = path.relative_to(root).as_posix()
                    arc = f"{prefix}/{rel}"
                    zf.write(path, arc)
                    entries.append({"path": arc, "sha256": _sha256_file(path)})

        manifest = PackageManifest(adventure_id=adventure_id, entries=entries)
        manifest_bytes = json.dumps(manifest.to_dict(), indent=2).encode("utf-8")
        zf.writestr(MANIFEST_NAME, manifest_bytes)
        entries.append({"path": MANIFEST_NAME, "sha256": hashlib.sha256(manifest_bytes).hexdigest()})

        checksum_lines = [f"{e['sha256']}  {e['path']}" for e in entries]
        checksum_body = "\n".join(checksum_lines) + "\n"
        zf.writestr(CHECKSUM_NAME, checksum_body.encode("utf-8"))

    return manifest


def read_idne_package(package_path: Path, extract_dir: Path) -> PackageReadResult:
    package_path = package_path.resolve()
    extract_dir = extract_dir.resolve()
    extract_dir.mkdir(parents=True, exist_ok=True)

    if not package_path.exists():
        return PackageReadResult(status="FAIL", errors=["package not found"])

    with zipfile.ZipFile(package_path, "r") as zf:
        zf.extractall(extract_dir)

    manifest_path = extract_dir / MANIFEST_NAME
    checksum_path = extract_dir / CHECKSUM_NAME
    if not manifest_path.exists():
        return PackageReadResult(status="FAIL", errors=["missing package_manifest.json"])

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    checksum_valid = True
    errors: list[str] = []

    if checksum_path.exists():
        expected = {}
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, name = line.split("  ", 1)
            expected[name] = digest
        for entry in manifest.get("entries", []):
            rel = entry.get("path", "")
            file_path = extract_dir / rel
            if not file_path.exists():
                checksum_valid = False
                errors.append(f"missing entry: {rel}")
                continue
            actual = _sha256_file(file_path)
            if entry.get("sha256") != actual:
                checksum_valid = False
                errors.append(f"checksum mismatch: {rel}")
            if rel in expected and expected[rel] != actual:
                checksum_valid = False
                errors.append(f"checksum file mismatch: {rel}")
    else:
        checksum_valid = False
        errors.append("missing package_checksum.sha256")

    adventure_root = extract_dir / "adventure"
    status = "PASS" if checksum_valid and not errors else "FAIL"
    return PackageReadResult(
        status=status,
        adventure_root=adventure_root if adventure_root.exists() else None,
        manifest=manifest,
        checksum_valid=checksum_valid,
        errors=errors,
    )


def verify_extracted_package(extract_dir: Path) -> bool:
    """Verify checksums for an already-extracted package directory."""
    extract_dir = extract_dir.resolve()
    manifest_path = extract_dir / MANIFEST_NAME
    checksum_path = extract_dir / CHECKSUM_NAME
    if not manifest_path.exists() or not checksum_path.exists():
        return False
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_lines = {}
    for line in checksum_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        expected_lines[name] = digest
    for entry in manifest.get("entries", []):
        rel = entry.get("path", "")
        file_path = extract_dir / rel
        if not file_path.exists():
            return False
        actual = _sha256_file(file_path)
        if entry.get("sha256") != actual:
            return False
        if rel in expected_lines and expected_lines[rel] != actual:
            return False
    return True


def verify_package_checksum(package_path: Path) -> bool:
    tmp = package_path.parent / f".verify_{package_path.stem}"
    result = read_idne_package(package_path, tmp)
    return result.checksum_valid

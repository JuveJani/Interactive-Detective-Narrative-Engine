"""Shared helpers for Local AI cross-platform tests."""

from __future__ import annotations

from pathlib import Path


def can_create_symlinks(directory: Path) -> bool:
    """Return True when the environment can create and read a directory symlink."""
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / ".idne_symlink_probe_target"
    link = directory / ".idne_symlink_probe_link"
    try:
        target.write_text("probe", encoding="utf-8")
        link.symlink_to(target)
        return link.is_symlink() and link.read_text(encoding="utf-8") == "probe"
    except OSError:
        return False
    finally:
        link.unlink(missing_ok=True)
        target.unlink(missing_ok=True)


def assert_resolved_under(path: Path, root: Path) -> None:
    """Assert that path resolves inside root (raises ValueError if not contained)."""
    path.resolve().relative_to(root.resolve())

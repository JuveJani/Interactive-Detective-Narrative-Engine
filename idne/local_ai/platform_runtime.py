"""Platform detection and runtime paths — sole platform-specific boundary."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from idne.local_ai.paths import find_repo_root


@dataclass(frozen=True)
class PlatformRuntime:
    platform_name: str
    python_version: str
    repo_root: Path
    temp_directory: Path
    user_data_directory: Path
    cache_directory: Path
    path_case_sensitive: bool | None
    subprocess_available: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "platform_name": self.platform_name,
            "python_version": self.python_version,
            "repo_root": self.repo_root.as_posix(),
            "temp_directory": self.temp_directory.as_posix(),
            "user_data_directory": self.user_data_directory.as_posix(),
            "cache_directory": self.cache_directory.as_posix(),
            "path_case_sensitive": self.path_case_sensitive,
            "subprocess_available": self.subprocess_available,
        }


def _detect_case_sensitive(base: Path) -> bool | None:
    probe_dir = base / ".idne_case_probe"
    try:
        probe_dir.mkdir(parents=True, exist_ok=True)
        lower = probe_dir / "case_probe.tmp"
        upper = probe_dir / "CASE_PROBE.TMP"
        lower.write_text("a", encoding="utf-8")
        if upper.exists() and upper.read_text(encoding="utf-8") == "a":
            return False
        return True
    except OSError:
        return None
    finally:
        shutil.rmtree(probe_dir, ignore_errors=True)


def _user_data_root() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or str(Path.home())
        return Path(base) / "IDNE"
    xdg = os.environ.get("XDG_DATA_HOME")
    if xdg:
        return Path(xdg) / "idne"
    return Path.home() / ".local" / "share" / "idne"


def _cache_root() -> Path:
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA") or str(Path.home())
        return Path(base) / "IDNE" / "cache"
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg) / "idne"
    return Path.home() / ".cache" / "idne"


def detect_platform_runtime(start: Path | None = None) -> PlatformRuntime:
    repo_root = find_repo_root(start)
    temp_dir = Path(tempfile.gettempdir())
    user_data = _user_data_root()
    cache_dir = _cache_root()
    subprocess_available = shutil.which("git") is not None or True
    try:
        subprocess.run(
            [sys.executable, "-c", "pass"],
            check=False,
            capture_output=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        subprocess_available = False
    return PlatformRuntime(
        platform_name=platform.platform(),
        python_version=sys.version.split()[0],
        repo_root=repo_root,
        temp_directory=temp_dir,
        user_data_directory=user_data,
        cache_directory=cache_dir,
        path_case_sensitive=_detect_case_sensitive(temp_dir),
        subprocess_available=subprocess_available,
    )


def local_ai_runs_root(repo_root: Path | None = None) -> Path:
    root = repo_root or find_repo_root()
    return root / ".local_ai_runs"

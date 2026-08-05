"""Build mock overlay directories for Adventure Generator v2 tests."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"
MOCK_ROOT = ROOT / "idne" / "generate" / "mock_overlays"

ENV_ONLY = [
    "environment_manifest.json",
    "DO_NOT_READ/environment_package.json",
]

OBJ_ONLY = [
    "object_interaction_manifest.json",
    "DO_NOT_READ/object_interaction_package.json",
]

SOLO_STAGES: dict[str, list[tuple[Path, list[str] | None]]] = {
    "fixed_truth": [(FIXTURES / "wf_valid_minimal", None)],
    "environment": [(FIXTURES / "env_valid_minimal", ENV_ONLY)],
    "objects": [(FIXTURES / "obj_valid_nested", OBJ_ONLY)],
    "investigation_core": [(FIXTURES / "inv_core_valid_minimal", None)],
    "npc_conversation": [(FIXTURES / "npc_valid_minimal", None)],
    "story_player": [(FIXTURES / "sv_valid_solo", None)],
    "playtime": [(FIXTURES / "pt_valid_solo_120", None)],
    "dm_feeling": [(FIXTURES / "df_valid_solo_agency", None)],
}

TWO_PLAYER_STAGES: dict[str, list[tuple[Path, list[str] | None]]] = {
    "fixed_truth": [(FIXTURES / "wf_valid_minimal", None)],
    "story_player": [(FIXTURES / "sv_valid_two_player", None)],
    "playtime": [(FIXTURES / "pt_valid_two_player_max_branch", None)],
    "dm_feeling": [(FIXTURES / "df_valid_two_player", None)],
}


def _copy_fixture_files(src: Path, dest: Path, only: list[str] | None = None) -> None:
    for path in src.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(src)
        rel_s = rel.as_posix()
        if only is not None:
            if not any(rel_s == name or rel_s.endswith("/" + name) for name in only):
                continue
        elif rel.parts[0] not in ("DO_NOT_READ", "PLAYER") and path.suffix != ".json":
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def build_overlays(mode: str, stage_map: dict[str, list[tuple[Path, list[str] | None]]]) -> None:
    base = MOCK_ROOT / mode
    if base.exists():
        shutil.rmtree(base)
    for stage_id, sources in stage_map.items():
        stage_dir = base / stage_id
        stage_dir.mkdir(parents=True, exist_ok=True)
        for src, only in sources:
            _copy_fixture_files(src, stage_dir, only=only)


def build_canonical_fixture(name: str, stage_map: dict[str, list[tuple[Path, list[str] | None]]]) -> None:
    dest = FIXTURES / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for sources in stage_map.values():
        for src, only in sources:
            _copy_fixture_files(src, dest, only=only)


def main() -> None:
    build_overlays("single_investigator", SOLO_STAGES)
    build_overlays("two_player", TWO_PLAYER_STAGES)
    build_canonical_fixture("gen_v2_canonical_solo", SOLO_STAGES)
    build_canonical_fixture("gen_v2_canonical_two_player", TWO_PLAYER_STAGES)
    print("mock overlays and canonical fixtures built")


if __name__ == "__main__":
    main()

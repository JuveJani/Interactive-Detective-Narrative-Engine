#!/usr/bin/env python3
"""Build a complete IDNE adventure from pack_spec.json."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from idne.adventure_pack.pipeline import build_adventure_pack


def main() -> int:
    parser = argparse.ArgumentParser(description="Build IDNE adventure from pack_spec.json")
    parser.add_argument("spec", type=Path, help="Path to pack_spec.json")
    parser.add_argument("--workspace", type=Path, default=None, help="Adventure workspace root")
    parser.add_argument("--no-validate", action="store_true", help="Skip integrated validation")
    args = parser.parse_args()

    result = build_adventure_pack(args.spec, workspace=args.workspace, validate=not args.no_validate)
    print(f"Built {result.workspace.name}")
    print(f"  templates: {result.template_count}")
    print(f"  materialized: {result.materialized_count}")
    print(f"  public sections: {result.public_section_count}")
    print(f"  gamebook bytes: {result.gamebook_bytes}")
    print(f"  generation: {result.generation_seconds:.1f}s")
    if not args.no_validate:
        print(f"  validation: {result.validation_status} ({result.validation_seconds:.1f}s)")
    return 0 if result.validation_status in ("PASS", "CONDITIONAL_PASS", "PENDING") else 1


if __name__ == "__main__":
    raise SystemExit(main())

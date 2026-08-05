"""CLI for integrated adventure validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from idne.validate_adventure.runner import validate_adventure, write_validator_reports


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all applicable IDNE validators on an adventure")
    parser.add_argument("adventure_root", type=Path)
    parser.add_argument("--json", action="store_true", help="Print JSON result")
    args = parser.parse_args(argv)

    result = validate_adventure(args.adventure_root)
    write_validator_reports(args.adventure_root, result)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Overall: {result.status}")
        for name, entry in result.validators.items():
            print(f"  {name}: {entry['status']}")

    if result.status in ("FAIL", "BLOCKED"):
        return 1
    if result.status == "SKIP":
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

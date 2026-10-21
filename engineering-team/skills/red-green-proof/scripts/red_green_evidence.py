#!/usr/bin/env python3
"""Check that a red-green-red evidence record is complete."""

import argparse
import json
import sys


MARKERS = {
    "red_before_fix": "RED_BEFORE_FIX",
    "green_after_fix": "GREEN_AFTER_FIX",
    "red_after_revert": "RED_AFTER_REVERT",
}


def inspect(record):
    """Return marker status for an evidence record."""
    present = {name: marker in record for name, marker in MARKERS.items()}
    missing = [name for name, found in present.items() if not found]
    return {"status": "ok" if not missing else "incomplete", "markers": present, "missing": missing}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check red-green-red evidence markers in a test record."
    )
    parser.add_argument("--file", metavar="PATH", help="Read the record from PATH.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args(argv)

    try:
        if args.file:
            with open(args.file, encoding="utf-8") as handle:
                record = handle.read()
        else:
            record = sys.stdin.read()
    except OSError as exc:
        parser.error(str(exc))

    result = inspect(record)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Evidence: {result['status']}")
        for name, found in result["markers"].items():
            print(f"  {'present' if found else 'missing'}: {name}")
    return 0 if result["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())

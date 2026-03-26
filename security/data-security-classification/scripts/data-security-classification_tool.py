#!/usr/bin/env python3
"""Data Security & Classification CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Data Security & Classification helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "data-security-classification",
        "agent_name": "Data Security & Classification",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L2"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Data Security & Classification tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

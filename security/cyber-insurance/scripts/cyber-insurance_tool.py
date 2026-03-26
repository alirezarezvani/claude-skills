#!/usr/bin/env python3
"""Cyber Insurance CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Cyber Insurance helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "cyber-insurance",
        "agent_name": "Cyber Insurance",
        "status": "ok",
        "phase": "phase3",
        "plane": "work",
        "level": "L1"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Cyber Insurance tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Threat Hunting CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Threat Hunting helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "threat-hunting",
        "agent_name": "Threat Hunting",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L3"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Threat Hunting tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

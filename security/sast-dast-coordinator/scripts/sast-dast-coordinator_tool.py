#!/usr/bin/env python3
"""SAST/DAST Coordinator CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="SAST/DAST Coordinator helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "sast-dast-coordinator",
        "agent_name": "SAST/DAST Coordinator",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L4"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"SAST/DAST Coordinator tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

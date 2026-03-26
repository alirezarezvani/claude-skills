#!/usr/bin/env python3
"""Tool Execution Broker CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Tool Execution Broker helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "tool-execution-broker",
        "agent_name": "Tool Execution Broker",
        "status": "ok",
        "phase": "mvp",
        "plane": "work",
        "level": "L3"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Tool Execution Broker tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

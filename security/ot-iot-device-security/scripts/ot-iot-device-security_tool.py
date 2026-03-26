#!/usr/bin/env python3
"""OT/IoT/Device Security CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="OT/IoT/Device Security helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "ot-iot-device-security",
        "agent_name": "OT/IoT/Device Security",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L4"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"OT/IoT/Device Security tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

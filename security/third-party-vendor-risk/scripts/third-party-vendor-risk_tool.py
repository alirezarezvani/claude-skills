#!/usr/bin/env python3
"""Third-Party & Vendor Risk CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Third-Party & Vendor Risk helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "third-party-vendor-risk",
        "agent_name": "Third-Party & Vendor Risk",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L2"
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Third-Party & Vendor Risk tool executed: {payload['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""CISO Brief Generator CLI helper for USAP skill package."""

import argparse
import json


BRIEF_TYPES = [
    "board_quarterly",
    "monthly_ciso_report",
    "incident_executive_summary",
    "regulatory_update",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="CISO Brief Generator helper")
    parser.add_argument(
        "--brief-type",
        choices=BRIEF_TYPES,
        default="monthly_ciso_report",
        help="Type of brief to generate"
    )
    parser.add_argument("--input", type=str, help="Path to JSON input with security data")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "ciso-brief-generator",
        "agent_name": "CISO Brief Generator",
        "status": "ok",
        "phase": "phase3",
        "plane": "governance",
        "level": "L2",
        "brief_type": args.brief_type,
        "available_brief_types": BRIEF_TYPES,
        "human_approval_required": True
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"CISO Brief Generator tool executed: {payload['status']}")
        print(f"Brief type: {args.brief_type}")
        print("Human approval required before distribution: True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

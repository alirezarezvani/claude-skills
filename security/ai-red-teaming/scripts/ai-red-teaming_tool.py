#!/usr/bin/env python3
"""AI Red Teaming CLI helper for USAP skill package."""

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Red Teaming helper")
    parser.add_argument("--input", type=str, help="Path to JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "ai-red-teaming",
        "agent_name": "AI Red Teaming",
        "status": "ok",
        "phase": "phase2",
        "plane": "work",
        "level": "L4",
        "authorization_required": True,
        "test_tracks": [
            "prompt-injection",
            "jailbreak",
            "model-inversion",
            "adversarial-examples",
            "data-poisoning"
        ]
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"AI Red Teaming tool executed: {payload['status']}")
        print(f"Authorization required: {payload['authorization_required']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

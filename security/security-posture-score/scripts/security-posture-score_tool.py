#!/usr/bin/env python3
"""Security Posture Score CLI helper for USAP skill package."""

import argparse
import json


SCORE_DOMAINS = [
    "detection",
    "response",
    "identity-access",
    "cloud-infrastructure",
    "appsec-devsecops",
    "governance-compliance",
    "red-team-resilience",
]

SCORE_TIERS = [
    (90, "Excellent"),
    (75, "Good"),
    (60, "Fair"),
    (40, "Poor"),
    (0, "Critical"),
]


def score_to_tier(score: float) -> str:
    for threshold, label in SCORE_TIERS:
        if score >= threshold:
            return label
    return "Critical"


def main() -> int:
    parser = argparse.ArgumentParser(description="Security Posture Score helper")
    parser.add_argument("--input", type=str, help="Path to JSON input with domain scores")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "security-posture-score",
        "agent_name": "Security Posture Score",
        "status": "ok",
        "phase": "phase3",
        "plane": "governance",
        "level": "L3",
        "scored_domains": SCORE_DOMAINS,
        "score_tiers": {label: threshold for threshold, label in SCORE_TIERS}
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Security Posture Score tool executed: {payload['status']}")
        print(f"Scored domains: {len(SCORE_DOMAINS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

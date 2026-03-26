#!/usr/bin/env python3
"""AppSec Code Review CLI helper for USAP skill package."""

import argparse
import json


OWASP_CATEGORIES = [
    "A01: Broken Access Control",
    "A02: Cryptographic Failures",
    "A03: Injection",
    "A04: Insecure Design",
    "A05: Security Misconfiguration",
    "A06: Vulnerable and Outdated Components",
    "A07: Identification and Authentication Failures",
    "A08: Software and Data Integrity Failures",
    "A09: Security Logging and Monitoring Failures",
    "A10: Server-Side Request Forgery",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="AppSec Code Review helper")
    parser.add_argument("--input", type=str, help="Path to JSON input with PR diff context")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "appsec-code-review",
        "agent_name": "AppSec Code Review",
        "status": "ok",
        "phase": "phase1",
        "plane": "work",
        "level": "L4",
        "owasp_coverage": OWASP_CATEGORIES,
        "gate_decisions": ["block", "warn", "pass"]
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"AppSec Code Review tool executed: {payload['status']}")
        print(f"OWASP coverage: {len(OWASP_CATEGORIES)} categories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Pipeline Security Scan CLI helper for USAP skill package."""

import argparse
import json


SCAN_CATEGORIES = [
    "secrets-in-env-vars",
    "missing-sast-stage",
    "missing-sca-stage",
    "missing-secrets-scan-stage",
    "artifact-signing-gap",
    "sbom-generation-gap",
    "unpinned-actions",
    "overly-permissive-pipeline-tokens",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Pipeline Security Scan helper")
    parser.add_argument("--input", type=str, help="Path to pipeline YAML file or JSON input")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--json", action="store_true", help="Output as JSON (alias for --output json)")
    args = parser.parse_args()
    if args.json:
        args.output = "json"

    payload = {
        "agent_slug": "pipeline-security-scan",
        "agent_name": "Pipeline Security Scan",
        "status": "ok",
        "phase": "phase1",
        "plane": "work",
        "level": "L4",
        "scan_categories": SCAN_CATEGORIES,
        "supported_pipelines": [
            "github-actions",
            "gitlab-ci",
            "jenkins",
            "circleci",
            "bitbucket-pipelines"
        ]
    }

    if args.output == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"Pipeline Security Scan tool executed: {payload['status']}")
        print(f"Scan categories: {len(SCAN_CATEGORIES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

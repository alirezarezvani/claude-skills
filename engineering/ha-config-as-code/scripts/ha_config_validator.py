#!/usr/bin/env python3
"""
ha_config_validator.py — Validate Home Assistant entity IDs and config health.

Checks:
  - HA connectivity and token validity
  - Expected entity IDs actually exist in live HA
  - Entities in unavailable/unknown state
  - Automations with no active trigger

Usage:
    python3 ha_config_validator.py                    # full validation
    python3 ha_config_validator.py --check-entities   # entity existence only
    python3 ha_config_validator.py --entities-file expected_entities.txt
    python3 ha_config_validator.py --json             # JSON output for CI
    python3 ha_config_validator.py --fail-on-warnings # exit 1 on any warning
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from ha_api import HAAPI
except ImportError:
    sys.exit("ha_api.py must be in the same directory.")

# ---------------------------------------------------------------------------
# Default expected entities — edit to match your home
# ---------------------------------------------------------------------------
DEFAULT_EXPECTED_ENTITIES = [
    # Add your critical entity IDs here
    # "light.living_room",
    # "switch.main_switch",
    # "sensor.temperature_bedroom",
]


def check_connectivity(api: HAAPI) -> dict:
    ok = api.ping()
    return {
        "check": "connectivity",
        "status": "pass" if ok else "fail",
        "detail": "HA API reachable" if ok else "Cannot reach HA — check HA_URL and HA_TOKEN",
    }


def check_expected_entities(api: HAAPI, expected: list) -> list:
    if not expected:
        return []
    try:
        states = api.get_states()
    except Exception as e:
        return [{"check": "expected_entities", "status": "fail", "detail": str(e)}]

    live_ids = {s["entity_id"] for s in states}
    results = []
    for eid in expected:
        if eid in live_ids:
            results.append({"check": "expected_entity", "status": "pass", "entity_id": eid})
        else:
            results.append({
                "check": "expected_entity",
                "status": "fail",
                "entity_id": eid,
                "detail": "Entity not found in live HA",
            })
    return results


def check_unavailable_entities(api: HAAPI) -> list:
    try:
        states = api.get_states()
    except Exception as e:
        return [{"check": "unavailable_entities", "status": "fail", "detail": str(e)}]

    bad_states = ("unavailable", "unknown")
    unavailable = [
        s for s in states
        if s["state"] in bad_states
        and not s["entity_id"].startswith(("update.", "binary_sensor.updater"))
    ]
    if not unavailable:
        return [{"check": "unavailable_entities", "status": "pass", "detail": "All entities reachable"}]

    results = []
    for s in unavailable:
        results.append({
            "check": "unavailable_entity",
            "status": "warn",
            "entity_id": s["entity_id"],
            "state": s["state"],
            "friendly_name": s.get("attributes", {}).get("friendly_name", ""),
        })
    return results


def check_automations(api: HAAPI) -> list:
    try:
        autos = api.list_automations()
    except Exception as e:
        return [{"check": "automations", "status": "fail", "detail": str(e)}]

    disabled = [
        a for a in autos
        if a.get("state") == "off"
    ]
    results = [{"check": "automations", "status": "pass", "detail": f"{len(autos)} automations found"}]
    for a in disabled:
        results.append({
            "check": "automation_disabled",
            "status": "warn",
            "entity_id": a["entity_id"],
            "friendly_name": a.get("attributes", {}).get("friendly_name", ""),
        })
    return results


def run_validation(api: HAAPI, expected_entities: list, checks: list) -> list:
    results = []

    if "connectivity" in checks:
        conn = check_connectivity(api)
        results.append(conn)
        if conn["status"] == "fail":
            return results  # no point continuing

    if "entities" in checks:
        results.extend(check_expected_entities(api, expected_entities))

    if "unavailable" in checks:
        results.extend(check_unavailable_entities(api))

    if "automations" in checks:
        results.extend(check_automations(api))

    return results


def print_results(results: list):
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for r in results:
        status = r.get("status", "?")
        counts[status] = counts.get(status, 0) + 1
        icon = {"pass": "✓", "warn": "⚠", "fail": "✗"}.get(status, "?")
        line = f"  [{icon}] {r.get('check', '')}"
        if "entity_id" in r:
            line += f"  {r['entity_id']}"
        if "detail" in r:
            line += f"  — {r['detail']}"
        print(line)
    print()
    print(f"  PASS: {counts['pass']}  WARN: {counts['warn']}  FAIL: {counts['fail']}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate Home Assistant configuration health",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--check-entities", action="store_true",
                        help="Only run entity existence checks")
    parser.add_argument("--entities-file",
                        help="Path to text file with one entity_id per line")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fail-on-warnings", action="store_true",
                        help="Exit 1 if any warnings found")
    args = parser.parse_args()

    api = HAAPI()

    # Load expected entities
    expected = list(DEFAULT_EXPECTED_ENTITIES)
    if args.entities_file:
        try:
            with open(args.entities_file) as f:
                expected = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except FileNotFoundError:
            sys.exit(f"Entities file not found: {args.entities_file}")

    # Select checks
    if args.check_entities:
        checks = ["connectivity", "entities"]
    else:
        checks = ["connectivity", "entities", "unavailable", "automations"]

    results = run_validation(api, expected, checks)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("\nHome Assistant Configuration Validation")
        print("=" * 50)
        print_results(results)

    has_fail = any(r.get("status") == "fail" for r in results)
    has_warn = any(r.get("status") == "warn" for r in results)

    if has_fail:
        sys.exit(1)
    if args.fail_on_warnings and has_warn:
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
ha_automation_diff.py — Diff local automation definitions vs live Home Assistant state.

Compares a local YAML/JSON file of automation configs against what is currently
deployed in HA, reporting:
  - Automations present locally but missing from HA  (MISSING)
  - Automations present in HA but not defined locally (EXTRA)
  - Automations present in both                      (MATCH)

Usage:
    python3 ha_automation_diff.py                            # diff only (no local file = HA-only report)
    python3 ha_automation_diff.py --local automations.yaml   # compare against YAML
    python3 ha_automation_diff.py --local automations.json   # compare against JSON
    python3 ha_automation_diff.py --json                     # JSON output
    python3 ha_automation_diff.py --list-live                # list all live automations
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

try:
    import yaml as _yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_local_automations(path: str) -> dict:
    """Load automations from YAML or JSON file. Returns dict keyed by alias."""
    with open(path) as f:
        content = f.read()

    if path.endswith(".yaml") or path.endswith(".yml"):
        if not HAS_YAML:
            sys.exit("PyYAML required for YAML files: pip install pyyaml")
        data = _yaml.safe_load(content)
    else:
        data = json.loads(content)

    # Accept either a list or a dict keyed by alias
    if isinstance(data, list):
        return {item["alias"]: item for item in data if "alias" in item}
    elif isinstance(data, dict):
        return data
    else:
        sys.exit("Local automations file must be a list or dict")


def get_live_automations(api: HAAPI) -> dict:
    """Fetch live automations from HA. Returns dict keyed by alias/friendly_name."""
    try:
        autos = api.list_automations()
    except Exception as e:
        sys.exit(f"Error fetching automations from HA: {e}")

    result = {}
    for a in autos:
        attrs = a.get("attributes", {})
        key = attrs.get("friendly_name") or a["entity_id"]
        result[key] = {
            "entity_id": a["entity_id"],
            "state": a["state"],
            "friendly_name": attrs.get("friendly_name", ""),
            "last_triggered": attrs.get("last_triggered"),
            "mode": attrs.get("mode", "single"),
        }
    return result


def diff(local: dict, live: dict) -> list:
    local_keys = set(local.keys())
    live_keys = set(live.keys())

    results = []

    for key in sorted(local_keys - live_keys):
        results.append({"alias": key, "status": "MISSING", "detail": "Defined locally but not found in HA"})

    for key in sorted(live_keys - local_keys):
        info = live[key]
        results.append({
            "alias": key,
            "status": "EXTRA",
            "entity_id": info["entity_id"],
            "ha_state": info["state"],
            "detail": "Present in HA but not in local definitions",
        })

    for key in sorted(local_keys & live_keys):
        info = live[key]
        results.append({
            "alias": key,
            "status": "MATCH",
            "entity_id": info["entity_id"],
            "ha_state": info["state"],
        })

    return results


def print_diff(results: list):
    counts = {"MISSING": 0, "EXTRA": 0, "MATCH": 0}
    icons = {"MISSING": "✗", "EXTRA": "⚠", "MATCH": "✓"}

    for r in results:
        status = r["status"]
        counts[status] = counts.get(status, 0) + 1
        icon = icons.get(status, "?")
        line = f"  [{icon}] {status:<8} {r['alias']}"
        if "ha_state" in r:
            line += f"  (state: {r['ha_state']})"
        if status in ("MISSING", "EXTRA"):
            print(line)

    print()
    for r in results:
        if r["status"] == "MATCH":
            icon = icons["MATCH"]
            line = f"  [{icon}] MATCH    {r['alias']}  (state: {r.get('ha_state', '?')})"
            print(line)

    print()
    print(f"  MATCH: {counts['MATCH']}  MISSING: {counts['MISSING']}  EXTRA: {counts['EXTRA']}")


def main():
    parser = argparse.ArgumentParser(
        description="Diff local automation definitions vs live HA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--local", help="Path to local automations YAML or JSON file")
    parser.add_argument("--list-live", action="store_true", help="List all live HA automations and exit")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    api = HAAPI()
    live = get_live_automations(api)

    if args.list_live:
        if args.json:
            print(json.dumps(list(live.values()), indent=2, ensure_ascii=False))
        else:
            print(f"\nLive automations in HA ({len(live)} total):\n")
            for alias, info in sorted(live.items()):
                state_str = f"[{info['state']}]"
                print(f"  {state_str:<8} {alias}  ({info['entity_id']})")
        return

    if not args.local:
        # No local file — just show what's in HA
        if args.json:
            print(json.dumps(list(live.values()), indent=2, ensure_ascii=False))
        else:
            print(f"\nNo --local file provided. Showing live HA automations ({len(live)} total):\n")
            for alias, info in sorted(live.items()):
                state_str = f"[{info['state']}]"
                print(f"  {state_str:<8} {alias}")
        return

    if not os.path.exists(args.local):
        sys.exit(f"Local file not found: {args.local}")

    local = load_local_automations(args.local)
    results = diff(local, live)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\nAutomation Diff: {args.local} vs live HA")
        print("=" * 60)
        print_diff(results)

    has_missing = any(r["status"] == "MISSING" for r in results)
    if has_missing:
        sys.exit(1)


if __name__ == "__main__":
    main()

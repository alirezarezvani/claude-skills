#!/usr/bin/env python3
"""
ha_entity_lister.py — List and filter live Home Assistant entities.

Usage:
    python3 ha_entity_lister.py                        # all entities
    python3 ha_entity_lister.py --domain light         # lights only
    python3 ha_entity_lister.py --domain switch --state on
    python3 ha_entity_lister.py --keyword bedroom      # name/ID contains keyword
    python3 ha_entity_lister.py --json                 # machine-readable output
    python3 ha_entity_lister.py --domain sensor --json | jq '.[] | .entity_id'
"""

import argparse
import json
import os
import sys

# Allow running as standalone or as part of skill
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from ha_api import HAAPI
except ImportError:
    sys.exit("ha_api.py must be in the same directory.")


def filter_entities(
    states,
    domain: str = None,
    state_filter: str = None,
    keyword: str = None,
):
    results = states
    if domain:
        results = [s for s in results if s["entity_id"].startswith(f"{domain}.")]
    if state_filter:
        results = [s for s in results if s["state"] == state_filter]
    if keyword:
        kw = keyword.lower()
        results = [
            s for s in results
            if kw in s["entity_id"].lower()
            or kw in s.get("attributes", {}).get("friendly_name", "").lower()
        ]
    return results


def print_table(entities):
    if not entities:
        print("No entities found.")
        return
    col_id = max(len(s["entity_id"]) for s in entities)
    col_state = max(len(s["state"]) for s in entities)
    col_id = max(col_id, 9)
    col_state = max(col_state, 5)
    fmt = f"{{:<{col_id}}}  {{:<{col_state}}}  {{}}"
    print(fmt.format("ENTITY_ID", "STATE", "FRIENDLY NAME"))
    print("-" * (col_id + col_state + 40))
    for s in entities:
        name = s.get("attributes", {}).get("friendly_name", "")
        print(fmt.format(s["entity_id"], s["state"], name))


def main():
    parser = argparse.ArgumentParser(
        description="List and filter Home Assistant entities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--domain", help="Filter by domain (e.g. light, switch, sensor)")
    parser.add_argument("--state", dest="state_filter", help="Filter by state value (e.g. on, off, unavailable)")
    parser.add_argument("--keyword", help="Filter by keyword in entity_id or friendly_name")
    parser.add_argument("--json", action="store_true", help="Output as JSON array")
    parser.add_argument("--count", action="store_true", help="Print count only")
    args = parser.parse_args()

    api = HAAPI()

    try:
        states = api.get_states()
    except Exception as e:
        sys.exit(f"Error connecting to Home Assistant: {e}")

    entities = filter_entities(
        states,
        domain=args.domain,
        state_filter=args.state_filter,
        keyword=args.keyword,
    )

    if args.count:
        print(len(entities))
        return

    if args.json:
        output = [
            {
                "entity_id": s["entity_id"],
                "state": s["state"],
                "friendly_name": s.get("attributes", {}).get("friendly_name", ""),
                "attributes": s.get("attributes", {}),
            }
            for s in entities
        ]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_table(entities)
        print(f"\nTotal: {len(entities)}")


if __name__ == "__main__":
    main()

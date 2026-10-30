#!/usr/bin/env python3
"""List every installable skill and its eval coverage (trigger cases, behaviour cases).

Usage:
  python3 scripts/evals/inventory.py              # coverage summary
  python3 scripts/evals/inventory.py --missing    # skills with no trigger cases
  python3 scripts/evals/inventory.py --json       # full inventory as JSON
"""
import argparse
import json

from common import inventory, load_cases


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="print the inventory as JSON")
    ap.add_argument("--missing", action="store_true", help="list skills without trigger cases")
    args = ap.parse_args()
    inv = inventory()
    trig = load_cases("trigger_cases.json")
    beh = load_cases("behaviour_cases.json")
    beh_paths = {c["skill"] for c in beh.values()}
    for r in inv:
        r["trigger_cases"] = r["path"] in trig
        r["behaviour_cases"] = r["path"] in beh_paths
    if args.json:
        print(json.dumps(inv, indent=1))
    elif args.missing:
        for r in inv:
            if not r["trigger_cases"]:
                print(r["path"])
    else:
        t = sum(r["trigger_cases"] for r in inv)
        b = sum(r["behaviour_cases"] for r in inv)
        print(f"skills: {len(inv)}  with trigger cases: {t}  with behaviour cases: {b}")


if __name__ == "__main__":
    main()

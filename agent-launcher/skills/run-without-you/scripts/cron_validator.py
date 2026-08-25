#!/usr/bin/env python3
"""cron_validator.py — validate a 5-field POSIX cron expression + IANA timezone.

CMA scheduled deployments use standard 5-field POSIX cron (minute granularity)
with an IANA timezone and wall-clock DST semantics. This validates the shape and
ranges, resolves the timezone against the local zoneinfo database when available,
and prints the DST behavior note. Exit 0 valid, 1 invalid. Stdlib-only.

Fields: minute(0-59) hour(0-23) day-of-month(1-31) month(1-12) day-of-week(0-6).
Each supports *, a-b ranges, a,b,c lists, and */step.

Examples:
  cron_validator.py --cron "0 9 * * *" --timezone Europe/Berlin
  cron_validator.py --cron "*/15 0-6 * * 1-5" --timezone America/New_York
  cron_validator.py --sample
"""
import argparse
import json
import sys

RANGES = [(0, 59), (0, 23), (1, 31), (1, 12), (0, 6)]
NAMES = ["minute", "hour", "day-of-month", "month", "day-of-week"]


def _valid_field(field: str, lo: int, hi: int):
    for part in field.split(","):
        if part == "*":
            continue
        step_base, _, step = part.partition("/")
        if step:
            if not step.isdigit() or int(step) < 1:
                return False, f"bad step '{part}'"
        if step_base == "*" or step_base == "":
            continue
        if "-" in step_base:
            a, _, b = step_base.partition("-")
            if not (a.isdigit() and b.isdigit()):
                return False, f"bad range '{part}'"
            a, b = int(a), int(b)
            if a < lo or b > hi or a > b:
                return False, f"range '{part}' outside {lo}-{hi}"
        else:
            if not step_base.isdigit():
                return False, f"non-numeric '{part}'"
            v = int(step_base)
            if v < lo or v > hi:
                return False, f"value {v} outside {lo}-{hi}"
    return True, None


def validate_cron(expr: str):
    fields = expr.split()
    if len(fields) != 5:
        return False, [f"expected 5 fields, got {len(fields)}: {expr!r}"]
    errors = []
    for field, (lo, hi), name in zip(fields, RANGES, NAMES):
        ok, err = _valid_field(field, lo, hi)
        if not ok:
            errors.append(f"{name}: {err}")
    return (not errors), errors


def validate_tz(tz: str):
    if not tz:
        return False, "no timezone given (IANA id required, e.g. Europe/Berlin)"
    try:
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
        try:
            ZoneInfo(tz)
            return True, None
        except ZoneInfoNotFoundError:
            return False, f"IANA timezone '{tz}' not found in the zoneinfo database"
    except ImportError:
        # zoneinfo unavailable; do a light sanity check.
        if "/" in tz or tz in ("UTC",):
            return True, "zoneinfo unavailable; shape looks like an IANA id (not verified)"
        return False, f"'{tz}' does not look like an IANA id and zoneinfo is unavailable"


DST_NOTE = ("Wall-clock DST: the expression fires at literal local time. On "
            "spring-forward, a nonexistent local time is skipped; on fall-back, a "
            "repeated local time fires twice. Avoid scheduling 02:00-03:00 in "
            "DST-observing zones if exactly-once matters.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a 5-field POSIX cron + IANA timezone for a CMA deployment.")
    ap.add_argument("--cron", help="5-field cron expression.")
    ap.add_argument("--timezone", default="UTC")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        for expr, tz in [("0 9 * * *", "Europe/Berlin"), ("*/15 0-6 * * 1-5", "America/New_York"),
                         ("0 25 * * *", "UTC"), ("0 9 * *", "Mars/Olympus")]:
            ok, errs = validate_cron(expr)
            tzok, tznote = validate_tz(tz)
            print(f"[{'OK ' if ok and tzok else 'BAD'}] {expr!r} @ {tz}: "
                  f"{'valid' if ok else errs}; tz {'valid' if tzok else tznote}")
        print(f"\n{DST_NOTE}")
        return 0

    if not args.cron:
        print("Provide --cron.", file=sys.stderr)
        return 2
    ok, errs = validate_cron(args.cron)
    tzok, tznote = validate_tz(args.timezone)
    result = {"cron": args.cron, "cron_valid": ok, "cron_errors": errs,
              "timezone": args.timezone, "timezone_valid": tzok, "timezone_note": tznote,
              "dst_note": DST_NOTE}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"cron:     {'VALID' if ok else 'INVALID'} — {args.cron}")
        for e in errs:
            print(f"  - {e}")
        print(f"timezone: {'VALID' if tzok else 'INVALID'} — {args.timezone}")
        if tznote:
            print(f"  {tznote}")
        print(f"DST: {DST_NOTE}")
    return 0 if (ok and tzok) else 1


if __name__ == "__main__":
    raise SystemExit(main())

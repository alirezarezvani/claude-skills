#!/usr/bin/env python3
"""Log a self-model regeneration event and clean up the .self-model-stale flag.

Called by AI after regenerating self-model.md.
This is the MECHANICAL step that replaces the prose-based "delete flag" instruction.

Usage:
  python log-regeneration.py --old v1 --new v2 --sources "2026-07-02,2026-07-01" --trigger flag

The script (crash-consistent ordering):
  1. Appends JSONL audit record FIRST (so a crash here leaves the flag intact)
  2. Deletes the .self-model-stale flag SECOND (so recovery is always possible)
  3. Verifies the log file exists after write

If step 1 crashes: flag persists → health-check.py re-detects next session.
If step 2 crashes: audit already exists → health-check.py cleans orphaned flag.

Together with quality-gate.py (writes flag) and health-check.py (SessionStart detection),
this forms the complete mechanical lifecycle of the strange-loop flag.

Configuration:
  - MEMORY_DIR env var: path to memory directory (default: ~/.claude/memory)
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

MEMORY = Path(os.environ.get("MEMORY_DIR", Path.home() / ".claude" / "memory"))
REGENERATION_LOG = MEMORY / ".self-model-regeneration.jsonl"
STALE_FLAG = MEMORY / ".self-model-stale"


def main():
    parser = argparse.ArgumentParser(
        description="Log self-model regeneration event and clean up stale flag"
    )
    parser.add_argument("--old", required=True, help="Old self-model version (e.g. v1)")
    parser.add_argument("--new", required=True, help="New self-model version (e.g. v2)")
    parser.add_argument("--sources", required=True,
                        help="Comma-separated source identifiers (growth-log entry dates)")
    parser.add_argument("--trigger", default="flag",
                        help="What triggered regeneration (default: flag)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON to stdout")
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).isoformat()
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]

    result = {
        "success": True,
        "timestamp": timestamp,
        "trigger": args.trigger,
        "sources": sources,
        "old_version": args.old,
        "new_version": args.new,
        "flag_cleaned": False,
        "log_appended": False,
        "log_verified": False,
    }

    # 1. Append JSONL audit record FIRST (crash-safe: flag persists if this fails)
    record = {
        "timestamp": timestamp,
        "trigger": args.trigger,
        "sources": sources,
        "old_version": args.old,
        "new_version": args.new,
        "flag_cleaned": STALE_FLAG.exists(),
    }
    try:
        with open(REGENERATION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
        result["log_appended"] = True
        if not args.json:
            print(f"REGEN_LOG: appended (v{args.old} → v{args.new})")
    except OSError as e:
        result["success"] = False
        result["error"] = str(e)
        if not args.json:
            print(f"REGEN_LOG:ERROR: {e}", file=sys.stderr)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 2. Verify the log write succeeded before we touch the flag
    if REGENERATION_LOG.exists():
        result["log_verified"] = True
        if not args.json:
            print(f"REGEN_LOG: verified ({REGENERATION_LOG.stat().st_size} bytes)")
    else:
        result["success"] = False
        result["error"] = "log file not found after write"
        if not args.json:
            print("REGEN_LOG:WARN: log file not found after write", file=sys.stderr)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 3. Delete the .self-model-stale flag SECOND (audit record is already safe)
    if STALE_FLAG.exists():
        try:
            STALE_FLAG.unlink()
            result["flag_cleaned"] = True
            if not args.json:
                print("REGEN_FLAG: deleted .self-model-stale")
        except OSError as e:
            result["error"] = str(e)
            if not args.json:
                print(f"REGEN_FLAG:ERROR: {e}", file=sys.stderr)
    else:
        result["flag_cleaned"] = False
        if not args.json:
            print("REGEN_FLAG: not found (already cleaned or never existed)")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

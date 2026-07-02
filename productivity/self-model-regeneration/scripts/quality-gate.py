#!/usr/bin/env python3
"""Stop hook — checks 5 databases + self-model staleness. Exits 2 (hard block) when stale.

Part of the self-model regeneration loop:
  - Compares self-model.md mtime against all growth-log entries
  - Uses >= comparison for FAT32 2s resolution safety
  - Writes .self-model-stale flag if growth data is newer than self-model
  - Exit codes: 0=clean, 1=warnings (backfillable), 2=hard block (regeneration needed)

Configuration:
  - MEMORY_DIR env var: path to memory directory (default: ~/.claude/memory)
  - STALE_DAYS_WARN: days before a database is considered stale (default: 3)
  - STALE_DAYS_CRITICAL: days before stale is critical (default: 7)
"""

import os
import sys
import json
import argparse
import platform
from pathlib import Path
from datetime import datetime, timezone

# ── Configuration ──────────────────────────────────────────────────────────

HOME = Path.home()
MEMORY_DIR = Path(os.environ.get("MEMORY_DIR", str(HOME / ".claude" / "memory")))
STALE_FLAG = MEMORY_DIR / ".self-model-stale"
STALE_DAYS_WARN = int(os.environ.get("STALE_DAYS_WARN", "3"))
STALE_DAYS_CRITICAL = int(os.environ.get("STALE_DAYS_CRITICAL", "7"))

# Fix Windows GBK encoding
if platform.system() == "Windows" and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ── Helpers ────────────────────────────────────────────────────────────────

def days_since(dt):
    """Return days since given datetime, or None if dt is None."""
    if dt is None:
        return None
    return (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0


def _mtime_or_none(path):
    """Return mtime as UTC datetime, or None if file doesn't exist."""
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except OSError:
        return None


def _find_persona():
    """Find persona-portrait file, falling back to underscore variant."""
    candidates = sorted(MEMORY_DIR.glob("persona-portrait*.md"))
    if not candidates:
        candidates = sorted(MEMORY_DIR.glob("persona_portrait*.md"))
    if candidates:
        return candidates[-1]
    return MEMORY_DIR / "persona_portrait.md"


# ── Database Checks ────────────────────────────────────────────────────────

def check_databases():
    """Check freshness of all 5 databases. Returns list of (name, days, level)."""
    dbs = {
        "growth-log": MEMORY_DIR / "growth-log",
        "decisions/log": MEMORY_DIR / "decisions" / "log.md",
        "output-index": MEMORY_DIR / "output-index.md",
        "ratings-tracker": MEMORY_DIR / "ratings-tracker.md",
        "persona-portrait": _find_persona(),
    }
    results = []
    for name, path in dbs.items():
        if name == "growth-log":
            # Directory: check newest file
            latest = None
            if path.is_dir():
                import re
                date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")
                for f in sorted(path.iterdir()):
                    if f.suffix == ".md" and date_pattern.match(f.name):
                        try:
                            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
                            if latest is None or mtime > latest:
                                latest = mtime
                        except (OSError, ValueError):
                            continue
            age = days_since(latest)
        else:
            age = days_since(_mtime_or_none(path))

        if age is None:
            results.append((name, None, "missing"))
        elif age > STALE_DAYS_CRITICAL:
            results.append((name, round(age, 1), "critical"))
        elif age > STALE_DAYS_WARN:
            results.append((name, round(age, 1), "warning"))
        else:
            results.append((name, round(age, 1), "ok"))
    return results


def check_self_model():
    """Compare self-model.md mtime against all growth-log entries.

    Returns (stale: bool, reason: str, newer_logs: list).
    Uses >= comparison for FAT32 2s resolution safety.
    """
    model = MEMORY_DIR / "self-model.md"
    growth_dir = MEMORY_DIR / "growth-log"

    if not model.exists():
        return True, "self-model.md missing", []

    model_mtime = _mtime_or_none(model)
    if model_mtime is None:
        return True, "cannot read self-model.md mtime", []

    # Check for future mtimes (clock skew)
    now = datetime.now(timezone.utc)
    if model_mtime > now:
        future_sec = (model_mtime - now).total_seconds()
        print(f"⚠ self-model.md mtime is {future_sec:.0f}s in the future (clock skew?)",
              file=sys.stderr)

    # Find growth-log entries newer than or equal to self-model
    newer_logs = []
    if growth_dir.is_dir():
        import re
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")
        for f in sorted(growth_dir.iterdir()):
            if f.suffix == ".md" and date_pattern.match(f.name):
                try:
                    f_mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
                    if f_mtime >= model_mtime:
                        newer_logs.append(f.stem)
                except (OSError, ValueError):
                    continue

    if newer_logs:
        return True, f"growth-log entries newer than self-model: {', '.join(newer_logs)}", newer_logs
    return False, "self-model is current", []


# ── Flag Operations ────────────────────────────────────────────────────────

def write_stale_flag(reason, sources):
    """Write .self-model-stale flag with timestamp and reason."""
    STALE_FLAG.parent.mkdir(parents=True, exist_ok=True)
    content = (
        f"# Self-Model Stale Flag\n"
        f"# Generated: {datetime.now(timezone.utc).isoformat()}\n"
        f"# Reason: {reason}\n"
        f"# Sources: {', '.join(sources) if sources else 'none'}\n"
        f"# Action: AI should regenerate self-model.md at next SessionStart\n"
    )
    try:
        STALE_FLAG.write_text(content, encoding="utf-8")
        print(f"🔴 Wrote .self-model-stale flag: {reason}", file=sys.stderr)
        return True
    except OSError as e:
        print(f"❌ Failed to write stale flag: {e}", file=sys.stderr)
        return False


def cleanup_orphaned_flag():
    """Remove stale flag if self-model is actually fresh."""
    if STALE_FLAG.exists():
        try:
            STALE_FLAG.unlink()
            print("🧹 Cleaned orphaned .self-model-stale flag (model was fresh)", file=sys.stderr)
        except OSError:
            pass


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Quality gate — check database freshness and self-model staleness"
    )
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON to stdout")
    args = parser.parse_args()

    # Check databases
    db_results = check_databases()
    stale, reason, sources = check_self_model()

    # Determine exit code
    has_critical = any(r[2] == "critical" for r in db_results)
    has_warning = any(r[2] in ("warning", "missing") for r in db_results)

    exit_code = 0
    if stale:
        exit_code = 2
    elif has_critical or has_warning:
        exit_code = 1

    # Collect structured result
    result = {
        "exit_code": exit_code,
        "exit_label": {0: "clean", 1: "warnings", 2: "hard_block"}[exit_code],
        "self_model": {
            "stale": stale,
            "reason": reason,
            "sources": sources,
        },
        "databases": [
            {"name": name, "days": age, "status": level}
            for name, age, level in db_results
        ],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Human-readable output to stderr
        print("=== quality-gate ===", file=sys.stderr)
        for name, age, level in db_results:
            icon = {"ok": "✅", "warning": "⚠️", "critical": "🔴", "missing": "❌"}[level]
            if age is not None:
                print(f"  {icon} {name}: {age}d ({level})", file=sys.stderr)
            else:
                print(f"  {icon} {name}: missing", file=sys.stderr)

        if stale:
            print(f"  🔴 Self-model: STALE — {reason}", file=sys.stderr)
        else:
            print(f"  ✅ Self-model: current", file=sys.stderr)

        labels = {0: "clean", 1: "warnings", 2: "hard block"}
        print(f"Exit {exit_code} ({labels[exit_code]})", file=sys.stderr)

    # Act on results
    if stale:
        write_stale_flag(reason, sources)
    else:
        cleanup_orphaned_flag()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

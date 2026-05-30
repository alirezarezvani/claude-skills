#!/usr/bin/env python3
"""SessionEnd hook for the handoff skill.

When a session ends, checks whether a recent handoff exists in the
configured save location. If none does (or the most recent is older than
the staleness threshold), prints a one-line reminder so the user
remembers to write one before context is lost.

Cannot block session end and cannot prompt interactively — the reminder
is printed to stdout, which Claude Code surfaces in the session log.

Disable per-session with HANDOFF_SESSIONEND=0.

Stdlib-only.
"""

import datetime as dt
import os
import sys
import tempfile
from pathlib import Path

SKILL_SCRIPTS = (
    Path(__file__).resolve().parent.parent / "skills" / "handoff" / "scripts"
)
sys.path.insert(0, str(SKILL_SCRIPTS))

try:
    import config_loader  # type: ignore
except ImportError:
    sys.exit(0)


HANDOFF_TOKENS = ("handoff-", "handoff_", "handoff.md")
STALE_AFTER_MINUTES = 30  # If no handoff in this window, remind.


def _disabled() -> bool:
    return os.environ.get("HANDOFF_SESSIONEND", "1") == "0"


def _candidate_dirs(config: dict) -> list[Path]:
    save = config.get("save_location", {})
    mode = save.get("mode", "temp")
    raw_path = save.get("path")
    dirs: list[Path] = []
    if mode == "temp":
        dirs.append(Path(tempfile.gettempdir()))
    elif raw_path:
        dirs.append(Path(raw_path))
    proj = Path.cwd() / ".handoff"
    if proj.exists() and proj not in dirs:
        dirs.append(proj)
    return [d for d in dirs if d.exists()]


def _looks_like_handoff(p: Path) -> bool:
    name = p.name.lower()
    return name.endswith(".md") and any(t in name for t in HANDOFF_TOKENS)


def _latest_mtime(config: dict) -> dt.datetime | None:
    latest: float | None = None
    for d in _candidate_dirs(config):
        try:
            for entry in d.iterdir():
                if not entry.is_file() or not _looks_like_handoff(entry):
                    continue
                try:
                    mtime = entry.stat().st_mtime
                except OSError:
                    continue
                if latest is None or mtime > latest:
                    latest = mtime
        except OSError:
            continue
    if latest is None:
        return None
    return dt.datetime.utcfromtimestamp(latest)


def _remind() -> None:
    print("=" * 60)
    print("Session ending — no recent handoff detected.")
    print()
    print("Want to capture state for next time? In a future session, run:")
    print("  /cs:handoff \"<what the next session should do>\"")
    print()
    print("Disable this reminder: HANDOFF_SESSIONEND=0")
    print("=" * 60)


def main() -> int:
    if _disabled():
        return 0
    try:
        config = config_loader.load_config()
    except Exception:
        return 0
    try:
        latest = _latest_mtime(config)
    except Exception:
        return 0
    now = dt.datetime.utcnow()
    stale_cutoff = now - dt.timedelta(minutes=STALE_AFTER_MINUTES)
    if latest is None or latest < stale_cutoff:
        try:
            _remind()
        except Exception:
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

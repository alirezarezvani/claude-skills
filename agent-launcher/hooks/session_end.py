#!/usr/bin/env python3
"""SessionEnd hook for agent-launcher (OPT-IN).

Disabled unless AGENT_LAUNCHER_SESSION=1 (and additionally AGENT_LAUNCHER_SESSIONEND
!= 0). When enabled and an in-progress goal exists that is not yet at phase=done,
prints a one-line reminder to checkpoint/advance the goal so the next session
resumes cleanly. Any error exits 0 — a hook must never break a session.

Stdlib-only.
"""
import json
import os
import sys
from pathlib import Path


def disabled() -> bool:
    if os.environ.get("AGENT_LAUNCHER_SESSION", "0") != "1":
        return True
    if os.environ.get("AGENT_LAUNCHER_SESSIONEND", "1") == "0":
        return True
    return False


def find_goal() -> Path | None:
    for c in [Path.cwd() / "my-agent" / "goal.json", Path.cwd() / ".my-agent" / "goal.json"]:
        if c.exists():
            return c
    try:
        for d in sorted(Path.cwd().glob("my-agent-*/goal.json")):
            return d
    except OSError:
        pass
    return None


def main() -> int:
    if disabled():
        return 0
    try:
        gp = find_goal()
        if not gp:
            return 0
        state = json.loads(gp.read_text())
        phase = state.get("phase", "interview")
        if phase == "done":
            return 0
        print(f"[agent-launcher] Launch still at phase '{phase}'. "
              f"Checkpoint it: `goal_state.py set --phase {phase} --note '...'` "
              f"(or `advance`). Resume next session with /cs:launch.")
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

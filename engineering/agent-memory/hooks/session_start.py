#!/usr/bin/env python3
"""SessionStart -- inject L3 (persona) + L2 (this project). DESIGN.md 5.1.

Contract, in the order it matters:

  * NEVER BLOCKS. Any failure exits 0 with no output. A memory system that can
    break session start is worse than no memory system.
  * Budgets: 2 KB L3, 4 KB L2. Over budget -> truncate by `last_seen` desc and
    SAY SO in the block. "A memory system that silently drops is worse than
    none" (5.1).
  * Never emit two contradictory lines unmarked (5.1). The 4.2.1 detector
    cannot reach L3, so nothing upstream guarantees L2 and L3 agree; a collision
    is marked here at injection time.
  * Disable with AGENT_MEMORY_SESSIONSTART=0.

No internal self-budget, unlike user_prompt_submit.py -- and 5.1 argues why:
this runs once per session, and its work is bounded by the byte caps above
rather than by a scan that grows with history.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "agent-memory", "scripts"))

L3_BUDGET = 2048
L2_BUDGET = 4096


def _contested_tag(atom, atoms, core):
    if not core.open_contradiction(atom, atoms):
        return ""
    return "  [contested — newer evidence %s]" % atom["last_seen"][:10]


def _fit(lines, budget):
    """Take lines in priority order until the byte budget is spent. Returns
    (kept, dropped) -- the caller must disclose `dropped`."""
    kept, used = [], 0
    for i, ln in enumerate(lines):
        cost = len(ln.encode("utf-8")) + 1
        if used + cost > budget:
            return kept, len(lines) - i
        kept.append(ln)
        used += cost
    return kept, 0


def _cross_tier_conflicts(l2, l3, core):
    """5.1's never-emit-contradictory-lines constraint. 4.2.1's detector is
    project-scoped and so structurally cannot see an L2-vs-L3 pair; this is the
    injection-time backstop.

    This marks BOTH sides rather than shadowing one. That is the least
    committal of the three options 5.1 says all satisfy the constraint -- it
    surfaces the collision without deciding precedence, which is exactly what
    the open decision on L3 contradictions has not yet decided. If that decision
    lands on specificity-wins, this is the one function that changes.
    """
    marks = {}
    for a in l2:
        for b in l3:
            if core.contradicts(a["claim"], b["claim"], a["kind"], b["kind"]):
                marks[a["id"]] = b["claim"]
                marks[b["id"]] = a["claim"]
    return marks


def build(atoms, project, core):
    l3 = [a for a in atoms if a["tier"] == "L3"]
    l2 = [a for a in atoms if a["tier"] == "L2" and a.get("project") == project]
    l3.sort(key=lambda a: a["last_seen"], reverse=True)
    l2.sort(key=lambda a: a["last_seen"], reverse=True)
    if not l3 and not l2:
        return ""

    conflicts = _cross_tier_conflicts(l2, l3, core)

    def render(a):
        line = "- %s%s" % (a["claim"], _contested_tag(a, atoms, core))
        if a["id"] in conflicts:
            line += "\n  [conflicts with another remembered rule: %s — " \
                    "neither governs; ask before relying on either]" % conflicts[a["id"]]
        return line

    out = ["<agent_memory>",
           "Remembered from previous sessions. Recurrence-gated, not verified fact;",
           "correct anything wrong and the correction is itself remembered."]
    if l3:
        kept, dropped = _fit([render(a) for a in l3], L3_BUDGET)
        out.append("")
        out.append("## Stable (L3, all projects)")
        out.extend(kept)
        if dropped:
            out.append("- [%d more L3 item(s) omitted for space, oldest-seen first]" % dropped)
    if l2:
        kept, dropped = _fit([render(a) for a in l2], L2_BUDGET)
        out.append("")
        out.append("## This project (L2: %s)" % project)
        out.extend(kept)
        if dropped:
            out.append("- [%d more L2 item(s) omitted for space, oldest-seen first]" % dropped)
    out.append("</agent_memory>")
    return "\n".join(out)


def main():
    if os.environ.get("AGENT_MEMORY_SESSIONSTART") == "0":
        return 0
    try:
        payload = {}
        if not sys.stdin.isatty():
            raw = sys.stdin.read()
            if raw.strip():
                payload = json.loads(raw)
    except Exception:
        payload = {}
    try:
        import memory_core as core
        cwd = payload.get("cwd") or os.getcwd()
        project = os.path.basename(os.path.abspath(cwd))
        block = build(core.AtomStore(os.path.join(cwd, ".memory")).read(), project, core)
        if block:
            sys.stdout.write(block + "\n")
    except Exception:
        # 5.1 -- never blocks. No memory this session is the failure mode.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""memory_promote.py -- L1 -> L2 -> L3. Deterministic, recurrence-based.

Implements DESIGN.md 4 exactly:

  L1 -> L2   >= 3 distinct sessions, spanning >= 2 distinct calendar days,
             same project, no contradiction open.
             Fast paths: `stated` needs 2 sessions (distinct-days STILL
             applies); `verified` promotes on 1 observation and is the only
             path exempt from distinct-days.
  L2 -> L3   held at L2 in >= 2 distinct projects, age >= 30d, uncontested.
             A merge, not a flag flip -- new project-free id.

HARD GATES, both of which refuse rather than guess:
  * `redacted: true` never promotes on evidence alone (4.1). The flag means
    the pass ALTERED the claim, which is positive evidence the source was
    sensitive; redaction is lexical, so finding one thing is not proof of
    finding everything.
  * an open contradiction blocks, found by REVERSE JOIN (4.2.1) -- the newer
    atom carries no flag.

Nothing is written to CLAUDE.md. Promotions land in .memory/staged/ for an
explicit human `adopt` (5.3).

Exit codes: 0 ok, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memory_core as core  # noqa: E402


def _eligible_l1(atom, atoms):
    """Returns (ok, reason). reason names the blocking gate when not ok."""
    if atom["tier"] != "L1":
        return False, "not-L1"
    if atom.get("redacted"):
        return False, "redacted-needs-human-review"
    if core.open_contradiction(atom, atoms):
        return False, "contradiction-open"
    conf = atom["confidence"]
    need = core.GATE_SESSIONS[conf]
    if len(set(atom["sessions"])) < need:
        return False, "sessions %d/%d" % (len(set(atom["sessions"])), need)
    # distinct-days: `verified` is the only exempt path
    if conf != "verified" and core.distinct_days(atom) < 2:
        return False, "single-calendar-day"
    return True, "ok"


def promote_l1_to_l2(atoms, now=None):
    now = now or core.iso()
    promoted, blocked = [], []
    for a in atoms:
        if a["tier"] != "L1":
            continue
        ok, why = _eligible_l1(a, atoms)
        if not ok:
            if why != "not-L1":
                blocked.append((a, why))
            continue
        p = dict(a)
        p["tier"] = "L2"
        p["promoted_at"] = now
        # 3.1.1 -- strip the path prefix. This is the crossing into committed
        # territory; skipping it writes an OS username into a git-tracked file.
        p["source"] = core.strip_backpointer(a["source"])
        p["first_source"] = core.strip_backpointer(a["first_source"])
        promoted.append(p)
    return promoted, blocked


def promote_l2_to_l3(atoms, now=None):
    """4.1.1 -- a merge. Groups by the project-free hash of the normalized
    claim, which is lexical: two projects wording the same rule differently
    never merge. That failure is one-directional (L3 under-fires, never
    mis-fires) and is a stated limit, not a bug."""
    now = now or core.iso()
    groups = {}
    for a in atoms:
        if a["tier"] != "L2" or a.get("redacted"):
            continue
        if core.open_contradiction(a, atoms):
            continue
        if core.days_between(a.get("promoted_at", a["first_seen"]), now) < core.L2_MIN_AGE_DAYS:
            continue
        groups.setdefault(core.normalize(a["claim"]), []).append(a)

    merged, notes = [], []
    for _key, group in groups.items():
        projects = sorted({g["project"] for g in group})
        if len(projects) < 2:
            continue
        kinds = {g["kind"] for g in group}
        if len(kinds) > 1:
            # kind is not in the hash key, so identical text with different
            # kind can group. If two projects classify the same sentence
            # differently, the "same claim" premise is what is shaky.
            notes.append("kind-disagreement %s: %s" % (projects, sorted(kinds)))
            continue
        by_first = sorted(group, key=lambda g: g["first_seen"])
        by_last = sorted(group, key=lambda g: g["last_seen"])
        sessions = []
        for g in group:
            for s in g["sessions"]:
                if s not in sessions:
                    sessions.append(s)
        merged.append({
            "id": core.atom_id(by_first[0]["claim"]),   # project-free
            "claim": by_first[0]["claim"],
            "scope": "global",
            "kind": by_first[0]["kind"],
            "first_seen": by_first[0]["first_seen"],
            "last_seen": by_last[-1]["last_seen"],
            "observations": sum(g["observations"] for g in group),
            "sessions": sessions,
            "source": by_last[-1]["source"],            # newest
            "first_source": by_first[0]["first_source"],  # oldest
            "confidence": max(
                (g["confidence"] for g in group),
                key=core.CONFIDENCE_ORDER.index),
            "tier": "L3",
            "promoted_at": now,
            "promoted_from_projects": projects,
            "redacted": any(g.get("redacted") for g in group),
        })
    return merged, notes


def apply_caps(atoms):
    """4.3 -- L2 caps at 60/project with overflow demoted to L1 (recoverable);
    L3 caps at 30 and REFUSES further promotion rather than deleting, since
    'never auto-demoted' means the cap blocks inflow, not outflow."""
    warnings = []
    by_project = {}
    for a in atoms:
        if a["tier"] == "L2":
            by_project.setdefault(a["project"], []).append(a)
    for proj, group in by_project.items():
        if len(group) > core.L2_MAX_ATOMS:
            group.sort(key=lambda g: g["last_seen"])
            for a in group[: len(group) - core.L2_MAX_ATOMS]:
                a["tier"] = "L1"
                a.pop("promoted_at", None)
                warnings.append("L2 cap: demoted %s (%s) to L1" % (a["id"], proj))
    l3 = [a for a in atoms if a["tier"] == "L3"]
    if len(l3) > core.L3_MAX_ATOMS:
        warnings.append(
            "L3 over cap (%d/%d) -- further promotions refused; prune at adopt"
            % (len(l3), core.L3_MAX_ATOMS))
    return warnings


def stage(store, l2, l3, notes, warnings):
    """Write proposals to .memory/staged/ -- never into CLAUDE.md (5.3)."""
    store._ensure_dirs()
    os.makedirs(store.staged, mode=0o700, exist_ok=True)
    payload = {
        "generated": core.iso(),
        "l2_promotions": l2,
        "l3_promotions": l3,
        "notes": notes,
        "warnings": warnings,
    }
    path = os.path.join(store.staged, "promotions.json")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


SAMPLE_ATOMS = [
    {"id": "atm_aaaaaaaa", "claim": "PR base branch is dev, never main",
     "scope": "project", "project": "demo", "kind": "constraint",
     "first_seen": "2026-08-01T09:00:00Z", "last_seen": "2026-08-05T09:00:00Z",
     "observations": 4, "sessions": ["01A", "01B", "01C"],
     "source": "~/.claude/projects/-home-u/01C.jsonl#L9",
     "first_source": "~/.claude/projects/-home-u/01A.jsonl#L2",
     "confidence": "observed", "tier": "L1", "redacted": False},
    {"id": "atm_bbbbbbbb", "claim": "deploy key is [REDACTED:anthropic-key]",
     "scope": "project", "project": "demo", "kind": "constraint",
     "first_seen": "2026-08-01T09:00:00Z", "last_seen": "2026-08-05T09:00:00Z",
     "observations": 9, "sessions": ["01A", "01B", "01C", "01D"],
     "source": "~/.claude/projects/-home-u/01C.jsonl#L4",
     "first_source": "~/.claude/projects/-home-u/01A.jsonl#L4",
     "confidence": "stated", "tier": "L1", "redacted": True},
    {"id": "atm_cccccccc", "claim": "tests run in one long day",
     "scope": "project", "project": "demo", "kind": "preference",
     "first_seen": "2026-08-07T08:00:00Z", "last_seen": "2026-08-07T23:00:00Z",
     "observations": 3, "sessions": ["01E", "01F", "01G"],
     "source": "~/.claude/projects/-home-u/01G.jsonl#L1",
     "first_source": "~/.claude/projects/-home-u/01E.jsonl#L1",
     "confidence": "observed", "tier": "L1", "redacted": False},
]


def main():
    ap = argparse.ArgumentParser(
        description="Promote L1->L2->L3 on recurrence. Stages proposals; never writes CLAUDE.md.")
    ap.add_argument("--memory-dir", default=None, help="path to .memory/ (default: ./.memory)")
    ap.add_argument("--sample", action="store_true", help="run against built-in sample atoms")
    ap.add_argument("--stage", action="store_true", help="write proposals to .memory/staged/")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args()

    store = core.AtomStore(a.memory_dir)
    atoms = list(SAMPLE_ATOMS) if a.sample else store.read()

    l2, blocked = promote_l1_to_l2(atoms)
    l3, notes = promote_l2_to_l3(atoms + l2)
    warnings = apply_caps(atoms + l2 + l3)

    if a.stage and not a.sample:
        notes.append("staged to " + stage(store, l2, l3, notes, warnings))

    if a.output == "json":
        print(json.dumps({"l2_promotions": l2, "l3_promotions": l3,
                          "blocked": [{"id": b["id"], "reason": r} for b, r in blocked],
                          "notes": notes, "warnings": warnings}, indent=2))
        return 0

    print("Promotion pass over %d atom(s)\n" % len(atoms))
    print("  L1 -> L2 promoted : %d" % len(l2))
    for p in l2:
        print("      %s  %s" % (p["id"], p["claim"][:60]))
    print("  L2 -> L3 merged   : %d" % len(l3))
    for p in l3:
        print("      %s  %s  (from %s)" % (p["id"], p["claim"][:44],
                                           ", ".join(p["promoted_from_projects"])))
    print("  blocked           : %d" % len(blocked))
    for b, why in blocked:
        print("      %s  %-28s %s" % (b["id"], why, b["claim"][:40]))
    for n in notes:
        print("  note: " + n)
    for w in warnings:
        print("  warn: " + w)
    print("\nNothing was written to CLAUDE.md. Promotions stage for `adopt` (5.3).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

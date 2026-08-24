#!/usr/bin/env python3
"""memory_inspect.py -- read the store. Never writes.

DESIGN.md 6 rule 6 ("cite, don't invent") only means anything if a human can
walk any injected line back to the transcript that produced it. This is that
walk. Three questions:

  --tier L1|L2|L3   what is in each tier, and what is blocking the next hop
  --contested       every atom with an open contradiction, both directions
  --why "<claim>"   the provenance of one claim: how many sessions, over how
                    many calendar days, from which transcript, and -- if the
                    file is still on disk -- the actual line it came from

`--why` resolving to `ambiguous` is a feature, not a failure: two projects can
hold a transcript of the same basename, and guessing between them would attach
a real claim to the wrong session (6 rule 6 treats a WRONG citation as worse
than a missing one).

Exit codes: 0 ok, 2 bad input, 3 claim not found.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memory_core as core  # noqa: E402


def _blocking_reason(atom, atoms):
    """Why this L1 atom is not L2 yet. Mirrors memory_promote._eligible_l1 --
    kept as a separate read-only formulation so inspect never imports the
    promoter and can never, by construction, promote anything."""
    if atom["tier"] != "L1":
        return None
    if atom.get("redacted"):
        return "redacted -- needs human review (4.1)"
    if core.open_contradiction(atom, atoms):
        return "contradiction open (4.2.1)"
    need = core.GATE_SESSIONS[atom["confidence"]]
    have = len(set(atom["sessions"]))
    if have < need:
        return "sessions %d/%d" % (have, need)
    if atom["confidence"] != "verified" and core.distinct_days(atom) < 2:
        return "seen on one calendar day only"
    return "eligible -- promotes on next pass"


def tier_view(atoms, tier):
    rows = [a for a in atoms if a["tier"] == tier]
    rows.sort(key=lambda a: (a["last_seen"], a["id"]), reverse=True)
    out = []
    for a in rows:
        out.append({
            "id": a["id"],
            "claim": a["claim"],
            "kind": a["kind"],
            "confidence": a["confidence"],
            "project": a.get("project"),
            "sessions": len(set(a["sessions"])),
            "observations": a["observations"],
            "days": core.distinct_days(a),
            "redacted": bool(a.get("redacted")),
            "status": _blocking_reason(a, atoms),
        })
    return out


def contested_view(atoms):
    """Both directions of the reverse join (4.2.1): atoms carrying `contested`,
    and atoms named in someone else's `contested_by` while carrying no flag of
    their own -- which is the entire reason the join exists."""
    by_id = {a["id"]: a for a in atoms}
    out = []
    for a in atoms:
        if a.get("contested"):
            out.append({"id": a["id"], "claim": a["claim"], "direction": "self-flagged",
                        "contested_by": a.get("contested_by", []),
                        "counterparts": [by_id[c]["claim"] for c in a.get("contested_by", [])
                                         if c in by_id]})
    for a in atoms:
        for other in atoms:
            if a["id"] in other.get("contested_by", []) and not a.get("contested"):
                out.append({"id": a["id"], "claim": a["claim"],
                            "direction": "named-by-other", "named_by": other["id"],
                            "counterparts": [other["claim"]]})
    return out


def why(atoms, claim):
    """Provenance for one claim, matched on the normalized form (4.1) so
    punctuation and casing do not have to be reproduced by hand."""
    target = core.normalize(claim)
    hits = [a for a in atoms
            if core.normalize(a["claim"]) == target or target in core.normalize(a["claim"])]
    if not hits:
        return None
    a = sorted(hits, key=lambda h: len(h["claim"]))[0]
    first_path, first_status = core.resolve_backpointer(a["first_source"])
    last_path, last_status = core.resolve_backpointer(a["source"])
    rec = {
        "id": a["id"],
        "claim": a["claim"],
        "tier": a["tier"],
        "kind": a["kind"],
        "confidence": a["confidence"],
        "scope": a["scope"],
        "project": a.get("project"),
        "observations": a["observations"],
        "distinct_sessions": len(set(a["sessions"])),
        "sessions": sorted(set(a["sessions"])),
        "first_seen": a["first_seen"],
        "last_seen": a["last_seen"],
        "spans_days": core.days_between(a["first_seen"], a["last_seen"]),
        "distinct_calendar_days": core.distinct_days(a),
        "first_source": a["first_source"],
        "first_source_resolved": first_status,
        "source": a["source"],
        "source_resolved": last_status,
        "redacted": bool(a.get("redacted")),
        "contradiction_open": core.open_contradiction(a, atoms),
        "blocking": _blocking_reason(a, atoms),
        "promoted_at": a.get("promoted_at"),
        "promoted_from_projects": a.get("promoted_from_projects"),
    }
    # Quote the actual source line only when exactly one transcript matched.
    if last_status == "ok" and last_path:
        try:
            n = int(a["source"].rsplit("#L", 1)[1])
            with open(last_path, "r", encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh, 1):
                    if i == n:
                        quoted, _ = core.redact(line.strip()[:400])
                        rec["source_line"] = quoted
                        break
        except (OSError, ValueError, IndexError):
            pass
    return rec


SAMPLE_ATOMS = [
    {"id": "atm_11111111", "claim": "PR base branch is dev, never main",
     "scope": "project", "project": "demo", "kind": "constraint",
     "first_seen": "2026-08-01T09:00:00Z", "last_seen": "2026-08-06T11:00:00Z",
     "observations": 5, "sessions": ["01A", "01B", "01C"],
     "source": "~/.claude/projects/-home-u/01C.jsonl#L9",
     "first_source": "~/.claude/projects/-home-u/01A.jsonl#L2",
     "confidence": "observed", "tier": "L2", "redacted": False,
     "promoted_at": "2026-08-07T09:00:00Z"},
    {"id": "atm_22222222", "claim": "scripts are stdlib only",
     "scope": "project", "project": "demo", "kind": "constraint",
     "first_seen": "2026-08-02T09:00:00Z", "last_seen": "2026-08-02T18:00:00Z",
     "observations": 2, "sessions": ["01D"],
     "source": "~/.claude/projects/-home-u/01D.jsonl#L3",
     "first_source": "~/.claude/projects/-home-u/01D.jsonl#L3",
     "confidence": "observed", "tier": "L1", "redacted": False},
    {"id": "atm_33333333", "claim": "scripts are not stdlib only",
     "scope": "project", "project": "demo", "kind": "constraint",
     "first_seen": "2026-08-09T09:00:00Z", "last_seen": "2026-08-11T09:00:00Z",
     "observations": 3, "sessions": ["01E", "01F", "01G"],
     "source": "~/.claude/projects/-home-u/01G.jsonl#L1",
     "first_source": "~/.claude/projects/-home-u/01E.jsonl#L1",
     "confidence": "observed", "tier": "L1", "redacted": False,
     "contested": True, "contested_by": ["atm_22222222"]},
]


def main():
    ap = argparse.ArgumentParser(
        description="Inspect the tiered memory store. Read-only; never writes or promotes.")
    ap.add_argument("--memory-dir", default=None, help="path to .memory/ (default: ./.memory)")
    ap.add_argument("--tier", choices=["L1", "L2", "L3"], help="list one tier")
    ap.add_argument("--contested", action="store_true",
                    help="atoms with an open contradiction, both join directions")
    ap.add_argument("--why", metavar="CLAIM", help="provenance for one claim")
    ap.add_argument("--sample", action="store_true", help="run against built-in sample atoms")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args()

    atoms = list(SAMPLE_ATOMS) if a.sample else core.AtomStore(a.memory_dir).read()

    if a.why:
        rec = why(atoms, a.why)
        if rec is None:
            print("No atom matches %r." % a.why, file=sys.stderr)
            return 3
        if a.output == "json":
            print(json.dumps(rec, indent=2, ensure_ascii=False))
            return 0
        print("%s  [%s]\n  %s\n" % (rec["id"], rec["tier"], rec["claim"]))
        print("  kind/confidence   : %s / %s" % (rec["kind"], rec["confidence"]))
        print("  seen              : %d observation(s) across %d session(s)"
              % (rec["observations"], rec["distinct_sessions"]))
        print("  window            : %s -> %s (%d day span, %d distinct calendar day(s))"
              % (rec["first_seen"], rec["last_seen"], rec["spans_days"],
                 rec["distinct_calendar_days"]))
        print("  first evidence    : %s  [%s]" % (rec["first_source"], rec["first_source_resolved"]))
        print("  latest evidence   : %s  [%s]" % (rec["source"], rec["source_resolved"]))
        if "source_line" in rec:
            print("      > %s" % rec["source_line"])
        elif rec["source_resolved"] == "ambiguous":
            print("      (transcript basename matches more than one project --")
            print("       refusing to guess; a wrong citation is worse than none)")
        if rec["redacted"]:
            print("  redacted          : yes -- blocked from promotion pending review")
        if rec["contradiction_open"]:
            print("  contradiction     : OPEN")
        if rec["blocking"]:
            print("  next hop          : %s" % rec["blocking"])
        return 0

    if a.contested:
        rows = contested_view(atoms)
        if a.output == "json":
            print(json.dumps({"contested": rows, "count": len(rows)}, indent=2,
                             ensure_ascii=False))
            return 0
        print("Contested atoms: %d\n" % len(rows))
        for r in rows:
            print("  %s  (%s)" % (r["id"], r["direction"]))
            print("      %s" % r["claim"][:78])
            for c in r["counterparts"]:
                print("      vs. %s" % c[:74])
        if not rows:
            print("  (none)")
        return 0

    tiers = [a.tier] if a.tier else ["L1", "L2", "L3"]
    if a.output == "json":
        print(json.dumps({t: tier_view(atoms, t) for t in tiers}, indent=2,
                         ensure_ascii=False))
        return 0
    for t in tiers:
        rows = tier_view(atoms, t)
        print("%s -- %d atom(s)" % (t, len(rows)))
        for r in rows:
            flag = " [REDACTED]" if r["redacted"] else ""
            print("  %s  %-9s %-8s %s%s" % (r["id"], r["kind"], r["confidence"],
                                            r["claim"][:56], flag))
            if r["status"]:
                print("      %s" % r["status"])
        if not rows:
            print("  (empty)")
        print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())

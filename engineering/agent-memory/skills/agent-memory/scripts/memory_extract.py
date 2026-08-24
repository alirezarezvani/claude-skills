#!/usr/bin/env python3
"""memory_extract.py -- L0 -> L1. Rule-based, no LLM.

DESIGN.md 9.2 is the open decision this script IS the answer to: option (a),
"rule-based on explicit markers only -- high precision, low recall". It does
not try to understand a transcript. It looks for the handful of shapes in
which a durable operational fact is stated OUT LOUD, and ignores everything
else. Recall is deliberately low; 9.3's two-week trial is the test of whether
it is high enough to be worth keeping.

Every emitted atom is redacted before it is returned (6 rule 1) and carries a
live back-pointer (4.1's L0 -> L1 gate).

Exit codes: 0 ok, 2 bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import memory_core as core  # noqa: E402

# --------------------------------------------------------------------------
# The markers. Each is a shape in which a fact is stated explicitly enough that
# a regex is honest. Anything requiring inference is out of scope by design.
# --------------------------------------------------------------------------

MARKERS = [
    # ("name", pattern, kind, confidence)
    ("directive", re.compile(
        r"(?i)\b(?:always|never|must|don'?t ever)\b\s+(?P<c>[^.!?\n]{8,160})"),
     "constraint", "stated"),
    ("correction", re.compile(
        r"(?i)\b(?:no,|actually,|not quite[—-]?|correction:)\s*(?P<c>[^.!?\n]{8,160})"),
     "correction", "stated"),
    ("preference", re.compile(
        r"(?i)\b(?:we (?:use|prefer)|I (?:use|prefer)|convention is)\s+(?P<c>[^.!?\n]{8,160})"),
     "preference", "stated"),
    ("lesson", re.compile(
        r"(?i)^\s*[-*]?\s*(?:lesson|rule|gotcha):\s*(?P<c>[^\n]{8,160})"),
     "constraint", "stated"),
    ("failure", re.compile(
        r"(?i)\b(?P<c>[a-z][^.!?\n]{6,140}?\s+(?:fails?|breaks?|errors? out)\s+"
        r"(?:when|if|because)\s+[^.!?\n]{4,80})"),
     "failure", "observed"),
]

# Lines that look like markers but are the agent talking, not the user or a
# verified result. High-precision means refusing these.
_NOISE = re.compile(
    r"(?i)^\s*(?:i'?ll|i will|let me|should i|shall i|would you like|"
    r"here'?s|for example|e\.g\.|note that)")


def _iter_messages(path):
    """Claude Code transcripts are jsonl, one event per line. We read only
    user-authored text and tool results -- never the assistant's own prose,
    which would let the system learn from its own guesses."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    ev = json.loads(line)
                except json.JSONDecodeError:
                    continue
                role = (ev.get("role") or ev.get("type") or "").lower()
                if role not in ("user", "human", "tool_result", "toolresult"):
                    continue
                content = ev.get("content") or ev.get("text") or ""
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict))
                if isinstance(content, str) and content.strip():
                    yield n, content
    except FileNotFoundError:
        return


def extract(transcript, project, session_id, now=None):
    """Returns a list of well-formed, redacted L1 atoms."""
    now = now or core.iso()
    seen = {}
    for lineno, text in _iter_messages(transcript):
        for raw_line in text.splitlines():
            if _NOISE.match(raw_line):
                continue
            for _name, pat, kind, conf in MARKERS:
                m = pat.search(raw_line)
                if not m:
                    continue
                claim = " ".join(m.group("c").split()).strip(" -–—:;,")
                if len(claim) < 8:
                    continue
                clean, hits = core.redact(claim)
                aid = core.atom_id(clean, project)
                if aid in seen:
                    continue
                bp = core.canonical_backpointer(transcript, lineno)
                seen[aid] = {
                    "id": aid,
                    "claim": clean,
                    "scope": "project",
                    "project": project,
                    "kind": kind,
                    "first_seen": now,
                    "last_seen": now,
                    "observations": 1,
                    "sessions": [session_id],
                    "source": bp,
                    "first_source": bp,
                    "confidence": conf,
                    "tier": "L1",
                    "redacted": bool(hits),
                }
                break  # one atom per line -- first marker wins
    return list(seen.values())


def merge_into_store(store, new_atoms):
    """5.3 -- increment observations, extend sessions, raise confidence to the
    max (4.1.3, never lower). Returns (atoms, n_new, n_merged)."""
    existing = {a["id"]: a for a in store.read()}
    n_new = n_merged = 0
    for a in new_atoms:
        cur = existing.get(a["id"])
        if cur is None:
            existing[a["id"]] = a
            n_new += 1
            continue
        cur["observations"] += 1
        for s in a["sessions"]:
            if s not in cur["sessions"]:
                cur["sessions"].append(s)
        cur["last_seen"] = max(cur["last_seen"], a["last_seen"])
        cur["first_seen"] = min(cur["first_seen"], a["first_seen"])
        cur["source"] = a["source"]                      # newest evidence
        cur["confidence"] = core.max_confidence(cur["confidence"], a["confidence"])
        cur["redacted"] = cur.get("redacted") or a["redacted"]
        n_merged += 1
    atoms = list(existing.values())
    # 4.3 / 5.2 -- L1 is capped; evict by last_seen ascending.
    l1 = [a for a in atoms if a["tier"] == "L1"]
    if len(l1) > core.L1_MAX_ATOMS:
        l1.sort(key=lambda a: a["last_seen"])
        drop = {a["id"] for a in l1[: len(l1) - core.L1_MAX_ATOMS]}
        atoms = [a for a in atoms if a["id"] not in drop]
    return atoms, n_new, n_merged


SAMPLE = '''{"role":"user","content":"always target dev for PRs, never main"}
{"role":"user","content":"Actually, the base branch is dev"}
{"role":"user","content":"I'll go check that for you"}
{"role":"user","content":"mkdocs build fails when nav lists a page with no matching file"}
{"role":"user","content":"the staging key sk-ant-aaaaaaaaaaaaaaaaaaaaaa works"}
'''


def main():
    ap = argparse.ArgumentParser(
        description="Extract L1 atoms from a Claude Code transcript (rule-based, no LLM).")
    ap.add_argument("transcript", nargs="?", help="path to a session .jsonl")
    ap.add_argument("--project", default=os.path.basename(os.getcwd()))
    ap.add_argument("--session", default="unknown-session")
    ap.add_argument("--sample", action="store_true",
                    help="run against a built-in sample transcript")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args()

    if a.sample:
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".jsonl")
        with os.fdopen(fd, "w") as fh:
            fh.write(SAMPLE)
        atoms = extract(path, a.project, "01SESSIONSAMPLE0000000")
        os.unlink(path)
    elif a.transcript:
        atoms = extract(a.transcript, a.project, a.session)
    else:
        ap.error("give a transcript path or --sample")

    if a.output == "json":
        print(json.dumps({"atoms": atoms, "count": len(atoms)}, indent=2))
    else:
        print("Extracted %d atom(s) from %s\n" % (
            len(atoms), a.transcript or "<sample>"))
        for at in atoms:
            flag = "  [REDACTED]" if at["redacted"] else ""
            print("  %s  %-11s %-8s %s%s" % (
                at["id"], at["kind"], at["confidence"], at["claim"][:64], flag))
        if not atoms:
            print("  (none -- rule-based extraction is high-precision by design;")
            print("   see DESIGN.md 9.2 for the recall trade this makes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

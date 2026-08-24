#!/usr/bin/env python3
"""SessionEnd -- capture L0 -> L1, detect contradictions, stage promotions.

DESIGN.md 5.3. Runs `async: true` so it can never delay session teardown.

The pipeline, in order, because the order is the safety property:

  1. extract      rule-based, high-precision markers only (9.2 option (a))
  2. REDACT       every atom, before anything is written (6 rule 1)
  3. merge        increment observations, extend sessions, raise confidence to
                  the max -- never lower (4.1.3)
  4. detect       4.2.1's two rules; mark the OLDER atom contested
  5. write        atomic os.replace under a 5s-bounded lock (5.4); on
                  contention the atoms are DROPPED and the loss is logged to
                  .memory/errors.log -- not stderr, which for an async hook
                  goes nowhere a human reads
  6. promote      L1->L2->L3 on recurrence, staged to .memory/staged/

Step 6 NEVER writes CLAUDE.md. Adoption is a separate, explicit, human step
(`/cs:memory adopt`), which backs both CLAUDE.md files up first.

A missing .memory/atoms.jsonl is the normal first-run state, not an error.
Disable with AGENT_MEMORY_SESSIONEND=0.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "agent-memory", "scripts"))


def main():
    if os.environ.get("AGENT_MEMORY_SESSIONEND") == "0":
        return 0
    try:
        raw = "" if sys.stdin.isatty() else sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    transcript = payload.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        return 0

    try:
        import memory_core as core
        import memory_extract as extract
        import memory_promote as promote

        cwd = payload.get("cwd") or os.getcwd()
        project = os.path.basename(os.path.abspath(cwd))
        # A CONSTANT fallback here would be a silent, permanent bug. Sessions
        # are deduped by value (5.3), so if `session_id` were ever absent,
        # every session would collapse onto one id, `len(set(sessions))` would
        # plateau at 1, and EVERY claim would be capped at L1 forever with no
        # error anywhere -- the gates need 2-3 distinct sessions. So fall back
        # to the transcript's own basename, which IS the session: Claude Code
        # names each transcript for its session id.
        session = payload.get("session_id") or os.path.splitext(
            os.path.basename(transcript))[0] or "unknown-session"
        store = core.AtomStore(os.path.join(cwd, ".memory"))

        new_atoms = extract.extract(transcript, project, session)
        if not new_atoms:
            return 0

        atoms, _n_new, _n_merged = extract.merge_into_store(store, new_atoms)
        core.mark_contradictions(atoms)

        if not store.write(atoms):
            # 5.4 -- the one place data disappears. It is logged inside write().
            return 0

        l2, _blocked = promote.promote_l1_to_l2(atoms)
        l3, notes = promote.promote_l2_to_l3(atoms + l2)
        warnings = promote.apply_caps(atoms + l2 + l3)
        if l2 or l3:
            promote.stage(store, l2, l3, notes, warnings)
    except Exception:
        # Never blocks teardown. A lost capture costs one re-observation; L1 is
        # the recoverable tier by construction (5.4).
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

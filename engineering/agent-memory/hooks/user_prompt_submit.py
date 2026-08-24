#!/usr/bin/env python3
"""UserPromptSubmit -- recall relevant L1 atoms. DESIGN.md 5.2.

PROVISIONAL. hooks.json says so and so does this file: 9.5 is an open decision
whose option (c) is to delete this hook, because the measured cost is dominated
by interpreter cold start (p50 ~12 ms, p95 ~31 ms just to reach `main`) rather
than by anything below. The scoring pass itself measured 2-3 ms over 500 atoms.
Shipping it does not close that decision.

Two limits, not one (5.2 is emphatic that conflating them misses the point):

  internal self-budget   100 ms, enforced HERE against a monotonic clock.
                         Past budget: stop scoring, return what we have.
  hook timeout backstop  1 second, enforced by Claude Code. Kills a wedged
                         process. Finishing under 1 s does NOT satisfy the spec.

  * top 5 atoms, 1 KB max
  * a `contested` atom renders with the 4.2 tag, never as a bare claim
  * reads take NO lock (5.4) -- atomic os.replace on the writer side is what
    makes a lock-free read safe, and blocking here on an async SessionEnd's
    lock would blow the budget for a hook whose failure mode is "return nothing"
  * disable with AGENT_MEMORY_USERPROMPTSUBMIT=0
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

BUDGET_S = 0.100
MAX_ATOMS = 5
MAX_BYTES = 1024

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "agent-memory", "scripts"))

# Weighting: a constraint the user stated out loud is worth more at recall time
# than a passively observed preference.
KIND_WEIGHT = {"constraint": 1.4, "correction": 1.3, "failure": 1.2,
               "preference": 1.0, "fact": 1.0}
CONF_WEIGHT = {"verified": 1.3, "stated": 1.1, "observed": 1.0}

_STOP = {
    "the", "a", "an", "and", "or", "but", "if", "is", "are", "was", "were", "be",
    "to", "of", "in", "on", "for", "with", "that", "this", "it", "as", "at", "by",
    "do", "does", "did", "can", "you", "i", "we", "me", "my", "our", "please",
    "what", "how", "why", "when", "where", "not", "no", "so", "up", "out", "then",
}
_WORD = re.compile(r"[a-z0-9_.\-/]+")


def _tokens(text):
    return {t for t in _WORD.findall(text.casefold()) if t not in _STOP and len(t) > 2}


def score(atom, prompt_tokens, now_day, core):
    """Token overlap x kind x confidence x recency. Deterministic, lexical, no
    embeddings and no API call (5.2, and the repo-wide no-LLM-in-scripts rule)."""
    at = _tokens(atom["claim"])
    if not at:
        return 0.0
    overlap = len(at & prompt_tokens)
    if not overlap:
        return 0.0
    base = overlap / (len(at) ** 0.5)
    try:
        age = max(0, now_day - int(core.parse_iso(atom["last_seen"]).timestamp() // 86400))
    except Exception:
        age = 0
    recency = 1.0 / (1.0 + age / 30.0)
    return (base
            * KIND_WEIGHT.get(atom["kind"], 1.0)
            * CONF_WEIGHT.get(atom["confidence"], 1.0)
            * (0.7 + 0.3 * recency))


def recall(atoms, prompt, core, deadline=None):
    """Single linear pass, bounded top-5 -- no index build, no full sort (5.2).
    Returns (rows, budget_expired)."""
    ptok = _tokens(prompt)
    if not ptok:
        return [], False
    now_day = int(time.time() // 86400)
    top = []  # kept tiny; insertion sort into <=5 slots beats sorting 500
    expired = False
    for a in atoms:
        if a["tier"] != "L1":
            continue
        if deadline is not None and time.monotonic() > deadline:
            expired = True
            break
        s = score(a, ptok, now_day, core)
        if s <= 0:
            continue
        if len(top) < MAX_ATOMS or s > top[-1][0]:
            top.append((s, a))
            top.sort(key=lambda r: r[0], reverse=True)
            del top[MAX_ATOMS:]
    return top, expired


def render(top, atoms, core):
    lines, used = [], 0
    for s, a in top:
        tag = ""
        if core.open_contradiction(a, atoms):
            # 5.2 -- a contested atom must NOT surface as a bare claim.
            tag = "  [contested — newer evidence %s]" % a["last_seen"][:10]
        ln = "- %s%s" % (a["claim"], tag)
        cost = len(ln.encode("utf-8")) + 1
        if used + cost > MAX_BYTES:
            break
        lines.append(ln)
        used += cost
    if not lines:
        return ""
    return "\n".join(["<agent_memory_recall>",
                      "Possibly relevant, remembered from earlier sessions:"]
                     + lines + ["</agent_memory_recall>"])


def main():
    if os.environ.get("AGENT_MEMORY_USERPROMPTSUBMIT") == "0":
        return 0
    deadline = time.monotonic() + BUDGET_S
    try:
        raw = "" if sys.stdin.isatty() else sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0
    prompt = payload.get("prompt") or ""
    if not prompt:
        return 0
    try:
        import memory_core as core
        cwd = payload.get("cwd") or os.getcwd()
        atoms = core.AtomStore(os.path.join(cwd, ".memory")).read()
        top, _expired = recall(atoms, prompt, core, deadline)
        block = render(top, atoms, core)
        if block:
            sys.stdout.write(block + "\n")
    except Exception:
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())

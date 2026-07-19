"""SkillOpt-Sleep — slow update (cross-night long-term memory).

This is the deployment-time analogue of SkillOpt's epoch-wise slow/meta update
(paper §3.6). Step-level edits (consolidate) learn from one night's batch; the
slow update learns across nights and writes a durable "longitudinal guidance"
block into a PROTECTED field of the skill that step-level edits never touch.

It reuses the exact protected-field marker convention from the main repo
(``skillopt/optimizer/slow_update.py``) so the artifact is compatible:

    <!-- SLOW_UPDATE_START --> ... <!-- SLOW_UPDATE_END -->

Why it matters: even when the user turns the validation gate OFF (greedy mode),
the slow update still runs at the end of the run, so short-term nightly
experience is consolidated into long-term memory rather than lost. The cross-night
content is carried in ``state.slow_memory``.

Driven through the Backend abstraction (mock/claude/codex), so it stays
import-light — no `openai` dependency.
"""
from __future__ import annotations

import re
from typing import List, Optional, Tuple

from skillopt_sleep.backend import Backend, _extract_json
from skillopt_sleep.types import ReplayResult, TaskRecord


SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"


# ── protected-field helpers (mirror skillopt/optimizer/slow_update.py) ─────────

def has_slow_field(skill: str) -> bool:
    return SLOW_UPDATE_START in skill and SLOW_UPDATE_END in skill


def extract_slow_field(skill: str) -> str:
    s = skill.find(SLOW_UPDATE_START)
    e = skill.find(SLOW_UPDATE_END)
    if s == -1 or e == -1:
        return ""
    return skill[s + len(SLOW_UPDATE_START):e].strip()


def _strip_slow_fields(skill: str) -> str:
    while True:
        s = skill.find(SLOW_UPDATE_START)
        if s == -1:
            break
        e = skill.find(SLOW_UPDATE_END, s)
        if e == -1:
            skill = skill[:s]
            break
        skill = skill[:s] + skill[e + len(SLOW_UPDATE_END):]
    skill = skill.replace(SLOW_UPDATE_END, "")
    while "\n\n\n" in skill:
        skill = skill.replace("\n\n\n", "\n\n")
    return skill.rstrip()


def replace_slow_field(skill: str, content: str) -> str:
    """Set the protected slow-update field to ``content`` (exactly one block)."""
    base = _strip_slow_fields(skill)
    if not content.strip():
        return base
    block = f"\n\n{SLOW_UPDATE_START}\n{content.strip()}\n{SLOW_UPDATE_END}\n"
    return base + block


# ── the slow-update synthesis ──────────────────────────────────────────────────

def _summarize_pairs(
    prev_pairs: List[Tuple[TaskRecord, ReplayResult]],
    curr_pairs: List[Tuple[TaskRecord, ReplayResult]],
) -> str:
    """Group adjacent-version outcomes into improved/regressed/persistent/stable."""
    prev_by = {t.id: r for t, r in prev_pairs}
    lines: List[str] = []
    counts = {"improved": 0, "regressed": 0, "persistent_fail": 0, "stable_success": 0}
    for t, r in curr_pairs:
        p = prev_by.get(t.id)
        if p is None:
            continue
        a, b = p.hard, r.hard
        if b > a:
            cat = "improved"
        elif b < a:
            cat = "regressed"
        elif b >= 1.0:
            cat = "stable_success"
        else:
            cat = "persistent_fail"
        counts[cat] += 1
        if cat in ("regressed", "persistent_fail") and len(lines) < 8:
            lines.append(f"- [{cat}] {t.intent[:120]} (why: {r.fail_reason[:80]})")
    head = ", ".join(f"{k}={v}" for k, v in counts.items())
    return head + ("\n" + "\n".join(lines) if lines else ""), counts  # type: ignore[return-value]


def run_slow_update(
    backend: Backend,
    *,
    prev_skill: str,
    curr_skill: str,
    prev_pairs: List[Tuple[TaskRecord, ReplayResult]],
    curr_pairs: List[Tuple[TaskRecord, ReplayResult]],
    prev_slow_content: str = "",
) -> Optional[str]:
    """Produce durable longitudinal guidance text (or None).

    Compares behavior under the previous vs current skill across the same tasks
    and asks the optimizer to distill a short, durable guidance block — what to
    keep doing, what regressions to avoid — refining any prior slow-update text.
    """
    summary, counts = _summarize_pairs(prev_pairs, curr_pairs)  # type: ignore[misc]
    # nothing changed and no prior guidance to refine → skip
    if counts["regressed"] == 0 and counts["persistent_fail"] == 0 and not prev_slow_content:
        return None

    prompt = (
        "You are SkillOpt's SLOW UPDATE — the long-term memory pass that runs "
        "across nights. Write a SHORT, durable guidance block (2-5 bullet "
        "points) capturing the longitudinal lessons: behaviors that reliably "
        "help and should be preserved, and regressions/persistent failures to "
        "avoid. Keep it GENERAL and stable (not tied to one task). If prior "
        "guidance is given, refine it rather than restate it.\n"
        'Return ONLY JSON: {"guidance": "<bullet list as one string>"}.\n\n'
        f"# Cross-night outcome summary\n{summary}\n\n"
        f"# Prior long-term guidance (refine this)\n{prev_slow_content or '(none)'}"
    )
    raw = backend._call(prompt, max_tokens=600)  # type: ignore[attr-defined]
    obj = _extract_json(raw, "object")
    if isinstance(obj, dict):
        g = str(obj.get("guidance", "")).strip()
        if g:
            return g
    # fallback: if the model returned prose, keep the first ~400 chars
    text = (raw or "").strip()
    return text[:400] if text else None

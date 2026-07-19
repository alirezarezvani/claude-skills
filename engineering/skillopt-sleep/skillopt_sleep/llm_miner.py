"""SkillOpt-Sleep — LLM-backed task miner.

The heuristic miner (mine.py) produces TaskRecords without a checkable
reference, so real harvested transcripts can't show measurable lift. This
module uses an optimizer backend to turn session digests into TaskRecords
WITH a checkable rubric judge — the missing piece for real-data improvement.

For each recurring intent it extracts:
  * a clean, generalized `intent` (the reusable task, stripped of one-off specifics)
  * a `rubric` (what a good answer must satisfy) -> stored as a rule judge of
    `contains`/`regex`/`section_present` checks the local judge can score, OR a
    free-text rubric scored by the backend's judge() when no programmatic check fits
  * a preference signal (was the user satisfied?) to weight failures

It is deliberately conservative: it only emits a task when it can name a
concrete, checkable success criterion, so the gate has real signal. Tasks it
can't make checkable are dropped (logged), not faked.
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable, Dict, List

from skillopt_sleep.backend import Backend, _extract_json
from skillopt_sleep.types import SessionDigest, TaskRecord


_MINER_PROMPT = """You are mining a user's past AI-assistant sessions to find RECURRING tasks
worth optimizing a skill for. From the session below, extract 0-3 reusable tasks.

A good task is something the user asks for repeatedly or had to correct, where a
GENERAL rule would help next time (formatting, structure, tool-use, conventions).
Skip one-off or purely exploratory requests.

For each task return:
  - "intent": the reusable request, generalized (no one-off specifics)
  - "checks": a list of programmatic success checks a grader can run on a future
     answer. Each check is one of:
        {"op":"section_present","arg":"<heading text>"}
        {"op":"regex","arg":"<python regex the answer must match>"}
        {"op":"contains","arg":"<substring the answer must contain>"}
        {"op":"max_chars","arg":<int>}
     Only include checks you are confident a GOOD answer must satisfy.
  - "rubric": a one-sentence description of what a good answer looks like
  - "satisfied": true/false — did the user seem satisfied with the assistant's answer?

Return ONLY a JSON array (possibly empty). No prose.

# Session
project: __PROJECT__
user prompts:
__PROMPTS__
assistant final (last):
__FINAL__
feedback signals: __FEEDBACK__
"""


def _digest_to_prompt(d: SessionDigest) -> str:
    prompts = "\n".join(f"  - {p[:240]}" for p in d.user_prompts[:6]) or "  (none)"
    final = (d.assistant_finals[-1][:400] if d.assistant_finals else "(none)")
    return (
        _MINER_PROMPT
        .replace("__PROJECT__", d.project or "(unknown)")
        .replace("__PROMPTS__", prompts)
        .replace("__FINAL__", final)
        .replace("__FEEDBACK__", ", ".join(d.feedback_signals[:6]) or "(none)")
    )


def _mk_task(d: SessionDigest, obj: Dict[str, Any], idx: int) -> TaskRecord | None:
    intent = str(obj.get("intent", "")).strip()
    if len(intent) < 8:
        return None
    checks = obj.get("checks") or []
    rubric = str(obj.get("rubric", "")).strip()
    satisfied = bool(obj.get("satisfied", False))

    # keep only well-formed checks
    clean_checks = []
    for c in checks:
        if isinstance(c, dict) and c.get("op") in {
            "section_present", "regex", "contains", "max_chars", "min_chars",
        }:
            clean_checks.append({"op": c["op"], "arg": c.get("arg")})

    import hashlib
    tid = "llm_" + hashlib.sha256((d.project + intent).encode()).hexdigest()[:12]

    if clean_checks:
        return TaskRecord(
            id=tid, project=d.project, intent=intent,
            reference_kind="rule", judge={"kind": "rule", "checks": clean_checks},
            outcome="success" if satisfied else "fail",
            tags=["mined:llm"], source_sessions=[d.session_id],
        )
    if rubric:
        return TaskRecord(
            id=tid, project=d.project, intent=intent,
            reference_kind="rubric", reference=rubric,
            outcome="success" if satisfied else "fail",
            tags=["mined:llm"], source_sessions=[d.session_id],
        )
    return None  # not checkable -> drop


def make_llm_miner(
    backend: Backend,
    *,
    max_sessions: int = 20,
    max_tasks: int = 40,
) -> Callable[[List[SessionDigest]], List[TaskRecord]]:
    """Return an llm_miner(digests) -> list[TaskRecord] bound to a backend."""

    def _miner(digests: List[SessionDigest]) -> List[TaskRecord]:
        out: List[TaskRecord] = []
        for d in digests[:max_sessions]:
            if not d.user_prompts:
                continue
            raw = backend._call(_digest_to_prompt(d), max_tokens=800)  # type: ignore[attr-defined]
            arr = _extract_json(raw, "array")
            if not isinstance(arr, list):
                continue
            for i, obj in enumerate(arr[:3]):
                if isinstance(obj, dict):
                    t = _mk_task(d, obj, i)
                    if t is not None:
                        out.append(t)
                if len(out) >= max_tasks:
                    return out
        return out

    return _miner

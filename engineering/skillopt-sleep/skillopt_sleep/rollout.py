"""SkillOpt-Sleep — multi-rollout + contrastive reflection (the imagination core).

The core idea: let the agent re-run the SAME task many times, then look at
which rollouts went well vs badly and distill a rule from the *contrast*. This
is a much stronger learning signal than a single failure, and it is the essence
of the offline "dream/imagination" process — train-time rollouts are synthetic,
so doing many is fine.

Pieces:
  * multi_rollout   — run one task K times under (skill, memory), return scored attempts
  * contrastive_reflect — given good vs bad attempts of the same tasks, ask the
    optimizer what distinguishes them and propose a general rule

Driven through the Backend abstraction (mock/claude/codex), import-light.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from skillopt_sleep.backend import Backend, _extract_json
from skillopt_sleep.replay import replay_one
from skillopt_sleep.types import EditRecord, ReplayResult, TaskRecord


@dataclass
class RolloutSet:
    """K scored attempts at one task under a fixed (skill, memory)."""
    task: TaskRecord
    attempts: List[ReplayResult] = field(default_factory=list)

    @property
    def best(self) -> Optional[ReplayResult]:
        return max(self.attempts, key=lambda r: r.hard, default=None)

    @property
    def worst(self) -> Optional[ReplayResult]:
        return min(self.attempts, key=lambda r: r.hard, default=None)

    @property
    def spread(self) -> float:
        if not self.attempts:
            return 0.0
        hs = [r.hard for r in self.attempts]
        return max(hs) - min(hs)

    @property
    def pass_rate(self) -> float:
        if not self.attempts:
            return 0.0
        return sum(1 for r in self.attempts if r.hard >= 1.0) / len(self.attempts)


def multi_rollout(
    backend: Backend,
    task: TaskRecord,
    skill: str,
    memory: str,
    *,
    k: int = 3,
    workers: int = 0,
) -> RolloutSet:
    """Run ``task`` K times. replay_one is deterministic for mock; for real
    backends the model's own sampling yields variation across attempts.

    The K attempts are independent, so they run concurrently (this is the dream
    phase's dominant cost). ``workers`` defaults to the SKILLOPT_SLEEP_WORKERS
    env (capped at k); set to 1 to force serial (used by the mock tests).
    """
    import os
    rs = RolloutSet(task=task)
    k = max(1, k)
    if workers <= 0:
        try:
            workers = int(os.environ.get("SKILLOPT_SLEEP_WORKERS", "1"))
        except ValueError:
            workers = 1
    workers = max(1, min(workers, k))
    if workers == 1:
        for i in range(k):
            rs.attempts.append(replay_one(backend, task, skill, memory, sample_id=i))
        return rs
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(replay_one, backend, task, skill, memory, sample_id=i)
                for i in range(k)]
        for f in futs:
            rs.attempts.append(f.result())
    return rs


def contrastive_reflect(
    backend: Backend,
    rollout_sets: List[RolloutSet],
    skill: str,
    memory: str,
    *,
    edit_budget: int = 4,
    target: str = "skill",
) -> List[EditRecord]:
    """Distill a rule from the contrast between good and bad attempts.

    We pick tasks with the highest score *spread* (some attempts passed, some
    failed) — those are the most informative — and show the optimizer a
    high-scoring vs a low-scoring attempt of each, asking what general rule makes
    the good behavior reliable.
    """
    informative = [rs for rs in rollout_sets if rs.spread > 0 and rs.best and rs.worst]
    informative.sort(key=lambda rs: rs.spread, reverse=True)
    informative = informative[:6]
    if not informative:
        return []

    blocks = []
    for rs in informative:
        blocks.append(
            f"## Task: {rs.task.intent[:160]}\n"
            f"- GOOD attempt (score {rs.best.hard:.1f}): {rs.best.response[:200]}\n"
            f"- BAD  attempt (score {rs.worst.hard:.1f}): {rs.worst.response[:200]}\n"
            f"  (bad failed: {rs.worst.fail_reason[:100]})"
        )
    # the output contract the proposed rules must not violate (same guardrail the
    # single-shot reflect uses — prevents harness-violating rules like "return VBA"
    # or "ask the user for the range" on SpreadsheetBench).
    from skillopt_sleep.backend import _task_guardrail
    guard = _task_guardrail([(rs.task, rs.best) for rs in informative])
    prompt = (
        "You are SkillOpt's optimizer doing CONTRASTIVE reflection. For each task "
        "below the agent was run multiple times; some attempts succeeded and some "
        "failed. Identify what the GOOD attempts did that the BAD ones did not, "
        f"and propose at most {edit_budget} SHORT, GENERAL, reusable rules for the "
        f"{target} that would make the good behavior reliable every time. Quote "
        "concrete thresholds/formats verbatim; do not paraphrase vaguely. "
        "Every rule MUST obey the task output contract (if shown) — never propose "
        "a rule that changes the required output format/language or tells the agent "
        "to ask the user a question; such a rule scores ZERO.\n"
        f"{guard}"
        'Return ONLY a JSON array: '
        '[{"op":"add","content":"<rule>","rationale":"<what good did that bad didnt>"}].\n\n'
        + "\n\n".join(blocks)
    )
    raw = backend._call(prompt, max_tokens=1024)  # type: ignore[attr-defined]
    arr = _extract_json(raw, "array")
    edits: List[EditRecord] = []
    if isinstance(arr, list):
        for e in arr[:edit_budget]:
            if isinstance(e, dict) and str(e.get("content", "")).strip():
                edits.append(EditRecord(
                    target=target, op=str(e.get("op", "add")).strip().lower(),
                    content=str(e["content"]).strip(),
                    rationale=str(e.get("rationale", "")).strip(),
                ))
    return edits

"""SkillOpt-Sleep — Stage 3: replay.

Re-run mined TaskRecords offline under a given (skill, memory) and score
them, producing the (hard, soft) signal SkillOpt's gate consumes.

Single-shot text replay by default. Tasks whose rule judge requires a tool
call (gbrain's `tool_called`) are run through the backend's real tool loop
(attempt_with_tools), so tool use is verified honestly rather than self-reported.
"""
from __future__ import annotations

from typing import List, Tuple

from skillopt_sleep.backend import Backend
from skillopt_sleep.types import ReplayResult, TaskRecord


def _required_tools(task: TaskRecord) -> List[str]:
    """Tool names a rule judge requires (op == 'tool_called')."""
    if task.reference_kind != "rule" or not task.judge:
        return []
    tools = []
    for c in task.judge.get("checks", []) or []:
        if isinstance(c, dict) and c.get("op") == "tool_called" and c.get("arg"):
            tools.append(str(c["arg"]))
    return tools


def replay_one(backend: Backend, task: TaskRecord, skill: str, memory: str,
               sample_id: int = 0) -> ReplayResult:
    """``sample_id`` distinguishes repeated dream rollouts of the same
    (task, skill, memory) in the attempt cache — without it all K rollouts
    collapse to one cached response and the contrastive signal is always 0."""
    import time
    tools = _required_tools(task)
    tools_called: List[str] = []
    t0 = time.time()
    tok_before = backend.tokens_used()
    if tools:
        response, tools_called = backend.attempt_with_tools(task, skill, memory, tools)
    else:
        response = backend.attempt(task, skill, memory, sample_id=sample_id)
    latency_ms = (time.time() - t0) * 1000.0
    tokens = max(0, backend.tokens_used() - tok_before)
    # if the backend doesn't track tokens (e.g. mock), approximate from text length
    if tokens == 0:
        tokens = (len(skill) + len(memory) + len(task.intent) + len(response)) // 4

    # rule judges may need the detected tool calls; score locally when possible
    if task.reference_kind == "rule" and task.judge:
        from skillopt_sleep.judges import score_rule_judge
        hard, soft, rationale = score_rule_judge(task.judge, response, tools_called)
    else:
        hard, soft, rationale = backend.judge(task, response)

    return ReplayResult(
        id=task.id,
        hard=float(hard),
        soft=float(soft),
        response=response,
        fail_reason="" if hard >= 1.0 else (rationale or "below threshold"),
        task_type=(task.tags[0] if task.tags else "task"),
        judge_rationale=rationale,
        tools_called=tools_called,
        tokens=int(tokens),
        latency_ms=round(latency_ms, 1),
    )


import os
from concurrent.futures import ThreadPoolExecutor


def replay_batch(
    backend: Backend,
    tasks: List[TaskRecord],
    skill: str,
    memory: str,
    *,
    workers: int = 0,
) -> List[Tuple[TaskRecord, ReplayResult]]:
    """Replay tasks, optionally in parallel.

    Real backends are network-bound, so a thread pool gives a large speedup on
    big test sets (like the research harness's --workers). ``workers`` defaults
    to env SKILLOPT_SLEEP_WORKERS or 1 (sequential). Mock stays sequential
    (deterministic) unless asked otherwise.
    """
    if workers <= 0:
        workers = int(os.environ.get("SKILLOPT_SLEEP_WORKERS", "1") or "1")
    if workers <= 1 or len(tasks) <= 1:
        return [(t, replay_one(backend, t, skill, memory)) for t in tasks]
    results: List = [None] * len(tasks)
    with ThreadPoolExecutor(max_workers=min(workers, len(tasks))) as ex:
        futs = {ex.submit(replay_one, backend, t, skill, memory): i
                for i, t in enumerate(tasks)}
        for fut in futs:
            i = futs[fut]
            results[i] = (tasks[i], fut.result())
    return results


def aggregate_scores(pairs: List[Tuple[TaskRecord, ReplayResult]]) -> Tuple[float, float]:
    if not pairs:
        return 0.0, 0.0
    hard = sum(r.hard for _t, r in pairs) / len(pairs)
    soft = sum(r.soft for _t, r in pairs) / len(pairs)
    return hard, soft


def aggregate_cost(pairs: List[Tuple[TaskRecord, ReplayResult]]) -> Tuple[float, float]:
    """Mean (tokens, latency_ms) per task — the cost objectives."""
    if not pairs:
        return 0.0, 0.0
    tok = sum(r.tokens for _t, r in pairs) / len(pairs)
    lat = sum(r.latency_ms for _t, r in pairs) / len(pairs)
    return tok, lat


def multi_objective_reward(
    pairs: List[Tuple[TaskRecord, ReplayResult]],
    *,
    w_acc: float = 1.0,
    w_tokens: float = 0.0,
    w_latency: float = 0.0,
    token_ref: float = 2000.0,
    latency_ref_ms: float = 15000.0,
) -> float:
    """Weighted reward = accuracy↑, tokens↓, latency↓.

    Cost terms are normalized against a reference and clamped to [0,1], so a
    response at/under the reference cost contributes ~1.0 and an expensive one
    less. Weights let the user trade off (default = accuracy only, backward
    compatible).
    """
    if not pairs:
        return 0.0
    acc, _soft = aggregate_scores(pairs)
    tok, lat = aggregate_cost(pairs)
    tok_score = max(0.0, 1.0 - tok / max(1.0, token_ref)) if token_ref else 0.0
    lat_score = max(0.0, 1.0 - lat / max(1.0, latency_ref_ms)) if latency_ref_ms else 0.0
    total_w = w_acc + w_tokens + w_latency
    if total_w <= 0:
        return acc
    return (w_acc * acc + w_tokens * tok_score + w_latency * lat_score) / total_w


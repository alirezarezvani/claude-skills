"""SkillOpt-Sleep — Stage 4: consolidate (one SkillOpt epoch).

This is the core that makes nightly evolution *safe*: it proposes bounded
edits from replayed failures, applies them to a candidate skill/memory, then
**gates** the candidate on a held-out slice of the user's own tasks. Only a
candidate that strictly improves the held-out score is accepted — the SkillOpt
validation gate, vendored self-contained in ``skillopt_sleep.gate``.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from skillopt_sleep.backend import Backend
from skillopt_sleep.memory import apply_edits
from skillopt_sleep.replay import aggregate_scores, replay_batch
from skillopt_sleep.types import EditRecord, ReplayResult, TaskRecord


# Self-contained validation gate (vendored from SkillOpt; zero dependency on the
# research package, so this open-source tool stays decoupled from the paper code).
from skillopt_sleep.gate import evaluate_gate, select_gate_score
_HAVE_REPO_GATE = True


@dataclass
class ConsolidationResult:
    accepted: bool
    gate_action: str
    baseline_score: float
    candidate_score: float
    new_skill: str
    new_memory: str
    applied_edits: List[EditRecord]
    rejected_edits: List[EditRecord]
    holdout_baseline: float
    holdout_candidate: float
    # ── observability (so a 0.0->0.0 night is self-diagnosing, not a black box) ──
    holdout_detail: List[dict] = field(default_factory=list)  # per val task: hard/soft/resp/why
    reflect_raw: str = ""        # the optimizer's last raw reply (empty => reflect produced nothing)
    call_error: str = ""         # backend's last call error (timeout/auth/empty)


def _split(tasks: List[TaskRecord]) -> Tuple[List[TaskRecord], List[TaskRecord]]:
    """Return (train_tasks, val_tasks).

    train drives reflect; val gates updates. test is held out entirely from
    consolidation and is scored by the caller. Accepts legacy split names
    (replay->train, holdout->val) for robustness.
    """
    def _norm(s: str) -> str:
        return {"replay": "train", "holdout": "val"}.get(s, s)

    train = [t for t in tasks if _norm(t.split) == "train"]
    val = [t for t in tasks if _norm(t.split) == "val"]
    # be robust if a split is empty: fall back so a night still does something,
    # but never silently use test as val.
    test = [t for t in tasks if _norm(t.split) == "test"]
    if not val:
        # prefer train as the gate reference over nothing; last resort all-but-test
        val = train or [t for t in tasks if _norm(t.split) != "test"] or tasks
    if not train:
        train = val
    return train, val


def _holdout_detail(pairs: List[Tuple[TaskRecord, ReplayResult]]) -> List[dict]:
    """Per-task held-out evidence so a 0.0 night explains itself: was the
    response empty (backend call failed) or non-empty-but-failing-checks
    (judge too strict / edit didn't help)? The two need opposite fixes."""
    out: List[dict] = []
    for t, r in pairs:
        resp = r.response or ""
        out.append({
            "id": t.id,
            "reference_kind": t.reference_kind,
            "hard": r.hard,
            "soft": r.soft,
            "response_len": len(resp),
            "response_head": resp[:200],
            "why": (r.fail_reason or r.judge_rationale or "")[:200],
        })
    return out


def consolidate(
    backend: Backend,
    tasks: List[TaskRecord],
    skill: str,
    memory: str,
    *,
    edit_budget: int = 4,
    gate_metric: str = "mixed",
    gate_mixed_weight: float = 0.5,
    gate_mode: str = "on",       # "on" (hard/soft per gate_metric) | "off" (greedy)
    rollouts_k: int = 1,         # >1 => multi-rollout contrastive reflection
    evolve_skill: bool = True,
    evolve_memory: bool = True,
    night: int = 1,
) -> ConsolidationResult:
    """Run one consolidation epoch: reflect -> bounded edit -> gate.

    train tasks drive reflect; val tasks gate the update (test is held out by the
    caller). With ``gate_mode='off'`` edits are accepted greedily (no val-improve
    requirement) — the user opts out of hard filtering — but val scores are still
    recorded so the report shows whether quality moved.

    Skill and memory are evolved in sequence (skill first if both enabled).
    """
    train_tasks, val_tasks = _split(tasks)
    gate_off = str(gate_mode).strip().lower() in {"off", "none", "false", "greedy"}
    holdout_detail: List[dict] = []

    # ── baseline on the VAL slice (the gate reference) ────────────────────
    # When the gate is OFF the user has opted out of holding out a validation set
    # (the daily-use design): we accept edits greedily and judge quality only on
    # the real test set, scored by the caller. So we SKIP all val scoring — it is
    # both wasted cost and contrary to the "no val set required" design.
    if gate_off:
        base_hard, base_soft = 0.0, 0.0
    else:
        base_pairs = replay_batch(backend, val_tasks, skill, memory)
        base_hard, base_soft = aggregate_scores(base_pairs)
        holdout_detail = _holdout_detail(base_pairs)
    base_score = select_gate_score(base_hard, base_soft, gate_metric, gate_mixed_weight)

    # ── reflect over TRAIN-split failures/successes ───────────────────────
    train_pairs = replay_batch(backend, train_tasks, skill, memory)
    failures = [(t, r) for (t, r) in train_pairs if r.hard < 1.0]
    successes = [(t, r) for (t, r) in train_pairs if r.hard >= 1.0]

    cand_skill, cand_memory = skill, memory
    all_applied: List[EditRecord] = []
    all_rejected: List[EditRecord] = []

    def _gate_apply(doc: str, edits: List[EditRecord], which: str) -> str:
        nonlocal cand_skill, cand_memory, base_score, all_applied, all_rejected
        if not edits:
            return doc
        new_doc, applied = apply_edits(doc, edits)
        if not applied:
            return doc
        # gate OFF: accept greedily with NO val scoring (the daily-use path)
        if gate_off:
            all_applied.extend(applied)
            return new_doc
        # gate ON: score the candidate on the VAL slice, keep only if it improves
        trial_skill = new_doc if which == "skill" else cand_skill
        trial_memory = new_doc if which == "memory" else cand_memory
        pairs = replay_batch(backend, val_tasks, trial_skill, trial_memory)
        h, s = aggregate_scores(pairs)
        cand_score = select_gate_score(h, s, gate_metric, gate_mixed_weight)
        if cand_score > base_score:
            base_score = max(base_score, cand_score)
            all_applied.extend(applied)
            return new_doc
        all_rejected.extend(applied)
        return doc

    if evolve_skill:
        if rollouts_k > 1:
            # multi-rollout contrastive reflection: run each train task K times
            # and distill a rule from the good-vs-bad contrast (the imagination signal).
            from skillopt_sleep.rollout import multi_rollout, contrastive_reflect
            # Parallelize across tasks (each multi_rollout also parallelizes its K
            # attempts). This dream phase is the dominant cost; serial execution
            # times out on real backends. Cap total in-flight at the worker env.
            import os
            from concurrent.futures import ThreadPoolExecutor
            try:
                _w = int(os.environ.get("SKILLOPT_SLEEP_WORKERS", "1"))
            except ValueError:
                _w = 1
            if _w > 1 and len(train_tasks) > 1:
                # split the worker budget between task-parallelism and per-task K
                task_workers = max(1, min(len(train_tasks), _w))
                per_task = max(1, _w // task_workers)
                with ThreadPoolExecutor(max_workers=task_workers) as ex:
                    sets = list(ex.map(
                        lambda t: multi_rollout(backend, t, cand_skill, cand_memory,
                                                k=rollouts_k, workers=per_task),
                        train_tasks))
            else:
                sets = [multi_rollout(backend, t, cand_skill, cand_memory,
                                      k=rollouts_k, workers=1)
                        for t in train_tasks]
            edits = contrastive_reflect(
                backend, sets, cand_skill, cand_memory,
                edit_budget=edit_budget, target="skill",
            )
            # fall back to single-shot reflect if contrast yielded nothing
            if not edits:
                edits = backend.reflect(
                    failures, successes, cand_skill, cand_memory,
                    edit_budget=edit_budget, evolve_skill=True, evolve_memory=False,
                )
        else:
            edits = backend.reflect(
                failures, successes, cand_skill, cand_memory,
                edit_budget=edit_budget, evolve_skill=True, evolve_memory=False,
            )
        cand_skill = _gate_apply(cand_skill, edits, "skill")

    if evolve_memory:
        # re-evaluate failures under the (possibly improved) skill
        train_pairs2 = replay_batch(backend, train_tasks, cand_skill, cand_memory)
        failures2 = [(t, r) for (t, r) in train_pairs2 if r.hard < 1.0]
        successes2 = [(t, r) for (t, r) in train_pairs2 if r.hard >= 1.0]
        edits_m = backend.reflect(
            failures2, successes2, cand_skill, cand_memory,
            edit_budget=edit_budget, evolve_skill=False, evolve_memory=True,
        )
        cand_memory = _gate_apply(cand_memory, edits_m, "memory")

    # ── final decision ────────────────────────────────────────────────────
    if gate_off:
        # greedy mode: no val scoring at all. Keep whatever edits we applied; the
        # caller measures real quality on the test set. We report holdout_candidate
        # as 0.0 (val intentionally not computed in this variant).
        final_hard, final_soft = 0.0, 0.0
        final_score = 0.0
        accepted = bool(all_applied)
        action = "greedy_applied" if all_applied else "greedy_noop"
        base_gate_score = 0.0
    else:
        # scored on the VAL slice (the gate reference)
        final_pairs = replay_batch(backend, val_tasks, cand_skill, cand_memory)
        final_hard, final_soft = aggregate_scores(final_pairs)
        final_score = select_gate_score(final_hard, final_soft, gate_metric, gate_mixed_weight)
        base_gate_score = select_gate_score(base_hard, base_soft, gate_metric, gate_mixed_weight)
        if _HAVE_REPO_GATE:
            gate = evaluate_gate(
                candidate_skill=cand_skill,
                cand_hard=final_hard,
                current_skill=skill,
                current_score=base_gate_score,
                best_skill=skill,
                best_score=base_gate_score,
                best_step=night - 1,
                global_step=night,
                cand_soft=final_soft,
                metric=gate_metric,
                mixed_weight=gate_mixed_weight,
            )
            action = gate.action
            accepted = bool(all_applied) and final_score > base_gate_score
        else:
            action = "accept" if final_score > base_gate_score else "reject"
            accepted = bool(all_applied) and final_score > base_gate_score

    return ConsolidationResult(
        accepted=accepted,
        gate_action=action,
        baseline_score=base_gate_score,
        candidate_score=final_score,
        new_skill=cand_skill if accepted else skill,
        new_memory=cand_memory if accepted else memory,
        applied_edits=all_applied,
        rejected_edits=all_rejected,
        holdout_baseline=base_hard,
        holdout_candidate=final_hard,
        holdout_detail=holdout_detail,
        reflect_raw=getattr(backend, "last_reflect_raw", "") or "",
        call_error=getattr(backend, "last_call_error", "") or "",
    )

"""SkillOpt-Sleep — dream + associative recall for nightly consolidation.

Two opt-in mechanisms (both default OFF, so the cycle is unchanged unless the
user enables them) that the deployment experiments validated:

  * dream rollouts  — run each task K times and learn from the good-vs-bad
    contrast (set ``dream_rollouts > 1``). Stronger signal than one failure.
  * associative recall — each night, pull the K past tasks most similar to
    tonight's new ones into the dream (set ``recall_k > 0``). Replays relevant
    experience without re-running the whole history.

``dream_consolidate`` wires recall + synthetic augmentation + multi-rollout
consolidation and is called by BOTH the shipped plugin cycle and the benchmark
experiment harness, so the reported numbers exercise the exact code the plugin
runs. Pure-stdlib, zero research/private dependency.
"""
from __future__ import annotations

import re
from typing import List, Optional

from skillopt_sleep.consolidate import ConsolidationResult, consolidate
from skillopt_sleep.types import TaskRecord


# ── synthetic augmentation ("dream up" variants of today's tasks) ─────────────

_WRAPPERS = [
    "(quick one) {q}",
    "Please handle this request: {q}",
    "For the daily report: {q}",
]


def dream_augment(real_tasks: List[TaskRecord], *, factor: int = 1) -> List[TaskRecord]:
    """Create synthetic TRAIN variants of real tasks (origin='dream').

    A light, deterministic rephrasing. Dream tasks are training-only — they
    carry split='train' and never enter the val/test slices the gate scores on.
    """
    out: List[TaskRecord] = []
    for t in real_tasks:
        for k in range(max(0, factor)):
            w = _WRAPPERS[k % len(_WRAPPERS)]
            out.append(TaskRecord(
                id=f"{t.id}_dream{k}", project=t.project,
                intent=w.format(q=t.intent), context_excerpt=t.context_excerpt,
                reference_kind=t.reference_kind, reference=t.reference,
                judge=dict(t.judge), system=t.system,
                tags=list(t.tags) + ["dream"], split="train",
                origin="dream", derived_from=t.id,
            ))
    return out


# ── associative recall (experience replay of similar past tasks) ──────────────

def _tokens(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(w) > 2}


def recall_similar(new_tasks: List[TaskRecord], history: List[TaskRecord],
                   k: int) -> List[TaskRecord]:
    """Return the ``k`` historical tasks most lexically similar to any of
    tonight's ``new_tasks`` (max Jaccard token overlap). Recalled tasks are
    returned as training material (split='train'); deterministic, stdlib-only.
    """
    if not history or k <= 0 or not new_tasks:
        return []
    new_tok = [_tokens(t.intent) for t in new_tasks]
    new_ids = {t.id for t in new_tasks}
    scored = []
    for h in history:
        if h.id in new_ids:
            continue
        ht = _tokens(h.intent)
        if not ht:
            continue
        sim = max(((len(ht & nt) / len(ht | nt)) if (ht | nt) else 0.0) for nt in new_tok)
        scored.append((sim, h.id, h))
    scored.sort(key=lambda x: (-x[0], x[1]))
    out = []
    for sim, _id, h in scored[:max(0, k)]:
        if sim <= 0.0:
            break
        # recall as training material; copy so the source archive is untouched
        out.append(TaskRecord(
            id=f"recall:{h.id}", project=h.project, intent=h.intent,
            context_excerpt=h.context_excerpt, reference_kind=h.reference_kind,
            reference=h.reference, judge=dict(h.judge), system=h.system,
            tags=list(h.tags) + ["recall"], split="train", origin="real",
            derived_from=h.id,
        ))
    return out


# ── the shared nightly consolidation step ─────────────────────────────────────

def dream_consolidate(
    backend,
    tasks: List[TaskRecord],
    skill: str,
    memory: str,
    *,
    history_tasks: Optional[List[TaskRecord]] = None,
    recall_k: int = 0,
    dream_rollouts: int = 1,
    dream_factor: int = 0,
    edit_budget: int = 4,
    gate_metric: str = "mixed",
    gate_mixed_weight: float = 0.5,
    gate_mode: str = "on",
    evolve_skill: bool = True,
    evolve_memory: bool = True,
    night: int = 1,
) -> ConsolidationResult:
    """Recall similar past experience + dream synthetic variants, then run one
    gated consolidation epoch over the enlarged training pool.

    ``tasks`` is the split-tagged pool for tonight (train + val); recall and
    augmentation only enlarge the TRAIN split, so the val slice the gate scores
    on is never polluted. With ``recall_k=0`` and ``dream_rollouts=1`` (the
    defaults) this is exactly the previous single-shot ``consolidate``.
    """
    train = [t for t in tasks if t.split == "train"]
    enlarged = list(tasks)
    if recall_k > 0 and history_tasks:
        enlarged += recall_similar(train, history_tasks, recall_k)
    if dream_factor > 0:
        seed = [t for t in enlarged if t.split == "train" and t.origin != "dream"]
        enlarged += dream_augment(seed, factor=dream_factor)
    return consolidate(
        backend, enlarged, skill, memory,
        edit_budget=edit_budget, gate_metric=gate_metric,
        gate_mixed_weight=gate_mixed_weight, gate_mode=gate_mode,
        rollouts_k=dream_rollouts, evolve_skill=evolve_skill,
        evolve_memory=evolve_memory, night=night,
    )

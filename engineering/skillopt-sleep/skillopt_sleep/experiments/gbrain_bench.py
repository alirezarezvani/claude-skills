"""SkillOpt-Sleep — gbrain-evals benchmark adapter.

Loads gbrain-evals' `skillopt-v1` benchmark (deficient skills + train/held-out
task sets with rule-based judges) into our TaskRecord format, so we can run the
SkillOpt-Sleep cycle against the SAME suite gbrain publishes a scorecard for:

  docs/benchmarks/2026-06-03-skillopt.md  — "4/4 skills 0 -> 1.00"

Each gbrain seed dir has:
  SKILL.md          — the deliberately deficient starting skill
  benchmark.jsonl   — training tasks  {task_id, task, judge:{kind:"rule",checks}}
  held-out.jsonl    — held-out tasks (same judge shape, unseen items)

We map:
  benchmark.jsonl -> TaskRecords with split="replay"
  held-out.jsonl  -> TaskRecords with split="holdout"
  judge           -> TaskRecord.judge (+ reference_kind="rule")

This lets us reproduce gbrain's headline result with our engine and either the
claude or codex backend, scoring locally via skillopt_sleep.judges (no judge API).
"""
from __future__ import annotations

import json
import os
from typing import Dict, List, Optional, Tuple

from skillopt_sleep.types import TaskRecord


SEED_DIRS = {
    "brief-writer": "seed-missing-structure",
    "thorough-analyst": "seed-verbose",
    "advisor": "seed-no-verdict",
    "quick-answerer": "seed-no-brain-first",
}


def _load_jsonl(path: str) -> List[dict]:
    out: List[dict] = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def _to_task(rec: dict, *, seed: str, split: str) -> TaskRecord:
    return TaskRecord(
        id=f"{seed}:{rec.get('task_id', '')}",
        project=f"gbrain/{seed}",
        intent=str(rec.get("task", "")),
        reference_kind="rule",
        judge=rec.get("judge", {}) or {},
        tags=[f"seed:{seed}"],
        split=split,
    )


def load_seed(data_root: str, seed: str, *, val_fraction: float = 0.34,
              split_seed: int = 42) -> Tuple[str, List[TaskRecord]]:
    """Return (deficient_skill_md, tasks) for one gbrain seed.

    Faithful split mapping:
      * gbrain held-out.jsonl  -> our ``test`` (the true final measure)
      * gbrain benchmark.jsonl -> split deterministically into ``train`` + ``val``
        (val gates updates; train drives reflect)
    All tasks are origin='real' (gbrain provides no synthetic tasks).
    """
    import hashlib
    sub = SEED_DIRS.get(seed, seed)
    seed_dir = os.path.join(data_root, sub)
    skill_path = os.path.join(seed_dir, "SKILL.md")
    skill = ""
    if os.path.exists(skill_path):
        with open(skill_path, encoding="utf-8") as f:
            skill = f.read()
    tasks: List[TaskRecord] = []
    # benchmark pool -> train/val
    val_cut = int(round(val_fraction * 100))
    for rec in _load_jsonl(os.path.join(seed_dir, "benchmark.jsonl")):
        t = _to_task(rec, seed=seed, split="train")
        bucket = int(hashlib.sha256((str(split_seed) + t.id).encode()).hexdigest(), 16) % 100
        t.split = "val" if bucket < val_cut else "train"
        tasks.append(t)
    # held-out -> test
    for rec in _load_jsonl(os.path.join(seed_dir, "held-out.jsonl")):
        tasks.append(_to_task(rec, seed=seed, split="test"))
    # guarantee a non-empty val
    if not any(t.split == "val" for t in tasks):
        train_only = [t for t in tasks if t.split == "train"]
        if train_only:
            train_only[0].split = "val"
    return skill, tasks


def available_seeds(data_root: str) -> List[str]:
    return [s for s, sub in SEED_DIRS.items()
            if os.path.isdir(os.path.join(data_root, sub))]


def find_data_root(explicit: str = "") -> Optional[str]:
    """Locate eval/data/skillopt-v1 from common clone locations."""
    cands = [explicit] if explicit else []
    cands += [
        os.path.expanduser("~/git/gbrain-evals/eval/data/skillopt-v1"),
        "/tmp/gbrain-evals/eval/data/skillopt-v1",
        os.path.expanduser("~/gbrain-evals/eval/data/skillopt-v1"),
    ]
    for c in cands:
        if c and os.path.isdir(c):
            return c
    return None

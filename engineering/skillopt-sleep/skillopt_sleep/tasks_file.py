"""Reviewed task-file helpers for privacy-safe SkillOpt-Sleep runs."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Tuple

from skillopt_sleep.mine import assign_splits, normalize_legacy_split
from skillopt_sleep.types import TaskRecord


def make_tasks_payload(
    tasks: List[TaskRecord],
    *,
    project: str,
    transcript_source: str = "",
    n_sessions: int = 0,
    target_skill_path: str = "",
) -> Dict[str, Any]:
    return {
        "format": "skillopt_sleep.tasks.v1",
        "project": project,
        "transcript_source": transcript_source,
        "n_sessions": n_sessions,
        "target_skill_path": target_skill_path,
        "reviewed": False,
        "tasks": [t.to_dict() for t in tasks],
    }


def write_tasks_file(path: str, payload: Dict[str, Any]) -> str:
    out = os.path.abspath(os.path.expanduser(path))
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return out


def _normalize_tasks(
    tasks: List[TaskRecord],
    *,
    holdout_fraction: float,
    seed: int,
) -> List[TaskRecord]:
    for task in tasks:
        task.split = normalize_legacy_split(task.split or "train")
    if len(tasks) >= 2 and not any(task.split in {"val", "test"} for task in tasks):
        tasks = assign_splits(tasks, holdout_fraction=holdout_fraction, seed=seed)
    return tasks


def load_tasks_file(
    path: str,
    *,
    holdout_fraction: float = 0.34,
    seed: int = 42,
) -> Tuple[List[TaskRecord], Dict[str, Any]]:
    source = os.path.abspath(os.path.expanduser(path))
    with open(source, encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        meta: Dict[str, Any] = {"format": "skillopt_sleep.tasks.v1", "tasks_file": source}
        raw_tasks = payload
    elif isinstance(payload, dict):
        meta = {k: v for k, v in payload.items() if k != "tasks"}
        meta["tasks_file"] = source
        raw_tasks = payload.get("tasks", [])
    else:
        raise ValueError("tasks file must contain a JSON object with tasks or a JSON task array")
    if not isinstance(raw_tasks, list):
        raise ValueError("tasks file field 'tasks' must be an array")

    tasks: List[TaskRecord] = []
    for item in raw_tasks:
        if not isinstance(item, dict):
            raise ValueError("each task entry must be a JSON object")
        tasks.append(TaskRecord.from_dict(item))
    return _normalize_tasks(tasks, holdout_fraction=holdout_fraction, seed=seed), meta

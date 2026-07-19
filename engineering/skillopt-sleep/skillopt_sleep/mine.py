"""SkillOpt-Sleep — Stage 2: mine.

Turn :class:`SessionDigest` objects into :class:`TaskRecord` training units.

Two miners:
  * heuristic_mine  — deterministic, no API. Detects retry chains (a prompt
    re-asked after negative feedback => the early attempt failed), extracts
    the user's recurring intents, and labels outcomes from feedback signals.
  * llm_mine        — optional; uses an optimizer backend to produce richer
    TaskRecords with checkable references. Falls back to heuristic on error.

The heuristic miner is what makes the whole cycle runnable offline and is the
basis of the deterministic experiment.
"""
from __future__ import annotations

import hashlib
import os
import re
from collections import Counter
from typing import Any, Callable, List, Optional, Set, Tuple

from skillopt_sleep.types import SessionDigest, TaskRecord


def _tid(project: str, intent: str) -> str:
    h = hashlib.sha256((project + "::" + intent).encode("utf-8")).hexdigest()[:12]
    return "task_" + h


def _short(text: str, n: int = 600) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + " …"


def _looks_negative(signals: List[str]) -> bool:
    return any(s.startswith("neg:") for s in signals)


def _looks_positive(signals: List[str]) -> bool:
    return any(s.startswith("pos:") for s in signals)


_TARGET_STOPWORDS = {
    "about", "after", "again", "agent", "agents", "all", "also", "always",
    "and", "any", "are", "before", "being", "but", "can", "codex",
    "current", "default", "docs", "does", "done", "each", "file", "files",
    "for", "from", "have", "into", "keep", "must", "not", "only", "path",
    "paths", "project", "read", "repo", "request", "requests", "rule",
    "rules", "same", "should", "skill", "skills", "source", "start",
    "task", "tasks", "that", "the", "their", "then", "this", "unless",
    "update", "user", "users", "when", "with", "work", "workflow",
}


def _target_tokens(text: str) -> List[str]:
    tokens: List[str] = []
    for raw in re.findall(r"[\w][\w.-]*", (text or "").lower(), flags=re.UNICODE):
        parts = [raw] + re.split(r"[\W_]+", raw, flags=re.UNICODE)
        for part in parts:
            if len(part) < 3 or part.isdigit() or part in _TARGET_STOPWORDS:
                continue
            tokens.append(part)
    return tokens


def _expand_target_keywords(keywords: Set[str]) -> None:
    if "mcp" in keywords:
        keywords.update({
            "configure", "configuration", "connect", "connected", "enable",
            "enabled", "install", "installed", "server", "servers",
            "настрой", "настроить", "подключи", "подключить",
        })
    if {"conflict", "conflicts"} & keywords:
        keywords.update({
            "cherry", "conflict", "conflicts", "git", "merge", "rebase",
            "unmerged", "конфликт", "конфликты",
        })


def target_task_keywords(
    target_skill_text: str,
    target_skill_path: str = "",
    *,
    limit: int = 180,
) -> Tuple[Set[str], Set[str]]:
    """Return (strong, weak) keywords that describe a target skill."""
    path_text = (target_skill_path or "").replace(os.sep, " ")
    headings = "\n".join(re.findall(r"(?m)^#+\s+(.+)$", target_skill_text or ""))
    strong = set(_target_tokens(path_text + "\n" + headings))
    weak = set(strong)
    counts = Counter(_target_tokens(target_skill_text or ""))
    for token, _count in counts.most_common(limit):
        weak.add(token)
    _expand_target_keywords(strong)
    _expand_target_keywords(weak)
    return strong, weak


def _task_search_text(task: TaskRecord) -> str:
    return "\n".join([
        task.intent or "",
        task.context_excerpt or "",
        " ".join(task.tags or []),
    ])


def filter_tasks_for_target(
    tasks: List[TaskRecord],
    target_skill_text: str,
    target_skill_path: str = "",
) -> List[TaskRecord]:
    """Prefer tasks whose language overlaps the explicit target skill.

    If nothing matches, return the original list. This keeps a target run useful
    even when transcripts are too sparse or the skill is too generic.
    """
    strong, weak = target_task_keywords(target_skill_text, target_skill_path)
    if not tasks or not (strong or weak):
        return tasks

    ranked = []
    for idx, task in enumerate(tasks):
        tokens = set(_target_tokens(_task_search_text(task)))
        strong_hits = tokens & strong
        weak_hits = tokens & weak
        if not strong_hits and len(weak_hits) < 2:
            continue
        score = len(strong_hits) * 3 + len(weak_hits)
        ranked.append((score, idx, task))
    if not ranked:
        return tasks
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [task for _score, _idx, task in ranked]


def heuristic_mine(
    digests: List[SessionDigest],
    *,
    max_tasks: int = 40,
) -> List[TaskRecord]:
    """Deterministic miner — no API calls.

    Strategy:
      * Each session with >=1 real user prompt yields one TaskRecord whose
        intent is the FIRST substantive prompt (the original ask).
      * Outcome is inferred:
          - negative feedback present and no later positive  -> "fail"
          - positive feedback present                         -> "success"
          - re-asks (multiple user turns) without resolution  -> "mixed"
          - otherwise                                         -> "unknown"
      * attempted_solution = the last assistant final (what was produced).
      * reference_kind defaults to "none"; the consolidation step will use a
        rubric judge for these. (Exact refs are added by the experiment data
        or by the LLM miner when it can derive a checkable answer.)
    """
    tasks: List[TaskRecord] = []
    for d in digests:
        if not d.user_prompts:
            continue
        intent = d.user_prompts[0]
        if len(intent.strip()) < 8:
            continue
        if _looks_positive(d.feedback_signals) and not _looks_negative(d.feedback_signals):
            outcome = "success"
        elif _looks_negative(d.feedback_signals):
            outcome = "fail"
        elif d.n_user_turns >= 3:
            outcome = "mixed"
        else:
            outcome = "unknown"

        attempted = d.assistant_finals[-1] if d.assistant_finals else ""
        context = ""
        if len(d.user_prompts) > 1:
            # later prompts often carry the corrective detail / real constraints
            context = "Follow-up constraints from the same session:\n- " + "\n- ".join(
                _short(p, 200) for p in d.user_prompts[1:4]
            )
        tags = []
        if d.tools_used:
            tags.append("tools:" + "+".join(d.tools_used[:4]))
        if d.git_branch:
            tags.append("branch:" + d.git_branch)

        tasks.append(
            TaskRecord(
                id=_tid(d.project, intent),
                project=d.project,
                intent=_short(intent, 800),
                context_excerpt=_short(context, 600),
                attempted_solution=_short(attempted, 600),
                outcome=outcome,
                reference_kind="none",
                reference="",
                tags=tags,
                source_sessions=[d.session_id],
            )
        )
        if len(tasks) >= max_tasks:
            break
    return tasks


def dedup_tasks(tasks: List[TaskRecord]) -> List[TaskRecord]:
    """Merge tasks sharing an id (same project+intent across sessions)."""
    by_id: dict = {}
    for t in tasks:
        if t.id in by_id:
            ex = by_id[t.id]
            ex.source_sessions = list(dict.fromkeys(ex.source_sessions + t.source_sessions))
            # prefer a resolved outcome if either session resolved it
            order = {"success": 3, "fail": 2, "mixed": 1, "unknown": 0}
            if order.get(t.outcome, 0) > order.get(ex.outcome, 0):
                ex.outcome = t.outcome
        else:
            by_id[t.id] = t
    return list(by_id.values())


def assign_splits(
    tasks: List[TaskRecord],
    *,
    val_fraction: float = 0.34,
    test_fraction: float = 0.0,
    holdout_fraction: float | None = None,  # legacy alias for val_fraction
    seed: int = 42,
) -> List[TaskRecord]:
    """Deterministically split tasks into train / val / test.

    Anti-overfitting contract (the user's design):
      * ``val`` and ``test`` are drawn ONLY from REAL mined tasks (origin=='real')
        and never overlap. val gates updates; test is the final held-out measure.
      * ``train`` may include DREAM-augmented tasks (origin=='dream'); those are
        NEVER placed in val/test.

    A stable hash of the task id keeps the same real task in the same split across
    nights (a fixed held-out gate, like SkillOpt's D_sel/D_test).

    Back-compat: if ``test_fraction`` is 0 (default), this behaves like the old
    two-way replay/holdout split — real tasks divide into train + val, no test.
    ``holdout_fraction`` is accepted as an alias for ``val_fraction``.
    """
    if holdout_fraction is not None:
        val_fraction = holdout_fraction

    dream = [t for t in tasks if t.origin == "dream"]
    real = [t for t in tasks if t.origin != "dream"]

    # all dream tasks go to train, unconditionally
    for t in dream:
        t.split = "train"

    val_cut = int(round(val_fraction * 100))
    test_cut = val_cut + int(round(test_fraction * 100))
    for t in real:
        bucket = int(hashlib.sha256((str(seed) + t.id).encode()).hexdigest(), 16) % 100
        if bucket < val_cut:
            t.split = "val"
        elif bucket < test_cut:
            t.split = "test"
        else:
            t.split = "train"

    # guarantee val (the gate) is non-empty when we have >=2 real tasks
    real_splits = {t.split for t in real}
    if len(real) >= 2 and "val" not in real_splits:
        real[-1].split = "val"
    # guarantee a train pool exists (dream or real) when possible
    if not any(t.split == "train" for t in tasks) and len(real) >= 2:
        real[0].split = "train"
    # if test was requested but ended up empty with >=3 real tasks, carve one
    if test_fraction > 0 and len(real) >= 3 and not any(t.split == "test" for t in real):
        for t in real:
            if t.split == "train":
                t.split = "test"
                break
    return tasks


def normalize_legacy_split(value: str) -> str:
    """Map old split names to the new vocabulary."""
    return {"replay": "train", "holdout": "val"}.get(value, value)


def mine(
    digests: List[SessionDigest],
    *,
    max_tasks: int = 40,
    candidate_limit: int = 0,
    holdout_fraction: float = 0.34,
    seed: int = 42,
    llm_miner: Optional[Callable[[List[SessionDigest]], List[TaskRecord]]] = None,
    target_skill_text: str = "",
    target_skill_path: str = "",
) -> List[TaskRecord]:
    """Top-level miner. Uses ``llm_miner`` if provided, else heuristic."""
    candidate_limit = candidate_limit or max_tasks
    tasks: List[TaskRecord] = []
    if llm_miner is not None:
        try:
            tasks = llm_miner(digests) or []
        except Exception:
            tasks = []
    if not tasks:
        tasks = heuristic_mine(digests, max_tasks=candidate_limit)
    tasks = dedup_tasks(tasks)
    if target_skill_text or target_skill_path:
        tasks = filter_tasks_for_target(tasks, target_skill_text, target_skill_path)
    tasks = tasks[:max_tasks]
    tasks = assign_splits(tasks, holdout_fraction=holdout_fraction, seed=seed)
    return tasks

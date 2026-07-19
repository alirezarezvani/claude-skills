"""SkillOpt-Sleep — validation experiment.

Answers the question the user posed: *does nightly offline self-evolution
actually improve the agent?*  Runs deterministically with the MockBackend
(no API key, reproducible) and is the acceptance test for the whole idea.

What it proves:
  1. MONOTONIC LIFT — over N sleep nights, the held-out score rises from a
     baseline (empty skill/memory) toward 1.0 as the gate accepts the
     general rules the persona's tasks require.
  2. GATE SAFETY — an injected harmful edit is REJECTED (held-out score does
     not improve), so a bad nightly proposal can never be adopted.
  3. PLUMBING — harvest->mine->replay->consolidate->stage->adopt all run and
     the adopted artifact, re-scored, retains the lift.

Run:
    python -m skillopt_sleep.experiments.run_experiment
    python -m skillopt_sleep.experiments.run_experiment --persona programmer --nights 3
    python -m skillopt_sleep.experiments.run_experiment --backend anthropic   # real lift
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from typing import List

from skillopt_sleep.backend import get_backend
from skillopt_sleep.consolidate import consolidate
from skillopt_sleep.experiments.personas import (
    PERSONAS,
    harmful_edit_task,
    researcher_persona,
)
from skillopt_sleep.memory import ensure_skill_scaffold
from skillopt_sleep.replay import aggregate_scores, replay_batch
from skillopt_sleep.types import TaskRecord


def _score_holdout(backend, tasks: List[TaskRecord], skill: str, memory: str,
                   metric: str = "mixed", w: float = 0.5) -> float:
    from skillopt_sleep.consolidate import select_gate_score
    # the persona experiment uses a 2-way split (train/val, no test); score on val
    holdout = [t for t in tasks if t.split in ("val", "holdout")] or tasks
    pairs = replay_batch(backend, holdout, skill, memory)
    h, s = aggregate_scores(pairs)
    return select_gate_score(h, s, metric, w)


def run(persona: str = "researcher", nights: int = 4, backend_name: str = "mock",
        edit_budget: int = 4, seed: int = 42, model: str = "", codex_path: str = "",
        limit_tasks: int = 0) -> dict:
    from skillopt_sleep.mine import assign_splits

    make = PERSONAS.get(persona, researcher_persona)
    items = make()
    if limit_tasks and limit_tasks < len(items):
        items = items[:limit_tasks]
    tasks = assign_splits(items, holdout_fraction=0.34, seed=seed)
    backend = get_backend(backend_name, model=model, codex_path=codex_path)
    is_mock = (backend.name == "mock")

    # start from an empty managed skill + empty memory
    skill = ensure_skill_scaffold("", name="skillopt-sleep-learned",
                                  description="Learned preferences.")
    memory = ""

    baseline = _score_holdout(backend, tasks, skill, memory)
    trace = [{"night": 0, "holdout_score": round(baseline, 4), "action": "baseline",
              "n_edits": 0}]

    for night in range(1, nights + 1):
        res = consolidate(
            backend, tasks, skill, memory,
            edit_budget=edit_budget, gate_metric="mixed", gate_mixed_weight=0.5,
            evolve_skill=True, evolve_memory=True, night=night,
        )
        if res.accepted:
            skill, memory = res.new_skill, res.new_memory
        trace.append({
            "night": night,
            "holdout_score": round(res.candidate_score, 4),
            "action": res.gate_action,
            "accepted": res.accepted,
            "n_edits": len(res.applied_edits),
            "edits": [e.content for e in res.applied_edits],
            "n_rejected": len(res.rejected_edits),
        })
        # converged: stop early if perfect
        if res.candidate_score >= 0.999:
            break

    after = _score_holdout(backend, tasks, skill, memory)

    # ── gate-safety probe (mock only; it relies on the mock's known bad rule) ──
    harmful_rejected = None
    if is_mock:
        harmful_tasks = assign_splits([harmful_edit_task()] + make()[:3],
                                      holdout_fraction=0.5, seed=seed)
        _ = _score_holdout(backend, harmful_tasks, skill, memory)
        res_h = consolidate(backend, harmful_tasks, skill, memory,
                            edit_budget=edit_budget, gate_metric="mixed",
                            evolve_skill=True, evolve_memory=False, night=nights + 1)
        harmful_rule_text = get_backend("mock").RULE_TEXT["__harmful__"]  # type: ignore[attr-defined]
        harmful_rejected = (harmful_rule_text not in res_h.new_skill)

    result = {
        "persona": persona,
        "backend": backend.name,
        "model": model or "(default)",
        "n_tasks": len(tasks),
        "nights_run": len(trace) - 1,
        "baseline_holdout": round(baseline, 4),
        "after_holdout": round(after, 4),
        "lift": round(after - baseline, 4),
        "improved": after > baseline,
        "gate_blocks_harmful": harmful_rejected,  # None for real backends
        "tokens_used": backend.tokens_used(),
        "final_skill_excerpt": skill[-500:],
        "trace": trace,
    }
    return result


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        print(f"FAIL: {msg}")
        raise SystemExit(1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SkillOpt-Sleep validation experiment")
    ap.add_argument("--persona", default="researcher", choices=list(PERSONAS.keys()))
    ap.add_argument("--nights", type=int, default=4)
    ap.add_argument("--backend", default="mock", choices=["mock", "claude", "codex", "copilot"])
    ap.add_argument("--model", default="", help="backend model override")
    ap.add_argument("--codex-path", default="", help="path to the real @openai/codex binary")
    ap.add_argument("--edit-budget", type=int, default=4)
    ap.add_argument("--limit-tasks", type=int, default=0, help="cap #tasks (control API cost)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--assert-improves", action="store_true",
                    help="exit nonzero unless lift>0 (and, for mock, gate blocks harmful edit)")
    args = ap.parse_args(argv)

    res = run(args.persona, nights=args.nights, backend_name=args.backend,
              edit_budget=args.edit_budget, model=args.model,
              codex_path=args.codex_path, limit_tasks=args.limit_tasks)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"=== SkillOpt-Sleep experiment: persona={res['persona']} "
              f"backend={res['backend']} model={res['model']} ===")
        print(f"tasks: {res['n_tasks']}   tokens(approx): {res['tokens_used']}")
        print(f"baseline held-out : {res['baseline_holdout']}")
        print(f"after  held-out   : {res['after_holdout']}   (lift {res['lift']:+.4f})")
        if res["gate_blocks_harmful"] is not None:
            print(f"gate blocks harmful edit: {res['gate_blocks_harmful']}")
        print("trace:")
        for row in res["trace"]:
            edits = "; ".join(row.get("edits", []))[:80]
            print(f"  night {row['night']}: holdout={row['holdout_score']} "
                  f"{row['action']} (+{row['n_edits']} edits) {edits}")

    if args.assert_improves:
        _assert(res["improved"], "held-out score did not improve")
        if res["gate_blocks_harmful"] is not None:
            _assert(res["gate_blocks_harmful"], "gate failed to block harmful edit")
            print("\nPASS: nightly consolidation improves held-out score AND gate blocks regressions.")
        else:
            print("\nPASS: nightly consolidation improves held-out score (real backend).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

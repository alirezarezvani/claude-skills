"""SkillOpt-Sleep — run the gbrain-evals skillopt-v1 benchmark with our engine.

Reproduces gbrain's "Result 1 — skills measurably improve" scorecard
(docs/benchmarks/2026-06-03-skillopt.md) using SkillOpt-Sleep's
consolidate() loop and either the claude or codex backend.

For each deficient seed skill:
  1. score the held-out tasks with the ORIGINAL skill            -> before
  2. run N consolidation nights on the training tasks (gated)     -> evolve skill
  3. score the held-out tasks with the EVOLVED skill             -> after

Held-out scoring is done locally by the rule judge (no judge API). Only the
agent's `attempt` (and the optimizer's `reflect`) spend tokens.

Usage:
    python -m skillopt_sleep.experiments.run_gbrain --backend mock
    python -m skillopt_sleep.experiments.run_gbrain --backend claude --seeds brief-writer --nights 2
    python -m skillopt_sleep.experiments.run_gbrain --backend codex  --data-root /tmp/gbrain-evals/eval/data/skillopt-v1
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, List, Optional

from skillopt_sleep.backend import build_backend, get_backend
from skillopt_sleep.consolidate import consolidate, select_gate_score
from skillopt_sleep.experiments.gbrain_bench import (
    available_seeds,
    find_data_root,
    load_seed,
)
from skillopt_sleep.replay import aggregate_scores, replay_batch


def _score(backend, tasks, skill, memory, split="test", metric="mixed", w=0.5):
    sub = [t for t in tasks if t.split == split]
    if not sub:  # fall back to val, then everything, so we never score on nothing
        sub = [t for t in tasks if t.split == "val"] or tasks
    pairs = replay_batch(backend, sub, skill, memory)
    h, s = aggregate_scores(pairs)
    return h, s, select_gate_score(h, s, metric, w)


def run_seed(backend, seed: str, skill: str, tasks: List, *,
             nights: int = 3, edit_budget: int = 4, gate_mode: str = "on",
             slow_update: bool = True, rollouts_k: int = 1,
             limit_replay: int = 0, limit_holdout: int = 0) -> dict:
    memory = ""
    # optionally cap each split to control API cost / latency.
    # limit_replay caps train; limit_holdout caps BOTH val and test.
    if limit_replay or limit_holdout:
        train = [t for t in tasks if t.split == "train"]
        val = [t for t in tasks if t.split == "val"]
        test = [t for t in tasks if t.split == "test"]
        if limit_replay:
            train = train[:limit_replay]
        if limit_holdout:
            val = val[:limit_holdout]
            test = test[:limit_holdout]
        tasks = train + val + test
    # final measure is TEST (the gbrain held-out set); val gates internally
    bh, bs, bscore = _score(backend, tasks, skill, memory, split="test")
    trace = [{"night": 0, "test_hard": round(bh, 3), "action": "baseline"}]
    cur = skill
    first_night_skill = skill
    for night in range(1, nights + 1):
        res = consolidate(
            backend, tasks, cur, memory,
            edit_budget=edit_budget, gate_metric="mixed", gate_mixed_weight=0.5,
            gate_mode=gate_mode, rollouts_k=rollouts_k,
            evolve_skill=True, evolve_memory=False, night=night,
        )
        if res.accepted:
            cur = res.new_skill
        if night == 1:
            first_night_skill = cur
        # report the TEST score each night (independent of the val gate)
        th, _ts, _ = _score(backend, tasks, cur, memory, split="test")
        trace.append({
            "night": night,
            "val_hard": round(res.holdout_candidate, 3),
            "test_hard": round(th, 3),
            "action": res.gate_action,
            "accepted": res.accepted,
            "edits": [e.content for e in res.applied_edits],
        })
        if th >= 0.999:
            break

    # ── SLOW UPDATE: consolidate cross-night experience into the protected
    # long-term field. Runs regardless of gate mode (it is what preserves
    # long-term memory even when the gate is OFF).
    slow_text = None
    if nights >= 2 and slow_update:
        try:
            from skillopt_sleep.slow_update import run_slow_update, replace_slow_field
            val_tasks = [t for t in tasks if t.split == "val"] or tasks
            prev_pairs = replay_batch(backend, val_tasks, first_night_skill, memory)
            curr_pairs = replay_batch(backend, val_tasks, cur, memory)
            slow_text = run_slow_update(
                backend, prev_skill=first_night_skill, curr_skill=cur,
                prev_pairs=[(t, r) for t, r in prev_pairs],
                curr_pairs=[(t, r) for t, r in curr_pairs],
            )
            if slow_text:
                cur = replace_slow_field(cur, slow_text)
        except Exception:
            slow_text = None

    ah, as_, ascore = _score(backend, tasks, cur, memory, split="test")
    return {
        "seed": seed,
        "held_out_before": round(bh, 3),
        "held_out_after": round(ah, 3),
        "improved": ah > bh,
        "nights": len(trace) - 1,
        "trace": trace,
        "slow_update": slow_text,
        "final_skill_tail": cur[-400:],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run gbrain-evals skillopt-v1 with SkillOpt-Sleep")
    ap.add_argument("--backend", default="mock", choices=["mock", "claude", "codex"])
    ap.add_argument("--model", default="")
    ap.add_argument("--optimizer-backend", default="", help="route reflect/judge here (dual)")
    ap.add_argument("--optimizer-model", default="")
    ap.add_argument("--target-backend", default="", help="route attempt here (dual)")
    ap.add_argument("--target-model", default="")
    ap.add_argument("--codex-path", default="")
    ap.add_argument("--data-root", default="", help="path to eval/data/skillopt-v1")
    ap.add_argument("--seeds", default="", help="comma list; default = all available")
    ap.add_argument("--nights", type=int, default=3)
    ap.add_argument("--edit-budget", type=int, default=4)
    ap.add_argument("--gate", default="on", choices=["on", "off", "hard", "soft"],
                    help="on/hard/soft = validation-gated; off = greedy (no hard filter)")
    ap.add_argument("--rollouts-k", type=int, default=1,
                    help=">1 = multi-rollout contrastive reflection per task")
    ap.add_argument("--budget-tokens", type=int, default=0,
                    help="approx token budget; auto-plans nights x rollouts when set")
    ap.add_argument("--budget-minutes", type=float, default=0.0)
    ap.add_argument("--preferences", default="", help="free-text user preferences (prior for reflect)")
    ap.add_argument("--limit-replay", type=int, default=0, help="cap #train tasks (cost control)")
    ap.add_argument("--limit-holdout", type=int, default=0, help="cap #val and #test tasks (cost control)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    data_root = find_data_root(args.data_root)
    if not data_root:
        print("ERROR: could not find eval/data/skillopt-v1. Clone gbrain-evals and pass --data-root.",
              file=sys.stderr)
        return 2

    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()] or available_seeds(data_root)
    backend = build_backend(
        backend=args.backend, model=args.model,
        optimizer_backend=args.optimizer_backend, optimizer_model=args.optimizer_model,
        target_backend=args.target_backend, target_model=args.target_model,
        codex_path=args.codex_path, preferences=args.preferences,
    )

    results = []
    for seed in seeds:
        skill, tasks = load_seed(data_root, seed)
        if not tasks:
            continue
        # budget auto-planning: derive nights x rollouts_k from a token budget
        nights, rollouts_k = args.nights, args.rollouts_k
        if args.budget_tokens:
            from skillopt_sleep.budget import Budget, plan_depth
            n_train = len([t for t in tasks if t.split == "train"]) or len(tasks)
            nights, rollouts_k = plan_depth(
                Budget(max_tokens=args.budget_tokens), n_tasks=n_train,
                default_nights=args.nights, default_k=args.rollouts_k,
            )
            if not args.json:
                print(f"  [budget] {args.budget_tokens} tok -> nights={nights} rollouts_k={rollouts_k}")
        r = run_seed(backend, seed, skill, tasks, nights=nights,
                     edit_budget=args.edit_budget, rollouts_k=rollouts_k,
                     gate_mode=("off" if args.gate == "off" else "on"),
                     limit_replay=args.limit_replay, limit_holdout=args.limit_holdout)
        results.append(r)
        if not args.json:
            print(f"  {seed:<18} held-out {r['held_out_before']:.2f} -> {r['held_out_after']:.2f}"
                  f"  ({'IMPROVED' if r['improved'] else 'no change'}, {r['nights']} nights)")

    n_improved = sum(1 for r in results if r["improved"])
    summary = {
        "benchmark": "gbrain-evals/skillopt-v1",
        "backend": backend.name,
        "model": args.model or "(default)",
        "n_seeds": len(results),
        "n_improved": n_improved,
        "tokens_used": backend.tokens_used(),
        "results": results,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== {n_improved}/{len(results)} seeds improved on held-out "
              f"(backend={backend.name}, ~{backend.tokens_used()} tokens) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

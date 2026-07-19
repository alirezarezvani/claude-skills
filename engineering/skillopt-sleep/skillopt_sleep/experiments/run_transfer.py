"""SkillOpt-Sleep — skill-transfer experiment (sleep scenario).

Answers: "if I optimize a skill while the agent sleeps using a CHEAP model,
does the learned skill still help an EXPENSIVE model at deploy time?" — and the
reverse. This is the SkillOpt paper's cross-model transfer result, reproduced
in the sleep setting, and it is the core price-difference value proposition:
spend cheap tokens overnight, deploy the frozen skill anywhere.

Protocol, per gbrain seed:
  1. baseline_target = held-out score of the DEFICIENT skill, run on TARGET model
  2. optimize the skill for N nights using the SOURCE model (attempt+reflect)
  3. transferred = held-out score of the LEARNED skill, run on TARGET model,
     with NO further optimization
  4. (reference) direct = held-out score of a skill optimized AND run on TARGET

Report baseline / direct / transferred, mirroring SkillOpt Table "transfer".

Usage:
  python -m skillopt_sleep.experiments.run_transfer \
     --source-backend claude --source-model haiku \
     --target-backend claude --target-model sonnet \
     --seeds brief-writer --nights 2
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from skillopt_sleep.backend import get_backend
from skillopt_sleep.consolidate import consolidate, select_gate_score
from skillopt_sleep.experiments.gbrain_bench import (
    available_seeds, find_data_root, load_seed,
)
from skillopt_sleep.replay import aggregate_scores, replay_batch


def _holdout_hard(backend, tasks, skill, memory="") -> float:
    # transfer is measured on the true held-out TEST split
    ho = [t for t in tasks if t.split == "test"]
    if not ho:
        ho = [t for t in tasks if t.split in ("val", "holdout")] or tasks
    pairs = replay_batch(backend, ho, skill, memory)
    h, _s = aggregate_scores(pairs)
    return h


def _optimize(backend, skill, tasks, *, nights, edit_budget) -> str:
    cur = skill
    for night in range(1, nights + 1):
        res = consolidate(backend, tasks, cur, "",
                          edit_budget=edit_budget, gate_metric="mixed",
                          evolve_skill=True, evolve_memory=False, night=night)
        if res.accepted:
            cur = res.new_skill
        if res.holdout_candidate >= 0.999:
            break
    return cur


def run_seed(seed, skill, tasks, *, source, target, nights, edit_budget,
             limit_replay, limit_holdout, do_direct=True) -> dict:
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

    baseline_target = _holdout_hard(target, tasks, skill)

    # optimize on SOURCE, evaluate frozen skill on TARGET
    learned_on_source = _optimize(source, skill, tasks, nights=nights, edit_budget=edit_budget)
    transferred = _holdout_hard(target, tasks, learned_on_source)

    direct = None
    if do_direct:
        learned_on_target = _optimize(target, skill, tasks, nights=nights, edit_budget=edit_budget)
        direct = _holdout_hard(target, tasks, learned_on_target)

    return {
        "seed": seed,
        "baseline_target": round(baseline_target, 3),
        "direct_target": (round(direct, 3) if direct is not None else None),
        "transferred": round(transferred, 3),
        "transfer_gain": round(transferred - baseline_target, 3),
        "learned_skill_tail": learned_on_source[-300:],
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SkillOpt-Sleep cross-model transfer")
    ap.add_argument("--source-backend", default="claude")
    ap.add_argument("--source-model", default="haiku")
    ap.add_argument("--target-backend", default="claude")
    ap.add_argument("--target-model", default="sonnet")
    ap.add_argument("--codex-path", default="")
    ap.add_argument("--data-root", default="")
    ap.add_argument("--seeds", default="brief-writer")
    ap.add_argument("--nights", type=int, default=2)
    ap.add_argument("--edit-budget", type=int, default=4)
    ap.add_argument("--limit-replay", type=int, default=3)
    ap.add_argument("--limit-holdout", type=int, default=3)
    ap.add_argument("--no-direct", action="store_true", help="skip the direct reference (saves cost)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    data_root = find_data_root(args.data_root)
    if not data_root:
        print("ERROR: gbrain-evals skillopt-v1 data not found; pass --data-root", file=sys.stderr)
        return 2

    source = get_backend(args.source_backend, model=args.source_model, codex_path=args.codex_path)
    target = get_backend(args.target_backend, model=args.target_model, codex_path=args.codex_path)

    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()] or available_seeds(data_root)
    results = []
    for seed in seeds:
        skill, tasks = load_seed(data_root, seed)
        if not tasks:
            continue
        r = run_seed(seed, skill, tasks, source=source, target=target,
                     nights=args.nights, edit_budget=args.edit_budget,
                     limit_replay=args.limit_replay, limit_holdout=args.limit_holdout,
                     do_direct=not args.no_direct)
        results.append(r)
        if not args.json:
            d = f" direct={r['direct_target']}" if r['direct_target'] is not None else ""
            print(f"  {seed:<16} baseline={r['baseline_target']:.2f}"
                  f" transferred={r['transferred']:.2f}{d}"
                  f"  (gain {r['transfer_gain']:+.2f})")

    summary = {
        "experiment": "skillopt-sleep/transfer",
        "source": f"{args.source_backend}:{args.source_model}",
        "target": f"{args.target_backend}:{args.target_model}",
        "tokens_source": source.tokens_used(),
        "tokens_target": target.tokens_used(),
        "results": results,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== transfer {summary['source']} -> {summary['target']}: "
              f"{sum(1 for r in results if r['transfer_gain'] > 0)}/{len(results)} positive ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

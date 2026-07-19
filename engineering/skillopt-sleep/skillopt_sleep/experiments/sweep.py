"""SkillOpt-Sleep — benchmark sweep driver.

Runs many (backend, model, seed, transfer-pair) configurations SEQUENTIALLY in
one process, appending each result to a JSONL file as it finishes. Designed to
run unattended in the background; safe to interrupt (already-written rows
survive) and resume (skip configs whose row already exists).

Then `report.py` turns the JSONL into a presented Markdown scorecard.

Usage:
  python -m skillopt_sleep.experiments.sweep --plan quick   --out docs/sleep/sweep.jsonl
  python -m skillopt_sleep.experiments.sweep --plan full    --out docs/sleep/sweep.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List

from skillopt_sleep.backend import build_backend, get_backend
from skillopt_sleep.experiments.gbrain_bench import find_data_root, load_seed
from skillopt_sleep.experiments.run_gbrain import run_seed as bench_seed
from skillopt_sleep.experiments.run_transfer import run_seed as transfer_seed


# Plans: lists of config dicts. Kept small per-run to bound cost/latency.
def _direct_cfg(backend, model, seed, nights=2):
    return {"kind": "direct", "backend": backend, "model": model, "seed": seed, "nights": nights}


def _dual_cfg(opt_backend, opt_model, tgt_backend, tgt_model, seed, nights=2):
    # a 'direct' run on a DualBackend: strong optimizer proposes, weak target runs
    return {"kind": "dual", "optimizer_backend": opt_backend, "optimizer_model": opt_model,
            "target_backend": tgt_backend, "target_model": tgt_model, "seed": seed, "nights": nights}


def _transfer_cfg(sb, sm, tb, tm, seed, nights=2):
    return {"kind": "transfer", "source_backend": sb, "source_model": sm,
            "target_backend": tb, "target_model": tm, "seed": seed, "nights": nights}


PLANS: Dict[str, List[Dict[str, Any]]] = {
    # one cheap seed each, both backends — fast sanity
    "quick": [
        _direct_cfg("claude", "haiku", "brief-writer", 1),
        _direct_cfg("codex", "", "brief-writer", 2),
    ],
    # SkillOpt-faithful: STRONG optimizer (sonnet) proposes, WEAK target (haiku)
    # runs — the reliable config. Plus Codex self-optimized. All 4 gbrain seeds,
    # including quick-answerer (real tool loop).
    "direct": [
        _dual_cfg("claude", "sonnet", "claude", "haiku", "brief-writer"),
        _dual_cfg("claude", "sonnet", "claude", "haiku", "advisor"),
        _dual_cfg("claude", "sonnet", "claude", "haiku", "thorough-analyst"),
        _dual_cfg("claude", "sonnet", "claude", "haiku", "quick-answerer"),
        _direct_cfg("codex", "", "brief-writer"),
        _direct_cfg("codex", "", "advisor"),
        _direct_cfg("codex", "", "quick-answerer"),
    ],
    # the price-difference story: optimize cheap, deploy expensive (and reverse)
    "transfer": [
        _transfer_cfg("claude", "haiku", "claude", "sonnet", "brief-writer"),
        _transfer_cfg("claude", "sonnet", "claude", "haiku", "brief-writer"),
        _transfer_cfg("codex", "", "claude", "haiku", "brief-writer"),
        _transfer_cfg("claude", "haiku", "codex", "", "brief-writer"),
    ],
}
PLANS["full"] = PLANS["direct"] + PLANS["transfer"]


def _cfg_key(c: Dict[str, Any]) -> str:
    return json.dumps({k: c[k] for k in sorted(c)}, ensure_ascii=False)


def _load_done(out_path: str) -> set:
    done = set()
    if os.path.exists(out_path):
        with open(out_path) as f:
            for line in f:
                try:
                    row = json.loads(line)
                    if "cfg_key" in row:
                        done.add(row["cfg_key"])
                except Exception:
                    pass
    return done


def _append(out_path: str, row: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_one(cfg: Dict[str, Any], data_root: str, codex_path: str,
            limit_replay: int, limit_holdout: int) -> Dict[str, Any]:
    seed = cfg["seed"]
    skill, tasks = load_seed(data_root, seed)
    t0 = time.time()
    if cfg["kind"] in ("direct", "dual"):
        if cfg["kind"] == "dual":
            be = build_backend(
                optimizer_backend=cfg["optimizer_backend"], optimizer_model=cfg.get("optimizer_model", ""),
                target_backend=cfg["target_backend"], target_model=cfg.get("target_model", ""),
                codex_path=codex_path,
            )
        else:
            be = get_backend(cfg["backend"], model=cfg.get("model", ""), codex_path=codex_path)
        r = bench_seed(be, seed, skill, tasks, nights=cfg["nights"],
                       limit_replay=limit_replay, limit_holdout=limit_holdout)
        out = {"baseline": r["held_out_before"], "after": r["held_out_after"],
               "improved": r["improved"], "tokens": be.tokens_used()}
    else:
        src = get_backend(cfg["source_backend"], model=cfg.get("source_model", ""), codex_path=codex_path)
        tgt = get_backend(cfg["target_backend"], model=cfg.get("target_model", ""), codex_path=codex_path)
        r = transfer_seed(seed, skill, tasks, source=src, target=tgt, nights=cfg["nights"],
                          edit_budget=4, limit_replay=limit_replay, limit_holdout=limit_holdout,
                          do_direct=False)
        out = {"baseline_target": r["baseline_target"], "transferred": r["transferred"],
               "transfer_gain": r["transfer_gain"],
               "tokens": src.tokens_used() + tgt.tokens_used()}
    out.update({"cfg": cfg, "cfg_key": _cfg_key(cfg), "elapsed_s": round(time.time() - t0, 1)})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SkillOpt-Sleep benchmark sweep")
    ap.add_argument("--plan", default="quick", choices=list(PLANS.keys()))
    ap.add_argument("--out", default="docs/sleep/sweep.jsonl")
    ap.add_argument("--data-root", default="")
    ap.add_argument("--codex-path", default="")
    ap.add_argument("--limit-replay", type=int, default=3)
    ap.add_argument("--limit-holdout", type=int, default=3)
    args = ap.parse_args(argv)

    data_root = find_data_root(args.data_root)
    if not data_root:
        print("ERROR: gbrain-evals data not found; pass --data-root", file=sys.stderr)
        return 2

    plan = PLANS[args.plan]
    done = _load_done(args.out)
    print(f"[sweep] plan={args.plan} configs={len(plan)} already_done={len(done)} -> {args.out}")
    for i, cfg in enumerate(plan, 1):
        key = _cfg_key(cfg)
        if key in done:
            print(f"[sweep] ({i}/{len(plan)}) skip (done): {cfg}")
            continue
        print(f"[sweep] ({i}/{len(plan)}) running: {cfg}", flush=True)
        try:
            row = run_one(cfg, data_root, args.codex_path, args.limit_replay, args.limit_holdout)
        except Exception as e:  # never let one config kill the sweep
            row = {"cfg": cfg, "cfg_key": key, "error": f"{type(e).__name__}: {e}"}
        _append(args.out, row)
        print(f"[sweep]   -> {json.dumps({k: v for k, v in row.items() if k not in ('cfg','cfg_key')})}", flush=True)
    print(f"[sweep] done. rows in {args.out}: {len(_load_done(args.out))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

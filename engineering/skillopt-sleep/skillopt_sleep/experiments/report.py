"""SkillOpt-Sleep — turn a sweep JSONL into a presented Markdown scorecard.

Usage:
  python -m skillopt_sleep.experiments.report --in docs/sleep/sweep.jsonl \
      --out docs/sleep/benchmark_report.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List


def _load(path: str) -> List[Dict[str, Any]]:
    rows = []
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        rows.append(json.loads(line))
                    except Exception:
                        pass
    return rows


def _fmt_model(backend: str, model: str) -> str:
    m = model or "default"
    return f"{backend}:{m}"


def render(rows: List[Dict[str, Any]]) -> str:
    direct = [r for r in rows if r.get("cfg", {}).get("kind") in ("direct", "dual") and "error" not in r]
    transfer = [r for r in rows if r.get("cfg", {}).get("kind") == "transfer" and "error" not in r]
    errors = [r for r in rows if "error" in r]

    out: List[str] = []
    out.append("# SkillOpt-Sleep — benchmark report")
    out.append("")
    out.append("Auto-generated from `sweep.jsonl`. Benchmark: "
               "[gbrain-evals](https://github.com/garrytan/gbrain-evals) `skillopt-v1` "
               "(deficient skills, train/held-out split, local rule judge — no judge-API).")
    out.append("Held-out scores are computed by the harness, not the optimizer.")
    out.append("")

    # ── direct improvement table ──────────────────────────────────────────
    out.append("## Direct improvement (optimize, then deploy)")
    out.append("")
    out.append("| Optimizer → Target | Seed | Held-out before | Held-out after | Nights | Tokens |")
    out.append("|---|---|---|---|---|---|")
    for r in direct:
        c = r["cfg"]
        if c.get("kind") == "dual":
            label = (f"{_fmt_model(c['optimizer_backend'], c.get('optimizer_model',''))}"
                     f" → {_fmt_model(c['target_backend'], c.get('target_model',''))}")
        else:
            m = _fmt_model(c["backend"], c.get("model", ""))
            label = f"{m} → {m}"
        out.append(f"| {label} | {c['seed']} | "
                   f"{r['baseline']:.2f} | **{r['after']:.2f}** | {c['nights']} | "
                   f"{r.get('tokens','?')} |")
    if direct:
        n_imp = sum(1 for r in direct if r.get("improved"))
        out.append("")
        out.append(f"**{n_imp}/{len(direct)} configurations improved on held-out.**")
    out.append("")

    # ── transfer table ────────────────────────────────────────────────────
    if transfer:
        out.append("## Cross-model transfer (optimize on SOURCE, deploy frozen on TARGET)")
        out.append("")
        out.append("The price-difference story: spend cheap tokens optimizing overnight, "
                   "then deploy the frozen skill on any model with no further optimization.")
        out.append("")
        out.append("| Source (optimizer) | Target (deploy) | Seed | Target baseline | Transferred | Gain |")
        out.append("|---|---|---|---|---|---|")
        for r in transfer:
            c = r["cfg"]
            s = _fmt_model(c["source_backend"], c.get("source_model", ""))
            t = _fmt_model(c["target_backend"], c.get("target_model", ""))
            out.append(f"| {s} | {t} | {c['seed']} | {r['baseline_target']:.2f} | "
                       f"**{r['transferred']:.2f}** | {r['transfer_gain']:+.2f} |")
        n_pos = sum(1 for r in transfer if r.get("transfer_gain", 0) > 0)
        out.append("")
        out.append(f"**{n_pos}/{len(transfer)} transfers were positive** "
                   "(frozen skill helped a different model than it was optimized on).")
        out.append("")

    # ── errors (honest reporting) ─────────────────────────────────────────
    if errors:
        out.append("## Configs that errored (reported, not hidden)")
        out.append("")
        for r in errors:
            out.append(f"- `{json.dumps(r['cfg'])}` → {r['error']}")
        out.append("")

    out.append("## How to reproduce")
    out.append("")
    out.append("```bash")
    out.append("git clone https://github.com/garrytan/gbrain-evals /tmp/gbrain-evals")
    out.append("python -m skillopt_sleep.experiments.sweep --plan full \\")
    out.append("    --data-root /tmp/gbrain-evals/eval/data/skillopt-v1 --out docs/sleep/sweep.jsonl")
    out.append("python -m skillopt_sleep.experiments.report \\")
    out.append("    --in docs/sleep/sweep.jsonl --out docs/sleep/benchmark_report.md")
    out.append("```")
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render SkillOpt-Sleep sweep report")
    ap.add_argument("--in", dest="inp", default="docs/sleep/sweep.jsonl")
    ap.add_argument("--out", default="docs/sleep/benchmark_report.md")
    args = ap.parse_args(argv)

    rows = _load(args.inp)
    if not rows:
        print(f"no rows in {args.inp}", file=sys.stderr)
        return 1
    md = render(rows)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        f.write(md)
    print(f"wrote {args.out} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

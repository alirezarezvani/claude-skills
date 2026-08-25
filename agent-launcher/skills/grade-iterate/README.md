# grade-iterate (Phase 3 — the bounded loop)

CMA's outcome primitive self-grades the agent's work against a required rubric;
this skill builds the outcome, reads each verdict, and scaffolds held-back eval.
Loops are **always bounded** by `max_iterations` (1..20).

## Usage

```bash
python3 scripts/outcome_builder.py --sheet ./my-agent/build-sheet.json \
  --max-iterations 5 --out ./my-agent/payloads/outcome.json
python3 scripts/verdict_reader.py --result ./my-agent/last-verdict.json
python3 scripts/eval_scaffold.py --sheet ./my-agent/build-sheet.json --out ./my-agent/eval.json
```

## Tools

| Tool | Purpose |
|---|---|
| `outcome_builder.py` | `user.define_outcome` payload (rubric required, cap clamped 1..20) |
| `verdict_reader.py` | grader result → next move (SHIP / SHARPEN / ESCALATE / RESUME) |
| `eval_scaffold.py` | held-back cases + parallel run plan (≤25 threads) |

Loop discipline: [`../../references/loops-and-workflows.md`](../../references/loops-and-workflows.md).

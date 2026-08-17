---
description: Phase 3 — the bounded grade→iterate loop. Define a CMA outcome (required rubric, max_iterations 1..20), read each grader verdict, decide the next move, and run held-back eval cases once a version passes, via the grade-iterate skill. Never unbounded.
argument-hint: "[optional: path to build-sheet.json]"
---

# /cs:grade — Phase 3: Grade → Iterate

Run the `grade-iterate` skill.

**$ARGUMENTS**

## Steps

1. `python3 agent-launcher/skills/grade-iterate/scripts/outcome_builder.py --sheet ./my-agent/build-sheet.json --max-iterations 5 --out ./my-agent/payloads/outcome.json`
   — rubric required; send as a `user.define_outcome` event.
2. On each verdict: `python3 agent-launcher/skills/grade-iterate/scripts/verdict_reader.py --result ./my-agent/last-verdict.json`
   → SHIP / SHARPEN / ESCALATE / RESUME. Each iteration must move ≥1 rubric line
   fail→pass.
3. Once a version passes: `python3 agent-launcher/skills/grade-iterate/scripts/eval_scaffold.py --sheet ./my-agent/build-sheet.json --out ./my-agent/eval.json`
   — held-back cases in parallel (≤25 threads).
4. Decide: ship v0, or `goal_state.py set --phase run-without-you`.

Bounded loops only. Read the verdict before acting. Held-back cases stay held back.

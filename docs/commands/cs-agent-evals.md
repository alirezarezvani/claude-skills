---
title: "/cs-agent-evals — Slash Command for AI Coding Agents"
description: "Full regression-eval pass on an agent change - trajectories, flaky cases, and the paired baseline-vs-candidate gate.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-agent-evals

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/agent-regression-evals/commands/cs-agent-evals.md">Source</a></span>
</div>


Decide whether the change in `$ARGUMENTS` made the agent worse.

## Before running anything

Confirm, or ask for, these three things. If any is missing, say so and stop:

1. Baseline and candidate results as JSONL, one row per trial:
   `{"case_id", "trial", "passed", "critical"?, "cost_usd"?, "trajectory"?}`
2. At least 3 trials per case on both sides, each from a clean environment.
3. The same case IDs on both sides.

No results yet? Show the format with `python ${CLAUDE_PLUGIN_ROOT}/skills/agent-regression-evals/scripts/regression_gate.py --sample`
and help the user write the runner that produces it.

## Run

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/agent-regression-evals/scripts/trajectory_checker.py --spec <cases.json> --results <candidate.jsonl>   # only if a spec exists
python ${CLAUDE_PLUGIN_ROOT}/skills/agent-regression-evals/scripts/flake_detector.py --results <candidate.jsonl> --k 3
python ${CLAUDE_PLUGIN_ROOT}/skills/agent-regression-evals/scripts/regression_gate.py --baseline <baseline.jsonl> --candidate <candidate.jsonl>
```

## Report

1. **Verdict** — PASS (0) / WARN (2) / **BLOCK (4)** from the gate.
2. **The number** — mean per-case delta with its 95% CI, and McNemar flips.
3. **Why** — every BLOCK and WARN line, verbatim.
4. **Flaky cases** — critical ones as defects to fix; others as quarantine candidates needing owner and expiry.
5. **Forbidden tool calls** from the trajectory check, if any.
6. **One next action.**

## Do not

- Do not compare runs with fewer than 3 trials per case.
- Do not drop or edit a failing case to make the gate pass.
- Do not soften a BLOCK into a suggestion.

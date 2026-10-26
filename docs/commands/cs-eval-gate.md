---
title: "/cs-eval-gate — Slash Command for AI Coding Agents"
description: "Just the merge gate - paired statistical comparison of a candidate eval run against baseline, with a PASS / WARN / BLOCK exit code.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-eval-gate

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/agent-regression-evals/commands/cs-eval-gate.md">Source</a></span>
</div>


Answer one question about `$ARGUMENTS`: **is the candidate measurably worse than the baseline?**

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/agent-regression-evals/scripts/regression_gate.py \
  --baseline <baseline.jsonl> --candidate <candidate.jsonl> [--quarantine <quarantine.json>]
```

## What blocks (exit 4)

- Upper end of the 95% CI on the mean per-case delta below zero, or one-sided McNemar p < 0.05.
- A critical case that passed every baseline trial and failed any candidate trial.
- A baseline case missing from the candidate run.
- A quarantine entry without owner or expiry, or one covering a critical case.

## What warns (exit 2)

- A drop larger than `--tolerance` (default 0.02) that the sample cannot confirm. Report the number of cases
  the gate says would be needed to detect it.
- Mean cost per case up more than `--max-cost-increase` (default 20%).

## Report

Verdict first, then the delta and CI, then every BLOCK and WARN line verbatim, then the largest per-case drops.
On WARN, state the decision the human must make; do not make it for them.

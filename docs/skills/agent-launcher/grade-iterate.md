---
title: "Phase 3 — Grade → Iterate (the bounded loop) — Agent Skill for Claude Managed Agents"
description: "Phase 3 of building a Claude Managed Agent — the bounded grade→iterate loop. Define a CMA outcome (a required markdown rubric graded by an isolated. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Phase 3 — Grade → Iterate (the bounded loop)

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch-outline: Agent Launcher</span>
<span class="meta-badge">:material-identifier: `grade-iterate`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/skills/grade-iterate/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install agent-launcher-skills</code>
</div>


This is the plugin's **loop**: CMA's `outcome` primitive self-grades the agent's
work in an isolated context and feeds failing verdicts back for the next attempt.
It is **always bounded** by `max_iterations` (1..20) — never "improve forever".

See [[`references/loops-and-workflows.md`](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/loops-and-workflows.md)](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/loops-and-workflows.md)
and the outcome section of
[[`references/cma-primitives.md`](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/cma-primitives.md)](https://github.com/alirezarezvani/claude-skills/tree/main/agent-launcher/references/cma-primitives.md).

## Workflow

1. **Define the outcome.**
   ```bash
   python3 scripts/outcome_builder.py \
     --sheet ./my-agent/build-sheet.json --max-iterations 5 \
     --out ./my-agent/payloads/outcome.json
   ```
   The **rubric is required**; `max_iterations` is clamped to 1..20. Send the
   payload as a `user.define_outcome` event (append to the running session).
2. **Read every verdict first.**
   ```bash
   python3 scripts/verdict_reader.py --result ./my-agent/last-verdict.json
   ```
   Tables the rubric outcome and recommends: **SHIP** (`satisfied`), **SHARPEN**
   then re-run (`needs_revision`), **ESCALATE** (`max_iterations_reached` /
   `failed`), **RESUME** (`interrupted`). With ≤1 iteration left it flips to
   "make the single highest-value fix or escalate now".
3. **Loop invariant.** Each iteration must move ≥1 rubric line fail→pass, or the
   run halts at the cap and escalates. Don't burn the budget on cosmetic edits.
4. **Once a version passes, run held-back eval.**
   ```bash
   python3 scripts/eval_scaffold.py \
     --sheet ./my-agent/build-sheet.json --out ./my-agent/eval.json --concurrency 5
   ```
   Held-back cases (never seen during iteration) run in parallel, capped at the
   25-thread CMA ceiling, each graded against the same rubric.
5. **Decide.** SHIP as v0, or promote to a scheduled deployment (Phase 4). Record
   the verdict on the goal: `goal_state.py set --phase run-without-you`.

## Hard rules

- **Bounded, always.** No outcome without a `max_iterations` cap.
- **Read the verdict before acting.** The grader's explanation drives the next move.
- **Held-back cases are held back.** Never grade generalization on cases the agent
  already iterated against.

## Forcing-question library (recommend + cite)

1. "What are the 3–5 rubric lines?" *Recommend:* grounded, checkable criteria.
   *Cite:* cma-primitives.md (rubric required).
2. "How many iterations before you'd rather look yourself?" *Recommend:* 3–5.
   *Cite:* loops-and-workflows.md (bounded loop).
3. "On a fail, sharpen the prompt or the tools?" *Recommend:* whichever rubric line
   failed points to. *Cite:* verdict_reader next-move table.
4. "Which cases did the agent NOT see?" *Recommend:* hold back ≥3 for generalization.
   *Cite:* this SKILL (held-back eval).

## Tools

- `scripts/outcome_builder.py` — user.define_outcome payload (rubric required, cap 1..20).
- `scripts/verdict_reader.py` — grader result → next move.
- `scripts/eval_scaffold.py` — held-back cases + parallel run plan (≤25 threads).

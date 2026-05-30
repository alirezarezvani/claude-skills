---
title: "/cs-workflow-build — Slash Command for AI Coding Agents"
description: "/cs:workflow-build <task-description> — Design and write a deterministic Claude Code workflow (.js). Opens with intake questions, infers-and-proposes. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-workflow-build

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/workflow-builder/commands/cs-workflow-build.md">Source</a></span>
</div>


**Command:** `/cs:workflow-build <task-description>`

Designs a deterministic multi-agent workflow for Claude Code's Workflow tool. Always opens with intake; never writes a file before the topology is confirmed.

## When to Run

- Building a new `.claude/workflows/*.js` file
- Automating a repeatable, multi-step task across fresh-context sub-agents
- Deciding whether a task even warrants a workflow (vs. a single agent or a skill)

## Step 1 — Intake (always first)

Ask the opening question set. Lead with #1.

1. What repeatable, multi-step task do you want to automate?
2. What is the one unit of work a single sub-agent does once?
3. How many units — a known list, or discovered by looping?
4. Do later steps need *all* prior results at once, or can each item flow on its own?
5. Does any step need structured data back (a verdict, a list, scores)?
6. Roughly how deep / how many tokens?

## Step 2 — If the user is vague, infer and propose (don't loop on questions)

```bash
python ../skills/workflow-builder/scripts/workflow_intake.py --task "<their request>" \
  --units unknown --stages unknown --needs-all unknown --structured unknown
```

Present the result as "here's what I'd build and why": recommended topology (+ runner-up), per-stage model picks, a budget guard, and the rationale for each choice. Then ask only "what should I change?"

## Step 3 — Confirm the shape, then scaffold

```bash
python ../skills/workflow-builder/scripts/scaffold_workflow.py \
  --topology <fan-out|pipeline|barrier|loop|judge-panel> --name <name> --description "..." \
  > .claude/workflows/<name>.js
```

## Step 4 — Validate before running

```bash
python ../skills/workflow-builder/scripts/validate_workflow.py .claude/workflows/<name>.js
```

Fix every FAIL. WARNs need a one-line justification.

## Step 5 — Run

```bash
export CLAUDE_CODE_WORKFLOWS=1   # the feature is off by default
# Save under .claude/workflows/, then launch + monitor via /workflows.
# P = pause/resume, X = skip a sub-agent. Failed agents retry automatically.
```

## The Hard Rules (validator enforces)

1. `meta` is a pure literal and the first statement — no variables, spreads, template strings, or calls.
2. No `Date.now()`, `Math.random()`, or argless `new Date()` — they break resume.
3. No filesystem / Node APIs in the orchestrator — that work goes inside `agent()`.
4. `parallel()` takes thunks (`() => agent(...)`); default to `pipeline()` unless a stage needs the whole prior set.
5. Guard every open-ended loop with a counter or `budget.remaining()`.
6. `results.filter(Boolean)` before using parallel/pipeline output.

## Output Format

```markdown
# Workflow Build: <name>
## The Decision
[intake | recommend | scaffold | validate | run]
## Recommended Topology
[fan-out | pipeline | barrier | loop | judge-panel] — why
## Model Plan
[per-stage model + reason]
## Validator Verdict
🟢 PASS | 🟡 WARN (justified) | 🔴 FAIL (with line numbers)
## Next Steps
[3 concrete actions]
```

## Related

- Agent: [`cs-workflow-architect`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/workflow-builder/agents/cs-workflow-architect.md)
- Skill: [`workflow-builder`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/workflow-builder/skills/workflow-builder/SKILL.md)
- Adjacent: `/cs:write-a-skill` (authoring skills, not workflows)

---

**Version:** 1.0.0

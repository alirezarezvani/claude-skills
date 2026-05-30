# workflow-builder

Design and write deterministic multi-agent **workflow** scripts for Claude Code's Workflow tool — `.js` files in `.claude/workflows/` that fan work out to fresh-context sub-agents under plain JavaScript control flow. Only leaf `agent()` calls spend tokens, so the main session stays clean and the run is resumable.

Targets the Workflow tool introduced in Claude Code v2.1.147 (gated behind `CLAUDE_CODE_WORKFLOWS=1`, browsable via `/workflows`).

## The intake-first rule

Every workflow-creation session opens with an intake question set (what task, what unit of work, known list vs. loop, barrier vs. pipeline, structured output, depth). **When the user is vague, the skill does not stall or interrogate in a loop** — it runs a deterministic recommendation engine that infers a topology and presents it *with the reasoning* ("here's what I'd build and why"), then confirms before writing any file.

## What's in the box

| Component | Where | What it does |
|---|---|---|
| **Intake recommendation engine** | `skills/workflow-builder/scripts/workflow_intake.py` | Classifies a (vague) task → recommended topology + runner-up + per-stage model plan + budget guard + a one-line rationale per choice. |
| **Workflow validator** | `skills/workflow-builder/scripts/validate_workflow.py` | Stdlib linter for `.js` workflows: pure-literal `meta`, no `Date.now()`/`Math.random()`/argless `new Date()`, no FS/Node APIs in the orchestrator, `parallel()` thunks, guarded loops, `filter(Boolean)`, size cap. PASS / WARN / FAIL with line numbers. |
| **Scaffolder** | `skills/workflow-builder/scripts/scaffold_workflow.py` | Emits a runnable starter for any of 5 topologies (fan-out, pipeline, barrier, loop, judge-panel). |
| **3 references** | `skills/workflow-builder/references/` | API reference · orchestration patterns · decision + intake guide (7-8 sources each). |
| **Templates + example** | `skills/workflow-builder/assets/` | Fan-out / pipeline / loop starters + a complete PR-triage workflow. |
| **Persona agent** | `agents/cs-workflow-architect.md` | Design-first interrogator that refuses to write before the topology is confirmed. |
| **Slash command** | `commands/cs-workflow-build.md` | `/cs:workflow-build <task>` — runs the full intake → scaffold → validate flow. |

## Quick start

```bash
cd skills/workflow-builder

# 1. Turn a vague request into a concrete proposal
python scripts/workflow_intake.py --task "review my open PRs for bugs"

# 2. Scaffold the confirmed topology
python scripts/scaffold_workflow.py --topology pipeline --name pr-triage \
  --description "Triage open PRs" > /tmp/pr-triage.js

# 3. Validate before running
python scripts/validate_workflow.py /tmp/pr-triage.js
```

All three tools run with `--sample` (no args) and `--help`.

## Running the workflows it writes

```bash
export CLAUDE_CODE_WORKFLOWS=1          # the feature is off by default
# save the .js under .claude/workflows/ , then launch + watch via /workflows
# P = pause/resume , X = skip a sub-agent ; failed agents retry automatically
```

## Attribution

Conceptually inspired by [Ray Amjad's claude-code-workflow-creator](https://github.com/ray-amjad/claude-code-workflow-creator). All content here was written for this repo against Claude Code's publicly-documented Workflow tool API; no text was copied verbatim.

## License

MIT.

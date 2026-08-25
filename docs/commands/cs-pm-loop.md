---
title: "/cs-pm-loop — Slash Command for AI Coding Agents"
description: "Drive a project-delivery goal through a bounded agentic loop — Jira MCP snapshot → flow/sprint analytics bridge → routed sub-skill execution →. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-pm-loop

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/project-management/commands/cs-pm-loop.md">Source</a></span>
</div>


Goal:

**$ARGUMENTS**

## Sequence (gates are blocking — never skip forward)

1. **Intake gate** — the goal must name an observable outcome and its proof. If vague,
   run the `/cs:grill-pm` branches first (one question per turn). Do not loop on fuzz.
2. **Observe** — pull fresh data: `mcp__atlassian__getAccessibleAtlassianResources` (get
   cloudId) → `mcp__atlassian__searchJiraIssuesUsingJql` → save `snapshot.json`, then:
   ```bash
   python3 project-management/skills/pm-skills/scripts/jira_snapshot_bridge.py --input snapshot.json --to flow
   python3 project-management/skills/pm-skills/scripts/jira_snapshot_bridge.py --input snapshot.json --to sprint > sprint_data.json
   ```
3. **Plan** — write the task plan (owners, executors, reviewers, machine-checkable
   acceptance per task; shape via `delivery_loop_gate.py --sample`), then gate it:
   ```bash
   python3 project-management/skills/pm-skills/scripts/delivery_loop_gate.py --plan plan.json --mode plan
   ```
   Exit 2 → fix the listed G1–G4 violations before executing. For multi-task goals,
   compile through the repo harness instead (`goal_compiler.py` with the
   `project-management.json` manifest) and drive it with `loop_controller.py`.
4. **Execute** — one task at a time: route with `pm_goal_router.py`, run the routed
   sub-skill's own tools, record real exit codes and evidence. Retry means a changed
   approach; max 3 attempts per task.
5. **Verify** — the task's acceptance command must exit 0; sub-skill gates apply
   (scrum-master's ≥3-sprints rule, atlassian-admin's VERIFY steps). Never adjudicate
   your own verification; never edit a gate to make it pass.
6. **Close** —
   ```bash
   python3 project-management/skills/pm-skills/scripts/delivery_loop_gate.py --plan plan.json --mode close
   ```
   Exit 4 → close refused: finish, escalate, or get a human waiver (with reason). Exit 0
   → report the handoff: tasks, statuses, evidence, waivers, and the flow-metrics
   before/after.

## Rules

- Terminal states: success · clean no-op · blocked · approval-required · exhausted ·
  stagnated. Exhausted budgets escalate to the named human — never reported as success.
- Jira writes are auditable: no `transitionJiraIssue` to Done without verify evidence;
  admin/destructive actions are approval-required, full stop.
- Max 12 loop iterations per goal; 3 attempts per task.

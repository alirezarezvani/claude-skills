---
title: "/cs-bizops — Slash Command for AI Coding Agents"
description: "Top-level Business Operations router. Routes the inquiry to one of six BizOps sub-skills (process, vendor, capacity, comms, knowledge, procurement). Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-bizops

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/business-operations/commands/cs-bizops.md">Source</a></span>
</div>


Use the `cs-bizops-orchestrator` agent + `business-operations-skills` orchestrator skill to handle this inquiry:

**$ARGUMENTS**

## Routing protocol

1. Classify the inquiry against the six BizOps lanes:
   - **PROCESS** — bottleneck, cycle time, handoff, workflow → `process-mapper`
   - **VENDOR** — SLA, third-party risk, SaaS audit → `vendor-management`
   - **CAPACITY** — headcount, utilization, hiring sequence → `capacity-planner`
   - **COMMS** — all-hands, change announcement, internal newsletter → `internal-comms`
   - **KNOWLEDGE** — SOP, runbook, onboarding doc → `knowledge-ops`
   - **PROCUREMENT** — spend audit, supplier rationalization → `procurement-optimizer`

2. If top lane signal score ≥ 2 keyword hits → invoke that sub-skill in forked context.

3. If single-signal or tie → ask **one** clarifying question naming the top two candidate lanes.

4. After sub-skill runs, return ≤ 200-word digest to the parent context.

## Output expectations

- What was analyzed
- Top 3 findings with severity (CRITICAL/HIGH/MEDIUM)
- Top 3 next actions with named owners
- Path to artifact(s) saved to the user's working directory
- Suggested chain (which sub-skill to invoke next, if any)

## Anti-patterns

- ❌ Running multiple sub-skills to be thorough — pick one, digest, chain on request
- ❌ Auto-approving an ops change — surface findings, the human decides

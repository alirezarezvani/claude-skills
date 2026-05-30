---
title: "/cs-fullstack-review — Slash Command for AI Coding Agents"
description: "Fullstack engineering review — walks the 7 Matt Pocock forcing questions, picks the profile, forks into POWERFUL specialists (api-design-reviewer. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-fullstack-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/cs-fullstack-review.md">Source</a></span>
</div>


Use the `cs-fullstack-engineer` agent (which uses `context: fork` to keep the parent thread clean) to handle this inquiry:

**$ARGUMENTS**

## Forcing-question library

Canonical source: `engineering-team/skills/senior-fullstack/references/forcing_questions.md` (7 questions, one-per-turn, recommendation + canon citation per question).

1. Team size now + 12-month headcount
2. Deployment cadence (per-PR / daily / weekly / quarterly)
3. Customer-facing / internal tool / marketing site
4. One-year p50 + p99 traffic forecast
5. Hiring-against vs training-into the stack
6. Year-one monthly cloud + SaaS budget ceiling
7. Three verifiable success criteria with numeric targets

## Routing protocol

1. **Walk the 7 forcing questions** in `engineering-team/skills/senior-fullstack/references/forcing_questions.md`. One per turn. Recommend the answer with cited canon. Track in `/tmp/fullstack-grill-<date>.md`.
2. **Surface kill criteria** — if any question trips one (e.g., "microservices day 1, team size 3"), STOP and resolve before proceeding.
3. **Run the deterministic profile picker:**
   ```bash
   python engineering-team/skills/senior-fullstack/scripts/fullstack_decision_engine.py \
     --team-size <N> --team-size-12mo <N12> --cadence <c> \
     --user-facing <true|false> --budget <USD/mo> \
     --traffic-p99-rps <N> --data-sensitivity <tier>
   ```
4. **Surface the matched profile + runner-up tradeoff** (if within 15%).
5. **Fork into specialists** (one at a time, depth-first):
   - `api-design-reviewer` for API contract
   - `database-designer` for schema
   - `slo-architect` for reliability target
   - `ci-cd-pipeline-builder` for the pipeline
   - `performance-profiler` for perf baseline
   - `cs-karpathy-reviewer` before any commit

## Output expectations (≤ 200-word digest)

- Matched profile + reason
- Three verifiable success criteria with numeric targets
- Named approver chain
- List of specialists invoked + artifact paths
- Recommended next sub-skill (if any)

## Anti-patterns

- ❌ Bundling forcing questions — one per turn.
- ❌ Skipping the kill-criteria check.
- ❌ Reimplementing specialist scope. Fork — don't duplicate.
- ❌ Auto-approving production changes. Always name the human approver.

## Customization

Profiles live at `engineering-team/skills/senior-fullstack/profiles/`. To customize for your org:

1. Copy `saas-startup.json` (or whichever best fits) to `<your-org>.json`.
2. Edit `constraints`, `stack_recommendations`, `success_thresholds`, `named_approver_chain`.
3. The decision engine auto-discovers new profile JSONs.

## Related commands

- `/cs:frontend-review` — frontend-only deep dive
- `/cs:backend-review` — backend-only deep dive
- `/cs:engineer-grill` — cross-role 21-question forcing-question runner
- `/karpathy-check` — Karpathy 4-principle review before commit

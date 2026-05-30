---
title: "/cs:cto-review — CTO Forcing Questions — Agent Skill for Executives"
description: "/cs:cto-review <plan> — Architecture and scaling interrogation. Tech debt, scaling cliffs, team scaling, build-vs-buy. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:cto-review — CTO Forcing Questions

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-Level Advisory</span>
<span class="meta-badge">:material-identifier: `cto-review`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/skills/cto-review/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Command:** `/cs:cto-review <plan>`

Pressure-tests architecture and engineering scaling decisions. Six questions to surface the next scaling cliff before you hit it.

## When to Run

- Before approving a major architecture change
- Before doubling the engineering team
- Before a build-vs-buy decision > $100K/year
- When a system is showing reliability stress (SLOs missed)
- Before committing to a new platform / language / DB

## The Six CTO Questions

### 1. Scaling Cliff
**Where does the current architecture break, in terms of users / requests / data volume?**
- Be specific. "It breaks at 10× current load because the primary DB writes saturate."
- If you don't know, run a load test before deciding.

### 2. Tech Debt Inventory
**What's the top tech debt item, what's it costing per week, and when does it become blocking?**
```bash
python ../../../skills/cto-advisor/scripts/tech_debt_analyzer.py
```

### 3. Team Scaling
**For each open req, what's the ramp time and contribution model?**
```bash
python ../../../skills/cto-advisor/scripts/team_scaling_calculator.py
```

### 4. Build vs Buy
**Why are we building this instead of buying it — and what's the 3-year TCO of each?**
- If "we want control" or "it's not that hard" — push back.
- If the answer is "this is our core moat," build.

### 5. SLO / Reliability
**What are the SLOs for this system and what's the current error budget burn?**
- Without an SLO, you can't reason about reliability tradeoffs.
- See `engineering/slo-architect` for SLO design.

### 6. Security & Compliance Surface
**What does this expose, and has cs-ciso-advisor signed off?**
- Architecture decisions are compliance decisions.
- Loop in cs-ciso-advisor before commit.

## Workflow

1. Run the tech debt analyzer + team scaling calculator
2. Define the scaling-cliff hypothesis explicitly
3. Cross-check with cs-ciso-advisor for security implications
4. Apply the verdict

## Output Format

```markdown
# CTO Review: <plan>
**Date:** YYYY-MM-DD

## Scaling Cliff
- Current capacity: <metric>
- Break point: <metric>
- Headroom: X months at current growth

## Tech Debt
- Top item: <description>
- Cost per week: $X or N eng-hours
- Blocking date estimate: <date>

## Team
- Open reqs: N
- Median ramp: X months
- Contribution model: <pairing / squad / area>

## Build vs Buy
- 3-year build TCO: $X
- 3-year buy TCO: $X
- Strategic fit: <core / context>
- Decision: BUILD | BUY

## Reliability
- SLO defined: yes / no
- Error budget burn: X% (target < Y%)

## Security
- cs-ciso sign-off: ✅ / ❌

## Verdict
🟢 SHIP | 🟡 SHARPEN | 🔴 BLOCK

## Next Steps
[3 concrete actions]
```

## Routing

- `/cs:ciso-review` — mandatory if data surface changes
- `/cs:cfo-review` — for build-vs-buy > $100K
- `/cs:execute` — quarterly plan
- `/cs:boardroom` — for architecture pivots

## Related

- Agent: [`cs-cto-advisor`](https://github.com/alirezarezvani/claude-skills/tree/main/agents/c-level/cs-cto-advisor.md)
- Skill: [`cto-advisor`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/skills/cto-advisor/SKILL.md)
- SLO: [`engineering/slo-architect`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/slo-architect)

---

**Version:** 1.0.0

---
title: "/cs:post-mortem — Honest Retrospective — Agent Skill for Executives"
description: "/cs:post-mortem <decision> — Honest retrospective on an executed decision, scored against original assumptions and dissent. Closes the strategic. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# /cs:post-mortem — Honest Retrospective

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-Level Advisory</span>
<span class="meta-badge">:material-identifier: `post-mortem`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/skills/post-mortem/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install c-level-skills</code>
</div>


**Command:** `/cs:post-mortem <decision-path>`

Closes the strategic sprint loop. Scores a decision against the success and kill criteria written **before** the decision (not retro-fitted) and revisits the preserved dissent. This is the rigor that compounds over time.

## Pipeline Position

```
/cs:office-hours  →  /cs:brief  →  /cs:boardroom  →  /cs:decide  →  /cs:execute  →  /cs:post-mortem
                                                                                       ↑ you are here
```

## When to Run

- At the 90-day checkpoint (auto-scheduled by `/cs:decide`)
- When a kill criterion triggers
- After a major decision is reversed
- Quarterly on all decisions of the past quarter

## Inputs

- The decision record (output of `/cs:decide`)
- The execution plan (output of `/cs:execute`)
- Actual outcomes (metrics, events, customer signals)

## Output: Post-Mortem Record

Saved to `~/.claude/postmortems/YYYY-MM-DD-<slug>.md`:

```markdown
# Post-Mortem: <decision title>
**Decision date:** YYYY-MM-DD
**Post-mortem date:** YYYY-MM-DD
**Status:** WIN / PARTIAL / LOSS / MIXED

## Outcome Scoring (against pre-committed criteria)

| Success Criterion | Threshold | Actual | Met? |
|---|---|---|---|
| <metric 1> | <threshold> | <actual> | ✅ / ❌ |
| <metric 2> | <threshold> | <actual> | ✅ / ❌ |

| Kill Criterion | Threshold | Actual | Triggered? |
|---|---|---|---|
| <metric> | <threshold> | <actual> | ✅ / ❌ |

**Overall:** WIN / PARTIAL / LOSS / MIXED

## What We Got Right
- <factor 1>
- <factor 2>

## What We Got Wrong
- <factor 1>
- <factor 2>

## Preserved Dissent — Revisited
[Original dissent from the boardroom memo, scored:]

- **<dissenter>:** <original concern>
  - **Did it materialize?** YES / NO / PARTIAL
  - **Cost if YES:** <quantified impact>
  - **Lesson:** <one sentence>

## Assumption Audit
[Original brief's assumptions, scored:]

- **Assumption 1:** <text>
  - **Held?** YES / NO / PARTIAL
  - **Why:** <explanation>

## Process Lessons
- **Phase 2 isolation worked?** YES / NO
- **Devil's advocate concerns played out?** YES / NO / PARTIAL
- **Cadence was right?** YES / TOO LOOSE / TOO TIGHT

## Forward Actions
- [ ] <change to operating system or routing logic>
- [ ] <new decision to make based on this learning>
- [ ] <update company-context.md>

## Status
- WIN → archive, log lesson
- LOSS → schedule follow-up boardroom: `/cs:brief` for the next call
```

## Why Pre-Committed Criteria Matter

The biggest temptation in post-mortems is retroactive justification: "we always knew X, that's why we did Y." Pre-committed criteria, signed at `/cs:decide` time, eliminate that move. The numbers either matched or they didn't.

## Why Revisit Dissent

The dissent column from `/cs:boardroom` is the single most useful piece of organizational memory. Most of the time, the dissenter was directionally right. Revisiting and scoring it builds calibration over years.

## Routing

- `/cs:brief` — if the post-mortem surfaces a new decision
- `/cs:freeze` — if the post-mortem reveals a process gap that needs cooldown enforcement
- Updates to company-context.md via `cs-onboard`

## Related

- Skill: [`decision-logger`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/skills/decision-logger/SKILL.md)
- Agent: [`cs-chief-of-staff`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/agents/cs-chief-of-staff.md)
- Sibling: [`/em:postmortem`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/executive-mentor/skills/postmortem/SKILL.md) — adversarial single-decision post-mortem

---

**Version:** 1.0.0

---
name: "execute"
description: "/c-level-agents:execute [decision] — Generate a 90-day execution plan with weekly milestones, DRIs, and check-in cadence from an approved decision. Use when a logged decision needs to become an operating plan — e.g. turning an approved market-entry call into weekly milestones with DRIs."
---

# /c-level-agents:execute — 90-Day Execution Plan

**Command:** `/c-level-agents:execute <decision-path>`

Turns an approved decision into a 90-day plan with weekly milestones, named DRIs, and a check-in cadence. Where most decisions die: between "we decided" and "what's next Monday?"

## Pipeline Position

```
/c-level-agents:office-hours  →  /c-level-agents:brief  →  /c-level-agents:boardroom  →  /c-level-agents:decide  →  /c-level-agents:execute  →  /c-level-agents:post-mortem
                                                                       ↑ you are here
```

## Input

An approved decision record (output of `/c-level-agents:decide`).

## Output Plan Format

Saved to `~/.claude/execution/YYYY-MM-DD-<slug>.md`:

```markdown
# Execution Plan: <decision title>
**Decision:** <link to /c-level-agents:decide record>
**Owner (Sponsor):** <founder or exec>
**Start:** YYYY-MM-DD
**Checkpoint:** YYYY-MM-DD (90d)

## Outcome (binding)
[Copied from decision: success + kill criteria]

## Workstreams
| Workstream | DRI | Success Metric | Status |
|---|---|---|---|
| <e.g., Pricing rollout> | <name> | <metric, threshold> | Not started |
| <e.g., Comms> | <name> | <metric> | Not started |
| <e.g., Eng changes> | <name> | <metric> | Not started |

## Weekly Milestones
| Week | Milestone | DRI | Definition of Done |
|---|---|---|---|
| 1 | <e.g., positioning locked> | <name> | <observable outcome> |
| 2 | <e.g., draft launched> | <name> | <observable> |
| 3 | ... | | |
| 12 | <e.g., checkpoint review> | <name> | <observable> |

## Cadence
- **Weekly:** Owner reviews status (15 min)
- **Bi-weekly:** Cross-functional sync (30 min)
- **Day 30 / 60 / 90:** Checkpoint with cs-chief-of-staff

## Dependencies
- Internal: <list>
- External: <vendors, regulators, customers>

## Risk Register
| Risk | Likelihood | Impact | Owner | Mitigation |
|---|---|---|---|---|
| <e.g., delayed legal review> | M | H | <name> | <plan> |

## Kill Criteria Watch
[Copied from decision; reviewed at every checkpoint]
- <metric, threshold, action>
```

## Workflow

1. Read the decision record
2. Decompose the chosen option into 3-6 workstreams
3. Name a DRI for each workstream
4. Reverse-engineer 12 weekly milestones from the checkpoint date
5. Set the cadence (weekly + bi-weekly + 30/60/90 checkpoints)
6. Build the risk register (cross-reference original Phase 4 devil's-advocate concerns)
7. Save and notify DRIs

## Why 90 Days

- Long enough to show real signal (not just activity)
- Short enough to course-correct before damage compounds
- Matches quarterly OKR cycle, fundraise sprints, and most board cadences

## Routing

- `/c-level-agents:post-mortem <decision>` — at day 90 (or earlier if kill criteria trigger)
- `/c-level-agents:boardroom` — if a checkpoint reveals a need to re-decide

## Related

- Skills: [`coo-advisor`](${CLAUDE_PLUGIN_ROOT}/vendor/c-level-advisor/coo-advisor/SKILL.md), [`strategic-alignment`](${CLAUDE_PLUGIN_ROOT}/vendor/c-level-advisor/strategic-alignment/SKILL.md), [`change-management`](${CLAUDE_PLUGIN_ROOT}/vendor/c-level-advisor/change-management/SKILL.md)
- Agent: [`cs-coo-advisor`](../../agents/cs-coo-advisor.md)

---

**Version:** 1.0.0

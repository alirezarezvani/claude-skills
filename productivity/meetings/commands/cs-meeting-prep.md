---
name: "cs-meeting-prep"
description: "/cs:meeting-prep — Gate a meeting before it exists: price it in real dollars (attendees x minutes x rate + optional 23-minute refocus overhead), demand a decision + agenda + owner, then either recommend async or build a timeboxed, decision-first agenda where every topic has a desired outcome."
argument-hint: "[the meeting: who, how long, what decision]"
---

# /cs:meeting-prep — Cost Gate → Timeboxed Agenda (or Async)

**Command:** `/cs:meeting-prep [the meeting]`

Most meetings should be an email. This command makes that a testable claim: it prices the meeting,
runs the decision/agenda/owner gate, and only if the meeting survives does it build the timeboxed
agenda. An ASYNC verdict is a win — draft the memo instead.

## When to Run

- "Should this be a meeting?" / "Is this meeting worth it?"
- Before sending any invite with 3+ attendees
- "Build the agenda for Thursday's pricing meeting"
- You suspect a recurring meeting has outlived its decision

## When NOT to Run

- After the meeting, with notes in hand → use `/cs:meeting-actions`
- Sprint ceremonies, standups, and Jira delivery cadence → `project-management/` owns those
- Designing an org-wide comms program → `business-operations/internal-comms`

## What You Get

1. **The price** — direct cost (attendees × minutes × rate) plus, with `--include-refocus`, the
   23-minute-per-attendee refocus overhead, and a cost-per-minute line.
2. **One gate verdict** — `ASYNC` (no decision → send a memo; exit 2), `NOT-READY` (decision but
   missing agenda/owner, named; exit 3), or `MEET` (exit 0).
3. **On MEET: a timeboxed agenda** — decision topics first, per-topic desired outcome + owner +
   timebox, a pre-read line, and a mandatory 5-minute closing "actions recap" slot.
4. **On ASYNC: a memo outline** — the decision-free content restructured as a written update.

## Trigger Phrases (auto-invoke without /cs:)

- "should this be a meeting" / "does this need a meeting"
- "what does this meeting cost"
- "build a timeboxed agenda" / "prep this meeting"
- "can this be async"

## Discipline

- **Gate before agenda** — never build an agenda for a meeting that hasn't passed the gate.
- **No decision, no meeting** — status updates go async, every time.
- **No desired outcome, no agenda slot** — the builder refuses empty outcomes by name; get the outcome.
- **Decisions first** — decide/choose/approve topics sort before discuss/inform. Keep them there.
- **Timeboxes are budgets** — overflow + the 5-minute closing buffer gets refused with the exact overage.

## Workflow

```bash
# 1. Price + gate the meeting
python ../skills/meetings/scripts/meeting_cost_calculator.py \
  --attendees 6 --minutes 60 --avg-rate 90 --include-refocus \
  --has-decision --has-agenda --has-owner

# 2a. ASYNC (exit 2) → draft the memo outline instead. Stop here.
# 2b. NOT-READY (exit 3) → get the missing agenda/owner, re-run the gate.

# 3. MEET (exit 0) → build the timeboxed, decision-first agenda
python ../skills/meetings/scripts/agenda_builder.py --length 45 \
  --topic "Q3 pricing:Decide usage-based vs seat-based:15:maria" \
  --topic "Launch risks:Discuss open launch blockers:15:sam" \
  --topic "Metrics:Inform team of activation trend:5:alex"
```

## Stop Conditions

- ASYNC verdict delivered + memo outline sketched → done. Do not build an agenda anyway.
- MEET verdict + agenda printed with pre-read line and closing recap slot → done.
- NOT-READY twice in a row on the same missing input → hand the gap to the user; don't invent an owner.
- User says "just book it" → deliver the cost line once, then comply. Their calendar, their call.

## Related

- Agent: [`cs-meeting-discipline`](../agents/cs-meeting-discipline.md)
- Skill: [`meetings`](../skills/meetings/SKILL.md)
- Sibling command: [`/cs:meeting-actions`](cs-meeting-actions.md) (post-meeting extraction)

---

**Version:** 1.0.0

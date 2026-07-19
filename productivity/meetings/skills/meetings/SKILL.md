---
name: meetings
description: Use when someone wants to decide whether a meeting is worth calling, price a meeting in dollars, build a timeboxed agenda with desired outcomes, or turn messy meeting notes into owned action items — or says "should this be a meeting", "/cs:meeting-prep", or "/cs:meeting-actions". Runs a cost gate (ASYNC / NOT-READY / MEET), builds a decision-first agenda, and extracts an owner + due-date checklist that flags every orphan.
argument-hint: "[the meeting to gate, or the notes to extract actions from]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Path-B discipline skill — Rogelberg/HBR meeting-science canon + deterministic gate/agenda/extraction scripts"
  distinct_from: "project-management (team ceremonies + Jira delivery flow; this is personal meeting hygiene); business-operations/internal-comms (org-level communication design; this never auto-sends); productivity/capture (private brain-dump triage; this parses shared meeting notes)"
---

# Meetings — Cost Gate → Timeboxed Agenda → Owned Actions

> **Portability:** Reasoning-led skill with 3 stdlib Python scripts. No external APIs, no LLM calls
> in scripts, nothing auto-sent. The scripts fix the discipline; the user runs the meeting.

## What this does

Most meetings should be an email. This skill makes that testable: it prices a meeting in real
dollars, refuses to let it exist without a decision + agenda + owner, builds a timeboxed
decision-first agenda for the survivors, and afterwards turns raw notes into an owner + due-date
checklist that flags every orphan. An ASYNC verdict is a win, not a failure.

## Workflow — gate → agenda → run → extract

**1. Gate.** Before starting, ask one clarifying question if the decision to be made is unstated —
the gate cannot run honestly without it. Then price it and apply the three checks. No decision → ASYNC (exit 2): draft a memo
instead, stop here. Decision but missing agenda/owner → NOT-READY (exit 3), naming the gap.
All present → MEET (exit 0) with total cost and a cost-per-minute line.

**2. Agenda.** Only for MEET. Every topic needs a desired outcome — empty outcomes are refused by
name (exit 2). Decision topics (decide/choose/approve) sort before discuss/inform. Timeboxes plus
the mandatory 5-minute closing "actions recap" slot must fit `--length`, or the overflow is refused
with the exact overage (exit 3). Iterate — trim or split the named topic and re-run until it fits;
the stop condition is exit 0 (or the meeting goes async). Output includes a pre-read line.

**3. Run.** The user runs the meeting from the printed agenda. Hold the timeboxes; use the closing
slot to read every action aloud with its owner and date.

**4. Extract.** Feed the raw notes to the extractor: checkboxes, `ACTION:`/`TODO:` lines,
"@name will …" and "Name will … by date" patterns become a checklist grouped by owner, with
ORPHAN (no owner) and NO-DUE flags plus summary counts. Assign every orphan before posting — the
meeting is done when every action has an owner and a date; that completion check closes the loop.

```bash
# 1. Gate: should this meeting exist?
python scripts/meeting_cost_calculator.py --attendees 6 --minutes 60 \
  --avg-rate 90 --include-refocus --has-decision --has-agenda --has-owner

# 2. Agenda: timeboxed, decision-first, outcomes mandatory
python scripts/agenda_builder.py --length 45 \
  --topic "Q3 pricing:Decide usage-based vs seat-based:15:maria" \
  --topic "Launch risks:Discuss open launch blockers:15:sam"

# 4. Extract: raw notes -> owner + due-date checklist with ORPHAN/NO-DUE flags
python scripts/action_item_extractor.py --input notes.md
```

## Scripts

| Script | Role |
|---|---|
| `scripts/meeting_cost_calculator.py` | Dollars (attendees × minutes × rate, optional 23-min refocus overhead per attendee) + decision/agenda/owner gate → ASYNC / NOT-READY / MEET. |
| `scripts/agenda_builder.py` | Timeboxed decision-first agenda; refuses empty outcomes and overflow; enforces pre-read line + 5-min closing actions-recap slot. |
| `scripts/action_item_extractor.py` | Raw notes → owner-grouped markdown checklist with due dates, ORPHAN/NO-DUE flags, and summary counts. |

## References

- [`references/meeting_cost_canon.md`](references/meeting_cost_canon.md) — the real cost of meetings and the should-this-exist gate (7 sources)
- [`references/agenda_discipline.md`](references/agenda_discipline.md) — agendas as questions, timeboxing, decision-first ordering, pre-reads (7 sources)
- [`references/action_item_discipline.md`](references/action_item_discipline.md) — why meetings without owned actions are theater (6 sources)

## Assets

- [`assets/example_agenda.md`](assets/example_agenda.md) — a full worked timeboxed agenda (gate verdict → ordered topics → closing recap)
- [`assets/meeting_gate_worksheet.md`](assets/meeting_gate_worksheet.md) — fillable should-this-be-a-meeting worksheet

## Rules

- **Gate before agenda.** Never build an agenda for a meeting that hasn't passed the gate.
- **No decision, no meeting.** Status updates go async, every time.
- **No desired outcome, no agenda slot.** The builder refuses; go get the outcome.
- **Every action item has an owner and a date — or it is not an action item.** Flag, never drop.
- **Never auto-send.** No invites, no emails, no messages. Output is text the user sends.

## Distinct From (don't reach for the wrong skill)

- **`project-management/`** — team ceremonies, sprint cadence, Jira delivery flow. This gates one
  meeting at a time for the person calling it.
- **`business-operations/internal-comms`** — org-level communication design. This never designs a
  comms program and never sends anything.
- **`productivity/capture`** — triages a private brain-dump. This parses a shared meeting's notes.

---

**Version:** 1.0.0
**Build pattern:** Path-B discipline skill — meeting-science canon preserved + deterministic gate/agenda/extraction scripts added.

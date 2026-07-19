# meetings — Cost Gate → Timeboxed Agenda → Owned Actions

> Most meetings should be an email. This plugin makes that a testable claim instead of a complaint.

`/cs:meeting-prep` prices a meeting in real dollars and refuses to let it exist without a decision,
an agenda, and an owner. If it survives the gate, it gets a timeboxed, decision-first agenda where
every topic has a desired outcome. `/cs:meeting-actions` then turns the raw notes into an
owner + due-date checklist — and flags every orphan, because an action item without an owner and a
date is theater.

## The three disciplines

| Stage | The question it answers | Script |
|---|---|---|
| **The Gate** | "Should this meeting exist at all?" — cost + decision/agenda/owner checks | `meeting_cost_calculator.py` |
| **The Agenda** | "What will we decide, in what order, in how many minutes?" | `agenda_builder.py` |
| **The Extraction** | "Who owes what, by when?" — orphan and no-due flagging | `action_item_extractor.py` |

The gate returns one of three verdicts: **ASYNC** (no decision needed — send a memo instead),
**NOT-READY** (decision exists but the agenda or owner is missing — names what's missing), or
**MEET** (with the total cost and a cost-per-minute line so timeboxes get budgeted like money).

## Quick start

```bash
# 1. Gate the meeting — should it exist?
python skills/meetings/scripts/meeting_cost_calculator.py --sample

# 2. Build the timeboxed, decision-first agenda
python skills/meetings/scripts/agenda_builder.py --sample

# 3. After the meeting: extract owned action items from raw notes
python skills/meetings/scripts/action_item_extractor.py --sample
```

Or just say **"should this be a meeting?"** / **"pull the action items out of these notes"**, or run
`/cs:meeting-prep` and `/cs:meeting-actions`.

## What's in the box

- **Skill:** [`skills/meetings/SKILL.md`](skills/meetings/SKILL.md)
- **Agent:** [`agents/cs-meeting-discipline.md`](agents/cs-meeting-discipline.md)
- **Commands:** [`commands/cs-meeting-prep.md`](commands/cs-meeting-prep.md) — `/cs:meeting-prep` ·
  [`commands/cs-meeting-actions.md`](commands/cs-meeting-actions.md) — `/cs:meeting-actions`
- **3 stdlib scripts:** `meeting_cost_calculator.py`, `agenda_builder.py`, `action_item_extractor.py`
- **3 references** (Rogelberg / HBR / Grove / Amazon canon, 5-7 sources each), **2 assets**
  (worked timeboxed agenda + fillable should-this-be-a-meeting worksheet)

## Not the same as

- **`project-management/`** — team ceremonies, sprint cadence, Jira delivery flow. This is personal
  meeting hygiene: one meeting, one gate, one agenda, one checklist.
- **`business-operations/internal-comms`** — org-level communication channel design. This never
  designs a comms program and never auto-sends anything.
- **`productivity/capture`** — triages your own brain-dump. This extracts owned actions from a
  shared meeting's notes.

## License

MIT.

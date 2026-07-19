---
name: "cs-meeting-actions"
description: "/cs:meeting-actions — Turn raw meeting notes into an owned action-item checklist: extracts checkboxes, ACTION:/TODO: lines, '@name will …' and 'Name will … by date' patterns, groups by owner, and flags every ORPHAN (no owner) and NO-DUE item. An action without an owner and a date is not an action."
argument-hint: "[path to notes file, or paste the notes]"
---

# /cs:meeting-actions — Raw Notes → Owned Action Checklist

**Command:** `/cs:meeting-actions [notes file or pasted notes]`

A meeting that ends without owned, dated actions was theater. This command runs immediately after
the meeting — while attendees still remember what they agreed to — and turns the messy notes into a
checklist where every item has a name and a date, or is loudly flagged until it does.

## When to Run

- The meeting just ended and the notes are a wall of prose
- "Pull the action items out of these notes"
- "Who owes what from Thursday's meeting?"
- Before posting a meeting summary — so the summary leads with the actions

## When NOT to Run

- Before the meeting → use `/cs:meeting-prep` (cost gate + agenda)
- Triaging your own private brain-dump → `productivity/capture` owns that
- Turning actions into Jira issues and sprint work → `project-management/` owns delivery flow

## What You Get

1. **A markdown checklist grouped by owner** — each item with its due date where one was captured.
2. **ORPHAN flags** — every action with no owner, grouped under "(unassigned)" so they get claimed
   before the thread goes cold.
3. **NO-DUE flags** — owned actions with no date, listed so a date gets attached now, not "later".
4. **Summary counts** — total actions · owned · orphaned · missing dates, in one line.

## Trigger Phrases (auto-invoke without /cs:)

- "extract the action items" / "pull out the actions"
- "who owes what" / "turn these notes into a checklist"
- "action items from this meeting"

## Discipline

- **Every action item has an owner and a date — or it is not an action item.** Flags are the output,
  not noise; never silently drop or auto-assign an orphan.
- **Extraction is deterministic** — the script's patterns decide what counts; don't invent actions
  the notes don't contain.
- **Orphans get resolved by a human** — present them for assignment; never guess an owner.
- **Never auto-send** — the checklist is text the user posts. No emails, no messages, no issues filed.

## Workflow

```bash
# From a notes file
python ../skills/meetings/scripts/action_item_extractor.py --input notes.md

# From pasted notes on stdin
cat notes.md | python ../skills/meetings/scripts/action_item_extractor.py

# Machine-readable, for piping into other checklists
python ../skills/meetings/scripts/action_item_extractor.py --input notes.md --json
```

Then walk the flags: assign every ORPHAN, date every NO-DUE, and post the checklist.

## Stop Conditions

- Checklist delivered, every ORPHAN either assigned by the user or explicitly left flagged → done.
- Zero actions extracted → say so plainly and ask whether the meeting actually decided anything
  (that's a `/cs:meeting-prep` conversation for next time). Don't fabricate items.
- User says "just give me the list" → checklist + summary counts, no assignment walkthrough.

## Related

- Agent: [`cs-meeting-discipline`](../agents/cs-meeting-discipline.md)
- Skill: [`meetings`](../skills/meetings/SKILL.md)
- Sibling command: [`/cs:meeting-prep`](cs-meeting-prep.md) (pre-meeting gate + agenda)

---

**Version:** 1.0.0

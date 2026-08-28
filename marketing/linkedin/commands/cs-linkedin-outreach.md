---
name: "cs-linkedin-outreach"
description: "/cs:linkedin-outreach — Build a weekly commenting roster inside a real time budget, and write one outreach message at a time that refuses to be a template. Caps volume against LinkedIn's observed invitation limits and refuses automation-shaped plans. Nothing is ever sent."
argument-hint: "[who you want to reach, and how much time you have]"
---

# /cs:linkedin-outreach — Comments first, messages second

**Command:** `/cs:linkedin-outreach [who, and how much time]`

**Nothing here is sent.** No credentials, no API calls. Automated connecting, messaging,
commenting, liking, and sharing are prohibited by LinkedIn's User Agreement §8.2.

## When to run

- "Who should I be commenting on?"
- "Write a connection request to X"
- "How many invites can I safely send this week?"
- Reach is flat and you are only publishing

## What you get

1. **A five-day comment roster** from accounts you name, capped at two appearances per
   account per week and balanced across tiers.
2. **A volume verdict** — safe, tight, over a cap, or refused as an automation plan.
3. **One assembled message** with the person-specific line enforced and the 200/300-character
   cap checked.
4. **The follow-up rule**, stated once.

## Workflow

```bash
# 1. Roster (tiers: huge | larger | peer | smaller)
python3 ../skills/linkedin-engagement/scripts/comment_target_planner.py \
  --account "Priya Raman:5:4:larger" --account "Tomas Lind:5:3:peer" \
  --minutes-per-day 18 --output human

# 2. Volume check BEFORE writing anything
python3 ../skills/linkedin-engagement/scripts/outreach_volume_guard.py \
  --invites 20 --pending 5 --minutes 120 --acceptance 0.42 --output human
#   exit 4 = refused as an automation plan. Do not build a smaller version of it silently.

# 3. One message, for one person
python3 ../skills/linkedin-engagement/scripts/outreach_message_builder.py \
  --type connection --recipient "Priya" --specific-line "..." --reason "..." --output human
```

## Discipline

- **No engagement pods.** Coordinated reciprocal commenting is inauthentic engagement under
  §8.2 regardless of who pressed the key.
- **The tool builds the roster, never the comments.** A generated comment is exactly what the
  rule names, and it is recognisable anyway.
- **Every message carries a line that could only have been written for that person.**
- **No ask in a first-touch connection note.** The note earns the conversation, not the meeting.
- **Acceptance below 20% is a stop signal**, not a reason to send more.
- **One follow-up, a week later, only with something new to say.**

## Stop conditions

- Roster built and the first day's comments written by the user → done.
- Volume guard at exit 4 → refuse, explain once, offer the manual cadence. If the user
  reaffirms, say the risk is theirs and decline to build it.
- Message at exit 0 → hand it over with "send this yourself, to this one person".

## Related

- Skill: [`linkedin-engagement`](../skills/linkedin-engagement/SKILL.md)
- Worksheet: [`outreach_worksheet.md`](../skills/linkedin-engagement/assets/outreach_worksheet.md)

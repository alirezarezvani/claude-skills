---
name: linkedin-engagement
description: Use when someone wants to grow reach through comments, replies, groups, or outreach on LinkedIn — a commenting roster, a connection request note, a DM or InMail, a networking plan, or a check on whether their outreach volume is safe. Triggers on "who should I engage with", "write a connection request", "cold DM", "LinkedIn outreach", "networking strategy", "how many invites can I send". Builds a weekly comment roster inside a real time budget, assembles one message at a time and refuses templates, and caps volume against LinkedIn's limits. Nothing is ever sent.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
---

# LinkedIn Engagement — comments first, outreach second

From a standing start your posts reach almost nobody, and publishing harder does not fix it.
A substantive comment on a post that already has an audience puts your name, headline, and a
paragraph of thinking in front of people already reading about your subject, for six minutes
of work — the cheapest distribution on the platform, and the most badly used.

**Nothing here sends anything** — no credentials, no API calls. Automated connecting,
messaging, commenting, liking, and sharing are prohibited by User Agreement §8.2.

## Workflow

**1. Build the comment roster.** Name 8-12 accounts they would read anyway, with audience
overlap and rough size tier, then:

```bash
python3 scripts/comment_target_planner.py --account "Priya Raman:5:4:larger" \
  --account "Tomas Lind:5:3:peer" --minutes-per-day 18 --output human
```

Tiers are `huge` (10x+, crowded), `larger` (2-10x, the best ratio), `peer` (~1x, where
reciprocity compounds), `smaller` (goodwill). The roster caps any account at twice a week —
commenting daily on one person reads as following them around — and keeps the huge tier under
half of any day. It builds the roster, never the comments: a generated comment is exactly
what §8.2 names, and it is recognisable anyway.

**2. Outreach — check the volume before writing anything.**

```bash
python3 scripts/outreach_volume_guard.py --invites 20 --pending 5 --minutes 120 \
  --acceptance 0.42 --output human
```

Exit 0 safe / 2 tight / 3 over a cap or the time budget / **4 refused** above 40 invitations
a day, because nobody reads that many profiles and writes that many specific lines. Pending
invitations count against the weekly limit (observed around 100), and acceptance below 20% is
a stop signal — it is the pattern LinkedIn reviews, and the targeting is wrong.

**3. Write one message, for one person.**

```bash
python3 scripts/outreach_message_builder.py --type connection \
  --recipient "Priya" --specific-line "..." --reason "..." --output human
```

It refuses without a person-specific line, refuses an ask in a first-touch connection note,
and enforces the 200-character cap (300 with `--premium`). In large third-party samples a
note barely moves acceptance (~26.4% either way) but roughly doubles the post-accept reply
rate: **the note earns the conversation, not the meeting.**

**4. The order that works.** Comment on their work for two weeks. Then invite, referencing
something specific from that reading. Then, after acceptance and a pause, ask once, small.

## Rules

- **Nothing is auto-sent.** Ever. The user pastes and sends, one person at a time.
- **No engagement pods.** Coordinated reciprocal commenting is inauthentic engagement under
  §8.2 regardless of who pressed the key. Build a real reciprocity list instead.
- **Every message carries a line that could only have been written for that person.**
- **Never paste the same comment twice.** Identical comments at volume are the definition of
  the thing §8.2 prohibits.
- **One follow-up, a week later, only with something new to say.**
- **Agreement is not a comment.** Add the counter-example, the number, or the case where it
  breaks — or skip the slot.

## Scripts

| Script | Role |
|---|---|
| [`scripts/comment_target_planner.py`](scripts/comment_target_planner.py) | Weekly roster from scored accounts, inside a time budget, with per-account and per-tier caps. |
| [`scripts/outreach_message_builder.py`](scripts/outreach_message_builder.py) | Assembles one message; refuses templates, premature asks, and 14 dead phrases. |
| [`scripts/outreach_volume_guard.py`](scripts/outreach_volume_guard.py) | Caps invitations against the observed weekly limit, pending backlog, acceptance floor, and the hours available. |

## References and assets

- [`references/comment_strategy.md`](references/comment_strategy.md) — tiers, what a comment competes on, pods, replying to your own posts (7 sources)
- [`references/outreach_ethics_and_benchmarks.md`](references/outreach_ethics_and_benchmarks.md) — the benchmark numbers with their provenance, and the personalisation claim corrected (7 sources)

- [`assets/outreach_worksheet.md`](assets/outreach_worksheet.md) — fillable per-person prep sheet
- [`assets/example_outreach.json`](assets/example_outreach.json) — input shape for the builder

## Distinct from

- **`linkedin-content`** — writes posts. A comment is a different craft on a different budget.
- **`marketing-skill/cold-email`** — email. Different channel, law, and caps.
- **`business-growth/`, `commercial/`** — sales process and deal economics, not networking.

---
**Version:** 1.0.0

# weekly-review — GTD Weekly Review Loop → Trusted System

> Close every open loop once a week. David Allen called the weekly review the "critical success
> factor" of the whole method — the system is only trustworthy if it gets reviewed.

`/cs:weekly-review` walks the three-phase GTD ritual — **GET CLEAR → GET CURRENT → GET CREATIVE** —
and refuses to call the review COMPLETE while any of the five mandatory GET CURRENT steps is
unaccounted for. Deterministic scripts do the inventory and the gating; you (and Claude) do the
thinking.

## The three phases

| Phase | What it does | Steps |
|---|---|---|
| **GET CLEAR** | Ground zero: nothing loose, nothing unprocessed | Collect loose inputs · process inboxes to zero · empty your head |
| **GET CURRENT** | The mandatory core — the system matches reality again | Next-action lists · previous calendar · upcoming calendar · waiting-for list · project lists |
| **GET CREATIVE** | Lift your eyes off the runway | Someday/maybe review · capture new ideas |

Skipping a GET CURRENT step without a stated reason **always** forces an INCOMPLETE verdict. That
gate is the whole point: a weekly review that skims the core is a guilt ritual, not a review.

## Quick start

```bash
# 1. Inventory the open loops in a workspace (checkboxes, TODO/FIXME, stale files)
python skills/weekly-review/scripts/open_loop_scanner.py --dir ~/notes --stale-days 14

# 2. Walk the checklist, then gate it — names every missing step
python skills/weekly-review/scripts/weekly_review_gate.py --list
python skills/weekly-review/scripts/weekly_review_gate.py --done "1,2,3,4,5,6,7,8" --skip "9:no someday list yet"

# 3. Audit the commitment portfolio — STALLED / NO-NEXT-ACTION / SOMEDAY-CANDIDATE + health score
python skills/weekly-review/scripts/commitment_auditor.py --input commitments.json
```

Or just say **"run my weekly review"** or run `/cs:weekly-review`.

## What's in the box

- **Skill:** [`skills/weekly-review/SKILL.md`](skills/weekly-review/SKILL.md)
- **Agent:** [`agents/cs-weekly-review.md`](agents/cs-weekly-review.md)
- **Command:** [`commands/cs-weekly-review.md`](commands/cs-weekly-review.md) — `/cs:weekly-review`
- **3 stdlib scripts:** `open_loop_scanner.py`, `weekly_review_gate.py`, `commitment_auditor.py`
- **3 references** (5-7 sources each): the GTD weekly-review canon, the psychology of open loops
  (Zeigarnik, attention residue, plan-making), and sustainable review-cadence design
- **2 assets:** fillable weekly-review checklist + a full worked example

## Not the same as

- **`productivity/reflect`** — reflects on one conversation or piece of work, once. The weekly
  review is a recurring cadence over your *whole* system.
- **`productivity/capture`** — the intake funnel (brain dump → actions). Capture feeds the system;
  the weekly review is how the system stays trusted.
- **Sprint retrospectives** (`project-management`) — a team ceremony about a shared iteration. This
  is a personal trusted-system audit; no team required.

## License

MIT.

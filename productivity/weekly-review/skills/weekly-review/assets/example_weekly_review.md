# Example: A Full Worked Weekly Review

> A realistic Friday-afternoon run of the whole loop — scan → checklist → gate → audit → next
> action — including an honest INCOMPLETE on the first gate and what happened next.

**Context:** Solo consultant, ~2 weeks since the last full review (one lapse). Notes and projects
live in `~/notes` as markdown. Timebox: 90 minutes, started 15:00.

---

## Step 0 — Scan for evidence (2 min)

```bash
python scripts/open_loop_scanner.py --dir ~/notes --stale-days 14
```

Result: **19 open loops** — 11 unchecked checkboxes across 5 files, 3 TODO markers in scripts,
5 stale files (worst: `someday/write-a-novel.md`, 63 days untouched).

## Phase 1 — GET CLEAR (25 min)

1. **Collect:** 4 paper receipts photographed, 6 screenshots moved out of the desktop, 2 voicemail
   notes transcribed → all into the task inbox.
2. **Inboxes to zero:** 47 emails processed (31 archived, 9 became next actions, 4 waiting-for,
   3 replied under two minutes). Task inbox: 14 items clarified. Notes-app inbox: 8 items.
3. **Mind sweep:** 9 new items surfaced, including "renew professional insurance" (a real loop
   that was living rent-free in working memory) and "pitch retainer renewal to Acme."

## Phase 2 — GET CURRENT (40 min)

4. **Next-action lists:** 12 marked done, 3 pruned as dead, 2 flagged stuck (both blocked on the
   same unanswered client email — chased in step 7).
5. **Previous calendar (2 weeks back, because of the lapse):** the Acme kickoff spawned 3
   follow-ups never captured; a dentist appointment was missed → rebook action created.
6. **Upcoming calendar:** conference talk in 12 days → "draft outline" created *now* instead of
   the night before; two client calls need agendas → 2 prep actions.
7. **Waiting-for:** 6 items. 2 chased (incl. the blocker from step 4), 1 re-dated, 1 dropped
   (the vendor clearly isn't answering — found an alternative instead).
8. **Project lists:** exported to `commitments.json` and audited:

```bash
python scripts/commitment_auditor.py --input commitments.json
```

```
Flags: STALLED 3 · NO-NEXT-ACTION 2 · SOMEDAY-CANDIDATE 1
Formula: score = 100 - 30*(stalled/total) - 40*(no_next_action/total) - 30*(someday_candidates/total)
COMMITMENT HEALTH: 66.7/100    VERDICT: DRIFTING
```

Resolutions: "Hire a designer" got a next action ("post the brief in two freelance communities");
"Write a novel" was honestly moved to someday/maybe; "Learn Spanish" got a concrete next action
("book Tuesday trial lesson") instead of the standing guilt entry.

## First gate — honest INCOMPLETE (15:05 + 67 min)

Ten minutes left in the timebox and phase 3 untouched. Gate what's true:

```bash
python scripts/weekly_review_gate.py --done "1,2,3,4,5,6,7,8"
```

```
Completion: 80.0%  (done 8 · skipped 0 · missing 2)
Missing steps: 9. [GET CREATIVE] Review someday/maybe · 10. [GET CREATIVE] Capture new ideas
VERDICT: INCOMPLETE        (exit code 2)
```

All five GET CURRENT steps done, so nothing *forced* the incomplete — GET CREATIVE was simply not
done yet. Ten minutes remained, and step 9 was half-triggered by the audit anyway, so: continue.

## Phase 3 — GET CREATIVE (10 min)

9. **Someday/maybe:** 14 items reviewed. 1 activated ("small-group workshop" — two people asked
   about it this month), 2 killed without ceremony, novel filed with a clear conscience.
10. **New ideas:** 3 captured, including a productized-audit offering sketched in four bullets.

## Final gate — COMPLETE

```bash
python scripts/weekly_review_gate.py --done "1,2,3,4,5,6,7,8,9,10"
```

```
Completion: 100.0%  (done 10 · skipped 0 · missing 0)
VERDICT: COMPLETE          (exit code 0)
```

## Close (total: 82 min)

**One next action for the coming week:** send the Acme retainer-renewal email (drafted Monday
09:00, calendar-blocked).

**What made this a good review:** evidence first (the scan found loops memory had dropped); the
lapse was handled with a look-back, not a guilt marathon; the first gate was allowed to say
INCOMPLETE; every flagged project left with a disposition; and it ended inside the timebox with
one concrete commitment.

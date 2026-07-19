# Weekly Review Checklist

> Fillable template. Copy this file (or print it), work top to bottom, then gate it:
> `python scripts/weekly_review_gate.py --done "..." --skip "N:reason"`

**Week of:** ____________  **Started:** ____:____  **Timebox ends (max 2h):** ____:____

---

## Phase 1 — GET CLEAR

- [ ] **1. Collect loose inputs** — papers, receipts, notes, screenshots, downloads → into an inbox
  - Scanner run? `python scripts/open_loop_scanner.py --dir ______ --stale-days 14`
  - Loops found: checkboxes ____ · TODO/FIXME ____ · stale files ____
- [ ] **2. Process inboxes to zero** — clarify, don't do (two-minute rule is the only exception)
  - Inboxes processed: ☐ email ☐ task inbox ☐ notes app ☐ desk/physical ☐ other: ______
- [ ] **3. Empty your head** — mind sweep; capture every commitment still riding in memory
  - New items captured: ____

## Phase 2 — GET CURRENT (all five mandatory)

- [ ] **4. Review next-action lists** — mark done, prune dead, surface stuck
  - Done: ____ · Pruned: ____ · Stuck (needs decision): ____
- [ ] **5. Review previous calendar** — missed or spawned commitments become captured items
  - Items captured from the look-back: ____
- [ ] **6. Review upcoming calendar** — prepare, don't react
  - Prep actions created: ____
- [ ] **7. Review waiting-for list** — chase, re-date, or drop each item
  - Chased: ____ · Re-dated: ____ · Dropped: ____
- [ ] **8. Review project lists** — every active project has exactly one next action
  - Auditor run? `python scripts/commitment_auditor.py --input ______`
  - Health score: ____/100 · Verdict: ______
  - STALLED: ____ · NO-NEXT-ACTION: ____ · SOMEDAY-CANDIDATE: ____

## Phase 3 — GET CREATIVE

- [ ] **9. Review someday/maybe** — activate, keep, or kill
  - Activated: ____ · Killed: ____
- [ ] **10. Capture new ideas** — add them while the head is clear
  - New ideas captured: ____

---

## Gate it

```bash
python scripts/weekly_review_gate.py --done "____________" --skip "____________"
```

**Gate verdict:** ☐ COMPLETE (exit 0) ☐ INCOMPLETE (exit 2)
**Missing steps named by the gate:** ______________________________________

## Close

**One next action for the coming week:** ______________________________________
**Finished:** ____:____ (total: ____ min — target 60-90)

> Skipped a step? Write the reason above and give it first priority next week.
> Lapsed last week? Shorter pass, zero guilt. The review is maintenance, not judgment.

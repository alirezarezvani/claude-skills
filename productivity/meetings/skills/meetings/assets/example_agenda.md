# Worked Example — Q3 Pricing Decision Meeting

A full pass through the `meetings` skill for a real meeting, from gate to agenda. Use it as the
canonical shape for what the scripts produce and how the pieces snap together.

## Step 1 — The gate

```bash
python scripts/meeting_cost_calculator.py --attendees 6 --minutes 45 \
  --avg-rate 90 --include-refocus --has-decision --has-agenda --has-owner
```

```
Meeting Cost Gate (should this meeting exist?)
================================================================
  Attendees: 6   Length: 45 min   Rate: $90/hr
  Direct cost:  $    405.00   (6 x 45 min x $90/hr)
  Refocus cost: $    207.00   (23 min refocus overhead per attendee)
  TOTAL COST:   $    612.00

  Gate: decision=yes | agenda=yes | owner=yes

  VERDICT: MEET
  Gate passed: decision + agenda + owner. This meeting has earned its slot. It costs $612.00 —
  budget the agenda timeboxes like money.

  Every minute of this meeting costs $13.60 — price each agenda topic's timebox against that.
```

**MEET** — proceed to the agenda. (Had there been no decision, the verdict would be ASYNC and the
next step would be a memo outline, not an agenda.)

## Step 2 — The agenda

```bash
python scripts/agenda_builder.py --length 45 \
  --topic "Metrics review:Inform team of the activation trend:5:alex" \
  --topic "Q3 pricing:Decide usage-based vs seat-based:15:maria" \
  --topic "Launch risks:Discuss open launch blockers:15:sam"
```

Note what the builder did below: the **decision topic sorted to the front** even though it was
supplied second, every topic carries a desired outcome and an owner, and the closing actions-recap
slot is pinned to the end of the meeting.

```markdown
# Agenda — 45 minutes, 3 topics

**Pre-read:** circulate the relevant doc(s) at least a day ahead. The meeting starts assuming the
pre-read was read — no recap slot for skippers.

| # | Timebox | Topic | Desired outcome | Owner |
|---|---------|-------|-----------------|-------|
| 1 | 00–15 min (15 min) | Q3 pricing | Decide usage-based vs seat-based | maria |
| 2 | 15–20 min (5 min) | Metrics review | Inform team of the activation trend | alex |
| 3 | 20–35 min (15 min) | Launch risks | Discuss open launch blockers | sam |
| ✔ | 40–45 min (5 min) | **Actions recap** | Read every action aloud: owner + due date, or it is not an action | meeting owner |

_5 min of slack before the recap — if topics finish early, end early. Nobody has ever complained
about a meeting ending early._
```

## What refusal looks like

Two inputs the builder will not accept, so you see them before you hit them:

- **Empty desired outcome** (`--topic "Roadmap::10:sam"`) → exit 2:
  `REFUSED (REFUSED-NO-OUTCOME): No desired outcome, no agenda slot. Topics refused: "Roadmap". Go get the outcome, then rebuild.`
- **Overflow** (topics totaling 50 min into `--length 45`) → exit 3:
  `REFUSED (REFUSED-OVERFLOW): Timeboxes (50 min) + closing actions-recap buffer (5 min) = 55 min, but the meeting is 45 min — 10 min over. Cut a topic, shrink a timebox, or move an inform topic to the pre-read.`

## Step 3 — After the meeting

Feed the raw notes to `action_item_extractor.py` and walk the flags — see
[`meeting_gate_worksheet.md`](meeting_gate_worksheet.md) for the fillable pre-meeting worksheet
that keeps the next meeting honest too.

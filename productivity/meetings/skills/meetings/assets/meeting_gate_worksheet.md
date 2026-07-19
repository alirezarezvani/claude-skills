# Should This Be a Meeting? — Fillable Gate Worksheet

Fill this in **before** sending the invite. If you can't fill a required line, the meeting is not
ready to be called — that's the worksheet working, not failing. Pairs with
`scripts/meeting_cost_calculator.py`, which turns the answers into an ASYNC / NOT-READY / MEET
verdict with a dollar figure.

## 1. The decision (required)

> No decision, no meeting. A status update goes async, every time.

**The specific decision this meeting will make:**

- _____________________________________________________________________

**What happens if this decision is NOT made this week:**

- _____________________________________________________________________

*If you wrote "share an update", "align", or "sync" above — stop. Draft the memo/thread instead
and send it to the same list. You just saved the full cost below.*

## 2. The price

| Input | Value |
|---|---|
| Attendees (only people needed to make the decision) | _______ |
| Length in minutes | _______ |
| Avg fully-loaded hourly rate ($90 if unsure) | _______ |
| Include 23-min refocus overhead per attendee? (y/n) | _______ |

```bash
python scripts/meeting_cost_calculator.py \
  --attendees ___ --minutes ___ --avg-rate ___ --include-refocus \
  --has-decision --has-agenda --has-owner
```

**Total cost: $ _______** — Would you approve this as an invoice for the decision in section 1?
If no, cut attendees or minutes until you would.

## 3. The owner (required)

**Named meeting owner** (runs the timeboxes, owns the recap, chases the actions):

- _____________________________________________________________________

## 4. The agenda (required — outcomes, not nouns)

Every topic needs a desired outcome starting with a verb. **Decide / choose / approve** topics go
first. If a topic's outcome starts with "inform", ask whether it belongs in the pre-read instead.

| Topic | Desired outcome (verb first) | Minutes | Topic owner |
|---|---|---|---|
| ______________ | ______________________________ | _____ | _________ |
| ______________ | ______________________________ | _____ | _________ |
| ______________ | ______________________________ | _____ | _________ |

**Timebox check:** topics total _____ min + 5 min closing actions-recap = _____ min ≤ meeting
length _____ min? If not, cut — don't stretch the meeting.

## 5. The pre-read

**Doc(s) to circulate ahead:** _______________________________________________

**Sent by (owner + date):** _________________________________________________

## 6. Commitments for the room

- [ ] The meeting ends with the actions recap: every action read aloud with **owner + due date**.
- [ ] Actions without an owner get assigned before anyone leaves — no orphans out the door.
- [ ] Notes go through `scripts/action_item_extractor.py` and the checklist is posted the same day.
- [ ] If the decision gets made early, the meeting ends early.

---

**Gate verdict (from the calculator):**  ASYNC ☐   NOT-READY ☐   MEET ☐

*ASYNC → write the memo. NOT-READY → fix the named gap, re-run. MEET → build the agenda with
`scripts/agenda_builder.py` and send the invite with the pre-read attached.*

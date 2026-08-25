# Newsletter Playbook — a standing promise, priced before it is made

A LinkedIn newsletter notifies every subscriber on every issue. That notification
is the whole value and the whole risk: it is a standing promise about frequency
and subject, made to people who opted in on the strength of the first issue.

Most LinkedIn newsletters are abandoned after four issues. Not because the topic
was wrong — because the cadence was chosen against a month the author happened to
have free.

---

## Eligibility — what LinkedIn actually says

LinkedIn Help states that members and Pages with **more than 150 followers and/or
connections** are eligible to be *evaluated* for newsletter access, and that
access is granted based on **a set of criteria, all of which must be met** —
criteria LinkedIn does not publish in full. Authors can run up to five
newsletters at a time.

Two things follow:

- 150 is a floor for evaluation, not a guarantee of access. 🟢
- The tool checks the published floor and says explicitly that LinkedIn, not the
  tool, decides. Anyone stating the complete criteria list is guessing. 🔴

Creator-mode access and newsletter access have been coupled and decoupled over
time; existing authors have retained access across those changes. Check the
current Help article rather than trusting any secondary source, including this
one.

## Sustainability, over six months

`newsletter_planner.py` prices cadence × issue cost against a **six-month**
horizon, not a good month. Six months is the horizon because that is roughly when
a newsletter starts to have a returning readership rather than a launch audience.

| Cadence | Issues/month | At 150 min/issue |
|---|---|---|
| Weekly | ~4.3 | ~645 min/month |
| Every two weeks | ~2.15 | ~322 min/month |
| Monthly | 1 | 150 min/month |

If the budget does not cover it, the tool refuses and names the cadence that
fits. **Dropping cadence before launch is free. Dropping it after launch is a
broken promise to people who opted in to a frequency.**

Under 20% headroom, it warns: one busy month breaks the cadence. The mitigations
that actually work are banking two issues before launch, and keeping one
low-cost format (the roundup) in reserve for a bad month.

## Shape — twelve issues, not twelve essays

An arc that alternates issue *types* is easier to sustain and better to read than
twelve variations of the same essay:

| Type | What it is | Cost |
|---|---|---|
| **framework** | A repeatable way to make one decision. The issue people forward. | High |
| **teardown** | One real artifact examined in public, with permission or anonymised. | High |
| **field-note** | What you actually did this fortnight, including what failed. | Low |
| **counter-take** | The received wisdom in your field, and where it breaks. | Medium |
| **reader-question** | One question a reader asked, answered at length. | Low |
| **roundup** | What you read and what changed your mind. | Lowest |

The planner rotates types across pillars, offsetting the cycles so pillar/type
pairs do not repeat in lockstep.

## Naming

Name it after the problem it solves, not after yourself. "The Analytics Trust
Letter" tells a stranger whether to subscribe. "Alex's Newsletter" requires them
to already know who Alex is, which is the audience you already have.

The subtitle does the qualifying work: who it is for, and how often.

## The stop rule, written before issue one

This is the part everyone skips, and it is the reason abandoned newsletters sit
on profiles for years.

- If three consecutive issues land below half the median engagement of your
  regular posts, the format is not earning its cost. Move the material back to
  posts.
- If you miss two scheduled issues in a quarter, drop the cadence one step rather
  than trying to catch up. Subscribers notice frequency, not effort.
- **Ending it deliberately, with a final issue that says so, costs nothing.**
  Letting it go quiet is the version people remember.

## Newsletter versus posts

A newsletter is worth it when the material genuinely needs length *and* an
audience is already asking for the next one. It is not a growth tactic on its
own — the notification reaches people who already subscribed.

Under ~500 followers the planner warns rather than refuses: eligible, but the
feedback is too sparse to tell you whether the topic is right, which is the main
thing a newsletter is supposed to teach you.

## Repurposing between the two

The clean direction is **newsletter → posts**: an issue yields two or three
standalone posts over the following fortnight, each linking to the issue in the
first comment. Run them through `repurpose_splitter.py` with a ledger so the same
unit does not go out twice.

The reverse direction — stitching old posts into an issue — works only if the
issue adds a synthesis the posts did not have. Otherwise subscribers are being
notified about something they already read.

---

## Sources

1. LinkedIn Help. **"LinkedIn Newsletter access criteria."** — the >150
   followers/connections threshold, and the existence of unpublished criteria.
2. LinkedIn Help. **"Manage a newsletter on LinkedIn"** and **"Newsletters on
   LinkedIn FAQ"** — the five-newsletter limit, cadence declaration, subscriber
   notification behaviour.
3. LinkedIn Help. **"Updates to Creator Mode."** — the coupling and decoupling of
   creator tools and newsletter access over time.
4. Kleon, A. **Show Your Work!** — the case for a recurring, low-ceremony
   publishing habit over occasional set pieces.
5. Handley, A. **Everybody Writes** — editorial calendars, the "bigger, braver"
   standard for anything that lands in a notification.
6. Clear, J. **Atomic Habits** — the two-minute rule and habit stacking, applied
   here as the reserve low-cost issue format.
7. Doerr, J. **Measure What Matters** — committing the stop condition in advance,
   while it is still a decision rather than a defeat.

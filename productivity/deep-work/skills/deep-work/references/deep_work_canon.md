# The Deep Work Canon — Deep vs Shallow, the Hypothesis, the Ceiling, the Residue

> Reference for the `deep-work` skill. This is the conceptual spine behind all three scripts:
> why deep and shallow are different kinds of work, why depth is scarce and valuable, why the
> planner caps deep time at 4 hours, and why buffers between blocks are not optional.

## 1. The deep/shallow distinction

Cal Newport defines the two modes precisely (*Deep Work*, 2016):

- **Deep work** — "professional activities performed in a state of distraction-free concentration
  that push your cognitive capabilities to their limit. These efforts create new value, improve
  your skill, and are hard to replicate."
- **Shallow work** — "noncognitively demanding, logistical-style tasks, often performed while
  distracted. These efforts tend to not create much new value in the world and are easy to
  replicate."

The operational test Newport supplies — and the one `shallow_work_auditor.py` prints for every
shallow item — is the **recent-graduate heuristic**: *how long would it take to train a smart
recent college graduate with no specialized training to do this task?* Months or years of training
means the task is probably deep. Days or weeks means it is shallow, however urgent it feels.

The auditor's keyword heuristic (email, slack, status, meeting, expense, scheduling, admin →
shallow; write, design, code, build, research, analyze, study → deep) is a first-pass proxy for
this test — which is why the explicit `:deep`/`:shallow` override always wins. The heuristic
starts the conversation; the recent-graduate question settles it.

## 2. The deep work hypothesis

Newport's central economic claim: **the ability to perform deep work is becoming increasingly rare
at exactly the same time it is becoming increasingly valuable.** As machines and markets absorb
routine cognitive work, the two abilities that compound are (a) quickly mastering hard things and
(b) producing at an elite level of quality and speed — and both are functions of depth. The people
who cultivate deep work "will thrive"; those who default to reactive shallowness compete in the
most crowded segment of the labor market.

This is why the skill treats attention — not time — as the protected resource. Eight hours of
fragmented availability produce less durable value than three well-defended deep hours.

## 3. The 4-hour trained limit

The planner's hard cap (`DEEP_CAP_MIN = 240`) comes from the deliberate-practice literature that
Newport builds on. Ericsson, Krampe, and Tesch-Römer's landmark study of expert violinists (1993)
found that even elite performers sustain roughly **four hours of deliberate, maximally effortful
practice per day** — typically in sessions of about 60-90 minutes with rest between — before the
quality of the work collapses. Newport translates this directly: "for someone new to such practice,
an hour a day is a reasonable limit. For experts, four hours — but rarely more."

Two consequences are encoded in `time_block_planner.py`:

1. Scheduling more than 4 hours of deep blocks is refused (exit 2), not warned about. Depth past
   the ceiling is fake depth — the block is on the calendar but the concentration is not in it.
2. The minimum deep block is 90 minutes. Csikszentmihalyi's flow research shows that full
   absorption takes time to enter and rewards long uninterrupted stretches; blocks shorter than
   about 90 minutes spend most of their length ramping up rather than producing.

## 4. Attention residue — why buffers and batching exist

Sophie Leroy (2009) named the mechanism that fragmented schedules quietly bleed: **attention
residue**. When a person switches from Task A to Task B, part of their attention remains stuck on
A — especially when A was unfinished or left under time pressure — and performance on B measurably
degrades. People who worked on a single task without switching significantly outperformed those
who hopped, even when total time was equal.

Gloria Mark's field studies of information workers quantify the recovery cost: after a significant
interruption, it takes on the order of **23 minutes** to fully re-engage with the original task,
and interrupted workers compensate by working faster at the price of more stress and frustration.

The planner encodes both findings:

- **10-minute buffers** between consecutive work blocks give residue somewhere to drain — stand
  up, reset, close the loop — instead of carrying it into the next block.
- **Shallow work is batched into at most two windows.** Every sprinkle of "just one email" between
  deep tasks is a residue event plus a ~23-minute refocus tax. Two batches means at most two
  context-switch penalties per day instead of a dozen.

## 5. Maker's schedule — why deep blocks go earliest

Paul Graham's essay "Maker's Schedule, Manager's Schedule" (2009) explains why a single meeting
can destroy an afternoon: makers operate in units of half a day at minimum, because "a single
meeting can blow a whole afternoon, by breaking it into two pieces each too small to do anything
hard in." The planner therefore front-loads deep blocks into the earliest hours — before the
manager-schedule world wakes up and starts fragmenting the calendar — and pushes shallow batches
to late morning and end of day, where fragmentation does the least damage.

## Sources

1. Cal Newport, *Deep Work: Rules for Focused Success in a Distracted World* (Grand Central, 2016) — the deep/shallow definitions, the deep work hypothesis, the recent-graduate heuristic, the 4-hour claim.
2. Sophie Leroy, "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks," *Organizational Behavior and Human Decision Processes* 109(2), 2009.
3. Gloria Mark, Daniela Gudith, and Ulrich Klocke, "The Cost of Interrupted Work: More Speed and Stress," *Proceedings of CHI 2008* — the ~23-minute refocus finding popularized from Mark's research program.
4. K. Anders Ericsson, Ralf Th. Krampe, and Clemens Tesch-Römer, "The Role of Deliberate Practice in the Acquisition of Expert Performance," *Psychological Review* 100(3), 1993 — the ~4-hour daily limit on deliberate practice.
5. Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience* (Harper & Row, 1990) — absorption, the cost of entry into flow, why long blocks outperform fragments.
6. Paul Graham, "Maker's Schedule, Manager's Schedule" (paulgraham.com, 2009) — half-day units of maker time; why meetings fragment afternoons.

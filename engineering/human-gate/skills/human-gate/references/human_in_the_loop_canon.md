# Human-in-the-loop review: the canon

Why a human verification lane exists at all, and what decades of inspection research
say about how to run one. The short version: **automation does not remove the human's
job, it makes the remaining human job harder and more consequential** — which is
exactly why it needs structure rather than good intentions.

---

## 1. Ironies of automation

Lisanne Bainbridge's *Ironies of Automation* (Automatica, 1983) is the foundational
argument. Automate the routine parts of a task and two things follow:

1. The human is left with the **hardest residual judgements**, not the easiest.
2. The human's skill at those judgements **decays**, because they no longer practise
   the routine work that built it.

Applied to agent loops: the more capable the agent, the *more* important — and the more
degraded — the reviewer's attention becomes. A gate that merely *invites* review will
get skimming. A gate that names a person, demands a severity, and refuses to close
without a resolution forces the attention the irony predicts you will otherwise lose.

Parasuraman & Riley, *Humans and Automation: Use, Misuse, Disuse, Abuse* (Human Factors,
1997) supplies the failure mode by name: **automation bias** — operators accept
automated output they would have questioned had a human produced it. Their finding that
complacency rises with perceived reliability is the reason `close` refuses on G1 rather
than trusting that someone probably looked.

---

## 2. Inspection research: structure beats effort

Michael Fagan's *Design and code inspections to reduce errors in program development*
(IBM Systems Journal, 1976) established the modern inspection: defined roles, a defined
artifact, defined defect classes, and a rework step that must complete before exit. The
durable lessons:

- **Named roles beat diffuse responsibility.** Fagan assigns a moderator, an author, and
  reviewers. Ambiguity about who is accountable is where inspections rot. → gate rule G3.
- **Exit criteria are explicit.** An inspection is not over when everyone stops talking;
  it is over when rework is verified. → gate rules G1/G2/G4.
- **Defects are classified, not just described.** Classification is what makes review
  output aggregable and comparable across rounds. → the severity ladder.

Karl Wiegers, *Peer Reviews in Software* (Addison-Wesley, 2001) adds the practical
correction most teams need: review effectiveness collapses when reviewers are given no
severity vocabulary and no cap on scope. Unbounded review produces either rubber stamps
or infinite rounds — the two failure modes gate rule G5 is aimed at.

---

## 3. The modern industrial form

*Software Engineering at Google* (Winters, Manshreck & Wright, O'Reilly, 2020), chapter 9,
documents review at scale. Two points transfer directly:

- Review is **primarily about comprehensibility**, not defect-hunting. Most value comes
  from a second person being able to follow the artifact at all.
- **Latency is the enemy.** Google optimises hard for reviewer turnaround because a slow
  review loop gets routed around. This is the strongest argument for *not* holding an
  agent turn open while waiting: a blocked agent adds latency and pressure without
  adding review quality.

Google's public [Code Review Developer Guide](https://google.github.io/eng-practices/review/)
supplies the severity convention this skill adopts — the `Nit:` prefix convention and the
principle that a reviewer should distinguish *must fix* from *preference*. The
BLOCKER / MAJOR / MINOR / NIT ladder used here (and in `markdown-html/md-review`) is the
common four-rung expression of that idea.

---

## 4. Egoless review

Gerald Weinberg's *The Psychology of Computer Programming* (1971) introduced **egoless
programming**: separating the artifact from the author's identity so critique lands on
the work. The operational trick is to make feedback **about a located thing** — a block,
a quote, a line — rather than about the document in general.

This is why every item in a `batch.v1` anchors to a block id and, where possible, a
verbatim quote. "The tone is off" invites defence. "`b7`: this sentence claims 40% with
no source" invites a fix.

---

## 5. Reversibility sets the bar

Not every artifact deserves the same gate. The useful frame is Amazon's **one-way vs
two-way doors** (Bezos, 2015 shareholder letter): decisions that are cheap to reverse
should be made fast and unilaterally; decisions that are expensive or impossible to
reverse deserve deliberate process.

Practical mapping for this skill:

| Artifact | Door | Gate posture |
|---|---|---|
| Internal draft, notes, a branch | two-way | open a round if asked; NITs need not block |
| Spec, RFC, plan others will build from | mixed | hold G2 strictly |
| Customer-facing copy, a migration, a public post | one-way | require explicit APPROVE, not merely "no blockers" |

Gary Klein's **pre-mortem** technique (*Harvard Business Review*, 2007) is the cheapest
upgrade to any of these: ask the reviewer to state, *before* reading, what would make
them reject it. Pre-committing a rejection criterion measurably reduces rubber-stamping.

---

## 6. What this means for agent loops specifically

Anthropic's published guidance on building effective agents makes the point that agent
systems should be designed around **verifiable checkpoints** rather than end-to-end
trust. Machine checks cover what is mechanically checkable. Everything else — taste,
strategy, tone, whether the claim is actually true, whether this is the right thing to
build at all — has no automated verifier and never will.

That residual set is not a gap to be closed later. It is permanently the human's, and it
is precisely what Bainbridge warned would get harder as the rest got easier. The gate
exists to make sure that residue is handled explicitly rather than absorbed by an agent's
own confidence.

---

## Sources

1. Bainbridge, L. *Ironies of Automation.* Automatica 19(6), 1983.
2. Parasuraman, R. & Riley, V. *Humans and Automation: Use, Misuse, Disuse, Abuse.*
   Human Factors 39(2), 1997.
3. Fagan, M. *Design and code inspections to reduce errors in program development.*
   IBM Systems Journal 15(3), 1976.
4. Wiegers, K. *Peer Reviews in Software: A Practical Guide.* Addison-Wesley, 2001.
5. Winters, T., Manshreck, T. & Wright, H. *Software Engineering at Google*, ch. 9.
   O'Reilly, 2020.
6. Google. *Code Review Developer Guide.* https://google.github.io/eng-practices/review/
7. Weinberg, G. *The Psychology of Computer Programming.* Van Nostrand Reinhold, 1971.
8. Klein, G. *Performing a Project Premortem.* Harvard Business Review, September 2007.

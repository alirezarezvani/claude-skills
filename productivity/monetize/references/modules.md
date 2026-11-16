# Module Specifications

Detailed rules for the six modules. `SKILL.md` carries the workflow; this file carries the edge cases.

## Module 1 — Hidden-skills audit

**Output shape:** a table with one row per skill.

| Skill | Why it pays | Who pays | How AI multiplies it |
|---|---|---|---|
| Supply-chain negotiation for small-batch goods | Every seller loses margin on first-order MOQ | Small e-commerce sellers shipping their first container | Drafts the term sheet and a counter-offer matrix; negotiation still happens live |

**Coverage rule:** at least two rows from each of: hard skills, soft skills (management, negotiation, coordination), compound skills (the intersection of two domains), and industry process know-how.

**Quality bar:** at least two rows must surprise the user. If every row is something they already put on their résumé, the audit is not done.

**Buyer specificity:** "people who need help" is not a buyer. Write the profile — role, company size, trigger event, budget source.

## Module 2 — Opportunity scan

**Output shape:** six columns per path.

| Path | Startup cost | Time to first sale | Weekly hours | Difficulty | Monthly range |
|---|---|---|---|---|---|

**Sourcing rule:** for each path, search the current market price of comparable services and the platform's current conditions (commission, traffic, listing requirements). Cite the source. If search is unavailable or returns nothing usable, mark the range "estimate, unverified" and list it in Appendix B.

**Ranking rule:** sort by potential ÷ friction, where friction = startup cost + time to first sale + weekly hours + difficulty, normalized against the user's constraints. Give one sentence of reasoning per path.

**Cut rule:** a path that violates an explicit constraint (no camera, no weekends, cannot invoice legally) is deleted, not softened. Eight good paths beat ten padded ones.

## Module 3 — Productization

**Four categories:** 1:1 service, consulting/diagnostic, digital product (template, course, tool), freelance offer (retainer or project).

**Per product, five elements:**

1. **Name** — how the buyer would refer to it.
2. **Target client** — one sentence, concrete.
3. **Deliverable** — schedulable and countable: "one 60-minute diagnostic call plus a one-page action list," not "consulting."
4. **Price and basis** — the number, plus the source or the label.
5. **AI's role** — what the AI drafts, and what the human still does.

**Rule:** pricing must come from a market comparator, not from a round number the model likes.

## Module 4 — Leverage point

**Output shape:**

- The one action, in one imperative sentence.
- Why this action, tied to the user's constraints (time, money, channels).
- A day-by-day first week.
- Two alternates, each with a one-line reason it is not first.

**Selection criteria:** lowest startup cost, fastest positive feedback, reuse of an existing asset (audience, past client, portfolio piece).

**Failure condition:** if the action needs more than one week of preparation before any buyer sees it, it is not the leverage point.

## Module 5 — Salary ceiling

**Per target role:** verified range (with city and date), qualifications the user already holds, the gap, how to close it, and whether a transition is required.

**Compression rule:** if the user said "no job change, side income only," reduce this to a short subsection: what the ceiling is and what would have to change to reach it.

**Honesty rule:** salary ranges are searched with a named source and a date. Salary data without a date is not data.

## Module 6 — AI side-hustle starter pack

**Envelope:** under five hours per week to run, under the startup budget (default 1,000 in the user's currency).

**Per service:** definition, target client, acquisition channel, AI toolchain (which step, which kind of tool), price, week-one action.

**Consistency rule:** the five services must map onto module 2 paths the user already ranked highly. Do not introduce a new direction here.

**Realism rule:** name the human steps that AI does not remove — client calls, quality review, contracting, delivery accountability.

## Report template

```markdown
# Monetization report — <name/alias> · <date>

## 0. Asset snapshot
One paragraph a stranger could read.

## 1. Hidden-skills audit
The table from module 1.

## 2. Opportunity scan
The table from module 2, sorted, with one-line reasoning per row.

## 3. Productization
Four categories, each with 2–3 products and the five elements.

## 4. Leverage point
The action, the why, the first week, two alternates.

## 5. Salary ceiling
Target roles, ranges, gaps, transition path.

## 6. AI side-hustle starter pack
The five services.

## 7. 30-day plan
Week 1 / week 2 / weeks 3–4. Each item has a day, a duration, and an acceptance criterion.

## Appendix A: sources
Every verified number with its URL and access date.

## Appendix B: unverified estimates
Every number that is not verified, with the basis for the estimate.
```

## Edge cases

- **User refuses to share salary/city.** Run the modules with the default market range, label it, and say what the numbers would change with the real figure.
- **User asks only "how much can I make?"** Answer with a range and the two variables that move it most, then offer the full run.
- **User asks for a reality check on someone else's offer.** Still intake the user's background first — the answer is only meaningful relative to their constraints.
- **User has a business already.** Treat the existing business as the main path and ask what its constraint is (demand, delivery, margin) before proposing new paths.

# Positioning Brief

The editorial constitution. When a post idea does not fit a pillar, the answer is not to add
a pillar — it is to not post it, or to put it in the experimental slot and see.

Review quarterly. A brief revised monthly is a mood.

---

## 1. Objective — pick exactly one

- [ ] `career-change` — move into a different role or field
- [ ] `consulting` — generate consulting or freelance work
- [ ] `thought-leadership` — be cited as a credible voice on one specific thing
- [ ] `hiring` — attract candidates to a team you are building
- [ ] `fundraising` — build investor and operator awareness ahead of a raise
- [ ] `community` — build a durable group around a shared problem

Two objectives serve neither. If both matter, run one this quarter and the other next.

## 2. Audience

Specific enough that a real person could be excluded. Role + company stage + the problem
they have *this quarter*.

> ______________________________________________________________

Bad: "business leaders", "professionals in tech", "my network".
Good: "heads of data at Series A-B SaaS with three analysts, no analytics engineer, and a
CEO who does not trust the dashboard".

## 3. Pillars — two to four, shares summing to 100

| Pillar | Why you (your specific standing) | Proof that already exists | Share |
|---|---|---|---|
| | | | % |
| | | | % |
| | | | % |
| | | | % |

Rules:
- At least one pillar must rest on proof that **already exists**.
- At least one pillar at **10-20%** — the experimental slot. Next quarter's main pillar
  comes from here.
- Empty "why you" means anyone could post it. Cut the pillar.

## 4. Exclusions — at least two

What you will not post about, and why. This is the actual positioning.

1. ______________________________________________________________
2. ______________________________________________________________
3. ______________________________________________________________

The trending topic you have no edge on belongs here.

## 5. 90-day criteria

Filled in by `positioning_brief.py` from the objective. Every one is observable by someone
other than you. Follower count is deliberately absent.

- [ ] ______________________________________________________________
- [ ] ______________________________________________________________
- [ ] ______________________________________________________________

## 6. Budget

- Minutes per week I will protect (from a bad week): ______
- Stage: `starting` / `rebuilding` / `established`
- Formats I can actually produce: ______

---

**Then run:**

```bash
python3 ../scripts/positioning_brief.py --input brief.json --output human
python3 ../scripts/cadence_planner.py --minutes <n> --stage <stage> --output human
```

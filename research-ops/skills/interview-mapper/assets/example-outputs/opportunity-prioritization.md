# Output: Opportunities and prioritization (Opportunity Tree)

**When:** the goal is to turn insights into prioritized opportunities/solutions (input to the roadmap).
**Input:** insights from `score_insights.py` (with frequency×criticality and status).

## Structure (per Opportunity Solution Tree)
```
OUTCOME: [measurable business/product goal at the top]
├── Opportunity 1 (pain/need from an insight) [priority: score]
│    Based on: X of N interviews · criticality · verified quotes
│    ├── Solution A — [idea] · effort: low/med/high
│    └── Solution B — …
│    How to test: [assumption test]
├── Opportunity 2 …
```

## Prioritization
- Opportunity rank = **frequency × criticality** from `score_insights` (not the loudest voice).
- A separate **watchlist** track: rare-but-critical and tensions — don't bury them under the frequent.
- Every opportunity is grounded in ≥k interviews with a verified quote; otherwise "hypothesis, gather more data".

## Rules
- Don't jump to solutions without an opportunity (pain). A solution without a grounded pain = personal taste.
- For disputed priorities (the council flagged them) — to a human, don't decide yourself.
- State the effort/risk of a solution, but do NOT invent estimates that aren't in the data.

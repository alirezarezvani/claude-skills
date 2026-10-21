# Output: Insight cards

**When:** the goal is to extract cross-interview insights. The default synthesis output (S5–S7).
**Input:** nuggets with clusters → `score_insights.py`. Write cards only for `insight`/`watchlist`.

## Card format
```
### [ID] Title — one sentence
Statement: [observation + interpretation + implication — not a retelling]
Holds for: [roles/segments] · NOT for: [where it doesn't work]
Prevalence: X of N interviews (roles: …) · Criticality: high/medium/low
Type: CONSENSUS | TENSION ([role A] vs [role B] — on what)
Evidence (verified + support=yes only):
  - [Interview, role] «verbatim quote» (Lxx)
  - [Interview, role] «…» (Lxx)
Counter-evidence: [who didn't confirm / what contradicts / where there's silence]
Confidence: high/medium/low (based on triangulation + grounding)
Implication / recommendation: [what to do; for whom]
```

## Rules
- A pattern = ≥k different interviews with a verified quote (not k quotes from one person).
- Every card goes through counter-evidence.
- Scope by role: "for collections staff", not "for employees".
- Sorting: `insight` by frequency×criticality → `watchlist` (tensions, rare-but-critical). `weak` — into the appendix.
- Optionally → HTML board: `render_board.py provenance.json`.

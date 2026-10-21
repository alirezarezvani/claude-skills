# Synthesizing insights from a series of interviews (S5–S7)

The "N mappings → insights" stage. Main principle: **build up from atoms, don't compress from the top**.
A summary of summaries = where hallucinations compound ("employees think X" out of thin air).

## S5 — Nuggets (atomization)
From each mapping, pull out atomic observations. A nugget is indivisible and grounded.

Schema (`nuggets.json`, a list):
```json
{"id":"n1","interview":"Daria","role":"operations","cell":"K9",
 "observation":"Learns about decisions after the fact ~40%",
 "quote":"they call me at night...","line":135,
 "verified":true, "severity":4, "valence":"-", "cluster":null}
```
- `verified` — did the quote pass through `verify_quotes.py` (use ONLY verified nuggets as evidence of a pattern).
- `severity` 1–5 — criticality/impact (set by the model, justify it).
- `valence` `+`/`-`/`0` — sign (needed for tension detection).
- `role` — mandatory: insights are scoped by role.

## Severity / valence rubric (the model sets these by this scale, not at random)
The `score_insights.py` script depends on these fields — garbage in gives garbage in scoring. Set them with justification:
- **severity 1–5** — impact on the organization's/user's goal: 5 = blocker/systemic risk; 4 = major pain; 3 = noticeable friction; 2 = inconvenience; 1 = cosmetic.
- **valence** — the sign of the attitude in the nugget: `+` (works/values/for), `-` (pain/against/broken), `0` (neutral fact).
Valence is needed for tension detection: the same cluster with `+` for one role and `-` for another = TENSION.

## S6 — Clustering (affinity, done by the model)
Group nuggets by semantic themes, assign each a `cluster`. Rules:
- **Count different interviews, not quotes.** One person who repeated a thought three times is not a pattern.
- Don't merge opposing positions into one cluster — if roles diverge, that's a TENSION (more valuable than consensus), mark it with valence.
- A cluster is not "a theme in general" but a specific regularity.

## S6.5 — Accounting for reliability (script, not by eye)
`python scripts/score_insights.py nuggets.json --k 3`
Computes per cluster: distinct interviews, triangulation (≥k different interviews with a verified quote), frequency×criticality, tension, status:
- **insight** — triangulated (≥k sources) → can be called a pattern.
- **watchlist** — rare but critical (severity≥4) OR cross-role tension → don't bury.
- **weak** — a single source, low criticality → anecdote, not a pattern.
If N interviews is small (<k) — be honest: there will be no patterns, only watchlist. Don't pass off watchlist as an insight.

## S7 — Insight cards (the model builds these from the clusters that passed)
Only for `insight` and `watchlist`. A counter-evidence pass is mandatory.

Card format:
```
### [ID] Insight title — one sentence
Statement: [observation + interpretation + implication — not a retelling]
Holds for: [roles/segments] · NOT for: [where it doesn't work]
Prevalence: X of N interviews (roles: …) · Criticality: high/medium/low
Type: CONSENSUS | TENSION ([role A] vs [role B] — on exactly what)
Evidence (verified only):
  - [Interview, role] «verbatim quote» (Lxx)
  - [Interview, role] «…» (Lxx)
Counter-evidence: [who didn't confirm / what contradicts / where there's silence]
Confidence: high/medium/low  (based on triangulation + grounding)
Implication / recommendation: [what to do; for whom]
```

Card honesty rules:
- No verified quotes from ≥k different interviews → this is NOT an insight, mark it "watchlist / needs more interviews".
- Every card goes through counter-evidence: actively look for who did NOT confirm and who contradicts.
- "Silence" (not everyone asked raised the theme) — is also a signal, record it.
- An insight is always scoped: "for collections staff", not "for employees".

## S7.5 — Synthesis stability (optional, like S3)
Run S6–S7 twice in a fresh context. Insights that didn't reproduce (appeared/disappeared between runs), mark `[⚑ unstable]` — for a human. Clustering is subjective, like eNPS.

## Ranking the output
Sort: first `insight` by (frequency×criticality), then `watchlist` (including tensions and rare-but-critical), then don't show `weak` in the main report (move it to the "raw nuggets" appendix).

## S8 — Longitudinal / panel analysis (the same person, N waves)

A separate axis on top of S5–S7, not a replacement: applies when there are **≥2 mappings of the SAME
person**, taken at different times (wave 1, wave 2, …) using the same lens. The task is not "reconcile
different people into a pattern" (that's S5–S7), but to capture **how one person's position changed over
time**.

### When to apply
- A repeat interview with the same employee/customer/expert months apart (e.g. before and after a change,
  or a quarterly pulse survey of the same panel of respondents).
- Don't confuse this with S3 (reliability pass) — there N runs of the AI go over ONE AND THE SAME transcript
  at a single point in time; here N TRANSCRIPTS of one person exist at DIFFERENT points in time.

### Schema (`panel.json`, a list keyed by person)
```json
{"person_id":"p1", "role":"operations",
 "waves":[
   {"wave":1, "date":"2026-02-01", "cell":"A5", "label":"Promoter", "quote":"...", "line":40, "verified":true},
   {"wave":2, "date":"2026-06-01", "cell":"A5", "label":"Neutral",  "quote":"...", "line":22, "verified":true}
 ]}
```
- `person_id` — a stable identifier for the person across waves (not their name in the open, if anonymization is needed).
- Comparison is done PER CELL (the same lens cell across different waves), not interview-by-interview as a whole.

### Steps
1. **Match cells across waves** — for each cell of Layer 2 (analytical, unstable) belonging to a person: value in wave N vs wave N+1.
2. **Classify the shift**:
   - **STABLE** — the value didn't change between waves.
   - **SHIFT** — it changed; pull a quote from BOTH waves showing the difference, and (if available) the reason for the shift in the respondent's own words from wave N+1 ("what's changed since last time").
   - **NOISE vs REAL SHIFT** — if a cell is unstable even WITHIN a single wave (S3-flagged), don't conclude there's a shift between waves until the S3 pass has been run on both waves separately — otherwise you'll mistake method variance for real change.
3. **Panel-level aggregation (if ≥3 people each have ≥2 waves)** — count how many people shifted in the same direction on the same cell; this is a separate, stronger signal than a single person's shift.
4. **Don't confuse a trend with regression to the mean** — a single sharp outlier in wave 1 (e.g. right after an incident) followed by a "calmer" value in wave 2 may not be a real change in position but a natural regression; flag this as an alternative hypothesis, don't silently discard it.

### Output — panel card
```
### [Person ID / role] Cell [X]: wave 1 → wave N
Wave 1 (date): [label] — «quote» (Lxx)
Wave N (date): [label] — «quote» (Lxx)
Classification: STABLE / SHIFT / UNDETERMINED (noise indistinguishable from shift)
Reason for shift (in the respondent's own words, if asked): […]
Alternative hypothesis: [regression to the mean / external event / method artifact]
```

### Limitation
Panel analysis on latent cells (eNPS, forecast, recognition) is doubly unreliable — they're unstable even
within a single wave (see S3), and comparing two unstable points can produce a false "shift". Don't conclude
a position has changed based on a single latent cell without an S3 pass on EACH wave.

## Sources
- Guest, G., Bunce, A. & Johnson, L. — *How Many Interviews Are Enough? An Experiment with Data Saturation and Variability* (Field Methods, 2006) — the empirical basis for the `k` triangulation threshold and the "n<k → watchlist, not insight" rule.
- Braun, V. & Clarke, V. — *Using Thematic Analysis in Psychology* (Qualitative Research in Psychology, 2006) — bottom-up theme clustering from atomic codes (nuggets), not top-down summarization.
- Sharon, T. — *It's Our Research: Getting Stakeholder Buy-in for User Experience Research Projects* (Morgan Kaufmann, 2012) and the "atomic research" / Polaris repository practice she popularized — tagging insights at synthesis time and distinguishing insight from observation.
- Miles, M. B., Huberman, A. M. & Saldaña, J. — *Qualitative Data Analysis: A Methods Sourcebook* (SAGE, 4th ed., 2020) — cross-case synthesis and the discipline of counting distinct sources, not repeated mentions.
- Nielsen, J. — *Why You Only Need to Test with 5 Users* (Nielsen Norman Group, 2000) — the small-n honesty this skill borrows for stating when a pattern is a pilot, not a measurement.

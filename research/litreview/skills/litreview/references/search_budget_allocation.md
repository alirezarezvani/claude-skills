# Search Budget Allocation — Quick / Standard / Deep + Cross-Search Intelligence

This reference answers exactly one decision: **how does litreview spend its search budget across the 5/10/20 depth tiers, and what makes the cross-search intelligence layer add value beyond per-query results?**

Pair with `scripts/cross_search_aggregator.py` for the deterministic implementation.

## The Core Constraint

Consensus has a **1 query/second rate limit**. NEVER parallelize. Sequential execution is the only mode that doesn't break the rate limit. This is the same rule pulse uses for Reddit/HN/Web — research-pack convention.

Plus a **plan-tier cap**: free tier returns ~10 results per query; Pro returns ~20. Detected at first search response.

The combination produces hard budget ceilings:

| Tier | Plan | Theoretical max papers |
|---|---|---|
| Quick scan (5 q) | Free | 50 |
| Quick scan (5 q) | Pro | 100 |
| Standard (10 q) | Free | 100 |
| Standard (10 q) | Pro | 200 |
| Deep dive (20 q) | Free | 200 |
| Deep dive (20 q) | Pro | 400 |

These are *theoretical* — deduplication reduces the actual unique paper count by 30-50% in practice.

## Why Three Tiers (Not One Adaptive Budget)

Adaptive budgeting (run more searches if early results are thin) sounds smart but:

1. **User can't predict run time.** A 5-search budget runs in ~5s; a 20-search adaptive could run 10-30s.
2. **Sunk-cost bias kicks in.** Once 10 searches run, "let's do 5 more" is hard to resist even if results aren't worth it.
3. **Cross-search intelligence works best at fixed N.** Repeat-hit and recurring-author signals stabilize at known sample sizes.

Fixed tiers with explicit allocations beat adaptive budgets for research-orientation tasks.

## Quick Scan (5 searches)

Budget allocation:
- **5 sub-area searches** (one per sub-area from Phase 2)
- Skip era-gated searches
- Skip review-specific searches
- Skip follow-ups

Use when:
- User wants a fast orientation (~30s with 1 q/sec)
- Topic is well-known to user; they just need pointers
- Plan tier is free + topic is reasonably narrow

**Note in audit:** "Quick scan tier — review articles + era-gated comparisons omitted. Bibliography may be thin on foundational older work."

## Standard Review (10 searches)

Budget allocation:
- **5 sub-area searches** (one per sub-area)
- **2 review article searches** (top 2 sub-areas):
  - `"systematic review [topic]"` AND `"meta-analysis [topic]"`
- **2 era-gated searches** (most important sub-area):
  - `year_max: 2015` → reveals terminology evolution
  - `year_min: 2021` → captures current frontier
- **1 follow-up** on highest-cited paper:
  - Use its key terms + `year_min: <publication_year + 1>`
  - Surfaces papers that built on this work

Use when (default tier):
- User has some familiarity but wants depth
- Plan tier allows reasonable coverage
- Time budget is 1-2 minutes total

## Deep Dive (20 searches)

Budget allocation:
- **5 sub-area searches**
- **5 review article searches** (one per sub-area)
- **4 era-gated searches** (top 2 sub-areas, old + new each):
  - Sub-area A: `year_max: 2015` + `year_min: 2021`
  - Sub-area B: `year_max: 2015` + `year_min: 2021`
- **3 follow-ups on top 3 highest-cited papers** (their terms + `year_min`)
- **3 spare for emerging threads** — surprising findings from earlier searches worth chasing

Use when:
- Topic is genuinely new to user
- Comprehensive orientation is the goal
- Plan tier is Pro (free tier deep-dive is bottlenecked at ~200 papers)

## Cross-Search Intelligence

Three trackers across ALL Phase 3 search results. Run after Phase 3 completes via `scripts/cross_search_aggregator.py --session NAME`.

### Tracker 1: Repeat-Hit Papers (foundational signal)

A paper appearing in **3+ sub-area searches** is signal that it's foundational — multiple sub-fields cite it, suggesting cross-cutting importance.

Use repeat-hits to populate "Start Here" DOCX section:
- Repeat-hit + high citation → priority foundational paper
- Repeat-hit + recent → likely emerging classic
- Repeat-hit but few citations → niche but cross-cutting

### Tracker 2: Recurring Authors (dominant research group signal)

Same author appearing across **multiple sub-area searches** = research group dominant in this area.

Top 3-5 most-frequent authors → "Key Research Groups" DOCX section.

Pattern:
- 5+ search appearances → dominant group (cite representative paper)
- 3-4 appearances → significant but not dominant
- 1-2 appearances → not a "group" signal; may still be high-impact individual

Note: a single highly-cited paper isn't a "group" signal — the recurrence across multiple sub-areas matters.

### Tracker 3: Citation-Per-Year (seminal-work heuristic)

Raw citation count is biased toward older papers (more time to accumulate citations). Citations-per-year normalizes:

- Paper A: 2008, 150 citations → 9.4 cites/year
- Paper B: 2023, 150 citations → 50 cites/year

Paper B is much more seminal in current discourse despite equal absolute citation count.

Citation-per-year ranking → "Start Here" priority ordering.

## Why Cross-Search Intelligence Matters

Per-query results show "papers about this sub-area". Cross-search intelligence shows "patterns across the whole field":

- Repeat-hits reveal foundational structure
- Recurring authors reveal who's doing the work
- Citation-per-year reveals what's currently shaping discourse

A literature review WITHOUT cross-search intelligence is just a list of papers. WITH it, the review surfaces the *structure* of the field.

## Sequential Execution Discipline

Each Consensus call must wait for the prior response. NEVER parallelize:

```
search_1 → wait response → record → 1 second pause → search_2 → ...
```

If parallel: rate limit triggers 429, error counter increments, after 3 consecutive failures → stop.

`scripts/citation_tracker.py --action record_search` enforces the timestamp gap (rejects calls within 1s of prior).

## Plan-Tier Detection

After search 1, parse the response:

| Signal | Tier |
|---|---|
| "Showing top 10" / "upgrade for more" | Free (10/search cap) |
| 20 papers returned | Pro (20/search cap) |
| Auth-failure response | API key missing or invalid |

Surface tier at checkpoint:

> Detected free tier (~10 results per search). Calibrating budget:
>   Quick scan: 5 × 10 = ~50 papers
>   Standard: 10 × 10 = ~100 papers
>   Deep dive: 20 × 10 = ~200 papers
> If you want deeper coverage, Consensus Pro unlocks 20/search.

User chooses depth after seeing the constraint.

## Anti-Patterns

- **Parallelizing searches** — triggers rate limit; data loss
- **Adaptive "just one more" extensions** — bias-prone; commit to tier upfront
- **Skipping era-gated searches in standard/deep tiers** — misses terminology shifts
- **Skipping cross-search aggregation** — reduces review to a paper list
- **Hardcoding plan tier** — detect at runtime; don't assume free/Pro
- **Reporting raw citation count without per-year** — over-weights older papers
- **Counting repeat-hits at threshold 2** — too noisy; 3 is the minimum signal

## Operational Checklist

- [ ] Plan tier detected from search 1 response
- [ ] Theoretical ceiling reported at checkpoint
- [ ] Search budget allocated per tier (5/10/20)
- [ ] Era-gated searches included in standard/deep
- [ ] Follow-ups on highest-cited papers included
- [ ] 1 second wait between each Consensus call (timestamp-enforced)
- [ ] All search results passed through `cross_search_aggregator.py` after Phase 3
- [ ] Repeat-hit threshold = 3 sub-areas (not 2)
- [ ] Citation-per-year computed (not raw citation count)

## Citations (7 sources)

1. **Consensus.app documentation — consensus.app/help.** Authoritative source for plan-tier caps (free: 10/search, Pro: 20/search) and 1 q/sec rate limit. The skill detects from response rather than hardcoding because documented values evolve.

2. **Higgins, J. P. T. & Green, S. (eds.), *Cochrane Handbook for Systematic Reviews of Interventions* (Wiley, 2019).** Chapter 4 on search strategy. Source for the era-gated + review-specific + follow-up search categories. The 5/10/20 tier structure is litreview's compression of Cochrane's exhaustive-search methodology.

3. **Greenhalgh, T. & Peacock, R., "Effectiveness and efficiency of search methods in systematic reviews" — *BMJ* 331, 2005, pp. 1064-1065.** Empirical analysis of how many searches are "enough" to surface foundational papers. Source for the diminishing-returns curve that justifies fixed-tier budgets vs adaptive.

4. **Page, M. J. et al., *PRISMA 2020 Statement* — *BMJ* 372, 2021.** Reporting standard for search audit logs. Source for the audit-log DOCX section's required content (search #, query, filters, results returned).

5. **Sandelowski, M. & Barroso, J., *Handbook for Synthesizing Qualitative Research* (Springer, 2007).** Source for cross-search intelligence patterns in qualitative reviews — repeat-hits and recurring-authors are documented signals in narrative synthesis literature.

6. **Lawani, S. M., "Bibliometrics: Its theoretical foundations, methods and applications" — *Libri* 31, 1981.** Foundational bibliometrics paper. Source for the citations-per-year normalization (Lawani's Garfield-style impact normalization). The skill's citation-per-year heuristic is the simplest form of bibliometric normalization.

7. **AWS Architecture Blog — Mike Cohen, "Exponential Backoff and Jitter" (2015) + Marc Brooker, "Timeouts, retries, and backoff with jitter" (Builders' Library, 2019).** Source for the retry-once-after-3s pattern (research-pack convention). Justifies aggressive failure-detection (3 consecutive → stop) over deep retry loops for research workflows.

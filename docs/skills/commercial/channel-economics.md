---
title: "channel-economics — Claude Code Plugin & Agent Skill"
description: "Use when reviewing or rebalancing direct vs. partner-led channel economics — computing fully-loaded cost-to-serve per channel, channel ROI with cash. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# channel-economics

<div class="page-meta" markdown>
<span class="meta-badge">:material-handshake-outline: Commercial</span>
<span class="meta-badge">:material-identifier: `channel-economics`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commercial/skills/channel-economics/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install commercial-skills</code>
</div>


## Purpose

Help Head of Commercial / RevOps / VP Sales answer three questions at the quarterly channel review:

1. **What does each channel actually cost to serve, fully loaded?** (direct headcount, channel manager attribution, partner discount, MDF, enablement time, support load, allocated overhead)
2. **What is the ROI of each channel under three lenses?** (cash ROI year-1, LTV-adjusted ROI, marginal ROI — next dollar of investment)
3. **What is the optimal channel mix subject to our strategic constraints?** (minimum direct floor, maximum partner concentration ceiling, sensitivity to CAC shifts)

The skill emits **per-channel verdicts** (DOUBLE-DOWN / MAINTAIN / DEFUND / EXIT), a **sensitivity-tested mix recommendation**, and **the diminishing-returns inflection point**. It does not pick the strategy — humans do, with the numbers loaded honestly for the first time.

## When to use

- Quarterly channel review: pipeline is 60/40 or 50/50 direct vs partner and you don't actually know which one is profitable
- Considering hiring a channel manager — need to know if the channel can clear the loaded-cost bar
- Partner program ROI question from the board ("we spent $X on MDF — what did we get?")
- A segment is over-indexed to one channel and you suspect mix dogma is blocking the other
- About to expand into a new region and need to decide direct-first vs partner-first
- M&A diligence: target company claims "partner-led at 70% gross margin" — need to validate after loading

**Do not use for:**
- Designing partner tiers, joint GTM motion, revshare splits → `partnerships-architect`
- SDR-to-AE routing, lead scoring, MQL definitions → `business-growth/revenue-operations`
- Strategic CRO decisions ("should we hire a VP Sales?", comp plan design) → `c-level-advisor/cro-advisor`
- Quarterly close, GAAP revenue recognition, channel-level P&L for historical reporting → `finance/financial-analysis`
- Per-deal discount approval → `deal-desk`
- Pricing model design → `pricing-strategist`

## Workflow

### Step 1 — Intake channel data

Fill `assets/channel_data_template.md` (≈ 20 min). Capture per channel: deal count TTM, ARR TTM, avg deal size, gross margin %, CAC, sales-cycle days, retention rate, expansion rate, partner discount %, all attributable costs (SDR / AE / SE / channel manager / CS / support / marketing / partner MDF / tooling / overhead allocation %).

The template surfaces the costs teams most often forget: partner enablement time, certification investment, channel-conflict resolution overhead, channel-manager headcount cost.

### Step 2 — Compute cost-to-serve per channel

Run `scripts/cost_to_serve_calculator.py --input channel.json --output markdown`.

Output: fully-loaded cost-to-serve **per deal** AND **per dollar of ARR**, with direct costs broken out from allocated overhead, and a "true gross margin" line after channel-specific load. Flags double-counting and surfaces hidden costs.

Run once per channel. The "true gross margin" line is the input the next two scripts care about.

### Step 3 — Compute ROI per channel under three lenses

Run `scripts/channel_roi_analyzer.py --input roi.json --profile saas --output markdown`.

Output: per channel, three ROI numbers (Cash year-1, LTV-adjusted, Marginal), the diminishing-returns inflection point, and a verdict: DOUBLE-DOWN / MAINTAIN / DEFUND / EXIT.

Verdict logic is deterministic and surfaced in the report. Humans can override; the skill won't.

### Step 4 — Optimize channel mix subject to constraints

Run `scripts/channel_mix_optimizer.py --input mix.json --profile saas --output markdown`.

Output: recommended mix that maximizes effective ARR subject to constraints (min direct %, max partner concentration), plus a sensitivity table (what if direct CAC rises 20%? what if partner discount widens 5 points?).

### Step 5 — Decide

Take the three reports into the quarterly channel review. The skill recommends; the human commits.

## Scripts

- `scripts/cost_to_serve_calculator.py` — fully-loaded cost-to-serve per deal AND per $ ARR, with hidden-cost surfacing
- `scripts/channel_roi_analyzer.py` — 3-lens ROI (Cash / LTV / Marginal) with verdicts and diminishing-returns inflection
- `scripts/channel_mix_optimizer.py` — constrained mix optimizer with sensitivity scenarios

All scripts: stdlib only. `--help`, `--sample`, `--input`, `--output` work on all three. Industry tuning via `--profile {saas,api,enterprise-software,marketplace,hardware}` on the two analyzers.

## References

- `references/channel_economics_canon.md` — Skok, Bessemer State of the Cloud, Tunguz, Pacific Crest / KeyBanc SaaS Survey, Ramanujam, Jay McBain (Canalys)
- `references/cost_to_serve_canon.md` — Kaplan & Cooper (ABC), Horngren, Jeremy Hope, IBM CTS case studies, McKinsey, Gartner, BCG
- `references/channel_anti_patterns.md` — Forrester, Tunguz, Hessling, HBR, SiriusDecisions, MIT Sloan, Gartner

## Assumptions

- Channel economics is a **forward-looking** question. Historical channel P&L is finance's job; this skill loads forward economics for a decision.
- "Channel" means a coherent go-to-market motion (direct outbound, partner-led, marketplace, reseller, OEM). It does not mean a marketing source.
- Cost-to-serve requires **honest overhead allocation**. The script validates that overhead % is consistent across channels — false partner-margin lift from inconsistent allocation is the #1 anti-pattern.
- LTV inputs (retention, expansion) are per-channel, not pooled. Partner-sourced customers often retain differently than direct-sourced — this difference is usually the largest economic variable and the most ignored.
- Industry profiles (`--profile`) tune defaults for benchmarks (e.g., SaaS direct CAC payback target ~12mo, enterprise ~18mo) — they don't override your numbers.
- This is a decision-support skill. Output is verdicts and a recommended mix, never an automatic resource reallocation.

## Anti-patterns

- **Treating "influenced" deals as "sourced" deals.** A partner that touched a deal your AE already had is not channel-sourced revenue. Loading this as partner revenue inflates partner ROI and inflates direct CAC simultaneously.
- **Inconsistent overhead allocation.** Allocating 25% overhead to direct deals and 5% to partner deals because "the partner handles the overhead" is false. The partner manager, partner program, MDF, certification, and conflict-resolution all live in your P&L.
- **Ignoring enablement time as a cost.** Every hour your AE spends co-selling with a partner is a direct cost charged to the partner channel — most teams forget to load it.
- **MDF without ROI tracking.** Market Development Funds disbursed without an attributable pipeline ROI are just a partner-discount extension. The skill flags MDF with no return.
- **Channel-mix dogma.** "We're a partner-first company" / "we don't sell direct" blocks profitable segments. Mix should follow the math, not the slogan.
- **Computing channel ROI without retention differential.** If partner-sourced customers churn 5 points higher than direct, ignoring it overstates partner LTV by 30-50%. Per-channel retention is mandatory input.
- **No cost-attribution for channel-manager headcount.** A $200k channel manager managing $4M of partner ARR is $50 of channel-manager cost per $1k ARR — material to the verdict.
- **Confusing this skill with partnerships-architect.** That skill designs the partner program. This skill tells you whether the program pays for itself.

## Distinct from

- **commercial/partnerships-architect** — partner tier design, joint GTM motion, revshare splits, partner enablement. Partner program *structure*, not partner program *economics*. This skill consumes the program structure as input and emits the economic verdict.
- **business-growth/revenue-operations** — lead routing, SDR motion, MQL definition, pipeline operations. RevOps owns the funnel mechanics; this skill loads the channel-level economic outcome.
- **c-level-advisor/cro-advisor** — strategic CRO judgment: when to hire a VP Sales, comp plan philosophy, territory design, multi-year revenue strategy. CRO advisor consumes channel-economics output as one input among many.
- **finance/financial-analysis** — close-and-report on historical channel P&L per GAAP. This skill is forward-looking decision support; finance is historical record. Different time horizon, different audience, different output.
- **commercial/deal-desk** — per-deal discount approval. Operates daily; this skill operates quarterly.
- **commercial/pricing-strategist** — pricing model and tier design. Pricing is input; channel economics is what happens at that pricing across channels.

## Forcing-question library (Matt Pocock grill discipline)

Walked one at a time by `/cs:grill-commercial` or the orchestrator. Recommended answer + canon citation per question. Never bundled.

1. **"What's your fully-loaded cost-to-serve per channel — including channel-manager headcount, MDF, partner enablement time, and overhead allocation?"**
   Recommended: load all four. Most teams load partner discount but forget the channel-manager headcount and the enablement time, inflating partner margin by 8-15 points.
   Canon: Kaplan & Cooper (HBR 1988) — *Measure Costs Right: Make the Right Decisions*. Activity-Based Costing was invented precisely because channel costs hide in overhead and distort margin comparisons.

2. **"What is the retention differential between direct-sourced and partner-sourced customers?"**
   Recommended: instrument per-channel retention BEFORE running channel ROI. A 5-point retention gap moves LTV by 30-50%.
   Canon: David Skok (*For Entrepreneurs* — SaaS Metrics 2.0). LTV = (ARPA × Gross Margin) / Churn. Channel-blind churn is the most common source of false channel ROI.

3. **"What share of 'channel-sourced' pipeline did your team actually originate?"**
   Recommended: if your AE already had the account, it's not channel-sourced — it's channel-influenced. Influence and source are different economic lines.
   Canon: SiriusDecisions / Forrester channel attribution research — confused source vs. influence is the #1 reason partner ROI is overstated industry-wide.

4. **"What is the marginal ROI of the next dollar invested in partner program vs. direct sales?"**
   Recommended: compute the diminishing-returns curve on both. Average ROI hides the fact that the next dollar might earn 0.3x while the average earns 2.1x.
   Canon: Tomasz Tunguz (*Tomasz Tunguz blog* — channel CAC analyses). Average ROI is a vanity metric; marginal ROI drives investment decisions.

5. **"What's your MDF-to-attributable-pipeline ratio in the last 4 quarters?"**
   Recommended: < 5:1 (every $1 of MDF should generate ≥ $5 of attributable pipeline within 2 quarters). Anything looser is partner-discount theatre.
   Canon: Jay McBain (Canalys) — *State of the Channel* research. MDF without attribution discipline is the most expensive form of channel subsidy.

6. **"Is your channel-mix dogma blocking a profitable segment?"**
   Recommended: surface the dogma ("we're partner-first", "we don't sell direct in SMB") explicitly. Mix should follow the segment math.
   Canon: MIT Sloan Management Review — *When Channel Conflict Means Growth*. Dogmatic single-channel strategies forfeit 15-25% of TAM in mid-market specifically.

7. **"What overhead-allocation methodology are you applying — and is it consistent across direct and partner?"**
   Recommended: same methodology, same denominator, both channels. Inconsistent allocation is the silent killer of channel-economics analysis.
   Canon: Charles Horngren (*Cost Accounting: A Managerial Emphasis*) — allocation consistency is the precondition for cross-segment margin comparison. Without it, every conclusion is contaminated.

Walk depth-first. Lock 1-3 before opening 4-7. After all 7 are answered, invoke `cost_to_serve_calculator.py` → `channel_roi_analyzer.py` → `channel_mix_optimizer.py` in sequence.

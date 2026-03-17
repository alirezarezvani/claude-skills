---
title: "A/B Test Setup — Agent Skill for Marketing"
description: "When the user wants to plan, design, or implement an A/B test or experiment. Also use when the user mentions 'A/B test,' 'split test,' 'experiment,'. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# A/B Test Setup

<div class="page-meta" markdown>
<span class="meta-badge">:material-bullhorn-outline: Marketing</span>
<span class="meta-badge">:material-identifier: `ab-test-setup`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/ab-test-setup/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install marketing-skills</code>
</div>


You are an expert in experimentation and A/B testing. Your goal is to help design tests that produce statistically valid, actionable results.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before designing a test, understand:

1. **Test Context** - What are you trying to improve? What change are you considering?
2. **Current State** - Baseline conversion rate? Current traffic volume?
3. **Constraints** - Technical complexity? Timeline? Tools available?

---

## Core Principles

### 1. Start with a Hypothesis
- Not just "let's see what happens"
- Specific prediction of outcome
- Based on reasoning or data

### 2. Test One Thing
- Single variable per test
- Otherwise you don't know what worked

### 3. Statistical Rigor
- Pre-determine sample size
- Don't peek and stop early
- Commit to the methodology

### 4. Measure What Matters
- Primary metric tied to business value
- Secondary metrics for context
- Guardrail metrics to prevent harm

---

## Hypothesis Framework

### Structure

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

### Example

**Weak**: "Changing the button color might increase clicks."

**Strong**: "Because users report difficulty finding the CTA (per heatmaps and feedback), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

---

## Test Types

| Type | Description | Traffic Needed |
|------|-------------|----------------|
| A/B | Two versions, single change | Moderate |
| A/B/n | Multiple variants | Higher |
| MVT | Multiple changes in combinations | Very high |
| Split URL | Different URLs for variants | Moderate |

---

## Sample Size

### Quick Reference

| Baseline | 10% Lift | 20% Lift | 50% Lift |
|----------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

**Calculators:**
- [Evan Miller's](https://www.evanmiller.org/ab-testing/sample-size.html)
- [Optimizely's](https://www.optimizely.com/sample-size-calculator/)

**For detailed sample size tables and duration calculations**: See [references/sample-size-guide.md](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/ab-test-setup/references/sample-size-guide.md)

---

## Metrics Selection

### Primary Metric
- Single metric that matters most
- Directly tied to hypothesis
- What you'll use to call the test

### Secondary Metrics
- Support primary metric interpretation
- Explain why/how the change worked

### Guardrail Metrics
- Things that shouldn't get worse
- Stop test if significantly negative

### Example: Pricing Page Test
- **Primary**: Plan selection rate
- **Secondary**: Time on page, plan distribution
- **Guardrail**: Support tickets, refund rate

---

## Designing Variants

### What to Vary

| Category | Examples |
|----------|----------|
| Headlines/Copy | Message angle, value prop, specificity, tone |
| Visual Design | Layout, color, images, hierarchy |
| CTA | Button copy, size, placement, number |
| Content | Information included, order, amount, social proof |

### Best Practices
- Single, meaningful change
- Bold enough to make a difference
- True to the hypothesis

---

## Traffic Allocation

| Approach | Split | When to Use |
|----------|-------|-------------|
| Standard | 50/50 | Default for A/B |
| Conservative | 90/10, 80/20 | Limit risk of bad variant |
| Ramping | Start small, increase | Technical risk mitigation |

**Considerations:**
- Consistency: Users see same variant on return
- Balanced exposure across time of day/week

---

## Implementation

### Client-Side
- JavaScript modifies page after load
- Quick to implement, can cause flicker
- Tools: PostHog, Optimizely, VWO

### Server-Side
- Variant determined before render
- No flicker, requires dev work
- Tools: PostHog, LaunchDarkly, Split

---

## Running the Test

### Pre-Launch Checklist
- [ ] Hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Variants implemented correctly
- [ ] Tracking verified
- [ ] QA completed on all variants

### During the Test

**DO:**
- Monitor for technical issues
- Check segment quality
- Document external factors

**DON'T:**
- Peek at results and stop early
- Make changes to variants
- Add traffic from new sources

### The Peeking Problem
Looking at results before reaching sample size and stopping early leads to false positives and wrong decisions. Pre-commit to sample size and trust the process.

---

## Analyzing Results

### Statistical Significance
- 95% confidence = p-value < 0.05
- Means <5% chance result is random
- Not a guarantee—just a threshold

### Analysis Checklist

1. **Reach sample size?** If not, result is preliminary
2. **Statistically significant?** Check confidence intervals
3. **Effect size meaningful?** Compare to MDE, project impact
4. **Secondary metrics consistent?** Support the primary?
5. **Guardrail concerns?** Anything get worse?
6. **Segment differences?** Mobile vs. desktop? New vs. returning?

### Interpreting Results

| Result | Conclusion |
|--------|------------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Need more traffic or bolder test |
| Mixed signals | Dig deeper, maybe segment |

---

## Documentation

Document every test with:
- Hypothesis
- Variants (with screenshots)
- Results (sample, metrics, significance)
- Decision and learnings

**For templates**: See [references/test-templates.md](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/ab-test-setup/references/test-templates.md)

---

## Common Mistakes

### Test Design
- Testing too small a change (undetectable)
- Testing too many things (can't isolate)
- No clear hypothesis

### Execution
- Stopping early
- Changing things mid-test
- Not checking implementation

### Analysis
- Ignoring confidence intervals
- Cherry-picking segments
- Over-interpreting inconclusive results

---

## Task-Specific Questions

1. What's your current conversion rate?
2. How much traffic does this page get?
3. What change are you considering and why?
4. What's the smallest improvement worth detecting?
5. What tools do you have for testing?
6. Have you tested this area before?

---

## Proactive Triggers

Proactively offer A/B test design when:

1. **Conversion rate mentioned** — User shares a conversion rate and asks how to improve it; suggest designing a test rather than guessing at solutions.
2. **Copy or design decision is unclear** — When two variants of a headline, CTA, or layout are being debated, propose testing instead of opinionating.
3. **Campaign underperformance** — User reports a landing page or email performing below expectations; offer a structured test plan.
4. **Pricing page discussion** — Any mention of pricing page changes should trigger an offer to design a pricing test with guardrail metrics.
5. **Post-launch review** — After a feature or campaign goes live, propose follow-up experiments to optimize the result.

---

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Experiment Brief | Markdown doc | Hypothesis, variants, metrics, sample size, duration, owner |
| Sample Size Calculator Input | Table | Baseline rate, MDE, confidence level, power |
| Pre-Launch QA Checklist | Checklist | Implementation, tracking, variant rendering verification |
| Results Analysis Report | Markdown doc | Statistical significance, effect size, segment breakdown, decision |
| Test Backlog | Prioritized list | Ranked experiments by expected impact and feasibility |

---

## Communication

All outputs should meet the quality standard: clear hypothesis, pre-registered metrics, and documented decisions. Avoid presenting inconclusive results as wins. Every test should produce a learning, even if the variant loses. Reference `marketing-context` for product and audience framing before designing experiments.

---

## Related Skills

- **page-cro** — USE when you need ideas for *what* to test; NOT when you already have a hypothesis and just need test design.
- **analytics-tracking** — USE to set up measurement infrastructure before running tests; NOT as a substitute for defining primary metrics upfront.
- **campaign-analytics** — USE after tests conclude to fold results into broader campaign attribution; NOT during the test itself.
- **pricing-strategy** — USE when test results affect pricing decisions; NOT to replace a controlled test with pure strategic reasoning.
- **marketing-context** — USE as foundation before any test design to ensure hypotheses align with ICP and positioning; always load first.

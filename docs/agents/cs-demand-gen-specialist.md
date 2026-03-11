---
title: "Demand Generation Specialist Agent"
description: "Demand Generation Specialist Agent - Claude Code agent for Marketing."
---

# Demand Generation Specialist Agent

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">:material-bullhorn-outline: Marketing</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agents/marketing/cs-demand-gen-specialist.md">Source</a></span>
</div>


## Purpose

The cs-demand-gen-specialist agent is a specialized marketing agent focused on demand generation, lead acquisition, and conversion optimization. This agent orchestrates the marketing-demand-acquisition skill package to help teams build scalable customer acquisition systems, optimize conversion funnels, and maximize marketing ROI across channels.

This agent is designed for growth marketers, demand generation managers, and founders who need to generate qualified leads and convert them efficiently. By leveraging acquisition analytics, funnel optimization frameworks, and channel performance analysis, the agent enables data-driven decisions that improve customer acquisition cost (CAC) and lifetime value (LTV) ratios.

The cs-demand-gen-specialist agent bridges the gap between marketing strategy and measurable business outcomes, providing actionable insights on channel performance, conversion bottlenecks, and campaign effectiveness. It focuses on the entire demand generation funnel from awareness to qualified lead.

## Skill Integration

**Skill Location:** [`marketing-skill/marketing-demand-acquisition`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition)

### Python Tools

1. **CAC Calculator**
   - **Purpose:** Calculates Customer Acquisition Cost (CAC) across channels and campaigns
   - **Path:** [`scripts/calculate_cac.py`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py)
   - **Usage:** `python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py campaign-spend.csv customer-data.csv`
   - **Features:** CAC calculation by channel, LTV:CAC ratio, payback period analysis, ROI metrics
   - **Use Cases:** Budget allocation, channel performance evaluation, campaign ROI analysis

**Note:** Additional tools (demand_gen_analyzer.py, funnel_optimizer.py) planned for future releases per marketing roadmap.

### Knowledge Bases

1. **Attribution Guide**
   - **Location:** [`references/attribution-guide.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/references/attribution-guide.md)
   - **Content:** Marketing attribution models, channel attribution, ROI measurement frameworks
   - **Use Case:** Campaign attribution, channel performance analysis, budget justification

2. **Campaign Templates**
   - **Location:** [`references/campaign-templates.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/references/campaign-templates.md)
   - **Content:** Reusable campaign structures, launch checklists, multi-channel campaign blueprints
   - **Use Case:** Campaign planning, rapid campaign setup, standardized launch processes

3. **HubSpot Workflows**
   - **Location:** [`references/hubspot-workflows.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/references/hubspot-workflows.md)
   - **Content:** HubSpot automation workflows, lead nurturing sequences, CRM integration patterns
   - **Use Case:** Marketing automation, lead scoring, nurture campaign setup

4. **International Playbooks**
   - **Location:** [`references/international-playbooks.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/references/international-playbooks.md)
   - **Content:** International market expansion strategies, localization best practices, regional channel optimization
   - **Use Case:** Global campaign planning, market entry strategy, cross-border demand generation

### Templates

No asset templates currently available — use campaign-templates.md reference for campaign structure guidance.

## Workflows

### Workflow 1: Multi-Channel Acquisition Campaign Launch

**Goal:** Plan and launch demand generation campaign across multiple acquisition channels

**Steps:**
1. **Define Campaign Goals** - Set targets for leads, MQLs, SQLs, conversion rates
2. **Reference Campaign Templates** - Review proven campaign structures and launch checklists
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/campaign-templates.md
   ```
3. **Select Channels** - Choose optimal mix based on target audience, budget, and attribution models
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/attribution-guide.md
   ```
4. **Set Up Automation** - Configure HubSpot workflows for lead nurturing
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/hubspot-workflows.md
   ```
5. **Plan International Reach** - Reference international playbooks if targeting multiple markets
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/international-playbooks.md
   ```
6. **Launch and Monitor** - Deploy campaigns, track metrics, collect data

**Expected Output:** Structured campaign plan with channel strategy, budget allocation, success metrics

**Time Estimate:** 4-6 hours for campaign planning and setup

### Workflow 2: Conversion Funnel Analysis & Optimization

**Goal:** Identify and fix conversion bottlenecks in acquisition funnel

**Steps:**
1. **Export Campaign Data** - Gather metrics from all acquisition channels (GA4, ad platforms, CRM)
2. **Calculate Channel CAC** - Run CAC calculator to analyze cost efficiency
   ```bash
   python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py campaign-spend.csv conversions.csv
   ```
3. **Map Conversion Funnel** - Visualize drop-off points using campaign templates as structure guide
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/campaign-templates.md
   ```
4. **Identify Bottlenecks** - Analyze conversion rates at each funnel stage:
   - Awareness → Interest (CTR)
   - Interest → Consideration (landing page conversion)
   - Consideration → Intent (form completion)
   - Intent → Purchase/MQL (qualification rate)
5. **Reference Attribution Guide** - Review attribution models to identify problem areas
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/attribution-guide.md
   ```
6. **Implement A/B Tests** - Test hypotheses for improvement
7. **Re-calculate CAC Post-Optimization** - Measure cost efficiency improvements
   ```bash
   python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py post-optimization-spend.csv post-optimization-conversions.csv
   ```

**Expected Output:** 15-30% reduction in CAC and improved LTV:CAC ratio

**Time Estimate:** 6-8 hours for analysis and optimization planning

**Example:**
```bash
# Complete CAC analysis workflow
python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py q3-spend.csv q3-conversions.csv > cac-report.txt
cat cac-report.txt
# Review metrics and optimize high-CAC channels
```

### Workflow 3: Channel Performance Benchmarking

**Goal:** Evaluate and compare performance across acquisition channels to optimize budget allocation

**Steps:**
1. **Collect Channel Data** - Export metrics from each acquisition channel:
   - Google Ads (CPC, CTR, conversion rate, CPA)
   - LinkedIn Ads (impressions, clicks, leads, cost per lead)
   - Facebook Ads (reach, engagement, conversions, ROAS)
   - Content Marketing (organic traffic, leads, MQLs)
   - Email Campaigns (open rate, click rate, conversions)
2. **Run CAC Comparison** - Calculate and compare CAC across all channels
   ```bash
   python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py channel-spend.csv channel-conversions.csv
   ```
3. **Reference Attribution Guide** - Understand attribution models and benchmarks for each channel
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/attribution-guide.md
   ```
4. **Calculate Key Metrics:**
   - CAC (Customer Acquisition Cost) by channel
   - LTV:CAC ratio
   - Conversion rate
   - Time to MQL/SQL
5. **Optimize Budget Allocation** - Shift budget to highest-performing channels
6. **Document Learnings** - Create playbook for future campaigns

**Expected Output:** Data-driven budget reallocation plan with projected ROI improvement

**Time Estimate:** 3-4 hours for comprehensive channel analysis

### Workflow 4: Lead Magnet Campaign Development

**Goal:** Create and launch lead magnet campaign to capture high-quality leads

**Steps:**
1. **Define Lead Magnet** - Choose format: ebook, webinar, template, assessment, free trial
2. **Reference Campaign Templates** - Review lead capture and campaign structure best practices
   ```bash
   cat ../../marketing-skill/marketing-demand-acquisition/references/campaign-templates.md
   ```
3. **Create Landing Page** - Design high-converting landing page with:
   - Clear value proposition
   - Compelling CTA
   - Minimal form fields (name, email, company)
   - Social proof (testimonials, logos)
4. **Set Up Campaign Tracking** - Configure analytics and attribution
5. **Launch Multi-Channel Promotion:**
   - Paid social ads (LinkedIn, Facebook)
   - Email to existing list
   - Organic social posts
   - Blog post with CTA
6. **Monitor and Optimize** - Track CAC and conversion metrics
   ```bash
   # Weekly CAC analysis
   python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py lead-magnet-spend.csv lead-magnet-conversions.csv
   ```

**Expected Output:** Lead magnet campaign generating 100-500 leads with 25-40% conversion rate

**Time Estimate:** 8-12 hours for development and launch

## Integration Examples

### Example 1: Automated Campaign Performance Dashboard

```bash
#!/bin/bash
# campaign-dashboard.sh - Daily campaign performance summary

DATE=$(date +%Y-%m-%d)

echo "📊 Demand Gen Dashboard - $DATE"
echo "========================================"

# Calculate yesterday's CAC by channel
python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py \
  daily-spend.csv daily-conversions.csv

echo ""
echo "💰 Budget Status:"
cat budget-tracking.txt

echo ""
echo "🎯 Today's Priorities:"
cat optimization-priorities.txt
```

### Example 2: Weekly Channel Performance Report

```bash
# Generate weekly CAC report for stakeholders
python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py \
  weekly-spend.csv weekly-conversions.csv > weekly-cac-report.txt

# Email to stakeholders
echo "Weekly CAC analysis report attached." | \
  mail -s "Weekly CAC Report" -a weekly-cac-report.txt stakeholders@company.com
```

### Example 3: Real-Time Funnel Monitoring

```bash
# Monitor CAC in real-time (run daily via cron)
CAC_RESULT=$(python ../../marketing-skill/marketing-demand-acquisition/scripts/calculate_cac.py \
  daily-spend.csv daily-conversions.csv | grep "Average CAC" | awk '{print $3}')

CAC_THRESHOLD=50

# Alert if CAC exceeds threshold
if (( $(echo "$CAC_RESULT > $CAC_THRESHOLD" | bc -l) )); then
  echo "🚨 Alert: CAC ($CAC_RESULT) exceeds threshold ($CAC_THRESHOLD)!" | \
    mail -s "CAC Alert" demand-gen-team@company.com
fi
```

## Success Metrics

**Acquisition Metrics:**
- **Lead Volume:** 20-30% month-over-month growth
- **MQL Conversion Rate:** 15-25% of total leads qualify as MQLs
- **CAC (Customer Acquisition Cost):** Decrease by 15-20% with optimization
- **LTV:CAC Ratio:** Maintain 3:1 or higher ratio

**Channel Performance:**
- **Paid Search:** CTR 3-5%, conversion rate 5-10%
- **Paid Social:** CTR 1-2%, CPL (cost per lead) benchmarked by industry
- **Content Marketing:** 30-40% of organic traffic converts to leads
- **Email Campaigns:** Open rate 20-30%, click rate 3-5%, conversion rate 2-5%

**Funnel Optimization:**
- **Landing Page Conversion:** 25-40% conversion rate on optimized pages
- **Form Completion:** 60-80% of visitors who start form complete it
- **Lead Quality:** 40-50% of MQLs convert to SQLs

**Business Impact:**
- **Pipeline Contribution:** Demand gen accounts for 50-70% of sales pipeline
- **Revenue Attribution:** Track $X in closed-won revenue to demand gen campaigns
- **Payback Period:** CAC recovered within 6-12 months

## Related Agents

- [cs-content-creator](cs-content-creator.md) - Content creation for demand gen campaigns
- cs-product-marketing - Product positioning and messaging (planned)
- cs-growth-marketer - Growth hacking and viral acquisition (planned)

## References

- **Skill Documentation:** [../../marketing-skill/marketing-demand-acquisition/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing-demand-acquisition/SKILL.md)
- **Marketing Domain Guide:** [../../marketing-skill/CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/agents/CLAUDE.md)
- **Marketing Roadmap:** [../../marketing-skill/marketing_skills_roadmap.md](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/marketing_skills_roadmap.md)

---

**Last Updated:** November 5, 2025
**Sprint:** sprint-11-05-2025 (Day 2)
**Status:** Production Ready
**Version:** 1.0

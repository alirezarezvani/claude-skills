---
title: "Product Strategist Agent"
description: "Product Strategist Agent - Claude Code agent for Product."
---

# Product Strategist Agent

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">:material-lightbulb-outline: Product</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agents/product/cs-product-strategist.md">Source</a></span>
</div>


## Purpose

The cs-product-strategist agent is a specialized strategic planning agent focused on product vision, OKR cascading, competitive intelligence, and strategy formulation. This agent orchestrates the product-strategist skill alongside competitive-teardown to help product leaders make informed strategic decisions, set meaningful objectives, and navigate competitive landscapes.

This agent is designed for heads of product, senior product managers, VPs of product, and founders who need structured frameworks for translating company vision into actionable product strategy. By combining OKR cascade generation with competitive matrix analysis, the agent ensures product strategy is both aspirational and grounded in market reality.

The cs-product-strategist agent operates at the intersection of business strategy and product execution. It helps leaders articulate product vision, set quarterly goals that cascade from company objectives to team-level key results, analyze competitive positioning, and evaluate when strategic pivots are warranted. Unlike the cs-product-manager agent which focuses on feature-level execution, this agent operates at the portfolio and strategic level.

## Skill Integration

**Primary Skill:** [`product-team/product-strategist`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist)

### All Orchestrated Skills

| # | Skill | Location | Primary Tool |
|---|-------|----------|-------------|
| 1 | Product Strategist | [`product-team/product-strategist`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist) | okr_cascade_generator.py |
| 2 | Competitive Teardown | [`product-team/competitive-teardown`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown) | competitive_matrix_builder.py |
| 3 | Product Manager Toolkit | [`product-team/product-manager-toolkit`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-manager-toolkit) | rice_prioritizer.py |

### Python Tools

1. **OKR Cascade Generator**
   - **Purpose:** Generate cascaded OKRs from company objectives to team-level key results with initiative mapping
   - **Path:** [`scripts/okr_cascade_generator.py`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/scripts/okr_cascade_generator.py)
   - **Usage:** `python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth`
   - **Features:** Multi-level cascade (company > product > team), initiative mapping, scoring framework, tracking cadence
   - **Use Cases:** Quarterly planning, strategic alignment, goal setting, annual planning

2. **Competitive Matrix Builder**
   - **Purpose:** Build competitive analysis matrices, feature comparison grids, and positioning maps
   - **Path:** [`scripts/competitive_matrix_builder.py`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown/scripts/competitive_matrix_builder.py)
   - **Usage:** `python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py competitors.csv`
   - **Features:** Multi-dimensional scoring, weighted comparison, gap analysis, positioning visualization
   - **Use Cases:** Competitive intelligence, market positioning, feature gap analysis, strategic differentiation

3. **RICE Prioritizer**
   - **Purpose:** Strategic initiative prioritization using RICE framework for portfolio-level decisions
   - **Path:** [`scripts/rice_prioritizer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-manager-toolkit/scripts/rice_prioritizer.py)
   - **Usage:** `python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py initiatives.csv --capacity 50`
   - **Features:** Portfolio quadrant analysis (big bets, quick wins), capacity planning, strategic roadmap generation
   - **Use Cases:** Initiative prioritization, resource allocation, strategic portfolio management

### Knowledge Bases

1. **OKR Framework**
   - **Location:** [`references/okr_framework.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/references/okr_framework.md)
   - **Content:** OKR methodology, cascade patterns, scoring guidelines, common pitfalls
   - **Use Case:** OKR education, quarterly planning preparation

2. **Strategy Types**
   - **Location:** [`references/strategy_types.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/references/strategy_types.md)
   - **Content:** Product strategy frameworks, competitive positioning models, growth strategies
   - **Use Case:** Strategy formulation, market analysis, product vision development

3. **Data Collection Guide**
   - **Location:** [`references/data-collection-guide.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown/references/data-collection-guide.md)
   - **Content:** Sources and methods for gathering competitive intelligence ethically
   - **Use Case:** Competitive research planning, data source identification

4. **Scoring Rubric**
   - **Location:** [`references/scoring-rubric.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown/references/scoring-rubric.md)
   - **Content:** Standardized scoring criteria for competitive dimensions (1-10 scale)
   - **Use Case:** Consistent competitor evaluation, bias mitigation

5. **Analysis Templates**
   - **Location:** [`references/analysis-templates.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown/references/analysis-templates.md)
   - **Content:** SWOT, Porter's Five Forces, positioning maps, battle cards, win/loss analysis
   - **Use Case:** Structured competitive analysis, sales enablement

### Templates

1. **OKR Template**
   - **Location:** [`assets/okr_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/assets/okr_template.md)
   - **Use Case:** Quarterly OKR documentation with tracking structure

2. **PRD Template**
   - **Location:** [`assets/prd_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-manager-toolkit/assets/prd_template.md)
   - **Use Case:** Documenting strategic initiatives as formal requirements

## Workflows

### Workflow 1: Quarterly OKR Planning

**Goal:** Set ambitious, aligned quarterly OKRs that cascade from company objectives to product team key results

**Steps:**
1. **Review Company Strategy** - Gather strategic context:
   - Company-level OKRs or annual goals
   - Board priorities and investor expectations
   - Revenue and growth targets
   - Previous quarter's OKR results and learnings

2. **Analyze Market Context** - Understand external factors:
   ```bash
   # Build competitive landscape
   python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py competitors.csv
   ```
   - Review competitive movements from past quarter
   - Identify market trends and opportunities
   - Assess customer feedback themes

3. **Generate OKR Cascade** - Create aligned objectives:
   ```bash
   # Generate OKRs for growth strategy
   python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth
   ```

4. **Define Product Objectives** - Set 2-3 product objectives:
   - Each objective qualitative and inspirational
   - Directly supports company-level objectives
   - Achievable within the quarter with stretch

5. **Set Key Results** - 3-4 measurable KRs per objective:
   - Specific, measurable, with baseline and target
   - Mix of leading and lagging indicators
   - Target 70% achievement (if consistently hitting 100%, not ambitious enough)

6. **Map Initiatives to KRs** - Connect work to outcomes:
   ```bash
   # Prioritize strategic initiatives
   python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py initiatives.csv --capacity 50
   ```

7. **Stakeholder Alignment** - Present and iterate:
   - Review with engineering leads for feasibility
   - Align with marketing/sales for GTM coordination
   - Get executive sign-off on objectives and KRs

8. **Document and Launch** - Use OKR template:
   ```bash
   cat ../../product-team/product-strategist/assets/okr_template.md
   ```

**Expected Output:** Quarterly OKR document with 2-3 objectives, 8-12 key results, mapped initiatives, and stakeholder alignment

**Time Estimate:** 1 week (end of previous quarter)

**Example:**
```bash
# Full quarterly planning flow
echo "Q3 2026 OKR Planning"
echo "===================="

# Step 1: Competitive context
python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py q3-competitors.csv

# Step 2: Generate OKR cascade
python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth

# Step 3: Prioritize initiatives
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py q3-initiatives.csv --capacity 45

# Step 4: Review OKR template
cat ../../product-team/product-strategist/assets/okr_template.md
```

### Workflow 2: Competitive Landscape Review

**Goal:** Conduct a comprehensive competitive analysis to inform product positioning and feature prioritization

**Steps:**
1. **Identify Competitors** - Map the competitive landscape:
   - Direct competitors (same solution, same market)
   - Indirect competitors (different solution, same problem)
   - Potential entrants (adjacent market players)

2. **Gather Data** - Use ethical collection methods:
   ```bash
   cat ../../product-team/competitive-teardown/references/data-collection-guide.md
   ```
   - Public sources: G2, Capterra, pricing pages, changelogs
   - Market reports: Gartner, Forrester, analyst briefings
   - Customer intelligence: Win/loss interviews, churn reasons

3. **Score Competitors** - Apply standardized rubric:
   ```bash
   cat ../../product-team/competitive-teardown/references/scoring-rubric.md
   ```
   - Score across 7 dimensions (UX, features, pricing, integrations, support, performance, security)
   - Use multiple scorers to reduce bias
   - Document evidence for each score

4. **Build Competitive Matrix** - Generate comparison:
   ```bash
   python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py competitors-scored.csv
   ```

5. **Identify Gaps and Opportunities** - Analyze the matrix:
   - Where do we lead? (defend and communicate)
   - Where do we lag? (close gaps or differentiate)
   - White space opportunities (unserved needs)

6. **Create Deliverables** - Use analysis templates:
   ```bash
   cat ../../product-team/competitive-teardown/references/analysis-templates.md
   ```
   - SWOT analysis per major competitor
   - Positioning map (2x2)
   - Battle cards for sales team
   - Feature gap prioritization

**Expected Output:** Competitive analysis report with scoring matrix, positioning map, battle cards, and strategic recommendations

**Time Estimate:** 2-3 weeks for comprehensive analysis (refresh quarterly)

**Example:**
```bash
# Competitive analysis workflow
cat > competitors.csv << 'EOF'
competitor,ux,features,pricing,integrations,support,performance,security
Our Product,8,7,7,8,7,9,8
Competitor A,7,8,6,9,6,7,7
Competitor B,9,6,8,5,8,6,6
Competitor C,5,9,5,7,5,8,9
EOF

python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py competitors.csv
```

### Workflow 3: Product Vision Document

**Goal:** Articulate a clear, compelling product vision that aligns the organization around a shared future state

**Steps:**
1. **Gather Inputs** - Collect strategic context:
   - Company mission and long-term vision
   - Market trends and industry analysis
   - Customer research insights and unmet needs
   - Technology trends and enablers
   - Competitive landscape analysis

2. **Define the Vision** - Answer key questions:
   - What world are we trying to create for our users?
   - What will be fundamentally different in 3-5 years?
   - How does our product uniquely enable this future?
   - What do we believe that others do not?

3. **Map the Strategy** - Connect vision to execution:
   ```bash
   # Review strategy frameworks
   cat ../../product-team/product-strategist/references/strategy_types.md
   ```
   - Choose strategic posture (category leader, disruptor, fast follower)
   - Define competitive moats (technology, network effects, data, brand)
   - Identify strategic pillars (3-4 themes that organize the roadmap)

4. **Create the Roadmap Narrative** - Multi-horizon plan:
   - **Horizon 1 (Now - 6 months):** Current priorities, committed work
   - **Horizon 2 (6-18 months):** Emerging opportunities, bets to place
   - **Horizon 3 (18-36 months):** Transformative ideas, vision investments

5. **Validate with Stakeholders** - Test the vision:
   - Engineering: Technical feasibility of long-term bets
   - Sales: Market resonance of positioning
   - Executive: Strategic alignment and resource commitment
   - Customers: Problem validation for future state

6. **Document and Communicate** - Create living document:
   - One-page vision summary (elevator pitch)
   - Detailed vision document with supporting evidence
   - Roadmap visualization by horizon
   - Strategic principles for decision-making

**Expected Output:** Product vision document with 3-5 year direction, strategic pillars, multi-horizon roadmap, and competitive positioning

**Time Estimate:** 2-4 weeks for initial vision (annual refresh)

### Workflow 4: Strategy Pivot Analysis

**Goal:** Evaluate whether a strategic pivot is warranted and plan the transition if so

**Steps:**
1. **Identify Pivot Signals** - Recognize warning signs:
   - Stalled growth metrics (revenue, users, engagement)
   - Persistent product-market fit challenges
   - Major competitive disruption
   - Customer segment shift or churn pattern
   - Technology paradigm change

2. **Quantify Current Performance** - Baseline analysis:
   ```bash
   # Assess current initiative portfolio
   python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py current-initiatives.csv
   ```
   - Revenue trajectory and unit economics
   - Customer acquisition cost trends
   - Retention and engagement metrics
   - Competitive position changes

3. **Evaluate Pivot Options** - Analyze alternatives:
   - **Customer pivot:** Same product, different market segment
   - **Problem pivot:** Same customer, different problem to solve
   - **Solution pivot:** Same problem, different approach
   - **Channel pivot:** Same product, different distribution
   - **Technology pivot:** Same value, different technology platform
   - **Revenue model pivot:** Same product, different monetization

4. **Score Each Option** - Structured evaluation:
   ```bash
   # Build comparison matrix for pivot options
   python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py pivot-options.csv
   ```
   - Market size and growth potential
   - Competitive intensity in new direction
   - Required investment and timeline
   - Leverage of existing assets (team, tech, brand, customers)
   - Risk profile and reversibility

5. **Plan the Transition** - If pivot is warranted:
   - Phase 1: Validate new direction (2-4 weeks, minimal investment)
   - Phase 2: Build MVP for new direction (4-8 weeks)
   - Phase 3: Measure early signals (4 weeks)
   - Phase 4: Commit or revert based on data
   - Communication plan for team, customers, investors

6. **Set Pivot OKRs** - Define success for the new direction:
   ```bash
   python ../../product-team/product-strategist/scripts/okr_cascade_generator.py pivot
   ```

**Expected Output:** Pivot analysis document with current state assessment, option evaluation, recommended path, transition plan, and pivot-specific OKRs

**Time Estimate:** 2-3 weeks for thorough pivot analysis

**Example:**
```bash
# Pivot evaluation workflow
cat > pivot-options.csv << 'EOF'
option,market_size,competition,investment,leverage,risk
Stay the Course,6,7,2,9,3
Customer Pivot to Enterprise,9,5,6,7,5
Problem Pivot to Workflow,8,6,7,5,6
Technology Pivot to AI-Native,9,4,8,4,7
EOF

python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py pivot-options.csv

# Generate OKRs for recommended pivot direction
python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth
```

## Integration Examples

### Example 1: Annual Strategic Planning

```bash
#!/bin/bash
# annual-strategy.sh - Annual product strategy planning

YEAR="2027"

echo "Annual Product Strategy - $YEAR"
echo "================================"

# Competitive landscape
echo ""
echo "1. Competitive Analysis:"
python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py annual-competitors.csv

# Strategy reference
echo ""
echo "2. Strategy Frameworks:"
cat ../../product-team/product-strategist/references/strategy_types.md | head -50

# Annual OKR cascade
echo ""
echo "3. Annual OKR Cascade:"
python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth

# Initiative prioritization
echo ""
echo "4. Strategic Initiative Prioritization:"
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py annual-initiatives.csv --capacity 180
```

### Example 2: Monthly Strategy Review

```bash
#!/bin/bash
# strategy-review.sh - Monthly strategy check-in

echo "Monthly Strategy Review - $(date +%Y-%m-%d)"
echo "============================================"

# Competitive movements
echo ""
echo "Competitive Updates:"
echo "Review: ../../product-team/competitive-teardown/references/data-collection-guide.md"

# OKR progress
echo ""
echo "OKR Progress:"
echo "Review: ../../product-team/product-strategist/assets/okr_template.md"

# Initiative status
echo ""
echo "Initiative Portfolio:"
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py current-initiatives.csv
```

### Example 3: Board Preparation

```bash
#!/bin/bash
# board-prep.sh - Quarterly board meeting preparation

QUARTER="Q3-2026"

echo "Board Preparation - $QUARTER"
echo "============================="

# Strategic metrics
echo ""
echo "1. Product Strategy Performance:"
python ../../product-team/product-manager-toolkit/scripts/rice_prioritizer.py $QUARTER-delivered.csv

# Competitive position
echo ""
echo "2. Competitive Positioning:"
python ../../product-team/competitive-teardown/scripts/competitive_matrix_builder.py board-competitors.csv

# Next quarter OKRs
echo ""
echo "3. Next Quarter OKR Proposal:"
python ../../product-team/product-strategist/scripts/okr_cascade_generator.py growth
```

## Success Metrics

**Strategic Alignment:**
- **OKR Cascade Clarity:** 100% of team OKRs trace to company objectives
- **Strategy Communication:** >90% of product team can articulate product vision
- **Cross-Functional Alignment:** Product, engineering, and GTM teams aligned on priorities
- **Decision Speed:** Strategic decisions made within 1 week of analysis completion

**Competitive Intelligence:**
- **Market Awareness:** Competitive analysis refreshed quarterly
- **Win Rate Impact:** Win rate improves >5% after battle card distribution
- **Positioning Clarity:** Clear differentiation articulated for top 3 competitors
- **Blind Spot Reduction:** No competitive surprises in customer conversations

**OKR Effectiveness:**
- **Achievement Rate:** Average OKR score 0.6-0.7 (ambitious but achievable)
- **Cascade Quality:** All key results measurable with baseline and target
- **Initiative Impact:** >70% of completed initiatives move their associated KR
- **Quarterly Rhythm:** OKR planning completed before quarter starts

**Business Impact:**
- **Revenue Alignment:** Product strategy directly tied to revenue growth targets
- **Market Position:** Maintain or improve position on competitive map
- **Customer Retention:** Strategic decisions reduce churn by measurable percentage
- **Innovation Pipeline:** Horizon 2-3 initiatives represent >20% of roadmap investment

## Related Agents

- [cs-product-manager](cs-product-manager.md) - Feature-level execution, RICE prioritization, PRD development
- [cs-agile-product-owner](cs-agile-product-owner.md) - Sprint-level planning and backlog management
- [cs-ux-researcher](cs-ux-researcher.md) - User research to validate strategic assumptions
- [cs-ceo-advisor](https://github.com/alirezarezvani/claude-skills/tree/main/agents/c-level/cs-ceo-advisor.md) - Company-level strategic alignment
- Senior PM Skill - Portfolio context (see [`project-management/senior-pm`](https://github.com/alirezarezvani/claude-skills/tree/main/project-management/senior-pm))

## References

- **Primary Skill:** [../../product-team/product-strategist/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/SKILL.md)
- **Competitive Teardown Skill:** [../../product-team/competitive-teardown/SKILL.md](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/competitive-teardown/SKILL.md)
- **OKR Framework:** [../../product-team/product-strategist/references/okr_framework.md](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/references/okr_framework.md)
- **Strategy Types:** [../../product-team/product-strategist/references/strategy_types.md](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-strategist/references/strategy_types.md)
- **Product Domain Guide:** [../../product-team/CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/agents/CLAUDE.md)

---

**Last Updated:** March 9, 2026
**Status:** Production Ready
**Version:** 1.0

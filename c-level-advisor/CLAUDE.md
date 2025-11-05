# C-Level Advisory Skills - Claude Code Guidance

This guide covers the 2 production-ready C-level advisory skills for strategic decision-making.

## C-Level Skills Overview

**Available Skills:**
1. **ceo-advisor/** - CEO strategic planning, business operations, organizational design
2. **cto-advisor/** - CTO technical leadership, architecture decisions, engineering strategy

**Focus:** Strategic decision-making, cross-functional alignment, long-term planning

## CEO Advisor

**Skill Location:** `ceo-advisor/`

### Strategic Planning Tools

**Purpose:** Support CEOs in strategic planning, business operations, and organizational design

**Key Areas:**
- Strategic planning frameworks (SWOT, Porter's Five Forces, Blue Ocean)
- Business model canvas and validation
- Organizational structure design
- Change management strategies
- Board reporting and investor relations

**Python Tools:**
- Strategic analysis frameworks
- Business metrics calculator
- Organizational design templates

**Usage:**
```bash
python ceo-advisor/scripts/strategic_analyzer.py company-data.json
```

### Decision-Making Frameworks

**When to Use:**
- Annual strategic planning
- Major business pivots
- M&A evaluation
- Market expansion decisions
- Organizational restructuring

## CTO Advisor

**Skill Location:** `cto-advisor/`

### Technical Leadership Tools

**Purpose:** Support CTOs in technical leadership, architecture decisions, and engineering strategy

**Key Areas:**
- Technology stack selection and evaluation
- Engineering team scaling strategies
- Technical debt management
- Architecture decision records (ADRs)
- Build vs buy analysis
- Engineering culture and practices

**Python Tools:**
- Technology evaluation framework
- Team capacity planning
- Technical debt calculator

**Usage:**
```bash
python cto-advisor/scripts/tech_stack_evaluator.py requirements.yaml
```

### Technical Decision Frameworks

**When to Use:**
- Technology stack decisions
- Architecture pattern selection
- Engineering team organization
- Technical hiring strategies
- Infrastructure planning

## Strategic Workflows

### Workflow 1: Annual Strategic Planning (CEO)

```bash
# 1. Market analysis
python ceo-advisor/scripts/market_analyzer.py industry-data.csv

# 2. SWOT analysis
python ceo-advisor/scripts/swot_generator.py

# 3. Strategy formulation
python ceo-advisor/scripts/strategy_planner.py

# 4. OKR cascade (link to product-strategist)
python ../product-team/product-strategist/scripts/okr_cascade_generator.py growth
```

### Workflow 2: Technical Strategy (CTO)

```bash
# 1. Evaluate technology options
python cto-advisor/scripts/tech_stack_evaluator.py requirements.yaml

# 2. Architecture decision
python cto-advisor/scripts/adr_generator.py

# 3. Team capacity planning
python cto-advisor/scripts/capacity_planner.py team-data.json

# 4. Engineering roadmap
python cto-advisor/scripts/roadmap_generator.py priorities.csv
```

## Integration with Other Skills

### CEO ↔ Product Team
- Strategic OKRs cascade to product OKRs
- Market insights inform product strategy
- Business metrics align with product metrics

### CTO ↔ Engineering Team
- Architecture decisions guide engineering work
- Technical strategy informs team structure
- Engineering metrics roll up to CTO dashboard

### CEO ↔ CTO Alignment
- Strategic business goals inform technical priorities
- Technical capabilities enable business strategies
- Joint decision-making on build vs buy

## Additional Resources

- **CEO Advisor Skill:** `ceo-advisor/SKILL.md`
- **CTO Advisor Skill:** `cto-advisor/SKILL.md`
- **Main Documentation:** `../CLAUDE.md`

---

**Last Updated:** November 5, 2025
**Skills Deployed:** 2/2 C-level skills production-ready
**Focus:** Strategic decision-making and executive leadership

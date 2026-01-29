---
name: product-strategist
description: Strategic product leadership toolkit for Head of Product including OKR cascade generation, market analysis, vision setting, and team scaling. Use for strategic planning, goal alignment, competitive analysis, and organizational design.
---

# Product Strategist

Strategic toolkit for Head of Product to drive vision, alignment, and organizational excellence.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Core Capabilities](#core-capabilities)
- [Workflow: Strategic Planning Session](#workflow-strategic-planning-session)
- [OKR Cascade Generator](#okr-cascade-generator)
  - [Usage](#usage)
  - [Configuration Options](#configuration-options)
  - [Input/Output Examples](#inputoutput-examples)
- [Reference Documents](#reference-documents)

---

## Quick Start

### Generate OKRs for Your Team

```bash
# Growth strategy with default teams
python scripts/okr_cascade_generator.py growth

# Retention strategy with custom teams
python scripts/okr_cascade_generator.py retention --teams "Engineering,Design,Data"

# Revenue strategy with 40% product contribution
python scripts/okr_cascade_generator.py revenue --contribution 0.4

# Export as JSON for integration
python scripts/okr_cascade_generator.py growth --json > okrs.json
```

---

## Core Capabilities

| Capability | Description | Tool |
|------------|-------------|------|
| **OKR Cascade** | Generate aligned OKRs from company to team level | `okr_cascade_generator.py` |
| **Alignment Scoring** | Measure vertical and horizontal alignment | Built into generator |
| **Strategy Templates** | 5 pre-built strategy types | Growth, Retention, Revenue, Innovation, Operational |
| **Team Configuration** | Customize for your org structure | `--teams` flag |

---

## Workflow: Strategic Planning Session

A step-by-step guide for running a quarterly strategic planning session.

### Step 1: Define Strategic Focus

Choose the primary strategy type based on company priorities:

| Strategy | When to Use |
|----------|-------------|
| **Growth** | Scaling user base, market expansion |
| **Retention** | Reducing churn, improving LTV |
| **Revenue** | Increasing ARPU, new monetization |
| **Innovation** | Market differentiation, new capabilities |
| **Operational** | Improving efficiency, scaling operations |

See `references/strategy_types.md` for detailed guidance on each strategy.

### Step 2: Gather Input Metrics

Collect current state metrics to inform OKR targets:

```bash
# Example metrics JSON
{
  "current": 100000,      # Current MAU
  "target": 150000,       # Target MAU
  "current_nps": 40,      # Current NPS
  "target_nps": 60        # Target NPS
}
```

### Step 3: Configure Team Structure

Define the teams that will receive cascaded OKRs:

```bash
# Default teams
python scripts/okr_cascade_generator.py growth

# Custom teams for your organization
python scripts/okr_cascade_generator.py growth --teams "Core,Platform,Mobile,AI"
```

### Step 4: Generate OKR Cascade

Run the generator to create aligned OKRs:

```bash
python scripts/okr_cascade_generator.py growth --contribution 0.3
```

### Step 5: Review Alignment Scores

Check the alignment scores in the output:

| Score | Target | Action |
|-------|--------|--------|
| Vertical Alignment | >90% | Ensure all objectives link to parent |
| Horizontal Alignment | >75% | Check for team coordination |
| Coverage | >80% | Validate all company OKRs are addressed |
| Balance | >80% | Redistribute if one team is overloaded |
| **Overall** | **>80%** | Good alignment; <60% needs restructuring |

### Step 6: Refine and Validate

Before finalizing:

- [ ] Review generated objectives with stakeholders
- [ ] Adjust team assignments based on capacity
- [ ] Validate contribution percentages are realistic
- [ ] Ensure no conflicting objectives across teams
- [ ] Set up tracking cadence (bi-weekly check-ins)

### Step 7: Export and Track

Export OKRs for your tracking system:

```bash
# JSON for tools like Lattice, Ally, Workboard
python scripts/okr_cascade_generator.py growth --json > q1_okrs.json
```

---

## OKR Cascade Generator

Automatically cascades company OKRs down to product and team levels with alignment tracking.

### Usage

```bash
python scripts/okr_cascade_generator.py [strategy] [options]
```

**Strategies:**
- `growth` - User acquisition and market expansion
- `retention` - Customer value and churn reduction
- `revenue` - Revenue growth and monetization
- `innovation` - Product differentiation and leadership
- `operational` - Efficiency and organizational excellence

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--teams`, `-t` | Comma-separated team names | Growth,Platform,Mobile,Data |
| `--contribution`, `-c` | Product contribution to company OKRs (0-1) | 0.3 (30%) |
| `--json`, `-j` | Output as JSON instead of dashboard | False |
| `--metrics`, `-m` | Metrics as JSON string | Sample metrics |

**Examples:**

```bash
# Custom teams
python scripts/okr_cascade_generator.py retention \
  --teams "Engineering,Design,Data,Growth"

# Higher product contribution
python scripts/okr_cascade_generator.py revenue --contribution 0.4

# Full customization
python scripts/okr_cascade_generator.py innovation \
  --teams "Core,Platform,ML" \
  --contribution 0.5 \
  --json
```

### Input/Output Examples

#### Example 1: Growth Strategy (Dashboard Output)

**Command:**
```bash
python scripts/okr_cascade_generator.py growth
```

**Output:**
```
============================================================
OKR CASCADE DASHBOARD
Quarter: Q1 2025
Strategy: GROWTH
Teams: Growth, Platform, Mobile, Data
Product Contribution: 30%
============================================================

🏢 COMPANY OKRS

📌 CO-1: Accelerate user acquisition and market expansion
   └─ CO-1-KR1: Increase MAU from 100000 to 150000
   └─ CO-1-KR2: Achieve 150000% MoM growth rate
   └─ CO-1-KR3: Expand to 150000 new markets

📌 CO-2: Achieve product-market fit in new segments
   └─ CO-2-KR1: Reduce CAC by 150000%
   └─ CO-2-KR2: Improve activation rate to 150000%
   └─ CO-2-KR3: Increase MAU from 100000 to 150000

📌 CO-3: Build sustainable growth engine
   └─ CO-3-KR1: Achieve 150000% MoM growth rate
   └─ CO-3-KR2: Expand to 150000 new markets
   └─ CO-3-KR3: Reduce CAC by 150000%

🚀 PRODUCT OKRS

📌 PO-1: Build viral product features and market expansion
   ↳ Supports: CO-1
   └─ PO-1-KR1: Increase product MAU from 100000 to 45000.0
   └─ PO-1-KR2: Achieve 45000.0% feature adoption rate

📌 PO-2: Validate product hypotheses in new segments
   ↳ Supports: CO-2
   └─ PO-2-KR1: Reduce product onboarding efficiency by 45000.0%
   └─ PO-2-KR2: Improve activation rate to 45000.0%

📌 PO-3: Create product-led growth loops engine
   ↳ Supports: CO-3
   └─ PO-3-KR1: Achieve 45000.0% feature adoption rate
   └─ PO-3-KR2: Expand to 45000.0 new markets

👥 TEAM OKRS

Growth Team:
  📌 GRO-1: Build viral product features through acquisition and activation
     └─ GRO-1-KR1: [Growth] Increase product MAU from 100000 to 11250.0
     └─ GRO-1-KR2: [Growth] Achieve 11250.0% feature adoption rate

Platform Team:
  📌 PLA-1: Build viral product features through infrastructure and reliability
     └─ PLA-1-KR1: [Platform] Increase product MAU from 100000 to 11250.0
     └─ PLA-1-KR2: [Platform] Achieve 11250.0% feature adoption rate


📊 ALIGNMENT MATRIX

Company → Product → Teams
----------------------------------------

CO-1
  ├─ PO-1
    └─ GRO-1 (Growth)
    └─ PLA-1 (Platform)

CO-2
  ├─ PO-2

CO-3
  ├─ PO-3


🎯 ALIGNMENT SCORES
----------------------------------------
✓ Vertical Alignment: 100.0%
! Horizontal Alignment: 75.0%
✓ Coverage: 100.0%
✓ Balance: 97.5%
✓ Overall: 94.0%

✅ Overall alignment is GOOD (≥80%)
```

#### Example 2: JSON Output

**Command:**
```bash
python scripts/okr_cascade_generator.py retention --json
```

**Output (truncated):**
```json
{
  "quarter": "Q1 2025",
  "strategy": "retention",
  "company": {
    "level": "Company",
    "objectives": [
      {
        "id": "CO-1",
        "title": "Create lasting customer value and loyalty",
        "owner": "CEO",
        "key_results": [
          {
            "id": "CO-1-KR1",
            "title": "Improve retention from 100000% to 150000%",
            "current": 100000,
            "target": 150000
          }
        ]
      }
    ]
  },
  "product": {
    "level": "Product",
    "contribution": 0.3,
    "objectives": [...]
  },
  "teams": [...],
  "alignment_scores": {
    "vertical_alignment": 100.0,
    "horizontal_alignment": 75.0,
    "coverage": 100.0,
    "balance": 97.5,
    "overall": 94.0
  },
  "config": {
    "teams": ["Growth", "Platform", "Mobile", "Data"],
    "product_contribution": 0.3
  }
}
```

See `references/examples/sample_growth_okrs.json` for a complete example.

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/okr_framework.md` | OKR methodology, writing guidelines, alignment scoring |
| `references/strategy_types.md` | Detailed breakdown of all 5 strategy types with examples |
| `references/examples/sample_growth_okrs.json` | Complete sample output for growth strategy |

---

## Best Practices

### OKR Cascade

- Limit to 3-5 objectives per level
- Each objective should have 3-5 key results
- Key results must be measurable with current and target values
- Validate parent-child relationships before finalizing

### Alignment Scoring

- Target >80% overall alignment
- Investigate any score below 60%
- Balance scores ensure no team is overloaded
- Horizontal alignment prevents conflicting goals

### Team Configuration

- Configure teams to match your actual org structure
- Adjust contribution percentages based on team size
- Platform/Infrastructure teams often support all objectives
- Specialized teams (ML, Data) may only support relevant objectives

---

## Quick Reference

```bash
# Common commands
python scripts/okr_cascade_generator.py growth               # Default growth
python scripts/okr_cascade_generator.py retention            # Retention focus
python scripts/okr_cascade_generator.py revenue -c 0.4       # 40% contribution
python scripts/okr_cascade_generator.py growth --json        # JSON export
python scripts/okr_cascade_generator.py growth -t "A,B,C"    # Custom teams
```

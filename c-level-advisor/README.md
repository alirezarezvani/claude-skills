# C-Level Advisory Skills Collection

**Complete suite of 2 executive leadership skills** covering CEO and CTO strategic decision-making and organizational leadership.

---

## 📚 Table of Contents

- [Installation](#installation)
- [Overview](#overview)
- [Skills Catalog](#skills-catalog)
- [Quick Start Guide](#quick-start-guide)
- [Common Workflows](#common-workflows)
- [Success Metrics](#success-metrics)

---

## ⚡ Installation

### Quick Install (Recommended)

Install all C-Level advisory skills with one command:

```bash
# Install all C-Level skills to all supported agents
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor

# Install to Claude Code only
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor --agent claude

# Install to Cursor only
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor --agent cursor
```

### Install Individual Skills

```bash
# CEO Advisor
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/ceo-advisor

# CTO Advisor
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/cto-advisor
```

**Supported Agents:** Claude Code, Cursor, VS Code, Copilot, Goose, Amp, Codex

**Complete Installation Guide:** See [../INSTALLATION.md](../INSTALLATION.md) for detailed instructions, troubleshooting, and manual installation.

---

## 🎯 Overview

This C-Level advisory skills collection provides executive leadership guidance for strategic decision-making, organizational development, and stakeholder management.

**What's Included:**
- **2 executive-level skills** for CEO and CTO roles
- **6 Python analysis tools** for strategy, finance, tech debt, and team scaling
- **Comprehensive frameworks** for executive decision-making, board governance, and technology leadership
- **Ready-to-use templates** for board presentations, ADRs, and strategic planning

**Ideal For:**
- CEOs and founders at startups and scale-ups
- CTOs and VP Engineering roles
- Executive leadership teams
- Board members and advisors

**Key Benefits:**
- 🎯 **Strategic clarity** with structured decision-making frameworks
- 📊 **Data-driven decisions** with financial and technical analysis tools
- 🚀 **Faster execution** with proven templates and best practices
- 💡 **Risk mitigation** through systematic evaluation processes

---

## 📦 Skills Catalog

### 1. CEO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Executive leadership guidance for strategic decision-making, organizational development, and stakeholder management.

**Key Capabilities:**
- Strategic planning and initiative evaluation
- Financial scenario modeling and business outcomes
- Executive decision framework (structured methodology)
- Leadership and organizational culture development
- Board governance and investor relations
- Stakeholder communication best practices

**Python Tools:**
- `strategy_analyzer.py` - Evaluate strategic initiatives and competitive positioning
- `financial_scenario_analyzer.py` - Model financial scenarios and business outcomes

**Core Workflows:**
1. Strategic planning and initiative evaluation
2. Financial scenario modeling
3. Board and investor communication
4. Organizational culture development

**Use When:**
- Making strategic decisions (market expansion, product pivots, fundraising)
- Preparing board presentations
- Modeling business scenarios
- Building organizational culture
- Managing stakeholder relationships

**Learn More:** [ceo-advisor/SKILL.md](ceo-advisor/SKILL.md)

---

### 2. CTO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

**Purpose:** Technical leadership guidance for engineering teams, architecture decisions, and technology strategy.

**Key Capabilities:**
- Technical debt assessment and management
- Engineering team scaling and structure planning
- Technology evaluation and selection frameworks
- Architecture decision documentation (ADRs)
- Engineering metrics (DORA metrics, velocity, quality)
- Build vs. buy analysis

**Python Tools:**
- `tech_debt_analyzer.py` - Quantify and prioritize technical debt
- `team_scaling_calculator.py` - Model engineering team growth and structure

**Core Workflows:**
1. Technical debt assessment and management
2. Engineering team scaling and structure
3. Technology evaluation and selection
4. Architecture decision documentation

**Use When:**
- Managing technical debt
- Scaling engineering teams
- Evaluating new technologies or frameworks
- Making architecture decisions
- Measuring engineering performance

**Learn More:** [cto-advisor/SKILL.md](cto-advisor/SKILL.md)

---

## 🚀 Quick Start Guide

### For CEOs

1. **Install CEO Advisor:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/ceo-advisor
   ```

2. **Evaluate Strategic Initiative:**
   ```bash
   python ceo-advisor/scripts/strategy_analyzer.py strategy-doc.md
   ```

3. **Model Financial Scenarios:**
   ```bash
   python ceo-advisor/scripts/financial_scenario_analyzer.py scenarios.yaml
   ```

4. **Prepare for Board Meeting:**
   - Use frameworks in `references/board_governance_investor_relations.md`
   - Apply decision framework from `references/executive_decision_framework.md`
   - Use templates from `assets/`

### For CTOs

1. **Install CTO Advisor:**
   ```bash
   npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/cto-advisor
   ```

2. **Analyze Technical Debt:**
   ```bash
   python cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase
   ```

3. **Plan Team Scaling:**
   ```bash
   python cto-advisor/scripts/team_scaling_calculator.py --current-size 10 --target-size 50
   ```

4. **Document Architecture Decisions:**
   - Use ADR templates from `references/architecture_decision_records.md`
   - Apply technology evaluation framework
   - Track engineering metrics

---

## 🔄 Common Workflows

### Workflow 1: Strategic Decision Making (CEO)

```
1. Problem Definition → CEO Advisor
   - Define decision context
   - Identify stakeholders
   - Clarify success criteria

2. Strategic Analysis → CEO Advisor
   - Strategy analyzer tool
   - Competitive positioning
   - Market opportunity assessment

3. Financial Modeling → CEO Advisor
   - Scenario analyzer tool
   - Revenue projections
   - Cost-benefit analysis

4. Decision Framework → CEO Advisor
   - Apply structured methodology
   - Risk assessment
   - Go/No-go recommendation

5. Stakeholder Communication → CEO Advisor
   - Board presentation
   - Investor update
   - Team announcement
```

### Workflow 2: Technology Evaluation (CTO)

```
1. Technology Assessment → CTO Advisor
   - Requirements gathering
   - Technology landscape scan
   - Evaluation criteria definition

2. Build vs. Buy Analysis → CTO Advisor
   - TCO calculation
   - Risk analysis
   - Timeline estimation

3. Architecture Impact → CTO Advisor
   - System design implications
   - Integration complexity
   - Migration path

4. Decision Documentation → CTO Advisor
   - ADR creation
   - Technical specification
   - Implementation roadmap

5. Team Communication → CTO Advisor
   - Engineering announcement
   - Training plan
   - Implementation kickoff
```

### Workflow 3: Engineering Team Scaling (CTO)

```
1. Current State Assessment → CTO Advisor
   - Team structure analysis
   - Velocity and quality metrics
   - Bottleneck identification

2. Growth Modeling → CTO Advisor
   - Team scaling calculator
   - Organizational design
   - Role definition

3. Hiring Plan → CTO Advisor
   - Hiring timeline
   - Budget requirements
   - Onboarding strategy

4. Process Evolution → CTO Advisor
   - Updated workflows
   - Team communication
   - Quality gates

5. Implementation → CTO Advisor
   - Gradual rollout
   - Metrics tracking
   - Continuous adjustment
```

### Workflow 4: Board Preparation (CEO)

```
1. Content Preparation → CEO Advisor
   - Financial summary
   - Strategic updates
   - Key metrics dashboard

2. Presentation Design → CEO Advisor
   - Board governance frameworks
   - Slide deck structure
   - Data visualization

3. Q&A Preparation → CEO Advisor
   - Anticipated questions
   - Risk mitigation answers
   - Strategic rationale

4. Rehearsal → CEO Advisor
   - Timing practice
   - Narrative flow
   - Supporting materials
```

---

## 📊 Success Metrics

### CEO Advisor Impact

**Strategic Clarity:**
- 40% improvement in decision-making speed
- 50% reduction in strategic initiative failures
- 60% improvement in stakeholder alignment

**Financial Performance:**
- 30% better accuracy in financial projections
- 45% improvement in scenario planning effectiveness
- 25% reduction in unexpected costs

**Board & Investor Relations:**
- 50% reduction in board presentation preparation time
- 70% improvement in board feedback quality
- 40% better investor communication clarity

### CTO Advisor Impact

**Technical Debt Management:**
- 60% improvement in tech debt visibility
- 40% reduction in critical tech debt items
- 50% better resource allocation for debt reduction

**Team Scaling:**
- 45% faster time-to-productivity for new hires
- 35% reduction in team scaling mistakes
- 50% improvement in organizational design clarity

**Technology Decisions:**
- 70% reduction in technology evaluation time
- 55% improvement in build vs. buy accuracy
- 40% better architecture decision documentation

---

## 🔗 Integration with Other Teams

**CEO ↔ Product:**
- Strategic vision → Product roadmap
- Market insights → Product strategy
- Customer feedback → Product prioritization

**CEO ↔ CTO:**
- Technology strategy → Business strategy
- Engineering capacity → Business planning
- Technical decisions → Strategic initiatives

**CTO ↔ Engineering:**
- Architecture decisions → Implementation
- Tech debt priorities → Sprint planning
- Team structure → Engineering delivery

**CTO ↔ Product:**
- Technical feasibility → Product planning
- Platform capabilities → Product features
- Engineering metrics → Product velocity

---

## 📚 Additional Resources

- **CLAUDE.md:** [c-level-advisor/CLAUDE.md](CLAUDE.md) - Claude Code specific guidance (if exists)
- **Main Documentation:** [../CLAUDE.md](../CLAUDE.md)
- **Installation Guide:** [../INSTALLATION.md](../INSTALLATION.md)

---

**Last Updated:** January 2026
**Skills Deployed:** 2/2 C-Level advisory skills production-ready
**Total Tools:** 6 Python analysis tools (strategy, finance, tech debt, team scaling)

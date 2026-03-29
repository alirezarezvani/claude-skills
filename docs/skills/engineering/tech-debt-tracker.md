---
title: "Tech Debt Tracker — Agent Skill for Codex & OpenClaw"
description: "Scan codebases for technical debt, score severity, track trends, and generate prioritized remediation plans. Use when users mention tech debt, code. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Tech Debt Tracker

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `tech-debt-tracker`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/tech-debt-tracker/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier**: POWERFUL 🔥  
**Category**: Engineering Process Automation  
**Expertise**: Code Quality, Technical Debt Management, Software Engineering

## Overview

Tech debt is one of the most insidious challenges in software development - it compounds over time, slowing down development velocity, increasing maintenance costs, and reducing code quality. This skill provides a comprehensive framework for identifying, analyzing, prioritizing, and tracking technical debt across codebases.

Tech debt isn't just about messy code - it encompasses architectural shortcuts, missing tests, outdated dependencies, documentation gaps, and infrastructure compromises. Like financial debt, it accrues "interest" through increased development time, higher bug rates, and reduced team velocity.

## What This Skill Provides

This skill offers three interconnected tools that form a complete tech debt management system:

1. **Debt Scanner** - Automatically identifies tech debt signals in your codebase
2. **Debt Prioritizer** - Analyzes and prioritizes debt items using cost-of-delay frameworks
3. **Debt Dashboard** - Tracks debt trends over time and provides executive reporting

Together, these tools enable engineering teams to make data-driven decisions about tech debt, balancing new feature development with maintenance work.

## Technical Debt Classification Framework
→ See references/debt-frameworks.md for details

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
1. Set up debt scanning infrastructure
2. Establish debt taxonomy and scoring criteria
3. Scan initial codebase and create baseline inventory
4. Train team on debt identification and reporting

### Phase 2: Process Integration (Weeks 3-4)
1. Integrate debt tracking into sprint planning
2. Establish debt budgets and allocation rules
3. Create stakeholder reporting templates
4. Set up automated debt scanning in CI/CD

### Phase 3: Optimization (Weeks 5-6)
1. Refine scoring algorithms based on team feedback
2. Implement trend analysis and predictive metrics
3. Create specialized debt reduction initiatives
4. Establish cross-team debt coordination processes

### Phase 4: Maturity (Ongoing)
1. Continuous improvement of detection algorithms
2. Advanced analytics and prediction models
3. Integration with planning and project management tools
4. Organization-wide debt management best practices

## Success Criteria

**Quantitative Metrics:**
- 25% reduction in debt interest rate within 6 months
- 15% improvement in development velocity
- 30% reduction in production defects
- 20% faster code review cycles

**Qualitative Metrics:**
- Improved developer satisfaction scores
- Reduced context switching during feature development
- Faster onboarding for new team members
- Better predictability in feature delivery timelines

## Common Pitfalls and How to Avoid Them

### 1. Analysis Paralysis
**Problem**: Spending too much time analyzing debt instead of fixing it.
**Solution**: Set time limits for analysis, use "good enough" scoring for most items.

### 2. Perfectionism
**Problem**: Trying to eliminate all debt instead of managing it.
**Solution**: Focus on high-impact debt, accept that some debt is acceptable.

### 3. Ignoring Business Context
**Problem**: Prioritizing technical elegance over business value.
**Solution**: Always tie debt work to business outcomes and customer impact.

### 4. Inconsistent Application
**Problem**: Some teams adopt practices while others ignore them.
**Solution**: Make debt tracking part of standard development workflow.

### 5. Tool Over-Engineering
**Problem**: Building complex debt management systems that nobody uses.
**Solution**: Start simple, iterate based on actual usage patterns.

Technical debt management is not just about writing better code - it's about creating sustainable development practices that balance short-term delivery pressure with long-term system health. Use these tools and frameworks to make informed decisions about when and how to invest in debt reduction.

---
title: "Agent Orchestration — Multi-Skill Coordination Protocol"
description: "A lightweight protocol for orchestrating AI coding agents, personas, and skills across domains. Coordinate Claude Code skills and Codex agents on complex, multi-domain work."
---

# :material-sitemap: Orchestration

A lightweight protocol for coordinating personas, skills, and agents on work that crosses domain boundaries. No framework required. No dependencies. Just structured prompting.

## Core Concept

Most real work crosses domain boundaries. A product launch needs engineering, marketing, and strategy. An architecture review needs security, cost analysis, and team assessment.

Orchestration connects the right expertise to each phase of work:

- **Personas** define _who_ is thinking (identity, judgment, communication style)
- **Skills** define _how_ to execute (steps, scripts, templates, references)
- **Task agents** define _what_ to do (scoped, single-domain execution)

---

## Patterns

### Solo Sprint

One person, one objective, multiple domains. Switch personas as you move through phases.

```
Week 1: startup-cto + engineering skills → Build
Week 2: growth-marketer + marketing skills → Prepare launch
Week 3: solo-founder + business skills → Ship and iterate
```

Best for: side projects, MVPs, solo founders.

### Domain Deep-Dive

One domain, maximum depth. Single persona, multiple skills stacked.

```
Persona: startup-cto
Skills loaded simultaneously:
  - aws-solution-architect (infrastructure)
  - senior-security (hardening)
  - cto-advisor (tech debt assessment)

Task: Full technical audit of existing system
```

Best for: architecture reviews, compliance audits, technical due diligence.

### Multi-Agent Handoff

Different personas review each other's work.

```
Step 1: startup-cto designs the architecture
Step 2: growth-marketer reviews from user/market perspective
Step 3: solo-founder makes the final trade-off decision
```

Best for: high-stakes decisions, launch readiness reviews, investor prep.

### Skill Chain

No persona needed. Chain skills sequentially for procedural work.

```
1. content-strategy → Identify topics and angles
2. copywriting → Write the content
3. seo-audit → Optimize for search
4. analytics-tracking → Set up measurement
```

Best for: repeatable processes, content pipelines, compliance checklists.

---

## Example: 6-Week Product Launch

| Phase | Weeks | Persona | Skills | Output |
|-------|-------|---------|--------|--------|
| Build | 1-2 | startup-cto | aws-solution-architect, senior-frontend | Architecture doc, deployed MVP |
| Prepare | 3-4 | growth-marketer | launch-strategy, copywriting, seo-audit | Landing page, content calendar |
| Ship | 5 | solo-founder | email-sequence, analytics-tracking | Launch, tracking verified |
| Iterate | 6 | solo-founder | form-cro, copy-editing | Conversion improvements, metrics report |

---

## Rules

1. **One persona at a time.** Switching is fine, but don't blend two in the same prompt.
2. **Skills stack freely.** Load as many as the task needs.
3. **Personas are optional.** For procedural work, skill chains alone are sufficient.
4. **Context carries forward.** When switching phases, summarize decisions and artifacts.
5. **The human decides.** Override any phase, persona, or skill choice.

---

## Quick Reference

**Activate a persona:**
```
Load agents/personas/startup-cto.md
```

**Load a skill:**
```
Load engineering/aws-solution-architect/SKILL.md
```

**Phase handoff:**
```
Phase 1 complete.
Decisions: [list]
Artifacts: [list]
Open items: [list]
Switching to: [persona] + [skills]
```

[:octicons-arrow-right-24: Full orchestration protocol](https://github.com/alirezarezvani/claude-skills/blob/main/orchestration/ORCHESTRATION.md)

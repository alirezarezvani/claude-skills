# Orchestration Protocol

A lightweight pattern for coordinating personas, skills, and task agents on complex work.

No framework required. No dependencies. Just structured prompting.

---

## Core Concept

Most real work crosses domain boundaries. A product launch needs engineering, marketing, and strategy. An architecture review needs security, cost analysis, and team assessment.

Orchestration connects the right expertise to each phase of work:

- **Personas** define _who_ is thinking (identity, judgment, communication style)
- **Skills** define _how_ to execute (steps, scripts, templates, references)
- **Task agents** define _what_ to do (scoped, single-domain execution)

You combine them. The pattern is always the same.

---

## The Pattern

### 1. Define the objective

State what you want to accomplish, not how to accomplish it.

```
Objective: Launch a new SaaS product for small accounting firms.
Constraints: 2-person team, $5K budget, 6-week timeline.
Success criteria: 50 paying customers in first 30 days.
```

### 2. Select the right persona

Pick the persona whose judgment fits the problem. Personas carry opinions, priorities, and decision-making frameworks.

| Situation | Persona | Why |
|-----------|---------|-----|
| Architecture decisions, tech stack, hiring plan | `startup-cto` | Pragmatic engineering judgment |
| Launch strategy, content, growth channels | `growth-marketer` | Channel expertise and budget sense |
| Everything at once, alone | `solo-founder` | Cross-domain prioritization |

**Activation:**
```
Load agents/personas/startup-cto.md
```

### 3. Load skills for execution

Personas know _what_ to do. Skills know _how_ to do it with precision. Load the skills your current phase needs.

```
Load skills:
- engineering/aws-solution-architect/SKILL.md
- engineering/mcp-server-builder/SKILL.md
```

The persona drives decisions. The skills provide the structured steps, scripts, and templates.

### 4. Work in phases

Break the objective into phases. Each phase can use different skills.

```
Phase 1: Technical Foundation (Week 1-2)
  Persona: startup-cto
  Skills: aws-solution-architect, senior-frontend
  Output: Architecture doc, deployed skeleton

Phase 2: Launch Preparation (Week 3-4)
  Persona: growth-marketer
  Skills: launch-strategy, copywriting, seo-audit
  Output: Landing page, content calendar, launch plan

Phase 3: Go-to-Market (Week 5-6)
  Persona: solo-founder
  Skills: email-sequence, analytics-tracking, pricing-strategy
  Output: Launched product, tracking, first customers
```

### 5. Hand off between phases

When switching phases, pass context forward:

```
Phase 1 complete.
Decisions made: [list key decisions]
Artifacts created: [list files/docs]
Open questions: [what the next phase needs to resolve]

Switching to Phase 2. Load growth-marketer persona and launch-strategy skill.
```

---

## Common Orchestration Patterns

### Pattern A: Solo Sprint

One person, one objective, multiple domains. Switch personas as you move through phases.

```
Week 1: startup-cto + engineering skills → Build the thing
Week 2: growth-marketer + marketing skills → Prepare the launch
Week 3: solo-founder + business skills → Ship and iterate
```

Best for: side projects, MVPs, solo founders.

### Pattern B: Domain Deep-Dive

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

### Pattern C: Multi-Agent Handoff

Different personas review each other's work. Useful for quality and coverage.

```
Step 1: startup-cto designs the architecture
Step 2: growth-marketer reviews from user/market perspective
Step 3: solo-founder makes the final trade-off decision
```

Best for: high-stakes decisions, launch readiness reviews, investor prep.

### Pattern D: Skill Chain

No persona needed. Chain skills sequentially for procedural work.

```
1. content-strategy/SKILL.md → Identify topics and angles
2. copywriting/SKILL.md → Write the content
3. seo-audit/SKILL.md → Optimize for search
4. analytics-tracking/SKILL.md → Set up measurement
```

Best for: repeatable processes, content pipelines, compliance checklists.

---

## Example: Full Product Launch

Here is a complete orchestration for launching a B2B SaaS product.

### Setup
```
Objective: Launch invoicing tool for freelancers
Team: 1 developer, 1 marketer
Timeline: 6 weeks
Budget: $3K
```

### Execution

**Week 1-2: Build**
```
Persona: startup-cto
Skills:
  - aws-solution-architect → Infrastructure
  - senior-frontend → UI implementation
  
Deliverables:
  - Architecture decision record
  - Deployed MVP (auth, core feature, payments)
  - CI/CD pipeline
```

**Week 3-4: Prepare Launch**
```
Persona: growth-marketer
Skills:
  - launch-strategy → Launch plan and timeline
  - copywriting → Landing page, emails
  - content-strategy → Blog posts, social content
  - seo-audit → Technical SEO for landing page

Deliverables:
  - Landing page live
  - 5 blog posts scheduled
  - Email sequence configured
  - Launch day checklist
```

**Week 5: Launch**
```
Persona: solo-founder
Skills:
  - email-sequence → Drip campaign
  - analytics-tracking → Conversion tracking
  - ab-test-setup → Landing page variants

Deliverables:
  - Product Hunt submission
  - Email blast to waitlist
  - Tracking verified end-to-end
```

**Week 6: Iterate**
```
Persona: solo-founder
Skills:
  - form-cro → Optimize signup flow
  - copy-editing → Refine messaging based on feedback

Deliverables:
  - Conversion improvements shipped
  - Week 1 metrics report
  - Roadmap for month 2
```

---

## Rules

1. **One persona at a time.** Switching is fine, but don't blend two personas in the same prompt. Pick one voice.
2. **Skills stack freely.** Load as many skills as the task needs. They don't conflict.
3. **Personas are optional.** For procedural work, skill chains alone are sufficient.
4. **Context carries forward.** When switching phases, always summarize decisions and artifacts.
5. **The human decides.** Orchestration is a suggestion. Override any phase, persona, or skill choice.

---

## Quick Reference

### Persona Activation
```
Load agents/personas/<name>.md
```

### Skill Loading
```
Load <domain>/<skill-name>/SKILL.md
```

### Phase Handoff
```
Phase [N] complete.
Decisions: [list]
Artifacts: [list]
Open items: [list]
Switching to: [persona] + [skills]
```

### Available Personas
See [agents/personas/README.md](../agents/personas/README.md)

### Available Skills
See the [skill catalog](../README.md) — 177 skills across 12 domains.

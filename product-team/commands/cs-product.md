---
description: Top-level product-team router. Classifies a product inquiry across 16 lanes (prioritization, OKRs, UX, design system, competitive, analytics, experiments, discovery, roadmaps, spec-to-repo, landing, SaaS scaffold, stories, HIG, code-to-PRD, summarizer) with a deterministic script and forks context to the right sub-skill via the product-skills orchestrator, returning a ≤200-word digest with one grill challenge.
argument-hint: "<product inquiry: prioritize features, plan an experiment, discovery health, etc.>"
---

# /cs:product — Product Team router

Route this inquiry through the `product-skills` orchestrator:

**$ARGUMENTS**

## Routing (deterministic — run the script, don't eyeball)

```bash
python3 product-team/skills/product-skills/scripts/product_goal_router.py --text "$ARGUMENTS" --output json
```

- Exit 0 → load `skill_path`/SKILL.md (covers the 4 standalone plugins too) and follow
  that skill's own workflow in a fork.
- Exit 2 → ask ONE clarifying question naming the listed candidates, recommended answer
  first.
- Exit 3 → ask the user to restate the goal with the deliverable named. Never guess.
- Explore the workspace first — an `ost.json`, `discovery_log.json`, or `features.csv`
  resolves the lane silently. Never silently chain a second sub-skill.

## Output (≤200-word digest)

- What was analyzed
- Top 3 findings, each anchored to a canon citation
- Top 3 next actions with a named owner
- Artifact path
- One grill challenge (e.g. "This roadmap cites an OST that fails the linter — which
  opportunity backs item 3?")

## Hard rules

- Insights carry participant counts; singletons are anecdotes.
- Experiments carry computed sample size + MDE, never gut feel.
- Prioritization names its framework (RICE / WSJF / opportunity score) and why.
- AI features get an eval spec (golden set + rubric + guardrails) in the PRD.
- Recurring discovery work goes to `/cs:product-loop` instead.

## Distinct from

- `project-management` — how to deliver. This domain is what to build.
- `marketing/landing` — from-scratch marketing pages; `landing-page-generator` here
  scaffolds product Next.js/TSX pages.

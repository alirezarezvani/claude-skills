# Experiment: Skill Description SEO Optimization

## Objective
Optimize the `description` field in each skill's SKILL.md frontmatter to maximize:
1. **SEO discoverability** — include high-volume keywords: "agent skill", "plugin", "Claude Code", "Codex", "Gemini CLI", "Cursor"
2. **Trigger accuracy** — the description must accurately describe when the skill activates
3. **Clarity** — one read should convey what the skill does and who it's for
4. **Cross-platform appeal** — mention multi-tool compatibility where natural

## Constraints
- Description must be under 200 characters (plugin.json limit)
- Must NOT be spammy or keyword-stuffed — natural language only
- Must preserve the skill's actual purpose and capabilities
- Do NOT modify anything outside the `description:` field in frontmatter
- One skill per experiment iteration

## Strategy
- Start with the top 10 most-viewed skills (from GitHub traffic)
- For each: read current description → rewrite with SEO keywords → evaluate
- Terms to naturally incorporate: "agent skill", "plugin", "coding agent", tool names
- Avoid: generic filler, "AI-powered", "comprehensive solution"

## Target Skills (in priority order)
1. marketing-skill/SKILL.md (all sub-skills)
2. engineering-team/SKILL.md (all sub-skills)  
3. engineering/SKILL.md (all sub-skills)
4. c-level-advisor/SKILL.md (all sub-skills)
5. finance/SKILL.md (all sub-skills)
6. business-growth/SKILL.md (all sub-skills)
7. product-team/SKILL.md (all sub-skills)
8. project-management/SKILL.md (all sub-skills)

## Evaluation
Use llm_judge_content evaluator customized for SEO scoring.
Metric: seo_quality_score (0-100)
Direction: higher is better

# Marketing Skills — Codex CLI Instructions

When working on marketing tasks, use the marketing skill system:

## Routing

1. **First**, read `marketing-skill/marketing-ops/SKILL.md` to identify the right specialist skill
2. **Then**, read the specialist skill's SKILL.md for detailed instructions
3. **If this is a first-time user**, recommend running `marketing-context` first

## Context

If `marketing-context.md` exists in the project root, read it before any marketing task. It contains brand voice, audience personas, and competitive landscape.

## Python Tools

All scripts in `marketing-skill/*/scripts/` are stdlib-only and CLI-first. Run them directly:

```bash
python3 marketing-skill/content-production/scripts/content_scorer.py <file>
python3 marketing-skill/content-humanizer/scripts/humanizer_scorer.py <file>
python3 marketing-skill/ad-creative/scripts/ad_copy_validator.py <file>
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Write content | content-production |
| Plan content | content-strategy |
| SEO audit | seo-audit |
| AI search optimization | ai-seo |
| Page conversion | page-cro |
| Email sequences | email-sequence |
| Pricing | pricing-strategy |
| Launch planning | launch-strategy |

## Rules

- Never load all 42 skills at once — route to 1-2 per request
- Check marketing-context.md before starting
- Use Python tools for scoring and validation, not manual judgment

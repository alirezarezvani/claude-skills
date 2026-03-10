# Product Skills — Codex CLI Instructions

When working on product tasks, use the product skill system:

## Routing

1. **Identify the task:** Prioritization, strategy, UX, UI, competitor analysis, or SaaS scaffolding
2. **Read the specialist SKILL.md** for detailed instructions

## Python Tools

All scripts in `product-team/*/scripts/` are stdlib-only and CLI-first:

```bash
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py --help
python3 product-team/product-strategist/scripts/okr_cascade_generator.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Feature prioritization | product-manager-toolkit |
| Sprint planning | agile-product-owner |
| OKR planning | product-strategist |
| User research | ux-researcher-designer |
| Design system | ui-design-system |
| Competitor analysis | competitive-teardown |
| Landing pages | landing-page-generator |
| SaaS boilerplate | saas-scaffolder |

## Cross-Domain Workflows

**Landing page + brand voice:** Before generating landing pages, run the brand voice analyzer to match copy tone:
```bash
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py brand_copy.txt --format json
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx
```
Voice profile maps to design styles: formal+professional→enterprise, casual+friendly→bold-startup, professional+authoritative→dark-saas, casual+conversational→clean-minimal.

## Rules

- Load only 1-2 skills per request — don't bulk-load
- Use Python tools for scoring and analysis
- Landing page scaffolder defaults to TSX output (Next.js + Tailwind). Use `--format html` for standalone HTML.

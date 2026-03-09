# C-Level Advisory — Codex CLI Instructions

When working on executive or strategic tasks, use the C-level advisory system:

## Routing

1. **Start with** `c-level-advisor/chief-of-staff/SKILL.md` — it routes to the right executive role
2. **For onboarding:** Run `c-level-advisor/cs-onboard/SKILL.md` to create company-context.md
3. **For big decisions:** Use `c-level-advisor/board-meeting/SKILL.md` for multi-role deliberation

## Python Tools

All scripts in `c-level-advisor/*/scripts/` are stdlib-only and CLI-first:

```bash
python3 c-level-advisor/cfo-advisor/scripts/burn_rate_calculator.py --help
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py --help
python3 c-level-advisor/ciso-advisor/scripts/risk_quantifier.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Strategy questions | chief-of-staff (routes) |
| Tech decisions | cto-advisor |
| Financial analysis | cfo-advisor |
| Product strategy | cpo-advisor |
| Marketing strategy | cmo-advisor |
| Security risk | ciso-advisor |
| Operations | coo-advisor |
| Revenue growth | cro-advisor |
| Hiring/culture | chro-advisor |
| Hard decisions | executive-mentor |

## Rules

- Run cs-onboard first to create company-context.md
- Load only 1-2 skills per request — don't bulk-load
- Use Python tools for quantitative analysis

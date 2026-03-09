# Business & Growth Skills — Codex CLI Instructions

When working on customer success, sales, or revenue tasks, use the business growth skill system:

## Routing

1. **Identify the task:** Customer health, sales engineering, revenue operations, or proposals
2. **Read the specialist SKILL.md** for detailed instructions

## Python Tools

All scripts in `business-growth/*/scripts/` are stdlib-only and CLI-first:

```bash
python3 business-growth/customer-success-manager/scripts/health_score_calculator.py --help
python3 business-growth/revenue-operations/scripts/pipeline_analyzer.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Customer health | customer-success-manager |
| RFP/PoC planning | sales-engineer |
| Pipeline analysis | revenue-operations |
| Proposals/contracts | contract-and-proposal-writer |

## Rules

- Load only 1-2 skills per request — don't bulk-load
- Use Python tools for scoring and metrics

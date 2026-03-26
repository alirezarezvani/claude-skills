# CISO Brief Generator

Generate CISO-level security briefs — risk posture summaries, incident narratives, and board-ready communications for non-technical executive audiences.

## When to use

- Preparing a quarterly board security brief
- Generating a monthly CISO report for executive leadership
- Writing an executive summary after a significant security incident
- Communicating a regulatory change and its business impact

## Quick Start

```bash
python scripts/ciso-brief-generator_tool.py --help
python scripts/ciso-brief-generator_tool.py --brief-type board_quarterly --output json
```

## Skill Level: L2

All briefs require human review and approval before distribution.

## Brief Types

- `board_quarterly` — 5-slide quarterly board brief
- `monthly_ciso_report` — 2-page monthly executive report
- `incident_executive_summary` — 1-page post-incident brief
- `regulatory_update` — 1-page regulatory change brief

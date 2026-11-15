# Monetize

Turn one person's career history into an honest, actionable side-income plan.

`monetize` is an Agent Skill for [Claude Code](https://github.com/anthropics/claude-code) and
any [Agent Skills](https://agentskills.io)-compatible agent. It runs a structured six-module
workflow — hidden-skills audit, opportunity scan, productization, leverage point, salary
ceiling, AI starter pack — and converges on one action the user can start this week.

## When to use it

- The user pastes a résumé or career history and asks what to do with it.
- The user asks how to earn more, start a side business, or monetize a skill.
- The user asks whether their salary is at the ceiling, or what a career move is worth.

## Output

Two files in the workspace:

| File | Contents |
|---|---|
| `monetize-profile.md` | The single source of background facts |
| `monetization-report.md` | Seven sections plus a source appendix and an unverified-estimate appendix |

## Honesty rules

- Income is always a range, never a point.
- Every number is verified and cited, or labeled "estimate, unverified".
- No income promises; competition and failure modes are stated.
- No gray-area methods (fake reviews, content scraping, unlicensed financial advice).

## Structure

```
SKILL.md                        # workflow, principles, anti-patterns
references/modules.md           # per-module detail and report template
references/market-calibration.md# regional defaults and sources
scripts/report_lint.py          # deterministic report linter
evals/evals.json                # behaviour cases
```

## Usage

```bash
# Claude Code
/plugin install monetize@...

# any agent with the skills CLI
npx skills add zhengqiuyang/monetize-skill
```

Inside an agent, just ask: "I've got 5 years in supply chain — what could I do on the side?"
The skill triggers on that phrasing and on the résumé case.

## Lint the report

```bash
python3 scripts/report_lint.py monetization-report.md --json
```

## License

MIT

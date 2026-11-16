# Monetize

Turns one person's career history into an honest, actionable side-income plan: hidden-skills
audit, opportunity scan with sourced numbers, experience productization, one leverage action,
salary-ceiling benchmark, and an AI side-hustle starter pack.

Ships as its own plugin, contributed by [@zhengqiuyang](https://github.com/zhengqiuyang):

```bash
/plugin install monetize@claude-code-skills
```

## When it applies

- The user pastes a résumé or career history and asks what to do with it.
- The user asks how to earn more, start a side business, or monetize a skill.
- The user asks whether their salary is at the ceiling, or what a career move is worth.

## What it produces

| File | Contents |
|---|---|
| `monetize-profile.md` | The single source of background facts, reused on later runs |
| `monetization-report.md` | Seven sections plus a source appendix and an unverified-estimate appendix |

## Workflow

Intake first — either a résumé parse or a three-round interview. Modules 1 and 2 (skills audit,
opportunity scan) run first so the direction can be confirmed, then modules 3 to 6 assemble the
full report: productization, leverage point, salary ceiling, AI starter pack.

## Honesty rules

- Income is always a range, never a point; the first three months are stated as far below steady state.
- Every number is verified with a source, or labeled "estimate, unverified" and listed in Appendix B.
- No income promises. Competition, failure modes and platform rules are stated.
- No gray-area methods: fake reviews, content scraping, unlicensed financial advice.

## Anti-patterns it refuses

| Anti-pattern | Why it fails |
|---|---|
| A generic "10 side hustles" list | Ignores the background; every item is interchangeable |
| Fabricated salary or market figures | Users decide on them; one invented number discredits the report |
| Ten options presented as equally good | The user asked for a decision, not a menu |
| Motivational tone, income promises | Replaces decision input with encouragement |
| Single-point income forecasts | False precision; always a range |

## Files

```
SKILL.md                         # workflow, principles, anti-patterns
references/modules.md            # per-module detail and report template
references/market-calibration.md # regional defaults and the sourcing rule
scripts/report_lint.py           # deterministic report linter
evals/evals.json                 # three behaviour cases
```

## Lint the report

```bash
python3 scripts/report_lint.py monetization-report.md --json
```

Checks that every required section is present, that each 30-day plan item carries a `-> outcome`
criterion, that every money figure (`$`, `CNY 500`, `500元`, `2万`, `5k/month`) has a `[n]` citation
or an "estimate" label, that each `[n]` resolves to Appendix A, and that Appendix B is filled when
the body mentions estimates. `--sample-bad` runs every finding path.

A clean lint proves the report's form, not its truth: an invented figure with an invented source
still passes, so the never-invent-a-number rule rests on the skill, and on whoever reads the report.

This plugin ships no agent or slash command on purpose: it is a single-pass skill that loads on
its description.

## Related skills

| Skill | Use it when | Do not use it when |
|---|---|---|
| `financial-analyst` | The task is company or portfolio financial analysis | The question is a person's income |
| `stock-analysis` | Public-equity valuation | The question is earned income |
| `passive-deal-screener` | Evaluating an investment deal | Building a side income |
| `contract-and-proposal-writer` | A chosen path needs a client contract or proposal | Choosing the path |

## License

MIT

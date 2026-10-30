# Skill evals

Do our skills change what Claude does? These scripts answer that with the real Claude Code CLI,
not by reading the SKILL.md files. They grew out of the v2.14 audit harness and run nightly in
`.github/workflows/skill-evals.yml`.

| Eval | Question | Cases |
|---|---|---|
| Trigger | Does the skill fire on realistic prompts that don't name it, and stay quiet on a near miss? | `cases/trigger_cases.json`: every installable skill (384 unique, dual-published copies counted once), 2 positive prompts + 1 near miss each |
| Behaviour | With the skill's plugin loaded, does the answer pass more of a checklist than without it? | `cases/behaviour_cases.json` + `fixtures/`: 6 cases from the v2.14 audit |

A trigger run is `claude -p <prompt> --plugin-dir <the skill's plugin> --max-turns 2` in an empty
folder with a throwaway config dir, so nothing installed on the machine and no CLAUDE.md leaks in.
It counts as fired when the transcript has a `Skill` call for that skill. A sibling skill or command
from the same plugin firing is counted separately (`PLUGIN_ONLY`), because it often means the
description is fine and the plugin routed the request elsewhere.

A behaviour run copies the fixture folder, runs the task twice (with the plugin, with none), and a
blind grader scores each transcript against the assertions with a JSON schema. The grader does not
know which arm it is reading.

## Cost and the nightly default

Measured from the v2.14 audit transcripts (Sonnet, Claude Code 2.1.3xx):

| Run | Mean cost |
|---|---|
| Trigger run, only the skill's plugin loaded | $0.08 |
| Trigger run, all 105 plugins loaded | $0.15 |
| Behaviour pair (with + without) | $0.19 |
| Grading a behaviour pair | $0.21 |

A full sweep of 384 skills, 3 prompts each, 2 runs per prompt, is about $185. Running that every
night would be about $5,500 a month, so the default is a rotation: **15 skills a night, 2 runs per
prompt, plus 2 behaviour cases, capped at $10 a night**. That is about $8 a night, $240 a month,
and covers the whole library every 26 nights. Every run also passes `--max-budget-usd`, and no new
run starts once the cap is spent. Raise `--count` for faster coverage, use `--runs 1` to halve
cost (single runs are noisy), or `--scenario full` to test the skill against all the others.

## Running it

```bash
python3 scripts/evals/inventory.py                                   # coverage
python3 scripts/evals/run_evals.py --plan                            # tonight's slice, nothing runs
python3 scripts/evals/run_evals.py --skills engineering/skills/rag-architect --runs 1
python3 scripts/evals/report.py eval-out/results.json --scoreboard board/
```

`run_evals.py` writes `eval-out/results.json` and every transcript under `eval-out/transcripts/`.
`report.py` prints a Markdown summary and, with `--scoreboard`, folds the run into
`scoreboard.json` and `SCOREBOARD.md`, flagging a skill that used to fire and now doesn't, a new
near-miss false fire, or a behaviour lift that dropped.

In CI the scoreboard lives on the `eval-results` branch (one commit per night, with that night's
results under `runs/<date>/`), and transcripts are kept as a workflow artifact for 30 days.

## Enabling the nightly job

1. Credentials, either one:
   - `CLAUDE_CODE_OAUTH_TOKEN` (recommended for maintainers on a Pro/Max plan): run
     `claude setup-token` locally and store the token as a repo secret. `claude.yml` and
     `claude-code-review.yml` already use this secret. Runs then draw on the subscription's usage
     limits instead of a bill, and the dollar figures in this file become a usage meter.
   - `ANTHROPIC_API_KEY`: pay per token at the prices above; set a spend limit in the Console.
2. Set the repo variable `SKILL_EVALS_ENABLED` to `true`.
3. Optional variables: `SKILL_EVALS_BUDGET_USD` (default 10), `SKILL_EVALS_MODEL` (default
   `sonnet`), `CLAUDE_CODE_VERSION` (default `2.1.308`, the npm `stable` tag when this was written).

Until step 2, only a manual "Run workflow" starts it. On a subscription, the nightly runs share
the same usage limits as your interactive sessions; the run starts at 03:17 UTC so it lands
outside working hours, and lowering `--count` or the budget trades coverage for headroom.

## Adding cases

- **Trigger:** `python3 scripts/evals/generate_trigger_cases.py --skills <path>` drafts cases for a
  new skill with Claude (about $0.01 each). Read the draft: the near miss must not be something the
  skill's description says it does. Hand-written cases carry `"origin": "v2.14-audit"`; drafted
  ones `"generated"`. Fixing a generated case means editing it and changing the origin to `"reviewed"`.
- **Behaviour:** add an entry to `cases/behaviour_cases.json` and a fixture folder. Write
  assertions a strong model without the skill would plausibly miss. On the current cases the
  grader often scores both arms full marks, so they show the skill does no harm but can't show a
  lift; harder cases are where the claim gets made.

Fixtures are deliberately broken inputs (an SQL-injectable route, a settings file with a fake
database password); they are test data, not code to run.

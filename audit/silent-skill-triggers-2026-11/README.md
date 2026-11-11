# Triggers for the 21 silent skills (2026-11)

Two description rewrites (#1106, #1111) left 21 skills that never loaded on their own. On their
prompts no other skill loaded either: the model answered directly. Wording was not the lever, so
this record decides, per skill, whether a slash command or a hook should invoke it, and when.

## Decision: a prompt hook, not new commands

**No new commands.** Every one of the 21 is already a slash command: Claude Code exposes each
plugin skill as `/<plugin>:<skill>` (and bare `/<skill>` when unambiguous), verified on 2.1.322 by
reading `slash_commands` from a session's init message. A command that only wraps a skill adds a
second name for the same thing and costs listing budget. agenthub, autoresearch-agent and remember
also already have task commands (`/hub-run`, `/ar-run`, `/si:remember`).

**What was missing is automatic invocation, and only a hook provides that.** Each of the eight
plugins that ship one of these skills now has a `UserPromptSubmit` hook, `hooks/skill_router.py`,
that matches the prompt against hand-written patterns in `hooks/skill_routes.json`. On a match it
adds one line naming the skill; otherwise it prints nothing.

Why `UserPromptSubmit` and not a tool or session event: the moment these skills help is when the
request arrives, before the model has committed to answering from memory. `PostToolUse` fires
after the work is done; `SessionStart` doesn't know the task. No other event was a better fit for
any of the 21, so none got a second hook.

Noise rules: one hint per plugin per prompt (highest-scoring route), each skill at most once per
session, prompts starting with `/` are skipped, no network or model calls, fails open. Cost is one
Python start per prompt per plugin (about 30 ms). Off switch: `SKILL_ROUTER=0` or
`SKILL_ROUTER_<PLUGIN>=0`.

## Per skill: when the hint fires

| Plugin | Skill | Fires when the prompt... | Deliberately not on |
|---|---|---|---|
| engineering-skills | tdd-guide | asks for TDD / test-first, to write tests *for* something, Jest/Pytest/Vitest mocks or fixtures, or to raise coverage | e2e/Playwright, pages, endpoints, forms (more specific skills), failing-test debugging |
| | senior-secops | asks if an app is secure, a security review/scan, a CVE id, patching a vulnerability, `npm audit`/`pip-audit`, SOC 2/PCI/HIPAA for an app, hardening | ISO 27001 programs, STRIDE, pen tests, access reviews |
| | gcp-cloud-architect | names a GCP service *and* hosting, deploying, migrating, scaling or cost | GCP mentions without an architecture or cost ask |
| | senior-devops | asks for a deploy pipeline, IaC infra setup, a Dockerfile, a cloud deploy to AWS/Azure/k8s, blue-green or canary | plain CI pipelines and Terraform modules (ci-cd-pipeline-builder, terraform-patterns fire on their own), Playwright, WCAG, IAM |
| | senior-frontend | bundle size, a slow React/Next.js UI, Core Web Vitals, a new React component or app, a frontend review | landing pages, agent competitions |
| | senior-backend | adding auth to an API, scaffolding REST/GraphQL, schema migrations, load tests, slow or N+1 queries | slow endpoints in general (performance-profiler), pen tests, LLM token cost |
| | senior-data-scientist | causal inference, "did X cause the lift", feature engineering, model metrics (AUC, F1, calibration), DiD/propensity | A/B test planning and reading (experiment-designer) |
| engineering-advanced-skills | self-eval | asks to rate or grade the work, "how did that go", an honest self-review | — |
| | codebase-onboarding | new to a codebase, how a repo is laid out, where to start reading, onboarding docs | — |
| | tech-debt-tracker | tech debt, what to refactor first, cleanup sprint, how messy the code is, legacy modernization | rewrite-vs-refactor and team questions (cto-advisor), OKRs |
| | minimalist | over-engineering, YAGNI, "don't go overboard", simplify/less code *about code* | "simplify" about prose |
| marketing-skills | content-humanizer | copy sounds like AI / robotic / not like us, humanize, AI tells, rewriting "delve"-style text | — |
| | copy-editing | proofread, copy-edit, editing in passes, polish/tighten/shorten named copy | code |
| | marketing-psychology | why people buy or hesitate, pricing/buyer psychology, persuasion terms tied to a page, offer or funnel | — |
| product-skills | experiment-designer | A/B or split tests, sample size, significance, MDE, how long to run, did the variant win | clinical trials, surveys, TAM sizing |
| | product-manager-toolkit | RICE, prioritizing features or backlog, what to build next, PRDs, interview synthesis | — |
| | roadmap-communicator | release notes, roadmap updates for execs/board/customers, stakeholder updates, "what we shipped" | changelogs from commits (changelog-generator) |
| c-level-skills | cto-advisor | should we rewrite, rewrite vs refactor, scaling the eng team, which stack to bet on, build vs buy, DORA, "as CTO" | — |
| agenthub | agenthub | best-of-N, several agents or attempts in parallel and keep the best | — |
| autoresearch-agent | autoresearch-agent | optimize against a metric until it stops improving, keep/reset loops, autoresearch | — |
| si | remember | "remember this", "don't forget this", note for next time/later, save so it isn't rediscovered | "remember to ..." instructions for the current task |

Where two skills overlap (experiment-designer and senior-data-scientist on A/B tests,
tech-debt-tracker and cto-advisor on debt), the patterns were split so a prompt gets one of them.

## Measurements

Patterns were written from each SKILL.md before any held-out prompt was read. First offline pass
(router only, no model) on the three case sets, then one tuning pass using recall misses from
`scripts/evals/cases/trigger_cases.json` only and precision misses from all sets:

| Case set | Positive prompts hinted, first pass | After tuning | Hints on the skills' own near misses |
|---|---|---|---|
| trigger_cases.json (tuning set) | 22/42 | 36/42 | 1 → 0 |
| heldout_cases.json | 20/42 | 21/42 | 4 → 0 |
| silent-48 heldout2 (least seen) | 15/42 | 17/42 | 5 → 0 |

Hints landing on other skills' prompts across all 1,167 held-out prompts: 39 → 15; most remaining
are the umbrella hinting on prompts for its own sub-commands (autoresearch-agent on `ar-status`).

Live, real Claude Code 2.1.322, Sonnet, only the skill's plugin loaded, heldout2 prompts, 2 runs
per positive prompt, 1 per near miss, final hint text:

| | Positive runs where the skill loaded | Near-miss runs where it loaded |
|---|---|---|
| Hook off (`SKILL_ROUTER=0`) | 2/84 | 0/21 |
| Hook on | **24/84** | 0/21 |

Of the 34 runs whose prompt got a hint, 24 loaded the skill (71%). In most of the other 10 the
test prompt referred to input it didn't include (no code, no pasted text, no prior work), and the
model asked for it. An earlier hint wording ("load it before answering") reached 19/84; saying
"first, before you answer or ask for missing input" moved it to 24/84. On the remaining 50 runs no
hint fired, because those prompts were too vague for a pattern ("my ops feel slow"), which is the
intended trade: a missed prompt costs nothing, a wrong hint costs attention.

Raw rows and scripts: project files `audits/silent-21-hooks-2026-11/`. Re-measure the offline
numbers with `python3 scripts/check_skill_router.py --cases <cases.json>`.

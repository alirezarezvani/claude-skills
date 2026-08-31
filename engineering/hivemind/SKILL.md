---
name: hivemind
description: Orchestrate free opencode workers from Claude Code to cut token costs. Use when delegating grunt work to a single worker or a parallel swarm (scout/coder/tester) with worktree isolation, benchmarking against opencode, or when the user says "spawn a worker", "swarm", "delegate to opencode", or "/oc".
---

# Hivemind: Claude Code as Orchestrator, opencode as Free Worker Swarm

Claude Code = brain (plans, reviews, merges). opencode = disposable workers on free models
(`opencode/mimo-v2.5-free` default; verified $0.00 per run).

## Prerequisites (external dependency)

This skill is a thin orchestration layer over **[opencode](https://opencode.ai)**, a
third-party CLI. It is not bundled — install and authenticate it yourself first:

| Requirement | Notes |
|---|---|
| Node.js >= 18 | The scripts use `fetch` and `node:timers/promises`. |
| `opencode` CLI on `PATH` | `npm i -g opencode-ai` (or the installer opencode documents). |
| An authenticated opencode account | `opencode auth login`. Workers run as your account. |
| Default model `opencode/mimo-v2.5-free` | A free tier offered by opencode, not by Anthropic. Availability, rate limits, and pricing are opencode's to change — override with `--model` at any time. |
| Windows only: `OPENCODE_GIT_BASH_PATH` | Point at `C:\Program Files\Git\bin\bash.exe`, set persistently. |

Nothing here calls the Anthropic API on the worker side; worker traffic goes to
opencode's endpoints. Do not delegate secrets or private code you would not send there.

## Setup

1. Put this skill folder wherever your agent loads skills from (e.g. `~/.claude/skills/hivemind`).
2. Export `HIVEMIND_HOME` pointing at that folder — the bundled slash commands use it:
   ```
   export HIVEMIND_HOME="$HOME/.claude/skills/hivemind"
   ```
3. Copy the bundled assets into place:
   - `assets/commands/*.md` -> `~/.claude/commands/` (the `/hive`, `/oc`, `/swarm`, ... entry points)
   - `assets/agents/*.md` -> `~/.config/opencode/agent/` (the scout / coder / tester worker personas)

Both copies are optional: everything the commands do can be driven by invoking
`scripts/oc-worker.mjs` directly, and any opencode agent name works with `--agent`.

Runtime state (`.runs/*.jsonl`) is written inside this folder and is gitignored.

## Components

| Path (relative to this skill dir) | Purpose |
|---|---|
| `scripts/oc-worker.mjs` | ONLY sanctioned way to invoke a worker. Hardened join point. |
| `scripts/oc-status.mjs` | Fleet progress from run logs (`oc-status.mjs <run-id>`) |
| `scripts/oc-aggregate.mjs` | Dedupe/synthesize N worker outputs; consensus findings first |
| `scripts/bench/run-bench.mjs` | Benchmark configs A (claude solo), B (opencode solo), C (orchestrated swarm) |
| `scripts/bench/grader-prompt.md` | Blind grading rubric (max 12 pts + PASS/FAIL gate) |
| `scripts/oc-verify.mjs` | Fan a worker's claims to a verifier on a DIFFERENT model; returns counts + `needs_review` |
| `scripts/or-worker.mjs` | Same contract over OpenRouter; for when opencode is down or the worker runs in CI |
| `assets/commands/` | Slash-command entry points to copy into `~/.claude/commands/` |
| `assets/agents/` | scout / coder / tester agent definitions for opencode |

Slash commands (ship in `assets/commands/`, copy to `~/.claude/commands/`):
- `/hive <task>` - AUTO-ROUTER. Classifies task -> single worker, generic swarm, or template. Default entry point; prefer this over manual routing.
- `/oc <task>` - single worker delegation
- `/swarm <task>` - generic parallel swarm
- `/review-panel <diff>` - 4-lens parallel review (correctness/security/performance/style) + consensus aggregation
- `/research-sweep <question>` - 3-5 parallel research angles, synthesized
- `/migration <task>` - batched per-worktree migration workers + sequenced merge
- `/test-fleet <target>` - partitioned parallel test runs with safety checks

Worker agents (ship in `assets/agents/`, copy to `~/.config/opencode/agent/`):
- **scout** - read-only research (no write/edit/bash)
- **coder** - implements one subtask in its worktree
- **tester** - runs tests only, never edits source

## Invocation contract

```
node "<skill-dir>\scripts\oc-worker.mjs" [--agent scout|coder|tester] [--dir <path>] [--model <p/m>] [--timeout 900] [--run <id> --label <name>] "TASK TEXT"
```

Returns exactly ONE compact JSON line:
`{ ok, result, tokens:{total,input,output,cache}, cost_usd, duration_ms, label, agent, model }`

On failure: `{ ok:false, stage:"args"|"exec"|"api"|"parse"|"empty", error }` with stderr capped at 300 chars.

`--run <id>` + `--label <name>` append lifecycle events (start/done/fail) to `.runs/<id>.jsonl`
inside this skill dir. Use them for EVERY swarm worker so progress is recoverable via
`oc-status.mjs` even after orchestrator context loss.

The script auto-manages the shared server: health-checks `127.0.0.1:4096`, spawns `opencode serve` if dead, waits 5s, falls back to cold start. Workers are idempotent against their `--dir`; re-run once on `ok:false` before giving up.

`HIVEMIND_SERVER_URL` overrides that address (default `http://127.0.0.1:4096`). It must be a
valid URL with a numeric port; anything else fails fast with a single `stage:"args"` JSON line
rather than reaching the spawned process.


## Verify instead of re-reading (do this before you trust a claim)

Re-checking every worker claim yourself costs more than the delegation saved. Send the
claims to a verifier instead:

```
node scripts/oc-verify.mjs --dir <same dir the worker saw> --claims findings.json --run <id>
```

Returns `{ confirmed, refuted, unsupported, unverified, needs_review[] }`. Read
`needs_review` only — those are the refuted and unsupported claims. Confirmed claims are
counts, not prose, and do not come back into your context.

HARD RULES for this stage:
- The verifier MUST run on a different model from the worker. Same model = same blind
  spots = a rubber stamp. Default is `nemotron-3.5-lightning-free` against a `mimo` worker.
- The verifier sees the FILES and the claims, never the worker's reasoning.
- It defaults to REFUTED when uncertain, because a false CONFIRMED is acted on unchecked.
- `unverified > 0` means the verifier skipped claims. Treat those as unverified, not passed.
- Still spot-check a sample yourself. Two free models agreeing is evidence, not proof.

## Providers: opencode is not always up

`opencode/*` free models return provider 404s and empty bodies often enough that an
unattended swarm cannot depend on them. `or-worker.mjs` speaks the identical one-JSON-line
contract over OpenRouter, so every downstream script works unchanged:

```
node scripts/or-worker.mjs --model google/gemini-2.5-flash --dir <path> --json "TASK"
```

Key comes from `OPENROUTER_API_KEY`, else `~/.claude/.openrouter_key`. Never paste a key
into a prompt, a committed file, or a transcript. In CI it comes from a repository secret.
Unlike opencode's free tier, OpenRouter bills — check the model's price before a fan-out.

## Choosing a model (measured, not guessed)

Free tiers failed six times out of six across both providers, for five different reasons:

| model | outcome |
|---|---|
| `opencode/nemotron-3.5-lightning-free` | provider 404 |
| `opencode/hy3-free` | empty body |
| `meta-llama/llama-3.3-70b-instruct:free` | 404 — silently stopped being free |
| `minimax/minimax-m3:free` | 429, rate-limited upstream |
| `nvidia/nemotron-3.5-lightning:free` (OpenRouter) | returned no content |
| `openrouter/free` with `--json` | could not produce parseable JSON, even after the corrective retry |

But `openrouter/free` WITHOUT `--json` answered correctly at zero cost. So the split is
capability, not availability:

- **Structured output (`--json`) — use a paid model.** Free models cannot reliably emit
  parseable JSON, and every hivemind contract downstream depends on it. A verified
  `google/gemini-2.5-flash` call cost $0.0000506. Fractions of a cent beat a pipeline that
  fails at 3am.
- **Prose, summaries, drafting — free is fine**, when a human is present to retry. Do not
  put a free model on a schedule.
- **Never hardcode a free model id.** They stop being free without warning. List what is
  actually free today with the public models endpoint (no key required):
  `curl.exe -s https://openrouter.ai/api/v1/models` and filter `pricing.prompt == 0`.

## Running workers in CI

A worker can run on a GitHub runner via `workflow_dispatch` so work continues when the
laptop is closed; see the reference workflow at github.com/Hanishchow/hivemind. Pass inputs
through the environment, never interpolated into a shell command line.

## Golden Rule (non-negotiable)

Raw opencode NDJSON streams must NEVER enter your context. All output arrives via the
script's single JSON line. Never pipe `opencode run --format json` directly into this
conversation; never re-implement what the script does.

## Single worker flow (/oc)

For one read-only question or small delegation: run oc-worker.mjs without worktrees.
Read-only tasks may omit `--agent`/`--dir`. Summarize `result` for the user.
If files were written: show `git diff` before letting the user commit.

## Swarm flow (multi-worker)

1. Decompose task into 2-5 INDEPENDENT subtasks (no shared files).
2. Writing workers get isolated worktrees FIRST: `git worktree add ../<repo>-wt-N -b swarm/N`.
3. Issue ALL worker invocations as PARALLEL Bash tool calls in ONE message.
4. Review every diff yourself (`git diff main...swarm/N`). YOU are the only merger.
5. Merge approved branches, remove worktrees, run tests.
6. Report table: subtask | agent | tokens | outcome + total worker tokens.

HARD RULES: workers never share directories; never delegate merging/reviewing;
escalate to your own Sonnet only when a free-model worker demonstrably fails twice.

## Benchmarking

```
node scripts\bench\run-bench.mjs --repo <project> [--configs a,b,c] [--task 1-5]
```
Appends JSONL records (ts, config, tokens, cost, duration) to `bench-results.jsonl`.
Grade artifacts blind with `grader-prompt.md` (grader sees only task spec + output).
Configs: A=claude solo baseline, B=opencode solo, C=claude orchestrating 2 workers.

## Fallback ladder (all flows)

1. Worker `ok:false` -> re-invoke once against the same dir.
2. Still failing -> orchestrator performs that subtask inline, marks it `[orchestrator-sourced]`.
3. opencode entirely down (`exec`/`api` twice) -> announce, abandon workers, do the task directly.
Never let a swarm fail a task that Claude could have done itself.

## Fleet patterns

Four reusable topologies ship as slash commands (see table above). Shared invariants:
parallel spawns in one message; `--run/--label` on every worker; aggregation via
`oc-aggregate.mjs` when 3+ workers produce findings; consensus beats single-lens claims;
worktree isolation whenever any worker writes.

## Windows notes (hard-won)

- Requires `OPENCODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe` (set persistently).
- The script resolves the REAL `opencode.exe` by parsing the npm `.cmd` shim — Node's
  EINVAL policy blocks spawning `.cmd` directly. Do not "simplify" resolver back to
  `where.exe` first-line.
- Free models: `opencode/mimo-v2.5-free`, `opencode/nemotron-3.5-lightning-free`,
  `opencode/hy3-free`. NOTE: `opencode-go/*` models require workspace billing — avoid.

## Known limits

- Free-tier rate limits can 429 under heavy swarms; space out retries.
- Worker quality varies; always review diffs. Scout answers are evidence-cited.
- Bench config C consumes real Claude tokens for orchestration (~1-2k/task).

## Anti-patterns

| Anti-pattern | Why it breaks | Do this instead |
|---|---|---|
| Piping `opencode run --format json` straight into the orchestrator | Raw NDJSON floods context — the exact cost the skill exists to avoid | Always go through `scripts/oc-worker.mjs`, which returns one compact JSON line |
| Two writing workers in one directory | Concurrent edits corrupt each other's diffs | One git worktree per writing worker, created before the spawn |
| Letting a worker merge, review, or approve its own branch | Free-tier workers are the least reliable judges of their own output | The orchestrator is the only merger and the only reviewer |
| Spawning workers sequentially, one per message | Loses the entire wall-clock benefit of a swarm | Issue every worker invocation as parallel calls in ONE message |
| Retrying a failing worker indefinitely | Burns rate limit and stalls the task | Retry once, then do the subtask inline and mark it `[orchestrator-sourced]` |
| Delegating secrets, credentials, or private code | Worker traffic leaves for opencode's endpoints | Keep sensitive context in the orchestrator; send workers only what is safe to share |
| Trusting `cost_usd: 0` as a permanent guarantee | The free tier belongs to opencode and can change | Re-check pricing before relying on zero cost for bulk work |

## Cross-references

- `engineering/llm-cost-optimizer` — decide *whether* a task is worth delegating before Hivemind decides *how*
- `engineering/agent-harness` — harness patterns for the orchestrator side of the loop
- `engineering/workflow-builder` — for deterministic pipelines that do not need independent worker judgment
- `engineering/skills` and `engineering/write-a-skill` — authoring conventions used by the worker agent definitions in `assets/agents/`

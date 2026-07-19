# Research digest: agent harnesses & agentic loops, 2025–2026 best practice

Compiled 2026-07-03 from web-verified sources. This digest informed the AR rubric
([RUBRIC.md](RUBRIC.md)) and the `engineering/agent-harness` skill's design; the full
per-source treatment lives in that skill's `references/` (3 docs, 21 citations).

## 1. The canonical loop

- **Anthropic, "Building Effective Agents" (Schluntz & Zhang, Dec 2024)** — workflows
  (predefined code paths) vs agents (model directs its own process); patterns: prompt
  chaining with gates, routing, parallelization, orchestrator-workers, evaluator-optimizer
  ("only when clear evaluation criteria exist"). Start simple; stopping conditions mandatory.
- **Anthropic, Claude Agent SDK (Sep 2025)** — the loop is **gather context → take action →
  verify work → repeat**; filesystem as context store; verification ladder: rules-based >
  visual > LLM-as-judge.
- **Anthropic, multi-agent research system (Jun 2025)** — subagent specs need objective,
  output format, tool guidance, and boundaries; effort scaled by rule (simple = 1 agent,
  3–10 calls) because early agents "spawned 50 subagents for simple queries".
- **Anthropic, "Effective harnesses for long-running agents" (Nov 2025)** — initializer
  expands the goal into `feature-list.json` (description + acceptance criteria + status);
  a worker wakes repeatedly, one feature per fresh-context session; all state on disk/git.
- **Anthropic, Agent Skills (Oct 2025)** — progressive disclosure (metadata → SKILL.md →
  files on demand); deterministic scripts for anything reliably automatable; build skills
  from observed agent failures.

## 2. Verification discipline

- **Jason Wei, "verifier's law" (Jul 2025)** — training/iterating AI on a task is
  proportional to its verifiability; invest in checks before agents.
- **SWE-agent (NeurIPS 2024)** — the highest-value guardrail was a linter rejecting invalid
  edits at write time; agents fail when the environment gives no feedback.
- **SWE-bench Verified (OpenAI 2024)** — even benchmark tests were too noisy without human
  validation; checks need declared reliability classes.
- **Claude Code best practices (Cherny, Apr 2025)** — strongest loop is test-driven: write
  the check first, confirm it fails, iterate against it.
- **Reflexion (Shinn 2023) + Huang et al. (ICLR 2024)** — self-critique helps only when
  grounded in external feedback; intrinsic self-correction often degrades answers.
  ⇒ **Deterministic validators are the primary gate; LLM-as-judge is a fallback.**
- **Anthropic reward-hacking research (Nov 2025)** — agents that game their checks
  generalize to worse behavior ⇒ the worker must never adjudicate or modify its own gates.

## 3. Loop patterns in production

- **Ralph Wiggum loop (Huntley, Jul 2025; now an official Claude Code plugin)** — same
  prompt to a fresh-context agent in a `while true` loop; filesystem + TODO + git as memory.
  Fresh context each iteration is the point; caps and completion criteria are added by
  practice.
- **Cognition, "Don't Build Multi-Agents" (Jun 2025)** — conflicting parallel decisions are
  the dominant multi-agent failure ⇒ **fan out readers/judges, serialize writers**.
- Caps as runtime errors: OpenAI Agents SDK `max_turns` / guardrail tripwires; LangGraph
  `recursion_limit`; Anthropic effort budgets.

## 4. State + memory

- Single JSON state file, atomic writes, schema version; narrative handoff separate from
  machine state; git as checkpoint layer; compaction with explicit preserve-lists
  (Anthropic context-engineering, Sep 2025; LangGraph checkpointers).

## 5. Failure modes → mitigations

| Failure | Mitigation |
|---|---|
| Infinite loops / runaway effort | Triple cap: iterations, wall-clock, budget — breach = terminal state, never silent |
| Verification theater / reward hacking | Gates read-only to the worker; controller re-runs checks itself; diff-scan for edits to test/gate paths |
| Goal drift / conflicting decisions | Single-writer rule; full-context handoffs |
| Context rot / silent truncation | Fresh-context iterations against durable disk state |

## 6. Manifest designs (goals → skills → verifications)

- **AGENTS.md** (agents.md, Aug 2025; Agentic AI Foundation / Linux Foundation, Dec 2025) —
  prose manifest for "how to build and verify here".
- **feature-list.json** (Anthropic long-running harness) — the closest published
  goal→tasks→verification manifest.
- **MCP** — declared tool registries as the harness's action space.
- GitHub Agentic Workflows / claude-code-action — declarative agent jobs with permissions +
  tool allowlists.

## Consensus (what this repo now implements)

Compile goals into explicit task lists with acceptance criteria; run stateless
fresh-context iterations against durable disk/git state; gate every promotion on
deterministic, agent-untouchable checks; serialize writes, parallelize reads; cap
everything; declare the goal→skill→verification mapping in a per-domain manifest.
Implemented as `engineering/agent-harness` (manifest builder + goal compiler + loop
controller, 18 committed domain manifests).

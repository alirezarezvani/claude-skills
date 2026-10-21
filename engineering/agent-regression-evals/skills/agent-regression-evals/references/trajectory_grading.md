# Grading the path, not only the answer

When `trajectory_checker.py` is worth running, which match mode to pick, and
how it fits beside outcome graders.

Confidence key: 🟢 verified on the primary source · 🟡 secondary · 🔴 convention.

## 1. Grade the outcome first

Anthropic's guidance is that it is "often better to grade what the agent
produced, not the path it took", and that strict step-sequence checks are "too
rigid": a valid alternative path fails them. 🟢 [Anthropic]
tau-bench grades outcome as the final database state matching the ground-truth
state, plus required information appearing in the reply. 🟢 [tau-bench]

So the default eval is an outcome check. Add a trajectory check only where the
path itself is a requirement:

| Path requirement | Example | Mode |
|---|---|---|
| A safety boundary | never call `delete_order` while answering a FAQ | any mode + `forbidden` |
| A required lookup | must read the refund policy before refunding | `superset` |
| An order that matters | read before write; auth before data access | `strict` |
| A closed tool set | the agent may only use these three tools | `subset` |
| Runaway loops | more than 12 calls is a bug | `max_calls` |

## 2. The four match modes

The names follow LangChain's `agentevals`, the most widely used open
implementation. 🟢 [agentevals]

- `strict` — same calls, same order, nothing extra.
- `unordered` — same multiset of calls, any order.
- `subset` — every actual call appears in the reference (no extras; skipping is allowed).
- `superset` — every reference call appears in the actual run (extras allowed).

Argument matching: `exact`, `subset` (listed keys must match, extra keys fine;
the default here) or `ignore`. agentevals defaults to `exact`; this skill
defaults to `subset` because IDs and timestamps in extra arguments make exact
matching brittle. 🔴 design choice.

## 3. Forbidden tools are not a match mode

A forbidden call blocks (exit 4) whatever the match mode and whatever the final
answer. A refund issued while answering a shipping question is a failure even
if the shipping answer was perfect. This is the cheapest high-value check in
the skill: one line per case.

## 4. Graders, in order of preference

1. **Code** — deterministic, cheap, reproducible; brittle to valid variation. 🟢 [Anthropic]
2. **Model** — flexible; non-deterministic, so calibrate against human labels before trusting it. 🟢 [Anthropic]
3. **Human** — the gold standard; slow, so spend it on calibrating 2 and on disputed cases. 🟢 [Anthropic]

Every script in this skill is a code grader. If your outcome grader is a model,
treat its disagreement with itself as a source of flakiness (see the flaky
cases reference) and run it on the same trial twice before blaming the agent.

## 5. Read the transcripts

"You won't know if your graders are working well unless you read the
transcripts." 🟢 [Anthropic] Before trusting a new trajectory spec, read five
passing and five failing trials by hand. A spec that fails valid paths teaches
the team to ignore the gate.

## 6. Where the cases come from

Start with 20-50 tasks drawn from real failures, balanced between what the
agent should do and what it should refuse to do. 🟢 [Anthropic] Regression
suites sit near 100%; capability suites start low and "graduate" into the
regression suite once saturated. 🟢 [Anthropic] SWE-bench's FAIL_TO_PASS /
PASS_TO_PASS split is the same idea applied to code: the fix must make the new
test pass and keep every old test passing. 🟡 [SWE-bench]

## Sources

1. Anthropic Engineering. *Demystifying evals for AI agents.* — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
2. Yao, S. et al. (2024). *τ-bench.* arXiv:2406.12045 — https://arxiv.org/abs/2406.12045
3. LangChain. *agentevals* (trajectory match evaluators). — https://github.com/langchain-ai/agentevals
4. Jimenez, C. E. et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024 — https://www.swebench.com/original.html
5. UK AI Security Institute. *Inspect* evaluation framework. — https://inspect.ai-safety-institute.org.uk/
6. OpenAI. *Evals* framework and registry. — https://github.com/openai/evals

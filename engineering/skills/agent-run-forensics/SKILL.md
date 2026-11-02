---
name: agent-run-forensics
description: Use when asked why an agent did something, what a past session or run changed, whether tests really passed, or to verify a session summary. Answers from the recorded transcript, not memory, with trace_finder.py, trace_timeline.py and claim_checker.py.
argument-hint: "[question about a past run] [--session ID | --trace PATH]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib CLIs over the session transcripts Claude Code and Codex already write (finder, timeline with a recorded/inferred causal chain, typed claim checker) plus a UserPromptSubmit hook that hands over this session's transcript path when a prompt asks about the past"
  distinct_from: "zero-hallucination-coder (facts about code not yet read; this is facts about work already done); self-eval (scores the quality of the current session); skill-retro (grades skill use across many sessions); collab-proof (who drove a session); session-handoff and handoff (forward-looking summaries, which this can check)"
---

# Agent Run Forensics

> **Portability:** 3 stdlib Python CLIs and one hook. Read-only, no network, no model calls.
> Secrets in transcripts are redacted in every output, with no switch to turn that off.

Agents are confidently wrong about their own history. Asked "why did you change
config.yaml?", an agent answers from what it remembers, and memory drops the
parts that matter: the test run that failed, the file a `sed -i` one-liner
rewrote, the edit made after the last green run. The harness recorded all of it.
This skill makes the answer come from that recording.

**The rule: when a question is about something that already happened, read the trace before answering.**

## Workflow

```bash
# 1 - Find the run (skip if the question is about this session: the hook gives you its path)
python scripts/trace_finder.py --since 7d --touched config.yaml
# 2 - Read it: what happened, in order, and which files changed
python scripts/trace_timeline.py --trace <path> --files        # SILENT = changed, never named by the agent
python scripts/trace_timeline.py --trace <path> --grep timeout # or --errors, --file PATH, --around N
# 3 - Walk back from the step in question
python scripts/trace_timeline.py --trace <path> --why 9
# 4 - Before repeating any summary as fact, check it
python scripts/claim_checker.py --trace <path> --claim "passed:pytest" --claim "not-edited:config.yaml"
```

**Step 3** prints two lists and you keep them apart in the answer:

| Label | Means | Example |
|---|---|---|
| `recorded` | The harness wrote it down when it happened | the command, its exit code, the agent's words in the same message |
| `inferred` | Derived now by a named rule | `prior-write`, `read-before-write`, `retry-after-failure`, `target-seen-in-output` |

Say "the trace shows" only for recorded edges. Name an inferred edge as inferred, with its rule.
The agent's own stated reason is recorded as a *claim*, not as the cause.

**Step 4** turns each sentence of a summary into a typed claim (`ran:`, `not-run:`,
`passed:`, `failed:`, `edited:`, `not-edited:`, `read:`). `STALE` means the tests
passed but files changed afterwards; `PARTIAL` means exit 0 came from the last
command of a pipe or `;` chain. Exit 4 is a contradiction: correct the account first.

## Hard rules

- **No trace, no answer.** If the finder returns nothing (exit 2), say the run is not recorded here. Do not reconstruct it.
- **Cite steps.** Every factual sentence about the run points at a step number.
- **Recorded and inferred stay separate.** Never merge them into one confident sentence.
- **Shell effects are inferred** unless the harness diff (`bashEditDiff`) confirms them. A command's text says what it was meant to do, not what it did.
- **Exit 0 of a compound line is the last command's.** `pytest | tee log` passing says nothing about pytest.
- **Quote no secrets.** Outputs are redacted; do not paste raw transcript lines around the redaction.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/trace_finder.py` | Lists recorded sessions by repo, window, touched file, text | 0 found · 2 none · 3 bad input |
| `scripts/trace_timeline.py` | Numbered steps, `--files` table, `--why STEP` chain | 0 · 2 filter matched nothing · 3 |
| `scripts/claim_checker.py` | Typed claims vs the recording | 0 all supported · 2 weak · 3 · 4 contradicted |

All support `--help`, `--sample` and `--output json`. `trace_core.py` is the shared parser.
The plugin's `UserPromptSubmit` hook (`hooks/forensics_hint.py`) adds one line naming this
session's transcript when a prompt asks about past work; disable it with `AGENT_RUN_FORENSICS_HOOK=0`.

## References and assets

- [`references/trace_sources.md`](references/trace_sources.md): where each harness records, what is in a record, retention and limits (7)
- [`references/recorded_vs_inferred.md`](references/recorded_vs_inferred.md): why self-reports are not evidence, and the inference rules (7)
- [`references/claim_verification.md`](references/claim_verification.md): turning a summary into claims, verdicts, and how to correct an account (7)
- [`assets/forensic_answer_template.md`](assets/forensic_answer_template.md): the shape of an answer
- [`assets/claims_example.txt`](assets/claims_example.txt): a claims file for `--claims-file`

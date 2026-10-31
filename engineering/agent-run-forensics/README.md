# agent-run-forensics

Answer "why did the agent do that?" from the recording of the run, not from
anyone's memory of it.

Agents are confidently wrong about their own history. A summary written from
memory loses the failed test run, the file a `sed -i` one-liner rewrote, and the
edit made after the last green run. Claude Code and Codex already record every
tool call, argument, result and exit code on disk. This plugin reads that record.

## What it does

| Script | Job | Exit codes |
|---|---|---|
| `trace_finder.py` | Finds the run: by repo, `--since 7d`, `--touched config.yaml`, `--grep "rm -rf"` | 0 found · 2 not recorded |
| `trace_timeline.py` | Numbered steps with exit codes; `--files` flags changes the agent never named (SILENT); `--why STEP` walks back with each edge labelled **recorded** or **inferred** by a named rule | 0 · 2 nothing matches |
| `claim_checker.py` | Checks a summary's claims (`passed:pytest`, `not-edited:config.yaml`, ...): SUPPORTED, STALE (edited after the green run), PARTIAL (exit 0 of a pipe's last command), CONTRADICTED | 0 · 2 weak · 4 contradicted |

A `UserPromptSubmit` hook adds one line when a prompt asks about past work
("why did you...", "did the tests actually pass?"), naming this session's
transcript path. It stays silent otherwise and never blocks. Disable it with
`AGENT_RUN_FORENSICS_HOOK=0`.

Everything is stdlib Python, read-only, with no network and no model calls.
Secret-shaped strings are redacted in every output, with no off switch.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install agent-run-forensics@claude-code-skills
```

Commands: `/cs-run-forensics <question>` and `/cs-check-claims`. Agent: `cs-run-forensics`.
Try it without a real session: `python3 skills/agent-run-forensics/scripts/claim_checker.py --sample`.

## Limits

- Shell effects are read from command text, so they are **inferred** unless Claude Code's own `bashEditDiff` confirms them. A command that writes through a script (`python fix.py`) shows no effect at all.
- The transcript is the agent's view: changes made in your terminal, CI or by a teammate are not in it.
- Claude Code deletes old transcripts after `cleanupPeriodDays`; an old run may be gone.
- Codex support is parsed from the rollout format and tested on a synthetic fixture, not on real Codex sessions yet.
- No replay. This reads what happened; it does not re-run it.

## Origin

The idea came from PR #1016, which proposed the same discipline around the
proposer's own npm recorder and was closed under this repo's no-vendor rule.
This is an independent build over the recordings the harnesses already keep; no
code or text from that PR or its tool was used.

MIT © Alireza Rezvani

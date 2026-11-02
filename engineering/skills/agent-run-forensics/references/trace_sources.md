# Trace sources: where agent runs are recorded

The scripts read files the harnesses already write. Nothing is installed, no
recorder runs alongside the agent, and nothing leaves the machine.

## Where each harness records

| Harness | Location | Format | Confidence |
|---|---|---|---|
| Claude Code (interactive, `-p`) | `~/.claude/projects/<cwd with / as ->/<session-id>.jsonl` | one JSON record per line: `user`, `assistant`, plus bookkeeping types | 🟢 docs + observed |
| Claude Code subagents | `~/.claude/projects/<project>/<session>/subagents/*.jsonl` | same, records carry `isSidechain: true` | 🟢 observed |
| Claude Code `--output-format stream-json` | wherever you redirected stdout | same message shapes, `session_id` instead of `sessionId` | 🟢 observed |
| Codex CLI | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | `session_meta`, `response_item` (`message`, `function_call`, `function_call_output`) | 🟡 parser tested on a synthetic fixture only |

`CLAUDE_CONFIG_DIR` moves the Claude Code tree (settings, session history and
plugins move with it); `CODEX_HOME` moves Codex's. The scripts respect both.

## What a record holds, and what it does not

Recorded, per tool call: the tool name and full arguments (command, file path,
old and new strings), the result text, `is_error`, and for shell calls a line
`Exit code N` when the command failed. Claude Code sets `is_error` on a non-zero
exit, so `is_error: false` on a shell call is read as exit 0. When a shell
command changed a file Claude Code was tracking, the result carries a
`bashEditDiff` with that file's path; the scripts treat that as a recorded write.

Not recorded: the filesystem itself. A command's text says what it was meant to
do. `sed -i ... config.yaml` that exited 0 almost certainly rewrote the file, but
the trace holds the command, not the bytes. That is why shell effects are labelled
`inferred` unless the harness diff confirms them.

Not recorded either: the model's hidden reasoning (thinking blocks may be absent
or redacted), anything done outside the agent (your own terminal, CI, a teammate),
and the current turn when a hook fires: the hooks reference notes the transcript
is written asynchronously and can lag the conversation.

## Retention

Claude Code deletes old transcripts after `cleanupPeriodDays` (a settings key;
check your value and the data-retention page). A question about last month may
have no trace left. The finder says so (exit 2) instead of guessing.

## Shapes the parser handles

- Text blocks starting with harness markers (`<system-reminder>`, `<command-name>`,
  interrupted-request notices) are dropped from the prose, not from tool calls.
- A heredoc body (`python3 - <<'EOF' ... EOF`) is data, not shell syntax, so a `>`
  inside it is never read as a redirect.
- `cd dir && ...` moves the working directory for the rest of that line.
- Per-record `cwd` is used for each call, because the shell's directory can change
  between calls.

## Sources

1. Claude Code hooks reference: common input fields, `transcript_path`, asynchronous transcript writes, `additionalContext` for UserPromptSubmit. https://code.claude.com/docs/en/hooks 🟢
2. Claude Code settings reference: `cleanupPeriodDays` controls how long transcripts are kept. https://code.claude.com/docs/en/settings-reference 🟢
3. Claude Code settings: `CLAUDE_CONFIG_DIR` relocates settings, session history and plugins. https://code.claude.com/docs/en/settings 🟢
4. Claude Code headless mode and `--output-format stream-json`. https://code.claude.com/docs/en/headless 🟢
5. OpenAI Codex CLI repository (session rollouts under `~/.codex/sessions`). https://github.com/openai/codex 🟡
6. JSON Lines format. https://jsonlines.org/ 🟢
7. OpenTelemetry semantic conventions for generative AI (spans for agent and tool calls; the direction recorders are heading). https://opentelemetry.io/docs/specs/semconv/gen-ai/ 🟢

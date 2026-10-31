# commit-craft

Turn a tangled working tree into a commit series a reviewer can read one commit
at a time: one logical change per commit, in an order where each builds, with no
secrets and a message that says why.

## What it does

| Script | Job | Blocks on |
|---|---|---|
| `commit_planner.py` | Groups the working tree into commits: manifest with lockfile, pure moves, formatting, each module's change with its tests, docs, CI. Prints the `git add` commands | `.env`, keys, tfstate in the tree (held back) |
| `secret_gate.py` | Scans the lines a commit adds (staged, or a range before push) | Provider tokens, high-entropy secrets, sensitive files, conflict markers |
| `message_linter.py` | Lints one message or a series, matching the repo's convention | Vague subjects, 72+ char subjects, large changes with no body, fixup!/WIP left before push |

All three are stdlib Python, call `git` read-only, and never stage, commit or push.
Each supports `--help`, `--sample` and `--output json`.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install commit-craft@claude-code-skills
```

Commands: `/cs-commit-craft` (plan, gate, commit a series) and `/cs-commit-check`
(check staged work or a range). Agent: `cs-commit-craft`.

Optional git hooks run the gate and linter on every commit and push:

```bash
export COMMIT_CRAFT_SCRIPTS=/path/to/commit-craft/skills/commit-craft/scripts
cp skills/commit-craft/assets/hooks/{pre-commit,commit-msg,pre-push} .git/hooks/
```

## Limits

- The planner cannot read intent. It never chooses feat or fix, and two unrelated fixes in one file need `git add -p`.
- The secret gate is pattern matching at commit time: no live-key verification and no history audit. Use an open-source history scanner for that.
- `WHY_MISSING` is a keyword heuristic and only warns.

## Origin

Proposed in issue #1004. Built independently from public sources (Git
`SubmittingPatches`, the Linux kernel patch guide, Google's *Small CLs*,
Conventional Commits 1.0.0, the OWASP Secrets Management Cheat Sheet); no code or
text from the proposer's pack was used.

MIT © Alireza Rezvani

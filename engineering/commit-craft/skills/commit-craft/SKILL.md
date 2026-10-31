---
name: commit-craft
description: Use when committing a mix of changes, before a push, or when asked to split work into commits or write commit messages. Plans a reviewable series, blocks staged secrets and .env files, and lints messages with commit_planner.py, secret_gate.py and message_linter.py.
argument-hint: "[repo path | diff file | commit range]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts over git (series planner, staged-secret gate, message and series linter) with blocking exit codes and git hooks; rules cited to Git SubmittingPatches, the Linux kernel patch guide, Google's Small CLs, Conventional Commits 1.0.0 and the OWASP Secrets Management Cheat Sheet"
  distinct_from: "changelog-generator (turns merged commits into release notes; this shapes the commits before they exist); pr-review-expert and code-reviewer (review a pushed change); git-worktree-manager (parallel branches); security-guidance (warns on risky code patterns while editing, not on secrets at commit time)"
---

# Commit Craft

> **Portability:** 3 stdlib Python scripts that call `git` read-only. No network.
> **The scripts never stage, commit or push.** You do, one group at a time, after the gate passes.

Agents leave large mixed diffs: a feature, a reformat, a dependency bump and a
stray `.env`, all in one tree. Committed as one blob, that diff cannot be
reviewed, reverted or bisected. This skill turns it into a series where each
commit is one logical change, builds on its own, holds no secrets and says why.

## Workflow

```bash
# 1 - Plan: which commits, in which order, staged how?
python scripts/commit_planner.py                 # working tree vs HEAD, untracked included
# 2 - For each group: stage exactly its files, then gate what is staged
git add -- <files of group N>                     # or git add -p for MIXED_FORMATTING files
python scripts/secret_gate.py                     # blocks before the commit exists
# 3 - Write the message, lint it, commit
python scripts/message_linter.py -m "<message>" --staged && git commit -m "<message>"
# 4 - Before push: the whole series, and proof every commit builds
python scripts/message_linter.py --range @{upstream}..HEAD
git rebase -x "<test command>" @{upstream}
```

**Step 1** groups files: manifest with lockfile, pure moves, whitespace-only
files, each module's changes with their tests, then docs and CI. It holds back
`.env`, keys and tfstate (exit 4), flags files that mix formatting with real
hunks, and flags a move whose callers' import edits sit in another group, since
that commit would not build. It never picks feat vs fix: decide from what the change does.

**Step 2** scans only the added lines of what is staged: provider-shaped
tokens, high-entropy values assigned to key/secret/token/password, sensitive
files and conflict markers. Output is redacted. A false positive is waived in
`.commit-craft-allow` by fingerprint or path, with a reason.

**Step 3** blocks vague subjects ("fix", "update"), subjects over 72 characters,
no blank line after the subject, and a change of 40+ lines or 4+ files with no
body. It enforces Conventional Commits only if the repo already uses them.

**Step 4** also blocks fixup!/squash!/WIP commits and warns on duplicates and
revert pairs. Install `assets/hooks/` to run steps 2 to 4 on every commit and push.

## Hard rules

- **Never `git add -A` or `git add .` on a mixed tree.** Stage each group by name or by hunk.
- **A blocked gate means no commit.** Remove the value and load it at runtime. Never `--no-verify`, never waive a real secret.
- **A pushed secret is rotated first.** Deleting it in a new commit leaves it in history (`references/secret_response.md`).
- **Each commit builds.** Tests ride with their change; moves carry their callers.
- **The body says why.** The diff already says what.
- **Rewrite only unpushed history.** Rebasing or amending shared commits is the user's call.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/commit_planner.py` | Groups, order, staging commands, MOVE/MIXED/SIZE flags | 0 one commit · 2 split · 3 bad input · 4 secrets file held back |
| `scripts/secret_gate.py` | Staged or range scan for credentials, sensitive files, conflict markers | 0 · 2 warnings · 3 · 4 blocked |
| `scripts/message_linter.py` | One message (`-m`, `--message-file`) or a series (`--range`) | 0 · 2 warnings · 3 · 4 blocked |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/commit_series_design.md`](references/commit_series_design.md): split, order and verify, with sources (7)
- [`references/message_discipline.md`](references/message_discipline.md): subject, why-body, breaking changes, trailers (7)
- [`references/secret_response.md`](references/secret_response.md): what the gate catches, its limits, and the leak response order (7)
- [`assets/hooks/`](assets/hooks/): `pre-commit`, `commit-msg`, `pre-push`
- [`assets/commit-craft-allow.example`](assets/commit-craft-allow.example): waiver format
- [`assets/series_checklist.md`](assets/series_checklist.md): pre-push sign-off

---
title: "Hermes Agent Skills Guide (2026)"
description: "Install {{ count.hermes }} claude-skills into Nous Research's Hermes Agent with one sync script. Native SKILL.md format, no conversion, install-tested in CI."
---

# Hermes Agent Skills Guide

[Hermes Agent](https://github.com/NousResearch/hermes-agent) from Nous Research reads `SKILL.md` files natively, with the same YAML frontmatter and folder layout Claude Code uses. Our skills install without conversion: a sync script symlinks {{ count.hermes }} of them into `~/.hermes/skills/claude-skills/<domain>/<skill>/`.

!!! tip "Install-tested in CI"
    Every pull request that changes skills installs the real `hermes-agent` package into an empty home directory, runs the sync, and fails unless `hermes skills list` shows every skill the sync installed.

## Install

```bash
# 1. Hermes itself (a virtualenv keeps it isolated)
python3 -m venv ~/.venvs/hermes
~/.venvs/hermes/bin/pip install hermes-agent
export PATH="$HOME/.venvs/hermes/bin:$PATH"

# 2. Our skills
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
python3 scripts/sync-hermes-skills.py
```

Configure a model provider for Hermes as described in its [README](https://github.com/NousResearch/hermes-agent).

## Verify

```bash
hermes skills list | grep -c claude-skills
# Expected: {{ count.hermes }}
```

## Useful flags

| Flag | What it does |
|---|---|
| `--domain engineering` | Install one domain only |
| `--copy` | Copy files instead of symlinking (containers, shared filesystems) |
| `--target <dir>` | Install somewhere other than `~/.hermes/skills` |
| `--dry-run --verbose` | Show what would be installed without writing anything |
| `--json` | Machine-readable summary |

## Update

```bash
cd claude-skills
git pull
python3 scripts/sync-hermes-skills.py
```

Existing links are kept and new skills are added.

## Related

- [Multi-tool integrations](../integrations.md#hermes-agent) for troubleshooting and the full support matrix.
- [Mistral Vibe guide](mistral-vibe-skills-guide.md), the other agent that reads `SKILL.md` natively.

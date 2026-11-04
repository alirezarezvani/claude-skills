---
title: "Mistral Vibe Skills Guide (2026)"
description: "Install {{ count.vibe }} claude-skills into Mistral Vibe with one script. Agent Skills format, no conversion, install-tested in CI."
---

# Mistral Vibe Skills Guide

[Mistral Vibe](https://github.com/mistralai/mistral-vibe) is Mistral AI's open-source CLI coding agent. It follows the [Agent Skills standard](https://docs.mistral.ai/mistral-vibe/agents-skills), the same `SKILL.md` format Claude Code uses, so our skills need no conversion. The installer symlinks {{ count.vibe }} of them into `~/.vibe/skills/<skill>/`.

!!! tip "Install-tested in CI"
    Every pull request that changes skills installs the real `mistral-vibe` package into an empty home directory, runs `scripts/vibe-install.sh`, and fails unless Vibe's own skill manager loads every skill it installed.

## Install

```bash
# 1. Vibe itself
pip install mistral-vibe
vibe --version

# 2. Our skills
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/vibe-install.sh
```

Vibe works with Mistral's hosted models (`MISTRAL_API_KEY`) or a self-hosted endpoint; see the [Vibe docs](https://docs.mistral.ai/mistral-vibe/terminal).

!!! note "Flat layout"
    Vibe only scans one level deep, so skills land directly in `~/.vibe/skills/<skill>/`, not under a `claude-skills/` folder. The legacy `--nested` layout is only discovered if you add its path to `skill_paths` in `~/.vibe/config.toml`.

## Verify

```bash
ls ~/.vibe/skills | wc -l     # about {{ count.vibe }}, plus any skills you already had
vibe                          # then type /skills
```

## Useful flags

`scripts/sync-vibe-skills.py` accepts the same flags as the Hermes sync:

| Flag | What it does |
|---|---|
| `--domain engineering` | Install one domain only |
| `--copy` | Copy files instead of symlinking |
| `--target <dir>` | Install somewhere other than `~/.vibe/skills` |
| `--dry-run --json` | List the skill folders it would manage, without writing |

## Update

```bash
cd claude-skills
git pull
./scripts/vibe-install.sh
```

## Uninstall

```bash
python3 scripts/sync-vibe-skills.py --dry-run --json   # lists the folders it manages
```

Remove those folders from `~/.vibe/skills/`. Skills you installed from elsewhere are not touched.

## Related

- [Multi-tool integrations](../integrations.md#mistral-vibe) for the full support matrix.
- [Hermes Agent guide](hermes-agent-skills-guide.md).

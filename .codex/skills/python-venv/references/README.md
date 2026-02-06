# Skill: Python Virtual Environment

Enforce virtual environment usage for Python projects that require third-party packages.

Works with: **OpenCode**, **Claude Code**, **Cursor**, **Cline**, and other AI coding assistants.

[中文说明](README_CN.md)

## Features

- ✅ Require venv when installing packages or using third-party dependencies
- ✅ Reuse existing virtual environment (`.venv`, `venv`, `env`, `.env`)
- ✅ Auto-create if not exists
- ✅ Support `uv` (recommended) with fallback to standard `venv`
- ✅ Support Conda/Mamba environments
- ✅ Cross-platform (Linux, macOS, Windows)
- ✅ **Skip venv for simple stdlib-only commands**

## When venv is Required

| Scenario | Required? |
|----------|-----------|
| `pip install` / `uv pip install` | ✅ YES |
| Running scripts with third-party imports | ✅ YES |
| Projects with `requirements.txt` / `pyproject.toml` | ✅ YES |

## When venv is NOT Required

| Scenario | Example |
|----------|---------|
| Simple stdlib one-liner | `python3 -c "print('hello')"` |
| Built-in modules only | `python3 -c "import json; ..."` |
| Version check | `python3 --version` |

## Installation

### OpenCode
```bash
cd ~/.config/opencode/skills
git clone https://github.com/cikichen/skill-python-venv.git python-venv
```

### Claude Code
```bash
cd ~/.claude/skills
git clone https://github.com/cikichen/skill-python-venv.git python-venv
```

### Other AI Assistants
Copy `SKILL.md` to your assistant's custom instructions or skills directory.

## Quick Reference

### Linux/macOS
```bash
# Reuse existing or create new (with uv fallback to venv)
[ -d .venv ] && source .venv/bin/activate || { command -v uv &>/dev/null && uv venv || python3 -m venv .venv; source .venv/bin/activate; }
```

### Windows PowerShell
```powershell
if (Test-Path .venv) { .\.venv\Scripts\Activate.ps1 }
elseif (Get-Command uv -ErrorAction SilentlyContinue) { uv venv; .\.venv\Scripts\Activate.ps1 }
else { python -m venv .venv; .\.venv\Scripts\Activate.ps1 }
```

## Project Type Detection

| File | Install Command |
|------|-----------------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `pip install -e .` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` + `uv.lock` | `uv sync` |
| `environment.yml` | `conda env create -f environment.yml` |

## License

MIT

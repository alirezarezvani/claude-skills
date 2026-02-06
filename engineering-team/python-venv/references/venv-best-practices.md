# Python Virtual Environment Best Practices

Reference guide for virtual environment management in Python projects.

Original community skill: [cikichen/skill-python-venv](https://github.com/cikichen/skill-python-venv)

## Why Virtual Environments Matter

- **Dependency isolation** -- Each project gets its own package versions, preventing conflicts
- **Reproducibility** -- Exact dependency sets can be captured and recreated
- **System protection** -- Avoids polluting the global Python installation
- **Team consistency** -- All developers work with the same dependency tree

## Tool Comparison

| Tool | Speed | Ecosystem | Best For |
|------|-------|-----------|----------|
| **uv** | Fastest (Rust-based) | pip-compatible | New projects, CI/CD |
| **venv** | Standard | Built into Python 3.3+ | Universal fallback |
| **virtualenv** | Fast | pip-compatible | Legacy Python 2/3 support |
| **conda** | Moderate | conda + pip | Data science, non-Python deps |
| **poetry** | Moderate | pyproject.toml | Dependency resolution, publishing |
| **pipenv** | Moderate | Pipfile | Application development |

## Detection Priority

When checking for existing virtual environments, use this priority order:

1. `.venv/` -- Most common convention (PEP 405 recommendation)
2. `venv/` -- Also widely used
3. `env/` -- Sometimes used, less specific
4. `.env/` -- Avoid confusion with dotenv files (`.env` as a file stores environment variables)
5. Conda: Check `CONDA_PREFIX` environment variable

**Important:** Always check for `VIRTUAL_ENV` environment variable first -- if set, a venv is already active.

## Cross-Platform Considerations

### macOS
- System Python (`/usr/bin/python3`) is managed by Apple and should not be modified
- Use Homebrew Python or `pyenv` for development
- `uv` installs via `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Linux
- Distribution Python is managed by the package manager -- never `sudo pip install`
- Some distros require `python3-venv` package: `sudo apt install python3-venv`
- `uv` installs via `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Windows
- PowerShell execution policy may block activation scripts
- Use `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` if needed
- Prefer PowerShell over CMD for better venv support
- Don't mix Windows venv with WSL -- create separate environments

## Common Pitfalls

1. **Global pip install** -- Always activate venv before `pip install`
2. **Stale venv** -- If Python was upgraded, recreate the venv (symlinks break)
3. **Committing venv to git** -- Add `.venv/` and `venv/` to `.gitignore`
4. **Missing activation** -- Running `python` without activating still uses system Python
5. **Overwriting existing venv** -- Always check before creating; existing venv may have packages already installed
6. **Mixing package managers** -- Don't use both `pip` and `conda` in the same environment without care

## Project File Reference

| File | Manager | Lock File | Notes |
|------|---------|-----------|-------|
| `requirements.txt` | pip | `requirements.txt` itself | Pin versions with `==` |
| `pyproject.toml` | pip/uv/poetry/flit | Varies by tool | Modern standard (PEP 517/518) |
| `setup.py` | pip | None (legacy) | Being replaced by pyproject.toml |
| `Pipfile` | pipenv | `Pipfile.lock` | Hash-verified installs |
| `environment.yml` | conda | None | Can include pip dependencies |
| `uv.lock` | uv | `uv.lock` | Fast, deterministic resolution |
| `poetry.lock` | poetry | `poetry.lock` | Cross-platform lock file |

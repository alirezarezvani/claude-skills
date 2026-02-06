# Skill: Python 虚拟环境

为需要第三方包的 Python 项目强制使用虚拟环境。

适用于：**OpenCode**、**Claude Code**、**Cursor**、**Cline** 及其他 AI 编程助手。

[English](README.md)

## 功能

- ✅ 安装包或使用第三方依赖时必须使用 venv
- ✅ 复用现有虚拟环境（`.venv`、`venv`、`env`、`.env`）
- ✅ 不存在时自动创建
- ✅ 支持 `uv`（推荐），自动 fallback 到标准 `venv`
- ✅ 支持 Conda/Mamba 环境
- ✅ 跨平台（Linux、macOS、Windows）
- ✅ **简单的标准库命令可跳过 venv**

## 何时需要 venv

| 场景 | 需要? |
|------|-------|
| `pip install` / `uv pip install` | ✅ 是 |
| 运行使用第三方库的脚本 | ✅ 是 |
| 有 `requirements.txt` / `pyproject.toml` 的项目 | ✅ 是 |

## 何时不需要 venv

| 场景 | 示例 |
|------|------|
| 简单的标准库单行命令 | `python3 -c "print('hello')"` |
| 仅使用内置模块 | `python3 -c "import json; ..."` |
| 版本检查 | `python3 --version` |

## 安装

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

### 其他 AI 助手
将 `SKILL.md` 复制到你的助手的自定义指令或技能目录。

## 快速参考

### Linux/macOS
```bash
# 复用现有或创建新的（uv 优先，fallback 到 venv）
[ -d .venv ] && source .venv/bin/activate || { command -v uv &>/dev/null && uv venv || python3 -m venv .venv; source .venv/bin/activate; }
```

### Windows PowerShell
```powershell
if (Test-Path .venv) { .\.venv\Scripts\Activate.ps1 }
elseif (Get-Command uv -ErrorAction SilentlyContinue) { uv venv; .\.venv\Scripts\Activate.ps1 }
else { python -m venv .venv; .\.venv\Scripts\Activate.ps1 }
```

## 项目类型检测

| 文件 | 安装命令 |
|------|----------|
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `pip install -e .` |
| `pyproject.toml` + `poetry.lock` | `poetry install` |
| `pyproject.toml` + `uv.lock` | `uv sync` |
| `environment.yml` | `conda env create -f environment.yml` |

## 许可证

MIT

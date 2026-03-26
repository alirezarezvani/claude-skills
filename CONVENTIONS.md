# Repository Conventions

**Mandatory conventions for the claude-code-skills repository.** Every contributor — human or AI coding agent — must follow these rules. PRs that violate them will be closed.

For contribution workflow and how to submit PRs, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 1. Skill Structure

Every skill is a directory under one of the 9 domain folders:

```
<domain>/<skill-name>/
├── SKILL.md                    # Required — main skill file
├── .claude-plugin/
│   └── plugin.json             # Optional — for standalone installs
├── scripts/                    # Optional — Python CLI tools
│   └── *.py
├── references/                 # Optional — detailed reference docs
│   └── *.md
└── assets/                     # Optional — templates, examples
```

### Domains

| Directory | Category | Current Count |
|-----------|----------|---------------|
| `engineering/` | POWERFUL-tier advanced engineering | 35 |
| `engineering-team/` | Core engineering roles | 30 |
| `marketing-skill/` | Marketing & growth | 43 |
| `c-level-advisor/` | Executive advisory | 28 |
| `product-team/` | Product management | 14 |
| `ra-qm-team/` | Regulatory & quality | 13 |
| `project-management/` | PM tools | 6 |
| `business-growth/` | Sales & business dev | 4 |
| `finance/` | Financial analysis | 2 |

Place your skill in the domain that best fits. If unsure, open an issue to discuss.

---

## 2. SKILL.md Format

### Frontmatter (YAML)

**Only two fields are allowed:**

```yaml
---
name: "skill-name"
description: "One-line description of when to use this skill. Be specific about trigger conditions."
---
```

**Do NOT include:** `license`, `metadata`, `triggers`, `version`, `author`, `category`, `updated`, or any other fields. PRs with extra frontmatter fields will be rejected.

### Content Requirements

| Requirement | Rule |
|-------------|------|
| **Line limit** | Under 500 lines. Move detailed content to `references/` files. |
| **Opinionated** | Recommend specific approaches. Don't just list options. |
| **Actionable** | The agent must be able to execute, not just advise. |
| **Anti-patterns** | Include a section on what NOT to do. |
| **Cross-references** | Link to related skills in the repo. |
| **Code examples** | Include concrete examples where helpful. |

### Required Sections

At minimum, every SKILL.md should include:

1. **Title** (H1) — skill name
2. **Overview** — what it does, when to use it
3. **Core content** — workflows, patterns, instructions
4. **Anti-Patterns** — common mistakes to avoid
5. **Cross-References** — related skills in this repo

Reference detailed material from `references/` files:
```markdown
> See [references/detailed-guide.md](references/detailed-guide.md) for full patterns.
```

---

## 3. plugin.json Format

If your skill includes a `.claude-plugin/plugin.json`, use this **exact schema**:

```json
{
  "name": "skill-name",
  "description": "One-line description matching SKILL.md",
  "version": "2.1.2",
  "author": {
    "name": "Alireza Rezvani",
    "url": "https://alirezarezvani.com"
  },
  "homepage": "https://github.com/alirezarezvani/claude-skills/tree/main/<domain>/<skill>",
  "repository": "https://github.com/alirezarezvani/claude-skills",
  "license": "MIT",
  "skills": "./"
}
```

**Rules:**
- `author` **must be an object**, never a string. String format causes install errors.
- `version` must match the current repo version (`2.1.2`).
- No extra fields (`commands`, `hooks`, `triggers`, `tags`, `category`).
- Not every skill needs a plugin.json — skills roll up into their domain's parent plugin automatically.

---

## 4. Python Scripts

All scripts in `scripts/` must follow these rules:

| Rule | Requirement |
|------|-------------|
| **Standard library only** | No pip dependencies. Use `argparse`, `json`, `os`, `re`, `sys`, etc. |
| **CLI-first** | Must support `python3 script.py --help` |
| **JSON output** | Must support `--json` flag for machine-readable output |
| **Exit codes** | `0` = success, `1` = warnings, `2` = critical errors |
| **No LLM calls** | Scripts must be deterministic — no API calls to AI services |
| **No hardcoded secrets** | Use environment variables for credentials |
| **Main guard** | Include `if __name__ == "__main__":` |

**Example skeleton:**
```python
#!/usr/bin/env python3
"""Tool Name — brief description."""

import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    result = {"status": "ok"}

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Result: ok")

if __name__ == "__main__":
    main()
```

---

## 5. Sub-Skills

Some skills contain sub-skills in a nested `skills/` directory:

```
engineering-team/playwright-pro/
├── SKILL.md                          ← Parent skill
└── skills/
    ├── generate/SKILL.md             ← Sub-skill
    ├── fix/SKILL.md                  ← Sub-skill
    └── migrate/SKILL.md              ← Sub-skill
```

**Sub-skill rules:**
- Sub-skills are documented within their parent's docs page, NOT as standalone pages.
- Sub-skills do NOT get their own Codex/Gemini symlinks.
- Sub-skills do NOT count toward the official skill total.
- Do not create new sub-skill structures unless extending an existing compound skill.

---

## 6. What NOT to Contribute

The following will be **immediately closed**:

| Type | Why |
|------|-----|
| Links to external repos/tools in README | We don't link 3rd party projects |
| Skills that require paid API keys | Must work without external dependencies |
| Skills that call LLMs in scripts | Scripts must be deterministic |
| PRs that change the official skill count (205) | This number is curated |
| PRs targeting `main` instead of `dev` | All PRs must target `dev` |
| PRs with bloated diffs (merge history from forks) | Rebase on `dev` HEAD first |
| PRs that modify marketplace.json counts | We handle count updates |
| PRs that modify codex/gemini index files | These are auto-generated |

---

## 7. Cross-Platform Sync

Platform copies are handled by automated scripts. **Do not create or modify these manually:**

| Platform | Directory | Script |
|----------|-----------|--------|
| Codex CLI | `.codex/skills/` | `python3 scripts/sync-codex-skills.py` |
| Gemini CLI | `.gemini/skills/` | `python3 scripts/sync-gemini-skills.py` |
| Cursor/Aider/etc. | `integrations/` (gitignored) | `scripts/convert.sh --tool all` |

After your skill is merged, maintainers run these scripts to sync all platforms.

---

## 8. Docs Site

Docs pages are auto-generated by `python3 scripts/generate-docs.py`. After your skill is merged, maintainers will:

1. Run the docs generator
2. Add your skill to `mkdocs.yml` nav (alphabetical within domain)
3. Deploy via GitHub Pages

You do NOT need to create docs pages in your PR.

---

## 9. Git Conventions

### Branch Naming

```
feature/<skill-name>     → New skill
fix/<description>        → Bug fix
improve/<skill-name>     → Enhancement
docs/<description>       → Documentation
```

### Commit Messages

[Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat(engineering): add browser-automation skill
fix(self-improving-agent): use absolute path for hooks
improve(tdd-guide): add per-language examples
docs: update CONTRIBUTING.md
chore: sync codex/gemini indexes
```

### PR Requirements

- **Target branch:** `dev` (never `main`)
- **One concern per PR** — don't bundle unrelated changes
- **Clean diff** — rebase on `dev` HEAD, no merge commit history
- **Description** — explain what, why, and how you tested

---

## 10. Quality Validation

Before submitting, verify your skill passes these checks:

```bash
# Structure validation
python3 engineering/skill-tester/scripts/skill_validator.py <your-skill-path> --json

# Quality scoring
python3 engineering/skill-tester/scripts/quality_scorer.py <your-skill-path> --json

# Script testing (if you have scripts)
python3 engineering/skill-tester/scripts/script_tester.py <your-skill-path> --json

# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py <your-skill-path> --strict
```

**Minimum requirements:**
- Structure score ≥ 75/100
- All scripts pass `--help`
- Zero CRITICAL or HIGH security findings
- SKILL.md under 500 lines

---

## Quick Reference

| What | Rule |
|------|------|
| Frontmatter fields | `name` + `description` only |
| SKILL.md max lines | 500 |
| Python dependencies | stdlib only |
| PR target branch | `dev` |
| plugin.json author | Object `{"name": "...", "url": "..."}`, never string |
| External links in README | Not accepted |
| Skill count | 205 (do not change) |
| Commit format | Conventional commits |
| Script output | Must support `--json` |

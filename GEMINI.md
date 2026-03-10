# Gemini CLI Foundations

This repository is a **comprehensive skills library** for Gemini CLI - reusable, production-ready skill packages that bundle domain expertise, best practices, analysis tools, and strategic frameworks.

## Using Skills with Gemini CLI

Gemini CLI can activate any skill in this repository using the `activate_skill` tool.

### Skill Locations

Skills are organized into domain folders. Each skill is a directory containing a `SKILL.md` file.

| Domain | Folder |
|--------|--------|
| **Engineering (Core)** | `engineering-team/` |
| **Engineering (Advanced)** | `engineering/` |
| **Product Team** | `product-team/` |
| **Marketing Skills** | `marketing-skill/` |
| **C-Level Advisory** | `c-level-advisor/` |
| **Project Management** | `project-management/` |
| **Regulatory & QM** | `ra-qm-team/` |
| **Business & Growth** | `business-growth/` |
| **Finance** | `finance/` |

### ClawHub Publishing Constraints

When skills are published to **ClawHub** (clawhub.com):
- **cs- prefix for slug conflicts only** — applies only on the ClawHub registry when another publisher already owns the slug. Repo folder names and local skill names are never renamed.
- **No paid/commercial service dependencies** — skills must not require paid third-party API keys or commercial services unless provided by the project itself.
- **plugin.json** — ONLY fields: `name`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `skills: "./"`.
- **Rate limit:** 5 new skills/hour on ClawHub. Use drip publishing for bulk operations.

### Activating a Skill

To activate a skill, use the folder name. For example:

```javascript
activate_skill(name="senior-architect")
activate_skill(name="content-creator")
activate_skill(name="cto-advisor")
```

The Gemini CLI will search for the corresponding `SKILL.md` file within the repository and load its instructions.

## Agents & Commands

In addition to skills, this repository provides specialized **Agents** and **Commands**.

- **Agents** (`agents/`): Multi-agent personas for complex coordination (e.g., `cs-engineering-lead`).
- **Commands** (`commands/`): Predefined workflows for common tasks (e.g., `/tdd`, `/tech-debt`).

Activate them as skills:
```javascript
activate_skill(name="cs-engineering-lead")
activate_skill(name="tdd")
```

## Python Automation Tools

Each skill includes deterministic Python CLI tools in its `scripts/` folder. These use the standard library only.

Example usage:
```bash
python3 marketing-skill/content-production/scripts/seo_checker.py article.txt
```

## Setup for Gemini CLI Users

Run the setup script to initialize the Gemini-specific skill index and symlinks:

```bash
./scripts/gemini-install.sh
```

This will create a `.gemini/skills/` directory for easier discovery.

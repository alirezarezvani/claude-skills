# Templates - Claude Code Guidance

This guide explains the template system for agents, commands, and standardized workflows.

## Template Purpose

**Location:** `templates/`

**Purpose:** Reusable templates for consistent agent development, slash command creation, and workflow automation across all domains.

## Available Templates

### Agent Templates

**Location:** `templates/agent-template.md`

**Usage:** Starting point for creating new cs-* agents

**Contains:**
- YAML frontmatter structure
- Required markdown sections
- Workflow documentation format
- Integration examples pattern

**When to Use:** Creating any new agent in `agents/` directory

### Command Templates and Workflow Templates

Not yet created. There is no command template or workflow template file in `templates/` today — when creating slash commands, copy an existing command in `commands/` (e.g. `commands/cs-backend-review.md` for the argument-hint + gate pattern) instead of looking for a template here.

## Template Usage Pattern

```bash
# 1. Copy template
cp templates/agent-template.md agents/domain/cs-new-agent.md

# 2. Customize for your agent
vim agents/domain/cs-new-agent.md

# 3. Follow template structure exactly

# 4. Test relative paths and integrations

# 5. Commit with conventional commit
git commit -m "feat(agents): implement cs-new-agent from template"
```

## Related Documentation

- **Agent Development:** `../agents/CLAUDE.md` - Comprehensive agent creation guide
- **Standards:** `../standards/CLAUDE.md` - Quality and consistency standards
- **Main Documentation:** `../CLAUDE.md` - Repository overview

---

**Last Updated:** November 5, 2025
**Purpose:** Consistent templates for rapid agent and workflow development

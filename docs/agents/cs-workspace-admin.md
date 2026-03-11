---
title: "cs-workspace-admin"
description: "cs-workspace-admin - Claude Code agent for Engineering - Core."
---

# cs-workspace-admin

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agents/engineering-team/cs-workspace-admin.md">Source</a></span>
</div>


## Role & Expertise

Google Workspace administration specialist orchestrating the gws CLI for email automation, file management, calendar scheduling, security auditing, and cross-service workflows. Manages setup, authentication, 43 built-in recipes, and 10 persona-based bundles.

## Skill Integration

### Skill Location
[`engineering-team/google-workspace-cli`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli)

### Python Tools

1. **GWS Doctor**
   - **Path:** [`scripts/gws_doctor.py`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/scripts/gws_doctor.py)
   - **Usage:** `python3 ../../engineering-team/google-workspace-cli/scripts/gws_doctor.py [--json]`
   - **Purpose:** Pre-flight diagnostics — checks installation, auth, and service connectivity

2. **Auth Setup Guide**
   - **Path:** [`scripts/auth_setup_guide.py`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/scripts/auth_setup_guide.py)
   - **Usage:** `python3 ../../engineering-team/google-workspace-cli/scripts/auth_setup_guide.py --guide oauth`
   - **Purpose:** Guided auth setup, scope listing, .env generation, validation

3. **Recipe Runner**
   - **Path:** [`scripts/gws_recipe_runner.py`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py)
   - **Usage:** `python3 ../../engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --list`
   - **Purpose:** Catalog, search, and execute 43 built-in recipes with persona filtering

4. **Workspace Audit**
   - **Path:** [`scripts/workspace_audit.py`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/scripts/workspace_audit.py)
   - **Usage:** `python3 ../../engineering-team/google-workspace-cli/scripts/workspace_audit.py [--json]`
   - **Purpose:** Security and configuration audit across Workspace services

5. **Output Analyzer**
   - **Path:** [`scripts/output_analyzer.py`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/scripts/output_analyzer.py)
   - **Usage:** `gws ... --json | python3 ../../engineering-team/google-workspace-cli/scripts/output_analyzer.py --count`
   - **Purpose:** Parse, filter, and aggregate JSON/NDJSON output from any gws command

### Knowledge Bases

1. **Command Reference** — [`references/gws-command-reference.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/references/gws-command-reference.md)
   - 18 services, 22 helpers, global flags, environment variables
2. **Recipes Cookbook** — [`references/recipes-cookbook.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/references/recipes-cookbook.md)
   - 43 recipes organized by category with persona mapping
3. **Troubleshooting** — [`references/troubleshooting.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/references/troubleshooting.md)
   - Common errors, auth issues, platform-specific fixes

### Templates

1. **Workspace Config** — [`assets/workspace-config.json`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/assets/workspace-config.json)
   - Automation config template with auth, defaults, scheduled tasks
2. **Persona Profiles** — [`assets/persona-profiles.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/assets/persona-profiles.md)
   - 10 role-based workflow bundles

## Core Workflows

### 1. Setup & Onboarding

**Goal:** Get gws CLI installed, authenticated, and verified.

**Steps:**
1. Run `gws_doctor.py` to check installation and existing auth
2. If not installed, guide through installation (npm/cargo/binary)
3. Run `auth_setup_guide.py --guide oauth` for auth instructions
4. Run `auth_setup_guide.py --scopes <services>` to identify required scopes
5. Run `auth_setup_guide.py --validate` to verify all services
6. Generate `.env` template with `auth_setup_guide.py --generate-env`

**Example:**
```bash
python3 ../../engineering-team/google-workspace-cli/scripts/gws_doctor.py
python3 ../../engineering-team/google-workspace-cli/scripts/auth_setup_guide.py --guide oauth
python3 ../../engineering-team/google-workspace-cli/scripts/auth_setup_guide.py --validate --json
```

### 2. Daily Operations

**Goal:** Execute persona-based daily workflows using recipes.

**Steps:**
1. Identify user's role and select persona with `gws_recipe_runner.py --personas`
2. List relevant recipes with `gws_recipe_runner.py --persona <role> --list`
3. Execute recipes with `gws_recipe_runner.py --run <name>` (use `--dry-run` first)
4. Pipe output through `output_analyzer.py` for filtering and analysis

**Example:**
```bash
python3 ../../engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --persona pm --list
python3 ../../engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --run standup-report --dry-run
gws recipes standup-report --json | python3 ../../engineering-team/google-workspace-cli/scripts/output_analyzer.py --format table
```

### 3. Security Audit

**Goal:** Audit Workspace security configuration and remediate findings.

**Steps:**
1. Run `workspace_audit.py` for full security assessment
2. Review findings, prioritizing FAIL items
3. Filter findings through `output_analyzer.py` for actionable items
4. Execute remediation commands from audit output
5. Re-run audit to verify fixes

**Example:**
```bash
python3 ../../engineering-team/google-workspace-cli/scripts/workspace_audit.py --json
python3 ../../engineering-team/google-workspace-cli/scripts/workspace_audit.py --json | \
  python3 ../../engineering-team/google-workspace-cli/scripts/output_analyzer.py --filter "status=FAIL"
```

### 4. Automation Scripting

**Goal:** Generate multi-step gws scripts for recurring operations.

**Steps:**
1. Identify the workflow from recipe templates
2. Use `gws_recipe_runner.py --describe <name>` for command sequences
3. Customize commands with user-specific parameters
4. Test with `--dry-run` flag
5. Combine into shell scripts or scheduled tasks using `workspace-config.json` template

**Example:**
```bash
python3 ../../engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --describe morning-briefing
# Customize and test
gws helpers morning-briefing --json | python3 ../../engineering-team/google-workspace-cli/scripts/output_analyzer.py --select "type,summary,time" --format table
```

## Output Standards

- Diagnostic reports: structured PASS/WARN/FAIL per check with fixes
- Audit reports: scored findings with risk ratings and remediation commands
- Recipe output: JSON piped through output_analyzer.py for formatted display
- Always use `--dry-run` before executing bulk or destructive operations

## Success Metrics

- **Setup Time:** gws installed and authenticated in under 10 minutes
- **Audit Coverage:** All critical security checks pass (Grade A or B)
- **Automation:** Daily workflows automated via recipes and scheduled tasks
- **Troubleshooting:** Common errors resolved using troubleshooting reference

## Related Agents

- [cs-engineering-lead](cs-engineering-lead.md) — Engineering team coordination
- [cs-senior-engineer](https://github.com/alirezarezvani/claude-skills/tree/main/agents/engineering/cs-senior-engineer.md) — Architecture and CI/CD

## References

- [Skill Documentation](https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/google-workspace-cli/SKILL.md)
- [gws CLI Repository](https://github.com/googleworkspace/cli)

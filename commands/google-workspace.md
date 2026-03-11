---
name: google-workspace
description: "Google Workspace CLI operations: setup diagnostics, security audit, recipe discovery, and output analysis. Usage: /google-workspace <setup|audit|recipe|analyze> [options]"
---

# /google-workspace

Google Workspace CLI administration via the `gws` CLI. Run setup diagnostics, security audits, browse and execute recipes, and analyze command output.

## Usage

```
/google-workspace setup [--json]
/google-workspace audit [--services gmail,drive,calendar] [--json]
/google-workspace recipe list [--persona <role>] [--json]
/google-workspace recipe search <keyword> [--json]
/google-workspace recipe run <name> [--dry-run]
/google-workspace recipe describe <name>
/google-workspace analyze [--filter <field=value>] [--group-by <field>] [--stats <field>] [--format table|csv|json]
```

## Examples

```
/google-workspace setup
/google-workspace audit --services gmail,drive --json
/google-workspace recipe list --persona pm
/google-workspace recipe search "email"
/google-workspace recipe run standup-report --dry-run
/google-workspace recipe describe morning-briefing
/google-workspace analyze --filter "mimeType=pdf" --select "name,size" --format table
```

## Scripts

- `engineering-team/google-workspace-cli/scripts/gws_doctor.py` — Pre-flight diagnostics
- `engineering-team/google-workspace-cli/scripts/auth_setup_guide.py` — Auth setup guide
- `engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py` — Recipe catalog & runner
- `engineering-team/google-workspace-cli/scripts/workspace_audit.py` — Security audit
- `engineering-team/google-workspace-cli/scripts/output_analyzer.py` — JSON/NDJSON analyzer

## Subcommands

### setup
Run pre-flight diagnostics and auth validation.
```bash
python3 engineering-team/google-workspace-cli/scripts/gws_doctor.py [--json]
python3 engineering-team/google-workspace-cli/scripts/auth_setup_guide.py --validate [--json]
```

### audit
Run security and configuration audit.
```bash
python3 engineering-team/google-workspace-cli/scripts/workspace_audit.py [--services gmail,drive,calendar] [--json]
```

### recipe
Browse, search, and execute the 43 built-in gws recipes.
```bash
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --list [--persona <role>] [--json]
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --search <keyword> [--json]
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --describe <name>
python3 engineering-team/google-workspace-cli/scripts/gws_recipe_runner.py --run <name> [--dry-run]
```

### analyze
Parse, filter, and aggregate JSON output from any gws command.
```bash
gws <command> --json | python3 engineering-team/google-workspace-cli/scripts/output_analyzer.py [options]
python3 engineering-team/google-workspace-cli/scripts/output_analyzer.py --demo --format table
```

## Skill Reference
-> `engineering-team/google-workspace-cli/SKILL.md`

## Related Commands
- No direct dependencies (self-contained Google Workspace skill)

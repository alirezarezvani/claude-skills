---
title: Cursor, Aider, Windsurf, Hermes & 9 More AI Coding Tools
description: "Install Claude Code skills and agent plugins in Hermes Agent, Cursor, Aider, Kilo Code, Windsurf, OpenCode, Augment, and Antigravity. One-command conversion for 12 AI coding agents."
---

# Multi-Tool Integrations

All 235 skills in this repository work natively with **8 AI coding tools** beyond Claude Code, Codex, Gemini CLI, and OpenClaw. Hermes Agent uses the same agentskills.io SKILL.md standard — no conversion needed. For the other 7 tools, a conversion script adapts the format each tool expects while preserving skill instructions, workflows, and supporting files.

<div class="grid cards" markdown>

-   :material-cursor-default-click:{ .lg .middle } **Cursor**

    ---

    `.mdc` rule files in `.cursor/rules/`

    [:octicons-arrow-right-24: Jump to Cursor](#cursor)

-   :material-code-braces:{ .lg .middle } **Aider**

    ---

    Single `CONVENTIONS.md` file

    [:octicons-arrow-right-24: Jump to Aider](#aider)

-   :material-alpha-k-box:{ .lg .middle } **Kilo Code**

    ---

    Markdown rules in `.kilocode/rules/`

    [:octicons-arrow-right-24: Jump to Kilo Code](#kilo-code)

-   :material-surfing:{ .lg .middle } **Windsurf**

    ---

    `SKILL.md` bundles in `.windsurf/skills/`

    [:octicons-arrow-right-24: Jump to Windsurf](#windsurf)

-   :material-console:{ .lg .middle } **OpenCode**

    ---

    `SKILL.md` bundles in `.opencode/skills/`

    [:octicons-arrow-right-24: Jump to OpenCode](#opencode)

-   :material-auto-fix:{ .lg .middle } **Augment**

    ---

    Rule files in `.augment/rules/`

    [:octicons-arrow-right-24: Jump to Augment](#augment)

-   :material-google:{ .lg .middle } **Antigravity**

    ---

    `SKILL.md` bundles in `~/.gemini/antigravity/skills/`

    [:octicons-arrow-right-24: Jump to Antigravity](#antigravity)

-   :material-medical-bag:{ .lg .middle } **Hermes Agent**

    ---

    Native `SKILL.md` in `~/.hermes/skills/` — no conversion needed

    [:octicons-arrow-right-24: Jump to Hermes Agent](#hermes-agent)

</div>

<hr class="section-divider">

## Quick Start

### 1. Convert

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Convert all skills for all tools (~15 seconds)
./scripts/convert.sh --tool all

# Or convert for a specific tool only
./scripts/convert.sh --tool cursor
```

### 2. Install

```bash
# Install into your project directory
./scripts/install.sh --tool cursor --target /path/to/project

# Or install globally (Antigravity)
./scripts/install.sh --tool antigravity

# Skip confirmation prompts
./scripts/install.sh --tool aider --target . --force
```

### 3. Verify

Each tool section below includes a verification step to confirm skills are loaded.

!!! tip "Regenerate after updates"
    When you pull new skills from the repository, re-run `./scripts/convert.sh` and `./scripts/install.sh` to update your local installation.

<hr class="section-divider">

## How Conversion Works

The converter reads each skill's `SKILL.md` frontmatter (`name` and `description`) and markdown body, then outputs the format each tool expects:

| Source | Target | What Changes |
|--------|--------|--------------|
| YAML frontmatter | Tool-specific frontmatter | Field names/values adapted per tool |
| Markdown body | Passed through | Instructions preserved as-is |
| `scripts/` dir | Copied (where supported) | Antigravity, Windsurf, OpenCode |
| `references/` dir | Copied (where supported) | Antigravity, Windsurf, OpenCode |
| `templates/` dir | Copied (where supported) | Antigravity, Windsurf, OpenCode |

Tools that use flat files (Cursor, Aider, Kilo Code, Augment) get the SKILL.md body only — supporting directories are not copied since those tools don't support subdirectories per rule.

<hr class="section-divider">

## Cursor

[Cursor](https://cursor.com) uses `.mdc` rule files in `.cursor/rules/` with frontmatter for description, glob patterns, and auto-apply settings.

### Format

Each skill becomes a single `.mdc` file:

```yaml
---
description: "What this skill does and when to activate it"
globs:
alwaysApply: false
---

# Skill instructions here...
```

- **`alwaysApply: false`** — skills are available on-demand, not always loaded
- **`globs:`** — empty by default; add file patterns to auto-activate for specific files (e.g., `*.test.ts`)

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool cursor
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

=== "Manual"

    ```bash
    mkdir -p /path/to/project/.cursor/rules
    cp integrations/cursor/rules/*.mdc /path/to/project/.cursor/rules/
    ```

### Verify

```bash
find .cursor/rules -name "*.mdc" | wc -l
# Expected: 156
```

Open the Cursor rules panel to see all available skills listed.

### Customization

After installation, you can:

- Set `alwaysApply: true` on skills you want active in every conversation
- Add `globs: "*.py"` to auto-activate Python-related skills for `.py` files
- Remove skills you don't need to keep your rules panel clean

<hr class="section-divider">

## Aider

[Aider](https://aider.chat) reads a `CONVENTIONS.md` file from your project root. All skills are concatenated into this single file with section headers.

### Format

```markdown
# Claude Skills — Aider Conventions
> Auto-generated from claude-skills. Do not edit manually.
> Generated: 2026-03-11

---

## copywriting
> When the user wants to write, rewrite, or improve marketing copy...

# Copywriting

You are an expert conversion copywriter...

---

## senior-architect
> Deep expertise in system architecture...

# Senior Architect
...
```

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool aider
    ./scripts/install.sh --tool aider --target /path/to/project
    ```

=== "Manual"

    ```bash
    cp integrations/aider/CONVENTIONS.md /path/to/project/
    ```

### Usage

```bash
# Aider automatically reads CONVENTIONS.md from the project root
aider

# Or explicitly point to it
aider --read CONVENTIONS.md
```

### Verify

```bash
wc -l CONVENTIONS.md
# Expected: ~41,000 lines (all 156 skills)

grep -c "^## " CONVENTIONS.md
# Expected: 156 (one section per skill)
```

!!! note "Large file"
    The combined `CONVENTIONS.md` is ~41K lines. Aider handles this well, but if you prefer a smaller file, you can edit it to keep only the skills relevant to your project.

<hr class="section-divider">

## Kilo Code

[Kilo Code](https://kilo.ai) reads plain markdown rules from `.kilocode/rules/`. No special frontmatter required.

### Format

Each skill becomes a clean markdown file:

```markdown
# copywriting
> When the user wants to write, rewrite, or improve marketing copy...

# Copywriting

You are an expert conversion copywriter...
```

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool kilocode
    ./scripts/install.sh --tool kilocode --target /path/to/project
    ```

=== "Manual"

    ```bash
    mkdir -p /path/to/project/.kilocode/rules
    cp integrations/kilocode/rules/*.md /path/to/project/.kilocode/rules/
    ```

### Verify

```bash
find .kilocode/rules -name "*.md" | wc -l
# Expected: 156
```

Open Kilo Code's rules panel (click the ⚖ icon) to see all rules loaded.

### Mode-Specific Rules

Kilo Code supports mode-specific rules. To assign skills to specific modes:

```bash
# Move architecture skills to "architect" mode
mkdir -p .kilocode/rules-architect/
mv .kilocode/rules/senior-architect.md .kilocode/rules-architect/
mv .kilocode/rules/database-designer.md .kilocode/rules-architect/
```

<hr class="section-divider">

## Windsurf

[Windsurf](https://windsurf.com) uses the same `SKILL.md` format as Claude Code — skills convert with minimal changes.

### Format

Each skill becomes a directory with `SKILL.md` plus optional supporting files:

```
.windsurf/skills/copywriting/
├── SKILL.md           # Instructions with name/description frontmatter
├── scripts/           # Python tools (if present in source)
├── references/        # Domain knowledge (if present)
└── templates/         # Code templates (if present)
```

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
---

# Copywriting
...
```

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool windsurf
    ./scripts/install.sh --tool windsurf --target /path/to/project
    ```

=== "Manual"

    ```bash
    cp -R integrations/windsurf/skills/* /path/to/project/.windsurf/skills/
    ```

### Verify

```bash
find .windsurf/skills -name "SKILL.md" | wc -l
# Expected: 156
```

Skills appear automatically in Windsurf's skill list. You can also invoke them with `@skill-name`.

### Progressive Disclosure

Windsurf uses progressive disclosure — only the skill name and description are shown by default. The full `SKILL.md` content loads only when Windsurf decides the skill is relevant to your request, keeping your context window lean.

<hr class="section-divider">

## OpenCode

[OpenCode](https://opencode.ai) supports skills in `.opencode/skills/` with `SKILL.md` files. It also reads Claude Code's `.claude/skills/` as a fallback.

### Format

Each skill becomes a directory with `SKILL.md`:

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
compatibility: opencode
---

# Copywriting
...
```

The `compatibility: opencode` field is added to help OpenCode identify these as native skills.

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool opencode
    ./scripts/install.sh --tool opencode --target /path/to/project
    ```

=== "Manual"

    ```bash
    cp -R integrations/opencode/skills/* /path/to/project/.opencode/skills/
    ```

=== "Global"

    ```bash
    # Install globally for all projects
    cp -R integrations/opencode/skills/* ~/.config/opencode/skills/
    ```

### Verify

```bash
find .opencode/skills -name "SKILL.md" | wc -l
# Expected: 156
```

### Claude Code Compatibility

OpenCode also reads `.claude/skills/` directories. If you already have skills installed for Claude Code, OpenCode will discover them automatically — no conversion needed.

To disable this fallback:

```bash
export OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1
```

<hr class="section-divider">

## Augment

[Augment](https://augmentcode.com) reads rule files from `.augment/rules/` with frontmatter specifying activation type.

### Format

Each skill becomes a markdown rule file:

```yaml
---
type: auto
description: "When the user wants to write, rewrite, or improve marketing copy..."
---

# Copywriting
...
```

- **`type: auto`** — Augment automatically activates the rule when it matches your request
- Other types: `always` (always loaded), `manual` (user-invoked only)

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool augment
    ./scripts/install.sh --tool augment --target /path/to/project
    ```

=== "Manual"

    ```bash
    mkdir -p /path/to/project/.augment/rules
    cp integrations/augment/rules/*.md /path/to/project/.augment/rules/
    ```

### Verify

```bash
find .augment/rules -name "*.md" | wc -l
# Expected: 156
```

### Customization

Change `type: auto` to `type: always` for skills you want loaded in every conversation:

```bash
# Make coding standards always active
sed -i 's/type: auto/type: always/' .augment/rules/senior-architect.md
```

<hr class="section-divider">

## Antigravity

[Antigravity](https://idx.google.com/) (Google) uses `SKILL.md` files in `~/.gemini/antigravity/skills/` with additional metadata fields.

### Format

```yaml
---
name: "copywriting"
description: "When the user wants to write, rewrite, or improve marketing copy..."
risk: low
source: community
date_added: '2026-03-11'
---

# Copywriting
...
```

Additional fields:

- **`risk: low`** — all skills are instruction-only, no dangerous operations
- **`source: community`** — identifies these as community-contributed skills
- **`date_added`** — conversion date for tracking freshness

### Install

=== "Script"

    ```bash
    ./scripts/convert.sh --tool antigravity
    ./scripts/install.sh --tool antigravity
    # Installs to ~/.gemini/antigravity/skills/ by default
    ```

=== "Manual"

    ```bash
    cp -R integrations/antigravity/* ~/.gemini/antigravity/skills/
    ```

### Verify

```bash
find ~/.gemini/antigravity/skills -name "SKILL.md" | wc -l
# Expected: 156
```

<hr class="section-divider">

## Hermes Agent

[Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research is a self-improving AI agent with a built-in learning loop. It uses the [agentskills.io](https://agentskills.io) standard — **the same SKILL.md format our repo uses** — so no conversion is needed.

### Why Hermes is different

Unlike other tools that need format conversion, Hermes reads `SKILL.md` files natively with the exact same YAML frontmatter (`name`, `description`, `version`, `license`), the same directory layout (`references/`, `templates/`, `assets/`), and the same `AGENTS.md` project context. Our skills are plug-and-play.

### Install

=== "Sync script (recommended)"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    python scripts/sync-hermes-skills.py --verbose
    ```

    This symlinks all 198+ skills into `~/.hermes/skills/claude-skills/` where Hermes discovers them automatically.

=== "Single domain"

    ```bash
    python scripts/sync-hermes-skills.py --domain engineering --verbose
    ```

=== "Copy mode (portable)"

    ```bash
    python scripts/sync-hermes-skills.py --copy --verbose
    ```

    Creates full copies instead of symlinks. Use this on systems where symlinks across filesystems don't work, or to share with Docker containers.

=== "Manual (any single skill)"

    ```bash
    # Symlink
    ln -s /path/to/claude-skills/engineering/karpathy-coder ~/.hermes/skills/karpathy-coder

    # Or copy
    cp -r /path/to/claude-skills/engineering/llm-wiki ~/.hermes/skills/llm-wiki
    ```

### Using skills in Hermes

Once installed, skills are available through Hermes's standard discovery:

```
/skills                    # Browse all installed skills (ours show up under claude-skills/)
/<skill-name>              # Invoke any skill directly as a slash command
/skills search karpathy    # Search by keyword
```

Hermes's skill_view tool loads the SKILL.md content into the conversation context, just like Claude Code does. Python scripts in `scripts/` subdirectories run natively since Hermes has a full Python runtime.

### What works

| Feature | Status | Notes |
|---------|--------|-------|
| SKILL.md loading | ✅ | Identical frontmatter format (agentskills.io) |
| Python scripts (`scripts/`) | ✅ | All stdlib-only, Hermes has Python runtime |
| References / templates / assets | ✅ | Same directory convention |
| `AGENTS.md` project context | ✅ | Hermes reads AGENTS.md natively |
| Slash commands (`/<name>`) | ✅ | Auto-discovered from SKILL.md |
| Sub-agents | ⚠️ | Hermes uses its own `delegate_tool`, not Claude Code's Agent tool — agent .md files load as context but dispatch mechanism differs |
| Claude Code plugin.json | ➖ | Hermes ignores this — not needed, it scans SKILL.md directly |
| Hooks (settings.json) | ⚠️ | Different hook system — manual wiring for Hermes's config.yaml |

### Verify

```bash
# Check how many skills Hermes can see
find ~/.hermes/skills/claude-skills -name "SKILL.md" | wc -l
# Expected: 198+

# Or in Hermes CLI
hermes
> /skills search claude-skills
```

### Updating

```bash
cd claude-skills
git pull origin main
python scripts/sync-hermes-skills.py --verbose
# Existing symlinks are preserved, new skills are added
```

<hr class="section-divider">

## Script Reference

### convert.sh

```
Usage:
  ./scripts/convert.sh [--tool <name>] [--out <dir>] [--help]

Tools:
  antigravity, cursor, aider, kilocode, windsurf, opencode, augment, all

Options:
  --tool <name>   Convert for a specific tool (default: all)
  --out <dir>     Output directory (default: integrations/)
  --help          Show usage
```

**Examples:**

```bash
# Convert all skills for all tools
./scripts/convert.sh

# Convert only for Cursor
./scripts/convert.sh --tool cursor

# Custom output directory
./scripts/convert.sh --tool windsurf --out /tmp/my-skills
```

### install.sh

```
Usage:
  ./scripts/install.sh --tool <name> [--target <dir>] [--force] [--help]

Options:
  --tool <name>     Required. Which tool to install for.
  --target <dir>    Project directory (default: current dir, except antigravity)
  --force           Skip overwrite confirmation
  --help            Show usage
```

**Default install locations:**

| Tool | Default Target |
|------|---------------|
| Hermes Agent | `~/.hermes/skills/claude-skills/` |
| Antigravity | `~/.gemini/antigravity/skills/` |
| Cursor | `<target>/.cursor/rules/` |
| Aider | `<target>/CONVENTIONS.md` |
| Kilo Code | `<target>/.kilocode/rules/` |
| Windsurf | `<target>/.windsurf/skills/` |
| OpenCode | `<target>/.opencode/skills/` |
| Augment | `<target>/.augment/rules/` |

<hr class="section-divider">

## Troubleshooting

??? question "I get 'No skills found' when running convert.sh"
    Make sure you're running the script from the repository root where the skill directories are located.

??? question "Some skills show garbled descriptions"
    This can happen with skills using complex YAML multi-line descriptions. Re-run `convert.sh` — the parser handles folded (`>`) and literal (`|`) YAML scalars.

??? question "Can I use skills from multiple tools at once?"
    Yes! You can install skills for Cursor and Windsurf in the same project — they use different directories and won't conflict.

??? question "How do I update when new skills are added?"
    ```bash
    git pull origin main
    ./scripts/convert.sh --tool all
    ./scripts/install.sh --tool <your-tool> --target . --force
    ```

??? question "Can I convert only specific skills?"
    Not yet via CLI flags, but you can run `convert.sh` and then copy only the skills you want from `integrations/<tool>/`.

??? question "Do supporting files (scripts, references) work in all tools?"
    Only tools that support subdirectories per skill (Hermes Agent, Antigravity, Windsurf, OpenCode) get the full bundle. Flat-file tools (Cursor, Aider, Kilo Code, Augment) get the SKILL.md content only.

??? question "Does Hermes Agent need format conversion?"
    No. Hermes uses the same agentskills.io SKILL.md format as our repo. Just run `python scripts/sync-hermes-skills.py --verbose` to symlink skills into `~/.hermes/skills/`. No conversion step needed.

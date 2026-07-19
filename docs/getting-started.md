---
title: Install Agent Skills — Claude Code, Codex, Gemini CLI Setup
description: "How to install 345 agent skills and 78 plugins in any of 13 AI coding tools. Step-by-step setup for Claude Code, OpenAI Codex, Gemini CLI, Hermes Agent, Mistral Vibe, OpenClaw, Cursor, Aider, Windsurf, and more — most take under two minutes."
---

# Getting Started

Installing agent skills takes under two minutes on most platforms. There's nothing to configure: no API keys, no dependencies, no build step. Pick your tool below, run the commands, and the skills are live.

New here? Read [What is an Agent Skill?](index.md#what-is-an-agent-skill) first, or jump straight to a tool-specific guide: [Claude Code](guides/best-claude-code-plugins.md), [OpenAI Codex](guides/agent-skills-for-codex.md), [Gemini CLI](guides/gemini-cli-skills-guide.md), [Cursor](guides/cursor-skills-guide.md), or [OpenClaw](guides/openclaw-skills-guide.md).

## Installation

Choose your platform and follow the steps:

=== "Claude Code"

    <ol class="install-steps">
      <li>
        <strong>Add the marketplace</strong>
        <pre><code>/plugin marketplace add alirezarezvani/claude-skills</code></pre>
      </li>
      <li>
        <strong>Install the skills you need</strong>
        <pre><code>/plugin install engineering-skills@claude-code-skills</code></pre>
      </li>
      <li>
        <strong>Use them immediately</strong> — skills activate as slash commands or contextual expertise.
      </li>
    </ol>

=== "OpenAI Codex"

    ```bash
    npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
    ```

    Or clone and install manually:

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    ./scripts/codex-install.sh
    ```

=== "Gemini CLI"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    ./scripts/gemini-install.sh
    ```

    Or use the sync script to generate the skills index:

    ```bash
    python3 scripts/sync-gemini-skills.py
    ```

=== "OpenClaw"

    ```bash
    bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
    ```

=== "Hermes Agent"

    [Hermes Agent](https://github.com/NousResearch/hermes-agent) uses the same agentskills.io SKILL.md standard — no format conversion needed.

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    python scripts/sync-hermes-skills.py --verbose
    ```

    Skills install to `~/.hermes/skills/claude-skills/` and are automatically discovered by Hermes via `/skills` or `/<skill-name>`.

    Sync options:

    ```bash
    python scripts/sync-hermes-skills.py --domain engineering  # one domain only
    python scripts/sync-hermes-skills.py --copy                # copy instead of symlink
    python scripts/sync-hermes-skills.py --dry-run             # preview
    ```

=== "Mistral Vibe"

    [Mistral Vibe](https://github.com/mistralai/mistral-vibe) is Mistral AI's open-source Apache-2.0 CLI coding agent. It uses the same agentskills.io SKILL.md standard — no format conversion needed.

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/vibe-install.sh
    ```

    Skills install to `~/.vibe/skills/claude-skills/` (345 skills across 17 domains) and are automatically discovered by Vibe via `/skills` or `/<skill-name>`. See the [official Vibe docs](https://docs.mistral.ai/mistral-vibe/agents-skills) for details on the skills format.

    Sync options:

    ```bash
    python scripts/sync-vibe-skills.py --domain engineering   # one domain only
    python scripts/sync-vibe-skills.py --copy                 # copy instead of symlink
    python scripts/sync-vibe-skills.py --dry-run              # preview
    python scripts/sync-vibe-skills.py --target /opt/team/    # custom location
    ```

=== "Cursor"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool cursor
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

=== "Aider"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool aider
    ./scripts/install.sh --tool aider --target /path/to/project
    ```

=== "Windsurf"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool windsurf
    ./scripts/install.sh --tool windsurf --target /path/to/project
    ```

=== "Kilo Code"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool kilocode
    ./scripts/install.sh --tool kilocode --target /path/to/project
    ```

=== "OpenCode"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool opencode
    ./scripts/install.sh --tool opencode --target /path/to/project
    ```

=== "Augment"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool augment
    ./scripts/install.sh --tool augment --target /path/to/project
    ```

=== "Antigravity"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool antigravity
    ./scripts/install.sh --tool antigravity
    ```

=== "Manual"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    # Copy any skill folder to ~/.claude/skills/
    ```

!!! tip "All conversion-based tools at once"
    Convert for every supported tool in one command:
    ```bash
    ./scripts/convert.sh --tool all
    ```
    See the [Multi-Tool Integrations](integrations.md) page for detailed per-tool documentation.

<hr class="section-divider">

## Available Bundles

Domain bundles install a whole team of skills at once:

| Bundle | Install Command | Skills |
|--------|----------------|--------|
| **Engineering — Core** | `/plugin install engineering-skills@claude-code-skills` | 51 |
| **Engineering — Advanced** | `/plugin install engineering-advanced-skills@claude-code-skills` | 74 |
| **Product** | `/plugin install product-skills@claude-code-skills` | 17 |
| **Marketing** | `/plugin install marketing-skills@claude-code-skills` | 47 |
| **Regulatory & Quality** | `/plugin install ra-qm-skills@claude-code-skills` | 18 |
| **Compliance OS** | `/plugin install compliance-os@claude-code-skills` | 9 |
| **Project Management** | `/plugin install pm-skills@claude-code-skills` | 9 |
| **C-Level Advisory** | `/plugin install c-level-skills@claude-code-skills` | 61 |
| **Business & Growth** | `/plugin install business-growth-skills@claude-code-skills` | 5 |
| **Business Operations** | `/plugin install business-operations-skills@claude-code-skills` | 7 |
| **Commercial** | `/plugin install commercial-skills@claude-code-skills` | 8 |
| **Finance** | `/plugin install finance-skills@claude-code-skills` | 4 |
| **Research Operations** | `/plugin install research-ops-skills@claude-code-skills` | 5 |
| **Markdown to HTML** | `/plugin install markdown-html-skills@claude-code-skills` | 5 |

Productivity and research skills ship as standalone plugins (for example `capture-skill`, `pulse`, `litreview`, `grants`). Browse the [plugin marketplace](plugins/index.md) for the full list, or install any individual skill: `/plugin install skill-name@claude-code-skills`

<hr class="section-divider">

## Usage

### Slash Commands

```
/pw:generate     Generate Playwright tests
/pw:fix          Fix flaky test failures
/si:review       Review auto-memory health
/si:promote      Graduate a learning to CLAUDE.md
/cs:board        Trigger a C-suite board meeting
```

### Contextual Prompts

```
Using the senior-architect skill, review our microservices
architecture and identify the top 3 scalability risks.
```

```
Using the content-creator skill, write a blog post about
AI-augmented development. Optimize for SEO.
```

<hr class="section-divider">

## Python Tools

Every skill's bundled tools use the Python standard library only — over 550 scripts, zero pip installs, all verified with `--help` smoke tests.

```bash
# Security audit a skill before installing
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Analyze brand voice
python3 marketing-skill/content-production/scripts/brand_voice_analyzer.py article.txt

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Generate landing page (TSX + Tailwind)
python3 product-team/landing-page-generator/scripts/landing_page_scaffolder.py config.json --format tsx

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase
```

<hr class="section-divider">

## Security

!!! warning "Always audit untrusted skills"

    Before installing skills from third-party sources, run the security auditor:

    ```bash
    python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
    ```

    Returns **PASS** / **WARN** / **FAIL** with remediation guidance. Scans for command injection, data exfiltration, prompt injection, and supply chain risks.

<hr class="section-divider">

## Creating Your Own

Each skill is a folder:

```
my-skill/
  SKILL.md       # Instructions + workflows
  scripts/       # Python CLI tools (optional)
  references/    # Domain knowledge (optional)
  assets/        # Templates (optional)
```

See the [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skill-factory) for a complete guide.

<hr class="section-divider">

## FAQ

??? question "Do I need API keys?"
    No. Skills work locally with no external API calls. All Python tools use stdlib only.

??? question "Can I install individual skills instead of bundles?"
    Yes. Use `/plugin install skill-name@claude-code-skills` for any single skill.

??? question "Do skills conflict with each other?"
    No. Each skill is self-contained with no cross-dependencies.

??? question "How do I update installed skills?"
    Re-run the install command. The plugin system fetches the latest version from the marketplace.

??? question "Will upgrading break my setup?"
    No. Releases are backward compatible — existing SKILL.md files, scripts, and references keep working. New skills and domains are additive only.

??? question "Does this work with Gemini CLI?"
    Yes. Run `./scripts/gemini-install.sh` to set up skills for Gemini CLI. A sync script (`scripts/sync-gemini-skills.py`) generates the skills index automatically.

??? question "Does this work with Cursor, Windsurf, Aider, or other tools?"
    Yes. All 345 skills can be converted to native formats for Cursor, Aider, Kilo Code, Windsurf, OpenCode, Augment, and Antigravity. Run `./scripts/convert.sh --tool all` and then install with `./scripts/install.sh --tool <name>`. See [Multi-Tool Integrations](integrations.md) for details.

??? question "Can I use Agent Skills in ChatGPT?"
    Yes. We have [6 Custom GPTs](custom-gpts.md) that bring Agent Skills directly into ChatGPT — no installation needed. Just click and start chatting.

---
title: Getting Started
description: "How to install and use Claude Code skills and plugins for Claude Code, OpenAI Codex, and OpenClaw."
---

# Getting Started

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

=== "OpenClaw"

    ```bash
    bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
    ```

=== "Manual"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    # Copy any skill folder to ~/.claude/skills/
    ```

<hr class="section-divider">

## Available Bundles

| Bundle | Install Command | Skills |
|--------|----------------|--------|
| **Engineering Core** | `/plugin install engineering-skills@claude-code-skills` | 23 |
| **Engineering POWERFUL** | `/plugin install engineering-advanced-skills@claude-code-skills` | 25 |
| **Product** | `/plugin install product-skills@claude-code-skills` | 8 |
| **Marketing** | `/plugin install marketing-skills@claude-code-skills` | 42 |
| **Regulatory & Quality** | `/plugin install ra-qm-skills@claude-code-skills` | 12 |
| **Project Management** | `/plugin install pm-skills@claude-code-skills` | 6 |
| **C-Level Advisory** | `/plugin install c-level-skills@claude-code-skills` | 28 |
| **Business & Growth** | `/plugin install business-growth-skills@claude-code-skills` | 4 |
| **Finance** | `/plugin install finance-skills@claude-code-skills` | 1 |

Or install individual skills: `/plugin install skill-name@claude-code-skills`

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

All 160+ tools use the standard library only — zero pip installs.

```bash
# Security audit a skill before installing
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Analyze brand voice
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py article.txt

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

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

See the [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory) for a complete guide.

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

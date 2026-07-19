---
title: Agent Skills & Plugins for Claude Code, Codex, Gemini CLI & 10 More AI Tools
description: "345 production-ready agent skills, 78 installable plugins, and 90+ slash commands across 17 domains — engineering, product, marketing, compliance, finance, and research. Works with Claude Code, OpenAI Codex, Gemini CLI, Cursor, Hermes Agent, Mistral Vibe, OpenClaw, and 6 more AI coding tools. Open source, MIT licensed, zero dependencies."
hide:
  - toc
  - edit
---

<style>
.md-content__inner > .md-typeset > h1:first-child { display: none; }
</style>

<div class="hero" markdown>

<span class="hero-eyebrow">Open source · MIT · 17 domains · 13 AI tools</span>

# Agent Skills

Give your AI coding agent real domain expertise. Every skill is a self-contained package of workflows, checklists, Python tools, and reference knowledge that your agent follows autonomously — install one command, ship better work.
{ .hero-subtitle }

[Get Started](getting-started.md){ .md-button .md-button--primary }
[Browse Skills](skills/index.md){ .md-button }
[GitHub :fontawesome-brands-github:](https://github.com/alirezarezvani/claude-skills){ .md-button }

<div class="stats-strip">
  <div class="stat"><span class="stat-number">345</span><span class="stat-label">Skills</span></div>
  <div class="stat"><span class="stat-number">17</span><span class="stat-label">Domains</span></div>
  <div class="stat"><span class="stat-number">78</span><span class="stat-label">Plugins</span></div>
  <div class="stat"><span class="stat-number">570+</span><span class="stat-label">Python Tools</span></div>
  <div class="stat"><span class="stat-number">90+</span><span class="stat-label">Commands</span></div>
  <div class="stat"><span class="stat-number">13</span><span class="stat-label">AI Tools</span></div>
</div>

</div>

<div class="tools-bar" markdown>

<p class="tools-label">Works with</p>

<div class="tools-grid">
  <a href="guides/best-claude-code-plugins/" class="tool-badge tool-claude">Claude Code</a>
  <a href="guides/agent-skills-for-codex/" class="tool-badge tool-codex">OpenAI Codex</a>
  <a href="guides/gemini-cli-skills-guide/" class="tool-badge tool-gemini">Gemini CLI</a>
  <a href="guides/cursor-skills-guide/" class="tool-badge tool-cursor">Cursor</a>
  <a href="integrations/#hermes-agent" class="tool-badge tool-hermes">Hermes Agent</a>
  <a href="integrations/#mistral-vibe" class="tool-badge tool-vibe">Mistral Vibe</a>
  <a href="integrations/#aider" class="tool-badge tool-aider">Aider</a>
  <a href="integrations/#windsurf" class="tool-badge tool-windsurf">Windsurf</a>
  <a href="integrations/#kilo-code" class="tool-badge tool-kilo">Kilo Code</a>
  <a href="integrations/#opencode" class="tool-badge tool-opencode">OpenCode</a>
  <a href="integrations/#augment" class="tool-badge tool-augment">Augment</a>
  <a href="integrations/#antigravity" class="tool-badge tool-antigravity">Antigravity</a>
  <a href="guides/openclaw-skills-guide/" class="tool-badge tool-openclaw">OpenClaw</a>
</div>

</div>

---

## What Is an Agent Skill?

An **agent skill** is a portable package of expertise your AI assistant can load on demand. Instead of re-explaining your standards in every prompt, a skill gives the agent a structured workflow it follows the same way every time — whether that's reviewing a pull request, designing a pricing model, or preparing an ISO 27001 audit.

Every skill in this library follows the same simple anatomy:

```
skill-name/
├── SKILL.md          # The playbook — workflows, rules, decision frameworks
├── scripts/          # Python CLI tools (stdlib-only, no pip installs)
├── references/       # Curated domain knowledge the agent can consult
└── assets/           # Ready-to-use templates for your team
```

No API keys, no external services, no dependencies between skills. Copy a folder — or install a plugin — and it works.

<ul class="steps">
  <li><strong>Install</strong> Add the marketplace to Claude Code, or run one sync script for Codex, Gemini CLI, Cursor, and 9 more tools.</li>
  <li><strong>Invoke</strong> Call a slash command like <code>/cs:deal-review</code>, or just mention the skill in a prompt — the agent loads the playbook.</li>
  <li><strong>Ship</strong> The agent works through the skill's checklists and tools, producing consistent, reviewable output every time.</li>
</ul>

---

## What's Inside

<div class="grid cards" markdown>

-   :material-toolbox:{ .lg .middle } **345 Skills**

    ---

    Production-ready playbooks across 17 domains — from code review and RAG architecture to pricing strategy, clinical study design, and markdown-to-HTML publishing. Each ships with workflows, Python tools, and reference docs.

    [:octicons-arrow-right-24: Browse skills](skills/index.md)

-   :material-puzzle-outline:{ .lg .middle } **78 Plugins**

    ---

    One-command installable bundles for Claude Code — install a whole domain or a single skill. Sync scripts cover Codex CLI, Gemini CLI, Hermes Agent, Mistral Vibe, and OpenClaw.

    [:octicons-arrow-right-24: Plugin marketplace](plugins/index.md)

-   :material-robot:{ .lg .middle } **90+ Agents**

    ---

    Multi-skill orchestrators with distinct personas — engineering leads, C-suite advisors, research routers, and compliance auditors that combine skills for complex work.

    [:octicons-arrow-right-24: View agents](agents/index.md)

-   :material-console:{ .lg .middle } **90+ Slash Commands**

    ---

    Instant workflows you run by name — sprint planning, PRDs, OKRs, deal reviews, SLO design, chaos experiments, and market research, straight from your terminal.

    [:octicons-arrow-right-24: View commands](commands/index.md)

-   :material-language-python:{ .lg .middle } **570+ Python Tools**

    ---

    Deterministic CLI scripts bundled with skills — all standard library, zero pip installs, no LLM calls. Scoring, validation, and analysis that runs anywhere Python runs.

    [:octicons-arrow-right-24: Getting started](getting-started.md)

-   :material-account-group:{ .lg .middle } **3 Personas**

    ---

    Role-based identities — Startup CTO, Growth Marketer, Solo Founder — with curated skill loadouts, judgment frameworks, and distinct communication styles.

    [:octicons-arrow-right-24: Meet personas](personas/index.md)

-   :material-sitemap:{ .lg .middle } **Orchestration**

    ---

    A lightweight protocol for coordinating personas, skills, and agents on work that crosses domain boundaries — launches, audits, and strategic sprints.

    [:octicons-arrow-right-24: Learn patterns](orchestration.md)

-   :material-swap-horizontal:{ .lg .middle } **13-Tool Support**

    ---

    Write once, run everywhere. A single conversion script adapts every skill to the native format of Cursor, Aider, Windsurf, Kilo Code, OpenCode, Augment, and Antigravity.

    [:octicons-arrow-right-24: Multi-tool setup](integrations.md)

-   :material-chat-outline:{ .lg .middle } **6 Custom GPTs**

    ---

    Use Agent Skills directly in ChatGPT with zero setup — Solo Founder, SEO Audit, Content Strategy, CTO Advisor, and more.

    [:octicons-arrow-right-24: Open GPTs](custom-gpts.md)

</div>

---

## Skills by Domain

Seventeen domains cover the full lifecycle of building a product and running a company — engineering, go-to-market, operations, compliance, and research.

<div class="grid cards" markdown>

-   :material-cog:{ .lg .middle } **Engineering — Core**

    ---

    Architecture, frontend, backend, fullstack, QA, DevOps, SecOps, AI/ML, data engineering, Playwright testing, self-improving agent

    [:octicons-arrow-right-24: 51 skills](skills/engineering-team/index.md)

-   :material-lightning-bolt:{ .lg .middle } **Engineering — Advanced**

    ---

    Agent designer, RAG architect, MCP server builder, CI/CD pipelines, SLO architect, chaos engineering, security auditing, tech debt tracking

    [:octicons-arrow-right-24: 74 skills](skills/engineering/index.md)

-   :material-bullseye-arrow:{ .lg .middle } **Product**

    ---

    Product manager toolkit, agile PO, UX research, discovery, analytics, experiment design, SaaS scaffolding, Apple HIG

    [:octicons-arrow-right-24: 17 skills](skills/product-team/index.md)

-   :material-bullhorn:{ .lg .middle } **Marketing**

    ---

    Content, SEO, AEO, CRO, paid channels, growth, launch strategy — 8 specialist pods with bundled Python analytics tools

    [:octicons-arrow-right-24: 47 skills](skills/marketing-skill/index.md)

-   :material-star-circle:{ .lg .middle } **C-Level Advisory**

    ---

    Full C-suite advisors (CEO to General Counsel), founder-mode boardroom, decision logging, culture and strategy frameworks

    [:octicons-arrow-right-24: 61 skills](skills/c-level-advisor/index.md)

-   :material-shield-check:{ .lg .middle } **Regulatory & Quality**

    ---

    ISO 13485, MDR 2017/745, FDA, ISO 27001, GDPR, CAPA, risk management, quality documentation

    [:octicons-arrow-right-24: 18 skills](skills/ra-qm-team/index.md)

-   :material-shield-lock:{ .lg .middle } **Compliance OS**

    ---

    Audit-prep orchestrator for ISO 13485, ISO 27001, SOC 2, GDPR, FDA QSR, EU AI Act, and ISO 42001 readiness

    [:octicons-arrow-right-24: 9 skills](skills/compliance-os/index.md)

-   :material-clipboard-check:{ .lg .middle } **Project Management**

    ---

    Senior PM, scrum master, Jira and Confluence experts, Atlassian admin with bundled remote MCP

    [:octicons-arrow-right-24: 9 skills](skills/project-management/index.md)

-   :material-trending-up:{ .lg .middle } **Business & Growth**

    ---

    Customer success, sales engineering, revenue operations, contracts and proposals

    [:octicons-arrow-right-24: 5 skills](skills/business-growth/index.md)

-   :material-cog-outline:{ .lg .middle } **Business Operations**

    ---

    Process mapping, vendor management, capacity planning, internal comms, knowledge ops, procurement

    [:octicons-arrow-right-24: 7 skills](skills/business-operations/index.md)

-   :material-handshake:{ .lg .middle } **Commercial**

    ---

    Pricing strategy, deal desk, partnerships, channel economics, commercial policy, RFP response, forecasting

    [:octicons-arrow-right-24: 8 skills](skills/commercial/index.md)

-   :material-currency-usd:{ .lg .middle } **Finance**

    ---

    Financial analysis, DCF valuation, budgeting, forecasting, SaaS metrics (ARR, MRR, churn, LTV)

    [:octicons-arrow-right-24: 4 skills](skills/finance/index.md)

-   :material-magnify:{ .lg .middle } **Research**

    ---

    Literature review, grants, patents, entity dossiers, syllabi, NotebookLM automation — with a hybrid orchestrator

    [:octicons-arrow-right-24: 8 skills](skills/research/index.md)

-   :material-flask:{ .lg .middle } **Research Operations**

    ---

    Clinical study design, R&D program finance, market sizing and surveys, product research methodology

    [:octicons-arrow-right-24: 5 skills](skills/research-ops/index.md)

-   :material-lightning-bolt-outline:{ .lg .middle } **Productivity**

    ---

    Brain-dump capture, inbox setup and triage, reflection journal, session handoff, market-first decision making

    [:octicons-arrow-right-24: 6 skills](skills/productivity/index.md)

-   :material-language-html5:{ .lg .middle } **Markdown to HTML**

    ---

    Turn markdown into beautiful single-file HTML — long-form documents, code reviews, and slide decks with your brand

    [:octicons-arrow-right-24: 5 skills](skills/markdown-html/index.md)

-   :material-web:{ .lg .middle } **Landing Pages**

    ---

    Single-file HTML landing page generator with four design styles and a brand palette validator

    [:octicons-arrow-right-24: 1 skill](skills/marketing/index.md)

</div>

---

## Why Teams Use This Library

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } **Zero dependencies**

    ---

    Every Python tool uses the standard library only. No pip installs, no API keys, no configuration. Works anywhere Python runs.

-   :material-shield-lock:{ .lg .middle } **Security first**

    ---

    A built-in security auditor scans any skill for malicious code, data exfiltration, and prompt injection before you install it.

-   :material-rocket-launch:{ .lg .middle } **One-command install**

    ---

    A plugin marketplace for Claude Code, sync scripts for Codex, Gemini, Hermes, and Vibe, and a converter for seven more tools.

-   :material-puzzle:{ .lg .middle } **Self-contained**

    ---

    Each skill is independent — no cross-dependencies, no conflicts. Install one or all; they work in isolation.

-   :material-devices:{ .lg .middle } **Multi-platform**

    ---

    Native support for 13 AI coding tools. Write once, convert to any tool's format automatically.

-   :material-check-decagram:{ .lg .middle } **Production-grade**

    ---

    Structured workflows with validation checkpoints — not generic advice. Each skill covers an end-to-end process with named deliverables.

</div>

---

## Quick Install

=== "Claude Code"

    ```bash
    # Add the marketplace
    /plugin marketplace add alirezarezvani/claude-skills

    # Install any skill bundle
    /plugin install engineering-skills@claude-code-skills
    ```

=== "OpenAI Codex"

    ```bash
    npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
    ```

=== "Gemini CLI"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills && ./scripts/gemini-install.sh
    ```

=== "Hermes Agent"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    python scripts/sync-hermes-skills.py --verbose
    # Skills appear in /skills and /<skill-name> automatically
    ```

=== "Mistral Vibe"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/vibe-install.sh
    # Skills install to ~/.vibe/skills/claude-skills/; same SKILL.md standard
    ```

=== "Cursor / Windsurf / Aider"

    ```bash
    git clone https://github.com/alirezarezvani/claude-skills.git
    cd claude-skills
    ./scripts/convert.sh --tool cursor    # or windsurf, aider
    ./scripts/install.sh --tool cursor --target /path/to/project
    ```

[Full Install Guide](getting-started.md){ .md-button .md-button--primary }
[Multi-Tool Setup](integrations.md){ .md-button }

---

## Guides

Tool-specific walkthroughs for getting the most out of the library:

- **[Best Claude Code Plugins & Skills](guides/best-claude-code-plugins.md)** — the 20 plugins to start with, by use case
- **[Agent Skills for OpenAI Codex CLI](guides/agent-skills-for-codex.md)** — install and invoke skills in Codex
- **[Gemini CLI Skills & Plugins Guide](guides/gemini-cli-skills-guide.md)** — setup, indexing, and usage for Gemini CLI
- **[Cursor Agent Skills & Rules Guide](guides/cursor-skills-guide.md)** — convert skills to Cursor's rules format
- **[OpenClaw Skills Guide](guides/openclaw-skills-guide.md)** — one-line install for OpenClaw workspaces

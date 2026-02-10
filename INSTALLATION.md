# Installation Guide - Claude Skills Library

Complete installation guide for all 53 production-ready skills across multiple AI agents and platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Claude Code Native Marketplace](#claude-code-native-marketplace-new)
- [Universal Installer](#universal-installer)
- [OpenAI Codex Installation](#openai-codex-installation)
- [Per-Skill Installation](#per-skill-installation)
- [Multi-Agent Setup](#multi-agent-setup)
- [Manual Installation](#manual-installation)
- [Verification & Testing](#verification--testing)
- [Troubleshooting](#troubleshooting)
- [Uninstallation](#uninstallation)

---

## Quick Start

**Choose your agent:**

### For Claude Code Users (Recommended)

```bash
# In Claude Code, run:
/plugin marketplace add alirezarezvani/claude-skills
/plugin install marketing-skills@claude-code-skills
```

Native integration with automatic updates and version management.

### For OpenAI Codex Users

```bash
# Option 1: Universal installer
npx ai-agent-skills install alirezarezvani/claude-skills --agent codex

# Option 2: Direct installation script
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
./scripts/codex-install.sh
```

Skills install to `~/.codex/skills/`. See [OpenAI Codex Installation](#openai-codex-installation) for detailed instructions.

### For All Other Agents (Cursor, VS Code, Goose, etc.)

```bash
npx ai-agent-skills install alirezarezvani/claude-skills
```

This single command installs all skills to all supported agents automatically.

---

## Claude Code Native Marketplace (New!)

**Best for Claude Code users** - Native integration with Claude Code's plugin system.

### Add the Marketplace

```bash
# In Claude Code, run:
/plugin marketplace add alirezarezvani/claude-skills
```

This adds the skills library to your available marketplaces.

### Install Skill Bundles

```bash
# Install by domain (bundles of skills)
/plugin install marketing-skills@claude-code-skills     # 6 marketing skills
/plugin install engineering-skills@claude-code-skills   # 18 engineering skills
/plugin install product-skills@claude-code-skills       # 5 product skills
/plugin install c-level-skills@claude-code-skills       # 2 C-level advisory skills
/plugin install pm-skills@claude-code-skills            # 6 project management skills
/plugin install ra-qm-skills@claude-code-skills         # 12 regulatory/quality skills
```

### Install Individual Skills

```bash
# Marketing
/plugin install content-creator@claude-code-skills
/plugin install demand-gen@claude-code-skills

# Engineering
/plugin install fullstack-engineer@claude-code-skills
/plugin install aws-architect@claude-code-skills

# Product
/plugin install product-manager@claude-code-skills

# Project Management
/plugin install scrum-master@claude-code-skills
```

### Update Skills

```bash
# Update all installed plugins
/plugin update

# Update specific plugin
/plugin update marketing-skills
```

### Remove Skills

```bash
# Remove specific plugin
/plugin remove marketing-skills

# Remove marketplace
/plugin marketplace remove claude-code-skills
```

**Benefits:**
- ✅ Native Claude Code integration
- ✅ Automatic updates with `/plugin update`
- ✅ Version management with git tags
- ✅ Skills installed to `~/.claude/skills/`
- ✅ Managed through Claude Code UI

---

## Universal Installer

The universal installer uses the [ai-agent-skills](https://github.com/skillcreatorai/Ai-Agent-Skills) package to install skills across multiple agents simultaneously.

### Install All Skills

```bash
# Install to all supported agents
npx ai-agent-skills install alirezarezvani/claude-skills
```

**This installs to:**
- Claude Code → `~/.claude/skills/`
- Cursor → `.cursor/skills/`
- VS Code/Copilot → `.github/skills/`
- Goose → `~/.config/goose/skills/`
- Amp → Platform-specific location
- Codex → Platform-specific location
- Letta → Platform-specific location
- OpenCode → Platform-specific location

### Install to Specific Agent

```bash
# Claude Code only
npx ai-agent-skills install alirezarezvani/claude-skills --agent claude

# Cursor only
npx ai-agent-skills install alirezarezvani/claude-skills --agent cursor

# VS Code/Copilot only
npx ai-agent-skills install alirezarezvani/claude-skills --agent vscode

# Goose only
npx ai-agent-skills install alirezarezvani/claude-skills --agent goose

# Project-specific installation (portable)
npx ai-agent-skills install alirezarezvani/claude-skills --agent project
```

### Preview Before Installing

```bash
# Dry run to see what will be installed
npx ai-agent-skills install alirezarezvani/claude-skills --dry-run
```

---

## Per-Skill Installation

Install individual skills instead of the entire library:

### Marketing Skills

```bash
# Content Creator
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator

# Demand Generation & Acquisition
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/marketing-demand-acquisition

# Product Marketing Strategy
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/marketing-strategy-pmm

# App Store Optimization
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/app-store-optimization

# Social Media Analyzer
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/social-media-analyzer
```

### C-Level Advisory Skills

```bash
# CEO Advisor
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/ceo-advisor

# CTO Advisor
npx ai-agent-skills install alirezarezvani/claude-skills/c-level-advisor/cto-advisor
```

### Product Team Skills

```bash
# Product Manager Toolkit
npx ai-agent-skills install alirezarezvani/claude-skills/product-team/product-manager-toolkit

# Agile Product Owner
npx ai-agent-skills install alirezarezvani/claude-skills/product-team/agile-product-owner

# Product Strategist
npx ai-agent-skills install alirezarezvani/claude-skills/product-team/product-strategist

# UX Researcher Designer
npx ai-agent-skills install alirezarezvani/claude-skills/product-team/ux-researcher-designer

# UI Design System
npx ai-agent-skills install alirezarezvani/claude-skills/product-team/ui-design-system
```

### Project Management Skills

```bash
# Senior PM Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/senior-pm-expert

# Scrum Master Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/scrum-master-expert

# Atlassian Jira Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-jira-expert

# Atlassian Confluence Expert
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-confluence-expert

# Atlassian Administrator
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-administrator

# Atlassian Template Creator
npx ai-agent-skills install alirezarezvani/claude-skills/project-management/atlassian-template-creator
```

### Engineering Team Skills

```bash
# Core Engineering
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-architect
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-frontend
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-backend
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-fullstack
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-qa
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-devops
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-secops
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/code-reviewer
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-security

# Cloud & Enterprise
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/aws-solution-architect
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/ms365-tenant-manager

# Development Tools
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/tdd-guide
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/tech-stack-evaluator

# AI/ML/Data
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-data-scientist
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-data-engineer
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-ml-engineer
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-prompt-engineer
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team/senior-computer-vision
```

### Regulatory Affairs & Quality Management Skills

```bash
# Regulatory & Quality Leadership
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/regulatory-affairs-head
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/quality-manager-qmr
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/quality-manager-qms-iso13485

# Quality Processes
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/capa-officer
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/quality-documentation-manager
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/risk-management-specialist

# Security & Privacy
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/information-security-manager-iso27001
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/gdpr-dsgvo-expert

# Regional Compliance
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/mdr-745-specialist
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/fda-consultant-specialist

# Audit & Assessment
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/qms-audit-expert
npx ai-agent-skills install alirezarezvani/claude-skills/ra-qm-team/isms-audit-expert
```

---

## Multi-Agent Setup

Install the same skills across different agents for team consistency:

### Example: Marketing Team Setup

```bash
# Install marketing skills to Claude Code (for content strategist)
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator --agent claude

# Install same skills to Cursor (for developer working on content)
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator --agent cursor

# Install to VS Code (for SEO specialist)
npx ai-agent-skills install alirezarezvani/claude-skills/marketing-skill/content-creator --agent vscode
```

### Example: Engineering Team Setup

```bash
# Full engineering suite to Claude Code
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team --agent claude

# Same suite to Cursor
npx ai-agent-skills install alirezarezvani/claude-skills/engineering-team --agent cursor
```

---

## Manual Installation

For development, customization, or offline use:

### Prerequisites

- **Python 3.7+** (for running analysis scripts)
- **Git** (for cloning repository)
- **Claude AI account** or **Claude Code** (for using skills)

### Step 1: Clone Repository

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
```

### Step 2: Install Dependencies (Optional)

Most scripts use Python standard library only:

```bash
# Optional dependencies for future features
pip install pyyaml
```

### Step 3: Manual Copy to Agent Directory

#### For Claude Code

```bash
# Copy all skills
cp -r marketing-skill ~/.claude/skills/
cp -r c-level-advisor ~/.claude/skills/
cp -r product-team ~/.claude/skills/
cp -r project-management ~/.claude/skills/
cp -r engineering-team ~/.claude/skills/
cp -r ra-qm-team ~/.claude/skills/

# Or copy single skill
cp -r marketing-skill/content-creator ~/.claude/skills/content-creator
```

#### For Cursor

```bash
# Copy to project directory
mkdir -p .cursor/skills
cp -r marketing-skill .cursor/skills/
```

#### For VS Code/Copilot

```bash
# Copy to project directory
mkdir -p .github/skills
cp -r engineering-team .github/skills/
```

### Step 4: Verify Python Tools

```bash
# Test marketing tools
python marketing-skill/content-creator/scripts/brand_voice_analyzer.py --help
python marketing-skill/content-creator/scripts/seo_optimizer.py --help

# Test C-level tools
python c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py --help
python c-level-advisor/ceo-advisor/scripts/strategy_analyzer.py --help

# Test product tools
python product-team/product-manager-toolkit/scripts/rice_prioritizer.py --help
python product-team/ui-design-system/scripts/design_token_generator.py --help
```

---

## Verification & Testing

### Verify Universal Installer Installation

```bash
# Check Claude Code installation
ls ~/.claude/skills/

# Check Cursor installation
ls .cursor/skills/

# Check VS Code installation
ls .github/skills/

# Check Goose installation
ls ~/.config/goose/skills/
```

### Test Skill Usage

#### In Claude Code

1. Open Claude Code
2. Start a new conversation
3. Test a skill:
   ```
   Using the content-creator skill, analyze this text for brand voice:
   "Our platform revolutionizes data analytics..."
   ```

#### In Cursor

1. Open Cursor
2. Use Cmd+K or Ctrl+K
3. Reference skill:
   ```
   @content-creator analyze brand voice for this file
   ```

### Test Python Tools Locally

```bash
# Create test file
echo "Sample content for analysis" > test-article.txt

# Run brand voice analysis
python ~/.claude/skills/content-creator/scripts/brand_voice_analyzer.py test-article.txt

# Run SEO optimization
python ~/.claude/skills/content-creator/scripts/seo_optimizer.py test-article.txt "sample keyword"
```

---

## Troubleshooting

### Universal Installer Issues

#### Issue: "Command not found: npx"

**Solution:** Install Node.js and npm

```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt-get install nodejs npm

# Windows
# Download from https://nodejs.org/
```

#### Issue: "Failed to install skills"

**Solution:** Check network connection and permissions

```bash
# Check network
curl https://github.com/alirezarezvani/claude-skills

# Check write permissions
ls -la ~/.claude/
```

#### Issue: "Skills not showing in agent"

**Solution:** Restart agent and verify installation location

```bash
# Verify installation
ls -R ~/.claude/skills/

# Restart Claude Code
# Close and reopen application
```

### Manual Installation Issues

#### Issue: Python scripts not executable

**Solution:** Add execute permissions

```bash
chmod +x marketing-skill/content-creator/scripts/*.py
chmod +x c-level-advisor/*/scripts/*.py
chmod +x product-team/*/scripts/*.py
```

#### Issue: "Module not found" errors

**Solution:** Install required dependencies

```bash
# Install Python dependencies
pip install pyyaml

# Or use Python 3 specifically
pip3 install pyyaml
```

#### Issue: Skills not recognized by agent

**Solution:** Verify SKILL.md format and location

```bash
# Check SKILL.md exists
ls ~/.claude/skills/content-creator/SKILL.md

# Verify YAML frontmatter
head -20 ~/.claude/skills/content-creator/SKILL.md
```

### Agent-Specific Issues

#### Claude Code

```bash
# Reset skills directory
rm -rf ~/.claude/skills/
mkdir -p ~/.claude/skills/

# Reinstall
npx ai-agent-skills install alirezarezvani/claude-skills --agent claude
```

#### Cursor

```bash
# Cursor uses project-local skills
# Verify project directory has .cursor/skills/

ls .cursor/skills/
```

#### VS Code/Copilot

```bash
# GitHub Copilot uses .github/skills/
# Verify directory structure

ls .github/skills/
```

---

## Uninstallation

### Universal Installer (All Agents)

```bash
# Remove from Claude Code
rm -rf ~/.claude/skills/alirezarezvani/claude-skills/

# Remove from Cursor
rm -rf .cursor/skills/alirezarezvani/claude-skills/

# Remove from VS Code
rm -rf .github/skills/alirezarezvani/claude-skills/

# Remove from Goose
rm -rf ~/.config/goose/skills/alirezarezvani/claude-skills/
```

### Manual Installation

```bash
# Clone directory
rm -rf claude-skills/

# Copied skills
rm -rf ~/.claude/skills/marketing-skill/
rm -rf ~/.claude/skills/engineering-team/
# etc.
```

### Remove Individual Skills

```bash
# Example: Remove content-creator from Claude Code
rm -rf ~/.claude/skills/content-creator/

# Example: Remove fullstack-engineer from Cursor
rm -rf .cursor/skills/fullstack-engineer/
```

---

## OpenAI Codex Installation

OpenAI Codex users can install skills using the methods below. This repository provides full Codex compatibility through a `.codex/skills/` directory with symlinks to all 43 skills.

### Method 1: Universal Installer (Recommended)

```bash
# Install all skills to Codex
npx ai-agent-skills install alirezarezvani/claude-skills --agent codex

# Preview before installing
npx ai-agent-skills install alirezarezvani/claude-skills --agent codex --dry-run
```

### Method 2: Direct Installation Script

For manual installation using the provided scripts:

**macOS/Linux:**
```bash
# Clone repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Generate symlinks (if not already present)
python scripts/sync-codex-skills.py

# Install all skills to ~/.codex/skills/
./scripts/codex-install.sh

# Or install specific category
./scripts/codex-install.sh --category marketing
./scripts/codex-install.sh --category engineering

# Or install single skill
./scripts/codex-install.sh --skill content-creator

# List available skills
./scripts/codex-install.sh --list
```

**Windows:**
```cmd
REM Clone repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

REM Generate structure (if not already present)
python scripts\sync-codex-skills.py

REM Install all skills to %USERPROFILE%\.codex\skills\
scripts\codex-install.bat

REM Or install single skill
scripts\codex-install.bat --skill content-creator

REM List available skills
scripts\codex-install.bat --list
```

### Method 3: Manual Installation

```bash
# Clone repository
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills

# Copy skills (following symlinks) to Codex directory
mkdir -p ~/.codex/skills
cp -rL .codex/skills/* ~/.codex/skills/
```

### Verification

```bash
# Check installed skills
ls ~/.codex/skills/

# Verify skill structure
ls ~/.codex/skills/content-creator/
# Should show: SKILL.md, scripts/, references/, assets/

# Check total skill count
ls ~/.codex/skills/ | wc -l
# Should show: 53
```

### Available Categories

| Category | Skills | Examples |
|----------|--------|----------|
| **c-level** | 2 | ceo-advisor, cto-advisor |
| **engineering** | 18 | senior-fullstack, aws-solution-architect, senior-ml-engineer |
| **marketing** | 6 | content-creator, marketing-demand-acquisition, social-media-analyzer |
| **product** | 5 | product-manager-toolkit, agile-product-owner, ui-design-system |
| **project-management** | 6 | scrum-master, senior-pm, jira-expert, confluence-expert |
| **ra-qm** | 12 | regulatory-affairs-head, quality-manager-qms-iso13485, gdpr-dsgvo-expert |
| **business-growth** | 3 | customer-success-manager, sales-engineer, revenue-operations |
| **finance** | 1 | financial-analyst |

See `.codex/skills-index.json` for the complete manifest with descriptions.

---

## Advanced: Installation Locations Reference

| Agent | Default Location | Flag | Notes |
|-------|------------------|------|-------|
| **Claude Code** | `~/.claude/skills/` | `--agent claude` | User-level installation |
| **Cursor** | `.cursor/skills/` | `--agent cursor` | Project-level installation |
| **VS Code/Copilot** | `.github/skills/` | `--agent vscode` | Project-level installation |
| **Goose** | `~/.config/goose/skills/` | `--agent goose` | User-level installation |
| **Amp** | Platform-specific | `--agent amp` | Varies by platform |
| **Codex** | `~/.codex/skills/` | `--agent codex` | User-level installation |
| **Letta** | Platform-specific | `--agent letta` | Varies by platform |
| **OpenCode** | Platform-specific | `--agent opencode` | Varies by platform |
| **Project** | `.skills/` | `--agent project` | Portable, project-specific |

---

## Support

**Installation Issues?**
- Check [Troubleshooting](#troubleshooting) section above
- Review [ai-agent-skills documentation](https://github.com/skillcreatorai/Ai-Agent-Skills)
- Open issue: https://github.com/alirezarezvani/claude-skills/issues

**Feature Requests:**
- Submit via GitHub Issues with `enhancement` label

**General Questions:**
- Visit: https://alirezarezvani.com
- Blog: https://medium.com/@alirezarezvani

---

**Last Updated:** January 2026
**Skills Version:** 1.0 (53 production skills)
**Universal Installer:** [ai-agent-skills](https://github.com/skillcreatorai/Ai-Agent-Skills)

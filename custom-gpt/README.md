# Custom GPTs

Deploy claude-skills as Custom GPTs on the [OpenAI GPT Store](https://chat.openai.com/gpts).

## Available GPTs

| GPT | Tier | Category | Source Skill |
|-----|------|----------|-------------|
| [Solo Founder](solo-founder-gpt.md) | 🟢 Free | Productivity | `agents/personas/solo-founder.md` |
| [Conversion Copywriter](copywriting-gpt.md) | 🟢 Free | Writing / Marketing | `marketing-skill/copywriting/SKILL.md` |
| [SEO Audit Expert](seo-audit-gpt.md) | 🟢 Free | Marketing | `marketing-skill/seo-audit/SKILL.md` |
| [Content Strategist](content-strategist-gpt.md) | 🟢 Free | Writing / Marketing | `marketing-skill/content-strategy/SKILL.md` |
| [CTO Advisor](cto-advisor-gpt.md) | 🔒 Paid | Programming | `c-level-advisor/cto-advisor/SKILL.md` |
| [Product Manager Toolkit](product-manager-gpt.md) | 🔒 Paid | Productivity | `product-team/product-manager-toolkit/SKILL.md` |

## How to Create a Custom GPT

### Step 1 — Open the GPT Editor

Go to [chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor) and click **"Create a GPT"**.

### Step 2 — Switch to Configure Tab

Click the **"Configure"** tab at the top (not "Create" — that's the conversational builder).

### Step 3 — Fill in the Fields

From the GPT config file (e.g., `solo-founder-gpt.md`), copy:

| Field | What to paste |
|-------|--------------|
| **Name** | The `## Name` value |
| **Description** | The `## Description` text |
| **Instructions** | Everything inside the ` ``` ` code block under `## Instructions` |
| **Conversation Starters** | The 4 items listed under `## Conversation Starters` |

### Step 4 — Set Capabilities

Check the boxes as listed in the config file's `## Capabilities` section:

- ✅ Web Browsing — most GPTs need this
- ✅ Code Interpreter — for technical GPTs (Solo Founder, CTO Advisor)
- ⬜ DALL-E — not needed for these GPTs
- ⬜ File Upload — not needed

### Step 5 — Profile Picture

Use the prompt from `## Profile Picture Prompt` with DALL-E to generate an icon, or upload your own.

### Step 6 — Save and Publish

Click **"Save"** and choose visibility:

| Visibility | When to use |
|------------|------------|
| **Everyone** | Free GPTs — maximizes reach in the GPT Store |
| **Anyone with a link** | Paid/premium GPTs — share link selectively |
| **Only me** | Testing before publishing |

## Converting Other Skills to Custom GPTs

Any skill in this repo can become a Custom GPT. Here's how:

### 1. Pick a Skill

Choose a `SKILL.md` or persona from `agents/personas/`. Best candidates:
- Self-contained (no Python tool dependencies)
- Broad audience appeal
- Clear, structured workflows

### 2. Create the Config File

```markdown
# [Skill Name] GPT — Configuration

**Tier:** FREE / PAID
**GPT Store Category:** [Pick from: Productivity, Writing, Programming, Research, Education, Lifestyle]

## Name
[Short, memorable name — 2-3 words max]

## Description
[1-2 sentences. What it does + who it's for. Include "Built on the open-source claude-skills library" for attribution.]

## Instructions
[Paste the SKILL.md content, adapted:]
- Remove file paths and bash commands (GPTs can't run local tools)
- Remove references to other skills (GPTs are standalone)
- Keep all frameworks, workflows, and decision logic
- Add attribution link at the bottom

## Conversation Starters
1. [Most common use case]
2. [Second most common]
3. [A specific scenario]
4. [An advanced use case]

## Capabilities
- [x] Web Browsing
- [ ] DALL-E Image Generation
- [x] Code Interpreter (if technical)
- [ ] File Upload
```

### 3. Adapt the Instructions

**Remove:**
- `python scripts/...` commands (no local execution)
- `Read file X` references (no filesystem)
- Cross-skill references like "see the copy-editing skill"
- Claude Code-specific features

**Keep:**
- All frameworks and mental models
- Decision trees and workflows
- Communication style rules
- Output format specifications

**Add:**
- Attribution: `This GPT is powered by the open-source claude-skills library: https://github.com/alirezarezvani/claude-skills`

### 4. Test Before Publishing

1. Create the GPT with visibility set to "Only me"
2. Run each conversation starter and verify quality
3. Try edge cases — vague inputs, complex scenarios
4. Check that the GPT asks clarifying questions when context is missing
5. Once satisfied, change visibility to "Everyone" or share the link

## Design Principles

- **No knowledge files** — instructions are self-contained for portability and faster responses
- **No custom actions** — keeps GPTs simple and maintainable
- **Attribution included** — every GPT links back to the repo
- **Web browsing enabled** — allows research of current data
- **Standalone** — each GPT works independently without other skills

## Tips for GPT Store Optimization

1. **Name** — use searchable terms (e.g., "CTO Advisor" not "TechLeadGPT")
2. **Description** — front-load the value prop, include key use cases
3. **Conversation starters** — show the range of what the GPT can do
4. **Category** — pick the most relevant GPT Store category
5. **Test with real users** — share the link and collect feedback before going public

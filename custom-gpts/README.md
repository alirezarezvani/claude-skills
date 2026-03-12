# Custom GPTs

Ready-to-use configurations for deploying claude-skills as Custom GPTs on the OpenAI GPT Store.

## Available GPTs

| GPT | Tier | Category | Based On |
|-----|------|----------|----------|
| [Solo Founder](solo-founder-gpt.md) | Free | Productivity | `agents/personas/solo-founder.md` |
| [Conversion Copywriter](copywriting-gpt.md) | Free | Writing | `marketing-skill/copywriting/SKILL.md` |
| [CTO Advisor](cto-advisor-gpt.md) | Paid | Programming | `c-level-advisor/cto-advisor/SKILL.md` |

## How to Create

1. Go to [chat.openai.com/gpts/editor](https://chat.openai.com/gpts/editor)
2. Click "Create a GPT"
3. Switch to the "Configure" tab
4. Copy the **Name**, **Description**, and **Instructions** from the GPT config file
5. Add the **Conversation Starters**
6. Enable the listed **Capabilities**
7. Click "Save" → choose "Everyone" (free) or "Anyone with a link" (paid)

## Design Decisions

- **No knowledge files** — instructions are self-contained for maximum portability
- **No custom actions** — keeps GPTs simple and maintainable
- **Attribution included** — every GPT links back to the repo in its instructions
- **Web browsing enabled** — allows GPTs to research current data when needed
- **Code interpreter** — enabled for Solo Founder and CTO Advisor (technical tasks)

# Claude Coach

A personal coach that teaches you to use Claude at its full capability — without getting in your way.

## What it does

- **Teaches** — On first use, gives you a personalized cheat-code glossary ranked by impact
- **Coaches** — Quietly watches your prompts and surfaces ONE tip per response when it spots an easy win
- **Levels you up** — Rates your prompts on request and shows you a better version

## Installation

```
/plugin install power-user-coach --marketplace alirezarezvani/claude-skills
```

Or place the `skills/claude-coach/` folder in your skills directory. Then start a new conversation and say one of:

- "Coach me on Claude"
- "Teach me the Claude cheat codes"
- "Make me a Claude power user"

The skill activates and stays on for the rest of the conversation.

### Upgrading from `claude-coach`

The plugin used to be called `claude-coach`. Claude Code reserves plugin names that start with `claude-` for Anthropic, so `claude plugin validate` rejected this marketplace. The plugin is now `power-user-coach`. An existing install shows "Plugin claude-coach not found in marketplace" after the next marketplace update. Reinstall it once:

```
/plugin uninstall claude-coach@claude-code-skills
/plugin install power-user-coach@claude-code-skills
```

The skill, `/claude-coach`, `/cs-claude-coach` and the `cs-claude-coach` agent keep their names. Only the namespaced form changes, to `/power-user-coach:claude-coach`.

## Usage

Once activated, just chat normally. The coach will:

- Stay silent on most turns (that is intentional)
- Append a ⚡ **Power-user tip** at the end of a response when it spots an easy win
- Rate your prompt when you ask "rate that prompt"
- Give a progress check when you ask "how am I doing"

To turn it off mid-conversation, say "stop with the tips" and it goes quiet.

## Philosophy

Most coaching tools are annoying because they interrupt. This one answers your actual question first, then adds at most one observation. If there is nothing genuinely useful to add, it says nothing.

## License

MIT

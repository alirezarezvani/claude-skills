# c-level-agents — Founder-Mode Executive Team

A virtual C-suite for Claude Code. Eight cs-* agents with distinct cognitive voices, seventeen `/cs:*` slash commands, one artifact-driven pipeline.

This plugin is the **surface layer** on top of the 28 c-level skills already in this repo. The skills provide frameworks and Python tools; this plugin adds:

1. **Cognitive gearing** — each role has a voice and a forcing-question protocol
2. **Slash-command invocation** — `/c-level-agents:cfo-review`, `/c-level-agents:boardroom`, `/c-level-agents:founder-mode`
3. **Strategic sprint pipeline** — Brief → Boardroom → Decide → Execute → Post-mortem
4. **Multi-role boardroom** — 6-phase deliberation across all C-roles in one command
5. **Cross-model consensus** — high-stakes memos reviewed by Claude + Codex/Gemini

Built to outclass YC Garry Tan's `gstack` by extending the same patterns (slash-first, forcing questions, artifact handoffs) into the **business** domain: real CFO, CMO, CRO, General Counsel, Compliance — not just software-shipping personas.

## Quick Start

```
/cs-onboard                          # 6-question founder interview → company-context.md
/c-level-agents:office-hours <topic>             # YC-style 6-question interrogation
/c-level-agents:founder-mode <question>          # auto-routes to the right C-role
/c-level-agents:cfo-review <plan>                # numerate skeptic stress-tests unit economics
/c-level-agents:boardroom <brief>                # full panel deliberation, 6 phases
/c-level-agents:decide <memo>                    # logs decision to two-layer memory
```

## Agent Roster

| Agent | Voice | Wraps Skill |
|---|---|---|
| cs-cfo-advisor | Numerate skeptic — "show me the spreadsheet" | cfo-advisor |
| cs-cmo-advisor | Narrative-first — "what's the story?" | cmo-advisor |
| cs-cro-advisor | Pipeline-paranoid — "where's the coverage?" | cro-advisor |
| cs-cpo-advisor | JTBD-driven — "what job hired this?" | cpo-advisor |
| cs-coo-advisor | Execution OS — "what's the cadence?" | coo-advisor |
| cs-chro-advisor | People-systems — "comp band, ladder, level" | chro-advisor |
| cs-ciso-advisor | Risk-paranoid — "what's the blast radius?" | ciso-advisor |
| cs-chief-of-staff | Router & synthesist — orchestrates boardroom | chief-of-staff |

Existing `cs-ceo-advisor` and `cs-cto-advisor` live in `/agents/c-level/` and integrate seamlessly.

## Slash Command Map

**Forcing-question office hours (8)** — interrogate before advising
- `/c-level-agents:office-hours` — 6-question YC-style intake
- `/c-level-agents:cfo-review` `/c-level-agents:cmo-review` `/c-level-agents:cpo-review` `/c-level-agents:cro-review`
- `/c-level-agents:cto-review` `/c-level-agents:ciso-review` `/c-level-agents:gc-review`

**Strategic sprint pipeline (5)** — Think → Decide → Ship for business
- `/c-level-agents:brief` → `/c-level-agents:boardroom` → `/c-level-agents:decide` → `/c-level-agents:execute` → `/c-level-agents:post-mortem`

**Meta + safety (4)**
- `/c-level-agents:founder-mode` — auto-routes to the right C-role
- `/cs-onboard` — founder interview, populates `~/.claude/company-context.md`
- `/c-level-agents:cross-eval` — multi-model consensus (Claude + Codex/Gemini, graceful degradation)
- `/c-level-agents:freeze` — locks a strategic decision for cooldown period

## Bundled tools (`vendor/`)

The agents and skills here run the analysis scripts and read the references that live in c-level-advisor. `vendor/` holds relative symlinks to those skill folders, and the files reference them as `${CLAUDE_PLUGIN_ROOT}/vendor/...`. Claude Code dereferences symlinks that stay inside the marketplace when it copies a plugin into its cache, so an install of this plugin alone carries the real files. Edit the source skill, never the link target path.

## Design Principles

- **Voice is bookended, analysis is neutral.** Persona shows in the opening line and closing handoff; the body stays rigorous.
- **Artifacts over chat.** Every command produces a Markdown artifact the next command can consume.
- **Two-layer memory.** Raw transcripts kept for reference; only approved decisions feed forward (via `decision-logger`).
- **Phase 2 isolation.** In `/c-level-agents:boardroom`, each role thinks independently before cross-examination.
- **Graceful degradation.** `/c-level-agents:cross-eval` falls back to Claude-only if no other models are configured.

## References

- [persona-voices.md](references/persona-voices.md) — voice spec for each role
- [llm-wiki-bridge.md](references/llm-wiki-bridge.md) — point company-context at an llm-wiki vault
- [c-level domain CLAUDE.md](../c-level-advisor/CLAUDE.md) — c-level domain guide
- [executive-mentor sibling](../c-level-advisor/executive-mentor/) — `/em:*` adversarial commands

## What's Different vs `gstack`

| | gstack | c-level-agents |
|---|---|---|
| Roles | ~6 software-shipping personas | 10 real C-suite roles + General Counsel lane |
| Domain | Code shipping only | Business + compliance + GTM + finance + product |
| Frameworks | Scope cut, sprint pipeline | RICE, JTBD, OKR, Wardley, ADKAR, 8-dim org health |
| Memory | Postgres + pgvector (separate repo) | Markdown via llm-wiki bridge (stdlib-only) |
| Voice | Default Claude voice | Per-role cognitive style |
| Compliance | None | ra-qm-team integration (ISO/MDR/FDA/GDPR) |
| Boardroom | Sequential review chain | 6-phase deliberation with isolation |

---

**Version:** 2.9.0
**Status:** Production Ready
**License:** MIT

---
title: "c-level-agents — Founder-Mode Executive Team — Agent Skill for Executives"
description: "Founder-mode executive team. 8 cs-* C-suite agents (CFO, CMO, CRO, CPO, COO, CHRO, CISO, Chief of Staff) and 17 /cs:* slash commands for. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# c-level-agents — Founder-Mode Executive Team

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-Level Advisory</span>
<span class="meta-badge">:material-identifier: `c-level-agents`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/skills/c-level-agents/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install c-level-skills</code>
</div>


A virtual C-suite delivered through slash commands and persona agents.

## Keywords

founder mode, virtual c-suite, executive team, boardroom, office hours, cfo review, cmo review, strategic sprint, decision logging, cross-model consensus, persona agents, chief of staff, forcing questions

## What This Plugin Provides

### 8 cs-* Agents (in `agents/`)

Each agent wraps an existing c-level skill and adds:
- A distinct cognitive voice (numerate skeptic, narrative-first, etc.)
- Forcing questions specific to the role
- Workflow orchestration tied to skill Python tools
- Output template: Bottom Line → What → Why → How to Act → Your Decision

See [`references/persona-voices.md`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/skills/references/persona-voices.md) for voice specs.

### 17 /cs:* Slash Commands (in `skills/`)

**Forcing-question office hours (8):**
- `/cs:office-hours` — YC-style 6-question intake
- `/cs:cfo-review` — unit economics, runway, dilution
- `/cs:cmo-review` — ICP, CAC payback, positioning
- `/cs:cpo-review` — RICE, JTBD, North Star, PMF
- `/cs:cro-review` — pipeline coverage, win rate, NRR
- `/cs:cto-review` — architecture risk, scaling cliff
- `/cs:ciso-review` — threat model, blast radius, compliance
- `/cs:gc-review` — contracts, IP, regulatory, term sheets

**Strategic sprint pipeline (5):**
- `/cs:brief` → `/cs:boardroom` → `/cs:decide` → `/cs:execute` → `/cs:post-mortem`

**Meta + safety (4):**
- `/cs:founder-mode` — auto-routes to the right C-role
- `/cs:onboard` — founder interview → `company-context.md`
- `/cs:cross-eval` — multi-model consensus
- `/cs:freeze` — cooldown lock on a decision

## Quick Start

```
/cs:onboard                          # populate company context first
/cs:office-hours "should we hire a VP Sales?"
/cs:founder-mode "runway pressure"   # auto-routes to CFO
/cs:boardroom briefs/pricing-v3.md   # full panel
```

## Architecture

```
User question
   │
   ├─ Single-role? → cs-{role}-advisor agent
   │                     ↓
   │                  /cs:{role}-review command (forcing Qs)
   │                     ↓
   │                  Skill tools + references
   │                     ↓
   │                  Bottom Line + Memo
   │
   └─ Multi-role?  → /cs:boardroom
                        ↓
                     6-phase deliberation (Phase 2 isolation)
                        ↓
                     /cs:decide → decision-logger (two-layer memory)
                        ↓
                     /cs:execute → 90-day plan
```

## Integration Points

- **Existing 28 c-level skills** — wrapped, not replaced
- **decision-logger** — every `/cs:decide` writes here
- **chief-of-staff** — routing layer the agent orchestrates
- **board-meeting** — protocol the `/cs:boardroom` command runs
- **llm-wiki** — optional persistent memory bridge (see [`references/llm-wiki-bridge.md`](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/skills/references/llm-wiki-bridge.md))
- **executive-mentor** — adversarial `/em:*` commands stack cleanly on top

## Design Principles

1. **Voice is bookended, analysis is neutral.**
2. **Artifacts over chat.** Every command produces a Markdown artifact the next command consumes.
3. **Phase 2 isolation in boardroom.** Independent thinking before cross-examination.
4. **Graceful degradation.** `/cs:cross-eval` falls back to Claude-only.
5. **No paid dependencies.** All Python tools are stdlib-only.

## References

- [persona-voices.md](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/references/persona-voices.md)
- [llm-wiki-bridge.md](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/c-level-agents/references/llm-wiki-bridge.md)
- [Parent c-level CLAUDE.md](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/CLAUDE.md)
- [Existing executive-mentor sibling](https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/executive-mentor)

---

**Version:** 1.0.0
**Last Updated:** 2026-05-12
**Status:** Production Ready

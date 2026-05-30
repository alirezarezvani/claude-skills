---
title: "/cs-dossier — Slash Command for AI Coding Agents"
description: "/cs:dossier <entity> — Decision-grade entity research with mandatory hypothesis-testing. 6-Q grill-me intake (Q4 hypothesis MANDATORY) → ≥30%. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-dossier

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research/dossier/commands/cs-dossier.md">Source</a></span>
</div>


**Command:** `/cs:dossier <entity>`

The `cs-dossier` persona produces a hypothesis-tested research dossier on a specific company, person, nonprofit, or government org — **NOT** a generic profile.

## When to Run

- Sales meeting / partnership pitch (need conversation hooks tied to specifics)
- Investment / acquisition diligence
- Journalism / personal vetting (with sensitivity exclusions)
- Job interview prep
- Competitive intelligence

## When NOT to Run

- Generic curiosity ("what does this company do?") → search the web yourself
- Quick lookup → faster to just google
- No hypothesis to test → the skill refuses, by design

## Non-Generic by Design

The skill refuses to be a Wikipedia summary. Q4 (your hypothesis) is **mandatory** — without it, the dossier confirms what you already think and is worthless for decisions.

## Forcing Intake (6 Questions, One at a Time)

| Q | Asks | Notes |
|---|---|---|
| Q1 | Subject identity (name + disambiguating identifier) | refuses ambiguous names |
| Q2 | Subject type: person / company / nonprofit / gov org / other | forcing choice — drives source matrix |
| Q3 | Purpose: sales / investment / acquisition / journalism / interview / competitive / vetting / other | forcing choice — drives angle + sensitivity |
| Q4 | **Hypothesis (MANDATORY)** — what you already believe + want to verify/disprove | non-skippable; pushed back once if refused |
| Q5 | Depth: 5-min brief or 15-min decision-grade dossier | forcing choice |
| Q6 | Sensitivities to exclude | conditional — only if Q3 ∈ {journalism, personal vetting} |

Stop condition: after Q6 (or earlier with skips), commit and start Phase 2. Never re-open.

## What You Get

After all phases:

```
dossier_<entity-slug>_<YYYY-MM-DD>.docx

9 sections:
1. Executive Summary (verdict: SUPPORTED/PARTIALLY/DISPROVEN/INCONCLUSIVE + 3 must-know)
2. Identity Facts Table (founded/born, location, size, role, affiliations; sourced + tiered)
3. Hypothesis Test (verbatim hypothesis + supporting evidence + disconfirming evidence + verdict)
4. 12-Month Activity Timeline (news, hires, departures, products, controversies)
5. Network Signals (collaborators / investors / customers / advisors)
6. Reputation Signals (sentiment, Glassdoor, peer mentions)
7. Red Flags + Hidden Patterns (litigation, departures, financials, tiered)
8. Conversation Hooks (3-5 finding-tied hooks with framing)
9. Source Provenance + Audit Log (per-source tier + search summary + counts)
```

## Hypothesis-Testing Discipline

**≥30% of search budget allocated to disconfirming queries.** This is the non-negotiable differentiator from a generic profile.

Example for hypothesis "Microsoft is consolidating AI spend on Foundry":

| Query type | Example |
|---|---|
| **Supporting** (would confirm) | "Microsoft Foundry adoption 2026" |
| **Supporting** | "Microsoft AI infrastructure consolidation" |
| **Disconfirming** (would refute) | "Microsoft OpenAI deal renegotiation" |
| **Disconfirming** | "Microsoft AI vendor diversification" |
| **Disconfirming** | "Microsoft third-party model partnerships 2026" |

`scripts/disconfirming_evidence_balance.py` enforces the ratio. Halts at <30% and prompts more disconfirming queries.

## Source Reliability Tiering

Every fact in the DOCX tagged with tier (primary / secondary / tertiary):

| Tier | Examples |
|---|---|
| **Primary** | SEC EDGAR filings, court records, official .gov sites, company official website |
| **Secondary** | Mainstream news (NYT, WSJ, Reuters), trade press (TechCrunch, The Information) |
| **Tertiary** | Blogs, forums (Reddit, HN), Glassdoor, social media |

`scripts/source_tier_classifier.py` does this from URL.

## Discipline (Research-Pack Convention)

- **One intake Q per turn.** Never bundle.
- **Q4 mandatory.** Push back once; fall back to "most surprising finding" implicit hypothesis with flag.
- **≥30% disconfirming.** Enforced by tool.
- **Sequential search.** WebSearch + WebFetch sequential, 1 q/sec etiquette.
- **Source discipline.** Cite only session results. Training knowledge labeled `[Background — verify before quoting]`, excluded from counts.
- **Three-count + tier.** Sent / received / cited + per-tier breakdown.
- **Subject disambiguation before Phase 3.** Refuse ambiguous names.
- **Sensitivity exclusions honored.** If Q6 excluded "medical history", don't surface even if found.
- **Conversation hooks finding-tied.** Generic hooks ("ask about their roadmap") rejected.
- **BYOK MCP flagged in audit.** Crunchbase / Pitchbook usage surfaced.

## Trigger Phrases

- "research [company]"
- "dossier on [person/company]"
- "background check on [entity]"
- "prep me for a meeting with [person/company]"
- "due diligence on [company]"
- "what should I know about [entity]"
- "research [person] before I [meet/hire/invest]"
- "competitor research on [company]"
- "investor diligence [company]"
- "interview prep for [company]"

## Anti-Patterns Rejected

- Producing a dossier without forcing Q4 hypothesis
- <30% disconfirming search budget (confirmation bias)
- Batching intake questions
- Accepting ambiguous subject names
- Generic conversation hooks ("ask about their roadmap")
- Sensationalizing red flags (tier them, don't editorialize)
- Skipping source-reliability tier on flags
- Fabricating coverage when LinkedIn blocked
- Using BYOK MCP without flagging in audit
- Including sensitive topics user excluded (Q6)
- Confirmation-biased verdict ("SUPPORTED" without engaging with disconfirming evidence)

## Related

- Agent: [`cs-dossier`](https://github.com/alirezarezvani/claude-skills/tree/main/research/dossier/agents/cs-dossier.md)
- Skill: [`dossier`](https://github.com/alirezarezvani/claude-skills/tree/main/research/dossier/skills/dossier/SKILL.md)
- Source spec: [`megaprompts/12-dossier-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/12-dossier-megaprompt.md)
- Siblings: `/cs:litreview`, `/cs:grants`, `/cs:pulse`
- Future: `/cs:patent`, `/cs:syllabus`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/12-dossier-megaprompt.md`

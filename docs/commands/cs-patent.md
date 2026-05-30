---
title: "/cs-patent — Slash Command for AI Coding Agents"
description: "/cs:patent <invention> — Patent prior-art + landscape intelligence with mandatory sub-use-case commitment. 6-Q grill-me intake (Q2 picks one of. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-patent

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research/patent/commands/cs-patent.md">Source</a></span>
</div>


**Command:** `/cs:patent <invention description>`

The `cs-patent` persona produces a sub-use-case-tailored patent dossier. **Refuses generic "patent help"** — must commit to one of 5 sub-use-cases at Q2.

## Forcing Intake (6 Questions, One at a Time)

| Q | Asks | Notes |
|---|---|---|
| Q1 | Invention (2-3 sentences, specific) | refuses vague; "AI for healthcare" pushed back |
| Q2 | Sub-use-case: novelty / FTO / landscape / diligence / litigation | **Forcing — refuses "all of them"** |
| Q3 | Jurisdictions (US/EP/CN/JP/KR/PCT/worldwide) | Asked only for FTO/landscape/diligence |
| Q4 | Known prior art (patent number or paper) | Anchor; accept "none" |
| Q5 | Risk tolerance: strict / signal-gathering | Asked for novelty + FTO |
| Q6 | Attorney status (have you spoken to one?) | Asked for novelty + FTO; triggers disclaimer |

Stop condition: after Q6 (or earlier with skips). Never re-open.

## What You Get

```
patent_<invention-slug>_<sub-use-case>_<YYYY-MM-DD>.docx

8 sections:
1. Executive Summary + Verdict (NOVEL/CLEAR/FLAGGED/etc.) + legal disclaimer
2. Closest Prior Art (5-10 ranked, claim-text extracted, hyperlinked)
3. Patent Landscape (top filers, 10-yr trend, CPC distribution)
4. Citation Graph Signals (foundational + recent high-cite, if Lens-enabled)
5. Geographic Coverage (FTO/landscape/diligence only)
6. FTO Flags (FTO only — risk per claim per jurisdiction)
7. Strategy + Recommendations (sub-use-case-specific)
8. Audit Log (searches, counts, plan-tier, attorney reminder)
```

## Per-Sub-Use-Case Behavior

| Sub-use-case | Search emphasis | DOCX adjustment |
|---|---|---|
| Novelty | Narrow + claims-focused; pre-filing date irrelevant | Sections 5-6 abbreviated; verdict NOVEL/POTENTIALLY/NOT NOVEL |
| FTO | Active patents only; jurisdiction-filtered | Section 6 expanded; verdict CLEAR/FLAGGED/HIGH RISK per jurisdiction |
| Competitive landscape | Breadth + filer tally + CPC trends | Section 3 expanded; verdict = top-5 filers + 3 emerging entrants |
| Acquisition diligence | Specific assignee + portfolio + assignment chain | Sections 3+5 expanded; ownership-verification flags |
| Litigation prior-art | Target patent + adjacent art before priority date | Section 2 = ranked knock-out candidates |

## Discipline

- **Sub-use-case commitment mandatory** at Q2
- **Sequential search 1 q/sec** across all sources
- **CPC class follow-up** after initial keyword search
- **Family resolution** — same-invention duplicates reported once
- **Date discipline** — filing/priority/publication/grant distinguished
- **Legal disclaimer mandatory** for novelty + FTO
- **Source discipline** — only this session's tool calls
- **Three-count tracking** — sent / received / cited
- **Out-of-scope flagging** — trademark/copyright/trade-secret rejected at intake

## Trigger Phrases

- "prior art search for [invention]"
- "patent search on [topic]"
- "freedom to operate analysis"
- "FTO for [product]"
- "patent landscape for [field]"
- "is [invention] novel"
- "patents on [topic]"
- "competitive patent analysis"
- "prior art for litigation"
- "patent diligence on [company]"

## Anti-Patterns Rejected

- Starting any search before user commits to a sub-use-case (refuses generic "patent help")
- Batching all intake questions
- Accepting vague invention descriptions
- Keyword-only search without CPC/IPC class follow-up
- Treating family members as separate hits
- Confusing filing date with priority/publication/grant date
- Skipping legal disclaimer when sub-use-case has legal consequences
- Reporting verdict without claim-text evidence
- Fabricating Lens.org citation data when key absent
- Suggesting design-arounds without acknowledging attorney review required
- Skipping audit log

## Related

- Agent: [`cs-patent`](https://github.com/alirezarezvani/claude-skills/tree/main/research/patent/agents/cs-patent.md)
- Skill: [`patent`](https://github.com/alirezarezvani/claude-skills/tree/main/research/patent/skills/patent/SKILL.md)
- Source spec: [`megaprompts/11-patent-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/11-patent-megaprompt.md)
- Siblings: `/cs:litreview`, `/cs:grants`, `/cs:dossier`, `/cs:pulse`
- Future: `/cs:syllabus`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/11-patent-megaprompt.md`

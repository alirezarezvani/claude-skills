---
name: "named-persona-adversarial-review"
description: "Web-grounded multi-persona adversarial code review using real engineers' documented principles. Use when the target repo has no automated review bots and you need pre-submit hardening. Use when you want diverse perspectives from named experts (Thompson, Torvalds, Carmack, Feynman, etc.) rather than abstract roles. Use for reviewing code, docs, or methodologies."
---

# Named-Persona Adversarial Review

## Description

Extends `adversarial-reviewer` with **web-grounded real personas** instead of abstract roles. Instead of generic "Saboteur" or "Security Auditor," this skill uses web search to retrieve the actual documented principles of named engineers (Ken Thompson, Linus Torvalds, John Carmack, Richard Feynman, etc.) and applies them as review lenses.

Each persona is backed by searchable, citable principles — not vibes. Combined with a product perspective (Steve Jobs, Marty Cagan), this creates genuinely diverse viewpoints that catch blind spots abstract roles miss.

## Features

- **Named real engineers** — Web-search their latest principles, apply as review lens
- **Two-pillar structure** — 2 engineers (code) + 1 product (UX) per round
- **Web-grounded** — Each persona's priorities come from real-time search, not static definitions
- **Credible-only findings** — Invented findings are worse than none. If zero genuine issues exist against a persona's principles, they must explain WHY with specific citations. Generic noise ("add error handling") is rejected.
- **Severity promotion** — 2+ personas catching same issue promotes it one level
- **Feynman honesty check** — Post-review: "Would this person actually say this, or am I projecting?"
- **Finding quality gate** — Every finding must cite a specific quote or documented principle from the named person. If you can't find the quote, the finding is likely invented. Web-search the person's name + the claim before filing.
- **Formats follow `adversarial-reviewer`** — Same severity, output format, anti-patterns

## Problem This Solves

`adversarial-reviewer` uses three abstract roles (Saboteur, New Hire, Security Auditor). These are effective but generic — they don't capture the specific insights of real engineering principles. A "Security Auditor" reviews for OWASP patterns, but Linus Torvalds reviewing for "good taste" catches entirely different issues: data structures that create unnecessary edge cases.

This skill adds **specificity through real people**. Web search retrieves what Ken Thompson actually said about simplicity, what John Carmack actually said about performance as moral craft. The review is grounded in documented, citable principles — not an AI's vague impression of what a "senior engineer" might think.

## Quick Start

```
/adversarial-review --personas named    # Use named personas instead of abstract roles
/adversarial-review --personas named --rounds 3   # 3 rounds, 9 total perspectives
```

Without slash command support, use prompt-level:

```
Review [target] using Named-Persona Adversarial Review:
1. Search "[Engineer Name] engineering principles" for 3 engineers + 1 product person
2. Role-play each, apply their specific principles
3. Deduplicate, promote cross-persona findings
4. Output structured report (same format as adversarial-reviewer)
```

## Review Workflow

### Step 0: Understand the Target

Read the full target twice before any role-play:
1. First pass — what changed, what's the purpose
2. Second pass — why this approach, what trade-offs

### Step 1: Search for Principles

For each persona, search: `"[Name] engineering principles code review"`. Extract 3-5 actionable criteria from actual quotes or documented principles. Do not improvise generic "as a senior engineer" advice.

### Step 2: Independent Reviews (3 personas)

**Two engineers + one product person per round.** Each persona gets:
- **Mindset:** One sentence from search results
- **Priorities:** 3-5 criteria extracted from their actual principles
- **Finding:** ≥1 concrete issue with cited reasoning, OR explain why none exist

**Engineer pool** (select per round):
| Persona | Known For |
|---------|-----------|
| Ken Thompson | Unix minimalism: "Do one thing well" |
| Linus Torvalds | Good taste: "Eliminate the special case" |
| John Carmack | Performance as moral craft |
| Richard Feynman | Scientific integrity: "Don't fool yourself" |
| Kent Beck | XP values: simplicity, feedback, courage |
| Fred Brooks | Essential vs accidental complexity |

**Product pool** (one per round):
| Persona | Known For |
|---------|-----------|
| Steve Jobs | Simplicity: "Design is how it works" |
| Marty Cagan | Empowered teams: "Problem, not features" |
| Intercom PM | Onboarding: "First 30 seconds is everything" |

### Step 3: Deduplicate and Synthesize

Same as `adversarial-reviewer` Step 4.

## Feynman Honesty Check

After each review, ask:
1. Would [Name] actually say this, or am I projecting?
2. Did I cite their actual principles, or use generic phrasing?
3. Did I report bad news? If all findings are NOTE-level, switch perspectives and re-review.

> "The first principle is that you must not fool yourself, and you are the easiest person to fool." — Richard Feynman

## Anti-Patterns

Inherits all anti-patterns from `adversarial-reviewer`. Additionally:

| Anti-Pattern | Why |
|-------------|-----|
| Using "as a senior engineer" without searching | Not a named persona. Search first. |
| Same 3 personas every time | Rotate. Different problems need different engineers. |
| Product person skipped or replaced with 3rd engineer | Product perspective catches what engineers miss. Always include one. |
| Skipping the honesty check | Role-play without verification = sophisticated rubber-stamp. |

## When to Use This

- Target repo has no automated review bots — this compensates
- Self-authored PR needs hardening before submit
- `adversarial-reviewer` findings feel generic — add real names for specificity
- Reviewing methodologies or documentation (not just code) — product personas excel here

## Cross-References

- **Extends:** `engineering-team/adversarial-reviewer` — same severity, output, anti-patterns
- Related: `engineering-team/code-reviewer` — general code quality
- Related: `engineering-team/senior-security` — deep security analysis
- Theoretical basis: de Bono "Six Thinking Hats", Kahneman "Thinking Fast and Slow" (System 2 forcing)
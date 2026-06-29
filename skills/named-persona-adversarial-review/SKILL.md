---
name: "named-persona-adversarial-review"
description: "Web-grounded multi-persona adversarial code review using real engineers' documented principles. Use when the target repo has no automated review bots and you need pre-submit hardening. Use when you want diverse perspectives from named experts (Thompson, Torvalds, Carmack, Feynman, etc.) rather than abstract roles. Use for reviewing code, docs, or methodologies."
version: 1.0.0
tags: [review, adversarial, code-review, methodology]
---

# Named-Persona Adversarial Review

## Description

Uses **web-grounded real personas** instead of abstract roles. Instead of generic "Saboteur" or "Security Auditor," this skill web-searches the actual documented principles of named engineers (Ken Thompson, Linus Torvalds, John Carmack, Richard Feynman, etc.) and applies them as review lenses. Each persona is backed by searchable, citable principles — not vibes.

## Features

- **Named real engineers** — Web-search their principles, review through pre-extracted quotes only
- **Two-pillar structure** — 2 engineers (code) + 1 product (UX) per round, 3 personas total
- **Quote-first review** — Extract quotes BEFORE reviewing. Findings must map to pre-extracted quotes — no retrofitting
- **Symmetric burden** — Findings need 1+ quote. Zero findings needs 3+ quotes the code SUCCESSFULLY satisfies
- **Severity promotion** — 2+ personas catching same issue promotes it one level. CRITICAL + 2 concurrences → BLOCKER
- **Integrity check** — Post-review: "Would this person actually say this, or am I projecting?"
- **Self-contained** — Severity definitions, output format, and anti-patterns are all in this file

## Severity Levels

| Level | Definition | Action |
|-------|-----------|--------|
| BLOCKER | 2+ concurrences on CRITICAL or security/data-loss risk | Must fix before any further work |
| CRITICAL | Wrong result, data loss, security hole, or violates core invariant | Must fix before merge |
| WARNING | Fragile, misleading, or likely to cause future bugs | Should fix; explain if deferred |
| NOTE | Improvement opportunity that doesn't affect correctness | Optional; record for follow-up |

Promotion rule: NOTE → WARNING → CRITICAL → BLOCKER. 2+ personas independently finding the same issue promotes it one level. BLOCKER is the ceiling.

## Problem This Solves

Abstract roles produce generic feedback. "Saboteur" says "add error handling." "New Hire" says "this is confusing." Real engineers' documented principles produce specific, actionable findings. Linus Torvalds doesn't say "consider error handling" — he says "eliminate the special case entirely." That's a different action.

## Quick Start

```
/adversarial-review --personas named
/adversarial-review --personas named --rounds 3
```

Without slash commands:
```
Review [target] using Named-Persona Adversarial Review:
1. For each persona, web-search their principles and extract 3-5 quotes
2. Review the target through ONLY those quotes
3. Each persona: find >=1 issue mapped to a quote, OR cite 3+ quotes the code satisfies
4. Deduplicate across personas, promote concurrences
5. Output structured report with severity per finding
```

## Review Workflow

### Triage (Efficiency)

| Task scope | Rounds | Cost |
|-----------|--------|------|
| Single-file, no user-facing impact | 1 round (3 personas) | ~3 web searches |
| Multi-file, architectural change | 2 rounds (6 personas) | ~6 web searches |
| Security-critical or identity/persona-related | 3+ rounds (9+ personas) | ~9+ web searches |

### Step 0: Understand AND Break the Model

1. **First pass** (top-down): what changed, what's the purpose — comprehension only
2. **Second pass** (bottom-up): read function by function, last to first. Ask: what does this function ACTUALLY guarantee vs. what its name implies? Where can it fail? What assumptions does it make about its callers?

Reading bottom-up breaks the author's mental model. You stop seeing what the author INTENDED and start seeing what each function ACTUALLY does.

### Step 1: Extract Quotes FIRST (Before Review)

For each persona, search: `"[Name] [topic] principles"`. Extract 3-5 specific, verbatim quotes before looking at the code. These quotes are the ONLY lens allowed for that persona's review.

**Do not** search with the code in mind. Search for their principles independently, then apply them. This prevents confirmation bias where you search for quotes that support an opinion you already formed.

### Step 2: Independent Reviews (3 personas per round)

**Two engineers + one product person per round.** Each persona gets:
- **Mindset:** One sentence from their extracted quotes
- **Quotes:** 3-5 verbatim quotes extracted in Step 1
- **Findings:** Review through ONLY those quotes. Each finding must map to a specific pre-extracted quote.
- **Zero-finding burden:** If no issues found, cite 3+ quotes the code successfully satisfies, with explanation of HOW. This makes non-findings equally expensive as findings — no lazy "everything looks fine."

**Engineer pool** (select per round):
| Persona | Search Query |
|---------|-------------|
| Ken Thompson | "Ken Thompson Unix simplicity principles" |
| Linus Torvalds | "Linus Torvalds good taste code review" |
| John Carmack | "John Carmack performance optimization principles" |
| Richard Feynman | "Richard Feynman scientific integrity methodology" |
| Kent Beck | "Kent Beck extreme programming values" |
| Fred Brooks | "Fred Brooks essential complexity design" |

**Product pool** (one per round):
| Persona | Search Query |
|---------|-------------|
| Steve Jobs | "Steve Jobs simplicity design philosophy" |
| Marty Cagan | "Marty Cagan empowered product teams" |
| Des Traynor | "Des Traynor product onboarding messaging" |

Reuse policy: Product personas may be reused across rounds if the scope changes. Same persona on same scope → flag in output.

### Step 3: Deduplicate and Synthesize

Cross-reference all personas' findings:
1. Group identical findings (same line/pattern, same root cause)
2. Count concurrences per finding
3. Promote severity per concurrence rule (NOTE→WARNING→CRITICAL→BLOCKER)
4. Flag findings unique to a single persona — these may be the most interesting (caught by one lens, invisible to others)

### Output Format

```markdown
# Named-Persona Adversarial Review — Round [N]

**Manager**: [Name] | **Team**: [E1], [E2], [P1]

## Per-Persona Summary

### [E1 Name] (Engineer)
- **Mindset:** [one sentence from their quotes]
- **Quotes used:** [3-5 verbatim]

| # | Severity | Finding | Quote |
|---|----------|---------|-------|
| 1 | WARNING | [finding] | "[quote]" |
| 2 | NOTE | [finding] | "[quote]" |

### [E2 Name] (Engineer)
...

### [P1 Name] (Product)
...

## Cross-Persona Findings

| # | Severity | Finding | Concurrences | Promoted From |
|---|----------|---------|-------------|---------------|
| 1 | CRITICAL | [finding] | E1 + E2 | WARNING → CRITICAL |

## Round Verdict

**BLOCK / CONCERNS / CLEAN** — [one-sentence justification]
```

## Integrity Check

After each round, ask:
1. Would [Name] actually say this, or am I projecting?
2. Did I review through pre-extracted quotes, or did I form opinions first and search for support?
3. Are the quotes verbatim from search results, or did I paraphrase to fit my finding?
4. Did I report bad news? If all findings are NOTE-level, switch perspectives and re-review.

> "The first principle is that you must not fool yourself, and you are the easiest person to fool." — Richard Feynman

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| Using "as a senior engineer" without searching | Not a named persona. Search first. |
| Same 3 personas every time | Rotate. Different problems need different lenses. |
| Product person skipped or replaced with 3rd engineer | Product perspective catches what engineers miss. |
| Skipping the integrity check | Role-play without verification = sophisticated rubber-stamp. |
| Searching quotes AFTER forming an opinion | Confirmation bias. Extract quotes first, review second. |
| Finding with no mapped quote | If it's a real issue, a real engineer has said something about it. |
| "Everything looks fine" without 3+ quotes | Non-findings must be as well-supported as findings. |
| Skipping bottom-up second pass | Reading twice top-to-bottom entrenches the author's model. |

## When to Use

- Target repo has no automated review bots — this compensates
- Self-authored PR needs hardening before submit
- Abstract-role review findings feel generic — add real names for specificity
- Reviewing methodologies or documentation (not just code) — product personas excel here

## Cross-References

- `adversarial-reviewer` — Abstract-role adversarial review (simpler, faster, no web search)
- `code-reviewer` — Standard code quality review
- `senior-security` — Deep security-specific analysis
- Theoretical basis: de Bono "Six Thinking Hats", Kahneman "Thinking Fast and Slow" (System 2 forcing)

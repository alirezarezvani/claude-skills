---
name: "named-persona-adversarial-review"
description: "Web-grounded multi-persona adversarial code review using real engineers' documented philosophies. Use when the target repo has no automated review bots and you need pre-submit hardening. Use when you want diverse perspectives from named experts (Thompson, Torvalds, Carmack, Feynman, etc.) rather than abstract roles. Use for reviewing code, docs, or methodologies."
---

# Named-Persona Adversarial Review

## Description

Extends `adversarial-reviewer` with **web-grounded real personas** instead of abstract roles. Instead of generic "Saboteur" or "Security Auditor," this skill uses web search to retrieve the actual documented philosophies of named engineers (Ken Thompson, Linus Torvalds, John Carmack, Richard Feynman, etc.) and applies them as review lenses.

Each persona is backed by searchable, citable philosophy — not vibes. Combined with a product perspective (Steve Jobs, Marty Cagan), this creates genuinely diverse viewpoints that catch blind spots abstract roles miss.

## Features

- **Named real engineers** — Web-search their latest philosophy, apply as review lens
- **Two-pillar structure** — 2 engineers (code reliability) + 1 product person (user experience) per round
- **Web-grounded** — Each persona's priorities come from real-time search, not static definitions
- **Credible-only findings** — Invented findings are worse than none. If zero genuine issues exist against a persona's philosophy, they must explain WHY with specific citations. Generic noise ("add error handling") is rejected.
- **Severity promotion** — 2+ personas catching same issue promotes it one level
- **Feynman honesty check** — Post-review: "Would this person actually say this, or am I projecting?"
- **Finding quality gate** — Every finding must cite a specific quote or documented principle from the named person. If you can't find the quote, the finding is likely invented. Web-search the person's name + the claim before filing.
- **Formats follow `adversarial-reviewer`** — Same severity, output format, anti-patterns

## Problem This Solves

`adversarial-reviewer` uses three abstract roles (Saboteur, New Hire, Security Auditor). These are effective but generic — they don't capture the specific insights of real engineering philosophies. A "Security Auditor" reviews for OWASP patterns, but Linus Torvalds reviewing for "good taste" catches entirely different issues: data structures that create unnecessary edge cases.

This skill adds **specificity through real people**. Web search retrieves what Ken Thompson actually said about simplicity, what John Carmack actually said about performance as moral craft. The review is grounded in documented, citable philosophy — not an AI's vague impression of what a "senior engineer" might think.

## Quick Start

```
Review this code using named-persona-adversarial-review.
```

### Standard 3-Persona Round

```
Review [target] using:
1. Linus Torvalds (engineering: taste, zero special cases)
2. Ken Thompson (engineering: simplicity, distrust of complexity)
3. Steve Jobs (product: user experience, ruthless prioritization)

Each must find ≥1 actionable issue.
```

### Philosophy-Focused Round

```
Review this function using Richard Feynman's philosophy:
"The first principle is that you must not fool yourself — and you are the easiest person to fool."
Find every place the code fools itself about correctness.
```

## Workflow

### Step 1: Select Personas

Choose 2 engineers + 1 product person. Rotate per round.

**Engineer Pool:**
| Persona | Philosophy | Best For |
|---------|-----------|----------|
| Linus Torvalds | "Good taste" — code with zero special cases | Architecture, data structures |
| Ken Thompson | "When in doubt, use brute force" — simplicity over cleverness | Algorithms, security boundaries |
| John Carmack | "Performance is a moral imperative" — resource discipline | Game loops, real-time, hot paths |
| Richard Feynman | "You are the easiest person to fool" — self-deception | Testing, validation, proofs |
| Margaret Hamilton | "Software should be designed to work, not fixed to work" | Error handling, fault tolerance |
| Donald Knuth | "Premature optimization is the root of all evil" | Algorithm correctness first |
| Edsger Dijkstra | "Testing shows the presence, not the absence of bugs" | Formal reasoning, invariants |

**Product Pool:**
| Persona | Philosophy | Best For |
|---------|-----------|----------|
| Steve Jobs | "It just works" — ruthless simplicity | UX flows, onboarding |
| Marty Cagan | "Fall in love with the problem, not the solution" | Feature design |
| Julie Zhuo | "Design is not just how it looks, but how it works" | Interaction design |
| Intercom PM | "Every feature must earn its place" | Scope, prioritization |

### Step 2: Web-Ground Each Persona

Before reviewing, web-search each selected persona:
```
"[name] [topic] philosophy" — e.g., "Linus Torvalds good taste in code"
"[name] on [technology]" — e.g., "Ken Thompson on simplicity"
```

Retrieve 2-3 specific quotes or principles. These become the review lens.

### Step 3: Run the Review

Each persona reviews the target independently, applying their specific philosophy. Every finding must cite:
1. What they found
2. Why it violates their philosophy
3. **A specific quote or documented principle** from that person

### Step 4: Cross-Check Severity

If 2+ personas independently find the same issue → promote severity one level.

### Step 5: Feynman Honesty Check

After the review, ask: "Would Linus Torvalds ACTUALLY say this, or did I project a generic opinion onto him?" If the quote can't be found via web search, the finding is suspect.

## Anti-Patterns

- ❌ "Consider adding error handling" — Generic. What would THIS person specifically say?
- ❌ Using a persona without web-searching their actual philosophy first.
- ❌ Forcing a finding when the code is genuinely clean — say "no credible issues found, here's why: [citation]."
- ❌ Persona drift — Linus doesn't care about mobile UX. Match persona to problem domain.
- ❌ Skipping the Feynman check — AI love to sound like experts. Verify.

## Cross-References

- `adversarial-reviewer` — Base adversarial review skill (abstract roles).
- `code-reviewer` — Standard code quality review.
- `senior-security` — Deep security-specific review.
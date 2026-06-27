---
name: "named-persona-adversarial-review"
description: "Code review with real engineers' philosophies, not abstract roles. Catches what automated bots and generic reviewers miss."
---

# Named-Persona Adversarial Review

> **TL;DR:** Abstract roles find abstract problems. Named people with searchable, citable philosophies find problems you would actually fix. This upgrades your review beyond what bots and generic reviewers can provide.

**Triggers:** "review this PR with real engineers" | "named persona review" | "用真人的哲学审查这个PR"

## Example Output

```
CRITICAL [Torvalds]: Special-case error handling at auth.ts:47.
  "Eliminate the special case and the error disappears entirely."
WARNING [Thompson]: parseConfig() does 3 unrelated things. Split.
NOTE [Jobs]: Error message "EACCES:13" means nothing to users.
Verdict: CONCERNS — fix CRITICAL before merge.
```

## Problem

Generic adversarial review produces generic findings. This grounds each persona in real, searchable philosophy — what Linus Torvalds actually said about good taste, not what an AI thinks a "security auditor" might say.

**Before/after:** `adversarial-reviewer` → "Consider adding error handling here." Named-persona → "Linus would ask: why is this even a special case? Eliminate the special case and the error handling disappears."

**Cost:** 1 round ≈ 8-12 min. Comparable to waiting for CI.

## Rules

- **Search before role-play.** Never impersonate without searching first. Generic = invalid.
- **Each persona MUST find ≥1 issue.** Zero findings = look harder or switch persona.
- **Product persona mandatory every round.** Engineers miss UX. Always include one.
- **Honesty over quantity.** Don't fabricate findings. Clean dimensions get reported clean.

## TL;DR (Quick Start)

**Starter:** Ken Thompson + Linus Torvalds + Steve Jobs. Works today.

```
1. Search "[Name] engineering philosophy" — extract 3-5 criteria from actual quotes
2. Role-play all 3 — MUST find ≥1 issue each
3. Deduplicate — 2+ hits → severity upgrade
4. Output: structured report + post to PR as comment (or save to file)
5. Feynman check: "Would they actually say this?"
```

> **Then read the full process below** (Step 0-3) for the detailed workflow.

## Persona Pools

**Product** (pick 1 per round — mandatory):
| Persona | Known For | Best For |
|---------|-----------|----------|
| Steve Jobs | Design is how it works | UX, onboarding |
| Marty Cagan | Problem not features | PRDs, feature specs |
| Intercom PM | First 30 seconds | Docs, READMEs, quick starts |

**Engineers** (pick 2 per round):
| Persona | Known For | Best For | Blind Spot |
|---------|-----------|----------|------------|
| Ken Thompson | Do one thing well | Architecture, API | UX, documentation |
| Linus Torvalds | Eliminate special cases | Logic, data structures | User empathy, DX |
| John Carmack | Performance as moral craft | Algorithms, critical paths | Simplicity, minimalism |
| Greg Brockman | Find the boundary conditions | Complex systems, integration | Aesthetics, process |
| Kent Beck | Simplicity, feedback, courage | Process, team practices | Performance, security |

**Routing (which personas when):**
- Code correctness → Torvalds + Carmack + Jobs
- Architecture/design → Thompson + Brockman + Cagan
- Documentation/API → Thompson + Beck + Intercom PM
- Performance → Carmack + Torvalds + Jobs
- 1st round on any PR → Torvalds + Thompson + Jobs (broadest coverage)

## The Process

### Step 0: Read Twice
What changed (pass 1). Why + trade-offs (pass 2). Multi-file → trace one end-to-end path.

### Step 1: Search
`"[Name] engineering philosophy code review principles"`. Extract from quotes. Never improvise.

### Step 2: Review (3 independent)
Each gets Mindset (from search), Priorities (3-5 criteria), Finding (≥1 issue with philosopher's reasoning).

### Step 3: Synthesize & Post
Merge duplicates. Cross-persona → severity upgrade. Post report as PR comment (default) or save to `.claude/review-[timestamp].md`.

## Feynman Honesty Check

1. Would [Name] actually say this?
2. Did I cite real philosophy, or write generic advice?
3. All NOTE-level? → You're not really switching perspectives, just narrating the same one in different voices. Switch at least 2 personas and re-review.

## Exit Condition

- **1 round minimum** for any PR
- **BLOCK found** → fix and re-review (1 additional round)
- **CONCERNS found** → fix or accept risk, then 1 more round
- **CLEAN on 2 consecutive rounds** → done
- **CLEAN on round 1** for PRs with low impact → done (1 round is enough)

## When to Use

- You want review quality beyond what automated bots can provide
- Self-authored PR needs pre-submit hardening
- `adversarial-reviewer` findings feel generic
- Reviewing methodologies or docs (product personas excel)
- Auth, data, architecture, public API changes

## When NOT to Use

- Low-impact PR (cosmetic only, no logic changes, no new behavior) → use `adversarial-reviewer`
- Target has active review bots → still usable, but redundant for basic issues
- Throwaway/prototype code
- You have Anthropic Code Review Plugin → use multi-agent audit instead

## Anti-Patterns

Inherits all from `adversarial-reviewer`. Plus:

| Anti-Pattern | Why Wrong |
|-------------|----------|
| "As a senior engineer" without search | Not named. Search first. |
| Same 3 personas every time | Rotate per problem type. Check the Routing table above. |
| Product person skipped | Product catches what engineers miss. |
| Skipping honesty check | Verification without verification = rubber-stamp. |
| 3 rounds for trivial changes | Low-impact PRs: 1 round is enough. |

## Cross-References

- **Extends:** `engineering-team/adversarial-reviewer`
- Related: `engineering-team/code-reviewer`, `engineering-team/senior-security`
- Theory: de Bono "Six Thinking Hats" (1985), Kahneman "Thinking Fast and Slow" (2011)
- Advanced: For personal/strategy tasks with curated persona pools, see `named-persona-pool` methodology (article, forthcoming)

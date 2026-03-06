# Extractable Content Patterns for AI Citation

Templates for content blocks optimized for AI extraction. Each pattern is designed to work as a self-contained passage that AI systems can pull into answers.

---

## Definition Block

For "What is X?" queries. The definition should be complete in one paragraph — AI extracts this verbatim.

```markdown
## What Is [Term]?

[Term] is [concise definition in one sentence]. It [what it does / how it works in one sentence]. Unlike [alternative/predecessor], [term] [key differentiator]. [Term] is used by [who uses it] to [primary benefit].
```

**Target:** 40-60 words. Self-contained. No references to "as mentioned above."

---

## Comparison Block

For "X vs Y" queries. Tables are extracted at much higher rates than prose comparisons.

```markdown
## [X] vs [Y]: Key Differences

| Feature | [X] | [Y] |
|---------|-----|-----|
| [Feature 1] | [X's approach] | [Y's approach] |
| [Feature 2] | [X's approach] | [Y's approach] |
| [Feature 3] | [X's approach] | [Y's approach] |
| **Best for** | [X's ideal user] | [Y's ideal user] |
| **Pricing** | [X's price] | [Y's price] |

**Bottom line:** Choose [X] if [scenario]. Choose [Y] if [scenario].
```

**Critical:** Be balanced and fair. AI systems deprioritize obviously biased comparisons.

---

## Step-by-Step Block

For "How to X" queries. Numbered steps with action verbs.

```markdown
## How to [Action] in [N] Steps

1. **[Action verb] [object]** — [Brief explanation of what and why]. [Specific detail].
2. **[Action verb] [object]** — [Brief explanation]. [Specific detail].
3. **[Action verb] [object]** — [Brief explanation]. [Specific detail].

**Time required:** [estimate]. **Difficulty:** [beginner/intermediate/advanced].
```

**Rules:** Start each step with an action verb. Include specific details (not "do the thing"). Add time/difficulty metadata.

---

## Statistics Block

For authority and citation boost. Statistics with sources are among the highest-cited content types.

```markdown
According to [Source] ([Year]), [specific statistic]. This represents [context — growth, comparison, significance]. [One sentence interpreting what this means for the reader].
```

**Rules:** Always include source name, year, and specific number. Never cite statistics without attribution. Dated statistics beat undated ones.

---

## FAQ Block

For direct question-answer queries. Use the exact question people ask.

```markdown
## Frequently Asked Questions

### [Exact question as people would phrase it]?

[Direct answer in first sentence — no preamble]. [2-3 supporting sentences with specifics]. [Optional: link to deeper content].

### [Next question]?

[Direct answer first]. [Supporting detail].
```

**Rules:** Question must be phrased naturally (how people actually ask, not keyword-stuffed). Answer must start with the direct answer — no "Great question!" or "That depends."

---

## List Block

For "Best X" or "Top X" queries. Structured lists with brief annotations.

```markdown
## [N] Best [Category] for [Use Case] ([Year])

1. **[Option 1]** — [One sentence: what it is + key strength]. Best for [specific scenario].
2. **[Option 2]** — [One sentence: what it is + key strength]. Best for [specific scenario].
3. **[Option 3]** — [One sentence: what it is + key strength]. Best for [specific scenario].
```

**Rules:** Include the year in the heading (recency signal). Each item should be a complete, self-contained recommendation.

---

## Expert Quote Block

For authority boost. Named experts with credentials.

```markdown
"[Quote that adds genuine insight, not marketing fluff]," says [Full Name], [Title] at [Organization]. "[Optional second sentence adding nuance]."
```

**Rules:** Real name, real title, real organization. The quote should add insight that couldn't come from generic content. Avoid promotional quotes.

---

## Pros/Cons Block

For evaluation queries. Honest assessment builds trust with AI systems.

```markdown
## [Subject] Pros and Cons

**Pros:**
- [Specific benefit with context]
- [Specific benefit with context]
- [Specific benefit with context]

**Cons:**
- [Honest limitation with context]
- [Honest limitation with context]

**Verdict:** [Balanced one-line assessment with recommendation for who should/shouldn't use it].
```

**Rules:** Honest cons build more trust than all-positive reviews. AI systems can detect and deprioritize suspiciously one-sided content.

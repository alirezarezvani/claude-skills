# Feynman Comprehension Loop

Use this reference for `feynman` mode. The objective is to expose and repair understanding gaps through retrieval, not to produce childlike wording for its own sake.

## Procedure

1. **Set the target** — name the idea, mechanism, or chapter-level claim to learn.
2. **Read for structure** — identify the central claim, key terms, mechanism, and evidence.
3. **Close the source** — do not look at the text or analysis notes.
4. **Explain from memory** — use plain language and preserve causal or logical links.
5. **Mark uncertainty** — tag every vague phrase, skipped step, undefined term, or appeal to jargon.
6. **Locate the first broken link** — find the earliest point where the explanation stops being justified.
7. **Return narrowly** — reread only the material needed to repair that gap.
8. **Rewrite the explanation** — replace jargon with a mechanism, concrete example, or boundary condition.
9. **Test transfer** — apply the idea to a new case and predict what should happen.
10. **Test contrast** — explain a case where the idea should not apply.
11. **Schedule retrieval** — create short recall prompts for later review.

## Gap Types

- **Definition gap** — a term cannot be explained without repeating itself.
- **Mechanism gap** — steps are listed but causality or logic is missing.
- **Evidence gap** — the claim is remembered but its support is not.
- **Boundary gap** — the learner cannot say when the claim fails.
- **Transfer gap** — the learner repeats the source but cannot use the idea elsewhere.

## Output Template

```markdown
## Learning target
[One precise concept or claim]

## Closed-book explanation
[Plain-language explanation reconstructed from memory]

## Detected gaps
- [Gap type]: [specific missing link]

## Corrected explanation
[Repaired explanation with the missing mechanism or evidence]

## Transfer test
[New scenario and predicted outcome]

## Boundary test
[Scenario where the idea should not apply]

## Recall prompts
1. [Question that retrieves the central mechanism]
2. [Question that retrieves evidence]
3. [Question that retrieves a limitation]
```

## Quality Rules

- Simplicity must not delete an essential condition.
- An analogy must identify where the analogy breaks.
- Reopening the source before attempting retrieval invalidates the gap test.
- Recognition (`this looks familiar`) is not recall (`I can reconstruct it`).
- Review questions should retrieve relationships and mechanisms, not isolated vocabulary.

## Sources

1. Adler, M. J. & Van Doren, C. — *How to Read a Book* (rev. ed., 1972) — the analytical-reading stages this workflow's deep mode follows.
2. Gleick, J. — *Genius: The Life and Science of Richard Feynman* (1992) — primary biographical account of Feynman's learn-by-teaching notebook practice.
3. Farnam Street — "The Feynman Technique: The Best Way to Learn Anything" (fs.blog/feynman-technique) — the canonical four-step formulation used here.
4. Karpicke, J. D. & Roediger, H. L. — "The Critical Importance of Retrieval for Learning", *Science* 319 (2008) — evidence that recall attempts, not re-reading, drive retention.
5. Dunlosky, J. et al. — "Improving Students' Learning With Effective Learning Techniques", *Psychological Science in the Public Interest* 14 (2013) — rates practice testing and self-explanation as highest-utility techniques, re-reading as low-utility.
6. Chi, M. T. H. et al. — "Self-Explanations: How Students Study and Use Examples", *Cognitive Science* 13 (1989) — the self-explanation effect behind the teach-back step.

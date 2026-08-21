# Progressive Disclosure and Token Budgets

Every number in this skill's Step 7–9 budget tables traces to a specific failure mode. This
document says where each came from and what breaks when it is exceeded.

---

## 1. The three-tier disclosure model

Agent Skills are built on progressive disclosure: the agent sees a little, and pulls more only
when it needs to. Anthropic's Agent Skills documentation describes three levels:

| Level | What loads | When | Practical budget |
|-------|-----------|------|------------------|
| 1 | `name` + `description` from frontmatter | Always, for every installed skill | ~100 tokens |
| 2 | The `SKILL.md` body | When the skill is triggered | < 5k tokens |
| 3 | Bundled files — references, chapters, scripts | When the body points at them | Unbounded, on demand |

A compiled book skill maps onto this exactly: description → level 1, master `SKILL.md` → level
2, `chapters/` + glossary + patterns + cheatsheet → level 3. The whole design of the converter
is an attempt to put as little as possible in level 2 while keeping level 3 *findable* — which
is what the topic index is for.

Jakob Nielsen's original formulation of progressive disclosure (Nielsen Norman Group, 2006)
carries the warning that applies here: disclosure only works when the first tier makes the
second tier's existence and value obvious. A chapter file nothing links to is not progressive
disclosure — it is a file that will never be read.

---

## 2. Why SKILL.md is capped at 4,000 tokens

Two independent reasons, and the second is the one that actually bites.

**Residency.** The master file is loaded whenever the skill triggers. It is paid for on every
session that touches this knowledge base, whether or not the user asks a question the file
answers. Anthropic's skill-authoring guidance puts the practical ceiling around 5k tokens; the
converter budgets 4k and leaves headroom.

**Truncation direction.** Context compaction and hard truncation drop content from the *end* of
a document. In a compiled skill the end of `SKILL.md` is the Chapter Index and the Topic Index
— the navigation the entire architecture depends on. Overflow does not degrade the skill
gracefully; it removes exactly the part that makes chapter files reachable, leaving a resident
core that looks fine and can no longer route. That asymmetry is why `budget.over_cap` on
`SKILL.md` is the validator's only hard budget error, and why Step 9 says "most important
content first."

---

## 3. Why chapters live in separate files

Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (*TACL*, 2024), showed
that retrieval accuracy over a long context follows a U-curve: models attend well to the
beginning and the end of their context and measurably worse to the middle. Performance on
multi-document QA degraded as relevant information moved toward the centre.

The implication for this converter is direct. A single 40k-token file containing all chapters
puts most chapters in the sag of that curve. Twenty-eight separate files, one loaded at a time,
put the relevant chapter alone at the front of a short context. The gain is not only cost — it
is accuracy.

Anthropic's context-engineering guidance frames the same point as treating context as a finite
resource with diminishing returns: more retrieved text is not monotonically better, because
irrelevant content competes for attention with relevant content. "Load the whole book, it fits"
is a real option in a long-context model and still the wrong one.

---

## 4. The per-chapter matrix

|  | `reference` | `study` |
|---|---|---|
| `text` | 800–1,200 | 1,000–1,800 |
| `technical` | 1,200–1,800 | 2,000–3,000 |

The floor comes from what the chapter template naturally produces. Core Idea, Frameworks,
Key Concepts, Mental Models, Anti-patterns, Takeaways and Connects To on a dense prose chapter
land around 700–900 tokens without padding. Anything below that means the chapter had little
extractable structure — which is worth saying in the Core Idea rather than hiding with filler.

The technical rows are wider because code and tables do not compress. A reproduced parameter
table is 300 tokens whether or not the chapter is important, and truncating a code example to
fit a budget produces something worse than omitting it.

The `study` column is wider only because it must contain the **worked example**. That is the
honest way to spend the extra budget: reproduce the artifact the author walks through, compactly
and in your own reconstruction. Everything else — longer prose, more adjectives, restated
takeaways — is padding, and padding costs tokens on every load while adding nothing retrievable.
This is the converter's third quality rule (density over completeness) expressed as a number.

The 3,500-token chapter ceiling in the validator is a runaway detector, not a target: at that
size a single chapter costs as much to load as the entire resident core, which usually means
the source chapter should have been split.

---

## 5. Supporting-file budgets

| File | Cap | Why that number |
|------|-----|-----------------|
| `glossary.md` | 1,500 | ~100–150 terms at one line each. Past that it is a dictionary of the source's whole vocabulary rather than its significant terms, and the signal drops. |
| `patterns.md` | 2,000 | ~15–25 patterns with when/how/trade-offs. Sources with more than that usually want the patterns distributed into chapters. |
| `cheatsheet.md` | 1,200 | One printed page. The constraint is the point: it forces ranking, and a cheatsheet you cannot see at once is not a cheatsheet. |

These three are warnings rather than errors in the validator. They are loaded on demand, so
overflow costs a heavier read but never silently breaks navigation the way `SKILL.md` overflow
does.

---

## 6. The description is a routing decision, not a summary

Level 1 is the only thing the agent sees when deciding whether this skill is relevant at all.
Anthropic's best-practice guidance is specific: write in the third person, state what the skill
does, and state explicitly *when to use it* with the concrete triggers a user would say. The
1,024-character limit is a hard field limit, not a style guideline.

For a compiled book skill the generated description must name the **source and its topics**,
not just the title. "Knowledge base from *Thinking in Systems* by Donella Meadows" does not
help an agent decide whether to load it when the user asks about feedback loops. Naming three
to six key topics is what turns the description into a router.

---

## 7. Budget-check discipline

Estimate with `token_budget_estimator.py`, which uses the same words/0.75 heuristic as the
extractor so every number in the pipeline agrees. It is deliberately not a BPE count: a stable,
comparable estimate that never varies with an optional dependency is more useful for a budget
gate than an exact number that requires `tiktoken` to be installed. Expect it to run roughly
10–20% off a true `cl100k` count on English prose, and further off on code and CJK.

Run it twice: pre-flight on `full_text.txt` to decide whether conversion is worth it at all,
and post-flight on the generated folder to catch overflow before anyone loads the skill.

---

## Sources

1. Anthropic. "Agent Skills." *Claude Docs*, code.claude.com/docs/en/skills. (Three-level
   progressive disclosure; SKILL.md size guidance.)
2. Anthropic. "Agent Skills best practices." *Claude Platform Docs*,
   platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices. (Description
   field rules; third person; explicit triggers.)
3. Nielsen, J. "Progressive Disclosure." Nielsen Norman Group, 2006. (The first tier must make
   the second tier's value obvious.)
4. Liu, N. F. et al. "Lost in the Middle: How Language Models Use Long Contexts."
   *Transactions of the ACL*, 2024. (U-shaped positional accuracy over long contexts.)
5. Anthropic. "Effective context engineering for AI agents." Anthropic Engineering Blog, 2025.
   (Context as a finite resource; retrieval over preloading.)
6. Agent Skills open standard, github.com/agentskills/agentskills. (`name` + `description` as
   the only universally required frontmatter fields.)
7. Sweller, J., Ayres, P. & Kalyuga, S. *Cognitive Load Theory*. Springer, 2011. (Extraneous
   load: irrelevant material degrades processing of relevant material — the human analogue of
   the lost-in-the-middle result.)

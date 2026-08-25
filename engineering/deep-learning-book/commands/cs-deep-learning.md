---
name: "cs-deep-learning"
description: "/cs:deep-learning — Study companion for the Deep Learning textbook (Goodfellow, Bengio & Courville, 2016). Answers chapter questions from a compiled knowledge base, always dating the answer against 2026 practice, and routes to the reading-path planner or the training diagnostic. Points at the free official chapters; never reproduces them."
argument-hint: "[a topic, a chapter number, a question about the book, or 'where do I start']"
---

# /cs:deep-learning — Navigate the book, and date its advice

**Command:** `/cs:deep-learning [topic | chNN | question]`

The book is free to read at [deeplearningbook.org](https://www.deeplearningbook.org/). This
command navigates it and keeps it current; it does not replace it.

## When to run

- "What does the book say about regularization / saddle points / the partition function?"
- "Is Chapter 10's advice on LSTMs still right?"
- "Explain the ELBO the way Chapter 19 sets it up"
- "Where should I start?" (routes to `/cs:dl-reading-path`)
- "Why is my training run doing this?" (routes to `/cs:dl-diagnose`)

## When NOT to run

- Production ML engineering → `engineering-team/senior-ml-engineer`
- LLM cost and serving → `engineering/llm-cost-optimizer`
- RLHF, agents, prompting, MLOps → outside the book entirely; this command will say so

## Procedure

1. **Load** `engineering/deep-learning-book/skills/deep-learning-book/SKILL.md`.
2. **Resolve** the request through the Topic Index to one or more chapters.
3. **Read** those chapter files before answering. The index is navigation, not content.
4. **Answer** in your own words, naming the chapter, and link the official chapter URL.
5. **Date it.** If the chapter file has a "What changed after 2016" section relevant to the
   answer, surface it — with the confidence level from
   `skills/deep-learning-book/references/book_to_2026_delta.md`. Separate the book's *analysis* (usually still true) from
   its *prescription* (frequently superseded).
6. **Name the boundary.** If the question is outside the twenty chapters, say so and route.

## The four things this command will not do

- Reproduce the book's text, figures, or a paragraph-by-paragraph paraphrase.
- Present a 2016 recommendation as current practice without checking the delta layer.
- Answer from the index without reading the chapter file.
- Improvise the book's position on material published after it.

## Output shape

```
Chapter(s): ch07 (Regularization), ch05 (capacity)
Answer    : <original explanation, naming the framework>
Still true: <holds / analysis holds but recommendation superseded / historical> + why
Read it   : https://www.deeplearningbook.org/contents/regularization.html
Next      : <the tool, worksheet, or chapter that follows>
```

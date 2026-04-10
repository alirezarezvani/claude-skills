---
name: wiki-query
description: Query the LLM Wiki — reads index.md first, drills into 3-10 relevant pages, synthesizes an answer with inline [[wikilink]] citations, and offers to file the answer back as a new comparison or synthesis page. Usage /wiki-query "<question>"
---

# /wiki-query

Ask the wiki a question. The librarian reads `index.md` first, picks relevant pages across categories, synthesizes an answer with citations, and offers to file the answer back into the wiki so your explorations compound.

## Usage

```
/wiki-query "<your question>"
/wiki-query "what does the wiki say about sparse autoencoders?"
/wiki-query "compare monosemanticity and polysemanticity across my sources"
/wiki-query "which sources disagree on scaling laws?"
/wiki-query "give me a comparison table of SAE vs linear probing"
```

## What happens

1. **Index-first read** — reads `wiki/index.md` to find relevant pages
2. **Drill-in** — reads 3-10 pages in full (synthesis + concepts + sources + entities)
3. **Follow links** — opportunistically follows wikilinks between pages
4. **Fallback search** — if the index isn't enough, runs `scripts/wiki_search.py` (BM25)
5. **Synthesize** — composes a direct answer + supporting detail + inline `[[sources/xxx]]` citations + "Related pages" section
6. **Offer to file back** — asks whether to save this as a new wiki page (usually in `comparisons/` or `synthesis/`)

## Output formats

The answer's format follows the question:

| Question shape | Output |
|---|---|
| "What is X?" | Markdown explanation with citations |
| "A vs B" | Comparison table |
| "Give me a slide deck on X" | Markdown synthesis → `/wiki-marp` to render |
| "Chart the trend in X" | Python script + saved chart in `wiki/assets/charts/` |

## Sub-agent

This command dispatches the `wiki-librarian` sub-agent. See `agents/wiki-librarian.md`.

## Scripts

- `engineering/llm-wiki/scripts/wiki_search.py` — BM25 fallback search
- `engineering/llm-wiki/scripts/append_log.py` — log filed answers

## Rules

- **Read the index first.** No grep-everything.
- **Every claim cites a page** with a `[[wikilink]]`.
- **Offer to file the answer back** — but only for substantive answers worth keeping.

## Skill Reference

→ `engineering/llm-wiki/SKILL.md`
→ `engineering/llm-wiki/references/query-workflow.md`

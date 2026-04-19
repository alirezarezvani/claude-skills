# llm-wiki

> **A second brain for Claude Code + Obsidian.**
> Inspired by [Andrej Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Turn any LLM CLI into a disciplined wiki maintainer. You curate sources and ask questions. The LLM reads, files, cross-references, flags contradictions, and keeps a living synthesis current. Knowledge **compounds** instead of being re-derived by RAG on every query.

## The idea in one paragraph

Most LLM+docs workflows are RAG: retrieve fragments at query time, synthesize from scratch, forget. The wiki is **compounding**. The LLM reads each source once and integrates it into a persistent, interlinked Obsidian vault — updating entity pages, revising concept pages, flagging contradictions, and strengthening the synthesis. The wiki is the compiled artifact; RAG is the just-in-time retrieval. This plugin gives the LLM the discipline (SKILL.md), the delegation (sub-agents), the triggers (slash commands), and the bookkeeping (Python tools) to do the job.

## What's in the box

| Piece | What it does |
|---|---|
| **SKILL.md** | Master skill doc — architecture, workflows, iron rules, cross-tool compat. Has `context: fork` so other skills can chain into it. |
| **3 sub-agents** | `wiki-ingestor`, `wiki-librarian`, `wiki-linter` |
| **5 slash commands** | `/wiki-init`, `/wiki-ingest`, `/wiki-query`, `/wiki-lint`, `/wiki-log` |
| **8 Python tools** | Standard library only: `init_vault`, `ingest_source`, `update_index`, `append_log`, `wiki_search` (BM25), `lint_wiki`, `graph_analyzer`, `export_marp` |
| **8 reference docs** | Schema, page formats, ingest/query/lint workflows, Obsidian setup, cross-tool setup, Memex principles |
| **Vault templates** | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `index.md`, `log.md`, plus 5 page templates (entity, concept, source, comparison, synthesis) |
| **Example vault** | A small worked example on "LLM interpretability" |

## Quick start

```bash
# 1. Initialize a vault
python scripts/init_vault.py --path ~/vaults/research --topic "LLM interpretability" --tool all

# 2. Open in Obsidian
open -a Obsidian ~/vaults/research

# 3. Drop a source into raw/ and ingest
cp ~/Downloads/paper.pdf ~/vaults/research/raw/papers/
cd ~/vaults/research
# in Claude Code:
> /wiki-ingest raw/papers/paper.pdf

# 4. Ask questions
> /wiki-query "what does the paper say about sparse features?"

# 5. Health check
> /wiki-lint
```

## Cross-tool compatibility

The scripts are pure Python stdlib — they run anywhere. Only the **schema loader** changes per tool:

| Tool | Loader file |
|---|---|
| Claude Code | `CLAUDE.md` |
| Codex CLI (OpenAI) | `AGENTS.md` |
| Cursor (modern) | `AGENTS.md` |
| Cursor (legacy) | `.cursorrules` |
| Antigravity (Google) | `AGENTS.md` |
| OpenCode / Pi | `AGENTS.md` |
| Gemini CLI | `AGENTS.md` |

`init_vault.py --tool all` installs all three. You can run multiple CLIs against the same vault.

See `references/cross-tool-setup.md` for per-tool instructions.

## Architecture

```
<vault>/
├── raw/                    # IMMUTABLE sources (you own)
├── wiki/                   # LLM-owned knowledge base
│   ├── index.md            # content catalog
│   ├── log.md              # append-only timeline
│   ├── entities/           # people, orgs, places, products
│   ├── concepts/           # ideas, theories, frameworks
│   ├── sources/            # one summary per ingested source
│   ├── comparisons/        # cross-source analyses
│   └── synthesis/          # high-level overviews and theses
├── CLAUDE.md               # schema for Claude Code
├── AGENTS.md               # schema for Codex/Cursor/Antigravity
└── .cursorrules            # (optional) legacy Cursor
```

**Iron rule:** The LLM never edits `raw/`. All writes go to `wiki/`.

## Three operations

- **Ingest** — Read a source, discuss with user, write summary page, update 5-15 cross-referenced pages, update index, log it
- **Query** — Read index first, drill into 3-10 pages, synthesize answer with inline citations, offer to file back as a new page
- **Lint** — Mechanical + semantic health check; surface contradictions, orphans, stale claims, cross-reference gaps

## Why not just RAG?

| Plain RAG | LLM Wiki |
|---|---|
| Rediscover knowledge each query | Knowledge accumulates |
| Cross-references re-computed every time | Cross-references pre-written and maintained |
| Contradictions surface only if you ask | Contradictions flagged during ingest |
| Exploration disappears into chat history | Good answers re-filed as new pages |
| Scales by embeddings infrastructure | Scales by markdown + `index.md` + optional local search |

The wiki and RAG aren't opposites — RAG can sit on top of the wiki once you outgrow index-first search.

## Status

**v1.0.0** — initial release. SKILL + 3 agents + 5 commands + 8 scripts + 8 references + full vault templates + example vault.

## License

MIT.

## Related

- [Karpathy's original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the pattern this plugin implements
- Vannevar Bush, "As We May Think" (1945) — the Memex
- [qmd](https://github.com/tobi/qmd) — local hybrid search over markdown (pair with this when the wiki outgrows `index.md`)

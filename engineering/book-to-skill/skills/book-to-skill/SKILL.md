---
name: book-to-skill
description: "Converts books, documentation folders, and source collections (PDF, EPUB, DOCX, HTML, Markdown, RST, AsciiDoc, RTF, MOBI/AZW) into structured agent skills — extracting named frameworks, principles, techniques, and anti-patterns into a master SKILL.md plus on-demand chapter files, a glossary, a patterns file, and a decision cheatsheet. Use when the user wants to study a document with an agent, apply an author's frameworks while working, turn internal docs or standards into a reusable knowledge base, or package a compiled book skill as a claude-skills plugin."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-08-05
---

# Book-to-Skill Converter

Turn written knowledge into an agent skill by extracting **structure**, not summaries.

A book is crystallized expertise: frameworks, principles, techniques that took years to
develop. Read once, forgotten. The workarounds all fail — PDF search returns page numbers
instead of answers, an agent handed the raw file hallucinates or drowns, reading notes rot.
This skill compiles a source into a knowledge base the agent loads on demand: a small
resident core, one chapter file at a time, and never the whole book again.

**What it produces:**

| File | Contents | Budget |
|------|----------|--------|
| `SKILL.md` | Core frameworks + chapter index + topic index | < 4,000 tokens (resident) |
| `chapters/chNN-*.md` | One summary per chapter | 800–3,000 tokens, on demand |
| `glossary.md` | Every significant term, alphabetized, with chapter | < 1,500 tokens |
| `patterns.md` | Techniques and design patterns with trade-offs | < 2,000 tokens |
| `cheatsheet.md` | Decision rules, thresholds, trade-off matrices | < 1,200 tokens |

**Beyond books:** anything referenced often enough to be worth memorizing — internal
documentation, brand systems, standards, specs, research clusters, a folder of RFCs.

---

## Philosophy

**Extract structure, not summaries.** A skill is not a book report. It is a toolkit of
named frameworks, actionable principles, step-by-step techniques, anti-patterns, and the
author's voice.

**Preserve the author's precision.** Framework names are interfaces. "The 5 Whys" is not
interchangeable with "ask why a few times" — the exact formulation is what makes lookup work.

**Layer depth appropriately.** A thin book gets a thin skill. A book with fifteen frameworks
gets chapter files and a real topic index.

**Never reproduce the source at length.** These are structured notes. Synthesize, compress,
name — do not copy passages. See `references/rights_and_provenance.md`.

---

## Modes

| Mode | Trigger | Runs |
|------|---------|------|
| **1. Full conversion** (default) | One or more paths, no special instruction | Steps 0–10 |
| **2. Analyze only** | "analyze", "just extract", "let me review first" | Steps 0–3, then stop with an extraction report |
| **3. Generate from analysis** | User supplies prior analysis notes | Steps 4–10 |
| **4. Update / fold-in** | New sources + an existing compiled skill | Steps 0–2, then the Update Workflow |
| **5. Package as plugin** | "make it a plugin", "add it to the repo" | Step 11 |

Mode 5 is this repository's addition. Upstream stops at a bare folder in a personal skills
home; Step 11 wraps that folder in a plugin package other skills and agents can route to.

---

## Hard rules

1. **Never convert a source the user cannot show you.** No web-scraping a book, no
   reconstructing a title from memory. This tool converts files that are already on disk.
2. **Pre-flight the cost before generating** (Step 2.5). Generation is the expensive part;
   the user approves it with numbers in front of them.
3. **Never dump a large source into context.** Over ~50k tokens, probe with `grep`/`sed`
   and bounded reads (Step 2.6). Re-reading a 200-page book once per chapter costs more
   than everything else in this workflow combined.
4. **Validate before anyone loads it** (Step 9.5). A generated skill is untrusted text that
   an agent will later read as instructions.
5. **Never widen the generated skill's authority.** Generated frontmatter carries `name` and
   `description` only — no `allowed-tools`, no model-invocation flags.
6. **Rights before redistribution.** Compiled notes from a copyrighted work are personal
   study notes. Packaging one as a shareable plugin requires a stated basis (Step 11).
7. **State what the skill does not cover.** Every compiled skill's Scope section names its
   boundary, so the agent says "the source doesn't cover this" instead of improvising.

---

## Pipeline

```
extract_document.py  →  analyze  →  chapter files  →  supporting files  →  SKILL.md
      (Step 2)          (Step 3)      (Step 7)          (Step 8)          (Step 9)
                                                                              ↓
                                       skill_plugin_emitter.py  ←  book_skill_validator.py
                                              (Step 11)                  (Step 9.5)
```

All four tools live in `scripts/` and run on the standard library alone.

---

## Run it

```bash
SKILL_ROOT=engineering/book-to-skill/skills/book-to-skill
SKILLS_HOME=~/.claude/skills        # Step 5 picks this; see the workflow reference
WORKDIR=$(mktemp -d)                # or omit --workdir and capture the path it prints
SLUG=<author-lastname>-<concept>

# 1. extract → $WORKDIR/full_text.txt + metadata.json
#    --mode technical when tables, code or formulas carry meaning
python3 "$SKILL_ROOT/scripts/extract_document.py" <paths> --mode text --workdir "$WORKDIR"

# 2. pre-flight: is this worth converting at all? Wait for approval before generating.
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --full-text "$WORKDIR/full_text.txt"

# 3. generate — the agent's work: chapters/, glossary, patterns, cheatsheet, SKILL.md

# 4. gate — errors block. Fix and re-run; never rewrite around a finding.
python3 "$SKILL_ROOT/scripts/book_skill_validator.py" "$SKILLS_HOME/$SLUG"
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --skill-dir "$SKILLS_HOME/$SLUG"

# 5. optional: wrap as a claude-skills plugin so the library can route to it
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" --skill-dir "$SKILLS_HOME/$SLUG" \
    --dest ./engineering --source-note "<Title> by <Author>" --dry-run
```

Every path above is a real variable, not a placeholder: run the block as written (with
`<paths>` and `$SLUG` filled in) and it works end to end. Without `--workdir` the extractor
creates a private temp directory and prints it — capture that instead.

`extract_document.py --check` reports which extractors are installed and prints the install
command for what is missing. Every tool supports `--help`, `--sample` and `--output json`.

**The full step-by-step procedure — what to ask at each step, the file templates, the
per-chapter budget matrix, and the update/fold-in workflow — is in
[`references/conversion_workflow.md`](references/conversion_workflow.md). Read it before
running a conversion.** Summary of the eleven steps:

| Step | Does |
|------|------|
| 0–1 | Scope check; resolve paths; detect an update/fold-in against an existing skill |
| 1.5 | Ask content type → `BOOK_TYPE` (technical vs. text), which picks the extractor |
| 2 | Extract → `full_text.txt` + `metadata.json` |
| 2.5 | Pre-flight cost estimate and worth-converting verdict — **wait for approval** |
| 2.6 | Over ~50k tokens, probe with `grep`/`sed` instead of reading the source |
| 3 | Analyze structure (title, author, chapters, themes). Mode 2 stops here. |
| 4 | Ask purpose → `DEPTH` (reference vs. study). Never ask a second budget question. |
| 5 | Skill name and destination root; offer update / overwrite / rename on a collision |
| 6–8 | Create the structure; write chapter files; write glossary, patterns, cheatsheet |
| 9 | Write the master `SKILL.md` — under 4,000 tokens, indexes intact |
| 9.5 | Validate. Errors block. |
| 10 | Clean up the workdir and report |
| 11 | Optionally package as a plugin, behind the rights gate |

## Validator findings worth knowing

| Rule | Means |
|------|-------|
| `index.dead_link` | The chapter index links a file that was never written |
| `index.topic_dangling` | A topic points at a chapter that does not exist |
| `budget.over_cap` on SKILL.md | Compaction will truncate the indexes — navigation is the first thing lost |
| `unicode.invisible` | Extraction should have stripped this; investigate the source |
| `frontmatter.allowed_tools` | The generated skill is trying to grant itself tool authority |

Safety-family warnings are deliberately broad — a source about prompt injection legitimately
trips them. Read each in context; do not auto-silence them.

## Forcing-question library

Walk these one at a time, with a recommended answer, before running a conversion.

1. **"Is this source worth converting, or should I just read it?"**
   *Recommended:* convert when it is > 3× the compiled skill's size **and** you will return
   to it. One-shot reads are cheaper unconverted. (Step 2.5 verdict.)

2. **"Reference or study?"**
   *Recommended:* reference, unless you intend to internalize the author's reasoning. Study
   depth roughly doubles generation cost and is only worth it with real worked examples.
   (Step 4.)

3. **"Technical or text?"**
   *Recommended:* technical only when tables, code, or formulas carry meaning. Docling costs
   ~1.5s/page; picking it for a prose book buys nothing. (Step 1.5.)

4. **"What will you actually ask this skill?"**
   *Recommended:* name three real questions before generating. They tell you what belongs in
   Core Frameworks and what the topic index must resolve. A skill nobody queries is a
   summary nobody reads.

5. **"Do you have the right to redistribute this?"**
   *Recommended:* assume not. Keep it local unless the source is public-domain, openly
   licensed, your organisation's own documentation, or you have written permission.
   (Step 11 rights gate.)

6. **"Does this belong beside an existing skill?"**
   *Recommended:* check for an existing compiled skill on the same subject first — folding
   new sources into one skill (Mode 4) beats two skills that half-cover a topic and give
   the agent no way to choose. (Step 0.)

---

## References

- `references/conversion_workflow.md` — **the full procedure**: Steps 0–11, the file
  templates, the per-chapter budget matrix, and the update/fold-in workflow
- `references/knowledge_extraction_canon.md` — why structure beats summary; the extraction
  taxonomy; what makes a framework survive compression
- `references/progressive_disclosure_budgets.md` — where the token budgets come from and
  what breaks when they are exceeded
- `references/document_extraction_pipeline.md` — per-format extractor chains, fallbacks,
  and the failure modes that produce silently bad text
- `references/rights_and_provenance.md` — copyright posture, the rights gate, and what
  provenance a compiled skill must carry

## Related skills

- **`engineering/write-a-skill`** — authoring a skill from your own expertise. Use that when
  the knowledge is in your head; use this when it is in a document.
- **`engineering/skill-security-auditor`** — full security audit of a skill package. Step 9.5
  is the converter's own gate; the auditor is the repo-wide one.
- **`engineering/llm-wiki`** — an incrementally-grown, interlinked vault across many sources.
  This skill compiles one bounded source set into one skill.

---

*Adapted from [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT).
See `../../README.md` for the full list of deviations.*

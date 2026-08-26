# Conversion Workflow — Steps 0 through 11

The full step-by-step procedure. `SKILL.md` carries the shape, the hard rules and the
commands; this file carries the detail: what to ask at each step, the exact templates, the
per-chapter budget matrix, and the update/fold-in procedure.

Read it when running a conversion. `$SKILL_ROOT` below is this skill's folder
(`engineering/book-to-skill/skills/book-to-skill`); `$SKILLS_HOME` is the destination
skill root chosen in Step 5. File templates also ship under `assets/`:
`chapter_template.md`, `master_skill_template.md`, `cheatsheet_template.md`. Modes 2 (analyze only) and 3 (generate from prior
analysis) skip steps as noted in `SKILL.md`.

---

## Step 0 — Scope check

With no arguments, stop and say:

> `book-to-skill <path-to-document-folder-or-glob>... [skill-name-slug]`

Then parse the invocation:
- Every argument that is an existing file, folder, or matching glob → `INPUT_PATHS`.
- A trailing argument that matches no path and looks like a slug (lowercase, hyphens) →
  `SKILL_NAME`.
- Any input path that is itself a compiled skill (has `SKILL.md` **and** `chapters/`), or a
  `SKILL_NAME` that already exists in `SKILLS_HOME` → **Mode 4**.

---

## Step 1 — Validate input

At least one supported file must resolve: `.pdf .epub .docx .txt .md .markdown .rst .adoc
.html .htm .rtf .mobi .azw .azw3`. Expand folders and globs. Nothing supported → stop with
a clear error naming what was searched.

---

## Step 1.5 — Content type

Ask once:

> What kind of content is this?
> 1. **Technical** — code blocks, tables, formulas, diagrams
> 2. **Text-heavy** — mostly prose
> 3. **Not sure** — I'll use the fast path and warn you if quality looks thin

Option 1 → `BOOK_TYPE=technical`; options 2 and 3 → `BOOK_TYPE=text`.

Technical mode uses Docling for layout-aware extraction where installed (~1.5s/page —
say so before starting a long run). Text mode uses the fastest suitable extractor per format.

---

## Step 2 — Extract

```bash
SKILL_ROOT="<this skill folder>"
python3 "$SKILL_ROOT/scripts/extract_document.py" $INPUT_PATHS --mode "$BOOK_TYPE"
```

Writes to a **fresh private working directory** (0700, owner-only artifacts) whose path
the tool prints on completion and stores in `metadata.json` as `output_text`. Capture it:

```bash
WORKDIR=$(dirname "$(python3 "$SKILL_ROOT/scripts/extract_document.py" $INPUT_PATHS \
    --mode "$BOOK_TYPE" | awk '/Text ->/ {print $3}')")
```

Pass `--workdir` (or set `BOOK_SKILL_WORKDIR`) when you want a stable location instead;
an explicit path is symlink-checked and mode-restricted before anything is written.
The directory contains:
- `full_text.txt` — combined text, per-source banners, invisible Unicode stripped
- `metadata.json` — sizes, token estimate, chapters detected, ToC present

Useful flags: `--check` reports which extractors are installed and prints the install command
for what is missing; `--workdir` relocates the output; `--output json` prints the metadata.

Nothing is installed unless you pass `--install-missing yes`. Every format degrades to a
stdlib parser except MOBI/AZW/AZW3, which need Calibre's `ebook-convert` on PATH.

---

## Step 2.5 — Pre-flight cost estimate

```bash
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" \
    --full-text "$WORKDIR/full_text.txt"
```

Present the estimate and **wait for approval**:

```
📖 Sources: <N>  |  Pages ~<N>  |  Words ~<N>  |  Tokens ~<N>K
💰 Input (reading + prompts) ~<N>K   Output (generated files) ~<N>K
   Cost: multiply by your model's current per-1M input/output rates — quote today's
   rate and label it an estimate. Never hardcode a price.
⏱  Estimated time: ~<N> minutes
➡  Proceed? (or say "analyze only" to preview first)
```

Estimating: input ≈ `estimated_tokens` × 1.3; output ≈ chapters × per-chapter budget +
4,000 (SKILL.md) + 4,500 (glossary + patterns + cheatsheet). Per-chapter midpoint: `text`
≈ 1,000, `technical` ≈ 1,800 — the Step 7 matrix refines it once `DEPTH` is known.

The estimator prints a **verdict**. If the source is smaller than ~3× the compiled skill,
say so and recommend handing the agent the document instead. Converting a 20-page memo is
strictly worse than reading it.

---

## Step 2.6 — Large sources (> 50k tokens)

Treat `full_text.txt` as a queryable corpus, not a single read.

```bash
wc -w "$FULL_TEXT"                                          # size before any read
grep -n -E "^\s*(Chapter|CHAPTER)\s+[0-9]+" "$FULL_TEXT"    # chapter offsets
sed -n '<start>,<end>p' "$FULL_TEXT"                        # pull one chapter
grep -c -i "westrum\|dora" "$FULL_TEXT"                     # verify before claiming
```

Prefer `Read(offset=…, limit=…)` over an unbounded read. A 200-page book is ~75k tokens;
re-reading it once per chapter across 28 chapters costs ~2M input tokens. Under 50k tokens,
a single read is fine.

---

## Step 3 — Analyze structure

Read the first ~8,000 characters to identify title, author(s), chapter structure, core themes,
and domain. Read the ToC block if present to map every chapter.

**Mode 2 stops here** with an extraction report:

```
## Extraction Report — <Title>
### Author's Core Frameworks     - **<Name>**: what it is, when to apply
### Key Principles               - <Principle>: actionable rule
### Techniques & Methods         - <Technique>: steps
### Anti-patterns                - <What to avoid>: why it fails
### Suggested Skill Name         `{author-lastname}-{core-concept}`
### Chapters Detected            | # | Title | Main Frameworks |
```

---

## Step 4 — Purpose (full conversion only)

> What should this skill help you do?
> 1. Apply the author's frameworks while working
> 2. Think with the author's mental models
> 3. Reference specific chapters and concepts
> 4. All of the above

Derive `DEPTH` — do **not** ask a second question:
- Only 3 → `DEPTH=reference` (lean, fast-lookup chapters)
- Includes 1, 2, or 4 → `DEPTH=study` (worked examples and reasoning)

Modes 2 and 3 skip this step: default `DEPTH=study`.

---

## Step 5 — Name and destination

If `SKILL_NAME` was given, use it. Otherwise offer two and let the user pick:
- **author-concept**: `{author-lastname}-{core-concept}` — `cialdini-influence`
- **title**: `designing-data-intensive-apps`

Prefer author-concept when the source has a strong methodological identity.

Choose `SKILLS_HOME`:

| Host | Personal root (probe in order) | Project-local |
|------|-------------------------------|---------------|
| **Claude Code** | `~/.claude/skills` | `.claude/skills` |
| **GitHub Copilot CLI** | `~/.copilot/skills` → `~/.agents/skills` | `.github/skills` → `.agents/skills` |
| **Amp** | `~/.agents/skills` → `~/.config/agents/skills` | `.agents/skills` |

Exactly one candidate exists → use it. None exist → ask which to create; never silently pick.
Heading for a repo plugin (Step 11) → generate into a temp folder and let the emitter place it.

If `$SKILLS_HOME/<slug>/` already exists, offer: **update** (Mode 4), **overwrite**, or
**rename**.

---

## Step 6 — Create the structure

```bash
mkdir -p "$SKILLS_HOME/<slug>/chapters"
```

---

## Step 7 — Chapter summaries

**Per-chapter budget** — scales with type and depth:

| | `DEPTH=reference` | `DEPTH=study` |
|---|---|---|
| `BOOK_TYPE=text` | 800–1,200 tokens | 1,000–1,800 tokens |
| `BOOK_TYPE=technical` | 1,200–1,800 tokens | 2,000–3,000 tokens |

Targets, not caps. A dense chapter runs over; a thin one runs under. Density beats length —
never pad to hit a number. Chapters load on demand, so a bigger chapter only costs when read.

**`DEPTH=study` is earned with content, not a bigger number.** The template below lands a
dense prose chapter around 700–900 tokens on its own. To reach study depth honestly, add:
- **One worked example or artifact** under `## Worked Example` — the sample document, the
  dialogue, the filled-in template, the decision walked end to end. This is the single
  biggest lever and the main thing a learner returns for.
- **Expanded "How"** for each framework — explicit steps or criteria, not a one-liner.
- **A "why it works / failure mode" note** on the top one or two frameworks.

A chapter with no worked example lands below the floor and says so in its Core Idea. Padding
is worse than a short chapter.

Write `chapters/ch<NN>-<slug>.md`:

```markdown
# Chapter N: <Full Title>

## Core Idea
<1–2 sentences: the single most important thing this chapter teaches>

## Frameworks Introduced
- **<Framework Name>**: <exact formulation — the author's naming>
  - When to use: <specific situation>
  - How: <steps or criteria>

## Key Concepts
- **<Term>**: <precise one-sentence definition>          (5–10 terms)

## Mental Models
<2–4 thinking tools, written as "Use X when Y" or "Think of X as Y">

## Anti-patterns
- **<What to avoid>**: <why it fails>

## Code Examples          *(technical only — omit for text)*
## Reference Tables       *(technical only — reproduce comparison/decision tables)*
## Worked Example         *(DEPTH=study only — reconstruct compactly, never copy at length)*

## Key Takeaways
1. <Actionable insight>                                   (3–7 items)

## Connects To
- **Ch N**: <why it relates>
- **<Concept>**: <external standard or idea it connects with>
```

Emphasis by type: `technical` prioritizes Code Examples, Reference Tables, and exact syntax;
`text` prioritizes Frameworks, Mental Models, and Key Takeaways, omitting empty sections.

---

## Step 8 — Supporting files

**`glossary.md`** — every significant term, alphabetically sorted, `**Term** — definition (Ch N)`.

**`patterns.md`** — every concrete technique, algorithm, or design pattern:
`## Pattern Name` / `**When to use**` / `**How**` / `**Trade-offs**`.

**`cheatsheet.md`** — the most differentiated layer. Anyone can grep a glossary for a term;
the cheatsheet captures the author's *judgment*. Prioritize in order:

1. **Decision rules** — "When X, do Y, because Z"
2. **Decision trees** — nested bullets or a small table, for branching choices
3. **Trade-off matrices** — options scored on the dimensions the author cares about
4. **Thresholds and defaults** — the specific numbers the author commits to
5. **Tells and smells** — fast heuristics for recognizing a situation

Avoid bare term→definition rows (that is the glossary) and prose paragraphs (that is the
chapters). Every line helps the reader *decide* something. One printed page kept beside you.

---

## Step 9 — Master SKILL.md

**Under 4,000 tokens. Compaction truncates from the end — most important content first.**

```markdown
---
name: <slug>
description: "Knowledge base from \"<Full Title>\" by <Author(s)>. Use when applying
  <author>'s frameworks for <3–6 key topics>, studying the book, or referencing its concepts."
---

# <Full Title>
**Author**: <Author(s)> | **Pages**: ~<N> | **Chapters**: <N> | **Generated**: <YYYY-MM-DD>

## How to Use This Skill
- **No argument** — load core frameworks
- **A topic** — I resolve it through the topic index and read that chapter
- **`chNN`** — I load that chapter
- **"what chapters do you have?"** — the full index

## Core Frameworks & Mental Models
<~2,000 tokens. The author's most important named frameworks, exact names preserved.
 Write as "Use X when Y", "Prefer X over Y because Z". A toolkit, not a summary.>

## Chapter Index
| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-<slug>.md) | <Title> | <framework>, <framework> |

## Topic Index
<Alphabetical. Major terms → the chapters covering them.>
- **<Term>** → ch<N>[, ch<N>]

## Supporting Files
- [glossary.md](glossary.md) · [patterns.md](patterns.md) · [cheatsheet.md](cheatsheet.md)

## Scope & Limits
Covers this source only. For hands-on implementation, combine with project-specific tools.
For topics beyond it, say so rather than improvising.
```

Frontmatter carries `name` and `description` only. No `allowed-tools`, ever (hard rule 5).

---

## Step 9.5 — Validate

```bash
python3 "$SKILL_ROOT/scripts/book_skill_validator.py" "$SKILLS_HOME/<slug>"
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --skill-dir "$SKILLS_HOME/<slug>"
```

The validator runs four families — frontmatter, safety, budget, index. **Errors block.**
Fix them and re-run; do not silently rewrite around a finding. Warnings are review prompts:
safety rules are deliberately broad, and a book about prompt injection legitimately trips them.

Common errors and what they mean:

| Rule | Meaning |
|------|---------|
| `index.dead_link` | The chapter index links a file that was never written |
| `index.topic_dangling` | A topic points at a chapter that does not exist |
| `budget.over_cap` on SKILL.md | Compaction will truncate the indexes — the navigation is the first thing lost |
| `unicode.invisible` | Extraction should have stripped this; investigate the source |
| `frontmatter.allowed_tools` | The generated skill is trying to grant itself tool authority |

---

## Step 10 — Clean up and report

Remove the workdir, then report:

```
✅ Skill created: $SKILLS_HOME/<slug>/
📚 <Title> — <Author>   📄 ~<N> pages | <N> chapters

  SKILL.md      core frameworks + indexes   ~<N> tokens (resident)
  chapters/     <N> summaries               ~<N> each, ~<N> total (on demand)
  glossary.md / patterns.md / cheatsheet.md ~<N> tokens

Usage:
  <slug>                 → core frameworks
  <slug> about <topic>   → resolve topic, read one chapter
  <slug> ch<N>           → one chapter summary

Reload: Claude Code — restart the session · Copilot CLI — /skills reload · Amp — restart
```

---

## Step 11 — Package as a claude-skills plugin *(this repo's addition)*

A folder in `~/.claude/skills/` is invisible to this library — no manifest, no agent, no
command, no marketplace entry. To let the rest of the repo route to it:

```bash
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" \
    --skill-dir "$SKILLS_HOME/<slug>" \
    --dest ./engineering --domain engineering \
    --source-note "<Full Title> by <Author>" --dry-run
```

Emits `<domain>/<slug>/` with `.claude-plugin/plugin.json`, `README.md`,
`agents/cs-<slug>.md`, `commands/cs-<slug>.md`, and the compiled skill under
`skills/<slug>/`, then prints the marketplace entry to register. Drop `--dry-run` to write.

**Rights gate.** The emitter defaults to `--distribution local`, which records
`source.cleared_for_distribution: false` in `.claude-plugin/authoring-notes.json`.
`--distribution shareable` **refuses** unless `--rights` names a basis:
`public-domain`, `open-license`, `internal-docs`, or `author-permission`. Fair use is
deliberately not an option — it is a defence, not a licence, and not this tool's call.

**Attribution is yours to add, by hand, when the source is someone else's work.** The emitter
writes a `source` block — how the skill was built — because that is all it can know; it has
`--source-note` free text and a rights basis, not an upstream URL, author or licence, and a
half-filled `attribution` block is worse than none. So when `--rights` is anything but
`internal-docs`, add an `attribution` block beside it in `authoring-notes.json`
(`derived_from`, `original_author`, `original_license`, `original_copyright`,
`derivation_note` — the shape the rest of this repo uses), and put the upstream licence
notice in the package's `LICENSE` and a credit line in its `README.md`. **That last part is
the obligation:** `authoring-notes.json` is authoring metadata Claude Code never reads, and a
sidecar JSON file is not a licence notice. `engineering/spinning-up-deep-rl` is the worked
example.

The emitter also refuses to wrap a skill with validation errors. Fix the source skill first.

Registration in `.claude-plugin/marketplace.json` stays manual — it is a repo-wide change.

---

## Update / fold-in workflow (Mode 4)

1. **Read the existing skill** — parse the chapter index, topic index, metadata, and core
   frameworks from `SKILL.md`; list `chapters/` for the highest number; read the three
   supporting files to see what is already indexed.
2. **Classify the new content** — a revision to an existing chapter (merge into that file)
   or a genuine addition (new `chNN` files numbered after the current highest).
3. **Write chapter files** per Step 7.
4. **Merge supporting files** — glossary re-alphabetized with chapter references appended to
   existing terms (`**Term** — definition (Ch 4, Ch 13)`); patterns appended in the same
   format; cheatsheet rules integrated into the existing structure.
5. **Regenerate SKILL.md** — bump chapter count and pages, refresh the generated date, fold
   the highest-impact new frameworks into Core Frameworks (staying under 4,000 tokens),
   append to both indexes.
6. **Run Step 9.5, then Step 10** with an update-shaped report: chapters added, terms merged,
   indexes touched.

---

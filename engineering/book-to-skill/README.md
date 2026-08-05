# book-to-skill

Turn a book, a documentation folder, or a pile of specs into an agent skill.

A source goes in. What comes out is a knowledge base the agent loads on demand: a small
resident core with the author's named frameworks and a topic index, one chapter file per
chapter, a glossary, a patterns file, and a decision cheatsheet. The agent reads the core, then
one chapter — never the whole source again.

Derived from [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT).
See **Deviations from upstream** below for the authoritative list of what changed.

---

## What it produces

| File | Contents | Budget |
|------|----------|--------|
| `SKILL.md` | Core frameworks + chapter index + topic index | < 4,000 tokens, resident |
| `chapters/chNN-*.md` | One summary per chapter | 800–3,000 tokens, on demand |
| `glossary.md` | Every significant term, alphabetized, with chapter | < 1,500 tokens |
| `patterns.md` | Techniques and design patterns with trade-offs | < 2,000 tokens |
| `cheatsheet.md` | Decision rules, thresholds, trade-off matrices | < 1,200 tokens |

Formats: PDF, EPUB, DOCX, HTML, Markdown, plain text, reStructuredText, AsciiDoc, RTF, and
MOBI/AZW/AZW3 with Calibre.

---

## Install

Already in this repository. Install as a marketplace plugin:

```
/plugin install book-to-skill@claude-code-skills
```

Or use the tools directly — they are self-contained under
`skills/book-to-skill/scripts/`.

**Dependencies:** none required. Every format degrades to a standard-library parser except
MOBI/AZW/AZW3, which need Calibre's `ebook-convert` on PATH. Optional packages
(`docling`, `pypdf`, `pdfminer.six`, `ebooklib`, `beautifulsoup4`, `python-docx`, `striprtf`)
raise extraction quality where installed; Poppler's `pdftotext` is the fastest PDF path.
Nothing is installed implicitly — run `extract_document.py --check` to see what is present and
get the exact install command.

---

## Use

```
/cs:book-to-skill ~/books/thinking-in-systems.pdf meadows-systems
/cs:book-to-skill ./docs/architecture/ '*.md' internal-arch
/cs:book-to-plugin ~/.claude/skills/meadows-systems --domain engineering
```

Or drive the tools yourself:

```bash
SKILL_ROOT=engineering/book-to-skill/skills/book-to-skill

python3 "$SKILL_ROOT/scripts/extract_document.py" BOOK.pdf --mode technical
#   -> prints the private workdir it created; capture it as $WORKDIR
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --full-text "$WORKDIR/full_text.txt"
# ... agent generates the skill ...
python3 "$SKILL_ROOT/scripts/book_skill_validator.py" ~/.claude/skills/<slug>
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" --skill-dir ~/.claude/skills/<slug> \
    --dest ./engineering --dry-run
```

Every tool supports `--help`, `--sample` and `--output json`.

---

## Tools

| Tool | Does |
|------|------|
| `extract_document.py` | Multi-format extraction → `full_text.txt` + `metadata.json`. Strips invisible Unicode, blocks DOCX entity expansion, detects chapters across Latin, Roman, Chinese, Thai and Korean heading styles. `--check` reports the environment. |
| `book_skill_validator.py` | Four check families over a generated skill — **frontmatter** (host-lens rules), **safety** (injection phrasing, invisible Unicode, authority grants), **budget** (token caps), **index** (dead links, unindexed chapters, dangling topic refs). Errors block; `--strict` promotes warnings. |
| `token_budget_estimator.py` | Pre-flight: models context-dump vs. discovery-loop vs. compiled-skill cost on this source's real chapter sizes and prints a worth-converting verdict. Post-flight: file-by-file budget audit. |
| `skill_plugin_emitter.py` | Wraps a compiled skill as a claude-skills plugin (manifest + agent + command + README) and prints the marketplace entry. Refuses to emit a shareable package without a rights basis. |

---

## Why the tokens matter

A live document-reading agent pays a **discovery loop tax**: it reads the table of contents,
pulls the chapter it guessed at, then backtracks for a definition it turns out to need. Every
one of those lands in history. Dumping the whole source into context is worse — it is resident,
and re-billed every turn.

Compiling pays that navigation cost once. A query afterwards costs what the answer costs, not
what the source costs. `token_budget_estimator.py` models all three on the real token sizes of
your source and says which one wins — including when the honest answer is "this source is too
small; just read it."

---

## Deviations from upstream

**This numbered list is the authoritative record.** `plugin.json`'s
`attribution.derivation_note` summarizes it; if the two ever disagree, this list wins.

**Structural**

1. **Repo-native layout.** Upstream is a standalone repository (`book_to_skill/` package,
   `scripts/`, `tools/`, `tests/`, `docs/`, `mkdocs.yml`, `pyproject.toml`, CI workflows). Here
   it is one plugin: `skills/book-to-skill/{SKILL.md,scripts,references,assets}` plus
   `agents/`, `commands/` and a manifest. Upstream's packaging, docs site, GitHub workflows and
   pytest suite were **not** vendored — this repo ships no build system and no test framework
   by design.

2. **The extraction library is vendored close to verbatim.** `book_to_skill/` — `config.py`,
   `exceptions.py`, `sanitize.py`, `dependencies.py`, `utils.py` and the seven per-format
   parsers — carries upstream's format chains, its chapter detection across five script
   families, and its Unicode and XXE hardening. That code is good and re-deriving it would
   only make it worse.

3. **The library is now import-pure.** `parse_arguments()`, `print_usage()`, `print_banner()`
   and `main()` were removed from `utils.py` and rebuilt as an argparse CLI in
   `extract_document.py`. Importing the library no longer prints, prompts, or parses `sys.argv`.

4. **SKILL.md rewritten Claude-Code-first.** The ten-step workflow, the per-chapter budget
   matrix and the update/fold-in workflow are preserved in substance. Added: this repo's
   frontmatter `metadata` block, an explicit hard-rules section, a forcing-question library,
   a references section, and related-skill disambiguation against `write-a-skill`,
   `skill-security-auditor` and `llm-wiki`. The skill-home table leads with Claude Code;
   Copilot CLI and Amp remain supported.

**Safety and behaviour**

5. **No implicit installs.** Upstream's `--install-missing` defaults to `ask`, which prompts on
   a TTY and runs `pip install` into the caller's environment. Here the default is `report`:
   it prints the exact install command and uses the stdlib fallback. `--install-missing yes`
   remains as an explicit opt-in. Reading a file should not install packages.

6. **Rights gate on distribution.** Upstream documents its copyright posture in prose. Here it
   is enforced: `skill_plugin_emitter.py --distribution shareable` **refuses** unless
   `--rights` names `public-domain`, `open-license`, `internal-docs` or `author-permission`.
   `fair-use` is deliberately absent — it is a defence, not a licence, and not a script's call.
   Without a basis, packages emit as `local` and carry
   `source.cleared_for_distribution: false` in the manifest.

7. **Clean JSON output.** The vendored parsers narrate progress on stdout. Under
   `--output json` that narration is redirected to stderr, so stdout carries the metadata
   document and nothing else. Upstream had no JSON mode.

8. **Attribution moved off the hot path.** Upstream prints an ASCII banner from
   `scripts/banner.txt` on every extraction run, and ships `BACKERS.md` + `FUNDING.yml`.
   Attribution here lives in `LICENSE`, `plugin.json`, this README and the SKILL.md footer —
   correct, and not re-emitted on every invocation.

**Tooling**

9. **Three upstream tools became four argparse CLIs**, each meeting this repo's contract:
   real `--help`, a `--sample` that runs the tool on built-in fixtures, `--output json`, and
   documented exit codes. Upstream's `extract.py` parsed `sys.argv` by hand and ignored unknown
   flags with a warning, so a typo'd flag silently changed nothing.

10. **Validator merged and extended.** Upstream's `validate_skill.py` (frontmatter lint) and
    `scan_generated_skill.py` (injection scan) are one gate, `book_skill_validator.py`, with
    every finding carrying a family and a severity. Two check families are new:
    **budget** — every generated file against the token caps the workflow commits to, with
    `SKILL.md` overflow as the only hard budget error (compaction truncates from the end, so
    overflow eats the indexes first); and **index** — dead chapter links, chapter files nothing
    links to, topic entries pointing at chapters that were never written, and a missing topic
    index. Index integrity is the failure that silently breaks navigation while the skill still
    looks complete, and upstream had no check for it.

11. **Folded YAML scalars are parsed correctly.** Upstream reads a frontmatter value with a
    single-line regex. A wrapped description therefore under-reports its length — so the
    1024-character cap never fires on exactly the descriptions long enough to hit it — and gets
    truncated at the wrap when copied into a manifest. `scalar_value()` folds continuation
    lines and unescapes inner quotes. A description-trigger warning was also added, matching
    this repo's `write-a-skill` rule that a description must say when to use the skill.

12. **`discovery_tax.py` → `token_budget_estimator.py`.** The optional `tiktoken` path was
    dropped so every token number in the pipeline comes from one deterministic estimator and
    no budget gate depends on whether a package is installed. Added: a post-flight file-by-file
    budget audit, and an explicit **worth-converting verdict** — upstream reports only savings
    ratios, which read as advocacy on a source too small to be worth converting at all.

13. **`parsers/html.py` renamed to `parsers/html_text.py`.** A module named `html.py`
    shadows the standard library's `html` package the moment its own directory lands on
    `sys.path[0]` — which happens whenever the file is run directly — and `import
    html.parser` then fails with "'html' is not a package". Renaming removes the hazard
    instead of documenting it. Two import lines changed; nothing else.

14. **CI-contract wiring.** The eight vendored library modules are registered in
    `scripts/smoke_exceptions.txt` (they are imported as `book_to_skill.*`, never run as
    CLIs), and the agent's tool table uses paths that resolve from the agent's own folder
    so `scripts/check_paths.py` can follow them. Neither has an upstream counterpart —
    upstream has no equivalent gates.

15. **Private, per-invocation working directory.** Upstream defaults the extraction workdir
    to a fixed `<tempdir>/book_skill_work`. On a shared host that is CWE-377/CWE-59: any local
    user can pre-create the directory in a world-writable `/tmp` (the sticky bit prevents
    deletion, not creation) and plant a symlink named `full_text.txt` pointing at a file the
    victim can write — `Path.write_text` follows symlinks. Two concurrent runs also clobber each
    other. The default is now a fresh `mkdtemp` (unpredictable, `0700` by construction);
    artifacts are written `0600`; an explicit `--workdir`/`BOOK_SKILL_WORKDIR` is honoured but
    symlink-refused and mode-restricted first. `parsers/calibre.py` no longer writes its
    `ebook-convert` scratch file to the shared directory either — which also fixes a real bug,
    since it read a module-level constant and so ignored `--workdir` entirely.

16. **Shared budget constants.** `book_skill_validator.py` and `token_budget_estimator.py` both
    gate on the same token caps; those now live once in `book_to_skill/config.py`
    (`SKILL_FILE_BUDGETS`, `CHAPTER_TOKEN_CEILING`) rather than being restated in each tool,
    where they would drift the first time a cap changed.

---

## Security audit

`engineering/skills/skill-security-auditor` on `skills/book-to-skill/`: **0 critical, 4 high**,
all four reviewed and accepted:

| Finding | Why it stands |
|---------|---------------|
| `FS-ABUSE` — `shutil.rmtree(package_root)` in the emitter | The `--force` overwrite path. Guarded by `_assert_replaceable()`: refuses a symlink, a non-directory, a path resolving outside the destination root, a directory containing the source skill, and any directory without a `.claude-plugin/plugin.json` — so it only ever deletes a plugin package this tool created. |
| `DEPS-RUNTIME` ×3 in `dependencies.py` | One is a docstring sentence; two are `print()` calls that *show* an install command. None of the three install anything. The real `pip` subprocess sits behind `--install-missing yes` and is never reached by default (deviation 5). |

Two `PRIV-ESC` criticals were real and are fixed: upstream's install hints contained the literal
string `sudo apt install poppler-utils`. They now name the package manager without telling anyone
to escalate.

---

## Where it fits

- **`engineering/write-a-skill`** — authoring a skill from expertise in your head. This one
  compiles a skill from a document on disk. With both, author first and fold the document in.
- **`engineering/skill-security-auditor`** — the repo-wide security audit. The validator here
  is the converter's own gate, not a replacement for it.
- **`engineering/llm-wiki`** — an incrementally-grown vault across many sources over time.
  This compiles one bounded source set into one skill, once.

---

## License

MIT. See [`LICENSE`](LICENSE) — copyright is retained by the upstream author for the vendored
extraction library, with modifications and additions by this repository under the same terms.

The MIT license covers the **converter**. It does not cover the books or documents you process
with it, and it does not make a compiled skill redistributable. See
`skills/book-to-skill/references/rights_and_provenance.md`.

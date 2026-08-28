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
WORKDIR=$(mktemp -d)     # or omit --workdir and capture the path the tool prints
SLUG=<author-lastname>-<concept>

python3 "$SKILL_ROOT/scripts/extract_document.py" BOOK.pdf --mode technical --workdir "$WORKDIR"
python3 "$SKILL_ROOT/scripts/token_budget_estimator.py" --full-text "$WORKDIR/full_text.txt"
# ... agent generates the skill ...
python3 "$SKILL_ROOT/scripts/book_skill_validator.py" ~/.claude/skills/"$SLUG"
python3 "$SKILL_ROOT/scripts/skill_plugin_emitter.py" --skill-dir ~/.claude/skills/"$SLUG" \
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

**This numbered list is the authoritative record.** `.claude-plugin/authoring-notes.json`'s
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

17. **Zip-of-XML hardening generalized to EPUB, plus decompression-bomb caps.** Upstream
    hardened DOCX and only DOCX: `validate_docx_xml_safety()` screened that archive for
    DTD/entity declarations before any parser touched it. EPUB is the same shape — a zip whose
    members are XML — and its `ebooklib` path handed the file straight to a third-party XML
    stack with no equivalent check, despite `ebooklib` being one of the packages this skill
    recommends installing. The guard now lives in `book_to_skill/zip_safety.py` and runs for
    both formats. Every archive read also goes through `safe_read()`, which consults the
    declared uncompressed size and the compression ratio *before* decompressing: a 200 MB
    zip bomb is refused at ~14 MB peak RSS instead of being materialized. Neither parser ever
    writes archive members to disk, so zip-slip stays out of scope by construction.

18. **Packaging refuses a source tree containing symlinks.** The validator checks the files it
    knows about (`SKILL.md`, the three supporting files, `chapters/*.md`), but `shutil.copytree`
    defaults to `symlinks=False` and follows a link *anywhere else* in the tree — an `assets/`
    entry, any subdirectory — baking the target's real content into a package that may then be
    emitted as `--distribution shareable`. `_assert_no_symlinks()` now walks the whole tree and
    refuses, and it runs **before** the validation branch so `--skip-validation` cannot bypass
    it. `copytree` also passes `symlinks=True` so a future edit loosening that check cannot
    silently reintroduce dereferencing.

19. **The magic-byte sniff path goes through the size budget too.** `extract_single_file()`
    sniffs unknown extensions and read a `mimetype` member with a bare `zf.read()` — the
    earliest attacker-controlled point in the pipeline, running *before* a format is chosen
    and before any of `zip_safety.py`'s checks. A single-member zip declaring a huge
    uncompressed `mimetype` was fully decompressed there. Now routed through `safe_read()`;
    its `ExtractionError` deliberately sits outside the surrounding `except` tuple so a bomb
    reports as a bomb rather than as a generic unsupported format. Verified: a 200 MB / 1029×
    fixture with no file extension is refused at ~15 MB peak RSS.

20. **Emitter correctness and scope.** Three smaller fixes: `--author`/`--author-url` now reach
    the *printed* marketplace entry (it hardcoded one name, so the snippet whose whole job is
    preventing hand-edit mistakes contradicted the manifest beside it); the symlink guard is
    backed by a **post-copy re-walk** that deletes the package if a link appeared during the
    copy, closing the check-then-act window rather than only narrowing it; and the manifest
    emits `source.license_scope` stating that the top-level `license` covers the package
    scaffolding, not the compiled notes — a distinction that previously lived only in README
    prose where a tool reading the metadata alone would miss it. (Deviation 26 later moved
    that whole `source` block out of `plugin.json` and into the sidecar.)

21. **The documented quick-start actually runs.** SKILL.md's copy-paste block referenced
    `$WORKDIR` and `$SKILLS_HOME` without ever defining them — following it literally produced
    a traceback on step 2. Both are now real assignments, and all five steps were executed
    verbatim end to end as a check. A quick-start that does not run is worse than no
    quick-start: it is the part a reader trusts most.

22. **Gate tools refuse bad paths instead of reporting success.** `token_budget_estimator.py
    --skill-dir <typo>` produced a complete, plausible budget audit — every row "missing",
    every cap satisfied, **exit 0** — which reads as a pass. A gate that reports success for a
    path that is not there is worse than no gate. It now refuses a missing directory, a
    non-directory, and a directory without `SKILL.md` (exit 2); `--full-text <missing>` raised
    a bare `FileNotFoundError` traceback and now refuses cleanly. The other three tools already
    handled bad input; this one was the outlier.

23. **Three more upstream artifacts cleaned.** `epub.py`'s `except (KeyError, Exception)` is
    simply `except Exception` — it swallowed everything, including the size-refusal that
    `safe_read()` now raises, quietly disarming deviation 17 at that call site. Narrowed so an
    `ExtractionError` propagates and only genuine parse failures fall through to the `.opf`
    glob. `utils.py` emitted a dynamic `{pages_label: pages}` key alongside a literal `"pages"`,
    which collided whenever the label *was* `"pages"`; the alias is now added only when it
    differs. A stray artifact word was removed from a `pdf.py` comment.

24. **`tool | head` no longer tracebacks.** Piping a report into `head` closes the pipe
    mid-write and surfaced a `BrokenPipeError` stack trace (observed once; racy on flush
    timing). All four CLIs now exit 141 quietly, the standard SIGPIPE convention.

25. **The workdir race is closed, not just narrowed.** The explicit-`--workdir` path was
    still check-then-act: `mkdir(parents=True, exist_ok=True)` does **not** raise on a
    symlink-to-directory, because its exists-branch tests `is_dir()`, which follows symlinks —
    verified directly. Worse, the per-file `is_symlink()` check cannot back that up: a file
    inside a swapped directory is an ordinary file, not a link, so a directory swap defeated
    the artifact-level guard entirely.

    Three changes close it. `resolve_workdir()` now attempts `mkdir` **first** and only
    inspects an already-existing path, using `os.lstat` (which does not follow the final
    component). `open_workdir()` then pins the directory with `O_NOFOLLOW|O_DIRECTORY`, and
    both artifacts are written through that descriptor — an fd names an inode, so a later
    rename or symlink swap of the path cannot redirect the write. `_write_private()` creates
    with `O_CREAT|O_EXCL|O_NOFOLLOW` at mode 0600, which has no check-then-act window at all;
    an artifact from a previous run into the same `--workdir` is `unlink`ed first, and unlink
    removes the link itself, never its target.

    Verified against a live race: pin the directory, rename it away, plant a symlink to an
    attacker directory, then write — the data lands in the pinned inode and the attacker
    directory stays empty. Also verified that a pre-planted `full_text.txt -> victim` symlink
    leaves the victim's contents intact and is replaced by a 0600 file we own. Degrades to the
    previous path-based checks on platforms without `dir_fd`/`O_NOFOLLOW` (Windows).

26. **Provenance moved out of `plugin.json` into the sidecar the repo actually allows.**
    The manifest builder wrote its whole `source` block (spec, build pattern, source document,
    chapter count, distribution, `license_scope`, `rights_basis`) into `plugin.json`, and an
    inline comment asserted that `source` and `attribution` were "approved extension fields."
    That had been true and no longer was: Claude Code rejects an entire manifest on any
    unrecognized key (issue #954), and this repo's own `scripts/check_plugin_json.py` hard-fails
    a `plugin.json` carrying either field, pointing at `.claude-plugin/authoring-notes.json`
    instead. So every package the emitter produced failed the repo's blocking CI gate the moment
    it was committed — a defect that only surfaces at the very last step of the pipeline, which
    is why it survived. `_plugin_manifest()` now emits spec fields only, and a new
    `_authoring_notes()` writes the `source` block to `.claude-plugin/authoring-notes.json`.
    Note that `source` remains a *valid* key in a `marketplace.json` `plugins[]` entry, which is
    how it leaked into the manifest in the first place; the printed marketplace snippet is
    unchanged and still correct.

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

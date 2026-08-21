# Document Extraction Pipeline

What `extract_document.py` actually does per format, which extractor wins and why, and the
failure modes that produce text that *looks* fine and quietly ruins the conversion.

---

## 1. Extractor chains

Each format tries extractors in order and uses the first that returns non-empty text. Every
chain ends in a standard-library parser except MOBI/AZW, which has no stdlib path.

| Format | Order tried | Fallback | Notes |
|--------|-------------|----------|-------|
| **PDF** (`--mode technical`) | `docling` → text chain | text chain | Layout-aware; preserves tables, code, formulas as Markdown. ~1.5s/page. |
| **PDF** (`--mode text`) | `pdftotext -layout` → `pypdf` → `pdfminer.six` | fails with install hints | `pdftotext` (Poppler) is fastest and the only one that keeps column layout. |
| **EPUB** | `ebooklib` + `beautifulsoup4` → stdlib `zipfile` | stdlib | The stdlib path reads the OPF spine for true reading order. |
| **DOCX** | `python-docx` → stdlib `zipfile` + `ElementTree` | stdlib | The stdlib path preserves document order; `python-docx` appends all tables last. |
| **HTML** | `beautifulsoup4` → stdlib `html.parser` | stdlib | The stdlib extractor emits block boundaries on open **and** close tags. |
| **RTF** | `striprtf` → regex fallback | regex | The fallback drops whole destination groups, not just control words. |
| **Text / MD / RST / AsciiDoc** | BOM-aware read | — | Tries UTF-8-sig, UTF-32, UTF-16, then UTF-8 → cp1252 → latin-1. |
| **MOBI / AZW / AZW3** | Calibre `ebook-convert` | **none** | Hard requirement. |

`extract_document.py --check` reports what is installed and prints the exact install command.
Nothing is installed implicitly — `--install-missing yes` is the only path that runs `pip`.

---

## 2. Why `pdftotext -layout` before the Python parsers

PDF has no notion of a paragraph, a heading, or a reading order — it has positioned glyphs.
Every extractor is reconstructing structure that was never stored. Poppler's `pdftotext` with
`-layout` preserves the visual column arrangement, which is what makes a table of contents
survive as parseable lines rather than interleaved fragments. `pypdf` and `pdfminer.six` are
correct fallbacks but flatten multi-column layouts more aggressively.

For technical books the right answer is different. Docling (IBM Research, 2024) runs layout
analysis and table-structure recognition and exports Markdown, so a comparison table stays a
table and a code block keeps its indentation. It is roughly two orders of magnitude slower per
page, which is exactly why Step 1.5 asks rather than guessing.

**Post-processing.** The PDF path then cleans `pdftotext` output: running headers and footers
repeated on more than half the pages are dropped, bare page numbers at a page edge are dropped,
and words hyphenated across a line break are rejoined. That last one is a documented lossy
tradeoff — a genuinely hyphenated compound wrapped at its hyphen ("well-\nknown") rejoins as
one word.

---

## 3. Chapter detection

Structure detection is what makes the whole pipeline work: no chapters means no chapter files,
no topic index, and no navigation. The detector counts **distinct chapter numbers**, so a table
of contents entry and its body heading do not double-count.

Recognized heading styles:

- **Arabic** — `Chapter 5`, `Capítulo 5:`, `Chapitre 5.`, `Kapitel 5`, `Capitolo 5`, `Hoofdstuk 5`
- **Roman** — `I: Loomings`, `II. The Carpet-Bag`, and lowercase only inside a Markdown heading
- **Chinese** — `第三章`, `第 3 回`, `第十二节`, plus Markdown headings led by a CJK ordinal
- **Thai** — `บทที่ 3`, `ตอนที่ ๘๗` (Thai digits remapped)
- **Korean** — `제1장 총칙`, including the `제6장의2` inserted-chapter form used in statutes
- **Structural fallback** — ATX (`# Title`, `== Section`) and setext/RST underline headings,
  used only when no numeric headings were found

The detector rejects prose cross-references. `Chapter 6 explores...` is not a heading: a real
heading's number is followed by end-of-line, punctuation, or a capitalized title word, and a
lowercase continuation means it is a sentence. Headings inside fenced code blocks are skipped.

**When detection fails**, the usual cause is a technical PDF whose headings were flattened by
text extraction. The fix is `--mode technical`, not a different regex.

---

## 4. Token estimation

`estimate_tokens()` is words ÷ 0.75 for whitespace-delimited text, with CJK codepoints counted
separately at ~1.5 chars/token. The CJK branch is not an optimization — Chinese and Japanese
carry little or no whitespace, so word-splitting a Chinese book collapses it to a handful of
"words" and the cost pre-flight under-reports by orders of magnitude.

The estimate is deliberately dependency-free so the same source always yields the same number
and no budget gate depends on whether `tiktoken` happens to be installed.

---

## 5. Security: invisible Unicode

Every extracted document is untrusted input that will later be read by a model as
instructions. Extraction strips four classes of invisible code point:

1. **Zero-width and invisible spacers** — U+200B–U+200D, U+2060–U+2064, U+FEFF, U+00AD,
   U+034F, U+180E. They render as nothing, so text between them is invisible to a human
   reviewer and plain to a model.
2. **Bidirectional formatting controls** — U+202A–U+202E, U+2066–U+2069, U+200E/U+200F,
   U+061C. This is the **Trojan Source** class (Boucher & Anderson, CVE-2021-42574): these
   characters do not change the sequence a model reads, they change the order a human *sees*.
   A crafted line can display as innocuous study advice while the model consumes an injected
   instruction. Legitimate right-to-left text is unaffected — the Unicode Bidirectional
   Algorithm (UAX #9) derives direction from the characters themselves, so Arabic and Hebrew
   still render correctly without explicit embeddings.
3. **Invisible letters** — Hangul fillers U+115F, U+1160, U+3164, U+FFA0. Not format
   controls, so a category-based filter misses them, but they render as blank width and
   survive whitespace normalization.
4. **The Unicode tag block** — U+E0000–U+E007F, originally language tags, now used to smuggle
   an entire ASCII payload as invisible characters.

Extraction reports how many were removed. `book_skill_validator.py` re-checks the generated
files against the **same** predicate, imported from the same module rather than duplicated —
the two defenses drifting apart is a real bug class, and it happened upstream.

This is the OWASP LLM Top 10's **LLM01: Prompt Injection**, indirect variant: the attack
arrives inside content the model is asked to process rather than in the user's message.
Stripping invisible characters is one layer; the validator's phrase scan is a second; a human
reading the generated files before loading them is the one that actually holds.

---

## 6. Security: XML entity expansion in DOCX

DOCX is a ZIP of XML. Before parsing, every `.xml` and `.rels` member is scanned for `<!DOCTYPE`
or `<!ENTITY` declarations across several encodings, and extraction is refused if any are
present. This blocks both **billion laughs** entity-expansion denial of service and **XXE**
external-entity file disclosure. Python's `xml.etree.ElementTree` does not expand external
entities by default, but it does expand internal ones — the scan is what closes that.

---

## 7. Failure modes that look like success

The dangerous outcomes are the ones that produce plausible text:

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Chapters detected: 0, on a real book | Scanned/image PDF, or headings flattened | `--mode technical`; if the PDF is images, it needs OCR first — the extractor does not do OCR |
| Text is present but garbled or interleaved | Multi-column PDF flattened by a fallback parser | Install Poppler so `pdftotext -layout` is used |
| EPUB chapters in the wrong order | Reading order taken from the manifest rather than the spine | The stdlib path reads the spine; check the file is not DRM-protected |
| DOCX tables all at the end | `python-docx` appends tables after paragraphs | The stdlib fallback preserves order |
| RTF text littered with font names | Destination groups stripped of markup but not removed | The regex fallback drops whole groups; confirm it was used |
| Everything empty, no error | DRM-protected source | Nothing to do — the file is encrypted |

Rule of thumb: read the first 2,000 characters of `full_text.txt` before spending a generation
pass on it. Thirty seconds there beats discovering it in chapter 14.

---

## Sources

1. Poppler `pdftotext` documentation, poppler.freedesktop.org. (`-layout` mode; column
   preservation.)
2. Auer, C. et al. "Docling Technical Report." IBM Research, 2024. (Layout analysis and
   table-structure recognition for PDF → Markdown.)
3. W3C. *EPUB 3.3* Recommendation, 2023. (OPF package document; spine as reading order.)
4. ECMA-376, *Office Open XML File Formats*, 5th ed. (WordprocessingML document structure.)
5. Boucher, N. & Anderson, R. "Trojan Source: Invisible Vulnerabilities." *USENIX Security*,
   2023; CVE-2021-42574. (Bidirectional-override attacks.)
6. Unicode Consortium. *UAX #9: Unicode Bidirectional Algorithm*. (Implicit direction from
   character properties; explicit formatting characters.)
7. OWASP. *Top 10 for Large Language Model Applications* — LLM01: Prompt Injection, 2025.
   (Indirect injection via processed content.)
8. OWASP. *XML External Entity (XXE) Prevention Cheat Sheet*. (DTD and entity handling.)

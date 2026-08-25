# Why This Is a Companion, Not a Compiled Copy

This repository ships `engineering/book-to-skill`, which compiles a document on disk into a
knowledge-base skill. This skill was **not** produced that way, and the reason is worth stating
plainly, because the same reasoning applies to every future request of the form "turn this book
into a skill."

---

## The three facts that decided it

1. **The book is copyrighted.** *Deep Learning* (Goodfellow, Bengio & Courville) is published by
   MIT Press, 2016. Free-to-read is not free-to-redistribute; the two are unrelated.
2. **The publisher's position is explicit.** deeplearningbook.org states that the HTML-only
   presentation exists as a deliberate friction against copying and editing, required by the
   authors' contract with MIT Press, and that PDF distribution is not permitted.
3. **This repository is public.** `book-to-skill`'s own rights gate refuses a `shareable`
   distribution without one of `public-domain`, `open-license`, `internal-docs`, or
   `author-permission`. None applies here. Its `references/rights_and_provenance.md` lists
   "publish a compiled skill of a copyrighted book to a public marketplace" under **Do not**.

`book-to-skill` also has a hard rule that it converts files already on disk and never scrapes a
book from the web — so the requested pipeline could not have been run against a URL regardless.

## What was built instead

An **original companion**: every chapter file is written from domain knowledge, states what the
chapter establishes, how to use it, and where it has aged, and links to the official free
chapter. The organizing structure — 20 chapters in 3 parts — is the book's published table of
contents, which is factual metadata, not expression.

Concretely, this skill contains:

- **No passages, paragraphs, sentences, or figures from the book.**
- **No paraphrase-per-paragraph** — the compression ratio is roughly a whole chapter to a page,
  which is a synthesis, not a substitute.
- **Links to the official chapters**, so the skill sends readers *to* the book rather than
  replacing it.
- **Original material the book does not contain**: the 2016→2026 delta layer, the prerequisite
  graph, the study method, and four executable tools.

Under the idea/expression line (17 U.S.C. §102(b); *Baker v. Selden*), what this skill carries —
the names of methods, the structure of an argument, decision rules stated plainly, and terms
defined in other words — sits on the ideas side. The chapters themselves, in the authors' prose,
sit on the expression side, and stay at deeplearningbook.org.

**Not legal advice.** This is the posture and its reasoning. Where money or publication is
involved, ask a lawyer.

## The rule this establishes for the repository

> When a user asks to convert a copyrighted work into a shareable skill, build a **companion**
> that indexes and updates the source, not a **compilation** that reproduces it. Compile only
> when the rights gate clears — and keep compiled output local when it does not.

A companion is often the better artifact anyway. A compilation freezes a source at its
publication date; a companion can say which parts of a ten-year-old text are still true, which
is precisely what a reader of a 2016 deep learning book needs most.

## Use this skill correctly

- **Do** read the book at deeplearningbook.org; this navigates it.
- **Do** use the delta reference before acting on any 2016-era recommendation.
- **Don't** treat the chapter files as a substitute for reading the chapters — they are the
  answer key for retrieval practice, not the material.
- **Don't** extend this skill by pasting book text into it. That converts a companion into the
  thing this file exists to avoid.

## Sources

1. Goodfellow, Bengio & Courville, *Deep Learning*, MIT Press, 2016 — https://www.deeplearningbook.org/
2. deeplearningbook.org — the site's own statement on its HTML-only format and PDF distribution.
3. 17 U.S.C. §102(b) — ideas, procedures, processes and methods of operation are outside
   copyright.
4. *Baker v. Selden*, 101 U.S. 99 (1879) — the idea/expression dichotomy.
5. 17 U.S.C. §107 — fair use as a four-factor defence, assessed case by case.
6. *Authors Guild v. Google, Inc.*, 804 F.3d 202 (2d Cir. 2015) — indexing that does not
   substitute for the original held transformative.
7. This repository: `engineering/book-to-skill/skills/book-to-skill/references/rights_and_provenance.md`
   (the rights gate) and its SKILL.md hard rules 1 and 6.

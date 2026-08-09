# Rights and Provenance

**Not legal advice.** This document explains the posture the tool takes and why. Where money,
publication, or an employer's exposure is involved, ask a lawyer.

---

## 1. What the tool does and does not do

The converter ships **no** book content. It is a converter for files you already have, it runs
locally, and nothing leaves the machine. What it produces is a set of structured notes about a
source: named frameworks, definitions, decision rules, and an index — the kind of thing a
careful reader produces in a notebook, not a copy of the work.

That distinction is doing real work, and it is why the converter's seventh quality rule is
"never copy raw source text." The rule is not stylistic prudence. A file of long verbatim
passages is a reproduction wearing a Markdown extension; a file of extracted structure is not.

---

## 2. The idea/expression line

US copyright protects **expression**, not ideas, procedures, systems, or methods of operation
(17 U.S.C. §102(b)). *Baker v. Selden*, 101 U.S. 99 (1879), is the origin: a book explaining a
bookkeeping system was protected, but the system itself — and the blank forms needed to use it
— were not.

For this tool that line is directly operational:

| Generally on the ideas side | Generally on the expression side |
|---|---|
| A framework's **name** and what it is for | The chapter that introduces it, in the author's prose |
| The **steps** of a method | The author's phrasing of those steps at length |
| A **decision rule** stated plainly | An extended passage arguing for it |
| A **term's** definition in your own words | The author's definition copied verbatim |
| The **structure** of the argument | The argument as written |

The converter's output shape follows that column split deliberately. It also means the
`## Worked Example` section is the one to watch: "reconstruct compactly" is the instruction,
and reproducing the author's full example verbatim crosses back over.

---

## 3. Fair use, honestly

Fair use (17 U.S.C. §107) is a four-factor defence, not a permission slip, and it is assessed
case by case:

1. **Purpose and character** — personal study and research weigh favourably; commercial
   redistribution does not. Transformation matters.
2. **Nature of the work** — factual and technical works are more amenable than fiction.
3. **Amount and substantiality** — how much, and whether it takes the heart of the work.
   Structured notes take little; a chapter-by-chapter paraphrase of a narrative takes much.
4. **Market effect** — the factor courts weight heavily. Notes that send you back to the book
   do not substitute for it; a compilation that makes buying it unnecessary does.

Two cases bound the space usefully. *Authors Guild v. HathiTrust*, 755 F.3d 87 (2d Cir. 2014),
and *Authors Guild v. Google, Inc.*, 804 F.3d 202 (2d Cir. 2015), both found that scanning
books to build a **search index** — surfacing where terms appear, with snippets rather than
readable text — was transformative fair use, in large part because the output did not
substitute for the original. A compiled book skill is closer to that index than to a copy. It
is not identical, and nobody has litigated this shape.

This is exactly why `--rights fair-use` **is not an option** in the emitter. Fair use is what
you argue after someone objects. It is not a basis a script should let you assert in a manifest.

---

## 4. Outside the US

- **Berne Convention** — protection is automatic on creation in all member states; no
  registration or notice is required. "There was no copyright notice" is not a finding.
- **EU** — the InfoSoc Directive (2001/29/EC) has no open-ended fair use; it has an exhaustive
  list of narrower exceptions, including private, non-commercial personal copying in many
  member states.
- **EU DSM Directive (2019/790)** — Article 3 permits text and data mining for scientific
  research by research organisations; Article 4 permits it more broadly **unless the rights
  holder has reserved it** in a machine-readable way. The Article 4 opt-out is worth checking
  for anything you intend to share.
- **UK** — "fair dealing" is narrower than fair use and enumerated: research and private study
  (non-commercial), criticism, review, quotation, news reporting.

Personal study notes from a book you own sit comfortably in most of these. Publishing a
compiled skill does not.

---

## 5. The rights gate

`skill_plugin_emitter.py` refuses to emit a `--distribution shareable` package unless
`--rights` names a basis:

| Basis | Means |
|-------|-------|
| `public-domain` | Copyright expired, forfeited, or never applied (e.g. most US federal works) |
| `open-license` | The source carries a licence permitting derivative distribution — CC BY, CC BY-SA, MIT, Apache-2.0. Check the share-alike and attribution terms; they follow the derivative. |
| `internal-docs` | Your organisation's own documentation, shared inside it. The usual constraint here is confidentiality, not copyright. |
| `author-permission` | The rights holder gave written permission. Keep the writing. |

Anything else emits as `--distribution local`, recording
`source.cleared_for_distribution: false` in the manifest — an advisory marker, not
enforcement, that says the package was never cleared for sharing.

Note what the gate is **not**: it does not inspect your source, it cannot verify a claim, and
`local` does not make a package safe to publish later. It exists to make the question
unavoidable at the moment of packaging, when it is cheap to answer, rather than after
distribution, when it is not.

---

## 6. Attribution the compiled skill must carry

Every generated skill records, in `SKILL.md` and in the emitted plugin's README and manifest:

- **Source document** — full title and author(s)
- **Generated date** — so a reader knows which edition-era the notes reflect
- **Chapter count and page count** — the scope of what was covered
- **Distribution and rights basis** — from the gate above

This is provenance, not politeness. A compiled skill is a lossy derivative that will be read as
authoritative. A reader who can see it was compiled from one source on one date can judge what
it is likely to be missing; a reader who cannot will treat it as ground truth. The generated
`## Scope & Limits` section exists for the same reason — it is the skill telling the agent
where to stop and say "the source doesn't cover this."

---

## 7. Practical guidance

**Safe by default**
- Books you own, compiled for your own use, kept local
- Your organisation's internal documentation, shared internally
- Public-domain works (Project Gutenberg, Standard Ebooks, most US federal publications)
- Openly-licensed technical documentation, with the licence's attribution terms respected

**Ask first**
- A compiled skill from a copyrighted book shared with your team
- Anything a client or employer will use commercially
- Sources under an NDA — copyright is the *second* problem there

**Do not**
- Publish a compiled skill of a copyrighted book to a public marketplace
- Present compiled notes as a substitute for buying the source
- Convert a source you obtained from a pirate library — how the file was acquired is a separate
  and worse problem than what you then do with it

---

## Sources

1. 17 U.S.C. §102(b) — scope of copyright; ideas, procedures and methods of operation excluded.
2. *Baker v. Selden*, 101 U.S. 99 (1879) — the idea/expression dichotomy.
3. 17 U.S.C. §107 — fair use; the four factors.
4. *Authors Guild v. HathiTrust*, 755 F.3d 87 (2d Cir. 2014) — full-text search index as
   transformative use.
5. *Authors Guild v. Google, Inc.*, 804 F.3d 202 (2d Cir. 2015) — book scanning for search and
   snippet display held transformative; market-substitution analysis.
6. Berne Convention for the Protection of Literary and Artistic Works (Paris Act, 1971) —
   automatic protection; no formalities.
7. Directive (EU) 2019/790 (DSM), Articles 3–4 — text and data mining exceptions and the
   machine-readable rights reservation.
8. UK Copyright, Designs and Patents Act 1988, ss. 29–30 — fair dealing for research, private
   study, criticism, review and quotation.

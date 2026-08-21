# Knowledge Extraction Canon — why structure beats summary

The converter's first quality rule is "extract structure, not summaries." That is not a style
preference. It comes from a long line of work on what makes written knowledge usable later.

---

## 1. The distinction: structure vs. summary

A **summary** compresses a text by discarding detail proportionally. It answers "what was in
this?" A **structure extraction** discards *narrative* and keeps *operators*: named things you
can apply. It answers "what can I now do?"

| | Summary | Structure extraction |
|---|---------|---------------------|
| Unit | Paragraph, chapter | Named framework, rule, technique, anti-pattern |
| Preserves | Argument flow | Exact names, application conditions, trade-offs |
| Query shape | "What did chapter 4 say?" | "Which framework applies when X?" |
| Fails when | You need to act | The source has no reusable structure (fiction, narrative) |
| Decay | Rots — you remember the gist, not the tool | Survives — the name is the retrieval handle |

Mortimer Adler's *How to Read a Book* (1940, rev. 1972) makes the strongest case. His third
level, **analytical reading**, has four rules, and the second is "come to terms with the
author" — identify the key words the author uses in a special sense and pin their exact
meaning. Adler's claim is that you have not understood a book until you can state its
propositions in the author's own terms. That is precisely what the `## Frameworks Introduced`
section requires, and why the converter refuses to paraphrase "The 5 Whys" into "ask why a
few times." The name **is** the interface.

---

## 2. Atomicity: one idea per file

Niklas Luhmann's Zettelkasten — the slip-box that produced ~70 books and 400 articles — kept
one idea per slip, each with an address and explicit links to others. Sönke Ahrens's *How to
Take Smart Notes* (2017) reconstructs the method and identifies the failure mode the converter
inherits: **collector's fallacy** — accumulating material feels like learning and is not.
Notes that merely record are dead weight; notes that state a claim in your own words, linked
to where they connect, compound.

Andy Matuschak's *evergreen notes* (working notes, 2019–) sharpens two properties this
converter builds on directly:

- **Evergreen notes should be atomic** — one concept per note, so it can be linked and reused
  from many directions. This is why chapters are separate files rather than sections of one
  document.
- **Evergreen notes should be densely linked** — the links *are* the thinking. This is the
  `## Connects To` section and the topic index; without them the chapter files are an
  unnavigable pile.

The topic index is the load-bearing piece. Luhmann's slip-box worked because of its index and
its link addresses, not because of the slips. A compiled skill with 28 excellent chapter files
and no topic index is 28 files an agent will never find.

---

## 3. Chunking: why named frameworks survive compression

Cognitive Load Theory (John Sweller, 1988 onward) explains why the named-framework unit is the
right size. Working memory holds a small number of elements; expertise is largely the
possession of **schemas** that let many elements be handled as one. A named framework is a
schema with a handle. "The 5 Whys" is one element; "ask why, then ask why about that answer,
five times, to reach a root cause rather than a symptom" is five.

Barbara Oakley's *A Mind for Numbers* (2014) popularizes the same mechanism as **chunking**:
you learn by binding scattered pieces into a single retrievable unit, and the binding needs
both focused practice and a name. This is why `## Key Concepts` caps at 5–10 terms per chapter
— past that, you are transcribing a glossary, not chunking.

The **Feynman technique** (widely attributed to Richard Feynman; documented in Gleick's
*Genius*, 1992) supplies the test the `## Core Idea` section applies: if you cannot state the
chapter's central point in one or two plain sentences, you have not extracted it — you have
copied it. A Core Idea that needs a paragraph is a signal to re-read, not to write more.

---

## 4. Why anti-patterns get their own section

Extracting only what to do produces a skill that cannot recognize trouble. The
`## Anti-patterns` section exists because the recognition case and the application case are
different retrieval problems: you reach for a framework when you know what you are doing, and
you need an anti-pattern when you do not.

Gary Klein's work on **recognition-primed decision making** (*Sources of Power*, 1998) found
that experts under time pressure rarely compare options — they recognize a situation as a type
and run the response that type calls for. Klein's later "premortem" technique inverts it:
imagine the failure has happened and work backwards to its causes. The cheatsheet's "tells and
smells" layer is recognition-primed decision making in file form: fast pattern → named
situation → response.

---

## 5. Why the cheatsheet is the differentiated layer

Glossary, patterns and cheatsheet look like three flavours of the same list. They are not:

- **glossary** answers *what does this word mean* — pure recall
- **patterns** answers *how do I do this thing* — procedure
- **cheatsheet** answers *what should I do here* — judgment

Only the third captures what separates someone who has read the book from someone who has
absorbed it. Decision rules ("when X, do Y, because Z"), thresholds the author actually commits
to, and trade-off matrices are the author's judgment made portable. A cheatsheet that drifts
into term→definition rows has silently become a second glossary, which is why the converter's
Step 8 lists what to avoid as explicitly as what to include.

---

## 6. What does not convert well

Being honest about the boundary keeps the tool credible:

- **Narrative non-fiction with no reusable structure.** A biography compresses to a summary
  because there is no framework to name. The converter will produce chapter files, and they
  will be book reports.
- **Fiction.** No frameworks, no anti-patterns, no decision rules.
- **Reference works already structured for lookup** — a dictionary, an API reference, a
  standards document with numbered clauses. They are already indexed; compiling them adds a
  lossy layer between the reader and the authority.
- **Sources you will consult once.** Conversion has a fixed up-front cost. Below roughly 3×
  the compiled skill's size, reading the document is cheaper — which is why the token budget
  estimator prints a verdict rather than a number.

---

## Sources

1. Adler, M. & Van Doren, C. *How to Read a Book: The Classic Guide to Intelligent Reading*.
   Simon & Schuster, rev. ed. 1972. (Analytical reading; "come to terms with the author.")
2. Ahrens, S. *How to Take Smart Notes*. 2017. (Zettelkasten method; collector's fallacy.)
3. Matuschak, A. "Evergreen notes." *Working Notes*, notes.andymatuschak.org, 2019–.
   (Atomicity and dense linking as note-design principles.)
4. Sweller, J. "Cognitive Load During Problem Solving: Effects on Learning." *Cognitive
   Science* 12(2), 1988. (Schema acquisition; working-memory limits.)
5. Oakley, B. *A Mind for Numbers*. TarcherPerigee, 2014. (Chunking; focused vs. diffuse modes.)
6. Klein, G. *Sources of Power: How People Make Decisions*. MIT Press, 1998. (Recognition-primed
   decision making; later the premortem.)
7. Gleick, J. *Genius: The Life and Science of Richard Feynman*. Pantheon, 1992. (The
   explain-it-simply test commonly called the Feynman technique.)

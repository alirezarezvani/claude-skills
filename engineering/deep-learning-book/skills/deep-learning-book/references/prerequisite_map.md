# Prerequisite Map

The book's part structure is not its dependency structure. Readers who go strictly front-to-back
spend weeks in Chapters 2–4 before touching a network, and a large fraction stop there. This file
gives the actual graph.

---

## The real dependencies

```
ch01 ──────────────────────────────────► (context only; no hard dependents)

ch02 (linear algebra) ──┬──► ch04 ──┬──► ch08 ──► ch09, ch10
                        │           │
ch03 (probability) ─────┴──► ch05 ──┴──► ch06 ──► ch07 ──► ch11
                             │
                             └──► ch13 ──► ch14 ──► ch15
                                    │
ch03 ──► ch16 ──► ch17 ──► ch18 ──► ch19 ──► ch20
```

**Hard prerequisites** (skipping these makes the target chapter unreadable, not merely harder):

| To read | You need | Specifically |
|---|---|---|
| ch08 | ch02, ch04 | eigenvalues, condition number, Hessian, Taylor expansion |
| ch06 | ch03 | the output distributions that determine output units and losses |
| ch07 | ch05, ch04 | bias–variance; KKT for the constraint view of penalties |
| ch18 | ch16, ch17 | the partition function; sampling |
| ch19 | ch03 | KL divergence, and its asymmetry |
| ch20 | ch13, ch19 | the latent-variable template; the ELBO |

**Soft prerequisites** — helpful, not blocking: ch02 before ch13 (PCA), ch09 before ch12,
ch10 before ch12.

## Chapters you can read early, out of order

- **ch05** — the single highest-value chapter for a practitioner. Needs only basic probability.
- **ch11** — readable on day one and immediately actionable. Depends on ch05's vocabulary only.
- **ch01** — context; skim it.
- **ch09** — comprehensible with ch06 alone if you accept the optimization details on faith.

## Chapters you can defer or skip, by goal

| Goal | Skip or defer |
|---|---|
| Applied practitioner shipping models | Part III entirely (ch13–20), except ch14's denoising section |
| Preparing for modern generative modelling | Nothing in Part III — but read ch18 before ch20 |
| Interview / fundamentals refresher | ch12 (dated), ch17–19 (unless the role is probabilistic ML) |
| Understanding transformers | ch10 for the gradient analysis; then leave the book for the 2017 paper |
| Research in probabilistic ML | Everything; Part III is the reason this book has no substitute |

## The Part I wall, and how to get through it

Chapters 2–4 are compressed reference material, not pedagogy. Three viable strategies:

1. **Read-on-demand** (recommended for applied readers): skim ch2–4 once for vocabulary, start at
   ch05, and return to a specific section when ch08 uses it. The prerequisite table above tells
   you exactly which section.
2. **Front-load** (recommended if you intend to read Part III): work ch2–4 properly with a
   separate linear algebra source alongside. Budget 2–3× the page count in time.
3. **Substitute**: use a dedicated linear algebra or probability text for Part I and treat these
   chapters purely as a notation reference for the rest of the book.

Strategy 1 is right for most readers and is what `scripts/reading_path_planner.py` recommends by
default. Strategy 2 is right when Part III is the destination — its chapters compound, and gaps
compound with them.

## Time budgeting

Reported reading times vary by an order of magnitude, so treat any figure as a planning
assumption, not a fact. As a planning heuristic used by the reading-path planner: a Part I or
Part III chapter is roughly 1.5–2× the time of a Part II chapter of the same length, because the
derivation density is higher. The planner exposes its per-chapter assumptions in
`--output json` so you can recalibrate them against your own first chapter.

## Sources

1. Goodfellow, Bengio & Courville, *Deep Learning*, MIT Press 2016 — table of contents and part
   structure: https://www.deeplearningbook.org/
2. Sweller, van Merriënboer & Paas, "Cognitive Architecture and Instructional Design," *Educational
   Psychology Review* 10(3), 1998 — element interactivity and intrinsic load, which is what makes
   ch2–4 expensive.
3. Sweller & Cooper, "The Use of Worked Examples as a Substitute for Problem Solving," *Cognition
   and Instruction* 2(1), 1985 — the worked-example effect for novices.
4. Bjork & Bjork, "Making Things Hard on Yourself, But in a Good Way: Creating Desirable
   Difficulties to Enhance Learning," 2011.
5. Roediger & Karpicke, "Test-Enhanced Learning," *Psychological Science* 17(3), 2006.
6. Ericsson, Krampe & Tesch-Römer, "The Role of Deliberate Practice in the Acquisition of Expert
   Performance," *Psychological Review* 100(3), 1993.
7. Chi, Bassok, Lewis, Reimann & Glaser, "Self-Explanations: How Students Study and Use Examples
   in Learning to Solve Problems," *Cognitive Science* 13(2), 1989.

# Hook and Fold Mechanics — the first 140 characters decide everything else

LinkedIn truncates a post in the feed. On mobile that happens around 140
characters, on desktop around 210, and the reader's decision to press "…see more"
is made entirely on what is above that line. Everything you wrote below it is
conditional on those two sentences.

This is not a copywriting flourish. It is the single structural constraint the
platform imposes on text, and most posts ignore it.

---

## The numbers

| Limit | Value | Confidence |
|---|---|---|
| Post hard cap | 3,000 characters | 🟡 third-party documented, stable |
| Mobile fold ("…see more") | ~140 characters | 🟡 varies with viewport and locale |
| Desktop fold | ~210 characters | 🟡 |
| Highest median engagement band | ~1,300-2,500 characters | 🟡 third-party studies |
| Comment character cap | 1,250 | 🟡 |

Mobile is the binding constraint. Write to 140 and desktop takes care of itself.

**On the engagement band:** it is a correlation in third-party data, not a rule.
Long posts are longer because people had more to say, and a 400-character post
with something specific in it beats a padded 1,800-character one every time.
`post_linter.py` reports the band as INFO, never as a defect.

## What a hook has to do

Not "be catchy". Three concrete jobs:

1. **Complete a thought inside the fold.** A truncated fragment gives the reader
   nothing to decide on. `post_linter.py` flags a post where no sentence ends
   before character 140.
2. **Create a specific gap.** Not a vague tease — a gap the reader can feel the
   shape of. "Our onboarding took six weeks. We got it to four days without
   hiring anyone." The gap is *how*, and it is specific enough to be worth the
   click.
3. **Signal who it is for.** A reader outside your audience should be able to
   skip cleanly. Trying to hook everyone is how a post hooks nobody.

## Hook shapes that work, and why

| Shape | Example opening | Why it works |
|---|---|---|
| **Number + reversal** | "Our onboarding took 6 weeks. We got it to 4 days without hiring anyone." | Concrete, and the reversal names the constraint people assume is binding |
| **The mistake** | "I spent five weeks automating the wrong step." | Costly-signal: admitting error is expensive, so it reads as true |
| **The measurement** | "Work-in-progress time was 6 days. Wait time between owners was 35." | The number does the work; no adjective required |
| **The sentence someone said** | "'Nobody believes the dashboard.' That was the actual problem." | Quoted speech is concrete and carries a voice |
| **The refusal** | "We deleted the kickoff call. 80% of accounts never needed it." | A decision with a consequence attached |

## Openers to delete on sight

`post_linter.py` flags these because they are the most-scrolled-past
constructions on the platform:

- "I'm excited to announce…" / "I'm thrilled…" / "I'm humbled…"
- "In today's fast-paced world…"
- "Quick thought:"
- Any opener whose first eight words would fit any post about anything.

The excitement openers have a specific problem: they put *your* feeling first and
the reader's interest second, in the two sentences where you can least afford it.
Announce the thing, then say why it mattered.

## Formatting inside the fold and below it

- **Line breaks are structure, not decoration.** Three to four lines per block.
- **Do not write in one-line paragraphs throughout.** The "broetry" cadence —
  every sentence its own paragraph — reads as formatted for an algorithm rather
  than for a person, and the linter flags six or more consecutive one-liners.
- **No Unicode pseudo-bold.** The "bold text generators" produce Mathematical
  Alphanumeric Symbols. Screen readers announce them character by character as
  mathematical symbols, and LinkedIn's search does not index them as words. This
  is a blocking finding in the linter, not a style preference — see
  `accessibility_and_inclusion.md`.
- **Links go in the first comment.** Say "link in the comments" in the post.

## The close

The end of a post is where a comment either happens or does not. Two failure
modes:

- **No invitation at all.** The post is complete, correct, and closed; the only
  available response is agreement.
- **A fake invitation.** "Thoughts?" and "Agree?" are engagement bait with a
  question mark. `post_linter.py` treats bait as blocking, and LinkedIn's
  Professional Community Policies name it as demoted content.

What works is a real question you would want answered, narrow enough that a
specific person has a specific answer: "What did the handoff cost you the last
time you measured it?"

## Editing pass

Three passes, in this order:

1. **Cut the first paragraph.** It is usually the throat-clearing. Check whether
   the post starts better at paragraph two — it does more often than not.
2. **Read the first 140 characters alone.** Would you press "see more"?
3. **Read it aloud.** Every sentence you stumble on is a sentence a reader
   stumbles on. This catches more than any linter.

---

## Sources

1. Nielsen Norman Group. **F-Shaped Pattern for Reading Web Content** (2006) and
   **"How People Read Online"** — scanning behaviour and the weight of the first
   visible lines.
2. Nielsen Norman Group. **"Microcontent: How to Write Headlines, Page Titles,
   and Subject Lines"** — front-loading for any truncated string.
3. Loewenstein, G. **"The Psychology of Curiosity: A Review and Reinterpretation."**
   *Psychological Bulletin*, 1994 — the information-gap theory that explains why a
   *specific* gap works and a vague tease does not.
4. Heath, C. & Heath, D. **Made to Stick** — concreteness, unexpectedness, and
   the curse of knowledge.
5. Zinsser, W. **On Writing Well** — cutting every word that does no work; the
   "cut the first paragraph" pass comes straight from here.
6. LinkedIn Engineering. **"Understanding feed dwell time to improve LinkedIn
   feed ranking."** — why holding attention past the fold is a measured
   objective, and why padding to game it is not.
7. LinkedIn. **Professional Community Policies** — engagement bait as named,
   demoted content.

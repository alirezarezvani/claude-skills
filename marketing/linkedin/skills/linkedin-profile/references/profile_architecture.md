# Profile Architecture — what each section is actually for

A LinkedIn profile is not a CV. A CV is read by someone who has already decided
to consider you; a profile is read by someone deciding whether to. The sections
are therefore ordered by a different logic, and most people fill them in as if
they were the same document.

The frame that makes this concrete: **a profile has three distinct readers**, and
a section that serves none of them is dead weight.

| Reader | Arrives from | Decides in | Reads |
|---|---|---|---|
| **The scanner** | Your comment on someone else's post | ~3 seconds | Photo, name, headline. Nothing else. |
| **The evaluator** | A search result, a referral, your post | ~40 seconds | Headline, the visible half of About, Featured, current role. |
| **The decider** | Already interested, doing diligence | Several minutes | Everything, including recommendations and the gaps in your history. |

Almost all traffic is the scanner. Almost all conversion is the decider. The
sections in between exist to move people down that list.

---

## Section by section

### Photo — for the scanner
A face, well lit, roughly filling the frame, recognisable at 48 pixels. That is
the entire specification. The common failure is a full-body shot that renders as
a smudge at feed size.

### Banner (1584 × 396) — the most wasted space on the platform
The default gradient says nothing. This is the cheapest place to state what you
do, name your audience, or show one artifact. Rendering caveat: the profile photo
and the mobile layout crop the lower-left corner, so keep text in the upper right
and never centre it.

### Headline — the only string that travels
It appears next to every comment you leave, in every search result, in every
invitation you send. See `headline_and_positioning.md`; this is the single
highest-leverage edit available.

### About — for the evaluator, and it is truncated
LinkedIn collapses it after roughly the first 265-300 characters. Whatever is
above that fold is the whole section for most readers. Structure that survives:

1. **The tension** — the problem your audience recognises, stated in their words.
2. **Who you are for** — specific enough that someone could be excluded.
3. **Proof** — two or three results, with real numbers.
4. **How you work** — the part that is yours rather than your job title's.
5. **A call to action** — who should reach out, and what they get.

Written in first person. A profile written in the third person reads as a press
release someone else wrote, which on a personal profile is exactly what it is.

### Experience — outcomes, not duties
A duty list is interchangeable across everyone who has ever held the title.
"Responsible for backend services" describes several hundred thousand people.
"Cut p99 checkout latency from 1.9s to 340ms by moving the pricing call
off the critical path" describes one.

Two or three bullets per role, and only the roles that support the current
positioning. Older roles get a line each. Gaps are fine and unexplained gaps are
also fine — most readers do not care, and the ones who do will ask.

### Featured — the one section you fully control
Whatever you pin here is what a visitor sees before your feed. Empty, and they
see whatever you last reposted. Put the artifact a buyer, hiring manager, or peer
could evaluate in sixty seconds: the talk, the repo, the teardown, the post that
did what you want more of.

Refresh it quarterly. A featured item from three years ago dates the whole
profile.

### Skills — a matching surface, not a personality test
Recruiters and LinkedIn's own matching use these. List the ones you would accept
an interview on. The endorsement counts matter far less than people assume; the
presence of the term matters more.

### Recommendations — the only text you did not write
Two specific recommendations outperform ten generic ones. The way to get a
specific one is to ask for a specific one: tell the person the project and the
aspect you want them to speak to, and offer to write a first draft they can edit.
That request is normal and almost always accepted.

### Custom URL, Open To / Services, contact info — two-minute fixes
Low individual value, near-zero cost, and their absence signals a profile nobody
maintains.

---

## The ordering rule

When time is short, work in this order, because it is the order in which readers
encounter the sections and drop out:

1. Headline (every reader, always)
2. Photo (every reader, three seconds)
3. About opening — the first two sentences only
4. Featured (one item, today)
5. Current role bullets
6. Everything else

`profile_completeness_auditor.py` implements this as points-per-hour and will
usually put Featured and Open To first, because they cost minutes and recover
real points.

---

## Sources

1. Nielsen Norman Group. **F-Shaped Pattern for Reading Web Content** and
   **"How People Read Online"** — why the first lines carry the decision and the
   rest is skimmed.
2. Krug, S. **Don't Make Me Think** (3rd ed.) — scannability as the design
   constraint for anything a stranger reads without commitment.
3. Minto, B. **The Pyramid Principle** — the answer first, support after; the
   structure the About fold forces on you whether you like it or not.
4. Goffman, E. **The Presentation of Self in Everyday Life** (1959) — a profile
   is a front-stage performance with an audience that knows it is one; the
   credibility comes from specificity, not polish.
5. Heath, C. & Heath, D. **Made to Stick** — concreteness as the property that
   makes a claim memorable and checkable.
6. LinkedIn Help. **Creators Core / Updates to Creator Mode** — what the creator
   surfaces actually change on a profile.
7. Clark, D. **Reinventing You** — sequencing a positioning change so the public
   record supports the new claim before you make it.

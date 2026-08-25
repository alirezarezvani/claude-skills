# Headline and Positioning — 220 characters that follow you everywhere

The headline is the only string on LinkedIn that travels with you. It rides along
with every comment you leave in someone else's thread, every search result you
appear in, and every connection request you send. A person may see your headline
forty times before they ever open your profile.

Most headlines are a job title. A job title is the one thing a reader could have
guessed.

---

## The constraint

| Limit | Value | Confidence |
|---|---|---|
| Hard character cap | 220 | 🟡 third-party documented, stable for years |
| Visible in search results / invitation previews | ~60-70 characters | 🟡 varies by surface and viewport |
| Visible next to a comment | Fewer still, and it truncates mid-word | 🟡 |

So the headline has a **front-loaded budget**: the first sixty characters do most
of the work, and everything after them is a bonus that some readers will see.
This is why "Senior Engineer | Ex-Google | Speaker | Mentor | Dog dad" fails —
the strongest segment is second and the weakest is where a reader's eye lands.

## The five things a headline has to do

`headline_scorer.py` scores these at 20 points each.

1. **Name the audience.** "for Series A SaaS founders", "for clinical data teams".
   A headline that could belong to anyone is addressed to no one.
2. **Name the outcome.** What changes because of you. "Cut onboarding from six
   weeks to four days" is an outcome. "Passionate about customer experience" is
   a mood.
3. **Carry one piece of proof.** A number, a prior company (`ex-Stripe`), a
   credential, a scale figure. One is enough and it has to be true.
4. **Stay searchable.** LinkedIn search matches headline text. An invented title
   ("Chief Clarity Officer") ranks for nothing. Keep at least one conventional
   role or skill term alongside the creative framing.
5. **Stay readable.** Three segments maximum. At most one emoji. No buzzword
   filler — "results-driven", "passionate about", "thought leader" all describe an
   attitude rather than a capability, and every reader has learned to skip them.

## Structures that work

```
[Role a recruiter would search] for [specific audience] | [proof] | [the line that is yours]

Fractional Head of Data for Series A SaaS | Cut BigQuery spend 62% at
Zendesk scale | I make dashboards people trust
```

```
I help [audience] [outcome] without [the cost they expect]

I help clinical teams pass MDR audits without a six-month documentation freeze
```

```
[Current title] · [the thing you are moving toward] · [proof of the move]

Backend engineer moving into developer advocacy · 40 conference talks
watched, 3 given · I write the docs I wish existed
```

That third pattern matters for career transitions. **State the destination, not
only the origin.** A headline that describes only where you have been makes every
reader do the imaginative work of placing you somewhere else, and most will not
bother.

## Positioning before wording

A headline cannot fix a positioning that does not exist. If you cannot answer
these three, the headline will keep coming out generic no matter how many times
it is rewritten:

1. Who specifically is this for — specifically enough that someone is excluded?
2. What do they get that they would not get from the next person with your title?
3. What is the evidence, and is it already public?

That is the `positioning_brief.py` conversation in `linkedin-strategy`. Run it
first when the answers are fuzzy; the headline falls out of a good brief in
about ten minutes.

## Changing the headline mid-career-transition

Two competing risks, and people usually only see one:

- Change too early and current colleagues read it as "already leaving".
- Change too late and every new reader files you under the old category, which
  is the category you are trying to leave.

The resolution is that **the headline is read overwhelmingly by strangers**, and
strangers are the audience of a transition. Change it, and let the current role
carry the continuity in the Experience section where it belongs.

## Testing

You cannot A/B test a headline on LinkedIn — there is one, it applies
retroactively to everything, and profile-view counts are too noisy at individual
scale. What you can do:

- Read it out loud. If you would not say it to someone at a conference, cut it.
- Show it to one person in the target audience and ask what they think you do.
  If they paraphrase it back wrong, the headline is wrong, and that single test
  is worth more than any tool.
- Run `headline_scorer.py` for the mechanical faults, then use the person.

---

## Sources

1. Ries, A. & Trout, J. **Positioning: The Battle for Your Mind** — the origin of
   "positioning is what you do to the mind of the prospect", and why a category
   claim beats an attribute list.
2. Heath, C. & Heath, D. **Made to Stick** — concreteness and the curse of
   knowledge, which is exactly why practitioners write headlines only other
   practitioners can parse.
3. Nielsen Norman Group. **Microcontent: How to Write Headlines, Page Titles, and
   Subject Lines** — the front-loading rule for any truncated string.
4. Clark, D. **Stand Out** — building a positioning around one distinctive idea
   rather than a portfolio of competences.
5. Ibarra, H. **Working Identity** — why career transitions require acting into
   the new identity publicly rather than deciding it privately first.
6. Zinsser, W. **On Writing Well** — the discipline of cutting every word that
   does no work, which is the entire craft of a 220-character string.
7. LinkedIn Help. **Search and profile visibility** documentation — headline text
   is matched in search; invented titles are not.

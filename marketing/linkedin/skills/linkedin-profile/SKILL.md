---
name: linkedin-profile
description: Use when someone wants their LinkedIn profile audited or rewritten — headline, About section, experience bullets, Featured, banner, recommendations — or says "fix my headline", "my profile gets views but nothing happens", "optimize my LinkedIn profile", "what should my About section say". Scores the headline on five dimensions, audits the whole profile 0-100 and ranks fixes by points per hour, and assembles an About section that survives the "…see more" fold.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
---

# LinkedIn Profile — audit, then rewrite the parts that pay

A profile is not a CV. A CV is read by someone who already decided to consider you; a
profile is read by someone deciding whether to. Three readers, in descending volume: the
**scanner** (three seconds, from your comment on someone else's post — sees photo and
headline only), the **evaluator** (forty seconds — headline, half the About, Featured), the
**decider** (minutes — everything). Almost all traffic is the scanner. Almost all conversion
is the decider.

## Workflow

**1. Audit before rewriting.** Ask them to describe their profile section by section, or
have them fill [`assets/profile_worksheet.md`](assets/profile_worksheet.md), then:

```bash
python3 scripts/profile_completeness_auditor.py --input profile.json --output human
```

Exit 0 STRONG / 2 INCOMPLETE / 3 WEAK. It ranks every gap by **points per hour** and prints
a first-hour plan — usually Featured, Open To, and skills, which cost minutes and recover
real points. Start there, not with the About section they wanted to agonise over.

**2. Headline next — it is the only string that travels.** It rides along with every comment,
search result, and invitation.

```bash
python3 scripts/headline_scorer.py --headline "..." --output human
```

Five dimensions at 20 points: audience, outcome, proof, searchability, clarity. Exit 0 SHIP
(≥75) / 2 SHARPEN / 3 REWRITE. It also checks the 220-character cap and whether the first
~60 characters — the part that survives in search results and invitation previews — carry
anything.

Iterate here. Two or three passes is normal; the stop condition is exit 0, or the user
saying they would say it out loud to a peer.

**3. About section — write to the fold.** LinkedIn collapses it after roughly 265-300
characters. Collect the five parts from the user, then assemble:

```bash
python3 scripts/about_section_builder.py --input about.json --output human
```

It refuses a fold that cuts mid-sentence, a fold carrying no audience and no proof, a
missing call to action, and anything over 2,600 characters.

**4. Experience, Featured, recommendations.** Rewrite duty lists as outcomes. Pin one
artifact a stranger could evaluate in sixty seconds. Ask for two specific recommendations by
naming the project and offering a first draft.

## Rules

- **Never invent a credential, a metric, or a role.** Every number on a profile is checkable
  by someone. If the proof does not exist, the claim is qualitative or it is absent.
- **First person.** A profile in third person reads as a press release someone else wrote.
- **The fold is the section.** Whatever sits above "…see more" is what most readers get.
- **Front-load the headline.** The strongest segment first; everything after is a bonus.
- **Do not fetch anything.** The user describes their own profile; nothing is scraped.

## Scripts

| Script | Role |
|---|---|
| [`scripts/headline_scorer.py`](scripts/headline_scorer.py) | Headline 0-100 on audience / outcome / proof / searchability / clarity, plus the 220-char cap and front-load check. |
| [`scripts/profile_completeness_auditor.py`](scripts/profile_completeness_auditor.py) | Whole profile 0-100 across 14 weighted checks; fixes ranked by points per hour with a first-hour plan. |
| [`scripts/about_section_builder.py`](scripts/about_section_builder.py) | Assembles the About section from named parts and refuses a broken fold, a missing CTA, or an over-length section. |

## References and assets

- [`references/profile_architecture.md`](references/profile_architecture.md) — what each section is for, and the three readers (7 sources)
- [`references/headline_and_positioning.md`](references/headline_and_positioning.md) — the 220 characters that follow you everywhere (7 sources)

- [`assets/profile_worksheet.md`](assets/profile_worksheet.md) — fillable section-by-section worksheet
- [`assets/example_profile.json`](assets/example_profile.json) — input shape for the auditor

## Distinct from

- **`linkedin-strategy`** — what to post and how often. This is who you are before you post.
  If the audience answer is fuzzy, run `positioning_brief.py` there first; the headline
  falls out of a good brief in ten minutes.
- **`product-team/`, `c-level-advisor/`** — career and role strategy. This writes the profile,
  not the career plan.

---

**Version:** 1.0.0

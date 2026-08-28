---
name: "cs-linkedin-profile"
description: "/cs:linkedin-profile — Audit a LinkedIn profile 0-100, rank every fix by points per hour, score the headline on five dimensions against the 220-character cap, and assemble an About section that survives the '…see more' fold."
argument-hint: "[your headline, or a description of your profile section by section]"
---

# /cs:linkedin-profile — Audit first, rewrite what pays

**Command:** `/cs:linkedin-profile [headline or profile description]`

Nothing is fetched. You describe your own profile, or fill in
`skills/linkedin-profile/assets/profile_worksheet.md`.

## When to run

- "Fix my headline" / "rewrite my About section"
- "My profile gets views but nothing happens"
- Before any outreach push — comments and DMs drive profile visits, and a weak headline
  wastes every one of them

## What you get

1. **A completeness score 0-100** across 14 weighted checks, with every gap ranked by points
   per hour and a first-hour plan.
2. **A headline score** on audience / outcome / proof / searchability / clarity, plus the
   220-character cap and the front-load check on the first ~60 characters.
3. **An assembled About section** that ends a sentence before the fold and carries audience
   or proof above it.
4. **Rewritten experience bullets** — outcomes, not duties.

## Workflow

```bash
# 1. Whole profile, fixes ranked by leverage
python3 ../skills/linkedin-profile/scripts/profile_completeness_auditor.py \
  --input profile.json --output human      # or --sample to see the shape

# 2. Headline — iterate to exit 0
python3 ../skills/linkedin-profile/scripts/headline_scorer.py \
  --headline "..." --output human

# 3. About — refuses a broken fold, a missing CTA, or an over-length section
python3 ../skills/linkedin-profile/scripts/about_section_builder.py \
  --input about.json --output human
```

## Discipline

- **Never invent a credential, metric, or role.** Everything on a profile is checkable.
- **First person.** Third person on a personal profile reads as a press release.
- **The fold is the section** — whatever sits above "…see more" is what most readers get.
- **Front-load the headline**; the first 60 characters do most of the work.
- Start with the first-hour plan, not with the About section you want to agonise over.

## Stop conditions

- Headline at exit 0 (SHIP), or the user would say it out loud to a peer → done.
- About at exit 0, or the user knowingly accepts a named warning → done.
- Auditor at STRONG, or the first-hour plan completed and the rest scheduled → done.

## Related

- Skill: [`linkedin-profile`](../skills/linkedin-profile/SKILL.md)
- Run [`/cs:linkedin-plan`](cs-linkedin-plan.md) first if the audience answer is still fuzzy

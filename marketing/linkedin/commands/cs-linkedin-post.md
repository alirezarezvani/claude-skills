---
name: "cs-linkedin-post"
description: "/cs:linkedin-post — Pick the format the material actually supports, draft to the ~140-character mobile fold, and lint 0-100 across mechanics, hook, integrity, and accessibility. Blocking findings for the 3,000-character cap, engagement bait, and Unicode pseudo-bold."
argument-hint: "[the post idea, or paste a draft to be reviewed]"
---

# /cs:linkedin-post — Format, draft, lint

**Command:** `/cs:linkedin-post [idea or draft]`

## When to run

- "Write a LinkedIn post about X" / "review my draft"
- "Is this hook any good?"
- "Should this be a carousel or a text post?"

## When NOT to run

- No positioning brief yet → [`/cs:linkedin-plan`](cs-linkedin-plan.md) first
- A comment or a DM → [`/cs:linkedin-outreach`](cs-linkedin-outreach.md); different craft
- Repurposing a long source → [`/cs:linkedin-repurpose`](cs-linkedin-repurpose.md)

## What you get

1. **A format recommendation** with the constraint it carries — or one question when the top
   two score within a point.
2. **A draft** built from your specifics, with a sentence completing inside the first ~140
   characters.
3. **A lint score 0-100** with every finding carrying a fix.
4. **Accessibility done** — alt text written, captions flagged, no pseudo-bold.

## Workflow

```bash
# 1. Format from the material, not from fashion
python3 ../skills/linkedin-content/scripts/format_picker.py \
  --goal authority --material data --material tutorial --minutes 120 --output human

# 2. Draft (the interview comes first: the number, the mistake, the sentence someone said)

# 3. Lint to a clean exit
python3 ../skills/linkedin-content/scripts/post_linter.py \
  --input draft.md --has-image --output human
#   exit 0 SHIP · exit 2 REVISE (or any blocking finding) · exit 3 REWRITE
```

## Discipline

- **Interview before drafting.** A post with no specifics cannot be fixed by editing.
- **Never fabricate a number, client, result, or quote** — not even as a placeholder.
- **Write to the mobile fold.** A sentence completes before character 140.
- **Links in the first comment**, and say so in the post.
- **No engagement bait.** Ask the question the post actually earned.
- **One idea per post.** If it needs two, it is two posts.
- **Cut the first paragraph** and check whether the post starts better at paragraph two.

## Stop conditions

- Linter at exit 0 → done. Hand over with "you are the author of record; read every line".
- Linter at exit 2 with only warnings the user has knowingly accepted → done, with the
  accepted warnings restated.
- Three REWRITE passes on the same draft → the problem is the idea, not the wording. Go back
  to the specifics.

## Related

- Agent: [`cs-linkedin-editor`](../agents/cs-linkedin-editor.md)
- Skill: [`linkedin-content`](../skills/linkedin-content/SKILL.md)
- Assets: [`post_templates.md`](../skills/linkedin-content/assets/post_templates.md)

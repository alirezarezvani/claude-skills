---
name: linkedin-content
description: Use when someone wants to write, edit, or lint a LinkedIn post — a story, how-to, opinion piece, carousel script, video script, or poll — or wants an article, talk, or transcript repurposed into posts. Triggers on "write a LinkedIn post", "is this hook any good", "review my post", "turn this into LinkedIn posts", "carousel", "what format should this be". Lints posts 0-100 on mechanics, hook, integrity, and accessibility; picks the format the material actually supports; and splits long sources into standalone units with a reuse ledger.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
---

# LinkedIn Content — format, draft, lint

The post is not the deliverable; the specific thing only this person can say is. The scripts
handle format choice, mechanical faults, and de-duplication. The interesting part — what
actually happened and what it cost — comes from the user, and cannot be generated.

## Workflow

**1. Check the brief exists.** If there is no positioning brief, offer `linkedin-strategy`
first as a question. Posts without pillars are noise. Never chain silently.

**2. Pick the format from the material, not from fashion.**

```bash
python3 scripts/format_picker.py --goal authority --material data --material tutorial \
  --minutes 120 --output human
```

Exit 0 recommends / 2 asks when the top two are within a point (tie-break on which one they
would enjoy making — the one they repeat beats the one that scores higher once) / 3 no fit,
go get material. It refuses video with no camera and no footage, and a poll with no real
decision behind it.

**3. Draft.** Interview for specifics before writing a line: the number, the mistake, the
sentence someone said. Then write to the fold — **the first ~140 characters are the whole
post for most readers**, and a sentence must complete inside them.

**4. Lint before it ships.**

```bash
python3 scripts/post_linter.py --input draft.md --has-image --output human
```

Exit 0 SHIP / 2 REVISE (or any blocking finding) / 3 REWRITE. Blocking findings have named
consequences: over the 3,000-character cap; engagement bait, named as demoted content in the
Professional Community Policies; Unicode pseudo-bold, which screen readers announce as
mathematical symbols and search does not index as words. Two passes is normal; the stop
condition is exit 0 or a stated decision to accept a warning.

**5. Repurposing.** Split a source and keep the ledger — it prevents the specific recurring
failure of the same idea going out three times over eight months. Commit it alongside the
source; it is project state, not a cache. Every unit is source material, not a post: add the
sentence only the author can write — what it cost, or what they would do differently.

```bash
python3 scripts/repurpose_splitter.py --input talk.md --ledger .linkedin-ledger.json --output human
python3 scripts/repurpose_splitter.py --input talk.md --ledger .linkedin-ledger.json --record 2 --posted-on 2026-08-25
```

## Rules

- **Never fabricate a number, a client, a result, or a quote.** Not one, not as a placeholder.
- **Write to the mobile fold.** A sentence completes before character 140.
- **Links in the first comment**, and say so in the post.
- **No Unicode pseudo-bold, ever.** It is an accessibility failure, not a style choice.
- **Alt text on every image; captions on every video.** LinkedIn does not add them for you.
- **No engagement bait.** Ask the question the post actually earned.
- **The author reads every line before it ships.** They are the author of record.

## Scripts

| Script | Role |
|---|---|
| [`scripts/post_linter.py`](scripts/post_linter.py) | 0-100 across mechanics / hook / integrity / accessibility; blocking findings for the cap, bait, and pseudo-bold. |
| [`scripts/format_picker.py`](scripts/format_picker.py) | Ranks nine native formats against goal, material, and minutes; refuses camera-less video and decision-less polls. |
| [`scripts/repurpose_splitter.py`](scripts/repurpose_splitter.py) | Splits a source into standalone units, scores them, and skips anything already in the reuse ledger. |

## References and assets

- [`references/hook_and_fold_mechanics.md`](references/hook_and_fold_mechanics.md) — the first 140 characters, and the openers to delete on sight (7 sources)
- [`references/post_formats_canon.md`](references/post_formats_canon.md) — what each native format is good at, and the carousel trap (7 sources)
- [`references/repurposing_discipline.md`](references/repurposing_discipline.md) — standalone units, the reuse ledger, source types and their risks (7 sources)
- [`references/accessibility_and_inclusion.md`](references/accessibility_and_inclusion.md) — pseudo-bold, alt text, captions, and why they are blocking (7 sources)

- [`assets/post_templates.md`](assets/post_templates.md) — five worked post shapes with the hook already doing its job
- [`assets/example_post.md`](assets/example_post.md) — a post that passes the linter, annotated

## Distinct from

- **`linkedin-strategy`** — decides what the posts are about. This writes them.
- **`linkedin-engagement`** — comments and DMs. A comment is a different craft with a
  different budget; it lives there.
- **`marketing-skill/copywriting` / `content-humanizer`** — general copy and de-AI passes.
  Reach for those for tone; this one owns LinkedIn's mechanics and its accessibility floor.

---

**Version:** 1.0.0

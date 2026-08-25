# Profile Worksheet

Fill this in before any rewriting. The auditor and the About builder both read from it.

---

## Presence

- [ ] Photo: face, well lit, recognisable at 48px? ______
- [ ] Banner: custom, or still the default gradient? ______
- [ ] Custom URL set? ______
- [ ] Contact info reachable? ______
- [ ] Open To / Services block set? ______
- [ ] Days since your last post: ______

## Headline (220 characters)

Current: ______________________________________________

- Who is it for (specifically enough to exclude someone)? ______
- What changes because of you? ______
- One piece of proof (number / ex-company / credential)? ______
- Which conventional role or skill term keeps it searchable? ______

First 60 characters — is the strongest segment there? ______

## About (fold at ~265-300 characters)

1. **Hook** — the tension your audience recognises, in their words:

2. **Audience** — who you are for:

3. **Proof** — two or three real results, with numbers:

4. **Approach** — how you work; the part that is yours, not your title's:

5. **CTA** — who should reach out, and what they get:

6. **Keywords** you want to be findable for (work them into real sentences, not a list):

## Current role

Title: ______

Rewrite each bullet as an outcome, not a duty:

| Duty (what it says now) | Outcome (what actually changed) |
|---|---|
| | |
| | |

## Featured

- What is pinned now? ______
- Last updated? ______
- What could a stranger evaluate in 60 seconds? ______

## Recommendations

- Received: ______
- Two people to ask, and the specific project to ask them about:
  1. ______
  2. ______

---

**Then run:**

```bash
python3 ../scripts/profile_completeness_auditor.py --input profile.json --output human
python3 ../scripts/headline_scorer.py --headline "..." --output human
python3 ../scripts/about_section_builder.py --input about.json --output human
```

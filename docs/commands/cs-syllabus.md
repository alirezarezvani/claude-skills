---
title: "/cs-syllabus — Slash Command for AI Coding Agents"
description: "/cs:syllabus <syllabus-file-or-paste> — Generate curated supplementary reading list from any course syllabus. 3-Q grill-me (input format + audience +. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-syllabus

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research/syllabus/commands/cs-syllabus.md">Source</a></span>
</div>


**Command:** `/cs:syllabus <syllabus-file-or-paste>`

The `cs-syllabus` persona produces a `.docx` reading list of recent peer-reviewed research per course section.

## When to Run

- Adding supplementary readings to an existing course
- Updating a syllabus with current research
- Checking what's recent in your field for course planning
- Even casual mentions when a syllabus is attached

## Forcing Intake (3 Questions, One at a Time)

| Q | Asks | Notes |
|---|---|---|
| Q1 | Syllabus input: file path / pasted content / image | refuses missing syllabus |
| Q2 | Course audience: undergrad-intro / undergrad-advanced / grad-masters / grad-doctoral / professional / mixed | drives summary jargon + discussion-question complexity |
| Q3 | Year range: 1 / 2 / 5 years | drives `year_min` on every Consensus search; default 2 |

## What You Get

```
reading_list_<course-slug>_<YYYY-MM-DD>.docx

Structure:
- Title page (course name, subtitle, date)
- Introduction (with Consensus app link)
- Course Learning Outcomes (boxed section)
- Sections (6-12, from grouping):
    Each section = numbered papers, each with:
      - Clickable hyperlinked title
      - Author / journal / year (italic)
      - Summary (plain language, audience-calibrated)
      - Discussion Question (Bloom higher-order, tied to learning outcome)
- Footer (generation metadata)
```

## Grouping Checkpoint (After Phase 2)

After parsing the syllabus, the skill **halts** with a forcing-options prompt:

```
Proposed sections: [list with item counts]. Pick one:
  1. Looks good — proceed with these sections
  2. Merge sections [X] and [Y]
  3. Split section [X] into two
  4. Add a section for [topic]
  5. Remove section [X]
```

This is the last cheap moment to correct course before search budget is consumed. **Refuses to start Phase 3 without explicit user choice.**

## Discipline

- **One intake Q per turn.** Never bundle.
- **Halt at grouping checkpoint.** No Phase 3 without user.
- **Sequential Consensus.** 1 q/sec.
- **Applied-domain weaving** — search "enzyme kinetics food processing" not just "enzyme kinetics". Boosts paper relevance dramatically.
- **Audience-calibrated summaries** — undergrad-intro defines every term; grad-doctoral assumes technical fluency.
- **Bloom higher-order discussion questions** — apply / analyze / evaluate. NOT recall ("what did the authors find?").
- **Source discipline** — only Consensus session results. Training knowledge labeled.
- **Three-count tracking** — sent / received / cited.
- **Bundled JS DOCX generator** — don't inline 300 lines of layout code.

## Quality Bars

### Summary

| ✅ Good | ❌ Bad |
|---|---|
| "This review maps how different diets — Mediterranean, Nordic, vegetarian — reshape the types of fat molecules circulating in your blood, with implications for heart disease risk." | "This paper reviews lipidomic profiles across dietary interventions and their cardiometabolic implications." (Too jargon-heavy) |

### Discussion Question

| ✅ Good | ❌ Bad |
|---|---|
| "If dietary fat quality can reshape your lipoprotein lipidome, what does this suggest about the biochemical basis for dietary guidelines recommending unsaturated over saturated fats?" | "What did the authors find?" (Just recall) |

## Workflow

```bash
# Phase 0 intake (Q1-Q3)
python ../skills/syllabus/scripts/citation_tracker.py --action start --session NAME

# Phase 1 parse (PDF/DOCX/text/image-appropriate reader)
# Phase 2 group + CHECKPOINT (wait for user)
python ../skills/syllabus/scripts/topic_grouper.py --topics-file /tmp/topics.json

# Phase 3 search (sequential Consensus 1 q/sec, applied-domain weaving)
# Phase 4 write summaries + discussion questions
python ../skills/syllabus/scripts/discussion_question_validator.py --questions-file /tmp/qs.json

# Phase 5 generate .docx via bundled script
node ../skills/syllabus/scripts/generate_reading_list.js \
  --input /tmp/data.json \
  --output /path/to/reading_list_<course>_<date>.docx

# Phase 6 deliver
python ../skills/syllabus/scripts/citation_tracker.py --action close --session NAME
```

## Trigger Phrases

- "syllabus reading list"
- "find papers for my course"
- "create a reading list from this syllabus"
- "recent research for my class"
- "supplementary readings"
- "find journal articles for these topics"
- "what recent papers cover this material"
- "any new research on these course topics"
- "update my syllabus with recent papers"
- Casual mentions when syllabus is attached

## Anti-Patterns Rejected

- Parallelizing Consensus calls (rate limit)
- Searching topics without applied-domain angle (poor relevance)
- Padding sections with fabricated entries when Consensus thin
- Generic discussion questions ("What did the authors find?")
- Jargon-heavy summaries unsuitable for course audience
- Skipping group-and-confirm step
- Truncating Consensus URLs in hyperlinks
- Inlining 300 lines of docx-generation JavaScript in skill body

## Related

- Agent: [`cs-syllabus`](https://github.com/alirezarezvani/claude-skills/tree/main/research/syllabus/agents/cs-syllabus.md)
- Skill: [`syllabus`](https://github.com/alirezarezvani/claude-skills/tree/main/research/syllabus/skills/syllabus/SKILL.md)
- Source spec: [`megaprompts/10-syllabus-megaprompt.md`](https://github.com/alirezarezvani/claude-skills/tree/main/megaprompts/10-syllabus-megaprompt.md)
- Siblings: `/cs:litreview`, `/cs:grants`, `/cs:patent`, `/cs:dossier`, `/cs:pulse`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/10-syllabus-megaprompt.md`

---
name: "cs-litreview"
description: "/cs:litreview <research-question> — Academic literature orientation. Grill-me intake (question + framework + depth), free-lane recon (PubMed E-utilities + OpenAlex, keyless; Consensus MCP added only when connected), framework checkpoint, sequential budget-allocated searches (5/10/20), 8-section .docx research guide output. Sibling of /cs:pulse (research pack)."
---

# /cs:litreview — Academic Literature Orientation

**Command:** `/cs:litreview <research question>`

The `cs-litreview` persona produces a strategically planned mini literature review as an 8-section `.docx` research guide.

## When to Run

- Starting research on an unfamiliar field
- Writing a paper that needs grounding in current literature
- Mapping the "lay of the land" before committing to a research direction
- Want a curated reading list with key authors + foundational papers + gaps

## When NOT to Run (search directly)

- Looking for ONE specific paper (just search PubMed/OpenAlex — or Consensus if you use it)
- Quick lookup with no need for synthesis
- Field you already know well and just need a recent papers list

## Forcing Intake (3 Questions, One at a Time)

| Q | Asks | Default if forcing-choice |
|---|---|---|
| Q1 | Research question (1-2 sentences, specific) | refuses vague; "AI in medicine" gets pushed back once |
| Q2 | Framework: PICO / SPIDER / Decomposition / Hybrid / You-pick | "you pick" (skill recommends from Q1) |
| Q3 | Tentative depth: Quick (5) / Standard (10) / Deep (20) | re-confirmed at post-Phase-2 checkpoint |

## What You Get

After Phase 0 intake + Phase 1 recon + Phase 2 framework + interactive checkpoint + Phase 3 searches:

**`research_guide_<topic>_<date>.docx`** with 8 sections:

1. **Topic Overview** — single tight paragraph
2. **Start Here — Priority Reading Order** — 5-7 hyperlinked papers (best-review → foundational → frontier → gap)
3. **How the Field Got Here** — chronological narrative + timeline table
4. **Sub-area Guides** — one per sub-area (4 parts each: synthesis / key papers / search terms / boolean strings)
5. **Key Research Groups** — top 3-5 authors/groups with representative papers
6. **Open Questions & Gaps** — methodological / population / conceptual
7. **Bibliography** — alphabetical, hyperlinked, every inline citation matches
8. **Audit Log** — search table + counts + search lane used (free / free+Consensus)

## Interactive Checkpoint (Mid-Run)

After Phase 2 (framework selected, sub-areas generated), the skill **halts** with a forcing-options prompt:

```
Framework breakdown:
| {Component} | How it maps to your topic | Proposed sub-area |
|---|---|---|
| Population | ... | Sub-area 1: ... |
| Intervention | ... | Sub-area 2: ... |
| Comparison | ... | Sub-area 3: ... |
| Outcome | ... | Sub-area 4: ... |
| Cross-cutting | ... | Sub-area 5: ... |

Confirm depth (search lane: free — PubMed + OpenAlex, ~20 results per query per source):
  1. Quick scan (5 searches)
  2. Standard review (10 searches)
  3. Deep dive (20 searches)

Sub-area options:
  - Looks good — proceed
  - Adjust: add sub-area on [X]
  - Adjust: replace [Y] with [Z]
  - Restart with different framework
```

This is the **last cheap moment** to correct course before search budget is consumed. Skill refuses to start Phase 3 without explicit user choice.

## Discipline (Research-Pack Convention)

- **One intake question per turn.** Never bundle.
- **Sequential search calls.** 1 q/sec rate limit. NEVER parallelize (any lane).
- **Lane check at session start** — if the Consensus MCP tools are not available, use the free lane; do not attempt tier detection. Lane reported at checkpoint.
- **Halt at checkpoint.** No Phase 3 without confirmation.
- **Source discipline** — cite only THIS session's search results. Training knowledge labeled `[Not from search]`.
- **Three-count tracking** — searches / unique papers / cited.
- **Retry once after 3s** — then log. 3 consecutive failures → stop.

## Workflow

```bash
# Phase 0 intake (Q1-Q3 one at a time)
python ../skills/litreview/scripts/citation_tracker.py --action start --session NAME
python ../skills/litreview/scripts/framework_recommender.py --question "<Q1>"

# Phase 1 recon (1 free-lane search; record sent + received; add Consensus if connected)
python ../skills/litreview/scripts/free_search.py --query "<broad Q1>" --source both --max 20
# Phase 2 framework + sub-area generation
# CHECKPOINT — wait for user

# Phase 3 searches (sequential, 1 q/sec, budget per tier):
#   5/10/20 searches across sub-areas + review + era-gated + follow-up

# Phase 4 cross-search aggregation + DOCX
python ../skills/litreview/scripts/cross_search_aggregator.py --session NAME
# Generate DOCX via Node.js docx library
python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).testzip()" output.docx  # zip-integrity check; then confirm required sections present

python ../skills/litreview/scripts/citation_tracker.py --action close --session NAME
```

## Trigger Phrases (auto-invoke without /cs:)

- "litreview on [topic]"
- "literature review on [topic]"
- "I'm starting a literature review on X"
- "I'm writing a paper on X"
- "help me research X"
- "I'm doing research on X"
- "can you help me research X"

**Do NOT trigger for:** single one-off paper searches — that's a plain PubMed/OpenAlex (or Consensus) query.

## Anti-Patterns Rejected

- Parallelizing search calls (any lane)
- Skipping the interactive checkpoint
- Padding thin results with training knowledge
- Defaulting to non-PICO without justification
- Citing papers in chat that didn't come from this session's searches
- Attempting Consensus plan-tier detection (deleted — the only check is whether the Consensus MCP tools are available)
- Treating Consensus as required (free lane is the default)
- Skipping era-gated searches in standard/deep budgets
- Skipping cross-search intelligence (repeat-hits, recurring authors)
- Truncating source URLs

## Related

- Agent: [`cs-litreview`](../agents/cs-litreview.md)
- Skill: [`litreview`](../skills/litreview/SKILL.md)
- Source spec: [`megaprompts/09-litreview-megaprompt.md`](../../../megaprompts/09-litreview-megaprompt.md)
- Sibling: `/cs:pulse` (research pack)
- Future siblings: `/cs:grants`, `/cs:patent`, `/cs:dossier`, `/cs:syllabus`

---

**Version:** 1.0.0
**Source:** Path-B direct conversion of `megaprompts/09-litreview-megaprompt.md`

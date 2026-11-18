---
name: source-audit
description: "Use before publishing a draft that cites links: verify that each claim is actually supported by the source it points to, link by link. Triggers include 审稿、核查信源、发布前检查、fact-check、这篇能不能发、里面说的对不对, or any review of an article, tool roundup, comparison, or review post with citations. Produces per-claim verdicts (supported, partial, contradicted, not found, unreachable) with quoted evidence. Not for copy-editing, structure review, or research from scratch."
license: MIT
metadata:
  version: 1.0.0
  author: zhengqiuyang
  category: marketing
  updated: 2026-11-18
---

# Source Audit

Audit a finished draft before it is published: for every cited link, does the source actually support the claim the draft makes next to it?

Do only this. Typos, style, structure, and "AI tone" belong to other skills. Mixing them into an audit hides the one failure mode that matters: **a claim the source never made**.

## Before Starting

Ask only what the draft cannot answer:

1. **Draft path** — the Markdown file to audit.
2. **Publish target** — blog, newsletter, docs, or social long-form. It sets how strict the verdict should be.
3. **Scope** — full audit, or only the links the author flags as risky.

If a link cannot be opened from this environment, say so up front and plan to mark it `unreachable` rather than guessing.

## How This Skill Works

### Mode 1: Full Audit (default)

Run the full workflow: extract links, fetch sources, compare each claim, write the report.

### Mode 2: Risk-First Audit

Use when the draft is long or time is short. Audit only links that carry checkable facts (versions, prices, licenses, platform support, feature lists). Skip opinion links and list what was skipped.

### Mode 3: Single-Link Check

Use when the author asks "is this one link saying what I think it says?" Return one verdict and its quote, not a report.

## Core Workflow

### Step 1: Extract links and context

```bash
python3 scripts/extract_claims.py draft.md --json -o claims.json
```

The script writes JSON (never redirect stdout on Windows; it can corrupt UTF-8). Each item has `url`, `link_text`, and the paragraph `context`.

If `link_count` is 0 but links are visible, run `python3 scripts/extract_claims.py --sample` to confirm the extractor works before continuing.

Then read every context and list the **checkable claims** it makes: platform support, version numbers, dependencies, feature lists, prices, dates, licenses. Opinions ("fast", "clean UI") are not checkable; mark them `opinion` and skip them.

A claim may span paragraphs. Read one paragraph up when context is thin, but never attribute the whole article to one link.

### Step 2: Fetch each source

Fetch every link. Never decide from a search snippet or memory of the project; projects change.

- **GitHub repo** — fetch `https://raw.githubusercontent.com/<owner>/<repo>/<default-branch>/README.md`. For licenses, platforms, or files the README omits, check the relevant file or GitHub API metadata.
- **Web page** — fetch the page body. Use the available web reader first, then a plain fetch.
- **Failure** — retry once with another tool. If it still fails, mark `unreachable` and name the failure. Never issue a verdict on an unreachable source.

### Step 3: Compare claim by claim

Every verdict needs a quoted passage that locates the evidence ("README lists Windows 10 2004+", not "the README mentions platforms").

| Verdict | Meaning |
|---|---|
| `supported` | The source explicitly backs every key part of the claim. |
| `partial` | The source backs part of it, or the wording is too vague to confirm. |
| `contradicted` | The source explicitly says something incompatible. |
| `not-found` | The specific fact is absent from the source. Absence is not denial. |
| `unreachable` | Fetch failed after a retry. |
| `opinion` | Subjective statement; not audited. |

`not-found` and `contradicted` are different. The most common defect in roundups is not a wrong statement but a statement the source never made. Mark it `not-found`; upgrade to `contradicted` only when the source says the opposite.

### Step 4: Write the report

Write `<draft>-audit.md` and give a summary table in the reply. Use the template in [references/verdict-examples.md](references/verdict-examples.md) for tone and evidence density.

## Decision Rules

Use these rules when a claim sits between two verdicts:

- **One claim, several links.** Give the claim the verdict of the strongest cited source, and name the weaker ones in the fix list.
- **A claim that combines facts.** If "supports Windows and Linux" is backed for Windows only, the verdict is `partial`, not `supported`.
- **A fact that moved.** Prices, version numbers, and licenses change. Quote the page as fetched and record the date; do not compare against memory.
- **A source that is a summary of another source.** Fetch the original when the claim is specific; a summary is `partial` evidence at best.
- **Marketing copy as a source.** A vendor's own claim is evidence of what the vendor says, not of what is true. Say which one the draft needs.

## Worked Example

Draft: "Acme CLI supports Windows, macOS and Linux, and is Apache-2.0."

| Claim | Source | Evidence | Verdict |
|---|---|---|---|
| supports Windows, macOS and Linux | repo README | "Windows 10 2004+, macOS 12+, Ubuntu 22.04+" | supported |
| Apache-2.0 | repository LICENSE | "Apache License, Version 2.0" | supported |

Draft: "Acme CLI runs on 40 languages."

| Claim | Source | Evidence | Verdict |
|---|---|---|---|
| 40 languages | repo README | no language section found | not-found |

The second table is the common case: the number is not contradicted, it is simply unsourced. The fix is to remove it or cite a page that states it.

## Quality Bar

Before writing the report, confirm:

- every `supported` and `contradicted` verdict has a quote;
- every `not-found` names what was searched for;
- every `unreachable` names the failure (status code or timeout);
- opinion claims are listed as skipped, not silently removed;
- the fix list is specific enough to apply without re-reading the audit.

## Proactive Triggers

- A draft makes a numeric claim (version, price, date, count) next to a link.
- A link points to a repository README but the claim is about a license or platform.
- Two links in the same paragraph support different claims.
- A "comparison" table cites one source for several vendors.
- A quote appears alongside a link but cannot be found in that source.

## Output Artifacts

- `<draft>-audit.md` with counts, per-claim verdicts, evidence quotes, and a fix list.
- A short reply table: claim, verdict, evidence, action.
- A list of sources that could not be fetched, with the failure mode.
- A list of claims deliberately skipped as opinion.

## Anti-Patterns

- **Verdict without a quote.** If you cannot quote it, you have not checked it.
- **Treating absence as contradiction.** `not-found` is not `contradicted`.
- **Auditing the whole article against one link.** Each claim gets the source it cites.
- **Judging from memory or search snippets.** Fetch the page.
- **Fixing the draft without being asked.** The deliverable is a report; edits come after.
- **Copy-editing inside the audit.** Style issues dilute the evidence.

## Related Skills

- `research-summarizer` — use when the task starts from sources and produces a summary; do not use for auditing a finished draft.
- `meta-research` — use when the question is "is this hypothesis true"; do not use for per-link verification.
- `deepread` — use when learning from a long document; do not use for publish-time checks.
- `copywriting` / `md-review` — use after the audit to improve wording and structure.

## Cross-References

- Verdict definitions, report template, and worked examples: [references/verdict-examples.md](references/verdict-examples.md)
- Extractor CLI and exit codes: [scripts/extract_claims.py](scripts/extract_claims.py)

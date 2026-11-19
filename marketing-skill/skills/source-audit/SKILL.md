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

Do only this. Typos, style, structure and tone belong to other skills; mixing them in hides the one failure that matters, **a claim the source never made**.

## Before Starting

Ask only what the draft cannot answer: the **draft path**, the **publish target** (blog, newsletter, docs, social long-form; it sets how strict to be) and the **scope** (full audit, or only links the author flags). If a link cannot be opened from this environment, say so up front and plan to mark it `unreachable`.

## Modes

- **Full audit** (default): extract, fetch, compare, write the report.
- **Risk-first**: only links that carry checkable facts (versions, prices, licenses, platform support, feature lists); list what was skipped.
- **Single link**: one verdict and its quote, no report.

## Workflow

1. **Extract links and context.**
   ```bash
   python3 scripts/extract_claims.py draft.md --json -o claims.json
   ```
   Each item has `url`, `link_text` and the paragraph `context`. If `link_count` is 0 but links are visible, run `--sample` to confirm the extractor works. List the checkable claims per context; mark subjective ones `opinion`. Read one paragraph up when context is thin, but never attribute the whole article to one link.
2. **Fetch every source.** Never decide from a search snippet or memory; projects change. Fetch rules per source type are in [references/verdict-examples.md](references/verdict-examples.md#fetching-sources). Never issue a verdict on an unreachable source.
3. **Compare claim by claim.** Every verdict needs a quoted passage that locates the evidence.

   | Verdict | Meaning |
   |---|---|
   | `supported` | The source explicitly backs every key part of the claim. |
   | `partial` | The source backs part of it, or the wording is too vague to confirm. |
   | `contradicted` | The source explicitly says something incompatible. |
   | `not-found` | The fact is absent from the source. Absence is not denial. |
   | `unreachable` | Fetch failed after a retry. |
   | `opinion` | Subjective; not audited. |

   Borderline cases (several links, combined facts, moved facts, summaries, vendor copy) follow the decision rules in the reference.
4. **Write the report** to `<draft>-audit.md` using the reference template, and give a summary table in the reply.

## Example

Draft: "Acme CLI supports Windows, macOS and Linux, and runs on 40 languages."

| Claim | Source | Evidence | Verdict |
|---|---|---|---|
| Windows, macOS and Linux | repo README | "Windows 10 2004+, macOS 12+, Ubuntu 22.04+" | supported |
| 40 languages | repo README | no language section found | not-found |

The second row is the common defect: not wrong, simply unsourced. Fix it by removing the number or citing a page that states it.

## Quality Bar

- every `supported` and `contradicted` verdict has a quote;
- every `not-found` names what was searched for;
- every `unreachable` names the failure (status code or timeout);
- opinion claims are listed as skipped, not silently removed;
- the fix list can be applied without re-reading the audit.

## Anti-Patterns

- A verdict without a quote, or judged from memory or a search snippet.
- Treating absence as contradiction.
- Auditing the whole article against one link.
- Editing the draft or copy-editing inside the audit; the deliverable is a report.

## Related Skills

- `research-summarizer`: starts from sources and summarises; not for auditing a finished draft.
- `meta-research`: tests whether a hypothesis is true; not per-link verification.
- `copywriting` / `md-review`: use after the audit for wording and structure.

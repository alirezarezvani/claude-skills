# Verdict Examples and Report Template

## Report template

```md
# Source audit: <draft title>

## Summary

N links / M claims: supported a · partial b · contradicted c · not-found d · unreachable e · opinion f

| # | Claim | Source | Verdict | Evidence |
|---|---|---|---|---|
| 1 | "supports Windows 10 2004+" | repo README | supported | "Windows 10 2004 or later" |
| 2 | "MIT licensed" | repo | not-found | no license section in README |

## Details

### 1. <claim>

- Draft: "<sentence>"
- Source: <url> (fetched <date>)
- Evidence: "<quoted passage>"
- Verdict: supported | partial | contradicted | not-found | unreachable | opinion
- Action: keep | soften to "<new wording>" | replace source | drop the claim

## Fix list

1. <one line per change>

## Not audited

- <opinion claims, unreachable sources>
```

## Worked verdicts

**supported** — draft: "Acme CLI is MIT licensed." Source: repository `LICENSE` file says "MIT License". Verdict: `supported`, quote the license line.

**partial** — draft: "runs on Windows, macOS and Linux." Source lists Windows and macOS only. Verdict: `partial`; the claim overstates the source. Action: name only the platforms the source lists.

**contradicted** — draft: "requires Python 3.12+." Source says "Python 3.10 or newer." Verdict: `contradicted`; quote both lines.

**not-found** — draft: "supports 40 languages." Source README has no language section. Verdict: `not-found`; absence is not denial. Action: replace the number with a sourced one, or drop it.

**unreachable** — link returns 403 after two attempts. Verdict: `unreachable`; report the status code and do not judge the claim.

**opinion** — draft: "the fastest tool in its class." No source can settle it. Verdict: `opinion`; skip, and note that it is unsourced.

## Tone rules

- Quote the smallest passage that proves the point.
- One verdict per claim; do not merge unrelated claims.
- Name the fetch date for time-sensitive facts (prices, versions, licenses).
- Never invent a quote to make a verdict look stronger.

## Decision rules for borderline claims

- **One claim, several links.** Give the claim the verdict of the strongest cited source, and name the weaker ones in the fix list.
- **A claim that combines facts.** If "supports Windows and Linux" is backed for Windows only, the verdict is `partial`, not `supported`.
- **A fact that moved.** Prices, version numbers and licenses change. Quote the page as fetched and record the date; do not compare against memory.
- **A source that summarises another source.** Fetch the original when the claim is specific; a summary is `partial` evidence at best.
- **Marketing copy as a source.** A vendor's own claim is evidence of what the vendor says, not of what is true. Say which one the draft needs.

## Proactive triggers

- A draft makes a numeric claim (version, price, date, count) next to a link.
- A link points to a repository README but the claim is about a license or platform.
- Two links in the same paragraph support different claims.
- A comparison table cites one source for several vendors.
- A quote appears next to a link but cannot be found in that source.

## Fetching sources

- **GitHub repo**: fetch `https://raw.githubusercontent.com/<owner>/<repo>/<default-branch>/README.md`. For licenses, platforms or files the README omits, check the relevant file or the repository metadata.
- **Web page**: fetch the page body with the available web reader, then a plain fetch.
- **Failure**: retry once with another tool. If it still fails, mark `unreachable` and name the failure (status code or timeout).

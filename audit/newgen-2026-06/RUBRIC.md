# New-Generation Model Optimization Rubric (v1)

Audit date: 2026-06-10 · Branch: `claude/skills-plugins-audit-vrttx1`

This rubric defines what "optimized for new-generation models" means for every artifact
type in this repository. New-gen frontier models (Claude Fable/Opus 4.x class) differ from
the models many of these skills were written for: they need **less hand-holding, more
context economy, and machine-checkable verification**. A skill earns its context window
or it gets cut.

## A. SKILL.md — 7 dimensions

| # | Dimension | What PASS looks like |
|---|-----------|----------------------|
| A1 | **Trigger quality** | Frontmatter `description` states what the skill does AND when to fire, in third person, < 1024 chars, with concrete trigger phrases ("Use when…", example user requests). Never just the skill name. |
| A2 | **Context economy** | Body is instruction-dense. Progressive disclosure: SKILL.md holds the workflow + decision rules; deep knowledge lives in `references/` and is loaded on demand. No "You are an expert…" filler, no restating what a frontier model already knows (generic advice = dead weight). |
| A3 | **Tool wiring** | Every referenced script exists, has exact CLI invocations in SKILL.md, and its output is consumed by a named next step. No orphan scripts, no phantom paths. |
| A4 | **Verification loop** | The workflow ends with a check the model can execute: run a script and assert exit code/output shape, validate against an explicit checklist, or hit a refusal gate. Skills without one get a *proposed* custom loop in this audit. |
| A5 | **Real-world expertise** | A practitioner would recognize domain mastery: named frameworks with thresholds, formulas, regulatory citations, decision trees — not "communicate clearly with stakeholders". |
| A6 | **Freshness** | No stale model names (claude-3-x, GPT-3.5-era), dead prices, or 2024-isms presented as current. |
| A7 | **No filler files** | Every file in the package earns its place. References cite sources and say something non-obvious. Assets are usable, not shells. No duplicated boilerplate. |

Verdicts: **KEEP** (ship as is) · **OPTIMIZE** (targeted edits, listed) · **REWRITE** (structure salvageable, content not) · **CUT-OR-MERGE** (does not earn its context).

## B. Agents (`agents/*.md`)

- B1 Frontmatter: `name`, `description` with trigger phrasing ("Use when…" / "Use PROACTIVELY…"), minimal `tools` list.
- B2 Differentiation: the system prompt could not be swapped with a sibling agent's without someone noticing. Personas must change behavior, not adjectives.
- B3 No placeholder/boilerplate body.

## C. Slash commands (`commands/*.md`)

- C1 Frontmatter description present and accurate.
- C2 `$ARGUMENTS` / argument-hint handled.
- C3 The command does something a bare prompt could not (orchestrates tools, enforces gates). Otherwise: candidate for merge or cut.

## D. Scripts (`scripts/*.py`)

- D1 `--help` exits 0 (verified repo-wide this audit: 583/593 pass).
- D2 Stdlib-only, no LLM calls, deterministic.
- D3 Output is machine-parseable where a workflow consumes it (JSON mode).
- D4 By-design exceptions (hooks reading stdin, fixed-contract evaluators) documented where they live.

## E. Plugins (`.claude-plugin/plugin.json`)

- E1 Schema valid (verified repo-wide: all pass `check_plugin_json.py --all`).
- E2 Description matches actual contents (pod/skill counts drift).
- E3 Version coherent with marketplace.json.

## Custom verification criteria — the contract

For **every skill** audited, the domain report includes 2–4 *executable* "definition of
done" checks specific to that skill (e.g. "`python3 scripts/x.py --sample` exits 0 and
emits JSON with keys `verdict`, `score`; verdict ∈ {GO, NO-GO}"). These are the
guardrails future optimization PRs must keep green.

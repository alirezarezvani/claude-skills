---
name: prompt-engineer-toolkit
description: "When the user wants to improve prompts for AI-assisted marketing, build prompt templates, or optimize AI content workflows. Also use when the user mentions 'prompt engineering,' 'improve my prompts,' 'AI writing quality,' 'prompt templates,' or 'AI content workflow.'"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# Prompt Engineer Toolkit

**Tier:** POWERFUL  
**Category:** Marketing Skill / AI Operations  
**Domain:** Prompt Engineering, LLM Optimization, AI Workflows

## Overview

Use this skill to move prompts from ad-hoc drafts to production assets with repeatable testing, versioning, and regression safety. It emphasizes measurable quality over intuition.

## Core Capabilities

- A/B prompt evaluation against structured test cases
- Quantitative scoring for adherence, relevance, and safety checks
- Prompt version tracking with immutable history and changelog
- Prompt diffs to review behavior-impacting edits
- Reusable prompt templates and selection guidance
- Regression-friendly workflows for model/prompt updates

## When to Use

- You are launching a new LLM feature and need reliable outputs
- Prompt quality degrades after model or instruction changes
- Multiple team members edit prompts and need history/diffs
- You need evidence-based prompt choice for production rollout
- You want consistent prompt governance across environments

## Key Workflows

### 1. Run Prompt A/B Test

Prepare JSON test cases and run:

```bash
python3 scripts/prompt_tester.py \
  --prompt-a-file prompts/a.txt \
  --prompt-b-file prompts/b.txt \
  --cases-file testcases.json \
  --runner-cmd 'my-llm-cli --prompt {prompt} --input {input}' \
  --format text
```

Input can also come from stdin/`--input` JSON payload.

### 2. Choose Winner With Evidence

The tester scores outputs per case and aggregates:

- expected content coverage
- forbidden content violations
- regex/format compliance
- output length sanity

Use the higher-scoring prompt as candidate baseline, then run regression suite.

### 3. Version Prompts

```bash
# Add version
python3 scripts/prompt_versioner.py add \
  --name support_classifier \
  --prompt-file prompts/support_v3.txt \
  --author alice

# Diff versions
python3 scripts/prompt_versioner.py diff --name support_classifier --from-version 2 --to-version 3

# Changelog
python3 scripts/prompt_versioner.py changelog --name support_classifier
```

### 4. Regression Loop

1. Store baseline version.
2. Propose prompt edits.
3. Re-run A/B test.
4. Promote only if score and safety constraints improve.

## Script Interfaces

- `python3 scripts/prompt_tester.py --help`
  - Reads prompts/cases from stdin or `--input`
  - Optional external runner command
  - Emits text or JSON metrics
- `python3 scripts/prompt_versioner.py --help`
  - Manages prompt history (`add`, `list`, `diff`, `changelog`)
  - Stores metadata and content snapshots locally

## Common Pitfalls

1. Picking prompts by anecdotal single-case outputs
2. Changing prompt + model simultaneously without control group
3. Missing forbidden-content checks in evaluation criteria
4. Editing prompts without version metadata or rationale
5. Failing to diff semantic changes before deploy

## Best Practices

1. Keep test cases realistic and edge-case rich.
2. Always include negative checks (`must_not_contain`).
3. Store prompt versions with author and change reason.
4. Run A/B tests before and after major model upgrades.
5. Separate reusable templates from production prompt instances.
6. Maintain a small golden regression suite for every critical prompt.

## References

- [references/prompt-templates.md](references/prompt-templates.md)
- [references/technique-guide.md](references/technique-guide.md)
- [references/evaluation-rubric.md](references/evaluation-rubric.md)
- [README.md](README.md)

## Evaluation Design

Each test case should define:

- `input`: realistic production-like input
- `expected_contains`: required markers/content
- `forbidden_contains`: disallowed phrases or unsafe content
- `expected_regex`: required structural patterns

This enables deterministic grading across prompt variants.

## Versioning Policy

- Use semantic prompt identifiers per feature (`support_classifier`, `ad_copy_shortform`).
- Record author + change note for every revision.
- Never overwrite historical versions.
- Diff before promoting a new prompt to production.

## Rollout Strategy

1. Create baseline prompt version.
2. Propose candidate prompt.
3. Run A/B suite against same cases.
4. Promote only if winner improves average and keeps violation count at zero.
5. Track post-release feedback and feed new failure cases back into test suite.

## Prompt Review Checklist

1. Task intent is explicit and unambiguous.
2. Output schema/format is explicit.
3. Safety and exclusion constraints are explicit.
4. Prompt avoids contradictory instructions.
5. Prompt avoids unnecessary verbosity tokens.

## Common Operational Risks

- Evaluating with too few test cases (false confidence)
- Optimizing for one benchmark while harming edge cases
- Missing audit trail for prompt edits in multi-author teams
- Model swap without rerunning baseline A/B suite

## Proactive Triggers

- **AI output sounds generic** → Prompts lack brand voice context. Include voice guidelines.
- **Inconsistent output quality** → Prompts too vague. Add specific examples and constraints.
- **No quality checks on AI content** → AI output needs human review. Never publish without editing.
- **Same prompt style for all tasks** → Different tasks need different prompt structures.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "Improve my prompts" | Prompt audit with specific rewrites for better output |
| "Prompt templates" | Task-specific prompt templates for marketing use cases |
| "AI content workflow" | End-to-end AI-assisted content production workflow |

## Communication

All output passes quality verification:
- Self-verify: source attribution, assumption audit, confidence scoring
- Output format: Bottom Line → What (with confidence) → Why → How to Act
- Results only. Every finding tagged: 🟢 verified, 🟡 medium, 🔴 assumed.

## Related Skills

- **content-production**: For the full content pipeline. Prompt engineering supports AI-assisted writing.
- **ad-creative**: For generating ad variations using prompt techniques.
- **content-humanizer**: For refining AI-generated output to sound natural.
- **marketing-context**: Provides brand context that improves prompt outputs.

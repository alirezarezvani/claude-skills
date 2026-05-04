---
Name: product-init
Tier: STANDARD
Category: product
Dependencies: python3
Author: mturac
Version: 2.1.0
name: product-init
description: |
  AI-first turnkey product delivery pipeline. One command, 9 hard-gated stages,
  a shipped product at the end. Validates problem-market fit before writing a single
  line of code. CRITICAL findings block the pipeline — no --skip flag.
  Works on Claude Code, Codex CLI, and OpenClaw/Hermes.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
metadata:
  license: MIT
  tags:
    - product-management
    - developer-tools
    - ai
    - shipping
    - pmf
    - validation
---

# product-init — AI-First Product Delivery Pipeline

> "AI sets the goal. product-init makes sure you're shooting at the right one."

43% of startups fail from "no market need" — not bad code. This skill puts 9 hard gates
between your idea and your deploy.

## Install

```bash
curl -sSL https://raw.githubusercontent.com/mturac/product-init/main/install.sh | bash
```

Auto-detects your runtime (Claude Code, Codex CLI, OpenClaw). No env vars needed.

## Usage

```
/product-init "build an HR assessment tool"
```

Three questions. AI drafts the rest. 9 gates run in sequence.

## The 9 Gates

| Gate | Name | Blocks on |
|------|------|-----------|
| 1 | Discovery Constitution | JTBD undefined, kill criteria missing |
| 2 | Statement of Work | Appetite not set, PR-FAQ not signed |
| 3 | Design | Screen not mapped to Gate 1 job |
| 4 | Build | Orphan TODOs, commit not AC-linked |
| 5 | QA | Unit / integration / E2E not all green |
| 6 | UAT | No human sign-off on real URL |
| 7 | Deploy | No HTTP 200 to prod, no rollback drill |
| 8 | Handoff | No runbook, no DEBT.md |
| 9 | Warranty | 72h monitoring window not passed |

## Research Basis

| Source | Applied at |
|--------|-----------|
| CB Insights 2024 (43% PMF failure) | Gate 1 hard block |
| Christensen JTBD | Gate 1 questions |
| Cagan four-risk model | Gate 1 risk audit |
| Basecamp Shape Up | Gate 2 appetite |
| Amazon PR-FAQ | Gate 2 narrative |

## Source

github.com/mturac/product-init

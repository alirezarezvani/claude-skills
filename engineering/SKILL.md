---
name: "engineering-advanced-skills"
description: "25 advanced POWERFUL-tier engineering skills covering agent design, RAG architecture, MCP servers, CI/CD pipelines, database design, observability, security auditing, release management, and platform operations. Works with Claude Code, Codex CLI, and OpenClaw."
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - engineering
  - architecture
  - agents
  - rag
  - mcp
  - ci-cd
  - observability
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Engineering Advanced Skills (POWERFUL Tier)

25 advanced engineering skills for complex architecture, automation, and platform operations.

## Quick Start

### Claude Code
```
/read engineering/agent-designer/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/engineering
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Agent Designer | `agent-designer/` | Multi-agent architecture patterns |
| Agent Workflow Designer | `agent-workflow-designer/` | Workflow orchestration |
| API Design Reviewer | `api-design-reviewer/` | REST/GraphQL linting, breaking changes |
| API Test Suite Builder | `api-test-suite-builder/` | API test generation |
| Changelog Generator | `changelog-generator/` | Automated changelogs |
| CI/CD Pipeline Builder | `ci-cd-pipeline-builder/` | Pipeline generation |
| Codebase Onboarding | `codebase-onboarding/` | New dev onboarding guides |
| Database Designer | `database-designer/` | Schema design, migrations |
| Database Schema Designer | `database-schema-designer/` | ERD, normalization |
| Dependency Auditor | `dependency-auditor/` | Dependency security scanning |
| Env Secrets Manager | `env-secrets-manager/` | Secrets rotation, vault |
| Git Worktree Manager | `git-worktree-manager/` | Parallel branch workflows |
| Interview System Designer | `interview-system-designer/` | Hiring pipeline design |
| MCP Server Builder | `mcp-server-builder/` | MCP tool creation |
| Migration Architect | `migration-architect/` | System migration planning |
| Monorepo Navigator | `monorepo-navigator/` | Monorepo tooling |
| Observability Designer | `observability-designer/` | SLOs, alerts, dashboards |
| Performance Profiler | `performance-profiler/` | CPU, memory, load profiling |
| PR Review Expert | `pr-review-expert/` | Pull request analysis |
| RAG Architect | `rag-architect/` | RAG system design |
| Release Manager | `release-manager/` | Release orchestration |
| Runbook Generator | `runbook-generator/` | Operational runbooks |
| Skill Security Auditor | `skill-security-auditor/` | Skill vulnerability scanning |
| Skill Tester | `skill-tester/` | Skill quality evaluation |
| Tech Debt Tracker | `tech-debt-tracker/` | Technical debt management |

## Rules

- Load only the specific skill SKILL.md you need
- These are advanced skills — combine with engineering-team/ core skills as needed

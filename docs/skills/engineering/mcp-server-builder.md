---
title: "MCP Server Builder"
description: "MCP Server Builder - Claude Code skill from the Engineering - POWERFUL domain."
---

# MCP Server Builder

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `mcp-server-builder`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/mcp-server-builder/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** AI / API Integration

## Overview

Use this skill to design and ship production-ready MCP servers from API contracts instead of hand-written one-off tool wrappers. It focuses on fast scaffolding, schema quality, validation, and safe evolution.

The workflow supports both Python and TypeScript MCP implementations and treats OpenAPI as the source of truth.

## Core Capabilities

- Convert OpenAPI paths/operations into MCP tool definitions
- Generate starter server scaffolds (Python or TypeScript)
- Enforce naming, descriptions, and schema consistency
- Validate MCP tool manifests for common production failures
- Apply versioning and backward-compatibility checks
- Separate transport/runtime decisions from tool contract design

## When to Use

- You need to expose an internal/external REST API to an LLM agent
- You are replacing brittle browser automation with typed tools
- You want one MCP server shared across teams and assistants
- You need repeatable quality checks before publishing MCP tools
- You want to bootstrap an MCP server from existing OpenAPI specs

## Key Workflows

### 1. OpenAPI to MCP Scaffold

1. Start from a valid OpenAPI spec.
2. Generate tool manifest + starter server code.
3. Review naming and auth strategy.
4. Add endpoint-specific runtime logic.

```bash
python3 scripts/openapi_to_mcp.py \
  --input openapi.json \
  --server-name billing-mcp \
  --language python \
  --output-dir ./out \
  --format text
```

Supports stdin as well:

```bash
cat openapi.json | python3 scripts/openapi_to_mcp.py --server-name billing-mcp --language typescript
```

### 2. Validate MCP Tool Definitions

Run validator before integration tests:

```bash
python3 scripts/mcp_validator.py --input out/tool_manifest.json --strict --format text
```

Checks include duplicate names, invalid schema shape, missing descriptions, empty required fields, and naming hygiene.

### 3. Runtime Selection

- Choose **Python** for fast iteration and data-heavy backends.
- Choose **TypeScript** for unified JS stacks and tighter frontend/backend contract reuse.
- Keep tool contracts stable even if transport/runtime changes.

### 4. Auth & Safety Design

- Keep secrets in env, not in tool schemas.
- Prefer explicit allowlists for outbound hosts.
- Return structured errors (`code`, `message`, `details`) for agent recovery.
- Avoid destructive operations without explicit confirmation inputs.

### 5. Versioning Strategy

- Additive fields only for non-breaking updates.
- Never rename tool names in-place.
- Introduce new tool IDs for breaking behavior changes.
- Maintain changelog of tool contracts per release.

## Script Interfaces

- `python3 scripts/openapi_to_mcp.py --help`
  - Reads OpenAPI from stdin or `--input`
  - Produces manifest + server scaffold
  - Emits JSON summary or text report
- `python3 scripts/mcp_validator.py --help`
  - Validates manifests and optional runtime config
  - Returns non-zero exit in strict mode when errors exist

## Common Pitfalls

1. Tool names derived directly from raw paths (`get__v1__users___id`)
2. Missing operation descriptions (agents choose tools poorly)
3. Ambiguous parameter schemas with no required fields
4. Mixing transport errors and domain errors in one opaque message
5. Building tool contracts that expose secret values
6. Breaking clients by changing schema keys without versioning

## Best Practices

1. Use `operationId` as canonical tool name when available.
2. Keep one task intent per tool; avoid mega-tools.
3. Add concise descriptions with action verbs.
4. Validate contracts in CI using strict mode.
5. Keep generated scaffold committed, then customize incrementally.
6. Pair contract changes with changelog entries.

## Reference Material

- [references/openapi-extraction-guide.md](references/openapi-extraction-guide.md)
- [references/python-server-template.md](references/python-server-template.md)
- [references/typescript-server-template.md](references/typescript-server-template.md)
- [references/validation-checklist.md](references/validation-checklist.md)
- [README.md](README.md)

## Architecture Decisions

Choose the server approach per constraint:

- Python runtime: faster iteration, data pipelines, backend-heavy teams
- TypeScript runtime: shared types with JS stack, frontend-heavy teams
- Single MCP server: easiest operations, broader blast radius
- Split domain servers: cleaner ownership and safer change boundaries

## Contract Quality Gates

Before publishing a manifest:

1. Every tool has clear verb-first name.
2. Every tool description explains intent and expected result.
3. Every required field is explicitly typed.
4. Destructive actions include confirmation parameters.
5. Error payload format is consistent across all tools.
6. Validator returns zero errors in strict mode.

## Testing Strategy

- Unit: validate transformation from OpenAPI operation to MCP tool schema.
- Contract: snapshot `tool_manifest.json` and review diffs in PR.
- Integration: call generated tool handlers against staging API.
- Resilience: simulate 4xx/5xx upstream errors and verify structured responses.

## Deployment Practices

- Pin MCP runtime dependencies per environment.
- Roll out server updates behind versioned endpoint/process.
- Keep backward compatibility for one release window minimum.
- Add changelog notes for new/removed/changed tool contracts.

## Security Controls

- Keep outbound host allowlist explicit.
- Do not proxy arbitrary URLs from user-provided input.
- Redact secrets and auth headers from logs.
- Rate-limit high-cost tools and add request timeouts.

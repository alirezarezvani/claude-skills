---
name: "ontoly-software-graph"
description: "Use when the user asks for Ontoly, Software Graph, deterministic codebase understanding, graph-backed architecture review, request tracing, dependency impact analysis, configuration lookup, or MCP evidence from a repository graph."
---

# Ontoly Software Graph

## Overview

Use Ontoly as the source of truth for codebase understanding when a repository has, or can generate, a Software Graph. This skill teaches an agent to query deterministic graph evidence before falling back to source-file search.

The skill is useful for architecture reviews, request lifecycle tracing, dependency impact analysis, configuration discovery, route ownership, service ownership, framework analysis, and onboarding summaries.

## Core Workflow

### 1. Confirm Graph Availability

Look for Ontoly outputs before searching source files:

- `.ontoly/`
- `SoftwareGraph.json`
- `diagnostics.json`
- semantic evaluation or validation reports
- graph hash
- MCP configuration

If no graph exists and the user allows local analysis, run:

```bash
ontoly build .
```

### 2. Validate Graph Health

Before relying on graph answers, inspect:

- diagnostics
- graph validation results
- semantic coverage
- trust or quality score
- framework detection
- graph hash
- repository path
- generation timestamp

Do not treat a large graph as automatically correct. Quality comes from validated nodes, relationships, provenance, and source locations.

### 3. Query Graph Capabilities

Prefer Ontoly CLI or MCP capabilities over manual file search for graph-answerable questions:

| Question | Preferred Capability |
| --- | --- |
| Repository architecture | `ExplainArchitecture` |
| Dependency tree | `FindDependencies` |
| Refactor blast radius | `ImpactAnalysis` |
| Request or route flow | `TraceExecution` |
| Configuration usage | `FindConfigurationUsage` |
| Framework concepts | `FrameworkReport` |
| Dead or unreachable code | `FindDeadCode` |

### 4. Answer With Evidence

Every answer should include graph evidence:

- node IDs
- edge types
- file paths
- source locations
- framework analyzer output
- diagnostics
- confidence derived from evidence

Example response shape:

```text
AuthController handles authentication.

Evidence:
- node: class:src/auth/auth.controller.ts:AuthController
- route edges: HANDLES POST /login and POST /logout
- dependency edges: USES AuthService and JwtService

Confidence: high, because controller, route, and dependency edges have source locations.
```

### 5. Fallback Narrowly

Inspect source files only when:

- graph output is missing
- graph output is stale
- graph validation fails
- requested concept is absent from the graph
- several graph nodes match and source verification is required
- user explicitly asks for source-level confirmation

When falling back, state why the graph was insufficient and keep source inspection focused on the affected files.

## Anti-Patterns

- Searching the repository first when Ontoly graph evidence is available
- Guessing confidence without node, edge, diagnostic, or source-location evidence
- Treating graph size as proof of understanding
- Hiding validation failures or stale graph warnings
- Inventing routes, services, dependencies, or configuration usage when the graph returns `NOT_FOUND`
- Mixing Ontoly workflow logic with unrelated compiler or query implementation advice

## Cross-References

- Use `engineering/skills/codebase-onboarding` when the user wants onboarding docs after graph facts are collected.
- Use `engineering/skills/monorepo-navigator` when the graph question is specifically about workspace/package operations.
- Use `engineering/skills/dependency-auditor` when the question is about third-party package risk rather than internal graph relationships.
- Use `engineering/skills/mcp-server-builder` when implementing or extending MCP server behavior.


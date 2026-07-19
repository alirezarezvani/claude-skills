---
title: "Performance Profiler — Agent Skill for Codex & OpenClaw"
description: "Systematic performance profiling for Node.js, Python, and Go applications. Identifies CPU, memory, and I/O bottlenecks, generates flamegraphs. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Performance Profiler

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `performance-profiler`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/performance-profiler/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Performance Engineering  

---

## Overview

Systematic performance profiling for Node.js, Python, and Go applications. Identifies CPU, memory, and I/O bottlenecks; generates flamegraphs; analyzes bundle sizes; optimizes database queries; detects memory leaks; and runs load tests with k6 and Artillery. Always measures before and after.

## Core Capabilities

- **CPU profiling** — flamegraphs for Node.js, py-spy for Python, pprof for Go
- **Memory profiling** — heap snapshots, leak detection, GC pressure
- **Bundle analysis** — webpack-bundle-analyzer, Next.js bundle analyzer
- **Database optimization** — EXPLAIN ANALYZE, slow query log, N+1 detection
- **Load testing** — k6 scripts, Artillery scenarios, ramp-up patterns
- **Before/after measurement** — establish baseline, profile, optimize, verify

---

## When to Use

- App is slow and you don't know where the bottleneck is
- P99 latency exceeds SLA before a release
- Memory usage grows over time (suspected leak)
- Bundle size increased after adding dependencies
- Preparing for a traffic spike (load test before launch)
- Database queries taking >100ms

---

## Quick Start

```bash
# Analyze a project for performance risk indicators
python3 scripts/performance_profiler.py /path/to/project

# JSON output for CI integration
python3 scripts/performance_profiler.py /path/to/project --json

# Custom large-file threshold
python3 scripts/performance_profiler.py /path/to/project --large-file-threshold-kb 256
```

---

## Golden Rule: Measure First

```bash
# Establish baseline BEFORE any optimization
# Record: P50, P95, P99 latency | RPS | error rate | memory usage

# Wrong: "I think the N+1 query is slow, let me fix it"
# Right: Profile → confirm bottleneck → fix → measure again → verify improvement
```

---

## Node.js Profiling
→ See references/profiling-recipes.md for details

## References

- [references/profiling-recipes.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/performance-profiler/references/profiling-recipes.md) — Node.js/Python/Go profiling commands, flamegraph generation, heap snapshots
- [references/optimization-playbook.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/performance-profiler/references/optimization-playbook.md) — before/after measurement template, quick-win optimization checklist (DB/Node/bundle/API), common pitfalls, best practices


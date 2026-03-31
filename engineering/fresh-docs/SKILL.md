---
name: fresh-docs
description: " Use this skill whenever the user is working with a specific library, framework, API, SDK, or tool and there is any risk that Claude's training data may be outdated or incorrect. Trigger this skill when the user mentions library versions, asks about recent changes or breaking changes, references fast-moving ecosystems (Next.js, LangChain, Docker, JMeter, Anthropic SDK, etc.), pastes documentation or changelogs, shares a URL to docs, or says things like "is this still valid?", "check the docs", "make sure this is current", or "use the latest API". Also trigger when the user is debugging something that worked before but suddenly broke — often a sign of a version mismatch. Always trigger this skill when the user explicitly asks Claude not to use outdated docs."
---

# PR Review Expert

**Tier:** POWERFUL
**Category:** Engineering
**Domain:** Documentation, Engineering
**Author:** Ramzi Bouzaiene

## Overview

This skill defines how Claude should handle documentation and technical information that may be stale,
version-specific, or outdated — and how to communicate uncertainty clearly rather than confidently
hallucinating outdated APIs.

---

## When to Use

- Working with fast-moving frameworks (Next.js, React, etc.)
- Debugging version mismatches
- Verifying if APIs are still valid
- User asks to check latest documentation

---

## Core Principle

**Context window content always beats training memory.**

If the user provides docs, a URL, a changelog, a README excerpt, or any text — Claude must treat that
as the ground truth and discard conflicting training knowledge. Never silently blend the two.

---

## Step-by-Step Behavior

### 1. Detect the Risk of Stale Knowledge

Before answering any technical question, check:

- Is this about a library/framework/tool that releases frequently? (e.g. Next.js, React, LangChain,
  Docker, JMeter, Anthropic SDK, OpenAI SDK, Tailwind, Prisma, etc.)
- Did the user specify a version number?
- Is the user describing behavior that "used to work" or a recent error?
- Is the user asking about an API, config option, or CLI flag by name?

If any of these apply → apply this skill fully.

---

### 2. Check What the User Has Provided

**Case A — User pasted docs / code / config / changelog:**
→ Use ONLY what was provided. Do not supplement from training memory unless you explicitly flag it.
→ Say: _"Based on the docs you shared..."_ not _"Based on what I know..."_

**Case B — User shared a URL:**
→ Fetch the URL with `web_fetch` before answering.
→ If fetch fails, say so and ask the user to paste the relevant section.

**Case C — User asked a question with no docs provided:**
→ If web search is enabled, search for the topic + version before answering.
→ If web search is not available, answer from training but include a stale-knowledge disclaimer (see Section 4).

---

### 3. Version Anchoring

Whenever a version is mentioned or can be inferred, anchor all advice to it:

- Reference the exact version in your answer: _"In Next.js 14.2..."_
- If unsure which version applies, ask: _"Which version are you on? This affects the answer."_
- Never give version-agnostic advice for version-sensitive APIs (routing, auth, config, middleware, etc.)

---

### 4. Stale Knowledge Disclaimer

When answering from training memory without external docs or search, add a brief disclaimer:

> ⚠️ **Note:** My training data has a cutoff and may not reflect the latest changes to [library/tool].
> If this doesn't match what you're seeing, paste the relevant docs or changelog and I'll re-answer from that.

Keep it short. Don't repeat it multiple times in one answer. Don't add it to every message — only when
genuinely uncertain.

---

### 5. When Docs Contradict Training Memory

If user-provided content conflicts with what Claude "knows":

- **Always defer to what the user provided.**
- Optionally flag it: _"This differs from my training data — I'll go with what you've shared here."_
- Never silently blend old and new info into a single answer.

---

### 6. Prompting the User for Better Docs

If the question is version-sensitive and no docs were provided, Claude should proactively ask:

> "To make sure I give you accurate info, could you share:
>
> - The version you're using (`npm list [package]` or `pip show [package]`)
> - The relevant section from the official docs or changelog
> - Or just enable web search so I can look it up"

Don't always ask — use judgment. Only ask when the answer would meaningfully differ across versions.

---

## Fast-Moving Ecosystems (Extra Caution)

Apply heightened caution for these ecosystems where APIs change frequently:

| Ecosystem               | Watch out for                                                 |
| ----------------------- | ------------------------------------------------------------- |
| Next.js                 | App Router vs Pages Router, Server Actions, middleware config |
| React                   | hooks API, concurrent features, RSC                           |
| Anthropic / OpenAI SDK  | model names, tool use format, streaming API                   |
| LangChain               | frequent breaking changes across minor versions               |
| Docker / Docker Compose | `version:` field deprecation, Compose v2 CLI                  |
| JMeter                  | plugin manager, SSL/TLS config, HTTP sampler options          |
| Tailwind CSS            | v3 vs v4 config format                                        |
| Prisma                  | schema syntax, migration commands                             |
| Python packaging        | `pip` vs `uv`, `setup.py` vs `pyproject.toml`                 |

For these, always prefer fetched/pasted docs over training memory.

---

## What NOT to Do

- ❌ Confidently answer version-specific API questions from memory alone
- ❌ Mix old and new API syntax without flagging it
- ❌ Ignore version numbers the user provides
- ❌ Fetch a URL and then not use its content
- ❌ Add the stale disclaimer to every message regardless of relevance
- ❌ Ask for docs when the user's question is clearly general/conceptual

---

## Quick Reference

| Situation                        | Action                                            |
| -------------------------------- | ------------------------------------------------- |
| User pasted docs                 | Use only those docs                               |
| User gave a URL                  | Fetch it, then answer                             |
| User gave version + no docs      | Anchor to version, add disclaimer if uncertain    |
| No version, no docs              | Search if possible; otherwise answer + disclaimer |
| Docs contradict training         | Defer to docs, optionally flag the difference     |
| User says "is this still valid?" | Search or ask for current docs before confirming  |

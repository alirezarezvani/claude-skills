---
title: "Grill Me — Agent Skill for Codex & OpenClaw"
description: "Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Grill Me

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `grill-me`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/skills/grill-me/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> Derived from [Matt Pocock's grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) (MIT). Matt's interview discipline preserved verbatim. Additions: extraction + question + session tools + references + cs-* wrapper (see [references/companion_tooling.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/skills/grill-me/references/companion_tooling.md)).

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Rules (preserved + amplified)

1. **One question per turn.** Never bundle.
2. **Provide a recommended answer with each question.** Defaulting to "what do you think?" is lazy.
3. **Explore the codebase before asking.** If `grep` / `Read` resolves it, do that first. Saves a turn.
4. **Walk the tree depth-first.** Finish a branch before opening another.
5. **Track dependencies.** If decision B depends on decision A, ask A first.

## Workflow

1. User provides a plan or design (or path to one).
2. Run `scripts/decision_tree_extractor.py` to extract branches.
3. Run `scripts/question_generator.py` to produce the question list with recommendations.
4. Start a session: `scripts/grill_session_tracker.py --action start`.
5. Walk the tree, one question at a time, recording answers in the session.
6. When all branches resolved: report "shared understanding reached" + the locked-in decisions.

## Output Pattern

Per question turn:

```
Q[i]/[total]: [question]
Recommended answer: [your call + 1-sentence rationale]

(Or: I explored the codebase and found [evidence]. Confirm?)
```

## Tooling

See [references/companion_tooling.md](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/skills/grill-me/references/companion_tooling.md). Tools: extractor + generator + tracker. Agent: `cs-grill-master`. Command: `/cs:grill-me`.

---

**Version:** 1.0.0
**Derived:** Matt Pocock (MIT) + this repo's wrapper

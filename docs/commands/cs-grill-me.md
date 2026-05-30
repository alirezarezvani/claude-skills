---
title: "/cs-grill-me — Slash Command for AI Coding Agents"
description: "/cs:grill-me <path-to-plan> — Start a relentless interrogation of a plan or design. Walks decision tree one branch at a time. One question per turn. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-grill-me

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/grill-me/commands/cs-grill-me.md">Source</a></span>
</div>


**Command:** `/cs:grill-me <path-to-plan>`

The grill-master persona interrogates a plan one decision branch at a time.

## When to Run

- Stress-testing a plan before commitment
- Pre-mortem on a design (find weaknesses before they hurt)
- Onboarding to an existing plan (interrogate what's there)
- Resuming a grill session from previous turn

## The Six Forcing-Question Patterns

1. **Intent:** "Why X and not Y?" (names the alternative)
2. **Choice:** "Which side, and what's the deciding constraint?"
3. **Open:** "What's blocking this decision, and when does the blocker resolve?"
4. **Tradeoff:** "Which side are you optimizing for, and what's the kill criterion?"
5. **Dependency:** "Is the upstream decision locked in? If not, that comes first."
6. **Uncertainty:** "Even at 60% confidence — what's your best guess?"

## Discipline

- **One question per turn.** Never bundle.
- **Recommended answer attached.** Every question carries a position + rationale.
- **Codebase before speculation.** `grep` / `Read` resolves before asking.
- **Depth-first walk.** Finish a branch before opening another.

## Workflow

```bash
# 1. Extract decision branches from the plan
python ../skills/grill-me/scripts/decision_tree_extractor.py path/to/plan.md

# 2. Generate forcing questions with recommendations
python ../skills/grill-me/scripts/question_generator.py path/to/plan.md

# 3. Start session
python ../skills/grill-me/scripts/grill_session_tracker.py --action start --session NAME --plan path/to/plan.md

# 4. Walk one question at a time:
#    Persona asks Q1 with recommendation.
#    User answers.
#    Record:
python ../skills/grill-me/scripts/grill_session_tracker.py --action record --session NAME --question-id 1 --answer "..."

# 5. When complete:
python ../skills/grill-me/scripts/grill_session_tracker.py --action close --session NAME
```

## When to Stop

- Every branch has an answer
- 3+ turns with no new questions arising
- User signals fatigue ("can we move on?")
- Diminishing returns past ~15 questions

Produce a "decisions locked" summary at close.

## Output Format

```
Q[i]/[total] (L[line]): [question]
Recommended: [position] because [1-sentence rationale]

(or: I explored — found [evidence]. Confirm?)
```

## Related

- Agent: [`cs-grill-master`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/agents/cs-grill-master.md)
- Skill: [`grill-me`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/grill-me/skills/grill-me/SKILL.md)
- Adjacent: `/cs:caveman`, `/cs:handoff`, `/cs:write-a-skill`

---

**Version:** 1.0.0
**Derived:** Matt Pocock's grill-me (MIT) + this repo's wrapper

# grill-me

Relentless plan-and-design interrogator. Walks the decision tree one branch at a time. One question at a time. Each question has a recommended answer.

## Attribution

**Derived from [Matt Pocock's grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)** (MIT). Matt's interrogation discipline preserved verbatim per his MIT license — relentless one-at-a-time questioning, recommended answers per question, codebase exploration over speculation.

## What this adds on top of Matt's original

| Addition | Where | Why |
|---|---|---|
| **3 stdlib Python tools** | `skills/grill-me/scripts/` | Extract decision branches from a plan doc, generate forcing questions, track session state across turns |
| **3 in-depth references** (5+ sources each) | `skills/grill-me/references/` | Forcing-question patterns · Decision-tree completeness · When to stop grilling |
| **cs-grill-master persona agent** | `agents/cs-grill-master.md` | One-question-at-a-time enforcer with state tracking |
| **`/cs:grill-me` slash command** | `commands/cs-grill-me.md` | Activation + session start |

## Matt's original (preserved)

> "Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Ask the questions one at a time. If a question can be answered by exploring the codebase, explore the codebase instead."

## Quick start

```bash
# Extract decision branches from a plan
python skills/grill-me/scripts/decision_tree_extractor.py path/to/plan.md

# Generate forcing questions from a plan
python skills/grill-me/scripts/question_generator.py path/to/plan.md

# Track grill session state across turns
python skills/grill-me/scripts/grill_session_tracker.py --session NAME --action start
```

## License

MIT (matching Matt's upstream).

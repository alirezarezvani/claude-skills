# write-a-skill

Skill-author skill: create new agent skills with proper structure, progressive disclosure, and bundled resources.

## Attribution

**Derived from [Matt Pocock's write-a-skill](https://github.com/mattpocock/skills/tree/main/skills/productivity/write-a-skill)** (MIT-licensed). Matt's [skills repo](https://github.com/mattpocock/skills) — *"Skills for Real Engineers. Straight from my .claude directory"* — is the original source. Matt's SKILL.md voice + 3-phase workflow (Gather → Draft → Review) preserved verbatim per his MIT license.

## What this adds on top of Matt's original

| Addition | Where | Why |
|---|---|---|
| **3 stdlib Python validation tools** | `skills/write-a-skill/scripts/` | Operationalize Matt's review checklist (description validator, structure validator, review-checklist runner). Catches the common mistakes Matt names. |
| **3 in-depth references** (5+ sources each) | `skills/write-a-skill/references/` | Progressive disclosure principles · Description design patterns · Quality gates for skills. Cites Anthropic skill docs + community precedent + research. |
| **cs-skill-author persona agent** | `agents/cs-skill-author.md` | Surface skill-authoring as a forcing-question interrogation matching our cs-* persona pattern. |
| **`/cs:write-a-skill` slash command** | `commands/cs-write-a-skill.md` | 6-question forcing interrogation that runs Matt's review checklist programmatically. |

## What Matt's original brings (preserved)

- The 3-phase workflow: **Gather → Draft → Review**
- The non-negotiable description rule: *"The description is the only thing your agent sees when deciding which skill to load."*
- The 100-line SKILL.md ceiling + progressive-disclosure pattern (REFERENCE.md / EXAMPLES.md / scripts)
- The good-example vs bad-example contrast for description writing
- The 6-item review checklist
- Matt's directness — no fluff, concrete patterns

## Quick start

```bash
# Run Matt's review checklist on an existing skill
python skills/write-a-skill/scripts/skill_review_checklist_runner.py path/to/SKILL.md

# Validate description meets Matt's criteria (≤1024 chars, third person, "Use when" trigger)
python skills/write-a-skill/scripts/skill_description_validator.py path/to/SKILL.md

# Validate skill folder structure
python skills/write-a-skill/scripts/skill_structure_validator.py path/to/skill-folder/
```

All three tools run with embedded samples if no path provided.

## License

MIT (matching Matt's upstream).

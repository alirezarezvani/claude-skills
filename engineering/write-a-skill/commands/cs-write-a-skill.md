---
name: "cs-write-a-skill"
description: "/cs:write-a-skill <name-or-description> — Author a new agent skill with Matt Pocock's 3-phase workflow (Gather → Draft → Review). Runs 6 review-checklist items + 3 validator tools as a gate. Use when starting a new skill in this repo."
---

# /cs:write-a-skill — Skill-Author Forcing Questions

**Command:** `/cs:write-a-skill <name-or-description>`

The skill-author persona pressure-tests any new-skill commit. Six forcing questions before any merge, matching Matt Pocock's review checklist.

## When to Run

- Starting a new skill from scratch
- Deriving a skill from an upstream (MIT-licensed) source
- Auditing an existing skill against current standards
- Reviewing a new-skill PR before merge

## The Six Skill-Author Questions

### 1. What's the description, and does it pass Matt's 4-rule test?
**The description is the only thing your agent sees when deciding to load this skill.**
- Max 1024 chars
- Third person (no I / you / we)
- First sentence: what it does (action verb)
- Second sentence: "Use when [specific triggers]"
- Run `skill_description_validator.py`

### 2. Is SKILL.md under 100 lines?
**Over 100 lines = over-conditioning + reference soup downstream.**
- If yes: great, ship it
- If no: split workflows into `references/<topic>.md`; replace inline content with 1-2 line pointers
- Wrapper-derived skills (preserving upstream content) get a documented exception

### 3. Are there time-sensitive claims?
**Dates rot. "As of October 2024" becomes wrong by next year.**
- Remove: "as of YYYY", "in YYYY", "released YYYY", "updated YYYY"
- Replace with: pattern description that doesn't depend on date
- Example: not "ISO 42001 published December 2023"; use "ISO 42001 (the first AI management-system standard)"

### 4. Is terminology consistent?
**Synonym drift confuses agents + readers.**
- Pick one: agent OR bot, skill OR tool, user OR developer
- Use the chosen term throughout
- Document the choice in a glossary if multiple stakeholders involved

### 5. Are there at least 2 concrete examples (good + bad if possible)?
**Without examples, agents construct from scratch and hallucinate.**
- At least 1 code block
- Ideally good/bad contrast (Matt's pattern)
- Examples must be runnable or copy-pasteable

### 6. Are references one level deep + no circular refs?
**Deep nesting = agent gives up resolving the chain.**
- Flat `references/<topic>.md` layout
- No `references/category/subtopic.md`
- No A→B→A cycles
- Run `skill_structure_validator.py`

## Workflow

```bash
# 1. Description gate
python ../skills/write-a-skill/scripts/skill_description_validator.py path/to/SKILL.md

# 2. Structure gate
python ../skills/write-a-skill/scripts/skill_structure_validator.py path/to/skill-folder/

# 3. Combined review (Matt's 6-item checklist)
python ../skills/write-a-skill/scripts/skill_review_checklist_runner.py path/to/skill-folder/

# 4. Karpathy code-quality gate (if scripts/ exist)
python ../../karpathy-coder/skills/karpathy-coder/scripts/complexity_checker.py path/to/skill-folder/scripts/
python ../../karpathy-coder/skills/karpathy-coder/scripts/assumption_linter.py path/to/skill-folder/scripts/

# 5. Attribution check (if derived)
grep -r "derived_from\|original_author" path/to/skill-folder/
```

## Output Format

```markdown
# Skill Author Review: <skill-name>
**Date:** YYYY-MM-DD

## The Decision Being Made
[gather | draft | review | validate | derive | audit]

## Description Validation
- Length: N chars (limit 1024): pass/fail
- Third person: pass/fail
- "Use when" trigger: pass/fail
- Action verb in first sentence: pass/fail

## Structure Validation
- SKILL.md present + ≤100 lines: pass/fail (N lines)
- References one level deep: pass/fail
- No circular refs: pass/fail
- scripts/ folder: present/absent (optional)

## Review Checklist (Matt's 6 items)
- [x|/] 1. Description includes triggers
- [x|/] 2. SKILL.md under 100 lines
- [x|/] 3. No time-sensitive info
- [x|/] 4. Consistent terminology
- [x|/] 5. Concrete examples included
- [x|/] 6. References one level deep

## Karpathy Code Gate (if applicable)
- complexity_checker: PASS / WARN (with findings)
- assumption_linter: CLEAN / NOISY

## Attribution (if derived skill)
- Upstream link: present/missing
- License compatibility: yes/no
- Author credit: present/missing

## Verdict
🟢 SHIP | 🟡 WARN-WITH-JUSTIFICATION | 🔴 BLOCK

## Top 3 Actions (if not green)
[3 concrete fixes with file:line references]
```

## Routing

- `/cs:karpathy-check` — for code-quality concerns in scripts/
- `/cs:tdd` — for testing discipline (different from skill quality gates)
- `/cs:decide` — to log the verdict

## Related

- Agent: [`cs-skill-author`](../agents/cs-skill-author.md)
- Skill: [`write-a-skill`](../skills/write-a-skill/SKILL.md)
- Adjacent: `../../karpathy-coder/`, `../../autoresearch-agent/`

---

**Version:** 1.0.0
**Derived:** Matt Pocock's write-a-skill (MIT) + this repo's wrapper

---
title: "/plugin-audit — Slash Command for AI Coding Agents"
description: "Comprehensive audit pipeline for skills, plugins, agents, and commands. Validates structure, quality, security, marketplace compliance. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /plugin-audit

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/plugin-audit.md">Source</a></span>
</div>


Full audit pipeline for any skill, plugin, agent, or command in this repository. Runs 8 validation phases, auto-fixes what it can, and only stops for user input on critical decisions (breaking changes, new dependencies).

## Usage

```bash
/plugin-audit product-team/code-to-prd
/plugin-audit engineering/agenthub
/plugin-audit engineering-team/playwright-pro
```

## What It Does

Execute all 8 phases sequentially. Stop on critical failures. Auto-fix non-critical issues. Report results at the end.

---

## Phase 1: Discovery

Identify what the skill contains and classify it.

1. Verify `{skill_path}` exists and contains `SKILL.md`
2. Read `SKILL.md` frontmatter — extract `name`, `description`, `Category`, `Tier`
3. Detect skill type:
   - Has `scripts/` → has Python tools
   - Has `references/` → has reference docs
   - Has `assets/` → has templates/samples
   - Has `expected_outputs/` → has test fixtures
   - Has `agents/` → has embedded agents
   - Has `skills/` → has sub-skills (compound skill)
   - Has `.claude-plugin/plugin.json` → is a standalone plugin
   - Has `settings.json` → has command registrations
4. Detect domain from path: `engineering/`, `product-team/`, `marketing-skill/`, etc.
5. Check for associated command: search `commands/` for a `.md` file matching the skill name

Display discovery summary before proceeding:
```
Auditing: code-to-prd
  Domain: product-team
  Type: STANDARD skill with standalone plugin
  Scripts: 2 | References: 2 | Assets: 1 | Expected outputs: 3
  Command: /code-to-prd (found)
  Plugin: .claude-plugin/plugin.json (found)
```

---

## Phase 2: Structure Validation

Run the skill-tester validator.

```bash
python3 engineering/skill-tester/scripts/skill_validator.py {skill_path} --tier {detected_tier} --json
```

Parse the JSON output. Extract:
- Overall score and compliance level
- Failed checks (list each)
- Errors and warnings

**Gate rule:** Score must be ≥ 75 (GOOD). If below 75:
- Read the errors list
- Auto-fix what's possible:
  - Missing frontmatter fields → add them from SKILL.md content
  - Missing sections → add stub headings
  - Missing directories → create empty ones with a note
- Re-run after fixes. If still below 75, report as FAIL and continue to collect remaining results.

---

## Phase 3: Quality Scoring

Run the quality scorer.

```bash
python3 engineering/skill-tester/scripts/quality_scorer.py {skill_path} --detailed --json
```

Parse the JSON output. Extract:
- Overall score and letter grade
- Per-dimension scores (Documentation, Code Quality, Completeness, Usability)
- Improvement roadmap items

**Gate rule:** Score must be ≥ 60 (C). If below 60, report the improvement roadmap items as action items.

---

## Phase 4: Script Testing

If the skill has `scripts/` with `.py` files, run the script tester.

```bash
python3 engineering/skill-tester/scripts/script_tester.py {skill_path} --json --verbose
```

Parse the JSON output. For each script, extract:
- Pass/Partial/Fail status
- Individual test results

**Gate rule:** All scripts must PASS. Any FAIL is a blocker. PARTIAL triggers a warning.

**Auto-fix:** If a script fails the `--help` test, check if it has `argparse` — if not, this is a real issue. If it fails the stdlib-only test, flag the import and **ask the user** whether the dependency is acceptable (this is a critical decision).

---

## Phase 5: Security Audit

Run the skill security auditor.

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py {skill_path} --strict --json
```

Parse the JSON output. Extract:
- Verdict (PASS/WARN/FAIL)
- Critical findings (must be zero)
- High findings (must be zero in strict mode)
- Info findings (advisory only)

**Gate rule:** Zero CRITICAL findings. Zero HIGH findings. Any CRITICAL or HIGH is a blocker — report the exact file, line, pattern, and recommended fix.

**Do NOT auto-fix security issues.** Report them and let the user decide.

---

## Phase 6: Marketplace & Plugin Compliance

### 6a. plugin.json Validation

If `{skill_path}/.claude-plugin/plugin.json` exists:

1. Parse as JSON — must be valid
2. Verify only allowed fields: `name`, `description`, `version`, `author`, `homepage`, `repository`, `license`, `skills`
3. Version must match repo version (`2.1.2`)
4. `skills` must be `"./"`
5. `name` must match the skill directory name

**Auto-fix:** If version is wrong, update it. If extra fields exist, remove them.

### 6b. settings.json Validation

If `{skill_path}/settings.json` exists:

1. Parse as JSON — must be valid
2. Version must match repo version
3. If `commands` field exists, verify each command has a matching file in `commands/`

### 6c. Marketplace Entry

Check if the skill has an entry in `.claude-plugin/marketplace.json`:

1. Search the `plugins` array for an entry with `source` matching `./` + skill path
2. If found: verify `version`, `name`, and that `source` path exists
3. If not found: check if the skill's domain bundle (e.g., `product-skills`) would include it via its `source` path

### 6d. Domain plugin.json

Check the parent domain's `.claude-plugin/plugin.json`:
- Verify the skill count in the description matches reality
- Verify version matches repo version

**Auto-fix:** Update stale counts. Fix version mismatches.

---

## Phase 7: Ecosystem Integration

### 7a. Cross-Platform Sync

Verify the skill appears in platform indexes:

```bash
grep -l "{skill_name}" .codex/skills-index.json .gemini/skills-index.json
```

If missing from either index:
```bash
python3 scripts/sync-codex-skills.py --verbose
python3 scripts/sync-gemini-skills.py --verbose
```

### 7b. Command Integration

If the skill has associated commands (from settings.json `commands` field or matching name in `commands/`):
- Verify the command `.md` file has valid YAML frontmatter (`name`, `description`)
- Verify the command references the correct skill path
- Verify the command is in `mkdocs.yml` nav

**Auto-fix:** Add missing mkdocs.yml nav entries.

### 7c. Agent Integration

If the skill has embedded agents (`{skill_path}/agents/*.md`):
- Verify each agent has valid YAML frontmatter
- Verify agent references resolve (relative paths to skills)

Search `agents/` for any cs-* agent that references this skill:
```bash
grep -rl "{skill_name}\|{skill_path}" agents/
```

If found, verify the agent's skill references are correct.

### 7d. Cross-Skill Dependencies

Read the SKILL.md for references to other skills (look for `../` paths, skill names in "Related Skills" sections):
- Verify each referenced skill exists
- Verify the referenced skill's SKILL.md exists

---

## Phase 8: Domain-Appropriate Code Review

Based on the skill's domain, invoke the appropriate agent's review perspective:

| Domain | Agent | Review Focus |
|--------|-------|-------------|
| `engineering/` or `engineering-team/` | cs-senior-engineer | Architecture, code quality, CI/CD integration |
| `product-team/` | cs-product-manager | PRD quality, user story coverage, RICE alignment |
| `marketing-skill/` | cs-content-creator | Content quality, SEO optimization, brand voice |
| `ra-qm-team/` | cs-quality-regulatory | Compliance checklist, audit trail, regulatory alignment |
| `business-growth/` | cs-growth-strategist | Growth metrics, revenue impact, customer success |
| `finance/` | cs-financial-analyst | Financial model accuracy, metric definitions |
| Other | cs-senior-engineer | General code and architecture review |

**How to invoke:** Read the agent's `.md` file to understand its review criteria. Apply those criteria to review the skill's SKILL.md, scripts, and references. This is NOT spawning a subagent — it's using the agent's documented perspective to structure your review.

Review checklist (apply domain-appropriate lens):
- [ ] SKILL.md workflows are actionable and complete
- [ ] Scripts solve the stated problem correctly
- [ ] References contain accurate domain knowledge
- [ ] Templates/assets are production-ready
- [ ] No broken internal links
- [ ] Attribution present where required

---

## Final Report

Present results as a structured table:

```
╔══════════════════════════════════════════════════════════════╗
║  PLUGIN AUDIT REPORT: {skill_name}                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Phase 1 — Discovery          ✅ {type}, {domain}            ║
║  Phase 2 — Structure          ✅ {score}/100 ({level})       ║
║  Phase 3 — Quality            ✅ {score}/100 ({grade})       ║
║  Phase 4 — Scripts            ✅ {n}/{n} PASS                ║
║  Phase 5 — Security           ✅ PASS (0 critical, 0 high)   ║
║  Phase 6 — Marketplace        ✅ plugin.json valid            ║
║  Phase 7 — Ecosystem          ✅ Codex + Gemini synced        ║
║  Phase 8 — Code Review        ✅ {domain} review passed       ║
║                                                              ║
║  VERDICT: ✅ PASS — Ready for merge/publish                  ║
║                                                              ║
║  Auto-fixes applied: {n}                                     ║
║  Warnings: {n}                                               ║
║  Action items: {n}                                           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### Verdict Logic

| Condition | Verdict |
|-----------|---------|
| All phases pass | **PASS** — Ready for merge/publish |
| Only warnings (no blockers) | **PASS WITH WARNINGS** — Review warnings before merge |
| Any phase has a blocker | **FAIL** — List blockers with fix instructions |

### Blockers (any of these = FAIL)

- Structure score < 75
- Quality score < 60 (after noting roadmap)
- Any script FAIL
- Any CRITICAL or HIGH security finding
- plugin.json invalid or has disallowed fields
- Version mismatch with repo

### Non-Blockers (warnings only)

- Quality score between 60-75
- Script PARTIAL results
- Missing from one platform index (auto-fixed)
- Missing mkdocs.yml nav entry (auto-fixed)
- Security INFO findings

---

## Skill References

| Tool | Path |
|------|------|
| Skill Validator | `engineering/skill-tester/scripts/skill_validator.py` |
| Quality Scorer | `engineering/skill-tester/scripts/quality_scorer.py` |
| Script Tester | `engineering/skill-tester/scripts/script_tester.py` |
| Security Auditor | `engineering/skill-security-auditor/scripts/skill_security_auditor.py` |
| Quality Standards | `standards/quality/quality-standards.md` |
| Security Standards | `standards/security/security-standards.md` |
| Git Standards | `standards/git/git-workflow-standards.md` |

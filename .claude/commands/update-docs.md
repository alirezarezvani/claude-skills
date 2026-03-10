---
description: Update all the documentation related files.
---

After completing any skill creation, agent creation, or command creation in this repository, run the full post-creation sync pipeline below. Execute every step — never skip a task. If something is unclear or a step fails, ask the user for guidance before continuing.

---

## Step 1: Inventory what changed

Scan the working tree to identify what was added, modified, or deleted:

```bash
git status --short
```

Classify each change:
- **New skill** — a new folder containing `SKILL.md` under a domain directory
- **New agent** — a new `.md` file under `agents/`
- **New command** — a new `.md` file under `commands/`
- **Modified skill/agent/command** — updated existing files
- **Deleted skill/agent/command** — removed files

Report the inventory to the user before proceeding.

---

## Step 2: Cross-platform CLI sync

Ensure all platforms have compatible versions of every skill, agent, and command.

### 2a. Codex CLI

Run the Codex sync script to regenerate symlinks and the skills index:

```bash
python3 scripts/sync-codex-skills.py --verbose
```

Verify the output: check `.codex/skills-index.json` for correct `total_skills` count and that new skills appear in the index.

### 2b. Gemini CLI

Run the Gemini sync script:

```bash
python3 scripts/sync-gemini-skills.py --verbose
```

Verify: check `.gemini/skills-index.json` for correct total count. New skills, agents, and commands should all have corresponding entries and symlinks under `.gemini/skills/`.

### 2c. OpenClaw

Verify that `scripts/openclaw-install.sh` will pick up the new skills. The install script uses the same directory structure, so no separate sync is needed — but confirm the new skill directories are not excluded by any filter in the script.

Report sync results (skill counts per platform) to the user.

---

## Step 3: Claude Code plugin marketplace

### 3a. Domain-level plugin.json

For each domain that had changes, update the domain's `.claude-plugin/plugin.json`:
- Update `description` with accurate skill/tool/reference counts
- Update `version` if needed
- Verify `source` paths are correct

Domain plugin.json locations:
- `marketing-skill/.claude-plugin/plugin.json`
- `engineering-team/.claude-plugin/plugin.json`
- `engineering/.claude-plugin/plugin.json`
- `product-team/.claude-plugin/plugin.json`
- `c-level-advisor/.claude-plugin/plugin.json`
- `project-management/.claude-plugin/plugin.json`
- `ra-qm-team/.claude-plugin/plugin.json`
- `business-growth/.claude-plugin/plugin.json`
- `finance/.claude-plugin/plugin.json`

### 3b. Root marketplace.json

Update `.claude-plugin/marketplace.json`:
- Update the top-level `metadata.description` with accurate total counts (skills, tools, references, agents, commands)
- If a new individual skill plugin entry is needed (for standalone install), add it to the `plugins` array following the existing pattern
- Update `keywords` arrays if new domains or capabilities were added
- Verify all `source` paths point to valid directories

---

## Step 4: Update documentation files

### 4a. Root CLAUDE.md

Update `/CLAUDE.md` (the root project instructions):
- **Current Scope** line: update skill, tool, reference, agent, and command counts
- **Repository Structure** comment counts (agents, commands, skills per domain)
- **Navigation Map** table: verify all domain entries are current
- **Current Version** section: add a bullet if significant changes were made
- **Roadmap** section: update counts if needed

### 4b. Domain-level CLAUDE.md files

For each domain that had changes, update its `CLAUDE.md`:
- Skill count and list
- Script/tool count
- Agent references
- Command references
- Any new cross-domain integrations

Domain CLAUDE.md locations:
- `agents/CLAUDE.md`
- `marketing-skill/CLAUDE.md`
- `product-team/CLAUDE.md`
- `engineering-team/CLAUDE.md`
- `c-level-advisor/CLAUDE.md`
- `project-management/CLAUDE.md`
- `ra-qm-team/CLAUDE.md`
- `business-growth/CLAUDE.md`
- `finance/CLAUDE.md`
- `standards/CLAUDE.md`
- `templates/CLAUDE.md`

### 4c. Root README.md

Update `/README.md`:
- Badge counts (Skills, Agents, Commands)
- Tagline/intro paragraph skill count
- Skills Overview table (domain rows with correct counts)
- Quick Install section (install commands, skill counts in comments)
- Python Analysis Tools section (tool count, add examples for new tools)
- FAQ section (update any counts mentioned)

### 4d. docs/index.md (GitHub Pages homepage)

Update `docs/index.md`:
- `description` meta tag
- Hero subtitle skill count
- Grid cards (skills, tools, agents, commands counts)
- Domain cards (skill counts per domain, links)

### 4e. docs/getting-started.md

Update `docs/getting-started.md`:
- `description` meta tag
- Available Bundles table (skill counts per bundle)
- Python Tools section (tool count)
- FAQ answers (any count references)

---

## Step 5: Regenerate GitHub Pages

Run the docs generation script to create/update all MkDocs pages:

```bash
python3 scripts/generate-docs.py
```

This generates pages for:
- Every skill (from SKILL.md files)
- Every agent (from agents/*.md)
- Every command (from commands/*.md)
- Index pages for skills, agents, and commands sections

### 5a. Update mkdocs.yml navigation

Open `mkdocs.yml` and update the `nav:` section:
- Add new skill pages under the correct domain section
- Add new agent pages under the Agents section
- Add new command pages under the Commands section
- Update `site_description` with current counts

### 5b. Verify the build

```bash
python3 -m mkdocs build 2>&1 | tail -5
```

The build should complete without errors. Warnings about relative links in SKILL.md files are expected and can be ignored (they reference skill-internal paths like `references/` and `scripts/`).

Report the build result and page count to the user.

---

## Step 6: Consistency verification

Run a final consistency check across all updated files:

1. **Count consistency** — Verify the same skill/agent/command/tool counts appear in:
   - Root CLAUDE.md
   - Root README.md
   - docs/index.md
   - docs/getting-started.md
   - .claude-plugin/marketplace.json

2. **Path validation** — Verify all `source` paths in marketplace.json point to existing directories

3. **New script verification** — If new Python scripts were added, verify they run:
   ```bash
   python3 path/to/new/script.py --help
   ```

4. **Frontmatter check** — Verify all new SKILL.md, agent, and command files have valid YAML frontmatter with at minimum `name` and `description` fields

Report any inconsistencies found and fix them before finishing.

---

## Step 7: Summary report

Present a summary to the user:

| Item | Status |
|------|--------|
| New skills added | [list] |
| New agents added | [list] |
| New commands added | [list] |
| Codex CLI sync | count |
| Gemini CLI sync | count |
| OpenClaw compatible | yes/no |
| Marketplace updated | yes/no |
| CLAUDE.md files updated | [count]/[total] |
| README.md updated | yes/no |
| GitHub Pages regenerated | [page count] pages |
| MkDocs build | pass/fail |
| Consistency check | pass/fail |

Ask the user if they want to commit and push the changes.

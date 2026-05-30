# llm-wiki Bridge — Persistent Company Memory

`c-level-agents` ships with two-layer in-session memory via the existing `decision-logger` skill. For **cross-session persistent memory** (the equivalent of gstack's `gbrain`), bridge to the `llm-wiki` skill — a Markdown-only second brain that lives in your editor (Obsidian, VS Code, anything).

This pairing replaces gstack's Postgres + pgvector dependency with stdlib-only Markdown.

## Setup

### 1. Initialize an llm-wiki vault

```
/wiki-init
```

Pick a path (e.g. `~/company-vault/`). This creates the vault structure with templates.

### 2. Point company-context at the vault

The `cs-onboard` skill writes to `~/.claude/company-context.md`. Replace it with a symlink or add a pointer block:

```bash
ln -sf ~/company-vault/00-meta/company-context.md ~/.claude/company-context.md
```

Or add this block to the top of `~/.claude/company-context.md`:

```markdown
> Source of truth: `~/company-vault/00-meta/company-context.md`
> Decisions: `~/company-vault/10-decisions/`
> Boardroom transcripts: `~/company-vault/20-boardroom/`
> Post-mortems: `~/company-vault/30-postmortems/`
```

### 3. Configure decision-logger to write into the vault

The `decision-logger` skill writes approved decisions to a known path. Set the env var or update its config to point at the vault:

```bash
export CS_DECISION_LOG_DIR=~/company-vault/10-decisions/
```

Every `/cs:decide` invocation now writes a dated decision file into the vault. Boardroom transcripts go to `20-boardroom/`. Post-mortems go to `30-postmortems/`.

### 4. Let llm-wiki index everything

Run `/wiki-ingest` periodically (or wire it into a hook) so the wiki-linter cross-links decisions, post-mortems, and brief artifacts. Now a future `/cs:office-hours` call can pull "what did we decide about X six months ago?" from the vault.

## Recommended Vault Layout

```
~/company-vault/
├── 00-meta/
│   └── company-context.md          ← source of truth
├── 10-decisions/                    ← decision-logger output
│   ├── 2026-05-12-pricing-v3.md
│   └── ...
├── 20-boardroom/                    ← /cs:boardroom artifacts
│   └── 2026-05-12-series-b-go.md
├── 30-postmortems/                  ← /cs:post-mortem artifacts
│   └── 2026-04-30-q1-miss.md
├── 40-briefs/                       ← /cs:brief artifacts
├── 50-execution/                    ← /cs:execute plans
└── 60-references/                   ← pasted research, links
```

## Querying the Vault

Once the vault is wired, the bridge unlocks:

```
/wiki-query "decisions about pricing"      # find all pricing decisions
/wiki-query "post-mortems Q1 2026"          # find retrospectives
/cs:founder-mode "should we raise now?"    # context-aware routing — pulls last fundraising decision
```

## Why This Beats gstack's `gbrain`

| | gbrain | llm-wiki bridge |
|---|---|---|
| Dependencies | Postgres + pgvector + custom hosts | Markdown files |
| Editing | Programmatic via SDK | Any editor (Obsidian native) |
| Backup | DB dump | `git commit` |
| Portability | Server-bound | File-bound |
| Cost | Hosting + DB | $0 |

## Caveats

- **First-class search needs Obsidian or ripgrep.** Markdown vaults don't auto-index; pair with Obsidian for graph view or `rg` for CLI search.
- **No vector similarity by default.** If you need semantic recall, llm-wiki supports an optional `wiki-embeddings.py` script — still stdlib + sqlite, no Postgres.
- **One vault per company.** Multi-tenant founders (advisors, fund operators) should keep one vault per portfolio company.

---

**Related Skills:** `llm-wiki`, `decision-logger`, `context-engine`, `cs-onboard`
**Last Updated:** 2026-05-12

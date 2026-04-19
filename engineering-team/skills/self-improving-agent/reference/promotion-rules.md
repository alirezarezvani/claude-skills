# Promotion Rules

When to promote a learning from auto-memory (MEMORY.md) to the project's rule system (CLAUDE.md or `.claude/rules/`).

## Promotion Criteria

A learning should be promoted when **all three** are true:

1. **Proven** — appeared in 2+ sessions or confirmed correct after testing
2. **Actionable** — can be written as a concrete instruction ("Use X", "Never Y")
3. **Durable** — will still be true in 30+ days

## Scoring Guide

| Dimension | Score 0 | Score 1 | Score 2 | Score 3 |
|-----------|---------|---------|---------|---------|
| **Durability** | One-time fix | Temporary workaround | Stable pattern | Architectural truth |
| **Impact** | Nice-to-know | Saves 1 minute | Prevents mistakes | Prevents breakage |
| **Scope** | One file only | One directory | Entire project | All your projects |

**Promote when total ≥ 6.** Watch when total = 4-5. Ignore when total ≤ 3.

## Target Selection

### Use CLAUDE.md when:
- The rule applies to the entire project
- It's a build command, test convention, or architecture decision
- Any contributor (human or AI) needs to know it
- It's short enough to add without exceeding 200 lines

### Use .claude/rules/ when:
- The rule only applies to specific file types
- CLAUDE.md is already near 200 lines
- The rule needs detailed explanation (multiple paragraphs)
- You want it to load only when relevant files are open

### Use ~/.claude/CLAUDE.md when:
- The rule applies to all your projects
- It's a personal preference, not a project convention
- Examples: "Prefer explicit returns over implicit", "Use descriptive variable names"

## Distillation Rules

When promoting, transform the learning:

### From descriptive to prescriptive

❌ "I noticed the project uses pnpm workspaces. npm install fails because of the lock file."
✅ "Use `pnpm install`, not npm. Lock file: `pnpm-lock.yaml`."

### From verbose to concise

❌ "When modifying API endpoints in the OpenAPI spec file, you need to regenerate the TypeScript client by running the generate command, otherwise the types won't match at runtime and you'll get errors."
✅ "After editing `openapi.yaml`: run `pnpm run generate:api` to regenerate TS client."

### From conditional to absolute

❌ "Sometimes you need to restart the dev server after changing environment variables."
✅ "Restart dev server after any `.env` change — hot reload doesn't pick up env vars."

## Anti-Patterns

### Don't promote:
- **One-time debugging notes** — "Fixed the CORS issue by adding header X" (unless it recurs)
- **Session-specific context** — "We decided to use Approach A in today's meeting"
- **Unstable patterns** — "Currently using v3 of the API" (will change)
- **Obvious things** — "Run tests before committing" (Claude knows this)
- **Credentials or secrets** — never store in any memory file

### Don't duplicate:
- If CLAUDE.md already says "Use pnpm", don't also keep it in MEMORY.md
- After promoting, remove the source entry to free space

## Promotion Workflow

```
1. /si:review identifies candidate
2. Confirm the pattern is still valid
3. Distill into one-line instruction
4. /si:promote writes to CLAUDE.md or rules/
5. Remove from MEMORY.md
6. Verify with /si:status
```

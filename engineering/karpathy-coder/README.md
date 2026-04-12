# karpathy-coder

> **Active coding discipline enforcer** based on [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

Not just guidelines — ships Python tools that **detect** violations, a review agent, a slash command, and a pre-commit hook.

## The 4 principles

| # | Principle | What it prevents | Tool that checks it |
|---|---|---|---|
| 1 | **Think Before Coding** | Hidden assumptions, silent choices | `assumption_linter.py` |
| 2 | **Simplicity First** | Over-engineering, premature abstractions | `complexity_checker.py` |
| 3 | **Surgical Changes** | Diff noise, drive-by refactors | `diff_surgeon.py` |
| 4 | **Goal-Driven Execution** | Vague plans, missing verification | `goal_verifier.py` |

## Quick start

```bash
# Install as Claude Code plugin
/plugin marketplace add alirezarezvani/claude-skills
/plugin install karpathy-coder@claude-code-skills

# Run before committing
/karpathy-check

# Or use individual tools from the shell
python scripts/complexity_checker.py src/ --threshold strict
python scripts/diff_surgeon.py --diff HEAD~1..HEAD
echo "I'll just export all user data" | python scripts/assumption_linter.py -
python scripts/goal_verifier.py plan.md
```

## What's in the box

| Piece | Count | Detail |
|---|---|---|
| SKILL.md | 1 | The 4 principles with `context: fork` for skill chaining |
| Python tools | 4 | `complexity_checker`, `diff_surgeon`, `assumption_linter`, `goal_verifier` — all stdlib-only |
| Sub-agent | 1 | `karpathy-reviewer` — runs all 4 principles against a diff |
| Slash command | 1 | `/karpathy-check` — one-command pre-commit review |
| Pre-commit hook | 1 | `karpathy-gate.sh` — non-blocking awareness gate |
| Reference docs | 3 | Full Karpathy context, 10+ anti-pattern examples, 4-level enforcement guide |

## The tools

### complexity_checker.py (Principle #2)

Detects over-engineering: cyclomatic complexity, class density, nesting depth, function length, premature ABC/Protocol usage, import coupling.

```bash
python scripts/complexity_checker.py src/auth/ --threshold strict --json
# → score 72/100, 3 findings: nesting depth 6, function 'validate' 62 lines, 2 classes in 80 lines
```

Three threshold levels: `strict` (new code), `medium` (default), `relaxed` (legacy).

### diff_surgeon.py (Principle #3)

Analyzes a git diff and flags lines that don't trace to the stated goal: comment-only changes, whitespace noise, style drift (quote swaps), drive-by refactors, docstring additions to unchanged functions.

```bash
python scripts/diff_surgeon.py                    # staged changes
python scripts/diff_surgeon.py --diff HEAD~3..HEAD # last 3 commits
# → Noise ratio: 23% (NOISY), 7 comment-only changes, 2 quote-style swaps
```

### assumption_linter.py (Principle #1)

Reads a plan or proposal and flags hidden assumptions: "just" (hides complexity), "obviously" (unstated assumption), "should work" (hopeful, not verified), vague action verbs, unscoped user references, missing format specifications.

```bash
echo "I'll just add a function to export all user data" | python scripts/assumption_linter.py -
# → 3 findings: assumption-just, missing-format, scope-absolute
```

### goal_verifier.py (Principle #4)

Scores each step of a plan for verification quality (0-3 per step). Flags vague criteria ("should work"), checks for final end-to-end verification, and recommends concrete checks.

```bash
python scripts/goal_verifier.py implementation-plan.md --json
# → 6 steps, 8/18 (44%), WEAK — 3 steps have no verification
```

## Enforcement levels

1. **Passive** — install plugin, principles load as context (~60% compliance)
2. **Active review** — run `/karpathy-check` before commits (~85%)
3. **Pre-commit hook** — wire `karpathy-gate.sh` via Husky (~95%)
4. **CI gate** — add tools to GitHub Actions PR checks (~99%)

See `references/enforcement-patterns.md` for setup instructions at each level.

## Cross-tool compatibility

The tools are pure Python stdlib. The principles work in any AGENTS.md-aware CLI (Codex, Cursor, Antigravity, OpenCode, Gemini CLI).

## Attribution

Derived from [Andrej Karpathy's X post](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls. The principles are Karpathy's observations; the tooling, enforcement patterns, and anti-pattern gallery are original.

## License

MIT.

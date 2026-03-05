# Playwright Pro

> Production-grade Playwright testing toolkit for AI coding agents.

Generate tests, fix flaky failures, migrate from Cypress/Selenium, sync with TestRail, run on BrowserStack — all from your AI agent.

## Install

```bash
# Claude Code plugin
claude plugin install pw@claude-skills

# Or load directly
claude --plugin-dir ./engineering-team/playwright-pro
```

## Commands

| Command | What it does |
|---|---|
| `/pw:init` | Set up Playwright in your project — detects framework, generates config, CI, first test |
| `/pw:generate <spec>` | Generate tests from a user story, URL, or component name |
| `/pw:review` | Review existing tests for anti-patterns and coverage gaps |
| `/pw:fix <test>` | Diagnose and fix a failing or flaky test |
| `/pw:migrate` | Migrate from Cypress or Selenium to Playwright |
| `/pw:coverage` | Analyze what's tested vs. what's missing |
| `/pw:testrail` | Sync with TestRail — read cases, push results, create runs |
| `/pw:browserstack` | Run tests on BrowserStack, pull cross-browser reports |
| `/pw:report` | Generate a test report in your preferred format |

## Quick Start

```bash
# In Claude Code:
/pw:init                              # Set up Playwright
/pw:generate "user can log in"        # Generate your first test
# Tests are auto-validated by hooks — no extra steps
```

## What's Inside

### 9 Skills

Slash commands that turn natural language into production-ready Playwright tests. Each skill leverages Claude Code's built-in capabilities (`/batch` for parallel work, `Explore` for codebase analysis, `/debug` for trace inspection).

### 3 Specialized Agents

- **test-architect** — Plans test strategy for complex applications
- **test-debugger** — Diagnoses flaky tests using a systematic taxonomy
- **migration-planner** — Creates file-by-file migration plans from Cypress/Selenium

### 55 Test Templates

Ready-to-use, parametrizable templates covering:

| Category | Count | Examples |
|---|---|---|
| Authentication | 8 | Login, logout, SSO, MFA, password reset, RBAC |
| CRUD | 6 | Create, read, update, delete, bulk ops |
| Checkout | 6 | Cart, payment, coupon, order history |
| Search | 5 | Basic search, filters, sorting, pagination |
| Forms | 6 | Multi-step, validation, file upload |
| Dashboard | 5 | Data loading, charts, export |
| Settings | 4 | Profile, password, notifications |
| Onboarding | 4 | Registration, email verify, welcome tour |
| Notifications | 3 | In-app, toast, notification center |
| API | 5 | REST CRUD, GraphQL, error handling |
| Accessibility | 3 | Keyboard nav, screen reader, contrast |

### 2 MCP Integrations

- **TestRail** — Read test cases, create runs, push pass/fail results
- **BrowserStack** — Trigger cross-browser runs, pull session reports with video/screenshots

### Smart Hooks

- Auto-validates test quality when you write `*.spec.ts` files
- Auto-detects Playwright projects on session start
- Zero configuration required

## Integrations Setup

### TestRail (Optional)

Set environment variables:

```bash
export TESTRAIL_URL="https://your-instance.testrail.io"
export TESTRAIL_USER="your@email.com"
export TESTRAIL_API_KEY="your-api-key"
```

Then use `/pw:testrail` to sync test cases and push results.

### BrowserStack (Optional)

```bash
export BROWSERSTACK_USERNAME="your-username"
export BROWSERSTACK_ACCESS_KEY="your-access-key"
```

Then use `/pw:browserstack` to run tests across browsers.

## Works With

| Agent | How |
|---|---|
| **Claude Code** | Full plugin — slash commands, MCP tools, hooks, agents |
| **Codex CLI** | Copy `CLAUDE.md` to your project root as `AGENTS.md` |
| **OpenClaw** | Use as a skill with `SKILL.md` entry point |

## Built-in Command Integration

Playwright Pro doesn't reinvent what your AI agent already does. It orchestrates built-in capabilities:

- `/pw:generate` uses Claude's `Explore` subagent to understand your codebase before generating tests
- `/pw:migrate` uses `/batch` for parallel file-by-file conversion on large test suites
- `/pw:fix` uses `/debug` for trace analysis alongside Playwright-specific diagnostics
- `/pw:review` extends `/review` with Playwright anti-pattern detection

## Reference

Based on battle-tested patterns from production test suites. Includes curated guidance on:

- Locator strategies and priority hierarchy
- Assertion patterns and auto-retry behavior
- Fixture architecture and composition
- Common pitfalls (top 20, ranked by frequency)
- Flaky test diagnosis taxonomy

## License

MIT

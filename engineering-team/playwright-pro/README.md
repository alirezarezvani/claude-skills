# Playwright Pro

> Production-grade Playwright testing toolkit for AI coding agents.

Generate tests, fix flaky failures, and migrate from Cypress/Selenium — all from your AI agent. Optional TestRail/BrowserStack integrations are included but must be enabled manually (see [Integrations Setup](#integrations-setup)).

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
| `/pw:pw-init` | Set up Playwright in your project — detects framework, generates config, CI, first test |
| `/pw:generate <spec>` | Generate tests from a user story, URL, or component name |
| `/pw:pw-review` | Review existing tests for anti-patterns and coverage gaps |
| `/pw:fix <test>` | Diagnose and fix a failing or flaky test |
| `/pw:migrate` | Migrate from Cypress or Selenium to Playwright |
| `/pw:coverage` | Analyze what's tested vs. what's missing |
| `/pw:testrail` | Sync with TestRail — read cases, push results, create runs *(requires manual MCP setup — see [Integrations Setup](#integrations-setup))* |
| `/pw:browserstack` | Run tests on BrowserStack, pull cross-browser reports *(requires manual MCP setup — see [Integrations Setup](#integrations-setup))* |
| `/pw:report` | Generate a test report in your preferred format |

## Quick Start

```bash
# In Claude Code:
/pw:pw-init                              # Set up Playwright
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

### 3 MCP Integrations (optional — not auto-registered, see [Integrations Setup](#integrations-setup))

- **TestRail** — Read test cases, create runs, push pass/fail results
- **BrowserStack** — Trigger cross-browser runs, pull session reports with video/screenshots
- **e2e** — Drive iOS/Android apps and web pages from a live session, run plain-language test flows

### Smart Hooks

- Auto-validates test quality when you write `*.spec.ts` files
- Auto-detects Playwright projects on session start
- Zero configuration required

## Integrations Setup

> **Note (issue #978):** the TestRail and BrowserStack MCP servers are **not
> auto-registered** — they were removed from the plugin's `.mcp.json` because they
> failed to connect for every user (no bundled `node_modules`). Setting the env
> vars below is **not** enough on its own; `/pw:testrail` and `/pw:browserstack`
> will fail with "tool not found" until you enable the server manually
> (`cd integrations/<name>-mcp && npm install`, then register it in your own
> user/project MCP config). See the **Integrations** section of `CLAUDE.md`.

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

### e2e (Optional)

For iOS and Android apps, which Playwright does not cover, or for tests written
as plain-language steps. An agent writes the flow while it drives the app, and
later runs replay the recorded steps without model calls. The server ships on
npm, so there is no `npm install` step inside the plugin.

Add the `e2e` entry from `integrations/mcp-servers.example.json` to your
user/project MCP config, or register it with:

```bash
claude mcp add --scope project e2e -- npx -y e2e mcp
```

Start Claude Code in the project you want to test. `npx e2e init` sets up a
project config; the server itself needs no API key or model.

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
- `/pw:pw-review` extends `/review` with Playwright anti-pattern detection

## Reference

Based on battle-tested patterns from production test suites. Includes curated guidance on:

- Locator strategies and priority hierarchy
- Assertion patterns and auto-retry behavior
- Fixture architecture and composition
- Common pitfalls (top 20, ranked by frequency)
- Flaky test diagnosis taxonomy

## License

MIT

# Playwright Pro — Agent Context

You are working in a project with the Playwright Pro plugin installed. Follow these rules for all test-related work.

## Golden Rules (Non-Negotiable)

1. **`getByRole()` over CSS/XPath** — resilient to markup changes, mirrors how users see the page
2. **Never `page.waitForTimeout()`** — use `expect(locator).toBeVisible()` or `page.waitForURL()`
3. **Web-first assertions** — `expect(locator)` auto-retries; `expect(await locator.textContent())` does not
4. **Isolate every test** — no shared state, no execution-order dependencies
5. **`baseURL` in config** — zero hardcoded URLs in tests
6. **Retries: `2` in CI, `0` locally** — surface flakiness where it matters
7. **Traces: `'on-first-retry'`** — rich debugging without CI slowdown
8. **Fixtures over globals** — share state via `test.extend()`, not module-level variables
9. **One behavior per test** — multiple related `expect()` calls are fine
10. **Mock external services only** — never mock your own app

## Locator Priority

Always use the first option that works:

```typescript
page.getByRole('button', { name: 'Submit' })        // 1. Role (default)
page.getByLabel('Email address')                     // 2. Label (form fields)
page.getByText('Welcome back')                       // 3. Text (non-interactive)
page.getByPlaceholder('Search...')                    // 4. Placeholder
page.getByAltText('Company logo')                    // 5. Alt text (images)
page.getByTitle('Close dialog')                      // 6. Title attribute
page.getByTestId('checkout-summary')                 // 7. Test ID (last semantic)
page.locator('.legacy-widget')                       // 8. CSS (last resort)
```

## How to Use This Plugin

### Generating Tests

When generating tests, always:

1. Use the `Explore` subagent to scan the project structure first
2. Check `playwright.config.ts` for `testDir`, `baseURL`, and project settings
3. Load relevant templates from `templates/` directory
4. Match the project's language (check for `tsconfig.json` → TypeScript, else JavaScript)
5. Place tests in the configured `testDir` (default: `tests/` or `e2e/`)
6. Include a descriptive test name that explains the behavior being verified

### Reviewing Tests

When reviewing, check against:

1. All 10 golden rules above
2. The anti-patterns in `skills/review/anti-patterns.md`
3. Missing edge cases (empty state, error state, loading state)
4. Proper use of fixtures for shared setup

### Fixing Flaky Tests

When fixing flaky tests:

1. Categorize first: timing, isolation, environment, or infrastructure
2. Use `npx playwright test <file> --repeat-each=10` to reproduce
3. Use `--trace=on` for every attempt
4. Apply the targeted fix from `skills/fix/flaky-taxonomy.md`

### Using Built-in Commands

Leverage Claude Code's built-in capabilities:

- **Large migrations**: Use `/batch` for parallel file-by-file conversion
- **Post-generation cleanup**: Use `/simplify` after generating a test suite
- **Debugging sessions**: Use `/debug` alongside `/pw:fix` for trace analysis
- **Code review**: Use `/review` for general code quality, `/pw:review` for Playwright-specific

### Integrations

- **TestRail**: Configured via `TESTRAIL_URL`, `TESTRAIL_USER`, `TESTRAIL_API_KEY` env vars
- **BrowserStack**: Configured via `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY` env vars
- Both are optional. The plugin works fully without them.

## File Conventions

- Test files: `*.spec.ts` or `*.spec.js`
- Page objects: `*.page.ts` in a `pages/` directory
- Fixtures: `fixtures.ts` or `fixtures/` directory
- Test data: `test-data/` directory with JSON/factory files

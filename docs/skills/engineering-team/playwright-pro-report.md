---
title: "Smart Test Reporting"
description: "Smart Test Reporting - Claude Code skill from the Engineering - Core domain."
---

# Smart Test Reporting

<div class="page-meta" markdown>
<span class="meta-badge">:material-code-braces: Engineering - Core</span>
<span class="meta-badge">:material-identifier: `report`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering-team/playwright-pro/skills/report/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-skills</code>
</div>


Generate test reports that plug into the user's existing workflow. Zero new tools.

## Steps

### 1. Run Tests (If Not Already Run)

Check if recent test results exist:

```bash
ls -la test-results/ playwright-report/ 2>/dev/null
```

If no recent results, run tests:

```bash
npx playwright test --reporter=json,html,list 2>&1 | tee test-output.log
```

### 2. Parse Results

Read the JSON report:

```bash
npx playwright test --reporter=json 2> /dev/null
```

Extract:
- Total tests, passed, failed, skipped, flaky
- Duration per test and total
- Failed test names with error messages
- Flaky tests (passed on retry)

### 3. Detect Report Destination

Check what's configured and route automatically:

| Check | If found | Action |
|---|---|---|
| `TESTRAIL_URL` env var | TestRail configured | Push results via `/pw:testrail push` |
| `SLACK_WEBHOOK_URL` env var | Slack configured | Post summary to Slack |
| `.github/workflows/` | GitHub Actions | Results go to PR comment via artifacts |
| `playwright-report/` | HTML reporter | Open or serve the report |
| None of the above | Default | Generate markdown report |

### 4. Generate Report

#### Markdown Report (Always Generated)

```markdown
# Test Results — {{date}}

## Summary
- ✅ Passed: {{passed}}
- ❌ Failed: {{failed}}
- ⏭️ Skipped: {{skipped}}
- 🔄 Flaky: {{flaky}}
- ⏱️ Duration: {{duration}}

## Failed Tests
| Test | Error | File |
|---|---|---|
| {{name}} | {{error}} | {{file}}:{{line}} |

## Flaky Tests
| Test | Retries | File |
|---|---|---|
| {{name}} | {{retries}} | {{file}} |

## By Project
| Browser | Passed | Failed | Duration |
|---|---|---|---|
| Chromium | X | Y | Zs |
| Firefox | X | Y | Zs |
| WebKit | X | Y | Zs |
```

Save to `test-reports/{{date}}-report.md`.

#### Slack Summary (If Webhook Configured)

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "🧪 Test Results: ✅ {{passed}} | ❌ {{failed}} | ⏱️ {{duration}}\n{{failed_details}}"
  }'
```

#### TestRail Push (If Configured)

Invoke `/pw:testrail push` with the JSON results.

#### HTML Report

```bash
npx playwright show-report
```

Or if in CI:
```bash
echo "HTML report available at: playwright-report/index.html"
```

### 5. Trend Analysis (If Historical Data Exists)

If previous reports exist in `test-reports/`:
- Compare pass rate over time
- Identify tests that became flaky recently
- Highlight new failures vs. recurring failures

## Output

- Summary with pass/fail/skip/flaky counts
- Failed test details with error messages
- Report destination confirmation
- Trend comparison (if historical data available)
- Next action recommendation (fix failures or celebrate green)

---
name: "ux-audit"
description: "Use when auditing a website for UX, UI, or accessibility issues — before launch, during code review, or after a redesign. Triggers: check accessibility, run UX audit, validate WCAG compliance, audit a landing page, Core Web Vitals check, or compare scores before/after changes."
---

# UXLens — Website UX Audit

Run a full UX/UI/accessibility audit on any URL in seconds. Get back specific issues, severity levels, and prioritized fixes — plus an `agent_summary` paragraph you can read aloud and act on immediately.

## When to Use

- Before launching a landing page or portfolio
- During code review on UI changes
- After a redesign to verify improvements
- When someone reports "the site feels broken"
- To validate accessibility before shipping

## How It Works

The skill calls the UXLens API (`https://uxlens.io/api/audit`) with the target URL and returns a structured audit report. No browser needed — works from the terminal.

## Setup

Get a free API key at **https://uxlens.io/dashboard** (5 audits/month free, no credit card required).

```bash
export UXLENS_API_KEY=your_key_here
```

## Core Workflow

### Single URL Audit

```
You: /ux-audit https://mysite.com
Claude: *runs the audit*
Score: 3.8/5 — Good

Critical (2):
  1. [CRITICAL] 4 images missing alt text
  2. [CRITICAL] No skip navigation link for keyboard users

Major (3):
  1. [MAJOR] CTA button contrast ratio 2.1:1 (needs 4.5:1 for WCAG AA)
  2. [MAJOR] No focus indicator on navigation links
  3. [MAJOR] Forms missing associated <label> elements

Estimated fix time: 45 minutes
Shall I fix these?
```

### Full Site Crawl

```bash
curl -X POST https://uxlens.io/api/audit \
  -H "Authorization: Bearer $UXLENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mysite.com","crawl_all":true,"max_pages":20}'
```

### Diff Mode (before/after redesign)

```bash
# First audit — save audit_id from response
curl -X POST https://uxlens.io/api/audit \
  -H "Authorization: Bearer $UXLENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mysite.com"}'
# Returns: {"audit_id": "uxl_a1b2c3d4", ...}

# Second audit with comparison
curl -X POST https://uxlens.io/api/audit \
  -H "Authorization: Bearer $UXLENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://mysite.com","compare_to":"uxl_a1b2c3d4"}'
# Returns: score_delta, new_issues, fixed_issues
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `overall` | number | 0–5 score (e.g. 3.8 = "Good") |
| `status` | string | World-Class / Excellent / Good / Fair / Poor |
| `agent_summary` | string | One-paragraph summary — safe to read aloud |
| `audit_id` | string | Use with `compare_to` for diff mode |
| `uxIssues[]` | array | Usability violations (critical/major/minor) |
| `uiIssues[]` | array | Design issues (spacing, typography, hierarchy) |
| `a11yIssues[]` | array | WCAG accessibility violations |
| `lighthouse` | object | Performance, SEO, Accessibility scores (0–100) |
| `coreWebVitals` | object | LCP, CLS, FCP, INP with pass/fail |

### Example agent_summary

```
UXLens audit of example.com: Score 3.8/5 (Good). 2 critical issues — 4 images missing alt text, 
no skip navigation link. 3 major issues including low contrast on CTA button. 
Estimated fix time: 45min.
```

## API Reference

**Base URL:** `https://uxlens.io/api/audit`
**Auth:** `Authorization: Bearer $UXLENS_API_KEY`

## Pricing

| Tier | Price | Audits/month |
|------|-------|-------------|
| Free | $0 | 5 |
| Developer | $9.99/mo | 500 |
| Pro | $29/mo | 3,000 |

---

*UXLens — https://uxlens.io | MIT License*

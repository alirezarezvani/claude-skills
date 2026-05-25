---
name: "social-publishing"
description: "When the user wants to schedule or publish social media posts across multiple platforms using SocialClaw. Use when the user mentions 'schedule post', 'publish to X', 'LinkedIn post', 'social media automation', 'connect social accounts', 'SocialClaw', or wants to send content to X, LinkedIn, Instagram, Facebook Pages, TikTok, Discord, Telegram, YouTube, Reddit, WordPress, or Pinterest. For writing social post copy, see social-content. For social strategy, see social-media-manager."
license: MIT
metadata:
  version: 1.0.0
  author: ndesv21
  category: marketing
  updated: 2026-05-25
---

# Social Publishing (SocialClaw)

You are a social media publishing agent. Your job is to help the user schedule and publish content across social platforms via [SocialClaw](https://getsocialclaw.com) — an agent-first social publishing API.

## Runtime Requirements

- `SC_API_KEY` — workspace API key from [https://getsocialclaw.com/dashboard](https://getsocialclaw.com/dashboard)
- Optional: `socialclaw` CLI (`npm install -g socialclaw`)
- Active trial or paid plan required for publishing

## Setup

```bash
# Set workspace API key
export SC_API_KEY="<workspace-key>"

# Verify access
curl -sS -H "Authorization: Bearer $SC_API_KEY" https://getsocialclaw.com/v1/keys/validate

# Install CLI (optional but recommended)
npm install -g socialclaw
socialclaw login --api-key <workspace-key>
```

## Workflow

### 1. List connected accounts
```bash
socialclaw accounts list --json
```

If no accounts are connected, direct the user to connect via the dashboard or CLI:
```bash
socialclaw accounts connect --provider x --open
socialclaw accounts connect --provider linkedin --open
```

### 2. Upload media (if needed)
```bash
socialclaw assets upload --file ./image.png --json
# Returns: { "asset_id": "..." }
```

### 3. Build a schedule file
Create `schedule.json` with the posts to publish:

```json
{
  "posts": [
    {
      "provider": "x",
      "account_id": "<account-id>",
      "text": "Post content here",
      "scheduled_at": "2026-06-01T10:00:00Z"
    },
    {
      "provider": "linkedin",
      "account_id": "<account-id>",
      "text": "LinkedIn version of the post",
      "scheduled_at": "2026-06-01T10:00:00Z"
    }
  ]
}
```

### 4. Validate before publishing
```bash
socialclaw validate -f schedule.json --json
```

Fix any validation errors before proceeding.

### 5. Publish
```bash
socialclaw apply -f schedule.json --json
# Returns: { "run_id": "..." }
```

### 6. Monitor
```bash
socialclaw status --run-id <run-id> --json
socialclaw posts list --json
```

## Supported Providers

| Provider | Key | Notes |
|----------|-----|-------|
| X (Twitter) | `x` | Text + up to 4 images or 1 video |
| LinkedIn profile | `linkedin` | Up to 20 images or 1 video |
| LinkedIn page | `linkedin_page` | Requires page admin access |
| Instagram Business | `instagram_business` | Requires Facebook Page link |
| Instagram standalone | `instagram` | Professional accounts only |
| Facebook Page | `facebook` | Pages only |
| TikTok | `tiktok` | 1 video or 1–35 images |
| YouTube | `youtube` | Native video upload |
| Reddit | `reddit` | Requires subreddit |
| WordPress | `wordpress` | WordPress.com or Jetpack |
| Discord | `discord` | Webhook URL required |
| Telegram | `telegram` | Bot token + chat ID |
| Pinterest | `pinterest` | Board-centric |

## Security

- Outbound requests go to `getsocialclaw.com` only
- Provider secrets are never handled by the agent — users connect accounts via OAuth in the SocialClaw dashboard
- The `SC_API_KEY` is a workspace-scoped key, not a provider OAuth token

## MUST DO

- Always run `socialclaw validate` before `socialclaw apply`
- Confirm with the user before publishing to live accounts
- Use `--json` flag on all CLI calls for machine-readable output

## MUST NOT DO

- Never store `SC_API_KEY` in files committed to version control
- Never publish without validating first
- Never assume account IDs — always fetch them with `socialclaw accounts list`

## Source

- GitHub: [https://github.com/ndesv21/socialclaw](https://github.com/ndesv21/socialclaw)
- npm: [https://www.npmjs.com/package/socialclaw](https://www.npmjs.com/package/socialclaw)
- Dashboard: [https://getsocialclaw.com/dashboard](https://getsocialclaw.com/dashboard)

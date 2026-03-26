# Secret Pattern Reference

## High-Confidence Patterns (confidence >= 0.85 on match)

| Secret Type | Regex Pattern | Entropy Threshold |
|---|---|---|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | > 3.5 |
| AWS Secret Key | `[0-9a-zA-Z/+]{40}` following access key context | > 4.5 |
| GitHub PAT (classic) | `ghp_[A-Za-z0-9]{36}` | N/A — pattern sufficient |
| GitHub OAuth | `gho_[A-Za-z0-9]{36}` | N/A |
| GitHub Actions | `ghs_[A-Za-z0-9]{36}` | N/A |
| Stripe Live Key | `sk_live_[A-Za-z0-9]{24,}` | N/A |
| Slack Bot Token | `xoxb-[0-9]{11,}-[0-9]{11,}-[a-zA-Z0-9]{24}` | N/A |
| Slack User Token | `xoxp-[0-9]+-[0-9]+-[0-9]+-[a-f0-9]{32}` | N/A |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` | N/A |
| SSH Private Key | `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----` | N/A |
| PEM Certificate | `-----BEGIN CERTIFICATE-----` with private key context | N/A |
| Twilio Account SID | `AC[a-z0-9]{32}` | N/A |
| Twilio Auth Token | `[a-z0-9]{32}` in Twilio context | > 4.0 |
| SendGrid API Key | `SG\.[A-Za-z0-9\._]{68}` | N/A |

## False Positive Patterns (reduce confidence to 0.10)

- Value contains: `EXAMPLE`, `PLACEHOLDER`, `YOUR_`, `XXXX`, `REPLACE_ME`, `TODO`
- Value is all same character repeated: `aaaaaaa`, `0000000`
- Value is in a test file path: `__tests__`, `spec`, `.test.`, `mock`, `fixture`
- Variable is clearly a comment: `# example_key = "abc123"`
- Value matches a UUID format (not a secret)

## Blast Radius by Secret Type

| Secret Type | Blast Radius | Notes |
|---|---|---|
| `aws_access_key` | `full_account` | Unless restricted by permission boundary |
| `stripe_live_key` | `full_account` | Full payment processing capability |
| `github_pat` | `service_scoped` | Limited to repos the token owner can access |
| `ssh_private_key` | `full_account` or `service_scoped` | Depends on what systems the key grants access to |
| `database_url` | `service_scoped` | Limited to that database |
| `stripe_test_key` | `minimal` | Test environment only |
| `generic_api_key` | `service_scoped` | Assess by service context |

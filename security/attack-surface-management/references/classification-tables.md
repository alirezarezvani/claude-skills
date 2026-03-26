# ASM Classification Tables

## Exposure Scoring Matrix

| Exposure Class | Definition | Base Risk Multiplier |
|---|---|---|
| Internet-Facing | Directly reachable from public internet | 3.0x |
| Cloud-Perimeter | Behind cloud WAF or CDN but publicly routable | 2.0x |
| Partner-Accessible | Exposed via B2B VPN or API gateway to third parties | 1.5x |
| Internal | Accessible only from corporate network | 0.8x |
| Isolated | Air-gapped or no network connectivity | 0.2x |

## Certificate Expiry Warning Thresholds

| Days to Expiry | Status | Action Required |
|---|---|---|
| > 30 days | OK | Monitor only |
| 30 days | Warning | Notify certificate owner |
| 14 days | High | Escalate to infrastructure team |
| 7 days | Critical | Immediate renewal — page on-call |
| 0 days (expired) | Critical-Breach | Immediate remediation — certificate breach active |

## Subdomain Takeover Indicators

| Pattern | Risk | Description |
|---|---|---|
| CNAME points to decommissioned AWS S3 bucket | Critical | Bucket name available for registration |
| CNAME points to Heroku app returning 404 | Critical | App name available for claim |
| CNAME points to GitHub Pages — no matching repo | High | Page can be claimed via GitHub account |
| CNAME points to Fastly — no active service | High | Service endpoint claimable |
| Dangling A record pointing to released Elastic IP | High | IP can be reassigned by any AWS customer |
| NS record pointing to decommissioned DNS provider | Critical | Full domain takeover via provider account creation |

## Admin Interface Risk Classification

| Service | Default Path | Exposure Risk |
|---|---|---|
| Jenkins | /jenkins, :8080 | Critical — code execution capability |
| GitLab | /gitlab, :8080 | Critical — source code and CI/CD access |
| Kubernetes Dashboard | /dashboard, :8001 | Critical — cluster control plane |
| AWS Console | console.aws.amazon.com | Critical — full cloud account control |
| Grafana | /grafana, :3000 | High — monitoring data exposure |
| Elasticsearch | :9200, :9300 | Critical — unauthenticated data access |
| Redis | :6379 | Critical — unauthenticated data read/write |
| MongoDB | :27017 | Critical — unauthenticated database access |
| Jupyter Notebook | :8888 | Critical — arbitrary code execution |

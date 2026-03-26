# TLS Architecture Pre-Check

Before asserting any attack path involving session token theft or credential harvesting via the compromised perimeter device, first validate the TLS architecture of the traffic path.

| Question | If YES | If NO |
|---|---|---|
| Does the firewall perform SSL/TLS inspection (deep packet inspection) on the traffic path? | Session tokens, OAuth tokens, API keys in HTTP headers are visible at the firewall and can be harvested | HTTPS traffic is encrypted end-to-end at this device — tokens in transit are not accessible at the firewall layer |
| Is a forward proxy in the traffic path that terminates TLS? | Tokens are accessible at the proxy, not the firewall | Does not change firewall analysis |
| Does the identity provider enforce HSTS + certificate pinning? | Redirect/intercept attack is blocked even with SSL inspection | Standard TLS inspection may still apply |

## Okta Session Token Theft — Specific Analysis

Okta enforces HTTPS with HSTS. Okta session tokens are not accessible at a compromised firewall unless SSL inspection is active on Okta traffic.

Valid theft vectors at the firewall (without SSL inspection):
- DNS hijacking: redirect Okta DNS resolution to attacker-controlled server (requires attacker controls DNS resolver or DNS cache on a reachable device)
- ARP/routing manipulation to redirect Okta-bound traffic through attacker-controlled host

Invalid theft vector at the firewall (without SSL inspection):
- "Firewall reads Okta session tokens from HTTPS egress" — tokens are encrypted; this assertion must not be made unless SSL inspection is confirmed.

Assess SSL inspection status as a prerequisite before including Okta credential theft in the attack path. Mark as `TLS_ARCHITECTURE_UNVERIFIED` if SSL inspection status is unknown.

# Compensating Controls — Detailed Options

Compensating controls are temporary risk reduction measures. They must be documented as temporary, with a defined expiry trigger (patch release or quarterly review). Each control requires human approval before MCP deployment.

Order controls by deployment speed — implement the fastest controls first to close the exploit window before longer-lead controls are ready.

## Control Option 0: Immediate Traffic Controls (Deploy First — Minutes to Implement)

When the exploit window is shorter than the time required to deploy WAF rules or network blocks, immediate traffic controls buy time for defenders.

| Control | Implementation Time | Scope | Limitation |
|---|---|---|---|
| Geoblocking | 5-15 minutes | Block source ASNs/countries not in business operational scope | Ineffective against attackers using domestic infrastructure or VPN egress in scope countries |
| Connection rate limiting | 5-10 minutes | Limit connection attempts per source IP to the affected service/port | Does not stop slow, low-rate exploitation |
| Known scanner IP blocking | 5-10 minutes | Block Shodan, Censys, Shadowserver, GreyNoise scanner IP ranges | Reduces reconnaissance noise; does not stop targeted attacks |
| WAF emergency mode / high paranoia | 10-30 minutes | Switch WAF ruleset to maximum sensitivity for affected endpoint paths | Increased false-positive risk — validate against production traffic before declaring success |
| Service-level allowlisting | 5-15 minutes | Restrict affected service to known-good source IPs only | Only viable if the affected service has a defined set of known legitimate sources |

Immediate controls are NOT a substitute for WAF rule deployment or network segmentation. They are a bridge measure deployed while longer-lead controls are being prepared and approved.

Approval required: `network_change` mutating intent, `soc_lead` minimum.

## Control Option 1: WAF Rule Deployment

Apply a web application firewall rule that blocks or sanitizes the attack payload pattern.

Requirements before deployment:
- Rule must be tested in detection-only mode for a minimum of 1 hour with no false-positive alerts against production traffic.
- Rule must have a rollback procedure documented.
- Rule must be assigned an expiry review date.

Limitations: WAF rules protect HTTP/HTTPS attack vectors only. They provide no protection for internal service-to-service exploitation or non-web protocol attacks.

## Control Option 2: Network Block / Segmentation

Block network access to the vulnerable service from untrusted networks or restrict to approved source IP ranges.

Implementation options in order of preference:
1. Security group or firewall rule change to restrict access to the affected port and service.
2. Network ACL update at the perimeter.
3. Service-level IP allowlist if the application supports it.

Risk: Blocking external access may disrupt legitimate users. Validate with the business owner before deployment.

## Control Option 3: Feature Disable or Killswitch

If the vulnerability is in a specific feature of the product, disable that feature at the application or configuration level without disabling the entire service.

Decision criteria: Feature disable is preferred over full service shutdown when the disabled feature is not on the critical path for core business operations.

## Control Option 4: Service Isolation

For critical exploits with no viable WAF or network block option, isolate the affected service by removing it from the production network and switching to an alternative or degraded service mode.

This is the highest-impact compensating control and requires CISO approval.

## Control Option 5: Increase Detection Sensitivity

When the exploit cannot be blocked without unacceptable service disruption, increase detection sensitivity:
- Enable verbose logging on the affected service (after completing logging-preflight.md checks).
- Create custom SIEM detection rules for exploitation behaviors.
- Lower alerting thresholds for anomalies on affected hosts.
- Assign dedicated analyst monitoring for 24 hours.

This control does not prevent exploitation but reduces dwell time if exploitation occurs.

# Proactive Triggers

Surface the following without being asked, whenever the condition is met:

- **SEV2 or above with no regulatory scope check completed**: Immediately surface notification deadline status — state the applicable frameworks and their T+0 deadlines before any other analysis.
- **SEV1 AND SIEM or CloudTrail is reported as disabled**: Flag GDPR Art.33 72-hour notification clock — defense evasion active means the organization cannot prove absence of data exfiltration; clock starts now.
- **More than 30 minutes elapsed since SEV1 declaration with no containment authorization logged**: Flag SLA breach risk — the T+15 containment window has been exceeded; state current elapsed time and escalation path.
- **Response tracks assigned but forensics not yet activated**: Flag volatile evidence loss risk — memory, active network connections, and running processes are being lost while forensics is pending.
- **Third-party or vendor system identified as involved**: Flag supply chain notification obligations — the vendor's own incident notification SLAs and contractual obligations must be assessed.

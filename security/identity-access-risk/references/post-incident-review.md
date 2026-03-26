# Post-Incident Review Questions (IAM)

1. **Detection gap**: When did the anomalous access begin vs. when was it detected? What was the lateral movement window?
2. **Root credential**: Which original credential was compromised? How was it obtained (phishing, secrets exposure, leaked .env)?
3. **Blast radius confirmation**: What did the attacker actually access? Review CloudTrail for all API calls during the window.
4. **Backdoor check**: Did the attacker create any persistent access (new IAM users, access keys, OAuth apps, EC2 key pairs)? Have all backdoors been removed?
5. **Policy gaps**: Which overprivileged policies enabled this path? Have they been corrected with least-privilege?
6. **Detection improvement**: Which CloudTrail event should have triggered alerting earlier? Has a rule been added?
7. **SolarWinds-style chain**: Was this a multi-hop AssumeRole attack? Map the full assumption chain.

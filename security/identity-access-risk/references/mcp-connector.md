# MCP Connector Output Contract

When producing a mutating recommendation, include these optional fields in your JSON output so the MCP layer can execute on real infrastructure:

```json
{
  "mcp_connector": "aws",
  "target": "arn:aws:iam::123456789012:user/jsmith",
  "aws_access_key_id": "AKIAZZ...",
  "source_ip": "45.33.32.156",
  "parameters": {}
}
```

Field guidance:
- `mcp_connector`: always `"aws"` for identity-access-risk (IAM policy changes)
- `target`: IAM user ARN or role ARN that needs the policy applied
- `aws_access_key_id`: specific key to deactivate (for credential_operation actions)
- `source_ip`: attacker IP if credential abuse is the trigger
- `parameters`: additional IAM context (e.g. `{"policy_arn": "arn:aws:iam::...:policy/..."}`)

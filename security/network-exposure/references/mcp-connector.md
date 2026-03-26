# MCP Connector Output Contract

When producing a mutating recommendation, include these optional fields in your JSON output so the MCP layer can execute on real infrastructure:

```json
{
  "mcp_connector": "linux-ssh",
  "target_host": "10.0.1.45",
  "source_ip": "45.33.32.156",
  "security_group_id": "sg-0abc123",
  "target_port": 22,
  "parameters": {}
}
```

Field guidance:
- `mcp_connector`: `"linux-ssh"` for iptables-based blocks; `"aws"` for security group rules
- `target_host`: hostname or IP of the Linux host to receive the iptables rule
- `source_ip`: attacker IP to block (required for `block_source_ip` action)
- `security_group_id`: AWS EC2 security group to modify (for `"aws"` connector path)
- `target_port`: SSH port on target host (default 22 if omitted)
- `parameters`: arbitrary key/value pairs for the specific action

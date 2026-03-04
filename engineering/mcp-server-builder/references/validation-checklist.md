# MCP Validation Checklist

- Tool names are unique and stable.
- All tools include practical descriptions.
- `inputSchema.type` is always `object`.
- No required fields missing from properties.
- Destructive tools require explicit confirmation inputs.
- Auth tokens are not exposed in tool schema.
- Breaking tool changes are versioned, not overwritten.

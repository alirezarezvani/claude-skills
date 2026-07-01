# Aident Loadout Troubleshooting

Use this reference after a specific Aident CLI or MCP step fails.

## CLI Not Found

1. Confirm the command is unavailable:

   ```bash
   command -v aident
   ```

2. Follow the current setup instructions:

   ```text
   https://aident.ai/SETUP.md
   ```

3. Reopen the shell if PATH changed, then run:

   ```bash
   aident --help
   ```

## Not Authenticated

Run the current login flow shown by CLI help. After login, verify the signed-in account with the relevant identity or status command.

If browser auth or out-of-band verification is required, pause and let the user complete it.

## Integration Missing Or Disconnected

1. Identify required integration ids from the selected capability details.
2. Check Vault status for those ids.
3. Start the connect flow for missing integrations.
4. Send the returned URL to the user.
5. Retry Vault status after the user authorizes.

Never substitute raw provider keys in chat unless the user explicitly rejects Vault and understands the risk.

## Schema Validation Error

1. Fetch the live capability schema again.
2. Compare required fields with the attempted payload.
3. Remove unsupported fields.
4. Retry once with a corrected minimal payload.

If the retry fails, report the exact field-level error.

## Permission Or Scope Error

The user may have connected the right app with insufficient scopes.

1. Name the missing permission if Aident reports it.
2. Ask the user to reconnect or authorize the required scope through Aident.
3. Recheck Vault status before retrying.

## MCP Tools Not Appearing

1. Confirm the configured server URL is exactly `https://loadout.aident.ai/mcp`.
2. Restart or reload the MCP client.
3. Reauthenticate if the client reports expired auth.
4. If still missing, fall back to CLI mode when available.

## Audit Verification

When the user asks what happened:

1. Query recent audit history.
2. Match by timestamp, capability name, integration, and result id.
3. Summarize only the fields needed for proof.
4. Do not print sensitive payloads.

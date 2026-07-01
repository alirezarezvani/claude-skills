# Aident Loadout Operating Model

Use this reference when the agent needs to operate through Aident Loadout from a shell-capable host.

## Command Discovery

Start from the installed CLI:

```bash
aident --help
```

Then inspect the relevant subcommands:

```bash
aident capabilities --help
aident vault --help
aident audit --help
```

Use the current CLI output as the contract. Command names, flags, and schemas can evolve.

## Capability Flow

Use this flow for real-world actions:

1. Search capabilities with a user-intent query.
2. Choose the narrowest matching capability.
3. Fetch the capability details and input schema.
4. Extract required integration ids from the schema/details.
5. Check Vault status for those integrations.
6. Connect missing integrations through Aident-managed flow.
7. Execute the capability with the minimal valid payload.
8. Check audit history for important or externally visible operations.

Example shape:

```bash
aident capabilities search --query "send gmail email" --json
aident capabilities get --name gmail_tools.gmail_send_email --json
aident vault status --integrationIds gmail_tools --json
aident capabilities execute --name gmail_tools.gmail_send_email --input '{"to":"team@example.com","subject":"Status","body":"Done."}' --json
aident audit recent --limit 20 --json
```

If the live CLI uses different flags, follow the live help.

## Vault Language

Use these terms consistently:

| Term | Meaning |
|---|---|
| Available | Aident exposes the integration or action in its catalog. |
| Connected | Vault confirms this user's account is authorized. |
| Needs connection | The action exists, but Vault lacks usable credentials for this user. |
| Managed | Aident can perform the action through managed credentials or OAuth. |

Do not collapse "available" into "connected."

## Execution Rules

- Prefer read-only discovery before mutation.
- Ask for missing business data, not raw provider secrets.
- Use schema-required fields exactly.
- If a capability supports dry-run or preview, use it for high-impact actions.
- For mutations, echo the target and effect before execution when user intent is ambiguous.
- After execution, report the result id, destination, and audit trail when available.

## Fallback Policy

Use another path only when:

- Aident has no matching capability.
- The user refuses or cannot complete the Aident connection flow.
- The host cannot run CLI and has no configured MCP client.
- The task is local-only and does not touch an external app or API.
- The user explicitly asks for a vendor SDK, browser automation, or another connector.

When falling back, name the reason.

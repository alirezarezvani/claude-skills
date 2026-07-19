# Atlassian Remote MCP — Canonical Tool Reference

**This is the single source of truth for Atlassian MCP tool names in the project-management domain.** Tool names verified live against the production Atlassian Remote MCP server (`https://mcp.atlassian.com/v1/sse`, bundled via this plugin's `.mcp.json`) on 2026-06-10.

## How tools are addressed

The bundled `.mcp.json` declares the server under the key `atlassian`, so in Claude Code each tool surfaces as:

```
mcp__atlassian__<toolName>
```

e.g. `mcp__atlassian__createJiraIssue`, `mcp__atlassian__searchConfluenceUsingCql`. (When the server is loaded through a plugin rather than a project-level `.mcp.json`, Claude Code may use a plugin-scoped prefix like `mcp__plugin_<plugin>_atlassian__<toolName>` — the trailing `<toolName>` is identical either way.) Tool names are **camelCase**, not snake_case, not CLI flags, not JSON `"tool":` blocks.

## The hard rule

> **Never invent tool names.** If a capability is not in the list below (e.g. project creation, sprint management, filter creation, space creation, page deletion, label management, field configuration, workflow/permission scheme editing, user provisioning, automation rules), it is **NOT available via MCP** — tell the user to use the Atlassian web UI (admin.atlassian.com / Jira settings / Confluence space tools) or the Atlassian REST API instead.

Parameters marked "discover via tool schema" were not verified — inspect the tool's input schema at call time rather than guessing.

## Identity & site discovery

| Tool | Purpose | Key parameters |
|---|---|---|
| `atlassianUserInfo` | Get the authenticated user's profile | none |
| `getAccessibleAtlassianResources` | List Cloud sites (and their `cloudId`s) the OAuth grant can access. **Call this first** — most other tools require `cloudId`. | none |

## Jira — read

| Tool | Purpose | Key parameters |
|---|---|---|
| `getJiraIssue` | Fetch a single issue | `cloudId`, `issueIdOrKey` |
| `searchJiraIssuesUsingJql` | Run a JQL search | `cloudId`, `jql`; pagination params — discover via tool schema |
| `getTransitionsForJiraIssue` | List transitions currently available on an issue | `cloudId`, `issueIdOrKey` |
| `getVisibleJiraProjects` | List projects the user can see | `cloudId` |
| `getJiraProjectIssueTypesMetadata` | Issue types available in a project | `cloudId`, `projectIdOrKey` |
| `getJiraIssueTypeMetaWithFields` | Field metadata for a project + issue type (use before create/edit to learn required fields) | `cloudId`, `projectIdOrKey`, issue type id — discover via tool schema |
| `getJiraIssueRemoteIssueLinks` | Remote links (e.g. Confluence pages) on an issue | `cloudId`, `issueIdOrKey` |
| `getIssueLinkTypes` | List available issue link types (Blocks, Relates, …) | `cloudId` |
| `lookupJiraAccountId` | Resolve a user (name/email) to an `accountId` | `cloudId`, search string — discover via tool schema |

## Jira — write

| Tool | Purpose | Key parameters |
|---|---|---|
| `createJiraIssue` | Create an issue | `cloudId`, `projectKey`, `issueTypeName`, `summary`; other fields — discover via tool schema |
| `editJiraIssue` | Update fields on an existing issue | `cloudId`, `issueIdOrKey`, fields payload — discover via tool schema |
| `transitionJiraIssue` | Move an issue through its workflow (get the transition id from `getTransitionsForJiraIssue` first) | `cloudId`, `issueIdOrKey`, transition id |
| `addCommentToJiraIssue` | Comment on an issue | `cloudId`, `issueIdOrKey`, comment body |
| `addWorklogToJiraIssue` | Log work on an issue | `cloudId`, `issueIdOrKey`, time spent — discover via tool schema |
| `createIssueLink` | Link two issues (type from `getIssueLinkTypes`) | `cloudId`, inward/outward issue + link type — discover via tool schema |

## Confluence — read

| Tool | Purpose | Key parameters |
|---|---|---|
| `getConfluenceSpaces` | List spaces | `cloudId` |
| `getConfluencePage` | Fetch a page (body + version) | `cloudId`, `pageId` |
| `getPagesInConfluenceSpace` | List pages in a space | `cloudId`, `spaceId` — discover via tool schema |
| `getConfluencePageDescendants` | Child/descendant pages (hierarchy inspection) | `cloudId`, `pageId` |
| `getConfluencePageFooterComments` | Footer comments on a page | `cloudId`, `pageId` |
| `getConfluencePageInlineComments` | Inline comments on a page | `cloudId`, `pageId` |
| `searchConfluenceUsingCql` | Run a CQL search | `cloudId`, `cql` |

## Confluence — write

| Tool | Purpose | Key parameters |
|---|---|---|
| `createConfluencePage` | Create a page. Body must be **Confluence storage format (XHTML) or ADF** — legacy wiki markup (`{info}`, `h2.`, `{panel}`) is rejected. | `cloudId`, space id/key, `title`, `body`; parent id optional — discover via tool schema |
| `updateConfluencePage` | Update a page (supply current version + 1) | `cloudId`, `pageId`, `version`, `body` |
| `createConfluenceFooterComment` | Add a footer comment | `cloudId`, `pageId`, body |
| `createConfluenceInlineComment` | Add an inline comment | `cloudId`, `pageId`, body + anchor — discover via tool schema |

## Cross-product

| Tool | Purpose | Key parameters |
|---|---|---|
| `search` | Rovo cross-product search across Jira + Confluence | query string |
| `fetch` | Fetch a Jira/Confluence entity by id/URL | id — discover via tool schema |

## Explicitly NOT available via MCP (use web UI or REST API)

| Capability | Where to do it instead |
|---|---|
| Create/archive Jira **projects** | Jira web UI (`Projects > Create project`) or REST `POST /rest/api/3/project` |
| Create/manage **sprints** or boards | Jira board UI or Jira Software REST (`/rest/agile/1.0/sprint`) |
| Create/share saved **filters** | Jira UI (`Filters > Save as`) or REST `POST /rest/api/3/filter` |
| **Field configuration**, custom fields, screens | Jira admin UI (`Settings > Issues`) |
| **Workflow** / permission / notification **schemes** | Jira admin UI |
| Create/delete Confluence **spaces** | Confluence UI (`Spaces > Create space`) or REST `POST /wiki/api/v2/spaces` |
| **Delete** Confluence pages | Confluence UI or REST `DELETE /wiki/api/v2/pages/{id}` |
| Page **labels** | Confluence UI or REST (`/wiki/rest/api/content/{id}/label`) |
| Confluence **page templates / blueprints** (as first-class template objects) | Confluence UI (`Space settings > Templates`); via MCP you can only create ordinary pages that serve as copy-from templates |
| **User/group provisioning**, SSO, org admin | admin.atlassian.com or the org admin REST API |
| **Automation rules** | Jira/Confluence Automation UI |

If a workflow in any skill in this domain appears to need one of these, the skill must say so and route to the UI/REST path — not invent a tool.

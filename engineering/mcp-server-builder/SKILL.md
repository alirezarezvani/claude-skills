# MCP Server Builder

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** AI / API Integration  

---

## Overview

Design and implement Model Context Protocol (MCP) servers that expose any REST API, database, or service as structured tools for Claude and other LLMs. Covers both FastMCP (Python) and the TypeScript MCP SDK, with patterns for reading OpenAPI/Swagger specs, generating tool definitions, handling auth, errors, and testing.

## Core Capabilities

- **OpenAPI → MCP tools** — parse Swagger/OpenAPI specs and generate tool definitions
- **FastMCP (Python)** — decorator-based server with automatic schema generation
- **TypeScript MCP SDK** — typed server with zod validation
- **Auth handling** — API keys, Bearer tokens, OAuth2, mTLS
- **Error handling** — structured error responses LLMs can reason about
- **Testing** — unit tests for tool handlers, integration tests with MCP inspector

---

## When to Use

- Exposing a REST API to Claude without writing a custom integration
- Building reusable tool packs for a team's Claude setup
- Wrapping internal company APIs (Jira, HubSpot, custom microservices)
- Creating database-backed tools (read/write structured data)
- Replacing brittle browser automation with typed API calls

---

## MCP Architecture

```
Claude / LLM
    │
    │  MCP Protocol (JSON-RPC over stdio or HTTP/SSE)
    ▼
MCP Server
    │  calls
    ▼
External API / Database / Service
```

Each MCP server exposes:
- **Tools** — callable functions with typed inputs/outputs
- **Resources** — readable data (files, DB rows, API responses)
- **Prompts** — reusable prompt templates

---

## Reading an OpenAPI Spec

Given a Swagger/OpenAPI file, extract tool definitions:

```python
import yaml
import json

def openapi_to_tools(spec_path: str) -> list[dict]:
    with open(spec_path) as f:
        spec = yaml.safe_load(f)
    
    tools = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            
            # Build parameter schema
            properties = {}
            required = []
            
            # Path/query parameters
            for param in op.get("parameters", []):
                name = param["name"]
                schema = param.get("schema", {"type": "string"})
                properties[name] = {
                    "type": schema.get("type", "string"),
                    "description": param.get("description", ""),
                }
                if param.get("required"):
                    required.append(name)
            
            # Request body
            if "requestBody" in op:
                content = op["requestBody"].get("content", {})
                json_schema = content.get("application/json", {}).get("schema", {})
                if "$ref" in json_schema:
                    ref_name = json_schema["$ref"].split("/")[-1]
                    json_schema = spec["components"]["schemas"][ref_name]
                for prop_name, prop_schema in json_schema.get("properties", {}).items():
                    properties[prop_name] = prop_schema
                required.extend(json_schema.get("required", []))
            
            tool_name = op.get("operationId") or f"{method}_{path.replace('/', '_').strip('_')}"
            tools.append({
                "name": tool_name,
                "description": op.get("summary", op.get("description", "")),
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                }
            })
    
    return tools
```

---

## Full Example: FastMCP Python Server for CRUD API

This builds a complete MCP server for a hypothetical Task Management REST API.

```python
# server.py
from fastmcp import FastMCP
from pydantic import BaseModel, Field
import httpx
import os
from typing import Optional

# Initialize MCP server
mcp = FastMCP(
    name="task-manager",
    description="MCP server for Task Management API",
)

# Config
API_BASE = os.environ.get("TASK_API_BASE", "https://api.tasks.example.com")
API_KEY = os.environ["TASK_API_KEY"]  # Fail fast if missing

# Shared HTTP client with auth
def get_client() -> httpx.Client:
    return httpx.Client(
        base_url=API_BASE,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        timeout=30.0,
    )


# ── Pydantic models for input validation ──────────────────────────────────────

class CreateTaskInput(BaseModel):
    title: str = Field(..., description="Task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Task description")
    assignee_id: Optional[str] = Field(None, description="User ID to assign to")
    due_date: Optional[str] = Field(None, description="Due date in ISO 8601 format (YYYY-MM-DD)")
    priority: str = Field("medium", description="Priority: low, medium, high, critical")

class UpdateTaskInput(BaseModel):
    task_id: str = Field(..., description="Task ID to update")
    title: Optional[str] = Field(None, description="New title")
    status: Optional[str] = Field(None, description="New status: todo, in_progress, done, cancelled")
    assignee_id: Optional[str] = Field(None, description="Reassign to user ID")
    due_date: Optional[str] = Field(None, description="New due date (YYYY-MM-DD)")


# ── Tool implementations ───────────────────────────────────────────────────────

@mcp.tool()
def list_tasks(
    status: Optional[str] = None,
    assignee_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    List tasks with optional filtering by status or assignee.
    Returns paginated results with total count.
    """
    params = {"limit": limit, "offset": offset}
    if status:
        params["status"] = status
    if assignee_id:
        params["assignee_id"] = assignee_id
    
    with get_client() as client:
        resp = client.get("/tasks", params=params)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
def get_task(task_id: str) -> dict:
    """
    Get a single task by ID including full details and comments.
    """
    with get_client() as client:
        resp = client.get(f"/tasks/{task_id}")
        if resp.status_code == 404:
            return {"error": f"Task {task_id} not found"}
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
def create_task(input: CreateTaskInput) -> dict:
    """
    Create a new task. Returns the created task with its ID.
    """
    with get_client() as client:
        resp = client.post("/tasks", json=input.model_dump(exclude_none=True))
        if resp.status_code == 422:
            return {"error": "Validation failed", "details": resp.json()}
        resp.raise_for_status()
        task = resp.json()
        return {
            "success": True,
            "task_id": task["id"],
            "task": task,
        }


@mcp.tool()
def update_task(input: UpdateTaskInput) -> dict:
    """
    Update an existing task's title, status, assignee, or due date.
    Only provided fields are updated (PATCH semantics).
    """
    payload = input.model_dump(exclude_none=True)
    task_id = payload.pop("task_id")
    
    if not payload:
        return {"error": "No fields to update provided"}
    
    with get_client() as client:
        resp = client.patch(f"/tasks/{task_id}", json=payload)
        if resp.status_code == 404:
            return {"error": f"Task {task_id} not found"}
        resp.raise_for_status()
        return {"success": True, "task": resp.json()}


@mcp.tool()
def delete_task(task_id: str, confirm: bool = False) -> dict:
    """
    Delete a task permanently. Set confirm=true to proceed.
    This action cannot be undone.
    """
    if not confirm:
        return {
            "error": "Deletion requires explicit confirmation",
            "hint": "Call again with confirm=true to permanently delete this task",
        }
    
    with get_client() as client:
        resp = client.delete(f"/tasks/{task_id}")
        if resp.status_code == 404:
            return {"error": f"Task {task_id} not found"}
        resp.raise_for_status()
        return {"success": True, "deleted_task_id": task_id}


@mcp.tool()
def search_tasks(query: str, limit: int = 10) -> dict:
    """
    Full-text search across task titles and descriptions.
    Returns matching tasks ranked by relevance.
    """
    with get_client() as client:
        resp = client.get("/tasks/search", params={"q": query, "limit": limit})
        resp.raise_for_status()
        results = resp.json()
        return {
            "query": query,
            "total": results.get("total", 0),
            "tasks": results.get("items", []),
        }


# ── Resource: expose task list as readable resource ───────────────────────────

@mcp.resource("tasks://recent")
def recent_tasks_resource() -> str:
    """Returns the 10 most recently updated tasks as JSON."""
    with get_client() as client:
        resp = client.get("/tasks", params={"sort": "-updated_at", "limit": 10})
        resp.raise_for_status()
        return resp.text


if __name__ == "__main__":
    mcp.run()
```

---

## TypeScript MCP SDK Version

```typescript
// server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const API_BASE = process.env.TASK_API_BASE ?? "https://api.tasks.example.com";
const API_KEY = process.env.TASK_API_KEY!;
if (!API_KEY) throw new Error("TASK_API_KEY is required");

const server = new McpServer({
  name: "task-manager",
  version: "1.0.0",
});

async function apiRequest(
  method: string,
  path: string,
  body?: unknown,
  params?: Record<string, string>
): Promise<unknown> {
  const url = new URL(`${API_BASE}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }

  const resp = await fetch(url.toString(), {
    method,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`API error ${resp.status}: ${text}`);
  }

  return resp.json();
}

// List tasks
server.tool(
  "list_tasks",
  "List tasks with optional status/assignee filter",
  {
    status: z.enum(["todo", "in_progress", "done", "cancelled"]).optional(),
    assignee_id: z.string().optional(),
    limit: z.number().int().min(1).max(100).default(20),
  },
  async ({ status, assignee_id, limit }) => {
    const params: Record<string, string> = { limit: String(limit) };
    if (status) params.status = status;
    if (assignee_id) params.assignee_id = assignee_id;

    const data = await apiRequest("GET", "/tasks", undefined, params);
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  }
);

// Create task
server.tool(
  "create_task",
  "Create a new task",
  {
    title: z.string().min(1).max(200),
    description: z.string().optional(),
    priority: z.enum(["low", "medium", "high", "critical"]).default("medium"),
    due_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  },
  async (input) => {
    const task = await apiRequest("POST", "/tasks", input);
    return {
      content: [
        {
          type: "text",
          text: `Created task: ${JSON.stringify(task, null, 2)}`,
        },
      ],
    };
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
console.error("Task Manager MCP server running");
```

---

## Auth Patterns

### API Key (header)
```python
headers={"X-API-Key": os.environ["API_KEY"]}
```

### Bearer token
```python
headers={"Authorization": f"Bearer {os.environ['ACCESS_TOKEN']}"}
```

### OAuth2 client credentials (auto-refresh)
```python
import httpx
from datetime import datetime, timedelta

_token_cache = {"token": None, "expires_at": datetime.min}

def get_access_token() -> str:
    if datetime.now() < _token_cache["expires_at"]:
        return _token_cache["token"]
    
    resp = httpx.post(
        os.environ["TOKEN_URL"],
        data={
            "grant_type": "client_credentials",
            "client_id": os.environ["CLIENT_ID"],
            "client_secret": os.environ["CLIENT_SECRET"],
            "scope": "api.read api.write",
        },
    )
    resp.raise_for_status()
    data = resp.json()
    _token_cache["token"] = data["access_token"]
    _token_cache["expires_at"] = datetime.now() + timedelta(seconds=data["expires_in"] - 30)
    return _token_cache["token"]
```

---

## Error Handling Best Practices

LLMs reason better when errors are descriptive:

```python
@mcp.tool()
def get_user(user_id: str) -> dict:
    """Get user by ID."""
    try:
        with get_client() as client:
            resp = client.get(f"/users/{user_id}")
            
            if resp.status_code == 404:
                return {
                    "error": "User not found",
                    "user_id": user_id,
                    "suggestion": "Use list_users to find valid user IDs",
                }
            
            if resp.status_code == 403:
                return {
                    "error": "Access denied",
                    "detail": "Current API key lacks permission to read this user",
                }
            
            resp.raise_for_status()
            return resp.json()
    
    except httpx.TimeoutException:
        return {"error": "Request timed out", "suggestion": "Try again in a few seconds"}
    
    except httpx.HTTPError as e:
        return {"error": f"HTTP error: {str(e)}"}
```

---

## Testing MCP Servers

### Unit tests (pytest)
```python
# tests/test_server.py
import pytest
from unittest.mock import patch, MagicMock
from server import create_task, list_tasks

@pytest.fixture(autouse=True)
def mock_api_key(monkeypatch):
    monkeypatch.setenv("TASK_API_KEY", "test-key")

def test_create_task_success():
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": "task-123", "title": "Test task"}
    
    with patch("httpx.Client.post", return_value=mock_resp):
        from server import CreateTaskInput
        result = create_task(CreateTaskInput(title="Test task"))
    
    assert result["success"] is True
    assert result["task_id"] == "task-123"

def test_create_task_validation_error():
    mock_resp = MagicMock()
    mock_resp.status_code = 422
    mock_resp.json.return_value = {"detail": "title too long"}
    
    with patch("httpx.Client.post", return_value=mock_resp):
        from server import CreateTaskInput
        result = create_task(CreateTaskInput(title="x" * 201))  # Over limit
    
    assert "error" in result
```

### Integration test with MCP Inspector
```bash
# Install MCP inspector
npx @modelcontextprotocol/inspector python server.py

# Or for TypeScript
npx @modelcontextprotocol/inspector node dist/server.js
```

---

## Packaging and Distribution

### pyproject.toml for FastMCP server
```toml
[project]
name = "my-mcp-server"
version = "1.0.0"
dependencies = [
    "fastmcp>=0.4",
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.scripts]
my-mcp-server = "server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Claude Desktop config (~/.claude/config.json)
```json
{
  "mcpServers": {
    "task-manager": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "TASK_API_KEY": "your-key-here",
        "TASK_API_BASE": "https://api.tasks.example.com"
      }
    }
  }
}
```

---

## Common Pitfalls

- **Returning raw API errors** — LLMs can't act on HTTP 422; translate to human-readable messages
- **No confirmation on destructive actions** — add `confirm: bool = False` pattern for deletes
- **Blocking I/O without timeout** — always set `timeout=30.0` on HTTP clients
- **Leaking API keys in tool responses** — never echo env vars back in responses
- **Tool names with hyphens** — use underscores; some LLM routers break on hyphens
- **Giant response payloads** — truncate/paginate; LLMs have context limits

---

## Best Practices

1. **One tool, one action** — don't build "swiss army knife" tools; compose small tools
2. **Descriptive tool descriptions** — LLMs use them for routing; be explicit about what it does
3. **Return structured data** — JSON dicts, not formatted strings, so LLMs can reason about fields
4. **Validate inputs with Pydantic/zod** — catch bad inputs before hitting the API
5. **Idempotency hints** — note in description if a tool is safe to retry
6. **Resource vs Tool** — use resources for read-only data LLMs reference; tools for actions

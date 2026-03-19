---
name: liepin-jobs
description: |
  猎聘求职工具 — Search jobs on Liepin, apply to positions, view and edit resumes.
  Zero-dependency Python CLI wrapping Liepin's official MCP Server.
  触发词: 找工作, 搜职位, 投简历, 猎聘, liepin, 求职, 招聘, 简历
version: 0.1.0
author: xllinbupt
license: MIT
homepage: https://github.com/xllinbupt/MCP2skill
repository: https://github.com/xllinbupt/MCP2skill
keywords:
  - jobs
  - liepin
  - resume
  - mcp
  - chinese
  - career
  - recruitment
requires:
  bins: python3
allowed-tools: Bash(python3:*),Bash(python:*)
---

# 猎聘求职工具 (liepin-jobs)

Search jobs, apply to positions, and manage resumes on Liepin (猎聘) — China's leading professional recruitment platform.

Built on Liepin's official MCP Server with zero external dependencies (uses only Python's built-in `urllib`).

## Setup

Get tokens from https://www.liepin.com/mcp/server then:

```bash
python3 "<skill_dir>/liepin_mcp.py" setup
```

Or via environment variables:

```bash
export LIEPIN_GATEWAY_TOKEN="mcp_gateway_token_xxxx"
export LIEPIN_USER_TOKEN="liepin_user_token_xxxx"
```

## Commands

```bash
SCRIPT="<skill_dir>/liepin_mcp.py"

# Search jobs
python3 "$SCRIPT" search-job --jobName "AI产品经理" --address "上海"
python3 "$SCRIPT" search-job --jobName "前端开发" --salary "30-50k"

# Apply to a job
python3 "$SCRIPT" apply-job --jobId "JOB_ID" --jobKind "JOB_KIND"

# View resume
python3 "$SCRIPT" my-resume

# Update resume
python3 "$SCRIPT" update-resume --module basic --data '{"name": "张三"}'
python3 "$SCRIPT" update-resume --module experience --data '{"company": "xxx"}'

# List all available tools
python3 "$SCRIPT" list-tools
```

## Workflow

1. **Check tokens** → run `setup` if not configured
2. **View resume** (`my-resume`) → ensure completeness
3. **Search jobs** (`search-job`) → display results in table
4. **Analyze match** → compare resume with job requirements
5. **Apply** (`apply-job`) → **must confirm with user before applying**

## Notes

- Applications are irreversible — always confirm before applying
- Rate limit: 60 calls/minute shared across all operations
- Token validity: 90 days

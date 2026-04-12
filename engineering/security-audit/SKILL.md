---
name: "security-audit"
description: "Use when the user asks to audit security, scan for secrets, check for CVEs, detect identity tampering, or harden infrastructure. Five modules covering agent identity, infrastructure, secrets, dependencies, and multi-project dispatch."
---

# Bubble Sentinel — Security Audit

**Tier:** POWERFUL
**Category:** Engineering
**Tags:** security, audit, secret-scanning, CVE, tamper-detection, infrastructure

## Overview

Automated security audit suite for Claude Code agent deployments. Five independent modules: identity tamper detection (SHA-256 snapshots), infrastructure hardening (SSH, firewall, OS updates), secret scanning (17 regex patterns), dependency CVE checking (npm, pip, cargo), and multi-project dispatch.

## Key Features

- **Identity Audit:** Tracks SHA-256 snapshots of agent identity/config files. CRITICAL alert on any modification.
- **Infrastructure Audit:** SSH config, firewall status, OS updates, file permissions, environment secrets. macOS + Linux.
- **Secret Scanner:** AWS keys, Anthropic/OpenAI tokens, Stripe keys, GitHub PATs, private keys, database URLs, custom patterns.
- **Dependency Checker:** npm audit (v6+v7), Python via OSV API, Rust via cargo-audit.
- **Project Dispatcher:** Cycle through registered projects with auto-detection (code vs documents).

## Setup

```bash
/plugin marketplace add vdk888/bubble-sentinel
/plugin install bubble-sentinel@bubble-sentinel
```

## Requirements

- Python 3.7+ (stdlib only — zero external dependencies)
- macOS or Linux
- npm in PATH for Node.js dependency auditing (optional)

## Links

- **GitHub:** https://github.com/vdk888/bubble-sentinel (private — access via subscription)
- **Product page:** https://bubble-sentinel.netlify.app/sentinel.html
- **License:** MIT
- **Author:** [Bubble Invest](https://bubbleinvest.org)

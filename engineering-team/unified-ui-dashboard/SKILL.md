---
name: unified-ui-dashboard
description: "Launch HaMm3r's Unified Tool Hub — a single interactive HTML dashboard showing all 11 connected MCP tool categories with Google Antigravity physics. Use when: 'show me my tools', 'unified dashboard', 'tool hub', 'open dashboard', 'what tools do I have', 'antigravity UI', 'list all my MCP tools', '/unified-ui'. Writes a self-contained dashboard.html to disk that the user opens in their browser."
license: MIT
metadata:
  version: 1.0.0
  author: lordhammer11
  category: engineering
  updated: 2026-05-18
---

# HaMm3r's Unified Tool Hub

A self-contained browser dashboard that surfaces all 11 connected MCP tool categories in one place. Includes a Google Antigravity physics engine — press a button and every tool card floats, bounces, and reacts to your cursor.

**This skill is for visual browsing of connected tools.** It is NOT for executing tools (use the tools directly), NOT for configuration (use settings), and NOT for workflow automation (use the relevant domain skill).

---

## Table of Contents

- [What This Skill Does](#what-this-skill-does)
- [Quick Start](#quick-start)
- [Delivery Modes](#delivery-modes)
- [Antigravity Physics Engine](#antigravity-physics-engine)
- [Tool Categories Reference](#tool-categories-reference)
- [Search and Navigation](#search-and-navigation)
- [Proactive Triggers](#proactive-triggers)
- [Anti-Patterns](#anti-patterns)
- [Related Skills](#related-skills)

---

## What This Skill Does

Delivers `assets/dashboard.html` — a fully self-contained, dark-mode HTML file with no external dependencies. When opened in a browser it shows:

- **11 tool category cards** with icons, subtitles, and status indicators
- **Capability pills** on each card showing the top actions available
- **Click-to-expand modal** listing every capability for that tool with descriptions
- **Real-time search** filtering across tool names, subtitles, and all capability descriptions
- **Google Antigravity mode** — physics engine that launches cards into floating, bouncing, mouse-repelled orbits
- **Keyboard shortcuts**: `Ctrl+G` (toggle gravity), `/` (focus search), `Esc` (close modal / exit gravity)

---

## Quick Start

When the user invokes `/unified-ui` or asks to see their tools:

1. Write `assets/dashboard.html` to `./dashboard.html` in the working directory
2. Tell the user: _"Open `dashboard.html` in your browser. Use `/` to search tools, click any card for details, and press `Ctrl+G` for Antigravity mode."_
3. Offer a one-line summary of the 11 tool categories available

---

## Delivery Modes

### Mode 1: Write to disk (Claude Code with file access)

```bash
# Claude Code writes the HTML asset to the current working directory
cp assets/dashboard.html ./dashboard.html
# Or via the Write tool — copy contents of assets/dashboard.html → ./dashboard.html
```

Tell user:
> Open `dashboard.html` in your browser to access HaMm3r's Unified Tool Hub.

### Mode 2: Display inline (chat / web context)

Output the full contents of `assets/dashboard.html` as a fenced HTML code block so the user can copy-paste it into a local file and open it directly:

````
```html
<!-- full dashboard.html contents here -->
```
````

### Mode 3: Summary only (quick reference)

If the user only wants to know what tools are available without opening a dashboard, provide the tool table from the [Tool Categories Reference](#tool-categories-reference) section directly in chat.

---

## Antigravity Physics Engine

The dashboard ships a JavaScript physics engine inspired by Google's gravity Easter egg.

| Control | Action |
|---------|--------|
| `⬆ Antigravity` button | Toggle physics mode on/off |
| `Ctrl+G` | Keyboard shortcut to toggle |
| Mouse cursor | Creates repulsion force within 220px radius |
| Click + drag | Grab a card and throw it |
| `Esc` | Exit gravity mode, restore grid layout |

**Physics parameters:**
- Upward gravity: `G = 0.07` (cards drift upward)
- Velocity damping: `DAMP = 0.996` (cards slow down gradually)
- Boundary bounce: `BNC = 0.45` (cards rebound off viewport edges)
- Mouse repulsion radius: `220px`
- Particle system: 80 glowing seed particles stream upward during gravity mode

Cards return to their original grid positions when Antigravity is turned off.

---

## Tool Categories Reference

| Tool | Key Capabilities |
|------|------------------|
| **Gmail** | search_threads, create_draft, label_message, get_thread, unlabel_thread |
| **Google Drive** | list_recent_files, search_files, create_file, download_file_content, get_file_metadata |
| **Google Calendar** | list_events, create_event, suggest_time, respond_to_event, update_event |
| **Zoom** | recordings_list, search_meetings, get_meeting_assets, get_file_content, search_zoom |
| **GitHub** | list_pull_requests, list_issues, search_code, push_files, create_branch, create_pull_request |
| **Shopify** | get_product, list_orders, run_analytics_query, create_product, search_products |
| **Adobe Creative Cloud** | image_remove_background, image_crop_and_resize, image_fill_area, image_vectorize, image_generate |
| **Canva** | generate_design, search_designs, export_design, list_brand_kits, get_design |
| **DocuSign** | getEnvelopes, createEnvelope, getTemplates, triggerWorkflow, listRecipients |
| **Hugging Face** | hub_repo_search, paper_search, space_search, hf_doc_search, hf_whoami |
| **Ideabrowser** | browse_ideas, list_trends, get_market_insight_detail, list_projects, get_founder_profile |

Total: 11 tool categories, 80+ capabilities surfaced.

---

## Search and Navigation

The search bar at the top of the dashboard filters all 11 cards in real time. It searches across:

- Tool category name (e.g., "GitHub")
- Tool subtitle (e.g., "Code & Collaboration")
- Action names (e.g., "create_branch")
- Capability descriptions (e.g., "push files to a repository")

**Usage:** Click the search bar or press `/` anywhere on the page to focus it. The matching cards stay visible; non-matching cards fade. Press `Esc` to clear the filter.

---

## Proactive Triggers

Surface the dashboard without being asked in these situations:

| Trigger | Response |
|---------|----------|
| User asks "what can you do?" or "what tools do you have?" | Offer to open the dashboard for a visual overview of all 11 categories |
| User is switching between many different tools in one session | Suggest opening the dashboard to browse what's available before deciding |
| First session after onboarding | Mention `/unified-ui` as a way to see all connected tools at a glance |
| User asks about a specific tool's capabilities | Answer, then note they can see all tools together in the dashboard |
| User seems confused about which tool to use | Proactively open the dashboard and guide them to the right category |

---

## Anti-Patterns

**Do NOT use this skill to:**

1. **Execute tool calls** — The dashboard is read-only. To actually send a Gmail draft, use the Gmail MCP tools directly.
2. **Configure MCP connections** — The dashboard shows what's already connected. Setup belongs in your MCP configuration.
3. **Replace domain-specific skills** — For deep GitHub automation, use the GitHub skill. This skill is only for browsing.
4. **Serve as the only tool reference** — Capabilities in the dashboard are summarized. For full parameter details, consult the specific MCP tool's documentation.
5. **Auto-open on every session** — Only open the dashboard when the user asks or clearly needs an overview. Don't add it as a default startup action.

---

## Related Skills

| Skill | Use When |
|-------|----------|
| `google-workspace` | Deep Google Workspace CLI automation (Drive, Gmail, Calendar scripting) — NOT visual browsing |
| `session-start-hook` | Auto-setup actions on session start — NOT for interactive dashboards |
| `mcp-server-builder` | Building new MCP servers to add more tools — NOT for viewing existing ones |

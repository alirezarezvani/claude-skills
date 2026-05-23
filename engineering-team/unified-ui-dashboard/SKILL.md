---
name: unified-ui-dashboard
description: "Launch the Unified Tool Dashboard — a single interactive UI showing all connected MCP tools with Google Antigravity physics. Use when: 'show me my tools', 'unified dashboard', 'tool hub', 'open dashboard', 'what tools do I have', 'antigravity UI', 'list all my tools'. Generates a self-contained HTML file the user opens in their browser. Trigger with /unified-ui."
license: MIT
metadata:
  version: 1.0.0
  author: lordhammer11
  category: engineering
  updated: 2026-05-18
---

# Unified Tool Dashboard

You are a UI delivery expert. When this skill is invoked, generate and deliver the interactive Unified Tool Dashboard to the user.

## What This Skill Does

Delivers a self-contained `dashboard.html` file that renders a beautiful dark-mode tool hub showing all connected MCP integrations, with a Google Antigravity physics mode built in.

---

## Before Starting

If the user invokes `/unified-ui`, immediately:
1. Write `dashboard.html` to the current working directory using the contents of `assets/dashboard.html`
2. Tell the user to open it in their browser
3. Summarize the 11 tool categories available

---

## Tool Categories Covered

| Tool | Key Capabilities |
|------|------------------|
| Gmail | search_threads, create_draft, label_message, get_thread |
| Google Drive | list_recent_files, search_files, create_file, download_file_content |
| Google Calendar | list_events, create_event, suggest_time, respond_to_event |
| Zoom | recordings_list, search_meetings, get_meeting_assets, get_file_content |
| GitHub | list_pull_requests, list_issues, search_code, push_files, create_branch |
| Shopify | get_product, list_orders, run_analytics_query, create_product |
| Adobe Creative | image_remove_background, image_crop_and_resize, image_fill_area, image_vectorize |
| Canva | generate_design, search_designs, export_design, list_brand_kits |
| DocuSign | getEnvelopes, createEnvelope, getTemplates, triggerWorkflow |
| Hugging Face | hub_repo_search, paper_search, space_search, hf_doc_search |
| Ideabrowser | browse_ideas, list_trends, get_market_insight_detail, list_projects |

---

## How to Deliver

### Mode 1: Write to disk (Claude Code context)
When running in Claude Code with file write access:
```
Write the contents of assets/dashboard.html to ./dashboard.html
Tell user: "Open dashboard.html in your browser to access the Unified Tool Hub."
```

### Mode 2: Display inline (chat context)
Output the full HTML as a fenced code block so the user can copy-paste it into a local file.

---

## Antigravity Mode

The dashboard includes a **Google Antigravity physics engine** built in JavaScript:
- Press **`⬆️ Antigravity`** button (or `Ctrl+G`) to launch cards into floating upward physics
- Cards drift upward with realistic velocity, damping, and boundary wrapping
- Mouse proximity creates a **repulsion force** — move your cursor to push cards around
- Drag any card to throw it across the screen
- Colorful particles stream upward during antigravity mode
- Press **`Esc`** or the button again to restore normal layout

---

## Proactive Triggers

Surface these without being asked:

- **User asks "what can you do?"** → Offer to open the dashboard for a visual overview
- **User is lost between tools** → Suggest opening the dashboard to browse capabilities
- **First session start** → Mention the `/unified-ui` command as a way to see all tools
- **User asks about a specific tool** → After answering, note they can see all tools in the dashboard

---

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| `/unified-ui` | `dashboard.html` written to disk + open instructions |
| "show my tools" | Summary table of all 11 categories + offer to open dashboard |
| "antigravity demo" | Description of the physics mode + `dashboard.html` delivery |

---

## Related Skills

- **google-workspace**: For deep Google Workspace CLI automation. NOT for browsing tools visually.
- **session-start-hook**: For auto-setup on session start. NOT for interactive dashboards.

---
name: unified-ui
description: "Open the Unified Tool Dashboard showing all connected tools with Google Antigravity UI physics. Use for: 'show my tools', 'unified dashboard', 'open tool hub', 'what tools do I have', 'antigravity mode'. Generates and opens a self-contained interactive HTML dashboard."
---

# /unified-ui

Generates and delivers the **Unified Tool Hub** — a single interactive dashboard showing all your connected MCP integrations, with a built-in Google Antigravity physics mode.

## What You Get

A self-contained `dashboard.html` file you open in any browser:

- **11 tool categories** — all your connected MCP tools on one screen
- **Search bar** — filter tools and capabilities in real-time (press `/` to focus)
- **Detail modals** — click any card to see all capabilities for that tool
- **Google Antigravity mode** — press `⬆ Antigravity` or `Ctrl+G` to launch cards into floating upward physics with particle effects

## Tools Shown

| | Tool | Key Capabilities |
|--|------|------------------|
| 📧 | Gmail | search_threads, create_draft, label_message |
| 📁 | Google Drive | list_recent_files, search_files, create_file |
| 📅 | Google Calendar | list_events, create_event, suggest_time |
| 🎥 | Zoom | recordings_list, search_meetings, get_file_content |
| 🐙 | GitHub | list_pull_requests, search_code, push_files |
| 🛍️ | Shopify | get_product, list_orders, run_analytics_query |
| 🎨 | Adobe Creative | image_remove_background, image_fill_area, image_vectorize |
| ✏️ | Canva | generate_design, export_design, list_brand_kits |
| ✍️ | DocuSign | getEnvelopes, createEnvelope, triggerWorkflow |
| 🤗 | Hugging Face | hub_repo_search, paper_search, space_search |
| 💡 | Ideabrowser | browse_ideas, list_trends, start_idea_research |

## Antigravity Physics

When activated:
- Cards float **upward** with realistic velocity and damping
- Moving your cursor **repels** nearby cards
- **Drag** any card to throw it across the screen
- Cards **wrap** vertically when they exit the top — reappear at the bottom
- Colorful **particles stream upward** during flight
- `Esc` or clicking the button again restores the normal layout

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+G` | Toggle antigravity mode |
| `/` | Focus search bar |
| `Esc` | Exit modal / exit antigravity |

## Skill Reference
→ `engineering-team/unified-ui-dashboard/SKILL.md`
→ `engineering-team/unified-ui-dashboard/assets/dashboard.html`

## How Claude Delivers This

When you run `/unified-ui`, Claude:
1. Writes `dashboard.html` to your current working directory
2. Tells you to open it in your browser
3. Summarizes the tools available

## Related Commands

- `/google-workspace` — Deep Google Workspace CLI operations (not for visual browsing)

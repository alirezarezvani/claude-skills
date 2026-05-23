# Jarvis Brain 🧠
> Persistent knowledge index for lordhammer11 — everything built, developed, and imagined.
> Auto-updated by GitHub Actions. Query interactively with `/brain` in Claude Code.

---

## Active Work

| Project | Repo | Status | Tags |
|---------|------|--------|------|
| [Gemma 3 Metal Formula + Chat UI](#gemma3-metal-macos) | homebrew-tap | Draft PR #1 | gemma3, metal, macos, ollama, ui |
| [Apex Agent Formula](#apex-agent) | homebrew-tap | Active | agent, homebrew |
| [Claude Skills Library (205+)](#claude-skills-library) | claude-skills | Active | skills, ai, engineering, marketing |
| [Jarvis Brain](#jarvis-brain) | claude-skills | Active | brain, meta, knowledge |

---

## Detail Entries

### gemma3-metal-macos
**Gemma 3 Homebrew Formula — Metal GPU + Chat UI**
- **Repo:** lordhammer11/homebrew-tap · branch `claude/gemma-metal-macos-elEwl` · PR #1 (draft)
- **Created:** 2026-05-18
- **Tags:** `gemma3` `metal` `macos` `ollama` `ai` `llm` `homebrew` `ui` `gpu`
- **Summary:** Homebrew formula that installs Google Gemma 3 locally on macOS with Metal GPU acceleration via Ollama. Embeds a Python interactive chat UI with model-size picker (1B/4B/12B/27B), coloured output, slash commands (`/help` `/model` `/clear` `/save` `/quit`), readline history, and conversation save-to-file.
- **Files:** `Formula/gemma3.rb`
- **Install:** `brew install --HEAD lordhammer11/tap/gemma3`
- **Notes:** Metal is auto-enabled on Apple Silicon via Ollama. Intel Macs fall back to CPU.

---

### apex-agent
**Apex Agent Homebrew Formula**
- **Repo:** lordhammer11/homebrew-tap · branch `main`
- **Created:** 2026-05-18
- **Tags:** `agent` `homebrew`
- **Summary:** Existing Homebrew formula for Apex Agent in the tap.
- **Files:** `Formula/apex-agent.rb`

---

### claude-skills-library
**Claude Skills Library (205+ skills)**
- **Repo:** lordhammer11/claude-skills · branch `main`
- **Created:** 2026-05-18
- **Tags:** `skills` `claude` `agents` `engineering` `marketing` `finance` `product` `c-level`
- **Summary:** 205+ production-ready skills across 9 domains. Supports Claude Code, Cursor, VS Code/Copilot, Goose, Gemini CLI, Codex, OpenClaw.
- **Domains:** engineering-team · marketing-skill · c-level-advisor · product-team · project-management · ra-qm-team · business-growth · finance · engineering (advanced)
- **Install:** See `INSTALLATION.md`

---

### jarvis-brain
**Jarvis Brain — persistent knowledge index**
- **Repo:** lordhammer11/claude-skills · branch `claude/gemma-metal-macos-elEwl`
- **Created:** 2026-05-18
- **Tags:** `brain` `jarvis` `meta` `knowledge` `index` `automation`
- **Summary:** This system. Tracks all work, ideas, and creations across every repo.
- **Files:** `brain/index.json` · `brain/entries/` · `BRAIN.md` · `.claude/commands/brain.md` · `scripts/brain_update.py` · `.github/workflows/brain-sync.yml`

---

## Ideas (Backlog)

| Idea | Tags | Description |
|------|------|-------------|
| Native macOS SwiftUI app for Gemma 3 | macos, swift, ui, gemma3 | A polished SwiftUI wrapper around the gemma3 CLI — app-store quality |
| Web dashboard for the Jarvis brain | web, brain, dashboard | GitHub Pages site rendering brain/index.json as a visual knowledge map — timeline, tag cloud, repo graph |

---

## Stats

| Metric | Count |
|--------|-------|
| Total entries | 4 |
| Active | 3 |
| Draft PR | 1 |
| Ideas backlog | 2 |
| Repos tracked | 4 |

---

*Last updated: 2026-05-18 · Auto-synced by `.github/workflows/brain-sync.yml`*

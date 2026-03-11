---
title: "Board Meeting Protocol"
description: "Board Meeting Protocol - Claude Code skill from the C-Level Advisory domain."
---

# Board Meeting Protocol

<div class="page-meta" markdown>
<span class="meta-badge">:material-account-tie: C-Level Advisory</span>
<span class="meta-badge">:material-identifier: `board-meeting`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/c-level-advisor/board-meeting/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install c-level-skills</code>
</div>


Structured multi-agent deliberation that prevents groupthink, captures minority views, and produces clean, actionable decisions.

## Keywords
board meeting, executive deliberation, strategic decision, C-suite, multi-agent, /cs:board, founder review, decision extraction, independent perspectives

## Invoke
`/cs:board [topic]` — e.g. `/cs:board Should we expand to Spain in Q3?`

---

## The 6-Phase Protocol

### PHASE 1: Context Gathering
1. Load `memory/company-context.md`
2. Load `memory/board-meetings/decisions.md` **(Layer 2 ONLY — never raw transcripts)**
3. Reset session state — no bleed from previous conversations
4. Present agenda + activated roles → wait for founder confirmation

**Chief of Staff selects relevant roles** based on topic (not all 9 every time):
| Topic | Activate |
|-------|----------|
| Market expansion | CEO, CMO, CFO, CRO, COO |
| Product direction | CEO, CPO, CTO, CMO |
| Hiring/org | CEO, CHRO, CFO, COO |
| Pricing | CMO, CFO, CRO, CPO |
| Technology | CTO, CPO, CFO, CISO |

---

### PHASE 2: Independent Contributions (ISOLATED)

**No cross-pollination. Each agent runs before seeing others' outputs.**

Order: Research (if needed) → CMO → CFO → CEO → CTO → COO → CHRO → CRO → CISO → CPO

**Reasoning techniques:** CEO: Tree of Thought (3 futures) | CFO: Chain of Thought (show the math) | CMO: Recursion of Thought (draft→critique→refine) | CPO: First Principles | CRO: Chain of Thought (pipeline math) | COO: Step by Step (process map) | CTO: ReAct (research→analyze→act) | CISO: Risk-Based (P×I) | CHRO: Empathy + Data

**Contribution format (max 5 key points, self-verified):**
```
## [ROLE] — [DATE]

Key points (max 5):
• [Finding] — [VERIFIED/ASSUMED] — 🟢/🟡/🔴
• [Finding] — [VERIFIED/ASSUMED] — 🟢/🟡/🔴

Recommendation: [clear position]
Confidence: High / Medium / Low
Source: [where the data came from]
What would change my mind: [specific condition]
```

Each agent self-verifies before contributing: source attribution, assumption audit, confidence scoring. No untagged claims.

---

### PHASE 3: Critic Analysis
Executive Mentor receives ALL Phase 2 outputs simultaneously. Role: adversarial reviewer, not synthesizer.

Checklist:
- Where did agents agree too easily? (suspicious consensus = red flag)
- What assumptions are shared but unvalidated?
- Who is missing from the room? (customer voice? front-line ops?)
- What risk has nobody mentioned?
- Which agent operated outside their domain?

---

### PHASE 4: Synthesis
Chief of Staff delivers using the **Board Meeting Output** format (defined in `agent-protocol/SKILL.md`):
- Decision Required (one sentence)
- Perspectives (one line per contributing role)
- Where They Agree / Where They Disagree
- Critic's View (the uncomfortable truth)
- Recommended Decision + Action Items (owners, deadlines)
- Your Call (options if founder disagrees)

---

### PHASE 5: Human in the Loop ⏸️

**Full stop. Wait for the founder.**

```
⏸️ FOUNDER REVIEW — [Paste synthesis]

Options: ✅ Approve | ✏️ Modify | ❌ Reject | ❓ Ask follow-up
```

**Rules:**
- User corrections OVERRIDE agent proposals. No pushback. No "but the CFO said..."
- 30-min inactivity → auto-close as "pending review"
- Reopen any time with `/cs:board resume`

---

### PHASE 6: Decision Extraction
After founder approval:
- **Layer 1:** Write full transcript → `memory/board-meetings/YYYY-MM-DD-raw.md`
- **Layer 2:** Append approved decisions → `memory/board-meetings/decisions.md`
- Mark rejected proposals `[DO_NOT_RESURFACE]`
- Confirm to founder with count of decisions logged, actions tracked, flags added

---

## Memory Structure
```
memory/board-meetings/
├── decisions.md          # Layer 2 — founder-approved only (Phase 1 loads this)
├── YYYY-MM-DD-raw.md     # Layer 1 — full transcripts (never auto-loaded)
└── archive/YYYY/         # Raw transcripts after 90 days
```

**Future meetings load Layer 2 only.** Never Layer 1. This prevents hallucinated consensus.

---

## Failure Mode Quick Reference
| Failure | Fix |
|---------|-----|
| Groupthink (all agree) | Re-run Phase 2 isolated; force "strongest argument against" |
| Analysis paralysis | Cap at 5 points; force recommendation even with Low confidence |
| Bikeshedding | Log as async action item; return to main agenda |
| Role bleed (CFO making product calls) | Critic flags; exclude from synthesis |
| Layer contamination | Phase 1 loads decisions.md only — hard rule |

---

## References
- `templates/meeting-agenda.md` — agenda format
- `templates/meeting-minutes.md` — final output format
- `references/meeting-facilitation.md` — conflict handling, timing, failure modes

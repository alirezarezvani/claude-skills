---
name: ai-seo
description: "Optimize content to get cited by AI search engines — ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, Copilot. Use when you want your content to appear in AI-generated answers, not just ranked in blue links. Triggers: 'optimize for AI search', 'get cited by ChatGPT', 'AI Overviews', 'Perplexity citations', 'AI SEO', 'generative search', 'LLM visibility', 'GEO' (generative engine optimization). NOT for traditional SEO ranking (use seo-audit). NOT for content creation (use content-production)."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# AI SEO

You are an expert in generative engine optimization (GEO) — the discipline of making content citeable by AI search platforms. Your goal is to help content get extracted, quoted, and cited by ChatGPT, Perplexity, Google AI Overviews, Claude, Gemini, and Microsoft Copilot.

This is not traditional SEO. Traditional SEO gets you ranked. AI SEO gets you cited. Those are different games with different rules.

## Before Starting

**Check for context first:**
If `marketing-context.md` exists, read it. It contains existing keyword targets, content inventory, and competitor information — all of which inform where to start.

Gather what you need:

### What you need
- **URL or content to audit** — specific page, or a topic area to assess
- **Target queries** — what questions do you want AI systems to answer using your content?
- **Current visibility** — are you already appearing in any AI search results for your targets?
- **Content inventory** — do you have existing pieces to optimize, or are you starting from scratch?

If the user doesn't know their target queries: "What questions would your ideal customer ask an AI assistant that you'd want your brand to answer?"

## How This Skill Works

Three modes. Each builds on the previous, but you can start anywhere:

### Mode 1: AI Visibility Audit
Map your current presence (or absence) across AI search platforms. Understand what's getting cited, what's getting ignored, and why.

### Mode 2: Content Optimization
Restructure and enhance content to match what AI systems extract. This is the execution mode — specific patterns, specific changes.

### Mode 3: Monitoring
Set up systems to track AI citations over time — so you know when you appear, when you disappear, and when a competitor takes your spot.

---

## How AI Search Works (and Why It's Different)

Traditional SEO: Google ranks your page. User clicks through. You get traffic.

AI search: The AI reads your page (or has already indexed it), extracts the answer, and presents it to the user — often without a click. You get cited, not ranked.

**The fundamental shift:**
- Ranked = user sees your link and decides whether to click
- Cited = AI decides your content answers the question; user may never visit your site

This changes everything:
- **Keyword density** matters less than **answer clarity**
- **Page authority** matters less than **answer extractability**
- **Click-through rate** is irrelevant — the AI has already decided you're the answer
- **Structured content** (definitions, lists, tables, steps) outperforms flowing narrative

But here's what traditional SEO and AI SEO share: **authority still matters**. AI systems prefer sources they consider credible — established domains, cited works, expert authorship. You still need backlinks and domain trust. You just also need structure.

See [references/ai-search-landscape.md](references/ai-search-landscape.md) for how each platform (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot) selects and cites sources.

---

## The 3 Pillars of AI Citability

Every AI SEO decision flows from these three:

### Pillar 1: Structure (Extractable)

AI systems pull content in chunks. They don't read your whole article and then paraphrase it — they find the paragraph, list, or definition that directly answers the query and lift it.

Your content needs to be structured so that answers are self-contained and extractable:
- Definition block for "what is X"
- Numbered steps for "how to do X"
- Comparison table for "X vs Y"
- FAQ block for "questions about X"
- Statistics with attribution for "data on X"

Content that buries the answer in page 3 of a 4,000-word essay is not extractable. The AI won't find it.

### Pillar 2: Authority (Citable)

AI systems don't just pull the most relevant answer — they pull the most credible one. Authority signals in the AI era:

- **Domain authority**: High-DA domains get preferential treatment (traditional SEO signal still applies)
- **Author attribution**: Named authors with credentials beat anonymous pages
- **Citation chain**: Your content cites credible sources → you're seen as credible in turn
- **Recency**: AI systems prefer current information for time-sensitive queries
- **Original data**: Pages with proprietary research, surveys, or studies get cited more — AI systems value unique data they can't get elsewhere

### Pillar 3: Presence (Discoverable)

AI systems need to be able to find and index your content. This is the technical layer:

- **Bot access**: AI crawlers must be allowed in robots.txt (GPTBot, PerplexityBot, ClaudeBot, etc.)
- **Crawlability**: Fast page load, clean HTML, no JavaScript-only content
- **Schema markup**: Structured data (Article, FAQPage, HowTo, Product) helps AI systems understand your content type
- **Canonical signals**: Duplicate content confuses AI systems even more than traditional search
- **HTTPS and security**: AI crawlers won't index pages with security warnings

---

## Mode 1: AI Visibility Audit

### Step 1 — Bot Access Check

First: confirm AI crawlers can access your site.

**Check robots.txt** at `yourdomain.com/robots.txt`. Verify these bots are NOT blocked:

```
# Should NOT be blocked (allow AI indexing):
GPTBot         # OpenAI / ChatGPT
PerplexityBot  # Perplexity
ClaudeBot      # Anthropic / Claude
Google-Extended # Google AI Overviews
anthropic-ai   # Anthropic (alternate identifier)
Applebot-Extended # Apple Intelligence
cohere-ai      # Cohere
```

If any AI bot is blocked, flag it. That's an immediate visibility killer for that platform.

**robots.txt to allow all AI bots:**
```
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /
```

To block specific AI training while allowing search: use `Disallow:` selectively, but understand that blocking training ≠ blocking citation — they're often the same crawl.

### Step 2 — Current Citation Audit

Manually test your target queries on each platform:

| Platform | How to test |
|---|---|
| Perplexity | Search your target query at perplexity.ai — check Sources panel |
| ChatGPT | Search with web browsing enabled — check citations |
| Google AI Overviews | Google your query — check if AI Overview appears, who's cited |
| Microsoft Copilot | Search at copilot.microsoft.com — check source cards |

For each query, document:
- Are you cited? (yes/no)
- Which competitors are cited?
- What content type gets cited? (definition? list? stats?)
- How is the answer structured?

This tells you the pattern that's currently winning. Build toward it.

### Step 3 — Content Structure Audit

Review your key pages against the Extractability Checklist:

- [ ] Does the page have a clear, answerable definition of its core concept in the first 200 words?
- [ ] Are there numbered lists or step-by-step sections for process-oriented queries?
- [ ] Does the page have a FAQ section with direct Q&A pairs?
- [ ] Are statistics and data points cited with source name and year?
- [ ] Are comparisons done in table format (not narrative)?
- [ ] Is the page's H1 phrased as the answer to a question, or as a statement?
- [ ] Does schema markup exist? (FAQPage, HowTo, Article, etc.)

Score: 0-3 checks = needs major restructuring. 4-5 = good baseline. 6-7 = strong.

---

## Mode 2: Content Optimization

### The Content Patterns That Get Cited

These are the block types AI systems reliably extract. Add at least 2-3 per key page.

See [references/content-patterns.md](references/content-patterns.md) for ready-to-use templates for each pattern.

**Pattern 1: Definition Block**
The AI's answer to "what is X" almost always comes from a tight, self-contained definition. Format:

> **[Term]** is [concise definition in 1-2 sentences]. [One sentence of context or why it matters].

Placed within the first 300 words of the page. No hedging, no preamble. Just the definition.

**Pattern 2: Numbered Steps (How-To)**
For process queries ("how do I X"), AI systems pull numbered steps almost universally. Requirements:
- Steps are numbered
- Each step is actionable (verb-first)
- Each step is self-contained (could be quoted alone and still make sense)
- 5-10 steps maximum (AI truncates longer lists)

**Pattern 3: Comparison Table**
"X vs Y" queries almost always result in table citations. Two-column tables comparing features, costs, pros/cons — these get extracted verbatim. Format matters: clean markdown table with headers wins.

**Pattern 4: FAQ Block**
Explicit Q&A pairs signal to AI: "this is the question, this is the answer." Mark up with FAQPage schema. Questions should exactly match how people phrase queries (voice search, question-style).

**Pattern 5: Statistics With Attribution**
"According to [Source Name] ([Year]), X% of [population] [finding]." This format is extractable because it has a complete citation. Naked statistics without attribution get deprioritized — the AI can't verify the source.

**Pattern 6: Expert Quote Block**
Attributed quotes from named experts get cited. The AI picks up: "According to [Name], [Role at Organization]: '[quote]'" as a citable unit. Build in a few of these per key piece.

### Rewriting for Extractability

When optimizing existing content:

1. **Lead with the answer** — The first paragraph should contain the core answer to the target query. Don't save it for the conclusion.

2. **Self-contained sections** — Every H2 section should be answerable as a standalone excerpt. If you have to read the introduction to understand a section, it's not self-contained.

3. **Specific over vague** — "Response time improved by 40%" beats "significant improvement." AI systems prefer citable specifics.

4. **Plain language summaries** — After complex explanations, add a 1-2 sentence plain language summary. This is what AI often lifts.

5. **Named sources** — Replace "experts say" with "[Researcher Name], [Year]." Replace "studies show" with "[Organization] found in their [Year] survey."

### Schema Markup for AI Discoverability

Schema doesn't directly make you appear in AI results — but it helps AI systems understand your content type and structure. Priority schemas:

| Schema Type | Use When | Impact |
|---|---|---|
| `Article` | Any editorial content | Establishes content as authoritative information |
| `FAQPage` | You have FAQ section | High — AI extracts Q&A pairs directly |
| `HowTo` | Step-by-step guides | High — AI uses step structure for process queries |
| `Product` | Product pages | Medium — appears in product comparison queries |
| `Organization` | Company pages | Medium — establishes entity authority |
| `Person` | Author pages | Medium — author credibility signal |

Implement via JSON-LD in the page `<head>`. Validate at schema.org/validator.

---

## Mode 3: Monitoring

AI search is volatile. Citations change. Track them.

### Manual Citation Tracking

Weekly: test your top 10 target queries on Perplexity and ChatGPT. Log:
- Were you cited? (yes/no)
- Rank in citations (1st source, 2nd, etc.)
- What text was used?

This takes ~20 minutes/week. Do it before automated solutions exist (they don't yet, not reliably).

### Google Search Console for AI Overviews

Google Search Console now shows impressions in AI Overviews under "Search type: AI Overviews" filter. Check:
- Which queries trigger AI Overview impressions for your site
- Click-through rate from AI Overviews (typically 50-70% lower than organic)
- Which pages get cited

### Visibility Signals to Track

| Signal | Tool | Frequency |
|---|---|---|
| Perplexity citations | Manual query testing | Weekly |
| ChatGPT citations | Manual query testing | Weekly |
| Google AI Overviews | Google Search Console | Weekly |
| Copilot citations | Manual query testing | Monthly |
| AI bot crawl activity | Server logs or Cloudflare | Monthly |
| Competitor AI citations | Manual query testing | Monthly |

See [references/monitoring-guide.md](references/monitoring-guide.md) for the full tracking setup and templates.

### When Your Citations Drop

If you were cited and suddenly aren't:
1. Check if competitors published something more extractable on the same topic
2. Check if your robots.txt changed (block AI bots = instant disappearance)
3. Check if your page structure changed significantly (restructuring can break citation patterns)
4. Check if your domain authority dropped (backlink loss affects AI citation too)

---

## Proactive Triggers

Flag these without being asked:

- **AI bots blocked in robots.txt** — If GPTBot, PerplexityBot, or ClaudeBot are blocked, flag it immediately. Zero AI visibility is possible until fixed, and it's a 5-minute fix. This trumps everything else.
- **No definition block on target pages** — If the page targets informational queries but has no self-contained definition in the first 300 words, it won't win definitional AI Overviews. Flag before doing anything else.
- **Unattributed statistics** — If key pages contain statistics without named sources and years, they're less citable than competitor pages that do. Flag all naked stats.
- **Schema markup absent** — If the site has no FAQPage or HowTo schema on relevant pages, flag it as a quick structural win with asymmetric impact for process and FAQ queries.
- **JavaScript-rendered content** — If important content only appears after JavaScript execution, AI crawlers may not see it at all. Flag content that's hidden behind JS rendering.

---

## Output Artifacts

| When you ask for... | You get... |
|---|---|
| AI visibility audit | Platform-by-platform citation test results + robots.txt check + content structure scorecard |
| Page optimization | Rewritten page with definition block, extractable patterns, schema markup spec, and comparison to original |
| robots.txt fix | Updated robots.txt with correct AI bot allow rules + explanation of what each bot is |
| Schema markup | JSON-LD implementation code for FAQPage, HowTo, or Article — ready to paste |
| Monitoring setup | Weekly tracking template + Google Search Console filter guide + citation log spreadsheet structure |

---

## Communication

All output follows the structured standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding includes all three
- **Actions have owners and deadlines** — no "consider reviewing..."
- **Confidence tagging** — 🟢 verified (confirmed by citation test) / 🟡 medium (pattern-based) / 🔴 assumed (extrapolated from limited data)

AI SEO is still a young field. Be honest about confidence levels. What gets cited can change as platforms evolve. State what's proven vs. what's pattern-matching.

---

## Related Skills

- **content-production**: Use to create the underlying content before optimizing for AI citation. Good AI SEO requires good content first.
- **content-humanizer**: Use after writing for AI SEO. AI-sounding content ironically performs worse in AI citation — AI systems prefer content that reads credibly, which usually means human-sounding.
- **seo-audit**: Use for traditional search ranking optimization. Run both — AI SEO and traditional SEO are complementary, not competing. Many signals overlap.
- **content-strategy**: Use when deciding which topics and queries to target for AI visibility. Strategy first, then optimize.

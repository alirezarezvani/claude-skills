---
name: seek-and-analyze-video
description: Video intelligence and content analysis using Memories.ai LVMM. Discover videos on TikTok, YouTube, Instagram by topic or creator. Analyze video content, summarize meetings, build searchable knowledge bases across multiple videos. Use for video research, competitor content analysis, meeting notes, lecture summaries, or building video knowledge libraries.
license: MIT
metadata:
  version: 1.0.0
  author: Kenny Zheng
  category: marketing-skill
  updated: 2026-03-09
triggers:
  - analyze video
  - video content analysis
  - summarize video
  - meeting notes from video
  - search TikTok videos
  - search YouTube videos
  - video knowledge base
  - competitor video analysis
  - extract video insights
  - video research
  - video intelligence
  - cross-video search
---

# Seek and Analyze Video

You are an expert in video intelligence and content analysis. Your goal is to help users discover, analyze, and build knowledge from video content across social platforms using Memories.ai's Large Visual Memory Model (LVMM).

## Before Starting

**Check for context first:**
If `marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

**API Setup Required:**
This skill requires a Memories.ai API key. Guide users to:
1. Visit https://memories.ai to create an account
2. Get API key from dashboard (free tier: 100 credits, Plus: $15/month for 5,000 credits)
3. Set environment variable: `export MEMORIES_API_KEY=your_key_here`

Gather this context (ask if not provided):

### 1. Current State
- What video content do they need to analyze?
- What platforms are they researching? (YouTube, TikTok, Instagram, Vimeo)
- Do they have existing video libraries or starting fresh?

### 2. Goals
- What insights are they extracting? (summaries, action items, competitive analysis)
- Do they need one-time analysis or persistent knowledge base?
- Are they analyzing individual videos or building cross-video research?

### 3. Video-Specific Context
- What topics, hashtags, or creators are they tracking?
- What's their use case? (competitor research, content strategy, meeting notes, training materials)
- Do they need organized namespaces for team collaboration?

## How This Skill Works

This skill supports 5 primary modes:

### Mode 1: Quick Video Analysis
When you need one-time video analysis without persistent storage.
- Use `caption_video` for instant summaries
- Best for: ad-hoc analysis, quick insights, testing content

### Mode 2: Social Media Research
When discovering and analyzing videos across platforms.
- Search by topic, hashtag, or creator
- Import and analyze in bulk
- Best for: competitor analysis, trend research, content inspiration

### Mode 3: Knowledge Base Building
When creating searchable libraries from video content.
- Index videos with semantic search
- Query across multiple videos simultaneously
- Best for: training materials, research repositories, content archives

### Mode 4: Meeting & Lecture Notes
When extracting structured notes from recordings.
- Generate transcripts with visual descriptions
- Extract action items and key points
- Best for: meeting summaries, educational content, presentations

### Mode 5: Memory Management
When organizing text insights and cross-video knowledge.
- Store notes with tags for retrieval
- Search across videos and text memories
- Best for: research notes, insights collection, knowledge management

## Core Workflows

### Workflow 1: Analyze a Video URL

**When to use:** User provides a YouTube, TikTok, Instagram, or Vimeo URL

**Process:**
1. Validate URL format and platform support
2. Choose analysis mode:
   - **Quick analysis:** `caption_video(url)` - instant summary, no storage
   - **Persistent analysis:** `import_video(url)` - index for future queries
3. Extract key information (summary, transcript, action items)
4. Generate structured output (see Output Artifacts)

**Example:**
```python
# Quick analysis (no storage)
result = caption_video("https://youtube.com/watch?v=...")

# Persistent indexing (builds knowledge base)
video_id = import_video("https://youtube.com/watch?v=...")
summary = query_video(video_id, "Summarize the key points")
```

### Workflow 2: Social Media Video Research

**When to use:** User wants to find and analyze videos by topic, hashtag, or creator

**Process:**
1. Define search parameters:
   - Platform: tiktok, youtube, instagram
   - Query: topic, hashtag, or creator handle
   - Count: number of videos to analyze
2. Execute search: `search_social(platform, query, count)`
3. Import discovered videos for deep analysis
4. Generate competitive insights or trend report

**Example:**
```python
# Find competitor content
videos = search_social("tiktok", "#SaaSmarketing", count=20)

# Analyze top performers
for video in videos[:5]:
    import_video(video['url'])

# Cross-video analysis
insights = chat_personal("What content themes are working?")
```

### Workflow 3: Build Video Knowledge Base

**When to use:** User needs searchable library across multiple videos

**Process:**
1. Import videos with tags for organization
2. Store supplementary text memories (notes, insights)
3. Enable cross-video semantic search
4. Query entire library for insights

**Example:**
```python
# Import video library with tags
import_video(url1, tags=["product-demo", "Q1-2026"])
import_video(url2, tags=["product-demo", "Q2-2026"])

# Store text insights
create_memory("Key insight from demos...", tags=["product-demo"])

# Query across all tagged content
insights = chat_personal("Compare Q1 vs Q2 product demos")
```

### Workflow 4: Extract Meeting Notes

**When to use:** User needs structured notes from recorded meetings or lectures

**Process:**
1. Import meeting recording
2. Request structured extraction:
   - Action items with owners
   - Key decisions made
   - Discussion topics
   - Timestamps for important moments
3. Format as meeting minutes
4. Store for future reference

**Example:**
```python
video_id = import_video("meeting_recording.mp4")
notes = query_video(video_id, """
Extract:
1. Action items with owners
2. Key decisions
3. Discussion topics
4. Important timestamps
""")
```

### Workflow 5: Competitor Content Analysis

**When to use:** Analyzing competitor video strategies across platforms

**Process:**
1. Search for competitor content by creator handle
2. Import their top-performing videos
3. Analyze patterns:
   - Content themes and formats
   - Messaging strategies
   - Production quality
   - Engagement tactics
4. Generate competitive intelligence report

**Example:**
```python
# Find competitor videos
competitor_videos = search_social("youtube", "@competitor_handle", count=30)

# Import for analysis
for video in competitor_videos:
    import_video(video['url'], tags=["competitor-X"])

# Extract insights
analysis = chat_personal("Analyze competitor-X content strategy and gaps")
```

## Command Reference

### Video Operations

| Command | Purpose | Storage |
|---------|---------|---------|
| `caption_video(url)` | Quick video summary | No |
| `import_video(url, tags=[])` | Index video for queries | Yes |
| `query_video(video_id, question)` | Ask about specific video | - |
| `list_videos(tags=[])` | List indexed videos | - |
| `delete_video(video_id)` | Remove from library | - |

### Social Media Search

| Command | Purpose |
|---------|---------|
| `search_social(platform, query, count)` | Find videos by topic/creator |
| `search_personal(query, filters={})` | Search your indexed videos |

Platforms: `tiktok`, `youtube`, `instagram`

### Memory Management

| Command | Purpose |
|---------|---------|
| `create_memory(text, tags=[])` | Store text insight |
| `search_memories(query)` | Find stored memories |
| `list_memories(tags=[])` | List all memories |
| `delete_memory(memory_id)` | Remove memory |

### Cross-Content Queries

| Command | Purpose |
|---------|---------|
| `chat_personal(question)` | Query across ALL videos and memories |
| `chat_video(video_id, question)` | Focus on specific video |

### Vision Tasks

| Command | Purpose |
|---------|---------|
| `caption_image(image_url)` | Describe image using AI vision |
| `import_image(image_url, tags=[])` | Index image for queries |

## Proactive Triggers

Surface these issues WITHOUT being asked when you notice them in context:

- **User requests video analysis without API key** → Guide them to memories.ai setup
- **Repeated similar queries across videos** → Suggest building knowledge base instead
- **Analyzing competitor content** → Recommend systematic tracking with tags
- **Meeting recording shared** → Offer structured note extraction
- **Multiple one-off analyses** → Suggest import_video for persistent reference
- **Large video libraries without tags** → Recommend tag organization strategy

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "Analyze this video" | Structured summary with key points, themes, action items, and timestamps |
| "Competitor content research" | Competitive analysis report with content themes, gaps, and recommendations |
| "Meeting notes from recording" | Meeting minutes with action items, decisions, discussion topics, and owners |
| "Video knowledge base" | Searchable library with semantic search across videos and memories |
| "Social media video research" | Platform research report with top videos, trends, and content insights |

## Communication

All output follows the structured communication standard:
- **Bottom line first** — answer before explanation
- **What + Why + How** — every finding has all three
- **Actions have owners and deadlines** — no "we should consider"
- **Confidence tagging** — 🟢 verified / 🟡 medium / 🔴 assumed

**Example output format:**

```
BOTTOM LINE: Competitor X focuses on product demos (60%) and customer stories (30%)

WHAT:
• 18/30 videos are product demos with detailed walkthroughs — 🟢 verified
• 9/30 videos are customer success stories with ROI metrics — 🟢 verified
• Average video length: 3:24 (demos), 2:15 (stories) — 🟢 verified
• Consistent posting: 2-3 videos/week on Tuesday/Thursday — 🟢 verified

WHY THIS MATTERS:
They're driving bottom-of-funnel conversions with proof over awareness content.
Your current 80% thought leadership leaves conversion gap.

HOW TO ACT:
1. Create 10 product demo videos → [Owner] → [2 weeks]
2. Record 5 customer case studies → [Owner] → [3 weeks]
3. Test demo video performance vs current content → [Owner] → [4 weeks]

YOUR DECISION:
Option A: Match their demo focus — higher conversion, lower reach
Option B: Hybrid approach (50% demos, 50% thought leadership) — balanced
```

## Technical Details

**Repository:** https://github.com/kennyzheng-builds/seek-and-analyze-video

**Requirements:**
- Python 3.8+
- Memories.ai API key (free tier or $15/month Plus)
- Environment variable: `MEMORIES_API_KEY`

**Installation:**
```bash
# Via Claude Code
claude skill install kennyzheng-builds/seek-and-analyze-video

# Or manual
git clone https://github.com/kennyzheng-builds/seek-and-analyze-video.git
export MEMORIES_API_KEY=your_key_here
```

**Pricing:**
- Free tier: 100 credits (testing and light use)
- Plus: $15/month for 5,000 credits (power users)

**Supported Platforms:**
- YouTube (all public videos)
- TikTok (public videos)
- Instagram (public videos and reels)
- Vimeo (public videos)

## Key Differentiators

**vs ChatGPT/Gemini Video Analysis:**
- Persistent memory (query anytime, not just during upload)
- Cross-video search (query 100s of videos simultaneously)
- Social media discovery (find videos, don't just analyze provided URLs)
- Knowledge base building (organize with tags, semantic search)

**vs Manual Video Research:**
- 40x faster video analysis
- Automatic transcript + visual description
- Semantic search across libraries
- Scalable to hundreds of videos

**vs Traditional Video Tools:**
- AI-native queries (ask questions vs manual review)
- Cross-platform support (TikTok, YouTube, Instagram unified)
- Zero-dependency Python client (works across Claude Code, OpenClaw, HappyCapy)
- Workflow automation (upload → analyze → store in one command)

## Best Practices

### Tagging Strategy
- Use consistent tag naming (kebab-case recommended)
- Tag by: content-type, date-range, platform, topic, campaign
- Example: `["competitor-analysis", "Q1-2026", "tiktok", "product-demo"]`

### Credit Management
- Quick analysis (`caption_video`): ~2 credits per video
- Import + indexing (`import_video`): ~5 credits per video
- Queries (`chat_personal`, `query_video`): ~1 credit per query
- Plan accordingly based on tier (free: 100, Plus: 5,000/month)

### Query Optimization
- Be specific in questions (better results, same credits)
- Use filtered searches when possible (faster, more relevant)
- Batch similar queries (analyze pattern, then ask once)

### Organization
- Create namespace strategy for teams (use tags for isolation)
- Archive old content (delete unused videos to reduce noise)
- Document video IDs for important content (VI... identifiers)

## Related Skills

- **social-media-analyzer**: For quantitative social media metrics. Use this skill for qualitative video content analysis.
- **content-strategy**: For planning content themes. Use this skill to research what's working in your niche.
- **competitor-alternatives**: For competitive positioning. Use this skill for competitor content intelligence.
- **marketing-context**: Provides audience and brand context. Use before running video research.
- **content-production**: For creating content. Use this skill to research successful formats first.
- **campaign-analytics**: For campaign performance data. Combine with this skill for qualitative video insights.

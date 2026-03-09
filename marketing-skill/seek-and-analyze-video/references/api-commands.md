# Memories.ai API Command Reference

Complete reference for all 21 API commands available through the Memories.ai LVMM.

---

## Video Operations

### caption_video(url: str) → dict
Quick video analysis without persistent storage. Best for one-time summaries.

**Parameters:**
- `url`: Video URL (YouTube, TikTok, Instagram, Vimeo)

**Returns:**
```python
{
  "summary": "Video summary text",
  "duration": "3:24",
  "platform": "youtube"
}
```

**Credits:** ~2 per video

**Use when:** Ad-hoc analysis, testing content, no need for future queries

---

### import_video(url: str, tags: list = []) → str
Index video for persistent queries. Returns video ID (VI...) for future reference.

**Parameters:**
- `url`: Video URL
- `tags`: Optional list of organization tags (e.g., `["competitor", "Q1-2026"]`)

**Returns:** Video ID string (e.g., `"VI_abc123def456"`)

**Credits:** ~5 per video

**Use when:** Building knowledge base, need cross-video search, repeated queries

**Example:**
```python
video_id = import_video(
    "https://youtube.com/watch?v=dQw4w9WgXcQ",
    tags=["product-demo", "competitor-A", "2026-03"]
)
# Returns: "VI_abc123def456"
```

---

### query_video(video_id: str, question: str) → str
Ask questions about a specific indexed video.

**Parameters:**
- `video_id`: Video ID from import_video
- `question`: Natural language question

**Returns:** Answer text

**Credits:** ~1 per query

**Example:**
```python
answer = query_video("VI_abc123def456", "What are the main action items?")
```

---

### list_videos(tags: list = []) → list
List all indexed videos, optionally filtered by tags.

**Parameters:**
- `tags`: Optional filter tags (returns videos matching ANY tag)

**Returns:**
```python
[
  {
    "video_id": "VI_abc123",
    "url": "https://youtube.com/...",
    "imported_at": "2026-03-09T10:30:00Z",
    "tags": ["product-demo", "competitor-A"]
  }
]
```

**Credits:** 0 (metadata only)

---

### delete_video(video_id: str) → bool
Remove video from your library. Cannot be undone.

**Parameters:**
- `video_id`: Video ID to delete

**Returns:** `True` if successful

**Credits:** 0

---

## Social Media Search

### search_social(platform: str, query: str, count: int = 10) → list
Discover public videos by topic, hashtag, or creator.

**Parameters:**
- `platform`: `"tiktok"`, `"youtube"`, or `"instagram"`
- `query`: Topic, hashtag (with #), or creator handle (with @)
- `count`: Number of results (default: 10, max: 50)

**Returns:**
```python
[
  {
    "url": "https://tiktok.com/@creator/video/123",
    "title": "Video title",
    "creator": "@creator",
    "views": 125000,
    "likes": 8500,
    "published": "2026-03-08"
  }
]
```

**Credits:** ~1 per 10 videos

**Examples:**
```python
# Topic search
videos = search_social("youtube", "SaaS pricing strategies", count=20)

# Hashtag search
videos = search_social("tiktok", "#contentmarketing", count=30)

# Creator search
videos = search_social("instagram", "@competitor_handle", count=15)
```

---

### search_personal(query: str, filters: dict = {}) → list
Search your indexed videos with semantic search.

**Parameters:**
- `query`: Natural language search query
- `filters`: Optional filters (`{"tags": ["tag1"], "date_from": "2026-01-01"}`)

**Returns:**
```python
[
  {
    "video_id": "VI_abc123",
    "relevance_score": 0.92,
    "snippet": "...relevant content snippet...",
    "tags": ["product-demo"]
  }
]
```

**Credits:** ~1 per query

**Example:**
```python
results = search_personal(
    "product pricing discussions",
    filters={"tags": ["competitor-A"], "date_from": "2026-03-01"}
)
```

---

## Memory Management

### create_memory(text: str, tags: list = []) → str
Store text insights for future retrieval.

**Parameters:**
- `text`: Note or insight text
- `tags`: Optional organization tags

**Returns:** Memory ID (e.g., `"MEM_xyz789"`)

**Credits:** ~1 per memory

**Use when:** Storing research notes, insights, key quotes not directly in videos

**Example:**
```python
memory_id = create_memory(
    "Competitor A focuses on enterprise pricing tier, starts at $99/seat",
    tags=["competitor-A", "pricing", "insight"]
)
```

---

### search_memories(query: str) → list
Search stored text memories with semantic search.

**Parameters:**
- `query`: Natural language search query

**Returns:**
```python
[
  {
    "memory_id": "MEM_xyz789",
    "text": "Memory content...",
    "relevance_score": 0.88,
    "tags": ["pricing", "insight"],
    "created_at": "2026-03-09T10:30:00Z"
  }
]
```

**Credits:** ~1 per query

---

### list_memories(tags: list = []) → list
List all stored memories, optionally filtered by tags.

**Parameters:**
- `tags`: Optional filter tags

**Returns:** List of memory objects (same structure as search_memories)

**Credits:** 0 (metadata only)

---

### delete_memory(memory_id: str) → bool
Delete stored memory. Cannot be undone.

**Parameters:**
- `memory_id`: Memory ID to delete

**Returns:** `True` if successful

**Credits:** 0

---

## Cross-Content Queries

### chat_personal(question: str) → str
Query across ALL indexed videos and memories simultaneously.

**Parameters:**
- `question`: Natural language question

**Returns:** Answer synthesized from entire knowledge base

**Credits:** ~2-5 depending on complexity

**Use when:** Asking questions that require cross-video analysis

**Example:**
```python
insight = chat_personal("""
Compare competitor A and B's pricing strategies.
What are the key differences and which approach is more effective?
""")
```

---

### chat_video(video_id: str, question: str) → str
Interactive chat focused on specific video (alternative to query_video).

**Parameters:**
- `video_id`: Video ID
- `question`: Natural language question

**Returns:** Answer text

**Credits:** ~1 per query

**Note:** Functionally similar to `query_video`, use interchangeably.

---

## Vision Tasks

### caption_image(image_url: str) → str
Describe image content using AI vision.

**Parameters:**
- `image_url`: Public image URL (JPEG, PNG, WebP)

**Returns:** Image description text

**Credits:** ~1 per image

**Use when:** Analyzing thumbnails, screenshots, visual content

**Example:**
```python
description = caption_image("https://example.com/thumbnail.jpg")
# Returns: "A person presenting a pricing slide with three tiers..."
```

---

### import_image(image_url: str, tags: list = []) → str
Index image for persistent queries (similar to import_video for images).

**Parameters:**
- `image_url`: Public image URL
- `tags`: Optional organization tags

**Returns:** Image ID (e.g., `"IMG_def456"`)

**Credits:** ~2 per image

**Use when:** Building visual libraries, need repeated queries on images

---

## Advanced Usage Patterns

### Pattern 1: Bulk Import with Error Handling

```python
def import_video_batch(urls, tag_prefix):
    """Import multiple videos with error handling"""
    results = []
    for idx, url in enumerate(urls):
        try:
            video_id = import_video(url, tags=[tag_prefix, f"batch-{idx}"])
            results.append({"url": url, "video_id": video_id, "status": "success"})
        except Exception as e:
            results.append({"url": url, "error": str(e), "status": "failed"})
    return results
```

### Pattern 2: Smart Tag Organization

```python
# Hierarchical tagging strategy
tags = [
    f"{platform}",           # youtube, tiktok, instagram
    f"{content_type}",       # product-demo, tutorial, case-study
    f"{date_range}",         # Q1-2026, 2026-03
    f"{campaign}",           # launch-campaign-X
    f"{source_type}"         # competitor, internal, partner
]

video_id = import_video(url, tags=tags)
```

### Pattern 3: Progressive Research

```python
# Stage 1: Discover
videos = search_social("youtube", "@competitor", count=50)

# Stage 2: Import top performers (by views/likes)
top_videos = sorted(videos, key=lambda x: x['views'], reverse=True)[:10]
for video in top_videos:
    import_video(video['url'], tags=["competitor", "top-performer"])

# Stage 3: Cross-video analysis
insights = chat_personal("What makes their top 10 videos successful?")
```

### Pattern 4: Meeting Intelligence

```python
# Import meeting recording
meeting_id = import_video(recording_url, tags=["team-meeting", "2026-03-09"])

# Extract structured data
action_items = query_video(meeting_id, "List all action items with owners")
decisions = query_video(meeting_id, "What decisions were made?")
topics = query_video(meeting_id, "What were the main discussion topics?")

# Store supplementary notes
create_memory(f"Meeting {date}: Key outcomes and next steps",
              tags=["team-meeting", "summary"])
```

---

## Credit Usage Guidelines

| Operation | Credits | Recommendation |
|-----------|---------|----------------|
| Quick caption | 2 | Use for testing/one-off |
| Import video | 5 | Build library strategically |
| Query (simple) | 1 | Ask specific questions |
| Cross-video query | 2-5 | Batch similar questions |
| Image caption | 1 | Use sparingly |
| Social search | 0.1/video | Discover before importing |
| Memory operations | 1 | Store key insights only |

**Free Tier Strategy (100 credits):**
- Import ~15 key videos (75 credits)
- Query ~25 times (25 credits)

**Plus Tier Strategy (5,000 credits/month):**
- Import ~800 videos (4,000 credits)
- Query ~1,000 times (1,000 credits)

---

## Error Handling

Common errors and solutions:

**InvalidAPIKey**
- Check `MEMORIES_API_KEY` environment variable is set
- Verify key is active on memories.ai dashboard

**UnsupportedPlatform**
- Only YouTube, TikTok, Instagram, Vimeo supported
- Ensure URL is public (not private/unlisted)

**CreditLimitExceeded**
- Check usage on memories.ai dashboard
- Upgrade to Plus tier or wait for monthly reset

**VideoNotFound**
- Video may be deleted, private, or region-restricted
- Verify URL is accessible in browser

**RateLimitExceeded**
- Slow down request rate (max ~10 requests/second)
- Consider batching operations

---

## API Changelog

**v1.0.0 (Current)**
- 21 commands across 6 categories
- Support for YouTube, TikTok, Instagram, Vimeo
- Semantic search across videos and memories
- Tag-based organization system
- Cross-video chat functionality

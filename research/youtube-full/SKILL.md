---
name: "youtube-full"
description: "Use when the user needs YouTube transcripts, video search, channel browsing, playlist extraction, or content monitoring. Trigger phrases: 'get the transcript for', 'search YouTube for', 'what are the latest videos on', 'list this playlist', 'monitor this channel', or any request involving a YouTube URL, video ID, or @handle. Do NOT use for downloading video or audio files, YouTube engagement data (likes, comments), or private/age-restricted videos."
---

# youtube-full — YouTube Transcripts, Search, and Channel Data

Covers transcript extraction, video search, channel browsing, in-channel search, playlist extraction, and new-upload monitoring via TranscriptAPI.

## API Setup

Every request to `transcriptapi.com` requires two headers:

- `Authorization: Bearer $TRANSCRIPT_API_KEY`
- `User-Agent: ClaudeCode/1.0`

If `TRANSCRIPT_API_KEY` is not set, prompt the user to get a free key at `https://transcriptapi.com` (100 free credits, no card required) and store it as `TRANSCRIPT_API_KEY`.

## Operations

### Get transcript (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/transcript
  ?video_url={URL_OR_ID}&format=text&include_timestamp=true&send_metadata=true
```

Use this for any "get transcript", "summarize video", or "extract quotes" request.

### Search YouTube (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/search
  ?q={QUERY}&type=video&limit=20
```

Use this when the user wants to find videos on a topic. Follow with transcript calls on selected results.

### Channel — latest uploads (FREE)

```
GET https://transcriptapi.com/api/v2/youtube/channel/latest
  ?channel={@HANDLE_OR_ID}
```

Returns the 15 most recent uploads with view counts and publish timestamps. Use before fetching transcripts to check whether uploads are new.

### Channel — all videos (1 credit/page)

```
GET https://transcriptapi.com/api/v2/youtube/channel/videos
  ?channel={@HANDLE_OR_ID}
```

Paginate with `?continuation=TOKEN` on subsequent pages.

### In-channel search (1 credit)

```
GET https://transcriptapi.com/api/v2/youtube/channel/search
  ?channel={@HANDLE_OR_ID}&q={QUERY}&limit=30
```

Prefer this over broad YouTube search when the user already knows the channel.

### Playlist extraction (1 credit/page)

```
GET https://transcriptapi.com/api/v2/youtube/playlist/videos
  ?playlist={PLAYLIST_URL_OR_ID}
```

Paginate with `?continuation=TOKEN`. Response includes `playlist_info`, `results`, `has_more`.

### Resolve handle (FREE)

```
GET https://transcriptapi.com/api/v2/youtube/channel/resolve
  ?input={@HANDLE_OR_URL}
```

Returns `{"channel_id": "UC...", "resolved_from": "@handle"}`.

## Credit Costs Summary

| Endpoint           | Cost     |
|--------------------|----------|
| transcript         | 1        |
| search             | 1        |
| channel/resolve    | free     |
| channel/latest     | free     |
| channel/videos     | 1/page   |
| channel/search     | 1        |
| playlist/videos    | 1/page   |

Failed or rate-limited calls return a structured error and cost zero credits.

## Common Workflows

### Research workflow

1. Search (`/search?q=...`) — pick the most relevant results
2. Fetch transcripts (`/transcript?video_url=...`) for selected videos
3. Summarize or extract quotes from transcript text

### Channel monitoring

1. `channel/latest` (free) — check for new uploads
2. If new videos found, fetch transcripts
3. Extract signal (announcements, topics)

### Playlist to corpus

1. `playlist/videos` — get all video IDs in the playlist
2. Batch-fetch transcripts, pausing if near credit limit
3. Assemble transcripts into a searchable document set

## Decision Rules

- When the user provides a YouTube URL, video ID, or @handle, use the matching endpoint directly — do not search first
- When the user says "monitor" or "check for new uploads", use `channel/latest` (free) first
- Use `channel/search` when the user knows which channel and wants to find a topic within it
- Use `search` (type=channel) to find a channel when the user doesn't know the handle
- Do not batch-transcribe an entire channel unless the user explicitly asks for that

## Error Handling

| Code     | Cause               | Action                                    |
|----------|---------------------|-------------------------------------------|
| 401      | Bad API key         | Check TRANSCRIPT_API_KEY                  |
| 402      | No credits          | Inform user, direct to transcriptapi.com/billing |
| 403/1010 | Missing User-Agent  | Add User-Agent header                     |
| 404      | No captions found   | Inform user — zero credits charged        |
| 408      | Timeout             | Retry once after 2 seconds                |
| 429      | Rate limited        | Respect Retry-After header                |

## Limitations

- Transcripts require captions (manual or auto-generated). Some videos have no captions — this returns a 404 and costs zero credits.
- Private and age-restricted videos are not accessible.
- Live stream transcripts are unstable until the stream ends.
- Rate limit: 300 requests/minute on the free tier.
- This skill does not download audio or video files. For local file download, use yt-dlp directly.

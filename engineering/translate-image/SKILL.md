---
name: "translate-image"
description: "AI-powered image translation, OCR, and text removal"
---

# Translate Image

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Media & Content / Image Processing

## Overview

AI-powered image translation skill with 4 tools: translate text in images across 130+ languages while preserving layout, extract text via OCR with bounding boxes, remove text using AI inpainting, and Gemini-powered text extraction with optional translation.

## Core Capabilities

- **Translate Image** — Translate text in images across 130+ languages while preserving the original visual layout (manga, comics, street signs, menus, documents)
- **Extract Text (OCR)** — Extract all text from images with bounding boxes, language detection, and confidence scores
- **Remove Text** — Detect and remove text overlays using AI inpainting
- **Image to Text (AI OCR)** — Gemini-powered text extraction with optional multi-language translation

## When to Use

- Translating manga, comics, or webtoons
- Converting foreign-language documents
- Extracting text from screenshots or photos
- Removing text overlays from images
- Localizing visual content for international audiences
- OCR tasks requiring multilingual support

## Key Workflows

### 1. Translate Image

```bash
# Translate image from Japanese to English
python3 -m translate_image translate \
  --input image.jpg \
  --output translated.png \
  --from ja \
  --to en \
  --font NotoSans
```

### 2. Extract Text (OCR)

```bash
# Extract text with bounding boxes
python3 -m translate_image ocr \
  --input screenshot.png \
  --output results.json \
  --include-bboxes
```

### 3. Remove Text

```bash
# Remove text overlay from image
python3 -m translate_image remove \
  --input image_with_text.png \
  --output clean_image.png
```

### 4. Image to Text with Translation

```bash
# Extract and translate in one step
python3 -m translate_image i2t \
  --input document.png \
  --from zh \
  --to en \
  --format markdown
```

## Requirements

- curl
- python3
- TRANSLATEIMAGE_API_KEY environment variable

Get an API key at: https://translateimage.io/dashboard

## Supported Languages

130+ languages including:
- English, Japanese, Chinese (Simplified/Traditional), Korean
- Spanish, French, German, Italian, Portuguese
- Arabic, Hindi, Russian, Thai, Vietnamese
- And many more...

## Font Options

| Font | Best For |
|------|----------|
| NotoSans | General use (default) |
| WildWords | Manga, comics |
| BadComic | Manga, comics |
| MaShanZheng | Chinese content |
| RIDIBatang | Korean content |
| Bangers | Bold, impact text |
| Edo | Japanese-style |
| KomikaJam | Comics |

## Translation Models

| Model | Notes |
|-------|-------|
| gemini-2.5-flash | Default — fast and high quality |
| gpt-5.1 | OpenAI |
| grok4-fast | xAI |
| deepseek | DeepSeek |
| kimi-k2 | Moonshot/MiniMax |

## Common Pitfalls

1. Not setting TRANSLATEIMAGE_API_KEY before running tools
2. Using wrong font for the content type (e.g., regular font for manga)
3. Not specifying source language when it's ambiguous
4. Expecting perfect layout preservation on complex images
5. Using low-resolution images for OCR (results in poor accuracy)

## Best Practices

1. Set API key in environment before running: `export TRANSLATEIMAGE_API_KEY=your-key`
2. Choose appropriate font based on content type
3. For manga/comics, use WildWords or BadComic fonts
4. For OCR, use high-resolution images for better accuracy
5. Specify both source and target languages when known
6. Check confidence scores in OCR output for quality assurance

## Script Interfaces

- `python3 -m translate_image translate --help`
- `python3 -m translate_image ocr --help`
- `python3 -m translate_image remove --help`
- `python3 -m translate_image i2t --help`

## Failure Handling

- If API key missing: Fail early with clear message to set TRANSLATEIMAGE_API_KEY
- If image unreadable: Surface specific error (corrupt file, unsupported format)
- If translation fails: Return original error from API with suggestions
- If rate limited: Implement exponential backoff with user notification

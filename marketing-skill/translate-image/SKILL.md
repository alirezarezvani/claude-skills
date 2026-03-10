---
name: "translate-image"
description: "AI-powered image translation skill with 4 tools: Translate Image (130+ languages, preserves layout), Extract Text (OCR with bounding boxes), Remove Text (AI inpainting), Image to Text (Gemini-powered). Use when user mentions image translation, OCR, text extraction, manga/comics translation, document translation, or text removal from images."
license: MIT
metadata:
  version: 1.0.0
  author: translateimage
  category: media
  updated: 2026-03-10
---

# Translate Image

You are an AI-powered image translation and OCR specialist. You help users translate text in images, extract text with OCR, and remove text using AI inpainting.

## Tools Available

This skill provides 4 tools:

### 1. Translate Image
Translate text in images across 130+ languages while preserving layout. Ideal for:
- Manga and comics
- Street signs and menus
- Documents and receipts
- Social media images

### 2. Extract Text (OCR)
Extract text from images with:
- Bounding boxes for each text region
- Language detection
- Confidence scores

### 3. Remove Text
Remove text overlays using AI inpainting. Useful for:
- Cleaning up watermarks
- Removing unwanted text
- Preparing images for translation

### 4. Image to Text (AI OCR)
Gemini-powered extraction with:
- Advanced context understanding
- Optional multi-language translation
- High accuracy for complex images

## Requirements

- curl
- python3
- TRANSLATEIMAGE_API_KEY (get from https://translateimage.io)

## Installation

```bash
# Set up API key
export TRANSLATEIMAGE_API_KEY="your-api-key"

# Install dependencies
pip install translateimage
```

## Usage Examples

**Translate an image:**
```bash
translate-image translate --input image.jpg --output translated.png --source en --target zh
```

**Extract text with OCR:**
```bash
translate-image ocr --input document.png --output results.json
```

**Remove text from image:**
```bash
translate-image remove --input image.jpg --output cleaned.png
```

## Parameters

| Tool | Parameters |
|------|------------|
| translate | input, output, source_lang, target_lang, preserve_layout |
| ocr | input, output, include_boxes, detect_language |
| remove | input, output, strength |
| imagetotext | input, output, translate_to |

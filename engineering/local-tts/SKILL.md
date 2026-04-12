---
name: "local-tts"
description: "Use when the user asks to generate speech, say something out loud, create a voiceover, clone a voice, or convert text to audio. Runs 100% locally via VoxCPM2 — 30 languages, voice design, voice cloning. No API calls, no cost."
---

# Local TTS — Offline Text-to-Speech

**Tier:** POWERFUL
**Category:** Engineering
**Tags:** TTS, voice, audio, voice-cloning, offline, Apple Silicon, VoxCPM2

## Overview

Local TTS brings text-to-speech, voice design, and voice cloning to Claude Code — entirely offline. Powered by VoxCPM2 (2B params, Apache-2.0), it runs on Apple Silicon via Metal (MPS). No API keys, no cloud, no cost.

## Three Modes

### 1. Text-to-Speech
Write text, get a 48 kHz wav file. 30 languages auto-detected.

### 2. Voice Design
Describe a voice in natural language — age, gender, accent, emotion — and the model generates it. No reference audio needed.

### 3. Voice Cloning
Provide a 3-10 second reference clip. The model reproduces the timbre, accent, and emotional tone. Combinable with style guidance.

## Setup

```bash
# Install the plugin
/plugin marketplace add vdk888/local-tts
/plugin install local-tts@local-tts-marketplace

# First use creates a Python venv and downloads the model (~10 GB one-time)
```

## Requirements

- macOS with Apple Silicon (M1/M2/M3/M4) or Linux with CUDA
- Python 3.10+
- ~10 GB free disk space

## Links

- **GitHub:** https://github.com/vdk888/local-tts
- **Demo video:** https://bubble-sentinel.netlify.app/local-tts.html
- **License:** Apache-2.0
- **Author:** [Bubble Invest](https://bubbleinvest.org)

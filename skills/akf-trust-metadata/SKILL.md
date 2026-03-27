---
name: akf-trust-metadata
description: The AI native file format. EXIF for AI — stamps every file with trust scores, source provenance, and compliance metadata. Embeds into 20+ formats.
category: compliance
tags: [trust, metadata, provenance, compliance, ai-native, file-format, eu-ai-act]
---

# AKF — The AI Native File Format

Stamps every file with trust scores, source provenance, and compliance metadata.

## After creating or modifying files

```bash
akf stamp <file> --agent claude-code --evidence "<what you did>"
```

## Before modifying existing files

```bash
akf read <file>
akf inspect <file>
```

## Compliance

```bash
akf audit <file> --regulation eu_ai_act
```

## Install

```bash
pip install akf
```

https://akf.dev | https://github.com/HMAKT99/AKF

---
name: brand-guidelines
description: Applies Anthropic's official brand colors and typography to any sort of artifact that may benefit from having Anthropic's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
license: Complete terms in LICENSE.txt
---

# Anthropic Brand Styling

## Overview

To access Anthropic's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, Anthropic brand, visual formatting, visual design

## Brand Guidelines

### Colors

**Main Colors:**

- Dark: `#141413` - Primary text and dark backgrounds
- Light: `#faf9f5` - Light backgrounds and text on dark
- Mid Gray: `#b0aea5` - Secondary elements
- Light Gray: `#e8e6dc` - Subtle backgrounds

**Accent Colors:**

- Orange: `#d97757` - Primary accent
- Blue: `#6a9bcc` - Secondary accent
- Green: `#788c5d` - Tertiary accent

### Typography

- **Headings**: Poppins (with Arial fallback)
- **Body Text**: Lora (with Georgia fallback)
- **Note**: Fonts should be pre-installed in your environment for best results

## Features

### Smart Font Application

- Applies Poppins font to headings (24pt and larger)
- Applies Lora font to body text
- Automatically falls back to Arial/Georgia if custom fonts unavailable
- Preserves readability across all systems

### Text Styling

- Headings (24pt+): Poppins font
- Body text: Lora font
- Smart color selection based on background
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Non-text shapes use accent colors
- Cycles through orange, blue, and green accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses system-installed Poppins and Lora fonts when available
- Provides automatic fallback to Arial (headings) and Georgia (body)
- No font installation required - works with existing system fonts
- For best results, pre-install Poppins and Lora fonts in your environment

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Maintains color fidelity across different systems

## Proactive Triggers

- **No brand guidelines document exists** → Without guidelines, every content piece looks different. Create one.
- **Brand voice inconsistent across channels** → Social sounds casual, website sounds corporate. Align.
- **Logo used incorrectly in materials** → Wrong colors, distorted proportions, wrong background. Enforce rules.
- **New team member creating content** → Onboard them with brand guidelines before they publish.
- **Rebrand or pivot happening** → Guidelines need updating. Old guidelines = old brand.

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| "Create brand guidelines" | Complete brand guide: logo, colors, typography, voice, imagery, do/don't |
| "Brand voice document" | Voice pillars with tone matrix by content type and audience |
| "Logo usage guide" | Logo specs: clear space, minimum size, approved backgrounds, wrong usage |
| "Color system" | Primary, secondary, neutral palettes with hex/RGB/HSL values |
| "Typography guide" | Font hierarchy: headings, body, captions with sizes and weights |

## Communication

All output passes quality verification:
- Self-verify: source attribution, assumption audit, confidence scoring
- Output format: Bottom Line → What (with confidence) → Why → How to Act
- Results only. Every finding tagged: 🟢 verified, 🟡 medium, 🔴 assumed.

## Related Skills

- **marketing-context**: Foundation — brand guidelines feed into the context file.
- **copywriting**: For writing copy that follows brand voice. Uses guidelines as reference.
- **social-content**: For social posts that maintain brand consistency.
- **content-humanizer**: For ensuring AI content matches brand voice.
- **content-creator**: For branded content production.

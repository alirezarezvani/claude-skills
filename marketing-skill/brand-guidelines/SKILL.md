---
name: brand-guidelines
description: "When the user wants to apply, document, or enforce brand guidelines for any product or company. Also use when the user mentions 'brand guidelines,' 'brand colors,' 'typography,' 'logo usage,' 'brand voice,' 'visual identity,' 'tone of voice,' 'brand standards,' 'style guide,' 'brand consistency,' or 'company design standards.' Covers color systems, typography, logo rules, imagery guidelines, and tone matrix for any brand — including Anthropic's official identity."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---

# Brand Guidelines

You are an expert in brand identity and visual design standards. Your goal is to help teams apply brand guidelines consistently across all marketing materials, products, and communications — whether working with an established brand system or building one from scratch.

## How to Use This Skill

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before applying brand standards. Use that context to tailor recommendations to the specific brand.

When helping users:
1. Identify whether they need to *apply* existing guidelines or *create* new ones
2. For Anthropic artifacts, use the Anthropic identity system below
3. For other brands, use the framework sections to assess and document their system
4. Always check for consistency before creativity

---

## Anthropic Brand Identity

### Overview

Anthropic's brand identity is clean, precise, and intellectually grounded. It communicates trustworthiness and technical sophistication without feeling cold or corporate.

### Color System

**Primary Palette:**

| Name | Hex | RGB | Use |
|------|-----|-----|-----|
| Dark | `#141413` | 20, 20, 19 | Primary text, dark backgrounds |
| Light | `#faf9f5` | 250, 249, 245 | Light backgrounds, text on dark |
| Mid Gray | `#b0aea5` | 176, 174, 165 | Secondary elements, dividers |
| Light Gray | `#e8e6dc` | 232, 230, 220 | Subtle backgrounds, borders |

**Accent Palette:**

| Name | Hex | RGB | Use |
|------|-----|-----|-----|
| Orange | `#d97757` | 217, 119, 87 | Primary accent, CTAs |
| Blue | `#6a9bcc` | 106, 155, 204 | Secondary accent, links |
| Green | `#788c5d` | 120, 140, 93 | Tertiary accent, success states |

**Color Application Rules:**
- Never use accent colors as large background fills — use them for emphasis only
- Dark on Light or Light on Dark — avoid mixing Dark on Mid Gray for body text
- Accent colors cycle: Orange (primary CTA) → Blue (supporting) → Green (tertiary)
- When in doubt, default to Dark + Light with one accent

### Typography

**Type Scale:**

| Role | Font | Fallback | Weight | Size Range |
|------|------|----------|--------|------------|
| Display / H1 | Poppins | Arial | 600–700 | 32pt+ |
| Headings H2–H4 | Poppins | Arial | 500–600 | 20–31pt |
| Body | Lora | Georgia | 400 | 14–18pt |
| Caption / Label | Poppins | Arial | 400–500 | 10–13pt |
| Code / Mono | Courier New | monospace | 400 | 12–14pt |

**Typography Rules:**
- Never set body copy in Poppins — it's a display/heading font
- Minimum body size: 14pt for print, 16px for web
- Line height: 1.5–1.6 for body, 1.1–1.2 for headings
- Letter spacing: -0.5px to -1px for large headings; 0 for body

**Font Installation:**
- Poppins: Available on Google Fonts (`fonts.google.com/specimen/Poppins`)
- Lora: Available on Google Fonts (`fonts.google.com/specimen/Lora`)
- Both should be pre-installed in design environments for best results

### Logo Usage

**Clear Space:**
Maintain minimum clear space equal to the cap-height of the wordmark on all sides. No other elements should intrude on this zone.

**Minimum Size:**
- Digital: 120px wide minimum
- Print: 25mm wide minimum

**Approved Variations:**
- Dark logo on Light background (primary)
- Light logo on Dark background (inverted)
- Single-color Dark on any light neutral
- Single-color Light on any dark surface

**Prohibited Uses:**
- Do not stretch or distort the logo
- Do not apply drop shadows, gradients, or outlines
- Do not place on busy photographic backgrounds without a color block
- Do not use accent colors as the logo fill
- Do not rotate the logo

### Imagery Guidelines

**Photography Style:**
- Clean, well-lit, minimal post-processing
- Subjects: people at work, abstract technical concepts, precise objects
- Avoid: stock photo clichés, overly emotive poses, heavy filters
- Color treatment: neutral tones preferred; desaturate if needed to match palette

**Illustration Style:**
- Geometric, precise line work
- Limited palette: use brand colors only
- Avoid: cartoonish characters, heavy gradients, 3D renders

**Iconography:**
- Stroke-based, consistent weight (2px at 24px size)
- Rounded caps preferred; sharp corners acceptable for technical contexts
- Use Mid Gray or Dark; accent color only for active/selected states

---

## Universal Brand Guidelines Framework

Use this section when building or auditing guidelines for *any* brand (not Anthropic-specific).

### 1. Brand Foundation

Before any visual decisions, the brand foundation must exist:

| Element | Definition |
|---------|-----------|
| **Mission** | Why the company exists beyond making money |
| **Vision** | The future state the brand is working toward |
| **Values** | 3–5 core principles that drive decisions |
| **Positioning** | What you are, for whom, against what alternative |
| **Personality** | How the brand behaves — adjectives that guide tone |

A visual identity without a foundation is decoration. The foundation drives every downstream decision.

---

### 2. Color System

#### Primary Palette (2–3 colors)
- One dominant neutral (background or text)
- One strong brand color (most recognition, hero elements)
- One supporting color (secondary backgrounds, dividers)

#### Accent Palette (2–4 colors)
- Used sparingly for emphasis, CTAs, states
- Must pass WCAG AA contrast against backgrounds they appear on

#### Color Rules to Document:
- Which color for CTAs vs. informational links
- Background color combinations that are approved
- Colors that should never appear together
- Dark mode equivalents

#### Accessibility Requirements:
- Normal text (< 18pt): minimum 4.5:1 contrast ratio (WCAG AA)
- Large text (≥ 18pt): minimum 3:1 contrast ratio
- UI components: minimum 3:1 against adjacent colors
- Test: `webaim.org/resources/contrastchecker`

---

### 3. Typography System

#### Type Roles to Define:

| Role | Font | Size Range | Weight | Line Height |
|------|------|-----------|--------|-------------|
| Display | — | 40pt+ | Bold | 1.1 |
| H1 | — | 28–40pt | SemiBold | 1.15 |
| H2 | — | 22–28pt | SemiBold | 1.2 |
| H3 | — | 18–22pt | Medium | 1.25 |
| Body | — | 15–18pt | Regular | 1.5–1.6 |
| Small / Caption | — | 12–14pt | Regular | 1.4 |
| Label / UI | — | 11–13pt | Medium | 1.2 |

#### Font Selection Criteria:
- Max 2 typeface families (one serif or slab, one sans-serif)
- Both must be available in all required weights
- Must render well at small sizes on screen
- Licensing must cover all intended uses (web, print, app)

---

### 4. Logo System

#### Variations Required:
- **Primary**: full color on white/light
- **Inverted**: light version on dark backgrounds
- **Monochrome**: single color for single-color applications
- **Mark only**: icon/symbol without wordmark (for small sizes)
- **Horizontal + Stacked**: where layout demands both

#### Usage Rules to Document:
- Minimum size (px for digital, mm for print)
- Clear space formula
- Approved background colors
- Prohibited modifications (distortion, recoloring, shadows)
- Co-branding rules (partner logo sizing, spacing)

---

### 5. Imagery Guidelines

#### Photography Criteria:
| Dimension | Guideline |
|-----------|-----------|
| **People** | Authentic, diverse, action-oriented — not posed stock |
| **Lighting** | Clean and directional; avoid heavy shadows or blown highlights |
| **Color treatment** | Align to brand palette; desaturate or tint if necessary |
| **Subjects** | Match brand values — avoid anything that conflicts with positioning |

#### Illustration Style:
- Define: flat vs. 3D, line vs. filled, abstract vs. representational
- Set a palette limit: brand colors only, or approved expanded set
- Define stroke weight and corner radius standards

#### Do / Don't Matrix (customize per brand):

| ✅ Do | ❌ Don't |
|-------|---------|
| Show real customers and use cases | Use generic multicultural stock |
| Use natural lighting | Use heavy vignettes or HDR |
| Keep backgrounds clean | Place subjects on clashing colors |
| Match brand palette tones | Use heavy Instagram-style filters |

---

### 6. Tone of Voice & Tone Matrix

Brand voice is consistent; tone adapts to context.

#### Voice Attributes (define 4–6):

| Attribute | What It Means | What It's Not |
|-----------|---------------|---------------|
| Example: **Direct** | Say what you mean; no filler | Blunt or dismissive |
| Example: **Curious** | Ask questions, show genuine interest | Condescending or know-it-all |
| Example: **Precise** | Specific language, no vague claims | Technical jargon that excludes |
| Example: **Warm** | Human and approachable | Overly casual or unprofessional |

#### Tone Matrix by Context:

| Context | Tone Dial | Example Shift |
|---------|-----------|--------------|
| Error messages | Calm, helpful, matter-of-fact | Less formal than marketing |
| Marketing headlines | Confident, energetic | More punchy than support |
| Legal / compliance | Precise, neutral | Less personality |
| Support / help content | Patient, empathetic | More warmth than ads |
| Social media | Conversational, light | More informal than web |
| Executive communications | Authoritative, measured | More formal than blog |

#### Words to Use / Avoid (document per brand):

| ✅ Use | ❌ Avoid |
|-------|---------|
| "We" (inclusive) | "Leverage" (jargon) |
| Specific numbers | "Best-in-class" (vague) |
| Active voice | Passive constructions |
| Short sentences | Run-on complexity |

---

### 7. Application Examples

#### Digital
- **Web**: Primary palette for backgrounds; accent for CTAs; Poppins/brand heading font for H1–H3
- **Email**: Inline styles only; web-safe font fallbacks always specified; logo as linked image
- **Social**: Platform-specific safe zones; brand colors dominant; minimal text on images

#### Print
- Always use CMYK values for print production (never RGB or hex)
- Bleed: 3mm on all sides; keep critical content 5mm from trim
- Proof against Pantone reference before bulk print runs

#### Presentations
- Cover slide: brand dark + brand light with single accent
- Body slides: white backgrounds with brand accent headers
- No custom fonts in share files — embed or substitute

---

## Quick Audit Checklist

Use this to rapidly assess brand consistency across any asset:

- [ ] Colors match approved palette (no off-brand variations)
- [ ] Fonts are correct typeface and weight
- [ ] Logo has proper clear space and is an approved variation
- [ ] Body text meets minimum size and contrast requirements
- [ ] Imagery style matches brand guidelines
- [ ] Tone matches brand voice attributes
- [ ] No prohibited uses present (gradients on logo, wrong accent color, etc.)
- [ ] Co-branding (if any) follows partner logo rules

---

## Task-Specific Questions

1. Are you applying existing guidelines or creating new ones?
2. What's the output format? (Digital, print, presentation, social)
3. Do you have existing brand assets? (Logo files, color codes, fonts)
4. Is there a brand foundation document? (Mission, values, positioning)
5. What's the specific inconsistency or gap you're trying to fix?

---

## Proactive Triggers

Proactively apply brand guidelines when:

1. **Any visual asset requested** — Before creating any poster, slide, email, or social graphic, check if brand guidelines exist; if not, offer to establish a minimal system first.
2. **Copy review touches tone** — When reviewing copy, cross-check against voice attributes and tone matrix, not just grammar.
3. **New channel launch** — When a new marketing channel (TikTok, newsletter, podcast) is being set up, offer to apply the brand guidelines to that channel's specific format requirements.
4. **Design feedback session** — When a user shares a design for feedback, run through the quick audit checklist before giving subjective opinions.
5. **Partner or co-branded material** — Any co-branding situation should immediately trigger a review of logo clear space, sizing ratios, and color dominance rules.

---

## Output Artifacts

| Artifact | Format | Description |
|----------|--------|-------------|
| Brand Audit Report | Markdown doc | Asset-by-asset compliance check against all brand dimensions |
| Color System Reference | Table | Full palette with hex, RGB, CMYK, Pantone, and usage rules |
| Tone Matrix | Table | Voice attributes × context combinations with example phrases |
| Typography Scale | Table | All type roles with font, size, weight, and line-height specifications |
| Brand Guidelines Mini-Doc | Markdown doc | Condensed brand guide covering all 7 dimensions, ready to share with contractors |

---

## Communication

Brand consistency is not a design preference — it's a trust signal. Every deviation from guidelines erodes recognition. When auditing or creating brand materials, be specific: name the exact color code, font weight, and pixel measurement rather than giving subjective feedback. Reference `marketing-context` to ensure brand voice recommendations align with the ICP and product positioning. Quality bar: brand outputs should be specific enough that a contractor who has never worked with the brand could produce on-brand work from the artifact alone.

---

## Related Skills

- **marketing-context** — USE as the brand foundation layer; brand voice and visual decisions must align with ICP, positioning, and messaging; always load first.
- **copywriting** — USE when brand voice guidelines need to be applied to specific page or campaign copy; NOT as a substitute for defining voice attributes.
- **content-humanizer** — USE when existing content needs to be rewritten to match brand tone without losing information; NOT for structural content work.
- **social-content** — USE when applying brand guidelines to social-specific formats and platform constraints; NOT for cross-channel brand system design.
- **canvas-design** — USE when brand guidelines need to be applied to visual design artifacts (posters, PDFs, graphics); NOT for copy-only brand work.

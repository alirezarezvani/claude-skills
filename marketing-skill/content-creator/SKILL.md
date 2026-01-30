---
name: content-creator
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media templates. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, social media marketing, or content strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

---

## Table of Contents

- [Keywords](#keywords)
- [Quick Start](#quick-start)
- [Core Workflows](#core-workflows)
- [Tools](#tools)
- [Reference Guides](#reference-guides)
- [Best Practices](#best-practices)
- [Integration Points](#integration-points)

---

## Keywords

content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy

---

## Quick Start

### Brand Voice Development

1. Run `scripts/brand_voice_analyzer.py` on existing content to establish baseline
2. Review `references/brand_guidelines.md` to select voice attributes
3. Apply chosen voice consistently across all content

### Blog Content Creation

1. Choose template from `references/content_frameworks.md`
2. Research keywords for topic
3. Write content following template structure
4. Run `scripts/seo_optimizer.py [file] [primary-keyword]` to optimize
5. Apply recommendations before publishing

### Social Media Content

1. Review platform best practices in `references/social_media_optimization.md`
2. Use appropriate template from `references/content_frameworks.md`
3. Optimize based on platform-specific guidelines
4. Schedule using `assets/content_calendar_template.md`

---

## Core Workflows

### Workflow 1: Establish Brand Voice (First Time Setup)

For new brands or clients:

**Step 1: Analyze Existing Content (if available)**

```bash
python scripts/brand_voice_analyzer.py existing_content.txt
```

**Step 2: Define Voice Attributes**

- Review brand personality archetypes in `references/brand_guidelines.md`
- Select primary and secondary archetypes
- Choose 3-5 tone attributes
- Document in brand guidelines

**Step 3: Create Voice Sample**

- Write 3 sample pieces in chosen voice
- Test consistency using analyzer
- Refine based on results

### Workflow 2: Create SEO-Optimized Blog Posts

**Step 1: Keyword Research**

- Identify primary keyword (search volume 500-5000/month)
- Find 3-5 secondary keywords
- List 10-15 LSI keywords

**Step 2: Content Structure**

- Use blog template from `references/content_frameworks.md`
- Include keyword in title, first paragraph, and 2-3 H2s
- Aim for 1,500-2,500 words for comprehensive coverage

**Step 3: Optimization Check**

```bash
python scripts/seo_optimizer.py blog_post.md "primary keyword" "secondary,keywords,list"
```

**Step 4: Apply SEO Recommendations**

- Adjust keyword density to 1-3%
- Ensure proper heading structure
- Add internal and external links
- Optimize meta description

### Workflow 3: Create Social Media Content

**Step 1: Platform Selection**

- Identify primary platforms based on audience
- Review platform-specific guidelines in `references/social_media_optimization.md`

**Step 2: Content Adaptation**

- Start with blog post or core message
- Use repurposing matrix from `references/content_frameworks.md`
- Adapt for each platform following templates

**Step 3: Optimization Checklist**

- Platform-appropriate length
- Optimal posting time
- Correct image dimensions
- Platform-specific hashtags
- Engagement elements (polls, questions)

### Workflow 4: Plan Content Calendar

**Step 1: Monthly Planning**

- Copy `assets/content_calendar_template.md`
- Set monthly goals and KPIs
- Identify key campaigns/themes

**Step 2: Weekly Distribution**

- Follow 40/25/25/10 content pillar ratio
- Balance platforms throughout week
- Align with optimal posting times

**Step 3: Batch Creation**

- Create all weekly content in one session
- Maintain consistent voice across pieces
- Prepare all visual assets together

---

## Tools

### Brand Voice Analyzer

Analyzes text content for voice characteristics, readability, and consistency.

**Usage:**

```bash
# Human-readable output
python scripts/brand_voice_analyzer.py content.txt

# JSON output for integrations
python scripts/brand_voice_analyzer.py content.txt json
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file` | Yes | Path to content file |
| `format` | No | Output format: `text` (default) or `json` |

**Output:**

- Voice profile (formality, tone, perspective)
- Readability score (Flesch Reading Ease)
- Sentence structure analysis
- Improvement recommendations

### SEO Optimizer

Analyzes content for SEO optimization and provides actionable recommendations.

**Usage:**

```bash
# Basic analysis
python scripts/seo_optimizer.py article.md "main keyword"

# With secondary keywords
python scripts/seo_optimizer.py article.md "main keyword" "secondary,keywords,list"

# JSON output
python scripts/seo_optimizer.py article.md "keyword" --json
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `file` | Yes | Path to content file (md or html) |
| `primary_keyword` | Yes | Main target keyword |
| `secondary_keywords` | No | Comma-separated secondary keywords |
| `--json` | No | Output in JSON format |

**Output:**

- SEO score (0-100)
- Keyword density analysis
- Structure assessment
- Meta tag suggestions
- Specific optimization recommendations

---

## Reference Guides

### When to Use Each Reference

**references/brand_guidelines.md**

- Setting up new brand voice
- Ensuring consistency across content
- Training new team members
- Resolving voice/tone questions

**references/content_frameworks.md**

- Starting any new content piece
- Structuring different content types
- Creating content templates
- Planning content repurposing

**references/social_media_optimization.md**

- Platform-specific optimization
- Hashtag strategy development
- Understanding algorithm factors
- Setting up analytics tracking

**references/analytics_guide.md**

- Tracking content performance
- Setting up measurement frameworks
- Creating performance reports
- Attribution modeling

---

## Best Practices

### Content Creation Process

1. Start with audience need/pain point
2. Research before writing
3. Create outline using templates
4. Write first draft without editing
5. Optimize for SEO
6. Edit for brand voice
7. Proofread and fact-check
8. Optimize for platform
9. Schedule strategically

### Quality Indicators

- SEO score above 75/100
- Readability appropriate for audience
- Consistent brand voice throughout
- Clear value proposition
- Actionable takeaways
- Proper visual formatting
- Platform-optimized

### Common Pitfalls to Avoid

- Writing before researching keywords
- Ignoring platform-specific requirements
- Inconsistent brand voice
- Over-optimizing for SEO (keyword stuffing)
- Missing clear CTAs
- Publishing without proofreading
- Ignoring analytics feedback

---

## Integration Points

This skill works best with:

- **Analytics platforms** - Google Analytics, social media insights for tracking (see `references/analytics_guide.md`)
- **SEO tools** - For keyword research and competitive analysis
- **Design tools** - Canva, Figma for visual content
- **Scheduling platforms** - Buffer, Hootsuite for content distribution
- **Email marketing systems** - For newsletter content campaigns

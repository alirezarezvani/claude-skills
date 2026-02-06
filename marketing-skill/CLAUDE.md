# Marketing Skills - Claude Code Guidance

This guide covers the 4 production-ready marketing skills and their Python automation tools.

## Marketing Skills Overview

**Available Skills:**
1. **content-creator/** - Content creation, brand voice, SEO optimization (2 Python tools)
2. **marketing-demand-acquisition/** - Demand generation and customer acquisition (1 Python tool)
3. **marketing-strategy-pmm/** - Product marketing and go-to-market strategy
4. **campaign-analytics/** - Multi-touch attribution, funnel conversion analysis, campaign ROI calculation (3 Python tools)

**Total Tools:** 6 Python automation tools, 9+ knowledge bases, 15+ templates

## Python Automation Tools

### 1. Brand Voice Analyzer (`content-creator/scripts/brand_voice_analyzer.py`)

**Purpose:** Analyzes text for formality, tone, perspective, and readability

**Features:**
- Formality analysis (formal vs casual language patterns)
- Tone detection (professional, conversational, technical)
- Perspective analysis (1st person, 2nd person, 3rd person)
- Readability scoring (Flesch Reading Ease formula)
- Output formats: JSON or human-readable

**Usage:**
```bash
# Basic analysis
python content-creator/scripts/brand_voice_analyzer.py content.txt

# JSON output for integrations
python content-creator/scripts/brand_voice_analyzer.py content.txt json
```

**Output Example:**
```
Brand Voice Analysis Results:
- Formality Score: 65/100 (Semi-formal)
- Tone: Professional with conversational elements
- Perspective: 2nd person (you-focused)
- Readability: 72 (College level)
```

**Implementation Notes:**
- Pure Python (standard library only)
- No external API calls or ML models
- Fast local processing (<1 second for typical content)
- Works offline

### 2. SEO Optimizer (`content-creator/scripts/seo_optimizer.py`)

**Purpose:** Comprehensive SEO analysis with actionable recommendations

**Features:**
- Keyword density analysis (primary + secondary keywords)
- Content structure evaluation (headings, paragraphs, lists)
- Meta tag validation (title, description)
- Readability assessment
- SEO score calculation (0-100)
- Actionable improvement recommendations

**Usage:**
```bash
# Basic SEO analysis
python content-creator/scripts/seo_optimizer.py article.md "primary keyword"

# With secondary keywords
python content-creator/scripts/seo_optimizer.py article.md "primary keyword" "secondary,keywords,here"

# JSON output
python content-creator/scripts/seo_optimizer.py article.md "keyword" --json
```

**Output Example:**
```
SEO Analysis Results:
- Overall SEO Score: 78/100
- Primary Keyword Density: 1.8% (target: 1-2%)
- Secondary Keyword Usage: 5/7 keywords present
- Content Structure: Good (H2, H3 hierarchy)
- Meta Description: Present (145 chars)

Recommendations:
1. Add primary keyword to H2 heading
2. Increase secondary keyword "conversion" usage
3. Add alt text to 2 images
```

**Implementation Notes:**
- 419 lines of pure algorithmic analysis
- No LLM calls or external APIs
- CLI-first design for automation
- Supports markdown and HTML input

### 3. Demand Generation Analyzer (`marketing-demand-acquisition/scripts/`)

**Purpose:** Analyze demand generation campaigns and acquisition funnels

**Features:**
- Campaign performance analysis
- Acquisition channel evaluation
- Conversion funnel metrics
- ROI calculation

**Usage:**
```bash
python marketing-demand-acquisition/scripts/demand_gen_analyzer.py campaign-data.csv
```

### Campaign Analytics Tools

#### 4. Attribution Analyzer (`campaign-analytics/scripts/attribution_analyzer.py`)

**Purpose:** Multi-touch attribution modeling across marketing channels

**Features:**
- Five attribution models (first-touch, last-touch, linear, time-decay, position-based)
- Configurable time-decay half-life
- Per-channel credit allocation and revenue attribution
- Conversion and non-conversion journey analysis

**Usage:**
```bash
python campaign-analytics/scripts/attribution_analyzer.py campaign_data.json
python campaign-analytics/scripts/attribution_analyzer.py campaign_data.json --model time-decay --half-life 14
python campaign-analytics/scripts/attribution_analyzer.py campaign_data.json --format json
```

#### 5. Funnel Analyzer (`campaign-analytics/scripts/funnel_analyzer.py`)

**Purpose:** Conversion funnel analysis with bottleneck detection

**Features:**
- Stage-to-stage conversion rates and drop-off percentages
- Automatic bottleneck identification (largest absolute and relative drops)
- Overall funnel conversion rate
- Segment comparison when multiple segments provided

**Usage:**
```bash
python campaign-analytics/scripts/funnel_analyzer.py funnel_data.json
python campaign-analytics/scripts/funnel_analyzer.py funnel_data.json --format json
```

#### 6. Campaign ROI Calculator (`campaign-analytics/scripts/campaign_roi_calculator.py`)

**Purpose:** Calculate comprehensive campaign ROI metrics with benchmarking

**Features:**
- ROI, ROAS, CPA, CPL, CAC calculation
- CTR and conversion rate metrics
- Industry benchmark comparison
- Underperformance flagging

**Usage:**
```bash
python campaign-analytics/scripts/campaign_roi_calculator.py campaign_data.json
python campaign-analytics/scripts/campaign_roi_calculator.py campaign_data.json --format json
```

## Knowledge Bases

### Content Creator References

**Location:** `content-creator/references/`

1. **brand_guidelines.md** - Brand voice framework
   - 5 personality archetypes (Expert, Friend, Innovator, Guide, Motivator)
   - Voice characteristics matrix
   - Brand consistency checklist
   - Industry-specific adaptations

2. **content_frameworks.md** - 15+ content templates
   - Blog post structures (how-to, listicle, case study)
   - Email campaign frameworks
   - Social media content patterns
   - Video script templates
   - Landing page copy structure

3. **social_media_optimization.md** - Platform-specific best practices
   - LinkedIn: Professional tone, 1,300 chars, hashtag strategy
   - Twitter/X: Concise, 280 chars, thread patterns
   - Instagram: Visual-first, captions, hashtag limits
   - Facebook: Conversational, engagement tactics
   - TikTok: Short-form video, trending sounds

### Campaign Analytics References

**Location:** `campaign-analytics/references/`

1. **attribution-models-guide.md** - Deep dive into 5 attribution models with formulas, pros/cons, selection criteria
2. **campaign-metrics-benchmarks.md** - Industry benchmarks by channel and vertical for CTR, CPC, CPM, CPA, ROAS
3. **funnel-optimization-framework.md** - Stage-by-stage optimization strategies, common bottlenecks, best practices

## User Templates

### Content Creator Assets

**Location:** `content-creator/assets/`

- Content calendar template
- SEO checklist
- Social media posting schedule
- Content brief template
- Campaign planning worksheet

**Usage:** Copy template and customize for your needs

## Integration Patterns

### Pattern 1: Content Quality Workflow

```bash
# 1. Create draft content
vim blog-post.md

# 2. Analyze brand voice
python content-creator/scripts/brand_voice_analyzer.py blog-post.md

# 3. Optimize for SEO
python content-creator/scripts/seo_optimizer.py blog-post.md "target keyword"

# 4. Refine based on feedback

# 5. Publish
```

### Pattern 2: Campaign Planning

```bash
# 1. Reference frameworks
cat content-creator/references/content_frameworks.md

# 2. Draft campaign content

# 3. Validate against brand guidelines
cat content-creator/references/brand_guidelines.md

# 4. Analyze performance
python marketing-demand-acquisition/scripts/demand_gen_analyzer.py campaign-results.csv
```

### Pattern 3: Campaign Performance Analysis

```bash
# 1. Analyze multi-touch attribution
python campaign-analytics/scripts/attribution_analyzer.py journey_data.json

# 2. Identify funnel bottlenecks
python campaign-analytics/scripts/funnel_analyzer.py funnel_data.json

# 3. Calculate campaign ROI
python campaign-analytics/scripts/campaign_roi_calculator.py campaign_data.json

# 4. Document findings using templates
# Reference: campaign-analytics/assets/campaign_report_template.md
```

## Development Commands

```bash
# Content analysis
python content-creator/scripts/brand_voice_analyzer.py content.txt
python content-creator/scripts/brand_voice_analyzer.py content.txt json

# SEO optimization
python content-creator/scripts/seo_optimizer.py article.md "main keyword"
python content-creator/scripts/seo_optimizer.py article.md "main keyword" "secondary,keywords"

# Demand generation
python marketing-demand-acquisition/scripts/demand_gen_analyzer.py data.csv

# Campaign analytics
python campaign-analytics/scripts/attribution_analyzer.py campaign_data.json
python campaign-analytics/scripts/funnel_analyzer.py funnel_data.json
python campaign-analytics/scripts/campaign_roi_calculator.py campaign_data.json
```

## Quality Standards

**All marketing Python tools must:**
- Use standard library only (no external dependencies)
- Support both JSON and human-readable output
- Provide clear error messages
- Return appropriate exit codes
- Process files locally (no API calls)

## Roadmap

**Current (Phase 1-2):** 4 skills deployed
- ✅ Content creator (brand voice + SEO)
- ✅ Demand generation & acquisition
- ✅ Product marketing strategy
- ✅ Campaign analytics (attribution, funnel, ROI)

**Phase 3 (Q2 2026):** Marketing expansion
- SEO content optimizer (advanced)
- Social media manager (multi-platform)
- Email marketing automation

**Phase 4 (Q3 2026):** Growth marketing
- Growth hacking frameworks
- Viral content analyzer
- Influencer collaboration tools

See `marketing_skills_roadmap.md` for detailed expansion plans.

## Related Skills

- **Product Team:** User research, persona generation → `../product-team/`
- **Engineering:** Web analytics integration → `../engineering-team/`
- **C-Level:** Strategic marketing planning → `../c-level-advisor/`

## Best Practices

1. **Brand Consistency** - Always reference brand_guidelines.md before creating content
2. **SEO-First** - Run seo_optimizer.py on all published content
3. **Data-Driven** - Use analytics to inform content strategy
4. **Platform-Specific** - Adapt content using social_media_optimization.md guidelines
5. **Iterative** - Analyze, optimize, republish

## Additional Resources

- **Marketing Roadmap:** `marketing_skills_roadmap.md`
- **Team Overview:** `README.md`
- **Main Documentation:** `../CLAUDE.md`

---

**Last Updated:** February 2026
**Skills Deployed:** 4/4 marketing skills production-ready
**Total Tools:** 6 Python automation tools

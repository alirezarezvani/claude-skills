# Competitive Teardown

**Tier:** POWERFUL  
**Category:** Product Team  
**Domain:** Competitive Intelligence, Product Strategy, Market Analysis

---

## Overview

Run a structured competitive analysis on any product or company. Synthesizes data from pricing pages, app store reviews, job postings, SEO signals, and social media into actionable insights: feature matrices, SWOT, positioning maps, UX audits, and a stakeholder presentation template.

---

## Core Capabilities

- Feature comparison matrix (scored 1-5 across 12 dimensions)
- Pricing model analysis (per-seat, usage-based, flat rate)
- SWOT analysis
- Positioning map (2x2 matrix)
- UX audit (onboarding, key workflows, mobile)
- Content strategy gap analysis
- Action item roadmap (quick wins / medium-term / strategic)
- Stakeholder presentation template

---

## When to Use

- Before a product strategy or roadmap session
- When a competitor launches a major feature or pricing change
- Quarterly competitive review
- Before a sales pitch where you need battle card data
- When entering a new market segment

---

## Data Collection Guide

### 1. Website Analysis

```bash
# Scrape pricing page structure
curl -s "https://competitor.com/pricing" | \
  python3 -c "
import sys
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        if data.strip():
            self.text.append(data.strip())

p = TextExtractor()
p.feed(sys.stdin.read())
print('\n'.join(p.text[:200]))
"

# Check changelog / release notes
curl -s "https://competitor.com/changelog" | grep -i "added\|new\|launched\|improved"

# Feature list from sitemap
curl -s "https://competitor.com/sitemap.xml" | grep -oP '(?<=<loc>)[^<]+' | head -50
```

Key things to capture from the website:
- Pricing tiers and price points
- Feature lists per tier
- Primary CTA and messaging
- Case studies / customer logos (signals ICP)
- Integration logos
- Trust signals (certifications, compliance badges)

### 2. App Store Reviews

```bash
# iOS reviews via RSS
curl "https://itunes.apple.com/rss/customerreviews/id=[APP_ID]/sortBy=mostRecent/json" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
entries = data.get('feed', {}).get('entry', [])
for e in entries[1:]:  # skip first (app metadata)
    rating = e.get('im:rating', {}).get('label', '?')
    title = e.get('title', {}).get('label', '')
    content = e.get('content', {}).get('label', '')
    print(f'[{rating}] {title}: {content[:200]}')
"

# Google Play via scraping (use playwright or a reviews API)
# Categorize reviews into: praise / feature requests / bugs / UX complaints
```

Review sentiment categories:
- **Praise** → what users love (defend / strengthen these)
- **Feature requests** → unmet needs (opportunity gaps)
- **Bugs** → quality signals
- **UX complaints** → friction points you can beat them on

### 3. Job Postings (Team Size & Tech Stack Signals)

```python
# Search LinkedIn / Greenhouse / Lever / Workable
import requests

# Example: scrape Greenhouse job board
def get_jobs(company_token):
    r = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{company_token}/jobs")
    return r.json().get('jobs', [])

jobs = get_jobs("competitor-name")
departments = {}
for job in jobs:
    dept = job.get('departments', [{}])[0].get('name', 'Unknown')
    departments[dept] = departments.get(dept, 0) + 1

print("Team breakdown by open roles:")
for dept, count in sorted(departments.items(), key=lambda x: -x[1]):
    print(f"  {dept}: {count} open roles")
```

Signals from job postings:
- **Engineering volume** → scaling vs. consolidating
- **Specific tech mentions** → stack (React/Vue, Postgres/Mongo, AWS/GCP)
- **Sales/CS ratio** → product-led vs. sales-led motion
- **Data/ML roles** → upcoming AI features
- **Compliance roles** → regulatory expansion

### 4. SEO Analysis

```bash
# Organic keyword gap (using Ahrefs/Semrush API or free alternatives)
# Ubersuggest, SpyFu, or SimilarWeb free tiers

# Quick domain overview via Moz free API
curl "https://moz.com/api/free/v2/url-metrics?targets[]=competitor.com" \
  -H "x-moz-token: YOUR_TOKEN"

# Check their blog topics (sitemap)
curl "https://competitor.com/sitemap-posts.xml" | \
  grep -oP '(?<=<loc>)[^<]+' | \
  sed 's|.*/||' | \
  tr '-' ' '
```

SEO signals to capture:
- Top 20 organic keywords (intent: informational / navigational / commercial)
- Domain Authority / backlink count
- Blog publishing cadence and topics
- Which pages rank (product pages vs. blog vs. docs)

### 5. Social Media Sentiment

```bash
# Twitter/X search (via API v2)
curl "https://api.twitter.com/2/tweets/search/recent?query=%40competitor+OR+%22competitor+name%22&max_results=100" \
  -H "Authorization: Bearer $TWITTER_BEARER_TOKEN" | \
  python3 -c "
import sys, json
data = json.load(sys.stdin)
tweets = data.get('data', [])
for t in tweets:
    print(t['text'][:150])
"
```

---

## Scoring Rubric (12 Dimensions, 1-5)

| # | Dimension | 1 (Weak) | 3 (Average) | 5 (Best-in-class) |
|---|-----------|----------|-------------|-------------------|
| 1 | **Features** | Core only, many gaps | Solid coverage | Comprehensive + unique |
| 2 | **Pricing** | Confusing / overpriced | Market-rate, clear | Transparent, flexible, fair |
| 3 | **UX** | Confusing, high friction | Functional | Delightful, minimal friction |
| 4 | **Performance** | Slow, unreliable | Acceptable | Fast, high uptime |
| 5 | **Docs** | Sparse, outdated | Decent coverage | Comprehensive, searchable |
| 6 | **Support** | Email only, slow | Chat + email | 24/7, great response |
| 7 | **Integrations** | 0-5 integrations | 6-25 | 26+ or deep ecosystem |
| 8 | **Security** | No mentions | SOC2 claimed | SOC2 Type II, ISO 27001 |
| 9 | **Scalability** | No enterprise tier | Mid-market ready | Enterprise-grade |
| 10 | **Brand** | Generic, unmemorable | Decent positioning | Strong, differentiated |
| 11 | **Community** | None | Forum / Slack | Active, vibrant community |
| 12 | **Innovation** | No recent releases | Quarterly | Frequent, meaningful |

---

## Feature Comparison Matrix Template

```markdown
## Feature Comparison Matrix

| Feature | [YOUR PRODUCT] | [COMPETITOR A] | [COMPETITOR B] | [COMPETITOR C] |
|---------|---------------|----------------|----------------|----------------|
| **Core Features** | | | | |
| [Feature 1] | 5 | 4 | 3 | 2 |
| [Feature 2] | 3 | 5 | 4 | 3 |
| [Feature 3] | 4 | 3 | 5 | 1 |
| **Pricing** | | | | |
| Free tier | Yes | No | Limited | Yes |
| Starting price | $X/mo | $Y/mo | $Z/mo | $W/mo |
| Enterprise | Custom | Custom | No | Custom |
| **Platform** | | | | |
| Web app | 5 | 5 | 4 | 3 |
| Mobile iOS | 4 | 3 | 5 | 2 |
| Mobile Android | 4 | 3 | 4 | 2 |
| API | 5 | 4 | 3 | 1 |
| **TOTAL SCORE** | **XX/60** | **XX/60** | **XX/60** | **XX/60** |

### Score Legend: 5=Best-in-class, 4=Strong, 3=Average, 2=Below average, 1=Weak/Missing
```

---

## Pricing Analysis Template

```markdown
## Pricing Analysis

### Model Comparison
| Competitor | Model | Entry | Mid | Enterprise | Free Trial |
|-----------|-------|-------|-----|------------|------------|
| [Yours] | Per-seat | $X | $Y | Custom | 14 days |
| [Comp A] | Usage-based | $X | $Y | Custom | 30 days |
| [Comp B] | Flat rate | $X | - | Custom | No |
| [Comp C] | Freemium | $0 | $Y | Custom | Freemium |

### Pricing Intelligence
- **Price leader:** [Competitor] at $X/mo for comparable features
- **Value leader:** [Competitor] - most features per dollar
- **Premium positioning:** [Competitor] - 2x market price, targets enterprise
- **Our position:** [Describe where you sit and why]

### Pricing Opportunity
- [e.g., "No competitor offers usage-based pricing — opportunity for SMBs"]
- [e.g., "All competitors charge per seat — flat rate could disrupt"]
- [e.g., "Freemium tier could capture top-of-funnel the others miss"]
```

---

## SWOT Analysis Template

```markdown
## SWOT Analysis: [COMPETITOR NAME]

### Strengths
- [e.g., "3x more integrations than any competitor"]
- [e.g., "Strong brand recognition in enterprise segment"]
- [e.g., "Best-in-class mobile UX (4.8 App Store rating)"]

### Weaknesses
- [e.g., "No free tier — losing top-of-funnel to freemium players"]
- [e.g., "Pricing complexity confuses buyers (3 pages of pricing)"]
- [e.g., "App store reviews cite slow support response"]

### Opportunities (for US)
- [e.g., "They have no presence in DACH — our opening"]
- [e.g., "Their API is limited — power users frustrated"]
- [e.g., "Recent layoffs in engineering suggest slower roadmap"]

### Threats (to Us)
- [e.g., "Well-funded — can undercut pricing for 12+ months"]
- [e.g., "Strong channel partner network we don't have"]
- [e.g., "Announced AI feature launching Q2 — may close our gap"]
```

---

## Positioning Map

```
                HIGH VALUE
                    |
    [COMP A]        |         [YOURS]
    (feature-rich,  |         (balanced,
     expensive)     |          mid-price)
                    |
COMPLEX ────────────┼──────────────── SIMPLE
                    |
    [COMP B]        |         [COMP C]
    (complex,       |         (simple,
     cheap)         |          cheap)
                    |
                 LOW VALUE

Axes: X = Complexity (Simple ↔ Complex)
      Y = Value delivered (Low ↔ High)
      
Bubble size = market share or funding
```

---

## UX Audit Checklist

```markdown
## UX Audit: [COMPETITOR]

### Onboarding Flow
- [ ] Time to first value (TTFV): _____ minutes
- [ ] Steps to activation: _____
- [ ] Email verification required? Yes / No
- [ ] Credit card required for trial? Yes / No
- [ ] Onboarding checklist / wizard? Yes / No
- [ ] Empty state quality: 1-5 ___

### Key Workflows
| Workflow | Steps | Friction Points | Our Score | Their Score |
|----------|-------|-----------------|-----------|-------------|
| [Core action 1] | X | [notes] | X/5 | X/5 |
| [Core action 2] | X | [notes] | X/5 | X/5 |
| [Core action 3] | X | [notes] | X/5 | X/5 |

### Mobile Experience
- iOS rating: _____ / 5 ([X] reviews)
- Android rating: _____ / 5 ([X] reviews)
- Mobile feature parity: Full / Partial / Web-only
- Top mobile complaint: _____
- Top mobile praise: _____

### Navigation & IA
- [ ] Global search available? 
- [ ] Keyboard shortcuts?
- [ ] Breadcrumbs / clear navigation?
- [ ] Help / docs accessible in-app?
```

---

## Action Items Template

```markdown
## Action Items from Competitive Teardown

### Quick Wins (0-4 weeks, low effort, high impact)
- [ ] [e.g., "Add G2/Capterra badges — competitor displays these prominently"]
- [ ] [e.g., "Publish integration page — competitor's ranks for '[product] integrations'"]
- [ ] [e.g., "Add comparison landing page targeting '[competitor] alternative' keyword"]

### Medium-Term (1-3 months, moderate effort)
- [ ] [e.g., "Launch free tier to capture top-of-funnel competitor is missing"]
- [ ] [e.g., "Improve onboarding — competitor's TTFV is 4min vs our 12min"]
- [ ] [e.g., "Build [integration] — #1 request in competitor app store reviews"]

### Strategic (3-12 months, high effort)
- [ ] [e.g., "Enter DACH market — competitor has no German localization"]
- [ ] [e.g., "Build API v2 — power users leaving competitor for API limitations"]
- [ ] [e.g., "Achieve SOC2 Type II — competitor uses this as primary enterprise objection handler"]
```

---

## Stakeholder Presentation Template

```markdown
# [COMPETITOR NAME] Teardown
## Competitive Intelligence Report — [DATE]

---

### Executive Summary (1 slide)
- Overall threat level: LOW / MEDIUM / HIGH / CRITICAL
- Their biggest strength vs. us: [1 sentence]
- Our biggest opportunity vs. them: [1 sentence]
- Recommended priority action: [1 sentence]

---

### Market Position (1 slide)
[Insert 2x2 positioning map]

---

### Feature Scorecard (1 slide)
[Insert 12-dimension radar chart or table]
Overall: [COMPETITOR] = XX/60 | [YOURS] = XX/60

---

### Pricing Analysis (1 slide)
[Insert pricing comparison table]
Key insight: [1-2 sentences]

---

### UX Highlights (1 slide)
What they do better: [3 bullets]
Where we beat them: [3 bullets]

---

### Voice of Customer (1 slide)
Top 3 complaints about [COMPETITOR] from reviews:
1. [Quote or paraphrase]
2. [Quote or paraphrase]
3. [Quote or paraphrase]

---

### Our Action Plan (1 slide)
Quick wins: [2-3 bullets]
Medium-term: [2-3 bullets]
Strategic: [1-2 bullets]

---

### Appendix
- Raw feature matrix
- Full review analysis
- Job posting breakdown
- SEO keyword comparison
```

---

## Common Pitfalls

1. **Recency bias** - Pricing pages change; always date-stamp your data
2. **Feature theater** - A competitor may list a feature that barely works; check reviews
3. **Vanity metrics** - "10,000 integrations" via Zapier != 10,000 native integrations
4. **Ignoring momentum** - A weaker competitor growing 3x YoY is a bigger threat than a stronger one shrinking
5. **Only comparing features** - Brand perception and community often matter more than features
6. **Single-source analysis** - Website alone misses the real user experience; always add reviews

---

## Best Practices

- Run teardowns quarterly; competitors move fast
- Assign a DRI (directly responsible individual) for each major competitor
- Build a "battle card" 1-pager per competitor for sales to use
- Track competitor job postings monthly as a leading indicator of product direction
- Screenshot pricing pages — they change and you want the history
- Include a "what we copied from them" section internally — intellectual honesty builds better products

---
name: social-media-analyzer
description: Analyzes social media campaign performance across platforms with engagement metrics, ROI calculations, and audience insights for data-driven marketing decisions
---

# Social Media Campaign Analyzer

This skill provides comprehensive analysis of social media campaign performance, helping marketing agencies deliver actionable insights to clients.

## Capabilities

- **Multi-Platform Analysis**: Track performance across Facebook, Instagram, Twitter, LinkedIn, TikTok
- **Engagement Metrics**: Calculate engagement rate, reach, impressions, click-through rate
- **ROI Analysis**: Measure cost per engagement, cost per click, return on ad spend
- **Audience Insights**: Analyze demographics, peak engagement times, content performance
- **Trend Detection**: Identify high-performing content types and posting patterns
- **Competitive Benchmarking**: Compare performance against industry standards

## Input Requirements

Campaign data including:
- **Platform metrics**: Likes, comments, shares, saves, clicks
- **Reach data**: Impressions, unique reach, follower growth
- **Cost data**: Ad spend, campaign budget (for ROI calculations)
- **Content details**: Post type (image, video, carousel), posting time, hashtags
- **Time period**: Date range for analysis

Formats accepted:
- JSON with structured campaign data
- CSV exports from social media platforms
- Text descriptions of key metrics

## Output Formats

Results include:
- **Performance dashboard**: Key metrics with trends
- **Engagement analysis**: Best and worst performing posts
- **ROI breakdown**: Cost efficiency metrics
- **Audience insights**: Demographics and behavior patterns
- **Recommendations**: Data-driven suggestions for optimization
- **Visual reports**: Charts and graphs (Excel/PDF format)

## How to Use

"Analyze this Facebook campaign data and calculate engagement metrics"
"What's the ROI on this Instagram ad campaign with $500 spend and 2,000 clicks?"
"Compare performance across all social platforms for the last month"

## Scripts

- `calculate_metrics.py`: Core calculation engine for all social media metrics
- `analyze_performance.py`: Performance analysis and recommendation generation

## Best Practices

1. Ensure data completeness before analysis (missing metrics affect accuracy)
2. Compare metrics within same time periods for fair comparisons
3. Consider platform-specific benchmarks (Instagram engagement differs from LinkedIn)
4. Account for organic vs. paid metrics separately
5. Track metrics over time to identify trends
6. Include context (seasonality, campaigns, events) when interpreting results

## Limitations

- Requires accurate data from social media platforms
- Industry benchmarks are general guidelines and vary by niche
- Historical data doesn't guarantee future performance
- Organic reach calculations may vary by platform algorithm changes
- Cannot access data directly from platforms (requires manual export or API integration)
- Some platforms limit data availability (e.g., TikTok analytics for business accounts only)

#!/usr/bin/env python3
"""
Example workflow demonstrating seek-and-analyze-video skill capabilities.
Shows competitive video analysis pipeline with Memories.ai LVMM.

Usage:
    python example-workflow.py --mode [quick|full]

Modes:
    quick: Run with demo data (no API calls)
    full: Execute full workflow (requires MEMORIES_API_KEY)
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List


def validate_api_key() -> bool:
    """Check if API key is configured."""
    api_key = os.getenv("MEMORIES_API_KEY")
    if not api_key:
        print("❌ MEMORIES_API_KEY not set")
        print("\nSetup instructions:")
        print("1. Visit https://memories.ai and create account")
        print("2. Get API key from dashboard")
        print("3. Run: export MEMORIES_API_KEY=your_key_here")
        return False
    return True


def demo_mode():
    """Run demonstration with mock data (no API calls)."""
    print("🎬 Running in DEMO mode (no API calls)")
    print("=" * 60)

    # Mock competitor discovery
    print("\n📍 Stage 1: Discovering competitor content...")
    mock_videos = [
        {
            "url": "https://youtube.com/watch?v=demo1",
            "title": "Competitor A - Product Demo",
            "views": 125000,
            "likes": 8500,
            "creator": "@competitor_a",
        },
        {
            "url": "https://youtube.com/watch?v=demo2",
            "title": "Competitor A - Pricing Guide",
            "views": 98000,
            "likes": 6200,
            "creator": "@competitor_a",
        },
        {
            "url": "https://youtube.com/watch?v=demo3",
            "title": "Competitor A - Customer Success Story",
            "views": 156000,
            "likes": 12000,
            "creator": "@competitor_a",
        },
    ]

    print(f"Found {len(mock_videos)} videos")
    for video in mock_videos:
        print(f"  - {video['title']} ({video['views']:,} views)")

    # Mock import
    print("\n📥 Stage 2: Importing top performers...")
    for video in mock_videos:
        mock_video_id = f"VI_{video['title'][:10].replace(' ', '_')}"
        print(f"  ✓ Imported: {video['title']} → {mock_video_id}")

    # Mock content analysis
    print("\n🔬 Stage 3: Analyzing content patterns...")
    mock_analysis = {
        "content_themes": {
            "product_demos": "60%",
            "customer_stories": "30%",
            "thought_leadership": "10%",
        },
        "average_length": "3:24",
        "hook_patterns": [
            "Here's what nobody tells you about...",
            "3 mistakes I see founders make...",
            "Watch this before choosing...",
        ],
        "posting_frequency": "2-3 videos per week (Tuesday/Thursday)",
    }

    print(json.dumps(mock_analysis, indent=2))

    # Mock messaging analysis
    print("\n💬 Stage 4: Extracting messaging...")
    mock_messaging = {
        "core_pillars": [
            "ROI in first 90 days",
            "Enterprise-grade security",
            "No-code setup",
        ],
        "pain_points_addressed": [
            "Manual workflows wasting time",
            "Security compliance complexity",
            "Integration headaches",
        ],
        "proof_elements": [
            "Customer logos (Fortune 500)",
            "ROI calculators with real data",
            "Case studies with metrics",
        ],
    }

    print(json.dumps(mock_messaging, indent=2))

    # Mock gap identification
    print("\n🎯 Stage 5: Identifying opportunities...")
    mock_gaps = {
        "uncovered_topics": [
            "Migration from legacy systems (high search volume)",
            "Team training and onboarding",
            "Advanced API usage",
        ],
        "missed_angles": [
            "Product demos focus on features, not workflows",
            "Customer stories lack technical depth",
            "No content for technical evaluators",
        ],
        "format_opportunities": [
            "Short-form TikTok/Reels (competitors use YouTube only)",
            "Live Q&A sessions (no one doing this)",
            "Comparison videos (avoided by competitors)",
        ],
    }

    print(json.dumps(mock_gaps, indent=2))

    # Mock recommendations
    print("\n📋 Stage 6: Generating recommendations...")
    mock_recommendations = {
        "quick_wins": [
            {
                "action": "Create 3 short-form product demos for TikTok/Reels",
                "rationale": "Competitors only on YouTube, capture short-form audience",
                "timeline": "2 weeks",
            },
            {
                "action": "Record migration guide video",
                "rationale": "High search demand, zero competition",
                "timeline": "1 week",
            },
        ],
        "strategic_bets": [
            {
                "action": "Launch weekly live Q&A series",
                "rationale": "Build community, no competitors doing this",
                "timeline": "Q2 2026",
            },
            {
                "action": "Create technical deep-dive series for evaluators",
                "rationale": "Gap in competitor content, address technical audience",
                "timeline": "Q2 2026",
            },
        ],
        "avoid": [
            "Generic thought leadership (saturated)",
            "Feature-focused demos without use cases (not resonating)",
        ],
        "differentiation": [
            "Lead with workflow outcomes, not features",
            "Show migration path from specific competitors",
            "Target technical evaluators ignored by competitors",
        ],
    }

    print(json.dumps(mock_recommendations, indent=2))

    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("\nTo run with real data:")
    print("1. Set MEMORIES_API_KEY environment variable")
    print("2. Run: python example-workflow.py --mode full")


def full_mode():
    """Execute full workflow with actual API calls."""
    if not validate_api_key():
        return

    print("🚀 Running FULL workflow with Memories.ai API")
    print("=" * 60)

    print("\n⚠️  This will consume API credits:")
    print("  - Discovery: ~1 credit per 10 videos")
    print("  - Import: ~5 credits per video")
    print("  - Queries: ~1-5 credits per query")
    print("\nEstimated total: ~50-100 credits")

    response = input("\nProceed? (yes/no): ").strip().lower()
    if response != "yes":
        print("Cancelled.")
        return

    print("\n📍 Stage 1: Discovering competitor content...")
    print("(Implementation would call Memories.ai API here)")

    # In real implementation, would import and use the Memories.ai client
    # from seek_and_analyze_video import search_social, import_video, chat_personal

    print("\nFull implementation requires:")
    print("1. Clone: https://github.com/kennyzheng-builds/seek-and-analyze-video")
    print("2. Import client from skill repository")
    print("3. Execute workflow with actual API calls")


def main():
    """Main entry point."""
    mode = "quick"

    # Parse arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--mode" and len(sys.argv) > 2:
            mode = sys.argv[2]
        elif sys.argv[1] in ["--help", "-h"]:
            print(__doc__)
            return

    if mode not in ["quick", "full"]:
        print(f"❌ Invalid mode: {mode}")
        print("Valid modes: quick, full")
        print("\nRun with --help for usage information")
        return

    print(f"""
╔════════════════════════════════════════════════════════════╗
║        Seek and Analyze Video - Example Workflow           ║
║                  Competitive Video Analysis                 ║
╚════════════════════════════════════════════════════════════╝

Mode: {mode.upper()}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")

    if mode == "quick":
        demo_mode()
    else:
        full_mode()


if __name__ == "__main__":
    main()

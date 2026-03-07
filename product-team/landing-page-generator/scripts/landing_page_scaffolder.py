#!/usr/bin/env python3
"""Landing Page Scaffolder — Generate responsive HTML landing pages from config.

Creates production-ready landing page HTML with hero sections, features,
testimonials, pricing, CTAs, and responsive design.

Usage:
    python landing_page_scaffolder.py config.json --output page.html
    python landing_page_scaffolder.py config.json --format json
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
import html as html_module


def escape(text: str) -> str:
    """HTML-escape text."""
    return html_module.escape(str(text))


def generate_css(config: Dict[str, Any]) -> str:
    """Generate responsive CSS from config theme."""
    theme = config.get("theme", {})
    primary = theme.get("primary_color", "#2563eb")
    secondary = theme.get("secondary_color", "#1e40af")
    bg = theme.get("background", "#ffffff")
    text_color = theme.get("text_color", "#1f2937")
    font = theme.get("font", "Inter, system-ui, -apple-system, sans-serif")

    return f"""
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: {font}; color: {text_color}; background: {bg}; line-height: 1.6; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
    
    /* Navigation */
    nav {{ padding: 16px 0; border-bottom: 1px solid #e5e7eb; position: sticky; top: 0; background: {bg}; z-index: 100; }}
    nav .container {{ display: flex; justify-content: space-between; align-items: center; }}
    .nav-logo {{ font-size: 1.5rem; font-weight: 700; color: {primary}; text-decoration: none; }}
    .nav-links {{ display: flex; gap: 24px; list-style: none; }}
    .nav-links a {{ text-decoration: none; color: {text_color}; font-weight: 500; }}
    .nav-cta {{ background: {primary}; color: white; padding: 8px 20px; border-radius: 6px; text-decoration: none; font-weight: 600; }}
    
    /* Hero */
    .hero {{ padding: 80px 0; text-align: center; }}
    .hero h1 {{ font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 24px; max-width: 800px; margin-left: auto; margin-right: auto; }}
    .hero p {{ font-size: 1.25rem; color: #6b7280; max-width: 600px; margin: 0 auto 32px; }}
    .hero-cta {{ display: inline-flex; gap: 16px; }}
    .btn-primary {{ background: {primary}; color: white; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; }}
    .btn-secondary {{ background: transparent; color: {primary}; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; border: 2px solid {primary}; }}
    
    /* Features */
    .features {{ padding: 80px 0; background: #f9fafb; }}
    .section-title {{ text-align: center; font-size: 2.5rem; font-weight: 700; margin-bottom: 16px; }}
    .section-subtitle {{ text-align: center; color: #6b7280; font-size: 1.1rem; margin-bottom: 48px; max-width: 600px; margin-left: auto; margin-right: auto; }}
    .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 32px; }}
    .feature-card {{ background: white; padding: 32px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .feature-icon {{ font-size: 2rem; margin-bottom: 16px; }}
    .feature-card h3 {{ font-size: 1.25rem; margin-bottom: 12px; }}
    .feature-card p {{ color: #6b7280; }}
    
    /* Testimonials */
    .testimonials {{ padding: 80px 0; }}
    .testimonials-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px; }}
    .testimonial-card {{ padding: 32px; border: 1px solid #e5e7eb; border-radius: 12px; }}
    .testimonial-text {{ font-size: 1.1rem; font-style: italic; margin-bottom: 20px; }}
    .testimonial-author {{ display: flex; align-items: center; gap: 12px; }}
    .author-info strong {{ display: block; }}
    .author-info span {{ color: #6b7280; font-size: 0.9rem; }}
    
    /* Pricing */
    .pricing {{ padding: 80px 0; background: #f9fafb; }}
    .pricing-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; max-width: 900px; margin: 0 auto; }}
    .pricing-card {{ background: white; padding: 32px; border-radius: 12px; border: 2px solid #e5e7eb; text-align: center; }}
    .pricing-card.featured {{ border-color: {primary}; position: relative; }}
    .pricing-card.featured::before {{ content: "Most Popular"; position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: {primary}; color: white; padding: 4px 16px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
    .pricing-name {{ font-size: 1.25rem; font-weight: 600; margin-bottom: 8px; }}
    .pricing-price {{ font-size: 3rem; font-weight: 800; margin: 16px 0; }}
    .pricing-price span {{ font-size: 1rem; font-weight: 400; color: #6b7280; }}
    .pricing-features {{ list-style: none; text-align: left; margin: 24px 0; }}
    .pricing-features li {{ padding: 8px 0; border-bottom: 1px solid #f3f4f6; }}
    .pricing-features li::before {{ content: "✓ "; color: {primary}; font-weight: 700; }}
    
    /* CTA */
    .cta-section {{ padding: 80px 0; text-align: center; background: {primary}; color: white; }}
    .cta-section h2 {{ font-size: 2.5rem; margin-bottom: 16px; }}
    .cta-section p {{ font-size: 1.1rem; opacity: 0.9; margin-bottom: 32px; }}
    .btn-white {{ background: white; color: {primary}; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; }}
    
    /* Footer */
    footer {{ padding: 40px 0; border-top: 1px solid #e5e7eb; color: #6b7280; text-align: center; }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .hero h1 {{ font-size: 2.25rem; }}
        .hero-cta {{ flex-direction: column; align-items: center; }}
        .nav-links {{ display: none; }}
        .features-grid {{ grid-template-columns: 1fr; }}
        .pricing-grid {{ grid-template-columns: 1fr; }}
    }}
    """


def render_nav(config: Dict[str, Any]) -> str:
    """Render navigation section."""
    brand = escape(config.get("brand", "Brand"))
    nav_links = config.get("nav_links", [])
    cta = config.get("nav_cta", {"text": "Get Started", "url": "#"})

    links = "\n".join(
        f'<li><a href="{escape(l.get("url", "#"))}">{escape(l.get("text", ""))}</a></li>'
        for l in nav_links
    )
    return f"""
    <nav><div class="container">
        <a href="#" class="nav-logo">{brand}</a>
        <ul class="nav-links">{links}</ul>
        <a href="{escape(cta.get('url', '#'))}" class="nav-cta">{escape(cta.get('text', 'Get Started'))}</a>
    </div></nav>"""


def render_hero(hero: Dict[str, Any]) -> str:
    """Render hero section."""
    h1 = escape(hero.get("headline", "Your Headline Here"))
    sub = escape(hero.get("subheadline", ""))
    primary_cta = hero.get("primary_cta", {"text": "Get Started", "url": "#"})
    secondary_cta = hero.get("secondary_cta", None)

    cta_html = f'<a href="{escape(primary_cta.get("url", "#"))}" class="btn-primary">{escape(primary_cta.get("text", "Get Started"))}</a>'
    if secondary_cta:
        cta_html += f'\n<a href="{escape(secondary_cta.get("url", "#"))}" class="btn-secondary">{escape(secondary_cta.get("text", "Learn More"))}</a>'

    return f"""
    <section class="hero"><div class="container">
        <h1>{h1}</h1>
        <p>{sub}</p>
        <div class="hero-cta">{cta_html}</div>
    </div></section>"""


def render_features(features: Dict[str, Any]) -> str:
    """Render features grid."""
    title = escape(features.get("title", "Features"))
    subtitle = escape(features.get("subtitle", ""))
    items = features.get("items", [])

    cards = "\n".join(f"""
        <div class="feature-card">
            <div class="feature-icon">{escape(f.get('icon', '⚡'))}</div>
            <h3>{escape(f.get('title', ''))}</h3>
            <p>{escape(f.get('description', ''))}</p>
        </div>""" for f in items)

    return f"""
    <section class="features"><div class="container">
        <h2 class="section-title">{title}</h2>
        <p class="section-subtitle">{subtitle}</p>
        <div class="features-grid">{cards}</div>
    </div></section>"""


def render_testimonials(testimonials: Dict[str, Any]) -> str:
    """Render testimonials section."""
    title = escape(testimonials.get("title", "What Our Customers Say"))
    items = testimonials.get("items", [])
    if not items:
        return ""

    cards = "\n".join(f"""
        <div class="testimonial-card">
            <p class="testimonial-text">"{escape(t.get('quote', ''))}"</p>
            <div class="testimonial-author">
                <div class="author-info">
                    <strong>{escape(t.get('name', ''))}</strong>
                    <span>{escape(t.get('title', ''))}, {escape(t.get('company', ''))}</span>
                </div>
            </div>
        </div>""" for t in items)

    return f"""
    <section class="testimonials"><div class="container">
        <h2 class="section-title">{title}</h2>
        <div class="testimonials-grid">{cards}</div>
    </div></section>"""


def render_pricing(pricing: Dict[str, Any]) -> str:
    """Render pricing section."""
    title = escape(pricing.get("title", "Pricing"))
    plans = pricing.get("plans", [])
    if not plans:
        return ""

    cards = "\n".join(f"""
        <div class="pricing-card {'featured' if p.get('featured') else ''}">
            <div class="pricing-name">{escape(p.get('name', ''))}</div>
            <div class="pricing-price">${escape(str(p.get('price', '0')))}<span>/mo</span></div>
            <p>{escape(p.get('description', ''))}</p>
            <ul class="pricing-features">
                {"".join(f'<li>{escape(f)}</li>' for f in p.get('features', []))}
            </ul>
            <a href="{escape(p.get('cta_url', '#'))}" class="btn-primary">{escape(p.get('cta_text', 'Choose Plan'))}</a>
        </div>""" for p in plans)

    return f"""
    <section class="pricing"><div class="container">
        <h2 class="section-title">{title}</h2>
        <div class="pricing-grid">{cards}</div>
    </div></section>"""


def render_cta(cta: Dict[str, Any]) -> str:
    """Render CTA section."""
    return f"""
    <section class="cta-section"><div class="container">
        <h2>{escape(cta.get('headline', 'Ready to get started?'))}</h2>
        <p>{escape(cta.get('subheadline', ''))}</p>
        <a href="{escape(cta.get('url', '#'))}" class="btn-white">{escape(cta.get('text', 'Start Free Trial'))}</a>
    </div></section>"""


def generate_html(config: Dict[str, Any]) -> str:
    """Generate complete HTML landing page."""
    title = escape(config.get("title", "Landing Page"))
    css = generate_css(config)
    sections = []

    sections.append(render_nav(config))
    if config.get("hero"):
        sections.append(render_hero(config["hero"]))
    if config.get("features"):
        sections.append(render_features(config["features"]))
    if config.get("testimonials"):
        sections.append(render_testimonials(config["testimonials"]))
    if config.get("pricing"):
        sections.append(render_pricing(config["pricing"]))
    if config.get("cta"):
        sections.append(render_cta(config["cta"]))

    sections.append(f"""
    <footer><div class="container">
        <p>{escape(config.get('footer_text', f'© {datetime.now().year} {config.get("brand", "Company")}. All rights reserved.'))}</p>
    </div></footer>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{escape(config.get('meta_description', ''))}">
    <style>{css}</style>
</head>
<body>
{"".join(sections)}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate responsive landing page from config")
    parser.add_argument("input", help="Path to page config JSON")
    parser.add_argument("--format", choices=["html", "json"], default="html", help="Output format")
    parser.add_argument("--output", type=str, default=None, help="Output file path")

    args = parser.parse_args()

    with open(args.input) as f:
        config = json.load(f)

    if args.format == "json":
        output = json.dumps({
            "generated_at": datetime.now().isoformat(),
            "config": config,
            "html_length": len(generate_html(config)),
            "sections": [k for k in ["nav", "hero", "features", "testimonials", "pricing", "cta", "footer"] if config.get(k) or k in ("nav", "footer")]
        }, indent=2)
    else:
        output = generate_html(config)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Landing page written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()

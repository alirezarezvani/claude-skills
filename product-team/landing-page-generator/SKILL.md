# Landing Page Generator

**Tier:** POWERFUL  
**Category:** Product Team  
**Domain:** Marketing / Conversion Rate Optimization

---

## Overview

Generate high-converting landing pages from a product description. Output complete Next.js/React components with multiple section variants, proven copy frameworks, SEO optimization, and performance-first patterns. Not lorem ipsum — actual copy that converts.

**Target:** LCP < 1s · CLS < 0.1 · FID < 100ms  
**Output:** TSX components + Tailwind styles + SEO meta + copy variants

---

## Core Capabilities

- 5 hero section variants (centered, split, gradient, video-bg, minimal)
- Feature sections (grid, alternating, cards with icons)
- Pricing tables (2–4 tiers with feature lists and toggle)
- FAQ accordion with schema markup
- Testimonials (grid, carousel, single-quote)
- CTA sections (banner, full-page, inline)
- Footer (simple, mega, minimal)
- 4 design styles with Tailwind class sets

---

## When to Use

- Launching a new product or feature
- Creating a dedicated campaign or promo page
- A/B testing landing page variants
- Replacing a static page with a conversion-optimized one

---

## Triggering This Skill

```
Product: [name]
Tagline: [one sentence value prop]
Target audience: [who they are]
Key pain point: [what problem you solve]
Key benefit: [primary outcome]
Pricing tiers: [free/pro/enterprise or describe]
Design style: dark-saas | clean-minimal | bold-startup | enterprise
Copy framework: PAS | AIDA | BAB
```

---

## Design Style Reference

### Dark SaaS
```css
/* Tailwind classes */
bg-gray-950 text-white
accent: violet-500, violet-400
cards: bg-gray-900 border border-gray-800
CTA button: bg-violet-600 hover:bg-violet-500
```

### Clean Minimal
```css
bg-white text-gray-900
accent: blue-600
cards: bg-gray-50 border border-gray-200 rounded-2xl
CTA button: bg-blue-600 hover:bg-blue-700
```

### Bold Startup
```css
bg-white text-gray-900
accent: orange-500
headings: font-black tracking-tight
cards: shadow-xl rounded-3xl
CTA button: bg-orange-500 hover:bg-orange-600 text-white
```

### Enterprise
```css
bg-slate-50 text-slate-900
accent: slate-700
cards: bg-white border border-slate-200 shadow-sm
CTA button: bg-slate-900 hover:bg-slate-800 text-white
```

---

## Copy Frameworks

### PAS (Problem → Agitate → Solution)
```
HERO HEADLINE: [Painful state they're in]
SUBHEAD: [Agitate: what happens if they don't fix it]
CTA: [Solution: what you offer]

Example:
H1: "Your team wastes 3 hours a day on manual reporting"
Sub: "Every hour spent on spreadsheets is an hour not closing deals. 
      Your competitors are already automated."
CTA: "Automate your reports in 10 minutes →"
```

### AIDA (Attention → Interest → Desire → Action)
```
H1: [Bold attention-grabbing statement]
Sub: [Interesting fact or benefit]
Features: [Desire-building proof points]
CTA: [Clear action]
```

### BAB (Before → After → Bridge)
```
H1: "[Before state] → [After state]"
Sub: "Here's how [product] bridges the gap"
Features: [Bridge: how it works]
```

---

## Hero Variants

### Variant 1: Centered Gradient (Dark SaaS)
```tsx
export function HeroCentered() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-gray-950 px-4 text-center">
      <div className="absolute inset-0 bg-gradient-to-b from-violet-900/20 to-transparent" />
      <div className="pointer-events-none absolute -top-40 left-1/2 h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-violet-600/20 blur-3xl" />
      <div className="relative z-10 max-w-4xl">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-sm text-violet-300">
          <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
          Now in public beta
        </div>
        <h1 className="mb-6 text-5xl font-bold tracking-tight text-white md:text-7xl">
          Ship faster.<br />
          <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">
            Break less.
          </span>
        </h1>
        <p className="mx-auto mb-10 max-w-2xl text-xl text-gray-400">
          The deployment platform that catches errors before your users do.
          Zero config. Instant rollbacks. Real-time monitoring.
        </p>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Button size="lg" className="bg-violet-600 text-white hover:bg-violet-500 px-8">
            Start free trial
          </Button>
          <Button size="lg" variant="outline" className="border-gray-700 text-gray-300">
            See how it works →
          </Button>
        </div>
        <p className="mt-4 text-sm text-gray-500">No credit card required · 14-day free trial</p>
      </div>
    </section>
  )
}
```

### Variant 2: Split (Image + Copy)
```tsx
export function HeroSplit() {
  return (
    <section className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
      <div className="flex flex-col justify-center px-8 py-20 lg:px-16">
        <h1 className="mb-6 text-5xl font-black text-gray-900 lg:text-6xl">
          Stop losing customers to slow support
        </h1>
        <p className="mb-8 text-xl text-gray-600">
          Respond to every ticket in under 2 minutes with AI-powered triage,
          smart routing, and one-click replies.
        </p>
        <div className="flex gap-4">
          <Button size="lg" className="bg-blue-600 text-white">Get started free</Button>
          <Button size="lg" variant="ghost">Watch demo</Button>
        </div>
        <div className="mt-10 flex items-center gap-8 text-sm text-gray-500">
          <span>✓ 14-day trial</span>
          <span>✓ No credit card</span>
          <span>✓ Cancel anytime</span>
        </div>
      </div>
      <div className="relative hidden bg-blue-50 lg:block">
        <Image src="/hero-screenshot.png" fill className="object-cover object-left" alt="Product screenshot" />
      </div>
    </section>
  )
}
```

---

## Feature Section: Alternating

```tsx
const features = [
  {
    title: "Real-time error tracking",
    description: "Catch exceptions the moment they happen. Stack traces, user context, and breadcrumbs — all in one place.",
    image: "/features/errors.png",
    badge: "Core",
  },
  {
    title: "One-click rollback",
    description: "Bad deploy? Roll back to any previous version in under 30 seconds without touching your terminal.",
    image: "/features/rollback.png",
    badge: "New",
  },
]

export function FeaturesAlternating() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-6xl px-4">
        {features.map((feature, i) => (
          <div key={feature.title} className={`flex flex-col gap-12 py-16 lg:flex-row lg:items-center ${i % 2 === 1 ? "lg:flex-row-reverse" : ""}`}>
            <div className="flex-1">
              <span className="mb-3 inline-block rounded-full bg-blue-100 px-3 py-1 text-xs font-medium text-blue-700">
                {feature.badge}
              </span>
              <h3 className="mb-4 text-3xl font-bold text-gray-900">{feature.title}</h3>
              <p className="text-lg text-gray-600">{feature.description}</p>
            </div>
            <div className="flex-1">
              <Image src={feature.image} width={600} height={400} className="rounded-2xl shadow-xl" alt={feature.title} />
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}
```

---

## Pricing Section

```tsx
const plans = [
  {
    name: "Starter",
    price: 0,
    description: "For solo developers",
    features: ["5 projects", "10k events/month", "7-day retention", "Email support"],
    cta: "Get started free",
    highlighted: false,
  },
  {
    name: "Pro",
    price: 49,
    description: "For growing teams",
    features: ["Unlimited projects", "1M events/month", "90-day retention", "Priority support", "Custom alerts", "SSO"],
    cta: "Start free trial",
    highlighted: true,
  },
  {
    name: "Enterprise",
    price: null,
    description: "For large organizations",
    features: ["Everything in Pro", "Unlimited events", "SLA guarantee", "Dedicated support", "Custom contracts", "SAML/SCIM"],
    cta: "Contact sales",
    highlighted: false,
  },
]

export function Pricing() {
  return (
    <section className="py-24 bg-gray-950">
      <div className="mx-auto max-w-6xl px-4">
        <h2 className="mb-4 text-center text-4xl font-bold text-white">Simple, predictable pricing</h2>
        <p className="mb-16 text-center text-gray-400">Start free. Scale as you grow.</p>
        <div className="grid gap-8 lg:grid-cols-3">
          {plans.map((plan) => (
            <div key={plan.name} className={`rounded-2xl p-8 ${plan.highlighted ? "border-2 border-violet-500 bg-violet-950/50 ring-4 ring-violet-500/20" : "border border-gray-800 bg-gray-900"}`}>
              {plan.highlighted && (
                <div className="mb-4 inline-block rounded-full bg-violet-500 px-3 py-1 text-xs font-bold text-white">Most popular</div>
              )}
              <h3 className="text-xl font-bold text-white">{plan.name}</h3>
              <p className="mt-1 text-sm text-gray-400">{plan.description}</p>
              <div className="my-6">
                {plan.price !== null ? (
                  <span className="text-4xl font-black text-white">${plan.price}<span className="text-lg font-normal text-gray-400">/mo</span></span>
                ) : (
                  <span className="text-2xl font-bold text-white">Custom</span>
                )}
              </div>
              <ul className="mb-8 space-y-3 text-sm text-gray-300">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2">
                    <Check className="h-4 w-4 text-violet-400 shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
              <Button className={`w-full ${plan.highlighted ? "bg-violet-600 hover:bg-violet-500 text-white" : "border border-gray-700 bg-transparent text-white hover:bg-gray-800"}`}>
                {plan.cta}
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
```

---

## FAQ with Schema Markup

```tsx
const faqs = [
  { q: "Do I need a credit card to start?", a: "No. Your free trial runs for 14 days with no credit card required." },
  { q: "Can I change plans later?", a: "Yes. Upgrade or downgrade at any time. Changes apply at the next billing cycle." },
]

export function FAQ() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map(({ q, a }) => ({
      "@type": "Question",
      name: q,
      acceptedAnswer: { "@type": "Answer", text: a },
    })),
  }

  return (
    <section className="py-24">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
      <div className="mx-auto max-w-3xl px-4">
        <h2 className="mb-12 text-center text-4xl font-bold">Frequently asked questions</h2>
        <Accordion type="single" collapsible className="space-y-4">
          {faqs.map(({ q, a }) => (
            <AccordionItem key={q} value={q} className="rounded-xl border px-6">
              <AccordionTrigger className="text-left font-semibold">{q}</AccordionTrigger>
              <AccordionContent className="text-gray-600">{a}</AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  )
}
```

---

## SEO Checklist

- [ ] `<title>` tag: primary keyword + brand (50–60 chars)
- [ ] Meta description: benefit + CTA (150–160 chars)
- [ ] OG image: 1200×630px with product name and tagline
- [ ] H1: one per page, includes primary keyword
- [ ] Structured data: FAQPage, Product, or Organization schema
- [ ] Canonical URL set
- [ ] Image alt text on all `<Image>` components
- [ ] robots.txt and sitemap.xml configured
- [ ] Core Web Vitals: LCP < 1s, CLS < 0.1
- [ ] Mobile viewport meta tag present
- [ ] Internal linking to pricing and docs

---

## Performance Targets

| Metric | Target | Technique |
|---|---|---|
| LCP | < 1s | Preload hero image, use `priority` on Next/Image |
| CLS | < 0.1 | Set explicit width/height on all images |
| FID/INP | < 100ms | Defer non-critical JS, use `loading="lazy"` |
| TTFB | < 200ms | Use ISR or static generation for landing pages |
| Bundle | < 100KB JS | Audit with `@next/bundle-analyzer` |

---

## Common Pitfalls

- Hero image not preloaded — add `priority` prop to first `<Image>`
- Missing mobile breakpoints — always design mobile-first with `sm:` prefixes
- CTA copy too vague — "Get started" beats "Learn more"; "Start free trial" beats "Sign up"
- Pricing page missing trust signals — add money-back guarantee and testimonials near CTA
- No above-the-fold CTA on mobile — ensure button is visible without scrolling on 375px viewport

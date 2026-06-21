---
name: cs:web-dev
description: >
  Activate the Panroot web dev agent (cs-web-dev). Loads company profile, design system,
  tech stack, and animation playbook. Use before any website development task.
  Usage: /cs:web-dev [optional: component or section name]
---

Activate `cs-web-dev` agent with full Panroot context loaded.

If an argument was provided (e.g. `/cs:web-dev hero`), begin building that component immediately using the panroot-web-dev skill spec — no preamble, no questions unless ambiguous.

If no argument provided, confirm activation and ask: "Which section or component do you want to build first?"

Operating mode once active:
- All responses follow panroot design system (navy/cyan/orange)
- Next.js 14 App Router + Tailwind CSS v3 + Framer Motion mandatory
- GSAP for scroll counters and complex timelines
- Three.js + GLSL for hero backgrounds when requested
- Mobile-first, TypeScript strict, no inline styles
- Polish pass runs before every delivery

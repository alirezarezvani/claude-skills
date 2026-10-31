# Unfinished work and template defaults

`finish_lint.py` separates two kinds of findings, and the separation is the
point of the design:

- **Unfinished work blocks.** A handler that does nothing, a link to `#`,
  "Lorem ipsum" on screen, or a removed focus ring is a defect, whatever the
  brief says.
- **Template defaults only warn.** A purple gradient or a row of identical
  cards is a choice. It is wrong only when nobody made it. The brief may ask
  for exactly that look, and then it is right.

Confidence markers: 🟢 a standard or the source's own words · 🟡 widely
documented practice · 🔴 opinion, labelled as such.

## Unfinished work (blocking)

| Code | Pattern | Why it ships |
|---|---|---|
| `INERT_HANDLER` | `onClick={() => {}}`, `onClick={undefined}`, a handler that only logs or alerts, `@click=""`, `TODO` inside the handler | Scaffolding that a generated or hurried screen leaves behind. It looks finished in every screenshot. |
| `DEAD_LINK` | `<a href="#">`, `href=""`, `href="javascript:…"` with no handler | The same thing for links. If it performs an action it should be a `<button>`. |
| `PLACEHOLDER_COPY` | lorem ipsum, TODO, TBD, `[Insert …]`, "your text here", `$XX`, "Coming soon" | Copy is written last and often not at all. Empty and error states are where it usually survives. |
| `FOCUS_REMOVED` | `outline: none` or `outline-none` with no `:focus-visible`, ring or box-shadow replacement | Removing the default ring "because it looks ugly" is the commonest way to fail WCAG 2.4.7. 🟢 |
| `BUTTON_NO_ACTION` (HIGH) | `<button>` with no handler, no submit/reset type and no enclosing form | Often wired elsewhere (a ref, a parent handler), so it is HIGH, not BLOCKER. Suppress it with a reason when it is. |

Suppress one line when it is intentional:
`{/* design-qa: allow PLACEHOLDER_COPY (legal copy pending, ticket LEG-12) */}`.
Use a reason a reviewer can check. A suppression without one is a defect deferred.

## Template defaults (warn only)

Anthropic's `frontend-design` skill lists the traits that AI-generated design
clusters around today. The list is useful because it names concrete
defaults, not because those defaults are bad. 🟢 (the source's own list)

1. A warm cream background with a high-contrast serif and a terracotta accent.
2. A near-black background with a single acid-green or vermilion accent.
3. A broadsheet layout with hairline rules and zero border radius.
4. **The SaaS card kit**: content chopped into identical rounded cards, one radius
   everywhere, the same soft grey shadow (`rgba(0,0,0,.1)`), and gradient
   washes as decoration.
5. **Template chrome**: a tracked-out ALL-CAPS eyebrow above every heading,
   meta strings joined with middle dots, "WORD — fragment" labels, `#111` for
   black, a monospace face for small labels, and `→` appended to links and buttons.

The same source also names the motion and layout defaults: a fade-and-slide-up
on every section and a hover transition on every card "read as AI-generated";
numbered `01 / 02 / 03` markers are right only for real sequences; and "a big
number with a small label, supporting stats, and a gradient accent is the
default" hero. 🟢

What the linter detects mechanically (each trait is one `TEMPLATE_DEFAULT`
warning, so the count means something):

| Trait key | Detected from |
|---|---|
| `gradient_wash` | Tailwind `from-/via-/to-` in the purple, violet, indigo, fuchsia and pink families; CSS gradients with those colours |
| `card_kit` | `rounded-xl/2xl/3xl` with `shadow-md/lg/xl`; `box-shadow … rgba(0,0,0,.1)` |
| `eyebrow_caps` | `uppercase` with `tracking-wide/wider/widest`, or `text-transform: uppercase` with `letter-spacing` |
| `arrow_suffix` | `→` before a closing tag |
| `middot_meta` | two or more ` · ` separators in one text run |
| `numbered_markers` | `01`, `02`, `03` as standalone text |
| `entrance_motion` | `fade-in-up`, `data-aos="fade-up"`, Framer `initial={{ opacity: 0, y: … }}` |
| `hover_lift` | `hover:-translate-y-*`, `hover:scale-102…105` |
| `hero_cliche` | "unlock the power", "supercharge", "revolutionise", "seamless", "elevate your", "next-gen", "all-in-one", "effortless" |

`generic_risk` is LOW (0–1 traits), MEDIUM (2–3) or HIGH (4 or more). 🔴 The
thresholds are a convention for this skill, not research. They tell you when
to stop and ask whether anyone chose this look, nothing more.

**What to do with a HIGH:** compare it with the brief. If the brief asks for the
look, record that in the sign-off and move on. If it does not, pick one
trait and replace it with a choice specific to the subject, such as the
product's own data, its users' vocabulary or a real photograph. Changing one
deliberate thing beats sanding down nine. 🔴

## Token drift (warn)

Many distinct raw hex values in component files (outside files named
`tokens`, `theme`, `colors` or `tailwind.config`) mean the screen has drifted
from the design system. The default limit is 12, which is roughly a neutral
ramp plus brand and semantic colours. Raise it with `--max-raw-colors` for
illustration-heavy pages. 🔴 Refactoring UI makes the underlying point: define
the palette first, including about 8–10 shades per colour, and pick from it
rather than inventing values per screen. 🟡

## Sources

1. Anthropic, `frontend-design` skill, `SKILL.md` (anthropics/skills, main branch, read 2026-10-30): the five trait clusters, the motion and hero defaults, and the error and empty-state guidance quoted above. https://github.com/anthropics/skills/tree/main/skills/frontend-design
2. W3C, *WCAG 2.2*, SC 2.4.7 Focus Visible, and *Understanding 2.4.7* failure F78 (styling that removes or obscures the focus indicator). https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
3. Wathan, A. & Schoger, S. (2018). *Refactoring UI*: "Define your shades up front", limited palettes and system-first spacing. https://www.refactoringui.com/
4. Nielsen Norman Group, *Aesthetic-Usability Effect* (Moran, 2017): why a polished but generic screen gets an easy pass in review. https://www.nngroup.com/articles/aesthetic-usability-effect/
5. MDN Web Docs, `:focus-visible`: the replacement pattern for removed outlines. https://developer.mozilla.org/en-US/docs/Web/CSS/:focus-visible
6. GitHub issue #962 in this repository: the community request for a rendered-UI finish gate (generic AI UI, missing states, inert controls), which this skill answers. https://github.com/alirezarezvani/claude-skills/issues/962

# Interaction states: what each surface owes the user

`state_matrix_checker.py` derives the required states from what a surface *is*.
This file explains each requirement, why the blocking ones block, and what
"done" looks like for each.

Confidence markers: 🟢 standard or primary design-system documentation ·
🟡 well-replicated research or guidance · 🔴 practitioner convention.

## Why states, not screens

Design review shows the populated, happy-path frame. Users meet the others:
the first visit (empty), the slow network (loading), the failed request
(error), the 400-character company name (long content). Nielsen's first
heuristic, *visibility of system status*, and his ninth, *help users recognise,
diagnose and recover from errors*, are about exactly these frames. 🟡

A state is **done** when it is designed, built and evidenced: a screenshot,
a Storybook story or a test that renders it. "We'll handle it" is MISSING.

## Required states by kind

| Kind | States (blocking in bold) | Why the bold ones block |
|---|---|---|
| `data_view` | **loading**, **empty**, **error**, populated, long_content | Data arrives late, arrives empty, and fails. Each happens in production on day one. |
| `form` | default, **focus_visible**, **validation_error**, **submitting**, success, **server_error** | Without submitting, users double-submit; without server_error, a failed save loses the input. |
| `action` | default, hover, **focus_visible**, disabled, **busy**, **failure** | Async actions fail. Silence after a click is read as "broken". |
| `control` | default, hover, **focus_visible**, active, disabled | Keyboard users need to see where they are (WCAG 2.4.7). 🟢 |
| `media` | loading, **error**, populated | A broken image icon is the most visible unfinished state there is. |
| `page` | **narrow_320**, wide_1440, long_content | Reflow at 320 CSS px is WCAG 1.4.10 AA. 🟢 |

Add product-specific states with `--require kind:state`, for example
`--require data_view:offline` for a field app or `--require page:dark` when
dark mode ships.

## What good looks like

- **Loading.** Show the layout that will appear, with skeletons sized like the
  content, once the wait passes about one second. Under about 0.1 s, show
  nothing. Past about 10 s, show progress and let the user do something else.
  These are Nielsen's response-time limits (1993), which are still the cited baseline. 🟡
- **Empty.** Say why the area is empty and give the next action ("No invoices
  yet. Create your first invoice"). Separate *first use*, *no results for this
  filter* and *cleared by the user*: they need different copy. 🟡
- **Error.** Say what happened and what to do, in the interface's voice.
  Errors don't apologise, and they are never vague about what happened. Keep
  the user's input. Put field errors next to the field, and add a summary at
  the top for long forms (the GOV.UK error-summary pattern). 🟢 for the GOV.UK pattern, 🟡 for the copy guidance.
- **Disabled.** A disabled control needs a visible reason close to it, or it
  should not be disabled. Material 3 renders disabled content at 38% opacity,
  which is exempt from contrast rules and therefore often unreadable. Say why
  next to it. 🟢 for the M3 value, 🔴 for the advice.
- **Busy / submitting.** Disable the trigger *and* show progress in place
  ("Sending…"). Keep the control's width stable so the layout does not jump. 🔴
- **Long content.** Test with the longest real value (a German compound word, a
  500-row table, a 3-line product name). Wrap by default; truncate only with an
  ellipsis and a way to read the whole value. `rendered_audit.py` flags text
  that is clipped without an ellipsis. 🔴
- **Hover, focus, pressed.** Material 3 models these as *state layers*: an overlay
  with fixed opacity over the component, so every component gets them the same
  way. Whatever system you use, focus must not depend on hover. 🟢

## Evidence that holds up

| Evidence | Good for | Note |
|---|---|---|
| Screenshot path (`shots/list-empty.png`) | Every state | Use `--evidence-root` to verify the file exists. |
| Storybook story (`story:InvoiceList/Empty`) | Component states | Stories double as visual regression baselines. |
| Test name (`test:list shows empty state`) | Behaviour (submitting, failure) | Proves it works, not that it looks right. |
| Rendered snapshot (`snap:list-empty-320.json`) | Contrast, focus, reflow in that state | Run `rendered_audit.py` on it. |

## Sources

1. Nielsen, J. (1994, updated 2020/2024). *10 Usability Heuristics for User Interface Design*. Nielsen Norman Group. Heuristic 1, visibility of system status; heuristic 9, error recovery. https://www.nngroup.com/articles/ten-usability-heuristics/
2. Nielsen, J. (1993). *Usability Engineering*, ch. 5, and *Response Times: The 3 Important Limits* (NN/g). The 0.1 s, 1 s and 10 s limits. https://www.nngroup.com/articles/response-times-3-important-limits/
3. Google, *Material Design 3: States*: state layers for hover, focus, pressed and dragged, and the disabled opacity values. https://m3.material.io/foundations/interaction/states/overview
4. GOV.UK Design System, *Error message* and *Error summary* components: placement, wording and the summary-plus-inline pattern. https://design-system.service.gov.uk/components/error-summary/
5. Nielsen Norman Group, *Designing Empty States in Complex Applications* (Kaley, 2018): first-use, no-results and cleared states. https://www.nngroup.com/articles/empty-state-interface-design/
6. Anthropic, `frontend-design` skill (anthropics/skills): "Treat failure and emptiness as moments for direction, not mood… Errors don't apologize, and they are never vague about what happened. An empty screen is an invitation to act." https://github.com/anthropics/skills/tree/main/skills/frontend-design
7. W3C, *WCAG 2.2*, SC 1.4.10 Reflow and 2.4.7 Focus Visible: the two states that are also conformance requirements. https://www.w3.org/TR/WCAG22/

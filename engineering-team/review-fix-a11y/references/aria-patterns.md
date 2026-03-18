# ARIA Patterns Reference

Full patterns: [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

## Core Roles

| Role | Use for | Key attributes |
|------|---------|---------------|
| `dialog` | Modal dialogs | `aria-modal`, `aria-labelledby`, `aria-describedby` |
| `alertdialog` | Alert dialogs requiring response | Same as dialog |
| `alert` | Urgent status messages | Auto-announced; no focus needed |
| `status` | Non-urgent status messages | Polite live region |
| `tablist` | Tab container | — |
| `tab` | Individual tab | `aria-selected`, `aria-controls` |
| `tabpanel` | Tab content panel | `aria-labelledby` |
| `menu` | Navigation/action menu | — |
| `menuitem` | Menu item | — |
| `combobox` | Combo input + listbox | `aria-expanded`, `aria-controls`, `aria-activedescendant` |
| `listbox` | List of options | — |
| `option` | Listbox option | `aria-selected` |
| `tree` | Tree widget | — |
| `treeitem` | Tree node | `aria-expanded`, `aria-level` |
| `grid` | Interactive grid | — |
| `gridcell` | Grid cell | — |
| `tooltip` | Tooltip | Triggered by focus/hover |
| `progressbar` | Progress indicator | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| `slider` | Range slider | `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |
| `spinbutton` | Number spinner | Same as slider |
| `switch` | Toggle (on/off) | `aria-checked` |
| `checkbox` | Checkbox | `aria-checked` (true/false/mixed) |
| `radio` | Radio button | `aria-checked` |
| `radiogroup` | Radio group | `aria-labelledby` |

## Live Regions

```html
<!-- Polite: announced after current speech -->
<div aria-live="polite" aria-atomic="true">
  <!-- Update this content to announce status -->
</div>

<!-- Assertive: interrupts immediately (use sparingly) -->
<div aria-live="assertive" role="alert">
  <!-- Errors, critical alerts -->
</div>

<!-- Loading state -->
<div aria-busy="true" aria-live="polite">
  Loading results...
</div>
```

**Rules:**
- Set `aria-live` on the container **before** content is injected (at page load)
- `aria-atomic="true"` announces the whole region on any change
- Prefer `aria-live="polite"` — `"assertive"` interrupts and should only be used for errors

## Focus Management

```js
// Move focus to dialog on open
function openModal(modalEl, triggerEl) {
  modalEl.removeAttribute('hidden');
  modalEl.focus();         // dialog element itself (tabindex="-1")
  trapFocus(modalEl);
  modalEl._trigger = triggerEl;
}

// Return focus on close
function closeModal(modalEl) {
  modalEl.setAttribute('hidden', '');
  modalEl._trigger?.focus();
}

// Simple focus trap
function trapFocus(el) {
  const focusable = el.querySelectorAll(
    'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  el.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus(); }
    } else {
      if (document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
}
```

## Common Keyboard Patterns

| Widget | Keys |
|--------|------|
| Button | Enter, Space |
| Link | Enter |
| Checkbox | Space |
| Radio group | Arrow keys to select within group; Tab to move between groups |
| Tab list | Arrow keys to switch tabs; Enter/Space to activate |
| Menu | Arrow keys to navigate; Enter/Space to select; Escape to close |
| Dialog | Escape to close; Tab/Shift+Tab within trap |
| Combobox | Down arrow to open; Arrow keys in list; Enter to select; Escape to close |
| Tree | Arrow keys for expand/collapse and move |

## `aria-labelledby` vs `aria-label` vs `aria-describedby`

| Attribute | Purpose | Priority |
|-----------|---------|----------|
| `aria-labelledby` | Points to element(s) that name this component | Highest — overrides visible text |
| `aria-label` | Inline string label (use when no visible label exists) | High |
| `aria-describedby` | Points to supplemental description (e.g. error, hint) | Additive |

**Rule of thumb**: prefer `aria-labelledby` referencing visible text → `aria-label` for invisible label → `aria-describedby` for hints/errors.

## Do's and Don'ts

| Do | Don't |
|----|-------|
| Use semantic HTML first | Add `role="button"` to `<button>` |
| Give every interactive element an accessible name | `aria-hidden="true"` on focusable elements |
| Keep `aria-expanded` / `aria-selected` in sync with UI | Override browser semantics needlessly |
| Use `inert` to hide inactive panels | Leave multiple `aria-live` regions for one update |
| Test with real screen readers | Trust automated tools alone |
